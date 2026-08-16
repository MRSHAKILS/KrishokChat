"""T0-06: provider failover chain + circuit breaker tests (no network).

Fake clients implement the LLMClient port (name / classify_json / generate /
stream) exactly like ``tests.test_pipeline.FakeLLM``; no real provider is ever
constructed with a key and no network call is made.
"""

from __future__ import annotations

import asyncio
import os
import tempfile
import time
import unittest
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any
from unittest import mock

from fastapi.testclient import TestClient

from app.application.container import build_container
from app.application.generation import GroundedAnswerGenerator, REFERRAL
from app.application.safety import SafetyClassifier
from app.core.config import Settings
from app.domain.contracts import QueryContext, RetrievedSource
from app.infrastructure.llm.failover import (
    AllProvidersFailed,
    CircuitBreaker,
    FailoverLLMClient,
    build_failover_client,
    parse_chain_names,
)
from app.infrastructure.llm.openai_compatible import LLMError, OpenAICompatibleClient, UnavailableLLMClient
from app.main import create_app


class FakeLLM:
    """Minimal LLMClient-port fake that succeeds with canned answers."""

    def __init__(
        self,
        name: str = "fake-ok",
        answer: str = "উত্তর",
        classification: dict[str, Any] | None = None,
    ) -> None:
        self.name = name
        self.answer = answer
        self.classification = classification or {
            "category": "safe_agri",
            "confidence": 0.99,
            "reason": "ok",
        }
        self.calls = 0

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        self.calls += 1
        return self.classification

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        self.calls += 1
        return self.answer

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        self.calls += 1
        yield self.answer


class RaisingLLM(FakeLLM):
    """Port fake that always raises LLMError (the adapter failure contract)."""

    def __init__(self, name: str = "fake-fail") -> None:
        super().__init__(name=name)
        self.calls = 0

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        self.calls += 1
        raise LLMError(f"{self.name} boom")

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        self.calls += 1
        raise LLMError(f"{self.name} boom")

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        self.calls += 1
        raise LLMError(f"{self.name} boom")
        yield ""


class FlakyLLM(FakeLLM):
    """Port fake that fails the first N calls, then succeeds."""

    def __init__(self, name: str, failures: int = 1, answer: str = "উত্তর") -> None:
        super().__init__(name=name, answer=answer)
        self.failures = failures
        self.calls = 0

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        self.calls += 1
        if self.calls <= self.failures:
            raise LLMError("transient")
        return self.answer


def make_breaker(max_failures: int = 3, cooldown_seconds: float = 30.0) -> CircuitBreaker:
    return CircuitBreaker(max_failures=max_failures, cooldown_seconds=cooldown_seconds)


def make_failover(*entries: tuple[str, FakeLLM]) -> FailoverLLMClient:
    return FailoverLLMClient([(name, client, make_breaker()) for name, client in entries])


async def collect_stream(client: FailoverLLMClient, prompt: str) -> list[str]:
    chunks = []
    async for chunk in client.stream(prompt):
        chunks.append(chunk)
    return chunks


class CircuitBreakerTests(unittest.TestCase):
    def test_trips_after_max_failures(self) -> None:
        breaker = make_breaker(max_failures=3)
        for _ in range(2):
            breaker.record_failure()
            self.assertFalse(breaker.tripped)
        breaker.record_failure()
        self.assertTrue(breaker.tripped)
        self.assertGreater(breaker.cooldown_until, time.time())
        self.assertEqual(breaker.consecutive_failures, 3)

    def test_resets_on_success(self) -> None:
        breaker = make_breaker(max_failures=3)
        for _ in range(3):
            breaker.record_failure()
        self.assertTrue(breaker.tripped)
        breaker.record_success()
        self.assertFalse(breaker.tripped)
        self.assertEqual(breaker.consecutive_failures, 0)
        self.assertEqual(breaker.cooldown_until, 0.0)

    def test_probe_allowed_after_cooldown_and_retrips_on_failure(self) -> None:
        breaker = make_breaker(max_failures=3, cooldown_seconds=30.0)
        for _ in range(3):
            breaker.record_failure()
        self.assertTrue(breaker.tripped)
        breaker.cooldown_until = time.time() - 1.0  # cooldown expired -> probe allowed
        self.assertFalse(breaker.tripped)
        breaker.record_failure()  # probe fails -> re-trips
        self.assertTrue(breaker.tripped)
        self.assertGreater(breaker.cooldown_until, time.time())

    def test_parse_chain_names(self) -> None:
        self.assertEqual(
            parse_chain_names(" openrouter, GEMINI,ollama ,"),
            ["openrouter", "gemini", "ollama"],
        )
        self.assertEqual(parse_chain_names(""), [])
        self.assertEqual(parse_chain_names("  ,  "), [])


class FailoverLLMClientTests(unittest.TestCase):
    def test_fallback_on_failure(self) -> None:
        first = RaisingLLM("first")
        second = FakeLLM("second", answer="উত্তর-২")
        client = make_failover(("first", first), ("second", second))
        answer = asyncio.run(client.generate("q"))
        self.assertEqual(answer, "উত্তর-২")
        self.assertEqual(first.calls, 1)
        self.assertEqual(second.calls, 1)
        self.assertEqual(client.provider, "second")
        self.assertEqual(client.name, "second")

    def test_breaker_skips_tripped_provider(self) -> None:
        first = RaisingLLM("first")
        second = FakeLLM("second")
        first_breaker = make_breaker(max_failures=2)
        client = FailoverLLMClient(
            [
                ("first", first, first_breaker),
                ("second", second, make_breaker(max_failures=2)),
            ]
        )
        for _ in range(3):
            self.assertEqual(asyncio.run(client.generate("q")), "উত্তর")
        # Two failures trip the first provider; the third call skips it.
        self.assertEqual(first.calls, 2)
        self.assertEqual(second.calls, 3)
        self.assertTrue(first_breaker.tripped)

    def test_cooldown_probe_reaches_the_tripped_provider_again(self) -> None:
        first = RaisingLLM("first")
        second = FakeLLM("second")
        first_breaker = make_breaker(max_failures=1, cooldown_seconds=30.0)
        client = FailoverLLMClient(
            [
                ("first", first, first_breaker),
                ("second", second, make_breaker(max_failures=1)),
            ]
        )
        asyncio.run(client.generate("q"))  # first fails -> tripped, second answers
        self.assertTrue(first_breaker.tripped)
        asyncio.run(client.generate("q"))  # still in cooldown -> first skipped
        self.assertEqual(first.calls, 1)
        first_breaker.cooldown_until = time.time() - 1.0  # probe window opens
        asyncio.run(client.generate("q"))
        self.assertEqual(first.calls, 2)  # probed again
        self.assertTrue(first_breaker.tripped)  # probe failed -> re-tripped

    def test_success_resets_the_breaker(self) -> None:
        flaky = FlakyLLM("flaky", failures=2)
        second = FakeLLM("second")
        flaky_breaker = make_breaker(max_failures=3)
        client = FailoverLLMClient(
            [
                ("flaky", flaky, flaky_breaker),
                ("second", second, make_breaker(max_failures=3)),
            ]
        )
        for _ in range(2):
            self.assertEqual(asyncio.run(client.generate("q")), "উত্তর")  # flaky failed, second answered
        self.assertEqual(flaky_breaker.consecutive_failures, 2)
        self.assertEqual(asyncio.run(client.generate("q")), "উত্তর")  # flaky succeeds now
        self.assertEqual(flaky_breaker.consecutive_failures, 0)
        self.assertEqual(flaky_breaker.cooldown_until, 0.0)

    def test_classify_and_stream_ride_the_chain(self) -> None:
        first = RaisingLLM("first")
        second = FakeLLM("second")
        client = make_failover(("first", first), ("second", second))
        classification = asyncio.run(client.classify_json("q"))
        self.assertEqual(classification["category"], "safe_agri")
        self.assertEqual(asyncio.run(collect_stream(client, "q")), ["উত্তর"])
        self.assertEqual(first.calls, 2)
        self.assertEqual(second.calls, 2)

    def test_single_entry_chain_passthrough(self) -> None:
        only = FakeLLM("only", answer="একমাত্র")
        client = make_failover(("only", only))
        self.assertEqual(asyncio.run(client.generate("q")), "একমাত্র")
        self.assertEqual(client.provider, "only")
        self.assertEqual(client.name, "only")

    def test_all_fail_raises_all_providers_failed(self) -> None:
        client = make_failover(("a", RaisingLLM("a")), ("b", RaisingLLM("b")))
        with self.assertRaises(AllProvidersFailed) as ctx:
            asyncio.run(client.generate("q"))
        # AllProvidersFailed is an LLMError (a RuntimeError), exactly the
        # exception family the application layer already maps to fail-closed.
        self.assertIsInstance(ctx.exception, LLMError)
        self.assertIsInstance(ctx.exception, RuntimeError)
        self.assertIn("failed", str(ctx.exception))

    def test_all_fail_maps_to_fail_closed_generation_path(self) -> None:
        client = make_failover(("a", RaisingLLM("a")), ("b", RaisingLLM("b")))
        generator = GroundedAnswerGenerator(client)
        source = RetrievedSource(id="SRC-1", score=1.0, content_bn="প্রতি লিটার পানিতে ২ মিলি ব্যবহার করুন।")
        result = asyncio.run(generator.generate("q", QueryContext(), [source]))
        # Same fail-closed contract as today's LLMError: referral + error.
        self.assertEqual(result.answer, REFERRAL)
        self.assertEqual(result.mode, "generation_error")
        self.assertIsNotNone(result.error)
        self.assertIn("failed", result.error or "")

    def test_all_fail_maps_to_fail_closed_safety_path(self) -> None:
        # The classifier receives a FailoverLLMClient whose providers all
        # fail: classify_json raises AllProvidersFailed -> LOW_CONFIDENCE.
        client = make_failover(("a", RaisingLLM("a")), ("b", RaisingLLM("b")))
        classifier = SafetyClassifier(client)
        decision = asyncio.run(classifier.classify("q", QueryContext()))
        self.assertEqual(decision.category.value, "low_confidence")
        self.assertTrue(decision.requires_escalation)
        self.assertIn("১৬১২৩", decision.response or "")


class BuilderTests(unittest.TestCase):
    def test_chain_below_two_valid_returns_none(self) -> None:
        self.assertIsNone(build_failover_client(Settings(llm_failover_chain=""), role="generation"))
        self.assertIsNone(build_failover_client(Settings(llm_failover_chain="openrouter"), role="generation"))

    def test_chain_with_two_valid_names_builds_both_entries(self) -> None:
        client = build_failover_client(Settings(llm_failover_chain="openrouter,gemini"), role="generation")
        self.assertIsNotNone(client)
        self.assertEqual([name for name, _, _ in client.chain], ["openrouter", "gemini"])
        self.assertEqual(len(client.chain), 2)

    def test_unknown_names_skipped_with_warning(self) -> None:
        settings = Settings(llm_failover_chain="nonexistent,openrouter")
        with self.assertLogs("krishokchat.failover", level="WARNING") as logs:
            client = build_failover_client(settings, role="generation")
        self.assertTrue(any("nonexistent" in line for line in logs.output))
        # One valid entry -> no wrapper (single-provider behavior), and no crash.
        self.assertIsNone(client)


class ContainerWiringTests(unittest.TestCase):
    def test_two_provider_chain_wraps_generation_but_never_safety(self) -> None:
        container = build_container(Settings(llm_failover_chain="openrouter,gemini"))
        self.assertIsInstance(container.qa.generator.client, FailoverLLMClient)
        self.assertEqual(len(container.qa.generator.client.chain), 2)
        # The safety classifier keeps its direct factory client — the chain
        # must never influence a safety decision.
        self.assertNotIsInstance(container.qa.safety.client, FailoverLLMClient)
        self.assertIsInstance(container.qa.safety.client, OpenAICompatibleClient)
        # The rewrite lane rides the failover client.
        self.assertIsInstance(container.qa.rewriter.llm, FailoverLLMClient)

    def test_empty_chain_keeps_todays_factory_client(self) -> None:
        settings = Settings()
        container = build_container(settings)
        self.assertNotIsInstance(container.qa.generator.client, FailoverLLMClient)
        self.assertIsInstance(container.qa.generator.client, OpenAICompatibleClient)
        self.assertEqual(container.llm_name, settings.openrouter_model)

    def test_unknown_chain_names_do_not_crash_startup(self) -> None:
        settings = Settings(llm_failover_chain="nonexistent,openrouter")
        with self.assertLogs("krishokchat.failover", level="WARNING") as logs:
            container = build_container(settings)
        self.assertTrue(any("nonexistent" in line for line in logs.output))
        # Single valid entry -> today's plain factory client (openrouter).
        self.assertNotIsInstance(container.qa.generator.client, FailoverLLMClient)
        self.assertIsInstance(container.qa.generator.client, OpenAICompatibleClient)
        self.assertEqual(container.llm_name, settings.openrouter_model)


class OfflineQATests(unittest.TestCase):
    def test_single_provider_chain_offline_qa_identical_to_prechange(self) -> None:
        # llm_provider=gemini with no key resolves to the fail-closed
        # UnavailableLLMClient (zero network, instant LLMError). The chain
        # "openrouter" is a single entry, so the container must build exactly
        # the client built today — offline QA behavior is identical.
        query = "ধান চাষে ইউরিয়া সার কতটুকু দেব?"
        base = dict(
            llm_provider="gemini",
            llm_api_key="",
            gemini_api_key="",
            demo_mode=False,
            audit_log_path=str(Path(tempfile.mkdtemp()) / "audit.jsonl"),
        )
        with mock.patch.dict(
            os.environ,
            {key: "" for key in os.environ if key.startswith("GEMINI_API_KEY")},
        ):
            with TestClient(create_app(config=Settings(**base))) as client:
                before = client.post("/api/qa", json={"query": query}).json()
            with TestClient(create_app(config=Settings(llm_failover_chain="openrouter", **base))) as client:
                after = client.post("/api/qa", json={"query": query}).json()
        self.assertEqual(before["category"], after["category"])
        self.assertEqual(before["answer"], after["answer"])
        self.assertEqual(before["category"], "low_confidence")
        self.assertIn("১৬১২৩", after["answer"])


if __name__ == "__main__":
    unittest.main()