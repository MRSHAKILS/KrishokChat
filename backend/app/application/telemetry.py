"""T0-05: per-stage latency + token/provider/cost telemetry helpers.

Everything here is additive-only: consumers must keep tolerating audit records
written before these fields existed (None/absent keys), and no existing audit
field changes.

Conventions for the LLM lane:
- ``last_usage``: a dict with integer ``input``/``output`` keys. Today no
  checked-in adapter exposes it (OpenRouter and Gemini responses do carry
  usage, but the adapters discard it and ``infrastructure/llm/`` is out of
  scope for T0-05), so ``tokens`` stays null in production until a lane
  opts in — no fabrication.
- ``provider``: a string naming the provider that actually served the call.
  No adapter exposes it yet (T0-06 failover will need it); until then the
  pipeline falls back to the configured ``LLM_PROVIDER``.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from app.core.logging import request_id_var

# Contract keys — exactly these four stage names, in the order the pipeline
# runs them. Consumers rely on the spelling; do not rename.
STAGE_NAMES = ("safety", "retrieval", "generation", "verifier")


@contextmanager
def stage_timer(name: str, timings: dict[str, float]) -> Iterator[None]:
    """Time one pipeline stage into ``timings[name]`` (wall-clock ms).

    The caller pre-seeds ``timings`` with every stage name so the audit record
    always carries all four keys; a stage that did not run stays at its seed
    value (0.0), which is honest telemetry for a skipped/terminal path (the
    trace already records the SKIP status that explains it).
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        timings[name] = round((time.perf_counter() - start) * 1000.0, 4)


def capture_tokens(lane: Any) -> dict[str, int] | None:
    """Token counts when the lane exposes them; None otherwise.

    Source: ``lane.last_usage`` — a dict with integer ``input``/``output``
    keys. Anything else (absent attribute, non-dict, missing/wrong-typed
    keys) yields None: unknown usage is never guessed.
    """
    usage = getattr(lane, "last_usage", None)
    if not isinstance(usage, dict):
        return None
    input_tokens = usage.get("input")
    output_tokens = usage.get("output")
    if not isinstance(input_tokens, int) or not isinstance(output_tokens, int):
        return None
    return {"input": input_tokens, "output": output_tokens}


def serving_provider(lane: Any, fallback: str | None) -> str | None:
    """The provider that actually served the generation call.

    A lane may expose a ``provider`` attribute (the seam T0-06 failover will
    need); otherwise the configured ``LLM_PROVIDER`` is the honest answer —
    there is no failover today, so the configured provider is the one that
    served. NOTE: the local registry lane (krishokchat-4b via llama-server)
    currently reports the global configured provider; a per-lane ``provider``
    attribute is the fix once infrastructure/llm/ is in scope again.
    """
    return getattr(lane, "provider", None) or fallback


def estimate_cost(tokens: dict[str, int] | None, provider: str | None) -> float | None:
    """Estimated USD cost, or None when no real price basis exists.

    NO price table is wired anywhere in this codebase (backend/ and docs/ were
    searched; no per-provider pricing data exists), so this always returns
    None. When a real price basis lands (a checked-in price table per
    provider/model), add it HERE with a one-line comment citing its source —
    never invent a number.
    """
    return None


def current_request_id() -> str | None:
    """The T0-04 request ID from the middleware's contextvar, when present."""
    return request_id_var.get() or None