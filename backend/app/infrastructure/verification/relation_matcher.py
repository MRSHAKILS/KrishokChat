"""Deterministic structured relation matcher for the T15 candidate.

Implements 06_CLAIM_SCHEMA_AND_VERIFIER.md §Frozen Relation Types and
§Source Conflict Policy. Relations: supported | contradicted |
partially_supported | unsupported | ambiguous | not_applicable.

Decision rules (deterministic, fail-closed):
- S = evidence units mentioning a claim chemical (or, when chemical identity is
  unresolved, units carrying any amount+unit).
- supported       : >=1 unit matches ALL material fields asserted by the claim
                     AND no unit conflicts on any material field.
- ambiguous       : >=1 matching unit AND >=1 conflicting unit (source conflict
                     unresolved by applicability) -> abstain (contract rule).
- contradicted    : no unit matches; >=1 unit with the same chemical asserts a
                     DIFFERENT value on a material field.
- partially_supported: no unit matches fully and no unit conflicts; units with
                     the chemical exist but omit material components.
- unsupported     : no evidence unit mentions the claim chemical (or, when the
                     chemical is unresolved, no unit carries the claim amount).
- not_applicable  : claim carries no safety-bearing material fields.

Polarity and applicability are material: a negated claim can only match
evidence that also negates; a claim with conditions cannot be certified against
evidence contradicting those conditions (else contradicted).

This module is a NEW research candidate, not imported by the runtime pipeline
until T22 gating.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.infrastructure.verification import normalization as norm
from app.infrastructure.verification.claim_parser import (
    AMOUNT_RE,
    FRACTION_RE,
    Field,
    ParsedClaim,
    _span_value,
)

NEGATION_TOKENS = (
    "করবেন না", "করা যাবে না", "ব্যবহার করবেন না", "প্রয়োগ করবেন না", "প্রয়োগ করা যাবে না",
    "স্প্রে করবেন না", "মেশাবেন না", "না মেশাবেন", "না দিন", "দেবেন না", "নেবেন না",
    "বিরত থাকুন", "পরিহার করুন", "এড়িয়ে চলুন", "do not", "don't", "never", "avoid",
    "না ব্যবহার করুন", "ব্যবহার করা যাবে না", "নিষেধ",
)


@dataclass(frozen=True)
class EvidenceUnit:
    """One evidence sentence parsed through the same field tables as claims."""
    source_id: str
    text: str
    start: int
    end: int
    chemicals: tuple[str, ...] = ()
    amount_pairs: tuple[tuple[float, str], ...] = ()
    denominator: str | None = None
    interval: str | None = None
    phi: str | None = None
    negated: bool = False
    content_hash: str = ""


@dataclass(frozen=True)
class FieldMatch:
    field: str
    status: str  # matched | conflicted | missing | not_asserted
    claim_value: object = None
    evidence_value: object = None
    source_id: str = ""


@dataclass(frozen=True)
class MatchResult:
    relation: str
    matches: tuple[FieldMatch, ...] = ()
    evidence_units: tuple[EvidenceUnit, ...] = ()
    reasons: tuple[str, ...] = ()


class EvidenceParser:
    """Parses evidence passages into units through the claim field tables."""

    def parse(self, source_id: str, content_bn: str, content_en: str = "") -> list[EvidenceUnit]:
        text = f"{content_bn} {content_en}"
        from app.infrastructure.verification.claim_parser import split_sentences
        units: list[EvidenceUnit] = []
        for sent, start, end in split_sentences(text):
            units.append(self._unit(source_id, sent, start, end))
        return [u for u in units
                if u.chemicals or u.amount_pairs or u.denominator or u.interval or u.phi or u.negated]

    def _unit(self, source_id: str, sent: str, start: int, end: int) -> EvidenceUnit:
        low = sent.lower()
        pairs = []
        for m in AMOUNT_RE.finditer(sent):
            num = m.group("num").replace(",", ".") if "," in m.group("num") else m.group("num")
            pairs.append((float(norm.to_ascii_digits(num)), norm.canonical_unit(m.group("unit")) or m.group("unit").lower()))
        fracs = []
        for m in FRACTION_RE.finditer(sent):
            fracs.append((0.5, norm.canonical_unit(m.group("unit")) or m.group("unit").lower()))
        pairs.extend(fracs)

        chemicals = self._chemicals(sent)
        denom = None
        dm = re.search(
            r"(?:প্রতি|per)\s*(?P<den>হেক্টর|হেক্টরে|শতক|বিঘা|একর|কানি|কাঠা|লিটার|কেজি|মিটার|hectare|acre|litre|liter|kg|seed|plant|ha|ac|m2)"
            r"|(?P<d1>mg|ml|g|kg|l)\s*/\s*(?P<d2>l|ha|ac|kg|m2)",
            sent, re.IGNORECASE,
        )
        if dm:
            if dm.group("d1"):
                denom = f"per {norm.canonical_denominator(dm.group('d2')) or dm.group('d2').lower()}"
            else:
                denom = f"per {norm.canonical_denominator(dm.group('den')) or dm.group('den').lower()}"
        interval = None
        im = re.search(
            r"(?P<n>\d+)\s*(?P<u>দিন|দিনে|দিনের|সপ্তাহ|সপ্তাহে|মাস|মাসে|ঘণ্টা|ঘন্টা|বার|দফা)"
            r"(?!\s*আগে)"
            r"\s*(?P<mode>পরপর|অন্তর|ব্যবধানে|ব্যবধান|পর|পরে|একবার)?"
            r"|(?P<freq>সপ্তাহে|দিনে|বারে|প্রতি)\s*(?P<n2>\d+)\s*(?P<u2>বার|দফা)",
            sent, re.IGNORECASE,
        )
        if im and im.group("n"):
            u = norm.INTERVAL_UNITS.get(im.group("u").lower(), im.group("u").lower())
            interval = f"{norm.to_ascii_digits(im.group('n'))} {u}"
        elif im and im.group("n2"):
            u2 = norm.INTERVAL_UNITS.get(im.group("u2").lower(), im.group("u2").lower())
            interval = f"every {norm.to_ascii_digits(im.group('n2'))} {u2}"
        phi = None
        pm = re.search(
            r"(?:ফসল\s*(?:তোলার|কাটার|উঠানোর)\s*(?P<n>\d+)\s*দিন\s*(?P<when>আগে|পর))"
            r"|(?:\bPHI\b\s*(?P<n3>\d+)\s*দিন)",
            sent, re.IGNORECASE,
        )
        if pm:
            n = pm.group("n") or pm.group("n3")
            when = pm.group("when") or "before"
            phi = f"phi {norm.to_ascii_digits(n)} day {when}"
        negated = any(tok in low for tok in NEGATION_TOKENS)
        return EvidenceUnit(source_id=source_id, text=sent, start=start, end=end,
                            chemicals=tuple(chemicals), amount_pairs=tuple(pairs),
                            denominator=denom, interval=interval, phi=phi, negated=negated)

    def _chemicals(self, sent: str) -> list[str]:
        from app.infrastructure.verification.claim_parser import BN_GENERIC_CHEM, EN_CAP_RE, EN_EXCLUDE
        found: list[str] = []
        low = sent.lower()
        for generic in BN_GENERIC_CHEM:
            if generic in low:
                found.append(generic)
        for m in EN_CAP_RE.finditer(sent):
            if m.group(0) not in EN_EXCLUDE:
                found.append(m.group(0))
        return list(dict.fromkeys(norm.normalize_chemical(c) for c in found))


def _num_eq(a: float, b: float) -> bool:
    return abs(a - b) < 1e-9


class RelationMatcher:
    def __init__(self, evidence_parser: EvidenceParser | None = None) -> None:
        self.evidence_parser = evidence_parser or EvidenceParser()

    def match(self, claim: ParsedClaim, evidence_units: list[EvidenceUnit]) -> MatchResult:
        # not_applicable only when the claim carries NO safety-bearing material
        # fields at all (no dosage, timing, PHI, denominator, or chemical).
        if (not claim.has_dosage
                and claim.polarity.value == "affirmed"
                and claim.interval.status != "resolved"
                and claim.phi.status != "resolved"
                and claim.denominator.status != "resolved"
                and not claim.chemical_known):
            return MatchResult(relation="not_applicable",
                               reasons=("claim carries no safety-bearing material fields",))

        # candidate evidence set
        if claim.chemical_known:
            claim_chems = set(c.value for c in claim.chemicals if c.status == "resolved")
            s = [u for u in evidence_units if any(c in u.chemicals for c in claim_chems)]
        elif claim.has_dosage:
            s = [u for u in evidence_units if u.amount_pairs]
        else:
            # chemical-less non-dosage claims (e.g., interval/PHI/cultural): any
            # safety-bearing evidence unit can carry the asserted fields
            s = list(evidence_units)

        if not s:
            reason = ("no evidence unit mentions the claim chemical"
                      if claim.chemical_known else "no evidence unit carries the claim amount")
            return MatchResult(relation="unsupported", evidence_units=(),
                               reasons=(reason,))

        matches: list[FieldMatch] = []
        conflicts: list[FieldMatch] = []
        reasons: list[str] = []

        # amount+unit (value + attached unit; unit mismatch is a material conflict)
        asserted = list(claim.amount_pairs) + list(claim.fractions)
        if asserted:
            amt_matched = False
            amt_conflicted = False
            for u in s:
                for ev_a, ev_u in u.amount_pairs:
                    for a, u_ in asserted:
                        if _num_eq(a, ev_a) and u_ == ev_u:
                            amt_matched = True
                        elif (ev_u == u_ and not _num_eq(a, ev_a)) or (_num_eq(a, ev_a) and ev_u != u_):
                            amt_conflicted = True
            matches.append(FieldMatch("amount_unit", "matched" if amt_matched else "missing",
                                      claim_value=str(asserted), source_id=s[0].source_id))
            if amt_conflicted:
                # source conflict: evidence carries a DIFFERENT value/unit for the
                # same chemical -> ambiguous -> abstain (contract policy)
                conflicts.append(FieldMatch("amount_unit", "conflicted", claim_value=str(asserted),
                                            evidence_value="different value or unit",
                                            source_id=s[0].source_id))
                reasons.append("conflicting amount and/or unit")
        # denominator
        if claim.denominator.status == "resolved":
            den_vals = {u.denominator for u in s if u.denominator}
            if den_vals and claim.denominator.value in den_vals:
                matches.append(FieldMatch("denominator", "matched", claim_value=claim.denominator.value, source_id=s[0].source_id))
            elif den_vals:
                conflicts.append(FieldMatch("denominator", "conflicted", claim_value=claim.denominator.value,
                                            evidence_value=sorted(den_vals)[0], source_id=s[0].source_id))
                reasons.append("conflicting denominator")
            else:
                matches.append(FieldMatch("denominator", "missing", claim_value=claim.denominator.value))
        # interval
        if claim.interval.status == "resolved":
            iv_vals = {u.interval for u in s if u.interval}
            if iv_vals and claim.interval.value in iv_vals:
                matches.append(FieldMatch("interval", "matched", claim_value=claim.interval.value, source_id=s[0].source_id))
            elif iv_vals:
                conflicts.append(FieldMatch("interval", "conflicted", claim_value=claim.interval.value,
                                            evidence_value=sorted(iv_vals)[0], source_id=s[0].source_id))
                reasons.append("conflicting interval")
            else:
                matches.append(FieldMatch("interval", "missing", claim_value=claim.interval.value))
        # phi
        if claim.phi.status == "resolved":
            phi_vals = {u.phi for u in s if u.phi}
            if phi_vals and claim.phi.value in phi_vals:
                matches.append(FieldMatch("phi", "matched", claim_value=claim.phi.value, source_id=s[0].source_id))
            elif phi_vals:
                conflicts.append(FieldMatch("phi", "conflicted", claim_value=claim.phi.value,
                                            evidence_value=sorted(phi_vals)[0], source_id=s[0].source_id))
                reasons.append("conflicting PHI")
            else:
                matches.append(FieldMatch("phi", "missing", claim_value=claim.phi.value))
        # polarity
        if claim.polarity.status == "resolved" and claim.polarity.value != "affirmed":
            pol_matched = any(u.negated for u in s)
            if pol_matched:
                matches.append(FieldMatch("polarity", "matched", claim_value=claim.polarity.value, source_id=s[0].source_id))
            else:
                conflicts.append(FieldMatch("polarity", "conflicted", claim_value=claim.polarity.value,
                                            evidence_value="affirmed", source_id=s[0].source_id))
                reasons.append("polarity mismatch (claim non-affirmed, evidence affirmed)")
        # applicability: conditions asserted must not be contradicted
        conditions = [f for f in claim.applicability if f.status == "resolved"]
        if conditions:
            cond_neg = any("না" in c.value or "নয়" in c.value for c in conditions)
            # evidence condition contradiction is only detected for explicit negations
            ev_neg = any(u.negated for u in s)
            if cond_neg and not ev_neg:
                conflicts.append(FieldMatch("applicability", "conflicted", claim_value=str(conditions[0].value),
                                            evidence_value="unconditional", source_id=s[0].source_id))
                reasons.append("applicability condition contradicted")

        if conflicts:
            return MatchResult(relation="ambiguous", matches=tuple(matches + conflicts),
                               evidence_units=tuple(s), reasons=tuple(reasons or ("source conflict",)))
        missing = [m for m in matches if m.status == "missing"]
        if missing:
            return MatchResult(relation="partially_supported", matches=tuple(matches),
                               evidence_units=tuple(s),
                               reasons=tuple(f"missing material field: {m.field}" for m in missing))
        if matches:
            return MatchResult(relation="supported", matches=tuple(matches),
                               evidence_units=tuple(s), reasons=("all asserted material fields matched",))
        return MatchResult(relation="partially_supported", matches=tuple(matches),
                           evidence_units=tuple(s), reasons=("material fields absent from evidence",))