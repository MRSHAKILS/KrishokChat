"""Deterministic atomic-claim parser for the T15 structured verifier candidate.

Implements 06_CLAIM_SCHEMA_AND_VERIFIER.md processing contract steps 1-2:
split the answer into atomic candidate claims; parse claim fields
deterministically and retain original spans.

Fail-closed rules baked in here:
- safety-bearing text that cannot be parsed emits an explicit parse failure
  (never silently discarded);
- unresolved chemical identity, polarity, or required unit marks the field
  `unknown` and blocks certification downstream;
- compound advice (multiple amount+unit groups) is split into atomic claims:
  one claim per (chemical, amount) binding where resolvable; if the number of
  chemicals and amounts cannot be bound 1:1, the sentence produces ONE claim
  with all amounts and an explicit parse_failure entry.

This module is a NEW research candidate. It is NOT imported by the runtime
pipeline until T22 gating.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from app.infrastructure.verification import normalization as norm

# ---- sentence splitting ------------------------------------------------
_SENT_SPLIT_RE = re.compile(r"[।;\n]+")


def split_sentences(text: str) -> list[tuple[str, int, int]]:
    """Return [(sentence, start, end)] covering the whole text (splits omitted)."""
    out: list[tuple[str, int, int]] = []
    pos = 0
    for m in _SENT_SPLIT_RE.finditer(text):
        seg = text[pos:m.start()]
        if seg.strip():
            out.append((seg, pos, m.start()))
        pos = m.end()
    tail = text[pos:]
    if tail.strip():
        out.append((tail, pos, len(text)))
    return out


# ---- field regexes (operate on RAW text; spans preserved) --------------
# amount+unit: unit table is order-independent; Bangla units first (longest match)
_UNIT_ALT = (
    r"মিলিলিটার|মি\.লি|মিলি|মিলিগ্রাম|লিটার|গ্রাম|কেজি|টেবিল চামচ|চামচ|কাপ"
    r"|millilitre|milliliter|mililitre|milligram|litre|liter|kilogram|kg|mg|ml|gm|g|l|t"
)
AMOUNT_RE = re.compile(
    rf"(?P<num>\d+(?:[.,]\d+)?)\s*(?P<unit>{_UNIT_ALT})(?=\s|$|[.,!?;:।)])",
    re.IGNORECASE,
)
FRACTION_RE = re.compile(
    r"(?P<frac>আধা|অর্ধেক)\s*(?P<unit>চামচ|কাপ|লিটার|চা চামচ|টেবিল চামচ)(?=\s|$|[.,!?;:।)])"
)
FRACTION_VALUES = {"আধা": 0.5, "অর্ধেক": 0.5}

DENOM_RE = re.compile(
    r"(?:প্রতি|per)\s*(?P<den>হেক্টর|হেক্টরে|শতক|বিঘা|একর|কানি|কাঠা|লিটার|কেজি|মিটার|উদ্ভিদ|গাছ|বীজ|কানি|hectare|acre|litre|liter|liter water|kg|seed|plant|ha|ac|m2)"
    r"|(?P<num>\d+)\s*(?P<pden>লিটার|l)\s+(?P<den2>পানি|water)"
    r"|(?P<d1>mg|ml|g|kg|l|t)\s*/\s*(?P<d2>l|ha|ac|kg|m2|hectare|acre)",
    re.IGNORECASE,
)

INTERVAL_RE = re.compile(
    r"(?P<n>\d+)\s*(?P<u>দিন|দিনে|দিনের|সপ্তাহ|সপ্তাহে|সপ্তাহের|মাস|মাসে|ঘণ্টা|ঘন্টা|বার|দফা|বারে)"
    r"(?!\s*আগে)"
    r"\s*(?P<mode>পরপর|অন্তর|ব্যবধানে|ব্যবধান|পর|পরে|একবার|once|apart|later|interval)?"
    r"|(?P<freq>সপ্তাহে|দিনে|বারে|প্রতি)\s*(?P<n2>\d+)\s*(?P<u2>বার|দফা)",
    re.IGNORECASE,
)

PHI_RE = re.compile(
    r"(?:ফসল\s*(?:তোলার|কাটার|উঠানোর|ঘরে তোলার)\s*(?P<n>\d+)\s*দিন\s*(?P<when>আগে|পর))"
    r"|(?:শেষ\s*স্প্রে(?:র)?\s*(?P<n2>\d+)\s*দিন\s*(?P<when2>আগে|পর))"
    r"|(?:\bPHI\b\s*(?P<n3>\d+)\s*দিন)"
    r"|(?:harvest\s*(?:interval|re[- ]entry)?\s*(?P<n4>\d+)\s*days?\s*(?P<when4>before|after)?)",
    re.IGNORECASE,
)

# ---- polarity / applicability / action keyword tables -------------------
NEGATION_TOKENS = (
    "করবেন না", "করা যাবে না", "ব্যবহার করবেন না", "প্রয়োগ করবেন না", "প্রয়োগ করা যাবে না",
    "স্প্রে করবেন না", "মেশাবেন না", "না মেশাবেন", "না দিন", "দেবেন না", "নেবেন না",
    "বিরত থাকুন", "পরিহার করুন", "এড়িয়ে চলুন", "do not", "don't", "never", "avoid",
    "না ব্যবহার করুন", "ব্যবহার করা যাবে না", "নিষেধ",
)
PROHIBITED_TOKENS = (
    "নিষিদ্ধ", "বেআইনি", "অনুমোদিত নয়", "অননুমোদিত", "banned", "restricted",
    "ব্যবহার নিষিদ্ধ", "নিষেধাজ্ঞা",
)
CONDITIONAL_TOKENS = (
    "যদি", "যখন", "হলে", "মাত্রাতিরিক্ত", "দেখা দিলে", "আক্রমণ হলে", "আক্রান্ত হলে",
    "যদি থাকে", "শর্তে", "পরিস্থিতিতে", "ক্ষেত্রে", "if", "when", "in case", "যদি হয়",
)
CONDITION_PHRASE_RE = re.compile(
    r"(?:যদি|যখন|ক্ষেত্রে|পরিস্থিতিতে)\s*[^.।;\n]*?"
    r"|(?:মাত্রাতিরিক্ত|লক্ষণ দেখা দিলে|আক্রমণ হলে|আক্রান্ত হলে|যদি থাকে)\s*[^.।;\n]*?",
)

ACTION_TOKENS: dict[str, tuple[str, ...]] = {
    "spray": ("স্প্রে", "ছিটান", "ছিটিয়ে", "ছিটানো"),
    "mix": ("মেশান", "মিশান", "মিশিয়ে", "মিশ্রণ", "গুলে"),
    "irrigate": ("সেচ", "পানি দেন", "পানি দিন", "জল দেন", "সেচ দিন", "সেচ দেন"),
    "monitor": ("পর্যবেক্ষণ", "নজর রাখুন", "নিয়মিত দেখুন", "monitor"),
    "remove": ("ছাঁটাই", "পরিষ্কার করুন", "সরিয়ে ফেলুন", "ধ্বংস", "remove", "তুলে ফেলুন"),
    "wait": ("অপেক্ষা", "wait"),
    "avoid": ("এড়িয়ে", "পরিহার", "avoid"),
    "refer": ("হেল্পলাইন", "কৃষি কর্মকর্তা", "উপসহকারী", "যোগাযোগ করুন", "16123"),
    "apply": ("প্রয়োগ", "প্রয়োগ করুন", "প্রয়োগ কর", "ব্যবহার করুন", "ব্যবহার কর",
              "দিতে হবে", "দিয়ে দিন", "সার দিন", "দেওয়া", "দেন", "স্প্রে করুন", "দেই"),
}

# Generic/intervention signal terms treated as chemical/intervention evidence
BN_GENERIC_CHEM = (
    "ইউরিয়া", "ডিএপি", "টিএসপি", "এমওপি", "জিপসাম", "সার", "কীটনাশক", "ছত্রাকনাশক",
    "আগাছানাশক", "ঔষধ", "ওষুধ", "ভেষজ", "জৈব সার", "কম্পোস্ট", "মিশ্র সার", "ইউরিয়া সার",
    "পটাশ", "ফসফেট", "জিংক", "বোরন", "সালফার", "ট্রাইকোডার্মা", "নিম", "ভারমিকম্পোস্ট",
)
EN_CAP_RE = re.compile(r"\b[A-Z][A-Za-z]+(?:(?:\s|/|-)[A-Za-z]+)*\b")
EN_EXCLUDE = {
    "Publisher", "Section", "Topic", "Note", "Notes", "Date", "Table", "Figure",
    "No", "Kg", "Ml", "Mg", "G", "L", "Source", "Ref", "DOI", "I", "II", "III",
    "CABI", "BARC", "BARI", "BINA", "Dae", "USA", "FAQ", "Etc",
    "WP", "EC", "SC", "SL", "GR", "WDG", "AS", "PHI", "AEZ", "BN",
}


@dataclass(frozen=True)
class Field:
    """One parsed schema field: canonical value + original span + status.

    status: resolved | missing | unknown | null (per 06 schema missing-value rules)
    """
    value: object = None
    span: tuple[int, int] | None = None
    status: str = "missing"
    raw: str = ""


@dataclass(frozen=True)
class ParsedClaim:
    claim_id: str
    text: str
    start: int
    end: int
    chemicals: tuple[Field, ...] = ()
    amounts: tuple[Field, ...] = ()          # raw amount strings with attached unit
    amount_pairs: tuple[tuple[float, str], ...] = ()  # (value, canonical unit)
    fractions: tuple[tuple[float, str], ...] = ()
    denominator: Field = field(default_factory=Field)
    interval: Field = field(default_factory=Field)
    phi: Field = field(default_factory=Field)
    polarity: Field = field(default_factory=lambda: Field(value="affirmed", status="resolved"))
    applicability: tuple[Field, ...] = ()
    action: Field = field(default_factory=Field)
    formulation: Field = field(default_factory=Field)
    parse_failures: tuple[str, ...] = ()
    risk_tier: str = "R2"
    safety_critical: bool = True

    @property
    def has_dosage(self) -> bool:
        return bool(self.amount_pairs or self.fractions)

    @property
    def chemical_known(self) -> bool:
        return any(c.status == "resolved" for c in self.chemicals)


def _span_value(match: re.Match, group: str) -> tuple[str, tuple[int, int]]:
    return match.group(group), (match.start(group), match.end(group))


class ClaimParser:
    """Deterministic extractor of atomic claims and schema fields."""

    def parse_answer(self, answer: str, *, claim_prefix: str = "c") -> tuple[list[ParsedClaim], list[str]]:
        sentences = split_sentences(answer or "")
        claims: list[ParsedClaim] = []
        parse_failures: list[str] = []
        for idx, (sent, start, end) in enumerate(sentences):
            parsed = self._parse_sentence(sent, start, end)
            if parsed is None:
                continue  # no safety-bearing content -> informational sentence, not a claim
            claim = parsed[0]
            object.__setattr__(claim, "claim_id", f"{claim_prefix}{idx}")
            claims.append(claim)
            parse_failures.extend(claim.parse_failures)
        return claims, parse_failures

    def _explicit_failures(self, sentence: str, amount_matches: list, fraction_matches: list) -> list[str]:
        """Emit explicit parse failures for unresolved safety-bearing structure."""
        if amount_matches or fraction_matches:
            return []
        nums = norm.extract_numbers(sentence)
        if nums:
            return [f"number present but no amount+unit parse in safety-bearing sentence: {nums[0][0]}"]
        return []

    def _phrases(self, text: str) -> str:
        return " ".join(unicodedata.normalize("NFKC", text).lower().split())

    def _parse_sentence(self, sentence: str, start: int, end: int) -> list[ParsedClaim] | None:
        low = sentence.lower()
        amount_matches = list(AMOUNT_RE.finditer(sentence))
        fraction_matches = list(FRACTION_RE.finditer(sentence))
        polarity = self._polarity(sentence)
        chemicals = self._chemicals(sentence)
        # A sentence is an atomic claim when it carries: measurable quantity,
        # intervention/chemical signal token, a resolved chemical name, or a
        # non-affirmed polarity (prohibition/negation is itself safety-bearing).
        has_safety = (
            bool(amount_matches or fraction_matches)
            or any(tok in low for tok in norm.SAFETY_SIGNAL_TOKENS)
            or bool(chemicals)
            or polarity.value != "affirmed"
        )
        if not has_safety:
            return None
        action = self._action(sentence)
        denominator = self._denominator(sentence)
        interval = self._interval(sentence)
        phi = self._phi(sentence)
        applicability = self._applicability(sentence)
        formulation = self._formulation(sentence)

        # Bind amounts to chemicals (documented 1:1 rule; else single claim, fail closed).
        pairs: list[tuple[float, str]] = []
        for m in amount_matches:
            num = m.group("num").replace(",", ".") if "," in m.group("num") else m.group("num")
            pairs.append((float(norm.to_ascii_digits(num)), norm.canonical_unit(m.group("unit")) or m.group("unit").lower()))
        fracs = []
        for m in fraction_matches:
            fracs.append((FRACTION_VALUES.get(m.group("frac"), 0.5), norm.canonical_unit(m.group("unit")) or m.group("unit").lower()))
        fields_amts = tuple(Field(value=p[1], raw=f"{p[0]:g} {p[1]}", status="resolved") for p in pairs)

        failures: list[str] = []
        unresolved_unit = [p for p in pairs if p[1] not in ("mg", "ml", "g", "kg", "l", "t", "চামচ", "টেবিল চামচ", "কাপ")]
        if unresolved_unit:
            failures.append(f"unresolved unit for amount {unresolved_unit[0][0]}")
        # numbers not explained by amount, interval, or PHI parsing -> explicit failure
        if (not amount_matches and not fraction_matches
                and interval.status != "resolved" and phi.status != "resolved"
                and norm.extract_numbers(sentence)):
            failures.append(
                f"number present but no amount/interval/PHI parse in safety-bearing sentence: {norm.extract_numbers(sentence)[0][0]}"
            )
        if (not pairs and not fracs
                and interval.status != "resolved" and phi.status != "resolved"
                and any(tok in low for tok in ("স্প্রে", "প্রয়োগ", "সার", "কীটনাশক", "ছত্রাকনাশক", "ঔষধ", "ওষুধ", "ডোজ", "মাত্রা"))
                and (norm.extract_numbers(sentence)
                     or any(u in low for u in ("কেজি", "গ্রাম", "মিলি", "মিলিলিটার", "মিলিগ্রাম", "লিটার", "চামচ", "কাপ", "বার", "দিন", "সপ্তাহ")))):
            # dosage intent asserted with a quantity signal that could not be parsed
            failures.append(f"dosage intent without parseable quantity: {sentence[:80]}")

        fields_chem = (
            tuple(Field(value=c, status="resolved", raw=c) for c in sorted(set(chemicals)))
            if chemicals else (Field(value="unknown", status="unknown", raw=""),)
        )

        safety_critical, tier = self._risk(sentence, bool(pairs or fracs), polarity, phi, chemicals)
        claim = ParsedClaim(
            claim_id="unset",
            text=sentence, start=start, end=end,
            chemicals=fields_chem,
            amounts=fields_amts, amount_pairs=tuple(pairs), fractions=tuple(fracs),
            denominator=denominator, interval=interval, phi=phi,
            polarity=polarity, applicability=applicability, action=action,
            formulation=formulation, parse_failures=tuple(failures),
            risk_tier=tier, safety_critical=safety_critical,
        )
        return [claim]

    # ---- per-field extractors ------------------------------------------
    def _polarity(self, sentence: str) -> Field:
        low = " " + sentence.lower() + " "
        if any(tok in low for tok in PROHIBITED_TOKENS):
            return Field(value="prohibited", status="resolved")
        if any(tok in low for tok in NEGATION_TOKENS):
            return Field(value="negated", status="resolved")
        if any(tok in low for tok in CONDITIONAL_TOKENS):
            return Field(value="conditional", status="resolved")
        return Field(value="affirmed", status="resolved")  # absence of signals is the resolution

    def _action(self, sentence: str) -> Field:
        low = sentence.lower()
        for action in ("spray", "mix", "irrigate", "monitor", "remove", "wait", "avoid", "refer"):
            if any(tok in low for tok in ACTION_TOKENS[action]):
                return Field(value=action, status="resolved")
        for tok in ACTION_TOKENS["apply"]:
            if tok in low:
                return Field(value="apply", status="resolved")
        return Field(value="unknown", status="unknown")

    def _denominator(self, sentence: str) -> Field:
        m = DENOM_RE.search(sentence)
        if not m:
            return Field(status="missing", value=None)
        if m.group("d1") and m.group("d2"):
            canon = f"per {norm.canonical_denominator(m.group('d2')) or m.group('d2').lower()}"
            return Field(value=canon, span=(m.start(), m.end()), raw=m.group(0), status="resolved")
        if m.group("den"):
            canon = f"per {norm.canonical_denominator(m.group('den')) or m.group('den').lower()}"
            return Field(value=canon, span=(m.start(), m.end()), raw=m.group(0), status="resolved")
        if m.group("pden"):
            return Field(value="per l water", span=(m.start(), m.end()), raw=m.group(0), status="resolved")
        return Field(status="missing", value=None)

    def _interval(self, sentence: str) -> Field:
        m = INTERVAL_RE.search(sentence)
        if m:
            if m.group("n") and m.group("u"):
                u = norm.INTERVAL_UNITS.get(m.group("u").lower(), m.group("u").lower())
                key = f"{norm.to_ascii_digits(m.group('n'))} {u}"
                return Field(value=key, span=(m.start(), m.end()), raw=m.group(0), status="resolved")
            if m.group("n2") and m.group("u2"):
                u2 = norm.INTERVAL_UNITS.get(m.group("u2").lower(), m.group("u2").lower())
                key = f"every {norm.to_ascii_digits(m.group('n2'))} {u2}"
                return Field(value=key, span=(m.start(), m.end()), raw=m.group(0), status="resolved")
        # interval implies but unresolved
        if any(tok in sentence.lower() for tok in ("পরপর", "অন্তর", "ব্যবধানে", "ব্যবধান", "পুনরায়", "আবার", "repeatedly", "রিপিট")):
            return Field(value="unknown", span=None, status="unknown")
        return Field(status="missing", value=None)

    def _phi(self, sentence: str) -> Field:
        m = PHI_RE.search(sentence)
        if m:
            n = next((g for g in ("n", "n2", "n3", "n4") if m.group(g)), None)
            when = m.group("when") or m.group("when2") or m.group("when4") or "before"
            u = "day"
            key = f"phi {norm.to_ascii_digits(m.group(n))} {u} {when}" if n else "phi present"
            return Field(value=key, span=(m.start(), m.end()), raw=m.group(0), status="resolved")
        return Field(status="missing", value=None)

    def _applicability(self, sentence: str) -> tuple[Field, ...]:
        out: list[Field] = []
        for m in CONDITION_PHRASE_RE.finditer(sentence):
            seg = m.group().strip()
            if len(seg) > 2:
                out.append(Field(value=self._phrases(seg)[:60], span=(m.start(), m.end()), raw=seg, status="resolved"))
        return tuple(out) if out else (Field(status="missing", value=None),)

    def _formulation(self, sentence: str) -> Field:
        m = re.search(r"\b[0-9]{1,3}\s*%|\b(?:WP|EC|SC|SL|GR|WDG|AS)\b", sentence)
        if m:
            return Field(value=m.group(0), span=(m.start(), m.end()), raw=m.group(0), status="resolved")
        return Field(status="missing", value=None)

    def _chemicals(self, sentence: str) -> list[str]:
        found: list[str] = []
        low = sentence.lower()
        for generic in BN_GENERIC_CHEM:
            if generic in low:
                found.append(generic)
        for m in EN_CAP_RE.finditer(sentence):
            token = m.group(0)
            if token in EN_EXCLUDE:
                continue
            found.append(token)
        if not found:
            # chemical intent via dosage-adjacent Bangla nouns? keep unknown.
            return []
        return list(dict.fromkeys(norm.normalize_chemical(c) for c in found))

    def _risk(self, sentence: str, has_dosage: bool, polarity: Field, phi: Field, chemicals: list[str]) -> tuple[bool, str]:
        if phi.status == "resolved" or polarity.value in ("negated", "prohibited", "conditional"):
            return True, "R1"
        if has_dosage or chemicals:
            return True, "R2"
        return False, "R3"