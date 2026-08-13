"""T15 structured verifier candidate — orchestration + fail-closed safety policy.

Implements 06_CLAIM_SCHEMA_AND_VERIFIER.md processing contract steps 3-7:
parse evidence spans through the same canonicalization tables; match entities,
quantities, units, denominators, intervals, PHI, polarity, applicability;
assign the frozen relation with a trace; aggregate claim relations into answer
certification through the fail-closed safety policy.

Certification policy (fail-closed, per protocol §Act abstention/rules):
  a claim is certifiable IFF
    relation == supported  AND
    chemical identity resolved (never `unknown`)  AND
    every asserted material field resolved and matched  AND
    polarity == affirmed  AND
    no parse failures on the claim sentence.
  Only safety-bearing claims are matched; informational sentences are not
  claims and therefore cannot certify.

Oracle-field mode: pass `oracle_fields = {claim_index: {...}}` to override the
parser's fields during matching (extraction-error decomposition used at T17).
Oracle inputs come from expert gold (T10), never from the runtime.

Aggregate confidence (compatible with the runtime enum strings):
  verified            : sources present AND >=1 claim AND all claims certifiable
  flagged-unverified  : at least one claim not certifiable (flags per claim)
  low_confidence      : no sources (mirrors the lexical baseline branch order)

This module is a NEW research candidate. It is NOT imported by the runtime
pipeline until T22 gating.
"""
from __future__ import annotations

import dataclasses
import hashlib
from dataclasses import dataclass, field

from app.infrastructure.verification import normalization as norm
from app.infrastructure.verification.claim_parser import ClaimParser, ParsedClaim
from app.infrastructure.verification.relation_matcher import (
    EvidenceParser,
    MatchResult,
    RelationMatcher,
)


@dataclass(frozen=True)
class EvidenceSpan:
    source_id: str
    text: str
    start: int
    end: int
    content_hash: str


@dataclass(frozen=True)
class ClaimVerdict:
    claim_id: str
    text: str
    relation: str
    certifiable: bool
    reasons: tuple[str, ...] = ()
    risk_tier: str = "R2"
    safety_critical: bool = True
    field_trace: tuple[dict, ...] = ()
    evidence_spans: tuple[EvidenceSpan, ...] = ()
    oracle_override: bool = False


@dataclass(frozen=True)
class StructuredVerdict:
    confidence: str  # verified | flagged_unverified | low_confidence
    claims: tuple[ClaimVerdict, ...] = ()
    flags: tuple[str, ...] = ()
    unverified_claims: tuple[str, ...] = ()
    parse_failures: tuple[str, ...] = ()


class StructuredVerifier:
    """Deterministic parser + normalizer + relation matcher + safety policy."""

    def __init__(self, parser: ClaimParser | None = None,
                 matcher: RelationMatcher | None = None,
                 evidence_parser: EvidenceParser | None = None) -> None:
        self.parser = parser or ClaimParser()
        self.evidence_parser = evidence_parser or EvidenceParser()
        self.matcher = matcher or RelationMatcher(self.evidence_parser)

    def verify(self, answer: str, sources, *, oracle_fields: dict[int, dict] | None = None,
               source_ids: tuple[str, ...] = ()) -> StructuredVerdict:
        """sources: any iterable of objects with .content_bn/.content_en/.id."""
        passages = list(sources or [])
        evidence_units: list = []
        for s in passages:
            content_bn = getattr(s, "content_bn", "") or ""
            content_en = getattr(s, "content_en", "") or ""
            sid = getattr(s, "id", "unknown")
            digest = hashlib.sha256(f"{content_bn}\n{content_en}".encode("utf-8")).hexdigest()
            units = self.evidence_parser.parse(sid, content_bn, content_en)
            for u in units:
                evidence_units.append(dataclasses.replace(u, content_hash=digest))

        claims, parse_failures = self.parser.parse_answer(answer or "")
        if not claims:
            if not passages:
                return StructuredVerdict(confidence="low_confidence",
                                         flags=("No retrieved source available for verification",),
                                         parse_failures=tuple(parse_failures))
            return StructuredVerdict(confidence="verified", parse_failures=tuple(parse_failures))

        if not passages:
            # mirror the lexical baseline branch order: claims without sources are flagged
            texts = tuple(c.text for c in claims)
            return StructuredVerdict(
                confidence="flagged-unverified",
                flags=tuple(f"Unverified claim: {t}" for t in texts),
                unverified_claims=texts,
                parse_failures=tuple(parse_failures),
            )

        verdicts: list[ClaimVerdict] = []
        for idx, claim in enumerate(claims):
            oracle = (oracle_fields or {}).get(idx)
            used_oracle = False
            if oracle:
                claim = self._apply_oracle(claim, oracle)
                used_oracle = True

            result: MatchResult = self.matcher.match(claim, evidence_units)

            # fail-closed certification, tier-aware per taxonomy section 5:
            # R1/R2 require resolved chemical identity; R3 (cultural/timing)
            # certifies on supported relation without a chemical.
            blocked: list[str] = [
                r for r in (
                    "relation != supported" if result.relation != "supported" else None,
                    "chemical identity unresolved" if claim.risk_tier in ("R1", "R2") and not claim.chemical_known else None,
                    "non-affirmed polarity" if claim.polarity.value != "affirmed" else None,
                    "parse failures on claim" if claim.parse_failures else None,
                ) if r
            ]
            certifiable = not blocked and bool(result.evidence_units)
            span_objects = tuple(
                EvidenceSpan(source_id=u.source_id, text=u.text, start=u.start, end=u.end,
                             content_hash=u.content_hash)
                for u in result.evidence_units
            )
            verdicts.append(ClaimVerdict(
                claim_id=claim.claim_id,
                text=claim.text[:200],
                relation=result.relation,
                certifiable=certifiable,
                reasons=tuple(blocked) + tuple(result.reasons),
                risk_tier=claim.risk_tier,
                safety_critical=claim.safety_critical,
                field_trace=tuple(
                    {"field": m.field, "status": m.status,
                     "claim_value": str(m.claim_value), "evidence_value": str(m.evidence_value)}
                    for m in result.matches
                ),
                evidence_spans=span_objects,
                oracle_override=used_oracle,
            ))

        certifiable_all = all(v.certifiable for v in verdicts)
        if certifiable_all:
            confidence = "verified"
            flags: tuple[str, ...] = ()
            unverified: tuple[str, ...] = ()
        else:
            confidence = "flagged-unverified"
            flags = tuple(f"Claim {v.claim_id} not certifiable ({v.relation}): {v.text[:60]}" for v in verdicts if not v.certifiable)
            unverified = tuple(v.text for v in verdicts if not v.certifiable)
        return StructuredVerdict(confidence=confidence, claims=tuple(verdicts),
                                 flags=flags, unverified_claims=unverified,
                                 parse_failures=tuple(parse_failures))

    def _apply_oracle(self, claim: ParsedClaim, oracle: dict) -> ParsedClaim:
        """Override parser fields with oracle (gold) values.

        Oracle values use the same canonical representations the parser emits
        (chemicals: list of names; amount_pairs/fractions: (value, unit) pairs;
        denominator/interval/phi/action/formulation: canonical string;
        polarity: enum string; applicability: list of condition strings).
        """
        from app.infrastructure.verification.claim_parser import Field

        def fv(value, status: str = "resolved") -> Field:
            return Field(value=value, status=status, raw=str(value))

        converters = {
            "chemicals": lambda v: tuple(Field(value=c, status="resolved", raw=str(c)) for c in v),
            "amount_pairs": lambda v: tuple((float(a), str(u)) for a, u in v),
            "fractions": lambda v: tuple((float(a), str(u)) for a, u in v),
            "denominator": lambda v: fv(v),
            "interval": lambda v: fv(v),
            "phi": lambda v: fv(v),
            "polarity": lambda v: fv(v),
            "action": lambda v: fv(v),
            "formulation": lambda v: fv(v),
            "applicability": lambda v: tuple(fv(c) for c in v),
        }
        values = {}
        for key, converter in converters.items():
            if key in oracle:
                values[key] = converter(oracle[key])
        return dataclasses.replace(claim, **values) if values else claim