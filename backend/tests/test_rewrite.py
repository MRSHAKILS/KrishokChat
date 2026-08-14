from __future__ import annotations

import asyncio
import unittest
from typing import Any

from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.rewrite import ConversationalQueryRewriter
from app.application.safety import SafetyClassifier
from app.domain.contracts import RetrievedSource
from app.infrastructure.verification.dosage import DosageVerifier
from tests.test_pipeline import FakeAudit, FakeLLM, FakeRetriever, FakeSessions


class CapturingRetriever(FakeRetriever):
    def __init__(self, sources: list[RetrievedSource]) -> None:
        super().__init__(sources)
        self.last_query: str | None = None

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        self.last_query = query
        return super().retrieve(query, top_k=top_k)


class CapturingClassifyLLM(FakeLLM):
    """Records the classifier prompt so tests can prove safety saw the raw query."""

    def __init__(self) -> None:
        super().__init__()
        self.classify_prompts: list[str] = []

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        self.classify_prompts.append(prompt)
        return self.classification


def make_pipeline(
    classify_llm: FakeLLM,
    gen_llm: FakeLLM,
    retriever: CapturingRetriever,
    audit: FakeAudit,
    rewrite_llm: FakeLLM | None = None,
) -> QAPipeline:
    return QAPipeline(
        safety=SafetyClassifier(classify_llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(gen_llm),
        verifier=DosageVerifier(),
        audit=audit,
        sessions=FakeSessions(),
        top_k=5,
        rewriter=ConversationalQueryRewriter(rewrite_llm) if rewrite_llm else None,
    )


SOURCE = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধান চাষে ইউরিয়া সার ব্যবহার করুন।")
HISTORY = [
    {"role": "user", "content": "ধান চাষে কী কী সার দিতে হয়?"},
    {"role": "assistant", "content": "ধান চাষে ইউরিয়া, টিএসপি ও এমওপি সার ব্যবহার করা হয়।"},
]


class RewriterUnitTests(unittest.TestCase):
    def test_no_history_never_rewrites(self) -> None:
        rewriter = ConversationalQueryRewriter(FakeLLM())
        self.assertFalse(rewriter.should_rewrite("তাহলে কী করব?", []))
        self.assertFalse(rewriter.should_rewrite("ধান রোগের প্রতিকার কী করব?", []))

    def test_marker_with_history_triggers_gate(self) -> None:
        rewriter = ConversationalQueryRewriter(FakeLLM())
        self.assertTrue(rewriter.should_rewrite("তাহলে কী করব?", HISTORY))
        self.assertTrue(rewriter.should_rewrite("এটা কীভাবে দেব?", HISTORY))
        self.assertTrue(rewriter.should_rewrite("কতটুকু ইউরিয়া দেব?", HISTORY))

    def test_self_contained_query_with_history_not_rewritten(self) -> None:
        rewriter = ConversationalQueryRewriter(FakeLLM())
        self.assertFalse(rewriter.should_rewrite("আলু চাষে লেট ব্লাইটের প্রতিকার কী?", HISTORY))

    def test_rewrite_failure_returns_raw_query(self) -> None:
        class BoomLLM(FakeLLM):
            async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
                raise RuntimeError("provider down")

        rewriter = ConversationalQueryRewriter(BoomLLM())
        result = asyncio.run(rewriter.rewrite("তাহলে কী করব?", HISTORY))
        self.assertEqual(result, "তাহলে কী করব?")

    def test_empty_rewrite_returns_raw_query(self) -> None:
        rewriter = ConversationalQueryRewriter(FakeLLM(answer="   "))
        result = asyncio.run(rewriter.rewrite("তাহলে কী করব?", HISTORY))
        self.assertEqual(result, "তাহলে কী করব?")


class PipelineRewriteTests(unittest.TestCase):
    def test_single_turn_never_calls_rewrite_llm(self) -> None:
        rewrite_llm = FakeLLM(answer="ধান চাষে ইউরিয়া কতটুকু দেব?")
        retriever = CapturingRetriever([SOURCE])
        audit = FakeAudit()
        pipeline = make_pipeline(FakeLLM(), FakeLLM(), retriever, audit, rewrite_llm)

        asyncio.run(pipeline.run(QAInput(query="ধান চাষে কতটুকু ইউরিয়া দেব?")))

        self.assertEqual(rewrite_llm.generate_calls, 0)  # gated off: no history
        self.assertFalse(audit.entries[0]["retrieval_query_rewritten"])

    def test_followup_rewritten_for_retrieval_and_audited(self) -> None:
        rewrite_llm = FakeLLM(answer="ধান চাষে ইউরিয়া কতটুকু দেব?")
        retriever = CapturingRetriever([SOURCE])
        audit = FakeAudit()
        pipeline = make_pipeline(FakeLLM(), FakeLLM(), retriever, audit, rewrite_llm)

        asyncio.run(
            pipeline.run(QAInput(query="তাহলে কতটুকু দেব?", history=HISTORY))
        )

        self.assertEqual(rewrite_llm.generate_calls, 1)
        # The retriever saw the standalone query, not the deixis fragment
        self.assertIn("ইউরিয়া", retriever.last_query)
        self.assertNotIn("তাহলে", retriever.last_query)
        # Audited honestly: what was searched + that it was rewritten
        self.assertTrue(audit.entries[0]["retrieval_query_rewritten"])
        self.assertIn("ইউরিয়া", audit.entries[0]["retrieval_query_used"])

    def test_rewrite_failure_falls_back_to_raw_query(self) -> None:
        class BoomLLM(FakeLLM):
            async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
                raise RuntimeError("provider down")

        retriever = CapturingRetriever([SOURCE])
        audit = FakeAudit()
        pipeline = make_pipeline(FakeLLM(), FakeLLM(), retriever, audit, BoomLLM())

        result = asyncio.run(pipeline.run(QAInput(query="তাহলে কতটুকু দেব?", history=HISTORY)))

        self.assertEqual(result.category.value, "safe_agri")  # answered despite rewrite failure
        self.assertFalse(audit.entries[0]["retrieval_query_rewritten"])
        self.assertIn("তাহলে", retriever.last_query)  # raw query was searched

    def test_self_contained_followup_kept_unchanged_by_llm(self) -> None:
        rewrite_llm = FakeLLM(answer="ধান চাষে কতটুকু ইউরিয়া দেব?")  # returns same meaning
        retriever = CapturingRetriever([SOURCE])
        audit = FakeAudit()
        pipeline = make_pipeline(FakeLLM(), FakeLLM(), retriever, audit, rewrite_llm)

        asyncio.run(pipeline.run(QAInput(query="কতটুকু ইউরিয়া দেব?", history=HISTORY)))

        # Gate fires (marker + history) but the LLM's rewrite is a real rewrite
        self.assertEqual(rewrite_llm.generate_calls, 1)
        self.assertTrue(audit.entries[0]["retrieval_query_rewritten"])

    def test_no_rewriter_keeps_prior_behavior(self) -> None:
        retriever = CapturingRetriever([SOURCE])
        audit = FakeAudit()
        pipeline = make_pipeline(FakeLLM(), FakeLLM(), retriever, audit)  # no rewriter

        asyncio.run(pipeline.run(QAInput(query="তাহলে কতটুকু দেব?", history=HISTORY)))

        self.assertIn("তাহলে", retriever.last_query)  # exactly the old behavior
        self.assertFalse(audit.entries[0]["retrieval_query_rewritten"])

    def test_safety_classifier_always_sees_raw_query(self) -> None:
        classify_llm = CapturingClassifyLLM()
        rewrite_llm = FakeLLM(answer="ধান চাষে ইউরিয়া কতটুকু দেব?")
        retriever = CapturingRetriever([SOURCE])
        audit = FakeAudit()
        pipeline = make_pipeline(classify_llm, FakeLLM(), retriever, audit, rewrite_llm)

        asyncio.run(pipeline.run(QAInput(query="তাহলে কতটুকু দেব?", history=HISTORY)))

        # The classifier prompt contains the RAW query, never the rewrite —
        # rewriting is a retrieval-only concern, safety stays on the surface text.
        self.assertIn("তাহলে কতটুকু দেব?", classify_llm.classify_prompts[0])
        self.assertNotIn("ইউরিয়া কতটুকু দেব?", classify_llm.classify_prompts[0])

    def test_rewrite_surfaces_in_agent_trace(self) -> None:
        rewrite_llm = FakeLLM(answer="ধান চাষে ইউরিয়া কতটুকু দেব?")
        retriever = CapturingRetriever([SOURCE])
        audit = FakeAudit()
        pipeline = make_pipeline(FakeLLM(), FakeLLM(), retriever, audit, rewrite_llm)

        async def collect() -> list[dict[str, str]]:
            events: list[dict[str, str]] = []

            async def on_event(event) -> None:
                events.append({"stage": event.stage.value, "detail": event.detail or ""})

            await pipeline.run(
                QAInput(query="তাহলে কতটুকু দেব?", history=HISTORY),
                on_event=on_event,
            )
            return events

        events = asyncio.run(collect())
        retrieval_complete = next(e for e in events if e["stage"] == "retrieval" and e["detail"])
        self.assertIn("rewritten", retrieval_complete["detail"])


if __name__ == "__main__":
    unittest.main()