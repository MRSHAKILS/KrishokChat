"""Config-driven provider failover chain with per-provider circuit breakers.

T0-06: wraps the existing LLM adapters without modifying them. When the
container has two or more valid providers in ``LLM_FAILOVER_CHAIN``, the
generation lane (and the query-rewrite lane) ride a :class:`FailoverLLMClient`
that skips tripped breakers and falls through to the next provider on failure.
If every provider fails, an :class:`AllProvidersFailed` (an ``LLMError``) is
raised — the application layer already maps ``LLMError`` to its fail-closed
path (safety -> LOW_CONFIDENCE, generation -> referral), so total failure
behaves exactly as today.

The safety classifier is deliberately NOT part of the chain: the container
passes it the direct factory client, never this wrapper.
"""

from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

from app.core.config import Settings
from app.infrastructure.llm.factory import create_llm_client
from app.infrastructure.llm.openai_compatible import LLMError

logger = logging.getLogger("krishokchat.failover")

# Provider names the factory can actually build. "auto" is a resolution rule,
# not a chain entry — it must never appear here.
VALID_CHAIN_PROVIDERS = ("openrouter", "gemini", "ollama")


class AllProvidersFailed(LLMError):
    """Every provider in the failover chain failed.

    Subclasses ``LLMError`` so the application layer's existing fail-closed
    handling (safety -> LOW_CONFIDENCE, generation -> referral) applies with
    zero changes.
    """


@dataclass
class CircuitBreaker:
    """In-memory per-provider breaker (single process, no threads).

    Trips after ``max_failures`` consecutive failures; while tripped the
    provider is skipped. After ``cooldown_seconds`` a probe attempt is
    allowed; a failed probe re-trips, a successful call resets.
    """

    max_failures: int = 3
    cooldown_seconds: float = 30.0
    consecutive_failures: int = 0
    cooldown_until: float = 0.0  # epoch seconds; 0 = never cooldowning

    @property
    def tripped(self) -> bool:
        """True while the breaker is open (cooldown not yet expired)."""
        if self.consecutive_failures < self.max_failures:
            return False
        return time.time() < self.cooldown_until

    def record_failure(self) -> None:
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.max_failures:
            self.cooldown_until = time.time() + self.cooldown_seconds

    def record_success(self) -> None:
        self.consecutive_failures = 0
        self.cooldown_until = 0.0


def parse_chain_names(raw: str) -> list[str]:
    """Split the comma-separated chain, trimming and lowercasing entries."""
    return [name.strip().lower() for name in raw.split(",") if name.strip()]


def _build_chain(settings: Settings, *, role: str) -> list[tuple[str, Any, CircuitBreaker]]:
    """Ordered (provider_name, client, breaker) entries from the config.

    Unknown provider names are logged and skipped — never a startup crash.
    Known-but-unconfigured providers keep the factory's fail-closed behavior
    (e.g. ``UnavailableLLMClient``), which the breaker will trip and skip.
    """
    chain: list[tuple[str, Any, CircuitBreaker]] = []
    for name in parse_chain_names(settings.llm_failover_chain):
        if name not in VALID_CHAIN_PROVIDERS:
            logger.warning(
                "LLM_FAILOVER_CHAIN entry %r is not a known provider (%s); skipping",
                name,
                ", ".join(VALID_CHAIN_PROVIDERS),
            )
            continue
        client = create_llm_client(settings.model_copy(update={"llm_provider": name}), role=role)
        chain.append(
            (
                name,
                client,
                CircuitBreaker(
                    max_failures=settings.llm_circuit_max_failures,
                    cooldown_seconds=settings.llm_circuit_cooldown_seconds,
                ),
            )
        )
    return chain


def build_failover_client(settings: Settings, *, role: str) -> FailoverLLMClient | None:
    """The failover client when the chain has >= 2 valid providers, else None.

    None means the container keeps the exact factory client built today
    (single-provider / empty / all-unknown chains never change behavior).
    """
    chain = _build_chain(settings, role=role)
    if len(chain) < 2:
        return None
    return FailoverLLMClient(chain)


class FailoverLLMClient:
    """LLMClient-port adapter that tries providers in order.

    Same interface as every other adapter (``name``, ``classify_json``,
    ``generate``, ``stream``); only the transport policy differs. Exposes
    ``provider`` (name of the provider that last served) for T0-05 telemetry
    and forwards ``last_usage`` when a serving adapter opts in later.
    """

    def __init__(self, chain: list[tuple[str, Any, CircuitBreaker]]) -> None:
        self.chain = chain
        self.name = chain[0][1].name if chain else "unavailable"
        self.provider: str | None = None
        self.last_usage: dict[str, int] | None = None

    def _mark_served(self, provider_name: str, client: Any) -> None:
        self.provider = provider_name
        self.name = getattr(client, "name", provider_name)
        self.last_usage = getattr(client, "last_usage", None)

    async def _call(self, method: str, *args: Any, **kwargs: Any) -> Any:
        last_error: Exception | None = None
        attempted: list[str] = []
        for provider_name, client, breaker in self.chain:
            if breaker.tripped:
                continue
            attempted.append(provider_name)
            try:
                result = await getattr(client, method)(*args, **kwargs)
            except Exception as exc:
                breaker.record_failure()
                last_error = exc
                logger.warning("provider %r failed on %s: %s", provider_name, method, exc)
                continue
            breaker.record_success()
            self._mark_served(provider_name, client)
            return result
        raise AllProvidersFailed(
            f"All {len(attempted)} provider(s) failed for {method}: {last_error}"
        ) from last_error

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        return await self._call("classify_json", prompt)

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        return await self._call("generate", prompt, metadata=metadata)

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        last_error: Exception | None = None
        attempted: list[str] = []
        for provider_name, client, breaker in self.chain:
            if breaker.tripped:
                continue
            attempted.append(provider_name)
            try:
                async for chunk in client.stream(prompt, metadata=metadata):
                    yield chunk
            except Exception as exc:
                breaker.record_failure()
                last_error = exc
                logger.warning("provider %r failed on stream: %s", provider_name, exc)
                continue
            breaker.record_success()
            self._mark_served(provider_name, client)
            return
        raise AllProvidersFailed(
            f"All {len(attempted)} provider(s) failed for stream: {last_error}"
        ) from last_error