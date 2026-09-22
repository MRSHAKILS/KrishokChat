"""Smoke conversion of scripts/test_qa_pipeline.py (kept as-is).

Modernized from the legacy app.agents.* shims to the functional pipeline
(app.application.qa_pipeline.QAPipeline — the legacy agents/ and
services/advisory/ imports are compatibility shims only per AGENTS.md §5.1).
Replays the same potato-late-blight query through
safety -> retrieval -> generation -> verifier with a deterministic stub LLM
and the real offline BM25 index, asserting the agent-trace stages complete in
order and the answer reaches the verifier.

Fully offline: no network, no API keys (stub generator only).
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import pytest

BACKEND = Path(__file__).resolve().parent.parent.parent
INDEX = BACKEND / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl"
CORPUS = BACKEND / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"

from app.domain.safety_policy import precheck  # noqa: E402

QUERY = "আলুর দেরি ব্লাইট রোগের প্রতিকার কি?"


class StubLLM:
    """Deterministic AnswerGenerator port double (test-only, not production)."""

    name = "smoke-stub"

    async def generate(self, query: str, context, sources: list[Any]) -> Any:
        from app.application.generation import REFERRAL, GenerationResult

        if not sources:
            return GenerationResult(
                answer=REFERRAL, model=self.name, mode="no_sources", error="No sources"
            )
        return GenerationResult(
            answer="আলুর দেরি ব্লাইট রোগের প্রতিকারে কার্বেন্ডাজিম/ম্যানকোজেব জাতীয় ছত্রাকনাশক ব্যবহার করা যায়।",
            used_source_ids=tuple(s.id for s in sources),
            model=self.name,
            mode="grounded",
        )

    async def stream(self, query: str, context, sources: list[Any]) -> AsyncIterator[str]:
        from app.application.generation import REFERRAL

        if not sources:
            yield REFERRAL
        else:
            yield "আলুর দেরি ব্লাইট রোগের প্রতিকারে কার্বেন্ডাজিম/ম্যানকোজেব জাতীয় ছত্রাকনাশক ব্যবহার করা যায়।"

    async def generate_from_text(self, answer: str, sources: list[Any], *, mode: str) -> Any:
        from app.application.generation import REFERRAL, GenerationResult

        return GenerationResult(
            answer=answer.strip() or REFERRAL,
            used_source_ids=tuple(s.id for s in sources),
            model=self.name,
            mode=mode,
        )


@pytest.fixture(scope="module")
def pipeline():
    if not INDEX.exists() or not CORPUS.exists():
        pytest.skip("precomputed BM25 index not present in ml_assets/rag_index")
    from app.application.qa_pipeline import QAPipeline
    from app.application.verifier import HardenedDosageVerifier
    from app.infrastructure.audit.jsonl import JSONLAuditSink
    from app.infrastructure.retrieval.bm25 import BM25Retriever
    from app.infrastructure.sessions.memory import InMemorySessionStore

    import tempfile

    return QAPipeline(
        safety=_SafeStubClassifier(),
        retriever=BM25Retriever(index_path=INDEX, corpus_path=CORPUS),
        generator=StubLLM(),
        verifier=HardenedDosageVerifier(),
        audit=JSONLAuditSink(Path(tempfile.gettempdir()) / "krishokchat_smoke_audit.jsonl"),
        sessions=InMemorySessionStore(max_turns=10, ttl_seconds=1800),
        top_k=5,
    )


class _SafeStubClassifier:
    async def classify(self, query: str, context) -> Any:
        from app.domain.contracts import SafetyDecision
        from app.domain.enums import SafetyCategory

        match = precheck(query)
        if match:
            category, rules = match
            return SafetyDecision(
                category=category,
                confidence=1.0,
                reason="Deterministic safety rule matched",
                matched_rules=rules,
                requires_escalation=category is SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
                response=None,
            )
        return SafetyDecision(
            category=SafetyCategory.SAFE_AGRI,
            confidence=0.99,
            reason="smoke stub",
            matched_rules=(),
            requires_escalation=False,
            response=None,
        )


class TestSmokeQAPipeline:
    def test_trace_stages_complete_in_order(self, pipeline) -> None:
        from app.application.qa_pipeline import QAInput
        from app.domain.enums import PipelineStage

        result = asyncio.run(pipeline.run(QAInput(query=QUERY)))
        stages = [event.stage for event in result.trace if event.status.value == "complete"]
        expected_order = [PipelineStage.SAFETY, PipelineStage.RETRIEVAL, PipelineStage.GENERATION, PipelineStage.VERIFIER]
        indices = [stages.index(name) for name in expected_order]
        assert indices == sorted(indices), f"stages out of order: {[s.value for s in stages]}"
        assert result.category.value == "safe_agri"
        assert result.sources, "retrieval returned no sources"
        assert result.answer and "ছত্রাকনাশক" in result.answer
        assert result.error is None