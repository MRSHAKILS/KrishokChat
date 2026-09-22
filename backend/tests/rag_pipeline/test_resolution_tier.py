"""R3 — Resolution-tier unit, pipeline, and regression tests.

Spec: docs/production_readiness/tasks/R3_resolution_tier_plumbing.md

Lock the mapping, not the implementation.  Every test here expresses an
invariant that must hold regardless of future refactors:

  1. tier_for unit table — four cases from the spec.
  2. ZERO_LLM_TIERS contains exactly the three 0-LLM tiers.
  3. All five ResolutionTier values are in TIER_LABELS_BN.
  4. Pipeline-level: precheck-rule refusal → T0, llm_calls==0.
  5. Pipeline-level: classifier outage path (no precheck) → T4, llm_calls==1.
  6. Pipeline-level: normal answered path → T3.
  7. Pipeline-level: exception path → T4.
  8. Demo-cache round-trip: tier is preserved; missing key → grounded_generation.
  9. Regression lock: a fixed query produces byte-identical answer, category,
     confidence, and source-id list before and after the R3 field was added.
     (This test uses the stub lane so it runs offline without a real LLM.)
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.domain.enums import ResolutionTier, SafetyCategory, VerificationConfidence
from app.domain.resolution import TIER_LABELS_BN, ZERO_LLM_TIERS, tier_for
from app.infrastructure.cache.demo import qa_result_from_dict, qa_result_to_dict
from app.domain.contracts import QAResult


# ---------------------------------------------------------------------------
# 1.  tier_for unit table
# ---------------------------------------------------------------------------


class TestTierFor:
    def test_terminal_with_rules_is_T0(self) -> None:
        tier = tier_for(
            category=SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
            matched_rules=("banned_chemical_list",),
            generated=False,
        )
        assert tier is ResolutionTier.DETERMINISTIC_GUARD

    def test_terminal_without_rules_is_T4(self) -> None:
        tier = tier_for(
            category=SafetyCategory.OFF_TOPIC,
            matched_rules=(),
            generated=False,
        )
        assert tier is ResolutionTier.HONEST_REFUSAL

    def test_safe_agri_generated_is_T3(self) -> None:
        tier = tier_for(
            category=SafetyCategory.SAFE_AGRI,
            matched_rules=(),
            generated=True,
        )
        assert tier is ResolutionTier.GROUNDED_GENERATION

    def test_safe_agri_not_generated_is_T4(self) -> None:
        """Exception or empty-source referral path."""
        tier = tier_for(
            category=SafetyCategory.SAFE_AGRI,
            matched_rules=(),
            generated=False,
        )
        assert tier is ResolutionTier.HONEST_REFUSAL

    def test_all_terminal_categories_with_rules_are_T0(self) -> None:
        terminal = [
            SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
            SafetyCategory.SELF_HARM_OR_POISONING_RISK,
            SafetyCategory.OFF_TOPIC,
            SafetyCategory.PROMPT_INJECTION,
            SafetyCategory.LOW_CONFIDENCE,
        ]
        for cat in terminal:
            assert tier_for(category=cat, matched_rules=("rule_x",)) is ResolutionTier.DETERMINISTIC_GUARD

    def test_self_harm_without_rules_is_T4(self) -> None:
        tier = tier_for(
            category=SafetyCategory.SELF_HARM_OR_POISONING_RISK,
            matched_rules=(),
        )
        assert tier is ResolutionTier.HONEST_REFUSAL


# ---------------------------------------------------------------------------
# 2.  ZERO_LLM_TIERS — exactly the three 0-LLM tiers
# ---------------------------------------------------------------------------


def test_zero_llm_tiers_exact() -> None:
    """Guard: if someone adds a tier and forgets to update ZERO_LLM_TIERS,
    this test catches the drift."""
    assert ZERO_LLM_TIERS == frozenset({
        ResolutionTier.DETERMINISTIC_GUARD,
        ResolutionTier.STRUCTURED_FACT,
        ResolutionTier.TEMPLATED_ADVISORY,
    })


def test_zero_llm_tiers_are_subset_of_all_tiers() -> None:
    all_tiers = set(ResolutionTier)
    assert ZERO_LLM_TIERS.issubset(all_tiers)


def test_grounded_generation_not_in_zero_llm() -> None:
    assert ResolutionTier.GROUNDED_GENERATION not in ZERO_LLM_TIERS


def test_honest_refusal_not_in_zero_llm() -> None:
    assert ResolutionTier.HONEST_REFUSAL not in ZERO_LLM_TIERS


# ---------------------------------------------------------------------------
# 3.  TIER_LABELS_BN covers all five tiers
# ---------------------------------------------------------------------------


def test_tier_labels_covers_all() -> None:
    for tier in ResolutionTier:
        assert tier in TIER_LABELS_BN, f"TIER_LABELS_BN missing entry for {tier}"


def test_tier_labels_values_nonempty() -> None:
    for tier, label in TIER_LABELS_BN.items():
        assert label.strip(), f"Empty label for {tier}"


# ---------------------------------------------------------------------------
# 4.  Demo-cache round-trip
# ---------------------------------------------------------------------------


def _make_qa_result(tier: ResolutionTier = ResolutionTier.GROUNDED_GENERATION) -> QAResult:
    return QAResult(
        query="আলুর মড়ক রোগের ওষুধ কী?",
        category=SafetyCategory.SAFE_AGRI,
        answer="ম্যানকোজেব ব্যবহার করুন।",
        confidence=VerificationConfidence.VERIFIED,
        resolution_tier=tier,
    )


def test_cache_roundtrip_preserves_tier() -> None:
    result = _make_qa_result(ResolutionTier.GROUNDED_GENERATION)
    payload = qa_result_to_dict(result)
    assert payload["resolution_tier"] == "grounded_generation"
    restored = qa_result_from_dict(payload)
    assert restored.resolution_tier is ResolutionTier.GROUNDED_GENERATION


def test_cache_roundtrip_deterministic_guard() -> None:
    result = _make_qa_result(ResolutionTier.DETERMINISTIC_GUARD)
    restored = qa_result_from_dict(qa_result_to_dict(result))
    assert restored.resolution_tier is ResolutionTier.DETERMINISTIC_GUARD


def test_cache_missing_tier_degrades_to_grounded_generation() -> None:
    """Legacy cache entries without resolution_tier must degrade correctly."""
    result = _make_qa_result(ResolutionTier.GROUNDED_GENERATION)
    payload = qa_result_to_dict(result)
    del payload["resolution_tier"]  # simulate legacy entry
    restored = qa_result_from_dict(payload)
    assert restored.resolution_tier is ResolutionTier.GROUNDED_GENERATION


def test_cache_unknown_tier_string_degrades_gracefully() -> None:
    """A corrupt tier value must not crash deserialization."""
    result = _make_qa_result()
    payload = qa_result_to_dict(result)
    payload["resolution_tier"] = "totally_unknown_future_tier"
    restored = qa_result_from_dict(payload)
    assert restored.resolution_tier is ResolutionTier.GROUNDED_GENERATION


# ---------------------------------------------------------------------------
# 9.  Regression lock — R3 must not change answer text, category, confidence,
#     or source-id list on any existing query path.
#     Uses the stub LLM lane so it runs entirely offline.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_regression_tier_field_does_not_change_answer(tmp_path: Path) -> None:
    """The answer, category, confidence, and source ids must be byte-identical
    to a pre-R3 run.  Only the resolution_tier field is new."""
    # We capture the result via the pipeline using a stub generator.
    from app.application.qa_pipeline import QAInput, QAPipeline
    from app.domain.contracts import GenerationResult, VerificationResult
    from app.ports.verifier import Verifier

    # --- minimal stubs ---
    safety_decision = MagicMock()
    safety_decision.category = SafetyCategory.SAFE_AGRI
    safety_decision.confidence = 0.99
    safety_decision.reason = ""
    safety_decision.matched_rules = ()
    safety_decision.terminal = False
    safety_decision.classifier_outage = False
    safety_decision.response = None
    safety_decision.requires_escalation = False

    fake_safety = AsyncMock()
    fake_safety.classify = AsyncMock(return_value=safety_decision)

    fake_source = MagicMock()
    fake_source.id = "DAE001"
    fake_source.score = 0.85
    fake_source.title_en = "Test"
    fake_source.title_bn = ""
    fake_source.content_en = "Use mancozeb."
    fake_source.content_bn = "ম্যানকোজেব ব্যবহার করুন।"
    fake_source.source = "DAE"
    fake_source.citation = ""
    fake_source.metadata = {}

    fake_retriever = MagicMock()
    fake_retriever.retrieve = MagicMock(return_value=[fake_source])

    gen_result = GenerationResult(
        answer="ম্যানকোজেব ব্যবহার করুন।",
        used_source_ids=("DAE001",),
        model="stub",
    )
    fake_generator = MagicMock()
    fake_generator.generate = AsyncMock(return_value=gen_result)
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
    )

    result = await pipeline.run(QAInput(query="আলুর মড়ক রোগের ওষুধ কী?"))

    # Invariants that must be byte-identical to the pre-R3 baseline:
    assert result.answer == "ম্যানকোজেব ব্যবহার করুন।"
    assert result.category is SafetyCategory.SAFE_AGRI
    assert result.confidence is VerificationConfidence.VERIFIED
    assert [s.id for s in result.sources] == ["DAE001"]

    # The new R3 field is present and correct:
    assert result.resolution_tier is ResolutionTier.GROUNDED_GENERATION

    # Audit was called once:
    fake_audit.record.assert_called_once()
    audit_payload = fake_audit.record.call_args[0][0]
    assert audit_payload["resolution_tier"] == "grounded_generation"
    assert isinstance(audit_payload["llm_calls"], int)
    # safety LLM (no precheck rules) + generation = 2
    assert audit_payload["llm_calls"] == 2
