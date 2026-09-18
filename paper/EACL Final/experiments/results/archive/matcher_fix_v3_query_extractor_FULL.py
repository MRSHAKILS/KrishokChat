"""Stage 2B: Query Intent & Information-State Extraction (PRISM-RAG Module 2B.1).

Extracts structured agronomic slots from user queries deterministically
before invoking retrieval or generation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from app.domain.intent import (
    CROP_NAMES_BN,
    _CROP_ALIASES,
    _FERTILIZER_KW,
    _PLANT_PART_BN,
    _PLANT_PART_MAP,
    _PREVENTION_KW,
    _TREATMENT_KW,
    _match_crop_alias,
)


@dataclass(frozen=True)
class QueryInformationState:
    """Structured information state extracted from a single user turn."""

    intent: str
    crop: str | None = None
    crop_bn: str | None = None
    problem_type: str | None = None
    symptom: str | None = None
    plant_part: str | None = None
    location: str | None = None
    growth_stage: str | None = None
    temporal_event: str | None = None
    actionability: str = "high"  # "high" (seeking action/dose) | "informational"
    extracted_tokens: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent,
            "crop": self.crop,
            "crop_bn": self.crop_bn,
            "problem_type": self.problem_type,
            "symptom": self.symptom,
            "plant_part": self.plant_part,
            "location": self.location,
            "growth_stage": self.growth_stage,
            "temporal_event": self.temporal_event,
            "actionability": self.actionability,
            "extracted_tokens": list(self.extracted_tokens),
        }


# Known Bangladesh agricultural districts
_DISTRICTS_BN: dict[str, str] = {
    "নাটোর": "Natore", "নাটোরে": "Natore", "natore": "Natore",
    "বগুড়া": "Bogura", "বগুড়ায়": "Bogura", "বগুড়াত": "Bogura", "bogura": "Bogura",
    "রাজশাহী": "Rajshahi", "রাজশাহীতে": "Rajshahi", "rajshahi": "Rajshahi",
    "রংপুর": "Rangpur", "রংপুরে": "Rangpur", "rangpur": "Rangpur",
    "দিনাজপুর": "Dinajpur", "দিনাজপুরে": "Dinajpur", "dinajpur": "Dinajpur",
    "যশোর": "Jashore", "যশোরে": "Jashore", "jashore": "Jashore",
    "কুষ্টিয়া": "Kushtia", "কুষ্টিয়ায়": "Kushtia", "kushtia": "Kushtia",
    "ময়মনসিংহ": "Mymensingh", "ময়মনসিংহে": "Mymensingh", "mymensingh": "Mymensingh",
    "পাবনা": "Pabna", "পাবনায়": "Pabna", "pabna": "Pabna",
    "কুমিল্লা": "Cumilla", "কুমিল্লায়": "Cumilla", "cumilla": "Cumilla",
    "বরিশাল": "Barishal", "বরিশালে": "Barishal", "barishal": "Barishal",
    "সিলেট": "Sylhet", "সিলেটে": "Sylhet", "sylhet": "Sylhet",
    "চট্টগ্রাম": "Chattogram", "চট্টগ্রামে": "Chattogram", "chattogram": "Chattogram",
}

# Romanized & dialectal crop mappings
_ROMAN_CROP_ALIASES: dict[str, str] = {
    "dhan": "rice", "dhaner": "rice", "ধানর": "rice", "ধানত": "rice",
    "alu": "potato", "alor": "potato", "আলুত": "potato",
    "tomato": "tomato", "tomator": "tomato",
    "begun": "brinjal", "beguner": "brinjal", "বাইঙ্গন": "brinjal",
    "moris": "chilli", "moricer": "chilli", "morich": "chilli", "মরিস": "chilli",
    "gom": "wheat", "gomer": "wheat",
    "bhutta": "maize",
}

# Temporal / Weather events
_TEMPORAL_PATTERNS = [
    (r"(গত\s*সপ্তাহে\s*বৃষ্টি|বৃষ্টির\s*পর|বৃষ্টি\s*হইছিল|বৃষ্টি\s*হয়েছে|ভারী\s*বৃষ্টি|ঝড়\s*বৃষ্টি|বৃষ্টি)", "বৃষ্টির পর"),
    (r"(খরা|রোদের\s*পর|তীব্র\s*গরম|শুকনা\s*আবহাওয়া)", "খরার পর"),
    (r"(কুয়াশা|কুয়াশা|শীতের\s*সকালে|ঠান্ডা\s*পড়ছে)", "কুয়াশার পর"),
    (r"(আজকে|কালকে|সকালে|বিকালে)", "সাম্প্রতিক সময়"),
]

# Follow-up patterns
_FOLLOW_UP_PATTERNS = (
    "আগেরবার", "আগের", "আগে যে", "আবার কও", "আবার বল", "আবার বলুন",
    "তারপর কি", "এরপর কি", "তারপরে কি", "আরেকবার", "ওষুধের নাম আবার",
    "বিকল্প", "অন্য কোনো", "তুলে ফেলতে হবে", "কতদিন পর", "কত দিন পর",
)


class QueryExtractor:
    """Deterministic extractor for agricultural information state."""

    @classmethod
    def extract(cls, query: str) -> QueryInformationState:
        lowered = query.lower()
        extracted_tokens: list[str] = []

        # 1. Follow-up detection
        is_follow_up = any(p in lowered for p in _FOLLOW_UP_PATTERNS)

        # 2. Crop detection (token-start matching; see intent._match_crop_alias:
        # Bengali vowel signs defeat \b, so substring/regex matching fired inside
        # unrelated words, e.g. rice "ধান" inside "সমাধান" (solution). An alias
        # must open a whitespace-delimited token (leading punctuation stripped);
        # inflections (ধানের/আলুর) match. Fix 2026-09-17 (v2: punct-strip + লঙ্কা).
        import re as _re
        strip_pat = _re.compile(r"^[^\w\u0980-\u09FF]+")
        lowered_tokens = [t for t in (strip_pat.sub("", t) for t in lowered.split()) if t]
        detected_crop: str | None = None
        detected_alias: str | None = None
        for crop_id, aliases in _CROP_ALIASES.items():
            ordered = sorted((str(a).strip() for a in aliases if str(a).strip()), key=len, reverse=True)
            for alias in ordered:
                alias_lower = alias.lower()
                if " " in alias_lower:
                    hit = alias_lower in lowered
                else:
                    hit = any(tok == alias_lower or tok.startswith(alias_lower) for tok in lowered_tokens)
                if hit:
                    detected_crop = crop_id
                    detected_alias = alias
                    extracted_tokens.append(alias)
                    break
            if detected_crop:
                break

        if not detected_crop:
            for word, crop_id in _ROMAN_CROP_ALIASES.items():
                word_lower = str(word).strip().lower()
                if not word_lower:
                    continue
                if " " in word_lower:
                    hit = word_lower in lowered
                else:
                    hit = any(tok == word_lower or tok.startswith(word_lower) for tok in lowered_tokens)
                if hit:
                    detected_crop = crop_id
                    extracted_tokens.append(word)
                    break

        # 3. Location detection
        detected_location: str | None = None
        for dist_key, dist_en in _DISTRICTS_BN.items():
            if dist_key in lowered:
                detected_location = dist_en
                extracted_tokens.append(dist_key)
                break

        # 4. Temporal event detection
        detected_temporal: str | None = None
        for pat, label in _TEMPORAL_PATTERNS:
            if re.search(pat, query):
                detected_temporal = label
                extracted_tokens.append(label)
                break

        # 5. Plant part detection
        detected_plant_part: str | None = None
        for kw, part in _PLANT_PART_MAP.items():
            if kw in lowered:
                detected_plant_part = part
                extracted_tokens.append(kw)
                break

        # 6. Intent and Problem Type classification
        intent = "general_agriculture"
        problem_type = None

        treatment_extended = _TREATMENT_KW + (
            "করণীয়", "কী করণীয়", "কি করণীয়", "উপায়", "উপায়", "কী করব",
            "কী করবো", "কি করব", "কি করবো", "কি করুম", "কি দিমু", "দাবা কি",
            "ওষুধ কন", "কি স্প্রে", "দমন ব্যবস্থা", "দমন", "চিকিৎসা", "উপায় কি",
            "spray", "osudh", "cikitsha", "dava", "প্রতিকার", "লক্ষণ ও",
        )

        if is_follow_up:
            intent = "follow_up"
        elif any(kw in lowered for kw in _FERTILIZER_KW + ("সার", "ইউরিয়া", "ইউরিয়া", "পটাশ", "টিএসপি", "কত কেজি", "কতটুকু")):
            intent = "fertilizer"
            problem_type = "fertilizer"
        elif any(kw in lowered for kw in ("পোকা", "পোঁকা", "মাজরা", "লেদা", "জাব পোকা", "কীটপতঙ্গ", "pest", "worm", "chidro", "fota")):
            intent = "pest_management"
            problem_type = "pest"
        elif any(kw in lowered for kw in treatment_extended):
            intent = "disease_treatment"
            problem_type = "disease"
        elif any(kw in lowered for kw in _PREVENTION_KW):
            intent = "disease_prevention"
            problem_type = "prevention"
        elif any(kw in lowered for kw in ("কখন বুনব", "রোপণ", "রোপন", "বপন", "ফসল তোলার সময়", "ক্যালেন্ডার", "সময়")):
            intent = "crop_calendar"
            problem_type = "management"
        elif any(kw in lowered for kw in ("পানি দিব", "সেচ", "পানি দেওয়া", "ড্রেনেজ", "পানি নিষ্কাশন", "irrigation", "ড্রেন")):
            intent = "irrigation"
            problem_type = "irrigation"
        elif any(kw in lowered for kw in ("লক্ষণ", "দাগ", "রোগের নাম", "কি রোগ", "কী রোগ", "diagnosis")):
            intent = "disease_identification"
            problem_type = "disease"


        # 7. Symptom token extraction
        symptom_kws = (
            "বাদামি দাগ", "কালো দাগ", "হলুদ দাগ", "গোল দাগ", "ছিটা দাগ", "পুইড়া গেছে",
            "পোড়া দাগ", "মইরা যায়", "ঢলে পড়া", "কুঁকড়ায়", "পাতা হলুদ", "গাছ হলুদ",
            "ডগা পচা", "ফল পচা", "গোড়া পচন", "শিকড় পচা", "আঠা ঝরা",
        )
        detected_symptom: str | None = None
        for skw in symptom_kws:
            if skw in query:
                detected_symptom = skw
                extracted_tokens.append(skw)
                break

        # Actionability
        actionability = "high" if any(kw in lowered for kw in _TREATMENT_KW + _FERTILIZER_KW) else "informational"

        return QueryInformationState(
            intent=intent,
            crop=detected_crop,
            crop_bn=CROP_NAMES_BN.get(detected_crop) if detected_crop else None,
            problem_type=problem_type,
            symptom=detected_symptom,
            plant_part=detected_plant_part,
            location=detected_location,
            growth_stage=None,
            temporal_event=detected_temporal,
            actionability=actionability,
            extracted_tokens=tuple(dict.fromkeys(extracted_tokens)),
        )
