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


# Crop aliases for deterministic keyword detection (45 crops).
# Single-word aliases match at the START of a whitespace-delimited token
# (Bengali vowel signs defeat \b, so plain substring matching fires inside
# unrelated words, e.g. rice "ধান" inside "সমাধান" = solution). Inflected
# forms (ধানের/আলুর) match; multi-word aliases use substring matching.
# SHORT_EXACT_CROPS match single-word aliases by exact token equality only:
# 2-character names share prefixes with pronouns and common words
# (আম vs আমার/আমি, জাম vs জামা). NEGATIVE_CROP_TOKENS are generic
# collective nouns that never denote a specific crop.
_CROP_ALIASES: dict[str, list[str]] = {
    "potato": ["potato", "আলু", "আলুর", "আলুত", "aloo", "alu", "aloor"],
    "maize": ["maize", "corn", "ভুট্টা", "ভুট্টায়", "ভুট্তার", "ভুট্টা ফসলে", "bhutta", "makai"],
    "rice": ["rice", "ধান", "ধানের", "ধানক্ষেত", "ধান ক্ষেতে", "ধানর", "ধানত", "dhan", "dhaner", "paddy", "dhanor"],
    "tomato": ["tomato", "tomator", "টমেটো", "টমেটোর", "টমাটো", "টমাটোর"],
    "wheat": ["wheat", "গম", "গমের", "গমে", "গমর", "gomer"],
    "brinjal": ["brinjal", "eggplant", "বেগুন", "বেগুনের", "বেগুনর", "বেগুন গাছের", "বাইঙ্গন", "baingon", "begun", "beguner"],
    "chilli": ["chilli", "chili", "মরিচ", "মরিচের", "মরিচর", "মরিস", "মরিসর", "লঙ্কা", "লংকা", "moris", "morisor", "morich", "moricer"],
    "cabbage": ["cabbage", "বাঁধাকপি", "বাঁধাকপির", "পাতাকপি", "বাধাকপি"],
    "cauliflower": ["cauliflower", "ফুলকপি", "ফুলকপির"],
    "mango": ["আম", "আমের", "আমে", "আমটি", "আমগুলো", "আমগাছ", "আমগাছে", "আমগাছের", "আমবাগান", "আমবাগানে", "আম্রপালি", "আম্রপালির", "aam", "mango"],
    "papaya": ["পেঁপে", "পেপে", "পেঁপের", "পেপের", "পেঁপেগাছ", "পেঁপেতে", "pepe", "papaw", "pawpaw", "papaya"],
    "mustard": ["সরিষা", "সরষে", "সরিষার", "সরষের", "সরিষায়", "সরিষাক্ষেত", "সরিষা ক্ষেত", "shorisha", "sorisha", "mustard"],
    "cucumber": ["শসা", "শসার", "শসাগাছ", "শসাক্ষেত", "shosha", "cucumber"],
    "coconut": ["নারকেল", "নারিকেল", "নারকেলের", "নারিকেলের", "নারকেলগাছ", "ডাব", "ডাবের", "coconut", "narkel", "dab"],
    "lemon": ["লেবু", "লেবুর", "লেবুগাছ", "লেবুবাগান", "lebu", "lemon"],
    "guava": ["পেয়ারা", "পেয়ারা", "পেয়ারার", "পেয়ারার", "পেয়ারাগাছ", "peyara", "guava"],
    "banana": ["কলা", "কলার", "কলাগাছ", "কলাবাগান", "kola", "banana"],
    "bottle_gourd": ["লাউ", "লাউয়ের", "লাউতে", "লাউগাছ", "lau", "bottle gourd"],
    "watermelon": ["তরমুজ", "তরমুজের", "তরমুজগাছ", "tormuj", "watermelon"],
    "mushroom": ["মাশরুম", "মাশরুমের", "মাশরুমচাষ", "mashroom", "mushroom"],
    "jackfruit": ["কাঁঠাল", "কাঠাল", "কাঁঠালের", "কাঠালের", "কাঁঠালগাছ", "kathal", "jackfruit"],
    "jute": ["পাট", "পাটের", "পাটে", "পাটক্ষেত", "পাটখেতে", "jute"],
    "strawberry": ["স্ট্রবেরি", "স্ট্রবেরির", "স্ট্রবেরিগাছ", "strawberry"],
    "bamboo": ["বাঁশ", "বাঁশের", "বাঁশঝাড়", "বাঁশঝাড়ে", "bash", "bamboo"],
    "cashew": ["কাজুবাদাম", "কাজুবাদামের", "কাজুবাদামগাছ", "কাজু", "কাজুর", "কাজুগাছ", "kaju", "cashew"],
    "okra": ["ঢেঁড়স", "ঢেঁড়শ", "ঢেঁড়সের", "ঢেঁড়শের", "ঢেঁড়সগাছ", "ঢ্যাঁড়স", "ঢ্যাঁড়সের", "dherosh", "okra"],
    "betelnut": ["সুপারি", "সুপারির", "সুপারিগাছ", "supari", "betelnut"],
    "beans": ["শিম", "শিমের", "শিমগাছ", "বরবটি", "বরবটির", "বরবটিগাছ", "shim", "borboti", "beans"],
    "onion": ["পেঁয়াজ", "পিঁয়াজ", "পেঁয়াজের", "পিঁয়াজের", "পেঁয়াজগাছ", "peyaj", "piyaj", "onion"],
    "rose": ["গোলাপ", "গোলাপের", "গোলাপগাছ", "golap", "rose"],
    "grape": ["আঙুর", "আঙুরের", "আঙুরগাছ", "angur", "angor", "grape"],
    "pineapple": ["আনারস", "আনারসের", "আনারসগাছ", "anarosh", "pineapple"],
    "pomegranate": ["ডালিম", "ডালিমের", "ডালিমগাছ", "আনার", "আনারের", "dalim", "anar", "pomegranate"],
    "stem_amaranth": ["ডাঁটা", "ডাঁটার", "ডাঁটাগাছ", "ডাটা", "ডাটার", "ডাটাগাছ", "danta"],
    "leafy_greens": ["শাক", "শাকের", "শাকে", "shak"],
    "turmeric": ["হলুদগাছ", "হলুদগাছের", "হলুদ চাষ", "হলুদচাষ", "holud", "turmeric"],
    "litchi": ["লিচু", "লিচুর", "লিচুগাছ", "lichu", "litchi", "lychee"],
    "jamun": ["জাম", "জামের", "জামে", "জামগাছ", "jam", "jamun"],
    "ata": ["আতা", "আতার", "আতায়", "আতাগাছ", "ata"],
    "gladiolus": ["গ্ল্যাডিওলাস", "গ্ল্যাডিওলাসের", "gladiolus"],
    "bitter_gourd": ["করলা", "করলার", "করলাগাছ", "korola", "bitter gourd"],
    "hog_plum": ["আমড়া", "আমড়ার", "আমড়াগাছ", "amra", "hog plum"],
    "dragon_fruit": ["ড্রাগন", "ড্রাগনের", "ড্রাগন ফল", "ড্রাগনফল", "dragon", "dragonfruit", "dragon fruit"],
    "pomelo": ["জাম্বুরা", "জাম্বুরার", "জাম্বুরাগাছ", "বাতাবি", "বাতাবিলেবু", "jambura", "pomelo"],
    "akashmoni": ["আকাশমণি", "আকাশমণির", "আকাশমনি", "আকাশমনির", "akashmoni"],
}

# Crops whose single-word aliases match by exact token equality only.
SHORT_EXACT_CROPS = frozenset({"mango", "jamun", "ata", "jute"})

# Generic collective nouns and disease words that never denote a crop.
# "মরিচা" (moricha) = rust disease (e.g. সাদা মরিচা = white rust), never chilli crop.
NEGATIVE_CROP_TOKENS = frozenset({"শাকসবজি", "মরিচা", "মরিচায়", "মরিচার", "মরিচাতে", "মরিচাধরা"})


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
    "mango": "আম",
    "papaya": "পেঁপে",
    "mustard": "সরিষা",
    "cucumber": "শসা",
    "coconut": "নারকেল",
    "lemon": "লেবু",
    "guava": "পেয়ারা",
    "banana": "কলা",
    "bottle_gourd": "লাউ",
    "watermelon": "তরমুজ",
    "mushroom": "মাশরুম",
    "jackfruit": "কাঁঠাল",
    "jute": "পাট",
    "strawberry": "স্ট্রবেরি",
    "bamboo": "বাঁশ",
    "cashew": "কাজুবাদাম",
    "okra": "ঢেঁড়স",
    "betelnut": "সুপারি",
    "beans": "শিম",
    "onion": "পেঁয়াজ",
    "rose": "গোলাপ",
    "grape": "আঙুর",
    "pineapple": "আনারস",
    "pomegranate": "ডালিম",
    "stem_amaranth": "ডাঁটা",
    "leafy_greens": "শাক",
    "turmeric": "হলুদ",
    "litchi": "লিচু",
    "jamun": "জাম",
    "ata": "আতা",
    "gladiolus": "গ্ল্যাডিওলাস",
    "bitter_gourd": "করলা",
    "hog_plum": "আমড়া",
    "dragon_fruit": "ড্রাগন ফল",
    "pomelo": "জাম্বুরা",
    "akashmoni": "আকাশমণি",
}


def _match_crop_alias(lowered: str) -> str | None:
    """Crop match with Bengali word-boundary safety.

    Single-word aliases must match at the START of a whitespace-delimited
    token (leading punctuation stripped), so inflections (ধানের/আলুর) match
    while unrelated words containing an alias (সমাধান) do not. Crops in
    SHORT_EXACT_CROPS match single-word aliases by exact token equality
    only. Tokens in NEGATIVE_CROP_TOKENS never match. Multi-word aliases
    use substring matching. Table order is longest-first within a crop;
    more specific crops precede broader ones in table order.
    """
    import re as _re
    strip_pat = _re.compile(r"^[^\w\u0980-\u09FF]+")
    tokens = [strip_pat.sub("", t) for t in lowered.split()]
    tokens = [t for t in tokens if t and t not in NEGATIVE_CROP_TOKENS]
    for crop, aliases in _CROP_ALIASES.items():
        short_exact = crop in SHORT_EXACT_CROPS
        ordered = sorted((str(a).strip().lower() for a in aliases if str(a).strip()), key=len, reverse=True)
        for alias in ordered:
            if " " in alias:
                if alias in lowered:
                    return crop
            elif short_exact:
                if any(tok == alias for tok in tokens):
                    return crop
            elif any(tok == alias or tok.startswith(alias) for tok in tokens):
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
