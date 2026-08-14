"""P1 hardening: deterministic dosage-claim extraction and entailment.

Product-lane module. It is deliberately independent of the gated research
candidates (``claim_parser.py`` / ``structured.py`` / ``relation_matcher.py``,
which stay frozen until T22). Runtime verification now:

1. splits the answer into sentences,
2. extracts atomic dosage claims as (chemical, amount, unit) tuples —
   ``no_dosage`` sentences are informational and never blocked,
3. checks entailment per source passage: every amount+unit AND every detected
   chemical must appear in the SAME retrieved source (normalized) — a bare
   "2 ml" in an unrelated passage no longer certifies a dosage claim,
4. returns verdicts so the pipeline can annotate-and-drop, never hard-block.

Fail-closed rules: an unresolved amount+unit is unsupported; a claim whose
chemical cannot be detected is still checked on amount+unit alone (the
chemical binding strengthens, never loosens, the check).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from app.domain.contracts import RetrievedSource

# ---- normalization ----------------------------------------------------------
_BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

# Canonical unit table: surface alias -> canonical token (longest-first matching).
_UNIT_ALIASES: dict[str, str] = {
    "মিলিলিটার": "ml", "মিলি": "ml", "মি.লি": "ml", "এমএল": "ml", "ml": "ml",
    "মিলিগ্রাম": "mg", "মি.গ্রা": "mg", "mg": "mg",
    "গ্রাম": "g", "gm": "g", "g": "g",
    "কেজি": "kg", "kg": "kg",
    "লিটার": "l", "liter": "l", "litre": "l", "l": "l",
    "টেবিল চামচ": "টেবিল চামচ", "চামচ": "চামচ", "কাপ": "কাপ",
}
_UNIT_ALT = "|".join(sorted(_UNIT_ALIASES, key=len, reverse=True))

_SENT_SPLIT_RE = re.compile(r"[।;\n]+")

_AMOUNT_RE = re.compile(
    rf"(?P<amount>\d+(?:[.,]\d+)?)\s*(?P<unit>{_UNIT_ALT})(?=\s|$|[.,!?;:।()/])",
    re.IGNORECASE,
)
_FRACTION_RE = re.compile(
    r"(?P<frac>আধা|অর্ধেক)\s*(?P<unit>টেবিল চামচ|চামচ|কাপ|লিটার|l)(?=\s|$|[.,!?;:।()/])",
    re.IGNORECASE,
)
_FRACTION_VALUES = {"আধা": 0.5, "অর্ধেক": 0.5}

# Common Bangladeshi agrochemicals and intervention signals (Bengali).
_CHEMICAL_BN = (
    "ইউরিয়া", "ডিএপি", "টিএসপি", "এমওপি", "জিপসাম", "পটাশ", "ফসফেট", "জিংক",
    "বোরন", "সালফার", "সার", "কীটনাশক", "ছত্রাকনাশক", "আগাছানাশক", "ঔষধ", "ওষুধ",
    "কার্বেন্ডাজিম", "ম্যানকোজেব", "থায়ামেথক্সাম", "ইমিডাক্লোপ্রিড", "ক্লোরপাইরিফস",
    "সাইপারমেথ্রিন", "ডেল্টামেথ্রিন", "প্রোপিকোনাজল", "টেবুকোনাজল", "অ্যাজোক্সিস্ট্রোবিন",
    "ট্রাইসাইক্লাজল", "কারটাপ", "ফিপ্রোনিল", "গ্লাইফোসেট", "প্যারাকোয়াট", "ডাইমেথোয়েট",
    "ম্যালাথিয়ন",
)
_EN_CHEM_RE = re.compile(r"\b[A-Z][A-Za-z]+(?:[-/][A-Za-z]+)*\b")
_EN_CHEM_EXCLUDE = {
    "Per", "Litre", "Liter", "Liters", "Litres", "Ml", "Mg", "G", "Kg", "L", "T",
    "WP", "EC", "SC", "SL", "GR", "WDG", "AS", "PHI", "Ppm", "Use", "Add", "Mix",
    "Water", "Spray", "Apply", "Dose", "Source", "Note", "Notes", "Date", "Table",
    "Figure", "No", "FAQ", "Etc", "CABI", "BARC", "BARI", "BINA", "DAE", "IRRI",
    "NARS", "SRDI", "AEZ", "BN",
}


def normalize(text: str) -> str:
    """Canonical comparison form: NFKC, ASCII digits, lower, unit aliases."""
    t = unicodedata.normalize("NFKC", text).translate(_BN_DIGITS).lower().replace(",", ".")
    for alias in sorted(_UNIT_ALIASES, key=len, reverse=True):
        canon = _UNIT_ALIASES[alias]
        if alias.isascii():
            t = re.sub(rf"(?<![a-z0-9]){re.escape(alias.lower())}(?![a-z0-9])", canon, t)
        else:
            t = t.replace(alias.lower(), canon)
    return " ".join(t.split())


def normalize_chemical(name: str) -> str:
    return re.sub(r"[^\w\u0980-\u09FF]+", " ", unicodedata.normalize("NFKC", name)).strip().lower()


@dataclass(frozen=True)
class DosageClaim:
    """One atomic claim: sentence span + bound (chemical, amount, unit) fields."""

    sentence: str
    start: int
    end: int
    end_sep: int = 0  # end of the sentence INCLUDING its trailing separator/space
    chemicals: tuple[str, ...] = ()
    amounts: tuple[tuple[float, str], ...] = ()  # (value, canonical unit)
    fractions: tuple[tuple[float, str], ...] = ()
    parse_failures: tuple[str, ...] = ()

    @property
    def has_dosage(self) -> bool:
        return bool(self.amounts or self.fractions)

    @property
    def amount_tokens(self) -> tuple[str, ...]:
        tokens = tuple(f"{value:g} {unit}" for value, unit in self.amounts)
        tokens += tuple(f"{value:g} {unit}" for value, unit in self.fractions)
        return tokens


def _detect_chemicals(sentence: str) -> tuple[str, ...]:
    low = sentence.lower()
    found: list[str] = []
    for generic in _CHEMICAL_BN:
        if generic in low:
            found.append(generic)
    for m in _EN_CHEM_RE.finditer(sentence):
        token = m.group(0)
        if token not in _EN_CHEM_EXCLUDE:
            found.append(token)
    return tuple(dict.fromkeys(normalize_chemical(c) for c in found))


def extract_claims(answer: str) -> list[DosageClaim]:
    """Split the answer into atomic claims (sentence-level, spans preserved)."""
    claims: list[DosageClaim] = []
    pos = 0
    for m in _SENT_SPLIT_RE.finditer(answer or ""):
        seg, start, end = answer[pos : m.start()], pos, m.start()
        end_sep = m.end()
        while end_sep < len(answer) and answer[end_sep] in " \t\r\n":
            end_sep += 1
        pos = m.end()
        if seg.strip():
            claims.append(_parse_sentence(seg, start, end, end_sep))
    tail = answer[pos:]
    if tail.strip():
        claims.append(_parse_sentence(tail, pos, len(answer), len(answer)))
    return [claim for claim in claims if claim is not None]


def _parse_sentence(sentence: str, start: int, end: int, end_sep: int) -> DosageClaim | None:
    # Sentence may carry leading whitespace after a separator; exclude it from
    # the span but keep removal boundaries correct.
    lead = len(sentence) - len(sentence.lstrip())
    failures: list[str] = []
    amounts: list[tuple[float, str]] = []
    for m in _AMOUNT_RE.finditer(sentence):
        raw = m.group("amount").replace(",", ".")
        try:
            value = float(normalize(raw))
        except ValueError:
            failures.append(f"unparseable amount: {raw}")
            continue
        unit = _UNIT_ALIASES.get(m.group("unit").lower(), m.group("unit").lower())
        amounts.append((value, unit))
    fractions: list[tuple[float, str]] = []
    for m in _FRACTION_RE.finditer(sentence):
        unit = _UNIT_ALIASES.get(m.group("unit").lower(), m.group("unit").lower())
        fractions.append((_FRACTION_VALUES.get(m.group("frac"), 0.5), unit))
    chemicals = _detect_chemicals(sentence)
    return DosageClaim(
        sentence=sentence.strip(), start=start + lead, end=end,
        end_sep=end_sep,
        chemicals=chemicals,
        amounts=tuple(amounts), fractions=tuple(fractions),
        parse_failures=tuple(failures),
    )


def per_source_normalized(sources: list[RetrievedSource]) -> list[str]:
    """One normalized string per source (BN + EN content joined)."""
    return [normalize(f"{source.content_bn} {source.content_en}") for source in sources]


_AMOUNT_IN_SRC_RE = re.compile(
    r"(?<!\d)(?P<amt>\d+(?:\.\d+)?)(?!\d)\s*(?P<unit>ml|mg|g|kg|l|চামচ|টেবিল চামচ|কাপ)(?=\s|$|[.,;:!?/।()])"
)
_FRACTION_IN_SRC_RE = re.compile(
    r"(?P<frac>আধা|অর্ধেক)\s*(?P<unit>টেবিল চামচ|চামচ|কাপ|লিটার|l)(?=\s|$|[.,;:!?/।()])"
)


def _amount_grounded(source_text: str, value: float, unit: str) -> bool:
    token = f"{value:g}"
    return any(
        m.group("amt") == token and m.group("unit") == unit
        for m in _AMOUNT_IN_SRC_RE.finditer(source_text)
    )


def _fraction_grounded(source_text: str, value: float, unit: str) -> bool:
    # Grounded when the fraction word ("আধা চামচ") appears OR when the same
    # quantity is written numerically in the source ("0.5 চামচ").
    if any(m.group("unit") == unit for m in _FRACTION_IN_SRC_RE.finditer(source_text)):
        return True
    return _amount_grounded(source_text, value, unit)


def claim_grounded(claim: DosageClaim, source_texts: list[str]) -> bool:
    """Entailment: every amount+unit AND every chemical in the SAME passage."""
    if not claim.has_dosage:
        return True  # informational
    for source_text in source_texts:
        amounts_ok = all(_amount_grounded(source_text, value, unit) for value, unit in claim.amounts)
        fractions_ok = all(_fraction_grounded(source_text, value, unit) for value, unit in claim.fractions)
        chemicals_ok = all(chemical in source_text for chemical in claim.chemicals)
        if amounts_ok and fractions_ok and chemicals_ok:
            return True
    return False


def sanitize_answer(answer: str, claims: list[DosageClaim], unsupported: set[int]) -> str | None:
    """Annotate-and-drop: remove sentences with unsupported claims.

    Removal consumes each dropped sentence plus its trailing separator so the
    remaining text keeps its original punctuation. Returns None when nothing
    was dropped; the pipeline maps an empty result to the referral text.
    """
    if not unsupported:
        return None
    parts: list[str] = []
    cursor = 0
    for claim in claims:
        if claim.start in unsupported:
            cursor = max(cursor, claim.end_sep)
            continue
        # Keep the sentence WITH its trailing separator so punctuation survives.
        parts.append(answer[cursor : claim.end_sep])
        cursor = claim.end_sep
    parts.append(answer[cursor:])
    result = "".join(parts).strip()
    # "" (everything dropped) is a meaningful sanitization result; None means
    # nothing was dropped. The pipeline maps "" to the referral text.
    return result
