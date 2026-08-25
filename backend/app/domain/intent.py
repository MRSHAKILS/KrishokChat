"""R5 — Intent domain object and keyword-first extraction.

Intent is an advisory routing hint produced alongside the safety decision.
It is **never load-bearing for safety** — a missing or malformed intent block
must not change the safety category, and a terminal safety decision (T0/T4)
carries no intent (None is the correct value there).

Five fields mirror the structured classifier output (R5 spec §Design):
  kind      — treatment | prevention | fertilizer | general_info
  crop      — normalised crop string from the query (None if absent)
  problem   — disease/pest name (None if absent)
  stage     — growth stage hint (None if absent)
  upazila   — geographic sub-district (None if absent)
  source    — how intent was resolved: "keyword" | "llm" | "none"

``keyword_intent`` lifts the existing keyword scan from
``services/advisory/intent_classifier.py`` into a pure, testable function.
It runs BEFORE the LLM call; if it resolves the kind confidently the LLM
block is used only for crop/problem/stage/upazila enrichment, never to
override a confident keyword match.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    """Advisory routing hint produced alongside the safety decision.

    All fields are optional — absent = could not determine, not wrong.
    The ``source`` field records how ``kind`` was resolved:
      "keyword"  — deterministic keyword match (0 LLM cost)
      "llm"      — resolved from the LLM's intent block
      "none"     — no intent could be determined
    """

    kind: str | None = None          # treatment | prevention | fertilizer | general_info
    crop: str | None = None
    problem: str | None = None
    stage: str | None = None
    upazila: str | None = None
    source: str = "none"             # "keyword" | "llm" | "none"


# ---------------------------------------------------------------------------
# Keyword-first intent extraction
# ---------------------------------------------------------------------------

# Treatment keywords (Bengali + Banglish + English)
_TREATMENT_KW = (
    "প্রতিকার", "চিকিৎসা", "ওষুধ", "কীটনাশক", "ছত্রাকনাশক",
    "স্প্রে", "প্রয়োগ", "দাও", "treatment", "cure", "spray", "apply",
    "fungicide", "pesticide", "medicine",
)

# Prevention keywords
_PREVENTION_KW = (
    "প্রতিরোধ", "রোধ", "বাঁচানো", "আগে থেকে", "prevent", "protection",
    "prevention", "রক্ষা", "সুরক্ষা",
)

# Fertilizer keywords
_FERTILIZER_KW = (
    "সার", "ইউরিয়া", "পটাশ", "ফসফেট", "জৈব সার",
    "fertilizer", "fertiliser", "urea", "npk", "potash", "compost",
)


def keyword_intent(query: str) -> Intent | None:
    """Return a keyword-resolved Intent, or None if no keyword matches.

    Rules (deterministic, top-to-bottom):
    1. If a treatment keyword is present → ``kind="treatment"``.
    2. Else if a prevention keyword is present → ``kind="prevention"``.
    3. Else if a fertilizer keyword is present → ``kind="fertilizer"``.
    4. None → caller will use LLM block or fall back to ``general_info``.

    Only ``kind`` is set here; ``crop``, ``problem``, ``stage``, ``upazila``
    are enriched from the LLM's intent block in ``SafetyClassifier.classify``.
    """
    lowered = query.lower()

    if any(kw in lowered for kw in _TREATMENT_KW):
        return Intent(kind="treatment", source="keyword")
    if any(kw in lowered for kw in _PREVENTION_KW):
        return Intent(kind="prevention", source="keyword")
    if any(kw in lowered for kw in _FERTILIZER_KW):
        return Intent(kind="fertilizer", source="keyword")
    return None
