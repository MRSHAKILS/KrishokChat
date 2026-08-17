from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path

from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.safety import SafetyClassifier
from app.domain.contracts import PipelineEvent, QAResult, RetrievedSource, VerifierClaim
from app.domain.enums import PipelineStage, SafetyCategory, StageStatus, VerificationConfidence
from app.infrastructure.cache.demo import DemoAnswerCache, qa_result_from_dict, qa_result_to_dict
from app.infrastructure.verification.dosage import DosageVerifier
from tests.test_pipeline import FakeAudit, FakeLLM, FakeRetriever, FakeSessions


def make_pipeline(
    llm: FakeLLM,
    retriever: FakeRetriever,
    audit: FakeAudit,
    cache: DemoAnswerCache | None = None,
) -> QAPipeline:
    return QAPipeline(
        safety=SafetyClassifier(llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(llm),
        verifier=DosageVerifier(),
        audit=audit,
        sessions=FakeSessions(),
        top_k=5,
        answer_cache=cache,
    )


def sample_result() -> QAResult:
    return QAResult(
        query="ধান গাছের পাতায় বাদামি দাগ দেখা দিয়েছে, কী করব?",
        category=SafetyCategory.SAFE_AGRI,
        answer="বাদামি দাগ রোগে ম্যানকোজেব প্রয়োগ করুন।",
        confidence=VerificationConfidence.VERIFIED,
        model="fake-model",
        sources=(
            RetrievedSource(
                id="SRC-1",
                score=0.81,
                title_bn="ধানের বাদামি দাগ রোগ",
                content_bn="বাদামি দাগ রোগে ম্যানকোজেব ২ মিলি/লিটার হারে ব্যবহার করুন।",
                source="BARI",
                metadata={"publisher": "BARI", "crop_bn": "ধান"},
            ),
        ),
        trace=(
            PipelineEvent(stage=PipelineStage.SAFETY, status=StageStatus.START),
            PipelineEvent(stage=PipelineStage.SAFETY, status=StageStatus.COMPLETE, detail="safe_agri"),
            PipelineEvent(stage=PipelineStage.RETRIEVAL, status=StageStatus.START),
            PipelineEvent(stage=PipelineStage.RETRIEVAL, status=StageStatus.COMPLETE, detail="1 sources"),
            PipelineEvent(stage=PipelineStage.GENERATION, status=StageStatus.START),
            PipelineEvent(stage=PipelineStage.GENERATION, status=StageStatus.COMPLETE, detail="fake-model"),
            PipelineEvent(stage=PipelineStage.VERIFIER, status=StageStatus.START),
            PipelineEvent(stage=PipelineStage.VERIFIER, status=StageStatus.COMPLETE, detail="verified"),
        ),
        verifier_flags=(),
        verifier_claims=(
            VerifierClaim(text="ম্যানকোজেব ২ মিলি/লিটার", verdict="grounded", reason="dose found"),
        ),
    )


class DemoAnswerCacheTests(unittest.TestCase):
    def test_normalize_key_collapses_whitespace_and_strips_punctuation(self) -> None:
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        self.assertEqual(
            cache.key_for("ধান  রোগ? ।"),
            cache.key_for("ধান রোগ"),
        )
        self.assertEqual(
            cache.key_for("ধান রোগ!"),
            cache.key_for("ধান রোগ"),
        )

    def test_crop_disease_and_model_part_of_key(self) -> None:
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        base = cache.key_for("ধান রোগ")
        self.assertNotEqual(base, cache.key_for("ধান রোগ", crop="ধান"))
        self.assertNotEqual(
            cache.key_for("ধান রোগ", crop="ধান"),
            cache.key_for("ধান রোগ", crop="আলু"),
        )
        self.assertNotEqual(
            cache.key_for("ধান রোগ", model="gemini"),
            cache.key_for("ধান রোগ", model="krishokchat-4b"),
        )

    def test_corpus_version_part_of_key(self) -> None:
        """P0-7: a corpus-version bump must invalidate stored demo answers."""
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        self.assertNotEqual(
            cache.key_for("ধান রোগ", corpus="2026-08"),
            cache.key_for("ধান রোগ", corpus="2026-09"),
        )
        self.assertEqual(
            cache.key_for("ধান রোগ", corpus="2026-08"),
            cache.key_for("ধান রোগ", corpus="2026-08"),
        )

    def test_cap_evicts_oldest(self) -> None:
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json", max_entries=2)
        cache.put("a", {"answer": "1"})
        cache.put("b", {"answer": "2"})
        cache.put("c", {"answer": "3"})
        self.assertEqual(len(cache), 2)
        self.assertIsNone(cache.get("a"))
        self.assertIsNotNone(cache.get("b"))
        self.assertIsNotNone(cache.get("c"))

    def test_persistence_across_instances(self) -> None:
        path = Path(tempfile.mkdtemp()) / "cache.json"
        first = DemoAnswerCache(path)
        first.put("ধান|কী করব", {"answer": "উত্তর"})
        second = DemoAnswerCache(path)
        self.assertEqual(second.get("ধান|কী করব"), {"answer": "উত্তর"})

    def test_corrupt_file_loads_as_empty_cache(self) -> None:
        path = Path(tempfile.mkdtemp()) / "cache.json"
        path.write_text("{not json", encoding="utf-8")
        cache = DemoAnswerCache(path)
        self.assertEqual(len(cache), 0)

    def test_qa_result_round_trip_serialization(self) -> None:
        result = sample_result()
        payload = qa_result_to_dict(result)
        restored = qa_result_from_dict(payload)

        self.assertEqual(restored.query, result.query)
        self.assertEqual(restored.category, result.category)
        self.assertEqual(restored.answer, result.answer)
        self.assertEqual(restored.confidence, result.confidence)
        self.assertEqual(restored.model, result.model)
        self.assertIsNone(restored.error)
        self.assertEqual(len(restored.sources), 1)
        self.assertEqual(restored.sources[0].id, "SRC-1")
        self.assertEqual(restored.sources[0].metadata["publisher"], "BARI")
        self.assertEqual(len(restored.trace), 8)
        self.assertEqual(restored.trace[1].stage, PipelineStage.SAFETY)
        self.assertEqual(restored.verifier_claims[0].verdict, "grounded")
        # Round-trip through actual file storage
        path = Path(tempfile.mkdtemp()) / "cache.json"
        cache = DemoAnswerCache(path)
        cache.put("k", payload)
        reloaded = DemoAnswerCache(path)
        again = qa_result_from_dict(reloaded.get("k"))
        self.assertEqual(again.answer, result.answer)


class PipelineCacheTests(unittest.TestCase):
    def test_second_run_served_from_cache_without_llm_or_retrieval(self) -> None:
        source = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।")
        llm = FakeLLM()
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        pipeline = make_pipeline(llm, retriever, audit, cache)

        first = asyncio.run(pipeline.run(QAInput(query="ধান রোগ কীভাবে কমাব?")))
        self.assertEqual(retriever.calls, 1)
        self.assertEqual(llm.generate_calls, 1)

        second = asyncio.run(pipeline.run(QAInput(query="ধান রোগ কীভাবে কমাব?")))
        self.assertEqual(second.answer, first.answer)
        self.assertEqual(second.category, first.category)
        # No new LLM/retrieval work on the replay
        self.assertEqual(retriever.calls, 1)
        self.assertEqual(llm.generate_calls, 1)

    def test_replay_keeps_sources_trace_and_verifier_stamps(self) -> None:
        source = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।")
        llm = FakeLLM()
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        pipeline = make_pipeline(llm, retriever, audit, cache)

        asyncio.run(pipeline.run(QAInput(query="ধান রোগ কীভাবে কমাব?")))
        replay = asyncio.run(pipeline.run(QAInput(query="ধান রোগ কীভাবে কমাব?")))

        self.assertEqual([s.id for s in replay.sources], ["SRC-1"])
        self.assertEqual(replay.confidence, VerificationConfidence.VERIFIED)
        self.assertIn("verifier", [event.stage.value for event in replay.trace])

    def test_replay_audited_with_cached_flag_and_session(self) -> None:
        source = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।")
        llm = FakeLLM()
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        pipeline = make_pipeline(llm, retriever, audit, cache)

        asyncio.run(pipeline.run(QAInput(query="ধান রোগ", session_id="s1")))
        asyncio.run(pipeline.run(QAInput(query="ধান রোগ", session_id="s1")))

        self.assertEqual(len(audit.entries), 2)
        self.assertFalse(audit.entries[0]["cached"])
        self.assertTrue(audit.entries[1]["cached"])
        # Replay still appends to the session conversation
        self.assertTrue(any(item[0] == "s1" for item in pipeline.sessions.items))

    def test_cached_replay_emits_trace_events(self) -> None:
        source = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।")
        llm = FakeLLM()
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        pipeline = make_pipeline(llm, retriever, audit, cache)

        async def warm() -> None:
            await pipeline.run(QAInput(query="ধান রোগ"))

        async def replay() -> list[PipelineEvent]:
            events: list[PipelineEvent] = []

            async def on_event(event: PipelineEvent) -> None:
                events.append(event)

            await pipeline.run(QAInput(query="ধান রোগ"), on_event=on_event)
            return events

        asyncio.run(warm())
        events = asyncio.run(replay())
        # Full agent trace replayed for the stepper
        self.assertEqual(
            [event.stage.value for event in events],
            ["safety", "safety", "retrieval", "retrieval", "generation", "generation", "verifier", "verifier"],
        )

    def test_terminal_refusals_never_cached(self) -> None:
        llm = FakeLLM()
        retriever = FakeRetriever([])
        audit = FakeAudit()
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        pipeline = make_pipeline(llm, retriever, audit, cache)

        asyncio.run(pipeline.run(QAInput(query="পরাকুয়াট কীভাবে বেশি খাব?")))
        asyncio.run(pipeline.run(QAInput(query="পরাকুয়াট কীভাবে বেশি খাব?")))

        self.assertEqual(len(cache), 0)
        # Safety still evaluated live every time
        self.assertEqual(len(audit.entries), 2)
        self.assertFalse(audit.entries[1]["cached"])

    def test_referral_error_result_never_cached(self) -> None:
        llm = FakeLLM()
        retriever = FakeRetriever([])  # no sources -> generator error path
        audit = FakeAudit()
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        pipeline = make_pipeline(llm, retriever, audit, cache)

        result = asyncio.run(pipeline.run(QAInput(query="ধান রোগ কীভাবে কমাব?")))

        self.assertEqual(result.category, SafetyCategory.SAFE_AGRI)
        self.assertIsNotNone(result.error)
        self.assertEqual(len(cache), 0)

    def test_no_cache_keeps_pipeline_exactly_as_before(self) -> None:
        source = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।")
        llm = FakeLLM()
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        pipeline = make_pipeline(llm, retriever, audit)  # no cache

        first = asyncio.run(pipeline.run(QAInput(query="ধান রোগ")))
        second = asyncio.run(pipeline.run(QAInput(query="ধান রোগ")))

        # Identical behavior: every run is a fresh pipeline run
        self.assertEqual(retriever.calls, 2)
        self.assertEqual(llm.generate_calls, 2)
        self.assertEqual(len(audit.entries), 2)
        self.assertFalse(audit.entries[1]["cached"])
        self.assertEqual(first.answer, second.answer)

    def test_context_specific_cache_key(self) -> None:
        source = RetrievedSource(id="SRC-1", score=10.0, content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।")
        llm = FakeLLM()
        retriever = FakeRetriever([source])
        audit = FakeAudit()
        cache = DemoAnswerCache(Path(tempfile.mkdtemp()) / "cache.json")
        pipeline = make_pipeline(llm, retriever, audit, cache)

        asyncio.run(pipeline.run(QAInput(query="ধান রোগ", crop="ধান")))
        asyncio.run(pipeline.run(QAInput(query="ধান রোগ", crop="আলু")))  # different context

        self.assertEqual(retriever.calls, 2)  # miss on different crop


if __name__ == "__main__":
    unittest.main()