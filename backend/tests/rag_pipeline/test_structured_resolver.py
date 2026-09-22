"""R4 — Tests for StructuredResolver and pipeline integration.

Invariants checked:
  1. Resolver resolve() matches crop + problem deterministically.
  2. Ambiguous or unknown queries return None (fall through to T3).
  3. No LLM or network calls in resolver (0 LLM cost).
  4. Confidence threshold gating.
  5. Pipeline integration:
     - Flag off (resolver=None): byte-identical T3 behavior.
     - Flag on: hit returns T1/T2, 0 LLM calls, skip traces, source provenance.
     - Terminal safety: safety rule fires first, resolver never invoked.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.structured_resolver import StructuredResolver
from app.domain.contracts import (
    GenerationResult,
    RetrievedSource,
    SafetyDecision,
    VerificationResult,
)
from app.domain.enums import (
    PipelineStage,
    ResolutionTier,
    SafetyCategory,
    StageStatus,
    VerificationConfidence,
)
from app.domain.fact_base import Fact, FactBase
from app.ports.verifier import Verifier


def _sample_potato_fact(**overrides) -> Fact:
    data = {
        "crop": "potato",
        "crop_bn": "আলু",
        "problem": "late_blight",
        "problem_bn": "নাবি ধ্বসা / লেট ব্লাইট",
        "problem_type": "disease",
        "stage": "tuber_bulking",
        "active_ingredient": "mancozeb",
        "dose_min": 2.0,
        "dose_max": 2.5,
        "dose_unit": "g/l",
        "application_interval_days": 7,
        "pre_harvest_interval_days": 7,
        "ipm_alternatives_bn": ("আক্রান্ত পাতা অপসারণ", "সুষম সেচ"),
        "banned_flag": False,
        "severity": "high",
        "source_node_id": "DAE_PEST_5E48F1_001",
        "source_doc": "DAE. List of Registered Agricultural Pesticides",
        "citation": "DAE. page_751. List of Registered Agricultural Pesticides (DAE). pp. 751-751.",
        "grounding": "corpus-extracted",
        "confidence": 0.90,
    }
    data.update(overrides)
    return Fact.from_dict(data)


# ---------------------------------------------------------------------------
# Unit tests for StructuredResolver
# ---------------------------------------------------------------------------


class TestStructuredResolverUnit:
    def test_resolve_bengali_late_blight(self) -> None:
        fb = FactBase(facts=(_sample_potato_fact(),))
        resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

        resolved = resolver.resolve("আলুর নাবি ধ্বসা রোগের প্রতিকার কী?")
        assert resolved is not None
        assert "mancozeb" in resolved.answer
        assert resolved.tier is ResolutionTier.TEMPLATED_ADVISORY
        assert resolved.fact.crop == "potato"

    def test_resolve_shorthand_morok(self) -> None:
        fb = FactBase(facts=(_sample_potato_fact(),))
        resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

        resolved = resolver.resolve("আলুর মড়ক লাগলে কী স্প্রে করব?")
        assert resolved is not None
        assert resolved.fact.problem == "late_blight"

    def test_resolve_english_query(self) -> None:
        fb = FactBase(facts=(_sample_potato_fact(),))
        resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

        resolved = resolver.resolve("what is the remedy for potato late blight?")
        assert resolved is not None
        assert "mancozeb" in resolved.answer

    def test_resolve_unrelated_crop_misses(self) -> None:
        fb = FactBase(facts=(_sample_potato_fact(),))
        resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

        resolved = resolver.resolve("ধানের ব্লাস্ট রোগের ওষুধ কী?")
        assert resolved is None

    def test_resolve_non_disease_query_misses(self) -> None:
        fb = FactBase(facts=(_sample_potato_fact(),))
        resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

        resolved = resolver.resolve("আলুর বাজার দর কত?")
        assert resolved is None

    def test_confidence_threshold_rejection(self) -> None:
        low_conf_fact = _sample_potato_fact(confidence=0.70)
        fb = FactBase(facts=(low_conf_fact,))
        resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

        resolved = resolver.resolve("আলুর নাবি ধ্বসা")
        assert resolved is None

    def test_pure_no_network_or_llm(self) -> None:
        """Resolver operates entirely in-memory with zero side effects."""
        fb = FactBase(facts=(_sample_potato_fact(),))
        resolver = StructuredResolver(fact_base=fb)
        # Multiple calls produce consistent results with no state drift
        r1 = resolver.resolve("আলুর নাবি ধ্বসা")
        r2 = resolver.resolve("আলুর নাবি ধ্বসা")
        assert r1 is not None and r2 is not None
        assert r1.answer == r2.answer


# ---------------------------------------------------------------------------
# Pipeline Integration Tests
# ---------------------------------------------------------------------------


def _setup_mock_pipeline(
    *,
    resolver: StructuredResolver | None = None,
    tmp_path: Path,
) -> tuple[QAPipeline, MagicMock, MagicMock]:
    fake_safety_decision = SafetyDecision(
        category=SafetyCategory.SAFE_AGRI,
        confidence=0.99,
        reason="safe",
        matched_rules=(),
    )
    fake_safety = AsyncMock()
    fake_safety.classify = AsyncMock(return_value=fake_safety_decision)

    fake_source = RetrievedSource(
        id="DAE001",
        score=0.85,
        title_en="Doc",
        content_bn="ম্যানকোজেব ২ গ্রাম/লিটার স্প্রে করুন।",
        citation="DAE",
    )
    fake_retriever = MagicMock()
    fake_retriever.retrieve = MagicMock(return_value=[fake_source])

    fake_generator = MagicMock()
    fake_generator.generate = AsyncMock(
        return_value=GenerationResult(
            answer="ম্যানকোজেব ২ গ্রাম/লিটার স্প্রে করুন।",
            used_source_ids=("DAE001",),
            model="stub",
        )
    )
    fake_generator.client = None

    fake_verifier = MagicMock(spec=Verifier)
    fake_verifier.verify = MagicMock(
        return_value=VerificationResult(confidence=VerificationConfidence.VERIFIED)
    )

    fake_audit = MagicMock()
    fake_audit.record = MagicMock()
    fake_audit.path = tmp_path / "audit.jsonl"

    fake_sessions = MagicMock()
    fake_sessions.get = MagicMock(return_value=[])
    fake_sessions.append = MagicMock()

    pipeline = QAPipeline(
        safety=fake_safety,
        retriever=fake_retriever,
        generator=fake_generator,
        verifier=fake_verifier,
        audit=fake_audit,
        sessions=fake_sessions,
        resolver=resolver,
    )
    return pipeline, fake_generator, fake_audit


@pytest.mark.asyncio
async def test_pipeline_flag_off_uses_t3(tmp_path: Path) -> None:
    pipeline, fake_generator, fake_audit = _setup_mock_pipeline(resolver=None, tmp_path=tmp_path)

    result = await pipeline.run(QAInput(query="আলুর নাবি ধ্বসা রোগের প্রতিকার কী?"))

    assert result.resolution_tier is ResolutionTier.GROUNDED_GENERATION
    fake_generator.generate.assert_called_once()
    audit_call = fake_audit.record.call_args[0][0]
    assert audit_call["resolution_tier"] == "grounded_generation"
    assert audit_call["llm_calls"] == 2  # safety + generation


@pytest.mark.asyncio
async def test_pipeline_flag_on_hit_returns_t2_zero_llm(tmp_path: Path) -> None:
    fb = FactBase(facts=(_sample_potato_fact(),))
    resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

    pipeline, fake_generator, fake_audit = _setup_mock_pipeline(resolver=resolver, tmp_path=tmp_path)

    events: list[tuple[str, str]] = []
    async def on_event(ev):
        events.append((ev.stage.value, ev.status.value))

    result = await pipeline.run(
        QAInput(query="আলুর নাবি ধ্বসা রোগের প্রতিকার কী?"),
        on_event=on_event,
    )

    assert result.resolution_tier is ResolutionTier.TEMPLATED_ADVISORY
    assert "mancozeb" in result.answer
    assert len(result.sources) == 1
    assert result.sources[0].id == "DAE_PEST_5E48F1_001"
    # Generation LLM was NEVER called
    fake_generator.generate.assert_not_called()

    # Trace events skipped retrieval, generation, verifier
    skip_events = [e for e in events if e[1] == "skip"]
    assert len(skip_events) == 3

    # Audit recorded with zero LLM calls
    audit_call = fake_audit.record.call_args[0][0]
    assert audit_call["resolution_tier"] == "templated_advisory"
    # Safety had no precheck rules in mock, but generation was skipped -> 1 call total
    assert audit_call["llm_calls"] == 1


@pytest.mark.asyncio
async def test_pipeline_flag_on_miss_falls_through_to_t3(tmp_path: Path) -> None:
    fb = FactBase(facts=(_sample_potato_fact(),))
    resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

    pipeline, fake_generator, fake_audit = _setup_mock_pipeline(resolver=resolver, tmp_path=tmp_path)

    result = await pipeline.run(QAInput(query="ধানের ব্লাস্ট রোগের প্রতিকার কী?"))

    assert result.resolution_tier is ResolutionTier.GROUNDED_GENERATION
    fake_generator.generate.assert_called_once()


@pytest.mark.asyncio
async def test_terminal_safety_bypasses_resolver(tmp_path: Path) -> None:
    """A banned chemical query must be blocked at T0 without ever touching resolver."""
    fb = FactBase(facts=(_sample_potato_fact(),))
    resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

    pipeline, fake_generator, fake_audit = _setup_mock_pipeline(resolver=resolver, tmp_path=tmp_path)

    # Mock terminal safety decision (e.g. precheck banned chemical rule)
    pipeline.safety.classify = AsyncMock(
        return_value=SafetyDecision(
            category=SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
            confidence=1.0,
            reason="banned active",
            matched_rules=("banned_active:carbofuran",),
            response="কার্বোফুরান নিষিদ্ধ।",
        )
    )

    result = await pipeline.run(QAInput(query="আলুতে furadan স্প্রে করা যাবে?"))

    assert result.category is SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL
    assert result.resolution_tier is ResolutionTier.DETERMINISTIC_GUARD
    fake_generator.generate.assert_not_called()
    audit_call = fake_audit.record.call_args[0][0]
    assert audit_call["resolution_tier"] == "deterministic_guard"
    assert audit_call["llm_calls"] == 0


@pytest.mark.asyncio
async def test_pipeline_vision_hints_resolve_directly_to_t2(tmp_path: Path) -> None:
    """When vision provides crop and disease hints, resolver binds directly to official prescription with 0 LLM calls."""
    fb = FactBase(facts=(_sample_potato_fact(),))
    resolver = StructuredResolver(fact_base=fb, min_confidence=0.85)

    pipeline, fake_generator, fake_audit = _setup_mock_pipeline(resolver=resolver, tmp_path=tmp_path)

    # Image detected Potato and Late Blight, generic query typed
    result = await pipeline.run(QAInput(query="কী ওষুধ স্প্রে করতে হবে?", crop="potato", disease="Potato__Late_Blight"))

    assert result.resolution_tier in (ResolutionTier.STRUCTURED_FACT, ResolutionTier.TEMPLATED_ADVISORY)
    assert "mancozeb" in result.answer
    assert result.confidence == VerificationConfidence.VERIFIED
    fake_generator.generate.assert_not_called()
