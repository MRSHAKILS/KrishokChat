"""Deterministic normalization for the T15 structured verifier candidate.

Design per 06_CLAIM_SCHEMA_AND_VERIFIER.md §Normalization and Units:
- Normalize Unicode/grapheme variants without changing token order or polarity.
- Convert Bengali digits to ASCII for comparison (original span preserved by caller).
- Resolve reviewed Bengali/English/Banglish unit aliases to canonical tokens.
- Never compare dimensionally incompatible quantities (units stay dimensional).
- Do NOT infer denominators; only what the text asserts.
- Preserve negation/prohibition tokens (polarity handled by the parser).

This module is a NEW research candidate. It is not imported by the runtime
pipeline; runtime verification continues to use `dosage.py` until T22.
"""
from __future__ import annotations

import re
import unicodedata

# Canonical unit table: alias -> canonical token
UNIT_ALIASES: dict[str, str] = {
    # mass
    "মিলিগ্রাম": "mg", "মি.গ্রা": "mg", "mg": "mg",
    "গ্রাম": "g", "গ্রাম": "g", "gm": "g", "g": "g",
    "কেজি": "kg", "kg": "kg",
    "মেট্রিক টন": "t", "টন": "t", "t": "t",
    # volume
    "মিলিলিটার": "ml", "মিলি": "ml", "মি.লি": "ml", "এমএল": "ml", "ml": "ml",
    "লিটার": "l", "লিটার": "l", "liter": "l", "litre": "l", "l": "l",
    # household (kept as-is; canonical form is the Bengali token)
    "চামচ": "চামচ", "টেবিল চামচ": "টেবিল চামচ", "কাপ": "কাপ",
}

# Denominator (base) canonical table: per-X / X per ...
DENOMINATOR_ALIASES: dict[str, str] = {
    "হেক্টর": "ha", "হেক্টরে": "ha", "hectare": "ha", "hectares": "ha",
    "একর": "ac", "acre": "ac", "acres": "ac",
    "শতক": "শতক", "বিঘা": "বিঘা", "কানি": "কানি", "কাঠা": "কাঠা",
    "লিটার": "l", "লিটার পানি": "l water", "পানি": "l water", "water": "l water",
    "কেজি": "kg", "কেজি বীজ": "kg seed", "বীজ": "seed", "seed": "seed",
    "মিটার": "m", "মিটার দূরত্ব": "m", "দূরত্ব": "m",
    "উদ্ভিদ": "plant", "গাছ": "plant", "plant": "plant",
    "কানি": "কানি",
}

# Interval/frequency canonical words
INTERVAL_UNITS: dict[str, str] = {
    "দিন": "day", "দিনে": "day", "দিনের": "day",
    "সপ্তাহ": "week", "সপ্তাহে": "week", "সপ্তাহের": "week",
    "মাস": "month", "মাসে": "month",
    "ঘণ্টা": "hour", "ঘন্টা": "hour", "ঘণ্টায়": "hour",
    "বার": "time", "দফা": "time", "বারে": "time",
}

# PHI / safety-condition signal words
PHI_UNITS: dict[str, str] = {"দিন": "day", "সপ্তাহ": "week", "মাস": "month"}

_BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
_NUM_RE = re.compile(r"(?P<num>\d+(?:[.,]\d+)?)")

# Safety-bearing signal tokens used to decide whether a sentence is a claim.
# Amount+unit sentences are claims regardless via the amount regex; these tokens
# gate amount-LESS sentences (intervention/chemical words only — generic nouns
# like "পানি"/water alone do not make a sentence a claim).
SAFETY_SIGNAL_TOKENS = (
    "স্প্রে", "ছিটান", "প্রয়োগ", "মেশান", "মিশান", "সার", "ঔষধ", "ওষুধ", "কীটনাশক",
    "ছত্রাকনাশক", "আগাছানাশক", "ডিএপি", "টিএসপি", "এমওপি", "ইউরিয়া", "জিপসাম",
    "সেচ", "ডোজ", "মাত্রা", "নিষেধ", "পরিহার",
)


def to_ascii_digits(text: str) -> str:
    """Convert Bengali digits to ASCII (original span preserved by the caller)."""
    return text.translate(_BN_DIGITS)


def nfkc(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def canonical_unit(word: str) -> str | None:
    """Return the canonical unit token for a surface unit word, else None."""
    key = nfkc(word.strip().lower())
    return UNIT_ALIASES.get(key)


def canonical_denominator(word: str) -> str | None:
    key = nfkc(word.strip().lower())
    return DENOMINATOR_ALIASES.get(key)


def normalize(text: str) -> str:
    """Canonical comparison form: NFKC, ASCII digits, lower, unit aliases.

    Unit-alias replacement is longest-first and word-boundary aware for ASCII
    aliases; Bengali aliases are replaced as substrings of canonical tokens only
    when the alias itself is a token (space-delimited). This preserves token
    order and never drops negation words.
    """
    t = to_ascii_digits(nfkc(text))
    t = " ".join(t.split())
    for alias in sorted(UNIT_ALIASES, key=len, reverse=True):
        canon = UNIT_ALIASES[alias]
        if alias.isascii():
            t = re.sub(rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])", canon, t, flags=re.IGNORECASE)
        else:
            t = re.sub(rf"(?<![\u0980-\u09FF]){re.escape(alias)}(?![\u0980-\u09FF])", canon, t)
    return " ".join(t.split())


def extract_numbers(text: str) -> list[tuple[float, int, int]]:
    """Return [(value, start, end)] for every decimal/Bengali number in text.

    Comma handling: "2,5" (single digit after comma, digits before) parses as
    the decimal 2.5; "1,000" (three digits after comma) parses as 1000.
    """
    out = []
    for m in _NUM_RE.finditer(to_ascii_digits(text)):
        raw = m.group("num")
        if "," in raw:
            before, after = raw.split(",", 1)
            if before.isdigit() and len(after) == 1 and after.isdigit():
                val = float(f"{before}.{after}")
            else:
                val = float(raw.replace(",", ""))
        else:
            val = float(raw)
        out.append((val, m.start(), m.end()))
    return out


def normalize_chemical(name: str) -> str:
    """Canonical chemical token for matching (lower, NFKC, punctuation-stripped)."""
    return re.sub(r"[^\w\u0980-\u09FF]+", " ", nfkc(name)).strip().lower()
