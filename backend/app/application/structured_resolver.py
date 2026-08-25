"""R4 — T1/T2 Structured Resolver.

Inserts into the pipeline AFTER the demo cache replay check and BEFORE
retrieval. Only runs when STRUCTURED_RESOLVER_ENABLED=true; otherwise
returns None immediately (zero cost, zero behavior change).

Design rules (from R4 spec):
  - Deterministic matcher only (no LLM in R4 — that's R5's routing enhancement).
  - A query resolves to T1/T2 only when BOTH crop AND problem match a fact
    row with confidence >= threshold. Anything ambiguous → None → T3.
  - Bias toward missing to T3 (safe, just costs an LLM call) over a wrong
    structured answer.
  - No network call, no LLM call, no I/O after construction.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.domain.advisory_templates import render_t1, render_t2
from app.domain.contracts import RetrievedSource
from app.domain.enums import ResolutionTier
from app.domain.fact_base import Fact, FactBase


# ---------------------------------------------------------------------------
# Keyword aliases for deterministic crop/problem matching
# ---------------------------------------------------------------------------

# These are the only aliases the R4 resolver recognises.  Wider matching is
# R5 + R6's job.  Every alias must be attested (not invented).
_CROP_ALIASES: dict[str, list[str]] = {
    "potato": ["potato", "আলু", "aloo", "alu"],
}

_PROBLEM_ALIASES: dict[str, list[str]] = {
    "late_blight": [
        "late blight", "late_blight",
        "নাবি ধ্বসা", "নাবি ব্লাইট", "লেট ব্লাইট",
        "মড়ক",  # common Bangla shorthand for late blight on potato
    ],
}

# Map alias (lowered) → canonical key, built once.
_CROP_LOOKUP: dict[str, str] = {
    alias.lower(): crop
    for crop, aliases in _CROP_ALIASES.items()
    for alias in aliases
}
_PROBLEM_LOOKUP: dict[str, str] = {
    alias.lower(): problem
    for problem, aliases in _PROBLEM_ALIASES.items()
    for alias in aliases
}


def _match_crop(query: str) -> str | None:
    """Return a canonical crop key if one is confidently matched, else None."""
    q = query.lower()
    for alias, crop in _CROP_LOOKUP.items():
        if alias in q:
            return crop
    return None


def _match_problem(query: str) -> str | None:
    """Return a canonical problem key if one is confidently matched, else None."""
    q = query.lower()
    for alias, problem in _PROBLEM_LOOKUP.items():
        if alias in q:
            return problem
    return None


# ---------------------------------------------------------------------------
# ResolvedAnswer — what the resolver returns on a hit
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResolvedAnswer:
    """A T1 or T2 answer produced without any LLM call."""

    answer: str
    fact: Fact
    tier: ResolutionTier  # STRUCTURED_FACT (T1) or TEMPLATED_ADVISORY (T2)


# ---------------------------------------------------------------------------
# StructuredResolver
# ---------------------------------------------------------------------------


class StructuredResolver:
    """Deterministic structured resolver for T1/T2 answers.

    Constructed by the container when STRUCTURED_RESOLVER_ENABLED=true.
    Holds a FactBase and (optionally) a CropCalendarLibrary for stage notes.

    ``resolve(query)`` is pure: no I/O, no LLM, no network.
    """

    def __init__(
        self,
        fact_base: FactBase,
        crop_calendars=None,  # CropCalendarLibrary | None (avoid import cycle)
        min_confidence: float = 0.85,
    ) -> None:
        self.fact_base = fact_base
        self.crop_calendars = crop_calendars
        self.min_confidence = min_confidence

    def resolve(self, query: str, stage: str | None = None) -> ResolvedAnswer | None:
        """Try to resolve *query* to a T1/T2 answer.

        Returns ``None`` on any miss — the pipeline then falls through to T3
        exactly as today.  A miss is correct when the query is ambiguous; T3
        is safe, not an error.

        *stage* is an optional growth-stage hint from ``farmer_context``.
        """
        crop = _match_crop(query)
        if crop is None:
            return None

        problem = _match_problem(query)
        if problem is None:
            return None

        # Prefer stage-specific fact; fall back to any matching stage.
        facts: list[Fact] = []
        if stage:
            facts = self.fact_base.lookup(crop, problem, stage=stage)
        if not facts:
            facts = self.fact_base.lookup(crop, problem)

        if not facts:
            return None

        # Reject if confidence is below the configured threshold.
        best = facts[0]
        if best.confidence < self.min_confidence:
            return None

        # Get stage advisory note from calendars (optional enrichment).
        stage_advisory_bn: str | None = None
        if self.crop_calendars is not None:
            try:
                effective_stage = stage or best.stage
                cal_crop = self.crop_calendars.get_crop(crop)
                if cal_crop:
                    for cal_stage in cal_crop.get("stages", []):
                        if cal_stage.get("key") == effective_stage:
                            stage_advisory_bn = cal_stage.get("advisory_bn") or None
                            break
            except Exception:
                pass  # Calendar unavailable → T1 fallback (not a failure)

        # Choose tier: T2 when IPM alternatives or stage advisory available, T1 otherwise.
        if best.ipm_alternatives_bn or stage_advisory_bn:
            answer = render_t2(best, stage_advisory_bn=stage_advisory_bn)
            tier = ResolutionTier.TEMPLATED_ADVISORY
        else:
            answer = render_t1(best)
            tier = ResolutionTier.STRUCTURED_FACT

        return ResolvedAnswer(answer=answer, fact=best, tier=tier)

    def _no_llm_assert(self) -> None:
        """Called in tests to assert no LLM method was touched.  No-op here."""
