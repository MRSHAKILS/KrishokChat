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


import json
import logging
from pathlib import Path

logger = logging.getLogger("krishokchat.telemetry")

_CACHED_PRICES: dict[str, dict[str, Any]] | None = None


def load_model_prices(path: Path | str | None = None) -> dict[str, dict[str, Any]]:
    """Load model pricing table from disk with fail-open caching.

    Returns a mapping of model/provider keys to pricing entries.
    Missing or unreadable file returns empty dict (estimate_cost falls back to None).
    """
    global _CACHED_PRICES
    if path is None and _CACHED_PRICES is not None:
        return _CACHED_PRICES

    try:
        from app.core.config import settings
        resolved_path = Path(path) if path is not None else settings.model_prices_resolved_path
    except Exception:
        resolved_path = Path("backend/config/model_prices.json")

    try:
        with open(resolved_path, encoding="utf-8") as fh:
            data = json.load(fh)
            prices = data.get("prices", {})
            if path is None:
                _CACHED_PRICES = prices
            return prices
    except (FileNotFoundError, OSError, json.JSONDecodeError) as exc:
        logger.debug("model_prices table not available at %s (%s)", resolved_path, exc)
        return {}


def estimate_cost(
    tokens: dict[str, int] | None,
    provider: str | None,
    model: str | None = None,
    price_table: dict[str, dict[str, Any]] | None = None,
) -> float | None:
    """Estimated USD cost, or None when token usage or pricing is unavailable.

    Calculation: (input_tokens / 1000) * input_usd_per_1k + (output_tokens / 1000) * output_usd_per_1k.
    Returns None if tokens are missing or the model/provider is not in the price table.
    """
    if not isinstance(tokens, dict):
        return None
    input_tokens = tokens.get("input")
    output_tokens = tokens.get("output")
    if not isinstance(input_tokens, (int, float)) or not isinstance(output_tokens, (int, float)):
        return None

    prices = price_table if price_table is not None else load_model_prices()
    if not prices:
        return None

    # Search candidates: "provider/model", "model", "provider"
    entry = None
    if provider and model:
        entry = prices.get(f"{provider.lower()}/{model.lower()}") or prices.get(f"{provider.lower()}/{model}")
    if entry is None and model:
        entry = prices.get(model.lower()) or prices.get(model)
    if entry is None and provider:
        entry = prices.get(provider.lower()) or prices.get(provider)

    if entry is None:
        return None

    input_rate = float(entry.get("input_usd_per_1k", 0.0))
    output_rate = float(entry.get("output_usd_per_1k", 0.0))
    cost = (input_tokens / 1000.0) * input_rate + (output_tokens / 1000.0) * output_rate
    return round(cost, 8)


def current_request_id() -> str | None:
    """The T0-04 request ID from the middleware's contextvar, when present."""
    return request_id_var.get() or None