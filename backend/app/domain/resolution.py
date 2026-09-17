"""Resolution-tier taxonomy and assignment logic (R3).

This is the **single source of truth** for how an answer was produced.
No caller may hardcode a tier string — call ``tier_for`` instead.

Five tiers define the five-tier resolution ladder:

  T0  deterministic_guard   — a precheck rule matched; 0 LLM calls
  T1  structured_fact       — answered from a provenance-carrying fact row; 0 LLM calls  (R4)
  T2  templated_advisory    — template filled from fact rows; 0 LLM calls                (R4)
  T3  grounded_generation   — retrieval → LLM generation → verifier; 1-2 LLM calls
  T4  honest_refusal        — classifier or coverage-gate refusal; 0-1 LLM calls

T1/T2 are defined here now so the audit schema never changes when R4 lands.

``ZERO_LLM_TIERS`` is the shared definition used by metrics code, tests, and
the R7 cost experiment — never recompute it elsewhere.

``TIER_LABELS_BN`` maps each tier to the Bengali badge text shown to the
farmer.  The label describes *who authored the answer*, not the internal name.
"""

from __future__ import annotations

from app.domain.enums import ResolutionTier, SafetyCategory


def tier_for(
    *,
    category: SafetyCategory,
    matched_rules: tuple[str, ...] = (),
    generated: bool = False,
) -> ResolutionTier:
    """Return the resolution tier for a completed pipeline request.

    Rules (deterministic, evaluated top-to-bottom):

    - A terminal decision with at least one matched precheck rule → T0.
      (The rule is the proof; no LLM classification was needed.)
    - A terminal decision with no matched rules → T4.
      (LLM classifier decided, or a coverage-gate / outage path refused.)
    - A safe_agri decision that reached generation → T3.
    - A safe_agri decision that did not reach generation → T4.
      (Pipeline error or empty-sources referral before generation ran.)

    T1 and T2 are not assigned here; R4 will call ``tier_for`` with those
    values when the structured resolver exists.
    """
    if category is not SafetyCategory.SAFE_AGRI:
        # Terminal path.
        if matched_rules:
            return ResolutionTier.DETERMINISTIC_GUARD  # T0
        return ResolutionTier.HONEST_REFUSAL  # T4

    # Safe-agri path.
    if generated:
        return ResolutionTier.GROUNDED_GENERATION  # T3
    return ResolutionTier.HONEST_REFUSAL  # T4


# ---------------------------------------------------------------------------
# Shared constants — used by metrics, cost experiment (R7), and tests.
# ---------------------------------------------------------------------------

#: Tiers that consumed zero LLM calls.  Used to compute ``zero_llm_rate``.
#: Keep in sync with the tier definitions above.
ZERO_LLM_TIERS: frozenset[ResolutionTier] = frozenset({
    ResolutionTier.DETERMINISTIC_GUARD,
    ResolutionTier.STRUCTURED_FACT,
    ResolutionTier.TEMPLATED_ADVISORY,
})

#: Bengali badge labels: tells the farmer *who authored* the answer.
TIER_LABELS_BN: dict[ResolutionTier, str] = {
    ResolutionTier.DETERMINISTIC_GUARD: "নিরাপত্তা নিয়ম (এআই ব্যবহার হয়নি)",
    ResolutionTier.STRUCTURED_FACT: "অনুমোদিত তথ্যসারণি (এআই ব্যবহার হয়নি)",
    ResolutionTier.TEMPLATED_ADVISORY: "অনুমোদিত তথ্যসারণি (এআই ব্যবহার হয়নি)",
    ResolutionTier.GROUNDED_GENERATION: "সূত্রভিত্তিক এআই উত্তর",
    ResolutionTier.PROGRESSIVE_GUIDANCE: "পরিবেশবান্ধব ও সাধারণ পরিচর্যা (নন-কেমিক্যাল)",
    ResolutionTier.HONEST_REFUSAL: "উত্তর দেওয়া হয়নি",
    ResolutionTier.INTERACTIVE_CLARIFICATION: "তথ্য স্পষ্টকরণ (স্লট যাচাই)",
}
