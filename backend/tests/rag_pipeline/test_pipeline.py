from __future__ import annotations

import asyncio
import unittest
from collections.abc import AsyncIterator
from typing import Any

from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.safety import SafetyClassifier
from app.domain.contracts import QueryContext, RetrievedSource
from app.infrastructure.verification.dosage import DosageVerifier
from app.core.config import Settings
from app.infrastructure.llm.factory import create_llm_client
from app.infrastructure.llm.openai_compatible import OpenAICompatibleClient


class FakeLLM:
    name = "fake-model"

    def __init__(self, classification: dict[str, Any] | None = None, answer: str = "উৎসভিত্তিক উত্তর।") -> None:
        self.classification = classification or {
            "category": "safe_agri",
            "confidence": 0.99,
            "reason": "agriculture",
        }
        self.answer = answer
        self.classify_calls = 0
        self.generate_calls = 0

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        self.classify_calls += 1
        return self.classification

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        self.generate_calls += 1
        return self.answer

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        yield self.answer


class FakeRetriever:
    def __init__(self, sources: list[RetrievedSource]) -> None:
        self.sources = sources
        self.calls = 0

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        self.calls += 1
        return self.sources[:top_k]


class FakeAudit:
    def __init__(self) -> None:
        self.entries: list[dict[str, Any]] = []

    def record(self, entry: dict[str, Any]) -> None:
        self.entries.append(entry)


class FakeSessions:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str]] = []

    def get(self, session_id: str) -> list[dict[str, str]]:
        return []

    def append(self, session_id: str, role: str, content: str) -> None:
        self.items.append((session_id, role, content))


def make_pipeline(llm: FakeLLM, retriever: FakeRetriever, audit: FakeAudit) -> QAPipeline:
    return QAPipeline(
        safety=SafetyClassifier(llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(llm),
        verifier=DosageVerifier(),
        audit=audit,
        sessions=FakeSessions(),
        top_k=5,
    )


class PipelineTests(unittest.TestCase):
    def test_rule_block_stops_before_llm_and_retrieval(self) -> None:
        llm = FakeLLM()
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="পরাকুয়াট কীভাবে বেশি খাব?")))

        self.assertEqual(result.category.value, "banned_or_restricted_chemical")
        self.assertEqual(llm.classify_calls, 0)
        self.assertEqual(retriever.calls, 0)
        self.assertEqual(len(audit.entries), 1)
        self.assertEqual(audit.entries[0]["action"], "blocked-canned-response")
        # P5: the refusal reason rides on the result for the UI. F1-01 replaced
        # the inline banned literal with the source-attributed registry, so the
        # matched rule is now the attributable tag banned_active:paraquat:bn.
        self.assertIn("banned_active:paraquat:bn", result.matched_rules)
        self.assertEqual(result.safety_reason, "Deterministic safety rule matched")

    def test_classifier_failure_fails_closed(self) -> None:
        llm = FakeLLM(classification={"not_category": "safe_agri"})
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ধানের রোগ কীভাবে কমাব?")))

        self.assertEqual(result.category.value, "low_confidence")
        self.assertEqual(retriever.calls, 0)
        self.assertEqual(result.confidence.value, "blocked")
        self.assertEqual(len(audit.entries), 1)

    def test_safe_query_uses_one_shared_pipeline_and_one_audit_record(self) -> None:
        source = RetrievedSource(
            id="SRC-1",
            score=10.0,
            title_bn="ধানের পরিচর্যা",
            content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।",
        )
        llm = FakeLLM()
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ধানের রোগ কীভাবে কমাব?")))

        self.assertEqual(result.category.value, "safe_agri")
        self.assertEqual(retriever.calls, 1)
        self.assertEqual(llm.generate_calls, 1)
        self.assertEqual(len(audit.entries), 1)
        self.assertEqual(audit.entries[0]["source_ids"], ["SRC-1"])
        self.assertIn("retrieval", [event.stage.value for event in result.trace])

    def test_streaming_uses_same_pipeline_without_a_second_generation_call(self) -> None:
        source = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।")
        llm = FakeLLM(answer="স্ট্রিম করা উৎসভিত্তিক উত্তর।")
        retriever = FakeRetriever([source])
        audit = FakeAudit()

        async def collect():
            return [item async for item in make_pipeline(llm, retriever, audit).stream(QAInput(query="ধানের রোগ কীভাবে কমাব?"))]

        items = asyncio.run(collect())
        result = items[-1]
        self.assertEqual(result.answer, "স্ট্রিম করা উৎসভিত্তিক উত্তর।")
        self.assertEqual(llm.generate_calls, 0)
        self.assertTrue(any(getattr(item, "event_type", "") == "token" for item in items))
        self.assertEqual(len(audit.entries), 1)


class VerifierTests(unittest.TestCase):
    def test_bengali_numeral_dosage_is_matched_after_normalization(self) -> None:
        source = RetrievedSource(id="SRC-1", score=1.0, content_bn="প্রতি লিটার পানিতে ২ মিলি ব্যবহার করুন।")
        result = DosageVerifier().verify("প্রতি লিটার পানিতে 2 ml ব্যবহার করুন।", [source])
        self.assertEqual(result.confidence.value, "verified")

    def test_ungrounded_dosage_is_flagged(self) -> None:
        source = RetrievedSource(id="SRC-1", score=1.0, content_bn="পাতা পরিষ্কার রাখুন।")
        result = DosageVerifier().verify("প্রতি লিটারে ৫০ মিলি ব্যবহার করুন।", [source])
        self.assertEqual(result.confidence.value, "flagged-unverified")
        self.assertTrue(result.unverified_claims)


class ProviderFactoryTests(unittest.TestCase):
    def test_auto_provider_uses_configured_openrouter_key(self) -> None:
        client = create_llm_client(
            Settings(llm_provider="auto", openrouter_api_key="test-key"),
            role="intent",
        )
        self.assertIsInstance(client, OpenAICompatibleClient)
        self.assertEqual(client.base_url, "https://openrouter.ai/api/v1")


if __name__ == "__main__":
    unittest.main()
