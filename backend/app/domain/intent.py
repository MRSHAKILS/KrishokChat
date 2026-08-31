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

    kind: str | None = None          # treatment | prevention | fertilizer | general_info | diagnosis
    crop: str | None = None
    problem: str | None = None
    stage: str | None = None
    upazila: str | None = None
    plant_part: str | None = None    # leaf | stem | root | fruit | flower | whole_plant
    problem_type: str | None = None  # disease | pest | fertilizer | weather | general
    is_ambiguous: bool = False
    clarification_question_bn: str | None = None
    suggested_crops: tuple[str, ...] = ()
    source: str = "none"             # "keyword" | "llm" | "none"


# ---------------------------------------------------------------------------
# Keyword-first intent extraction
# ----------------------------------------------------# Treatment keywords (Bengali + Banglish + Regional Dialects + English)
_TREATMENT_KW = (
    "প্রতিকার", "চিকিৎসা", "ওষুধ", "ঔষধ", "কীটনাশক", "ছত্রাকনাশক",
    "স্প্রে", "প্রয়োগ", "দাও", "কী দেব", "কী দিব", "কী করব", "কী করমু", "কী করুম",
    "দমন", "সমাধান", "উপায়", "উপায়", "করণীয়", "করনীয়", "বাঁচাব", "বাঁচানো",
    "বাঁচামু", "দাবা", "বিখ", "কী করণ যায়", "কি করমু",
    "treatment", "cure", "spray", "apply", "shomadhan", "bachamu", "kormu", "osudh", "dava",
    "fungicide", "pesticide", "medicine",
)

# Prevention keywords
_PREVENTION_KW = (
    "প্রতিরোধ", "রোধ", "বাঁচানো", "আগে থেকে", "prevent", "protection",
    "prevention", "রক্ষা", "সুরক্ষা", "আগে থিকা", "বাঁচাইয়া রাখা",
)

# Fertilizer keywords
_FERTILIZER_KW = (
    "সার", "ইউরিয়া", "পটাশ", "ফসফেট", "জৈব সার", "কম্পোস্ট", "shaar",
    "fertilizer", "fertiliser", "urea", "npk", "potash", "compost", "সার দেওন",
)

# Plant part keywords
_PLANT_PART_MAP = {
    "পাতা": "leaf", "পাতায়": "leaf", "পাতাত": "leaf", "পাতার": "leaf", "leaf": "leaf", "leaves": "leaf", "pata": "leaf", "patat": "leaf",
    "কাণ্ড": "stem", "কান্ড": "stem", "ডাল": "stem", "stem": "stem", "branch": "stem",
    "মূল": "root", "শিকড়": "root", "শিকড়": "root", "root": "root",
    "ফল": "fruit", "ফলে": "fruit", "fruit": "fruit", "fol": "fruit",
    "ফুল": "flower", "ফুলে": "flower", "flower": "flower",
    "শীষ": "panicle", "grain": "grain", "দানা": "grain", "shish": "panicle",
    "গাছ": "whole_plant", "গাছে": "whole_plant", "গাছের": "whole_plant", "plant": "whole_plant", "gach": "whole_plant", "gache": "whole_plant",
}

_PLANT_PART_BN = {
    "leaf": "পাতায়",
    "stem": "কাণ্ডে",
    "root": "শিকড়ে",
    "fruit": "ফলে",
    "flower": "ফুলে",
    "panicle": "শীষে",
    "grain": "দানায়",
    "whole_plant": "গাছে",
}


# Crop aliases for deterministic keyword detection
_CROP_ALIASES: dict[str, list[str]] = {
    "potato": ["potato", "আলু", "আলুর", "আলুত", "aloo", "alu", "aloor"],
    "maize": ["maize", "corn", "ভুট্টা", "ভুট্টায়", "ভুট্তার", "ভুট্টা ফসলে", "bhutta", "makai"],
    "rice": ["rice", "ধান", "ধানের", "ধানক্ষেত", "ধান ক্ষেতে", "ধানর", "ধানত", "dhan", "paddy", "dhanor"],
    "tomato": ["tomato", "টমেটো", "টমেটোর", "টমাটো", "টমাটোর"],
    "wheat": ["wheat", "গম", "গমের", "গমে", "গমর"],
    "brinjal": ["brinjal", "eggplant", "বেগুন", "বেগুনের", "বেগুনর", "বেগুন গাছের", "বাইঙ্গন", "baingon", "begun", "beguner"],
    "chilli": ["chilli", "chili", "মরিচ", "মরিচের", "মরিচর", "মরিস", "মরিসর", "moris", "morisor", "morich"],
    "cabbage": ["cabbage", "বাঁধাকপি", "বাঁধাকপির", "পাতাকপি", "বাধাকপি"],
    "cauliflower": ["cauliflower", "ফুলকপি", "ফুলকপির"],
}


CROP_NAMES_BN: dict[str, str] = {
    "potato": "আলু",
    "rice": "ধান",
    "wheat": "গম",
    "maize": "ভুট্টা",
    "tomato": "টমেটো",
    "brinjal": "বেগুন",
    "chilli": "মরিচ",
    "cabbage": "বাঁধাকপি",
    "cauliflower": "ফুলকপি",
}


def _match_crop_alias(lowered: str) -> str | None:
    for crop, aliases in _CROP_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            return crop
    return None


def normalize_crop_name(crop: str | None) -> str | None:
    if not crop:
        return None
    c = crop.strip().lower()
    if c in ("corn", "maize"):
        return "maize"
    if c in ("eggplant", "brinjal"):
        return "brinjal"
    if c in ("paddy", "rice"):
        return "rice"
    return _match_crop_alias(c) or c


def detect_cross_modal_conflict(
    image_crop: str | None, query: str
) -> tuple[bool, str | None, str | None, str | None]:
    """Detect if an uploaded photo crop contradicts the user's text query.

    Returns:
        (has_conflict, image_crop_norm, query_crop_norm, clarification_prompt_bn)
    """
    if not image_crop or not query:
        return False, None, None, None

    img_norm = normalize_crop_name(image_crop)
    query_norm = _match_crop_alias(query.lower())

    if img_norm and query_norm and img_norm != query_norm:
        img_bn = CROP_NAMES_BN.get(img_norm, img_norm.title())
        query_bn = CROP_NAMES_BN.get(query_norm, query_norm.title())
        prompt = (
            f"আপনি {img_bn} গাছের ছবি দিয়েছেন, কিন্তু বার্তায় {query_bn}-এর কথা উল্লেখ করেছেন। "
            f"আপনি কোন ফসলের সমস্যার জন্য পরামর্শ চাচ্ছেন? ({img_bn} নাকি {query_bn}?)"
        )
        return True, img_norm, query_norm, prompt

    return False, img_norm, query_norm, None


def keyword_intent(query: str) -> Intent | None:
    """Return a keyword-resolved Intent, or None if no keyword matches.

    Rules (deterministic, top-to-bottom):
    1. If a treatment keyword is present → ``kind="treatment"``.
    2. Else if a prevention keyword is present → ``kind="prevention"``.
    3. Else if a fertilizer keyword is present → ``kind="fertilizer"``.
    4. None → caller will use LLM block or fall back to ``general_info``.

    Also deterministically resolves ``crop``, ``plant_part``, and ``is_ambiguous``.
    """
    lowered = query.lower()

    kind: str | None = None
    if any(kw in lowered for kw in _TREATMENT_KW):
        kind = "treatment"
    elif any(kw in lowered for kw in _PREVENTION_KW):
        kind = "prevention"
    elif any(kw in lowered for kw in _FERTILIZER_KW):
        kind = "fertilizer"

    if kind is None:
        return None

    detected_part: str | None = None
    for alias, part in _PLANT_PART_MAP.items():
        if alias in lowered:
            detected_part = part
            break

    detected_crop = _match_crop_alias(lowered)

    # An advisory/treatment/prevention/fertilizer query without any crop is ambiguous by definition
    is_ambiguous = (detected_crop is None)
    clarification_prompt = None
    if is_ambiguous:
        part_bn = _PLANT_PART_BN.get(detected_part or "", "")
        part_text = f"{part_bn} " if part_bn else ""
        if kind == "fertilizer":
            clarification_prompt = "কোন ফসলের সার প্রয়োগ বা মাত্রা সম্পর্কে জানতে চাচ্ছেন বলবেন কি? (যেমন: ধান, আলু, বা ভুট্টা)"
        else:
            clarification_prompt = f"কোন ফসলের {part_text}এই সমস্যা হয়েছে বলবেন কি? (যেমন: আলু, ধান, বা টমেটো)"

    return Intent(
        kind=kind,
        crop=detected_crop,
        plant_part=detected_part,
        is_ambiguous=is_ambiguous,
        clarification_question_bn=clarification_prompt,
        source="keyword",
    )
