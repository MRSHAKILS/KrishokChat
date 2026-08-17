"""P0-6: local-lane concurrency guard tests.

The llama.cpp lane must never run more than ``local_lane_concurrency``
generations at once (extra requests queue); cloud/named-other lanes and the
default generator must be unaffected (guard off by default = no semaphore).
"""

from __future__ import annotations

import asyncio
import threading
import time
import unittest

from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAInput, QAPipeline
from app.domain.contracts import QueryContext, RetrievedSource
from app.domain.enums import SafetyCategory
from app.domain.safety_policy import canned_response

from tests.test_pipeline import FakeAudit, FakeRetriever, FakeSessions

_SOURCE = RetrievedSource(
    id="SRC-1",
    score=0.8,
    title_bn="সোর্স",
    content_bn="সোর্স কনটেন্ট",
    source="BARI",
    metadata={},
)


class _SlowLLM:
    """Records how many generate() calls overlap (concurrency observed).
    Mirrors the real LLM client protocol used by GroundedAnswerGenerator."""

    name = "slow-test-llm"

    def __init__(self, delay: float = 0.25) -> None:
        self.delay = delay
        self.active = 0
        self.max_active = 0
        self._lock = threading.Lock()

    async def _run(self, prompt: str) -> str:
        with self._lock:
            self.active += 1
            self.max_active = max(self.max_active, self.active)
        try:
            await asyncio.sleep(self.delay)
        finally:
            with self._lock:
                self.active -= 1
        return f"ok:{prompt}"

    async def generate(self, prompt: str, *, metadata: dict | None = None) -> str:
        return await self._run(prompt)

    async def stream(self, prompt: str, *, metadata: dict | None = None):
        yield await self._run(prompt)


def _pipeline(
    *,
    local_concurrency: int | None,
    local_models: frozenset[str] = frozenset({"krishokchat-4b"}),
) -> tuple[QAPipeline, _SlowLLM]:
    slow = _SlowLLM()
    pipeline = QAPipeline(
        safety=None,  # type: ignore[arg-type] - replaced below
        retriever=FakeRetriever(sources=[_SOURCE]),
        generator=GroundedAnswerGenerator(_SlowLLM()),  # default lane client
        verifier=None,  # type: ignore[arg-type] - replaced below
        audit=FakeAudit(),
        sessions=FakeSessions(),
        generation_clients={"krishokchat-4b": slow},
        local_lane_models=local_models,
        local_lane_concurrency=local_concurrency,
    )
    # Stub the safety/verifier seams the same way test_pipeline does for the
    # happy path (safe agri decision, no verification flags).
    pipeline.safety = _FakeSafety()
    pipeline.verifier = _FakeVerifier()
    return pipeline, slow


class _FakeSafety:
    async def classify(self, query: str, context: QueryContext):
        from app.domain.contracts import SafetyDecision

        return SafetyDecision(
            category=SafetyCategory.SAFE_AGRI,
            confidence=0.99,
            reason="test",
            matched_rules=(),
            requires_escalation=False,
            response=None,
        )


class _FakeVerifier:
    def verify(self, answer, sources):
        from app.domain.contracts import VerificationResult

        return VerificationResult(
            confidence="verified", flags=(), claims=(), sanitized_answer=None
        )


class LocalLaneConcurrencyTests(unittest.TestCase):
    def test_concurrency_1_serializes_local_lane(self) -> None:
        pipeline, slow = _pipeline(local_concurrency=1)

        async def scenario() -> int:
            await asyncio.gather(
                pipeline.run(QAInput(query="q1", model="krishokchat-4b")),
                pipeline.run(QAInput(query="q2", model="krishokchat-4b")),
            )
            return slow.max_active

        self.assertEqual(asyncio.run(scenario()), 1, "local lane must be serialized")

    def test_concurrency_2_allows_two_overlapping(self) -> None:
        pipeline, slow = _pipeline(local_concurrency=2)

        async def scenario() -> int:
            await asyncio.gather(
                pipeline.run(QAInput(query="q1", model="krishokchat-4b")),
                pipeline.run(QAInput(query="q2", model="krishokchat-4b")),
            )
            return slow.max_active

        self.assertEqual(asyncio.run(scenario()), 2)

    def test_default_lane_never_touches_semaphore(self) -> None:
        """No model requested -> default generator, no guard involvement."""
        pipeline, slow = _pipeline(local_concurrency=1)

        async def scenario() -> int:
            await asyncio.gather(
                pipeline.run(QAInput(query="q1")),
                pipeline.run(QAInput(query="q2")),
            )
            return slow.max_active

        self.assertEqual(asyncio.run(scenario()), 0, "local lane must not run at all")
        self.assertEqual(pipeline._local_semaphore, None, "semaphore must stay uncreated")

    def test_named_non_local_model_unguarded(self) -> None:
        """A model not in local_lane_models must not be serialized."""
        other = _SlowLLM()
        pipeline = QAPipeline(
            safety=_FakeSafety(),
            retriever=FakeRetriever(sources=[_SOURCE]),
            generator=GroundedAnswerGenerator(other),
            verifier=_FakeVerifier(),
            audit=FakeAudit(),
            sessions=FakeSessions(),
            generation_clients={"krishokchat-4b": _SlowLLM()},
            local_lane_models=frozenset({"krishokchat-4b"}),
            local_lane_concurrency=1,
        )

        async def scenario() -> int:
            await asyncio.gather(
                pipeline.run(QAInput(query="q1", model="unknown-model")),
                pipeline.run(QAInput(query="q2", model="unknown-model")),
            )
            return other.max_active

        self.assertEqual(asyncio.run(scenario()), 2, "non-local lanes run freely")

    def test_guard_off_by_default(self) -> None:
        """local_lane_concurrency=None => the local lane is NOT serialized."""
        pipeline, slow = _pipeline(local_concurrency=None)

        async def scenario() -> int:
            await asyncio.gather(
                pipeline.run(QAInput(query="q1", model="krishokchat-4b")),
                pipeline.run(QAInput(query="q2", model="krishokchat-4b")),
            )
            return slow.max_active

        self.assertEqual(asyncio.run(scenario()), 2)

    def test_config_bounds_reject_zero(self) -> None:
        """LOCAL_LLM_MAX_CONCURRENCY is bounded 1..16 by Settings."""
        from app.core.config import Settings

        with self.assertRaises(Exception):
            Settings(local_llm_max_concurrency=0)
        Settings(local_llm_max_concurrency=1)
        Settings(local_llm_max_concurrency=16)


if __name__ == "__main__":
    unittest.main()