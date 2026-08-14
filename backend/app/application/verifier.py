"""P1 hardened verifier: per-claim dosage entailment + annotate-and-drop.

Wired in place of the lexical ``DosageVerifier`` (which remains untouched as
the research-track baseline). Port-compatible: ``verify(answer, sources)``.

Verdicts per claim:
- ``grounded``   — amount+unit (and chemical, when detected) appear in one
                   retrieved passage;
- ``unsupported``— a measurable dosage claim not entailed by any passage;
- ``no_dosage``  — informational sentence without measurable quantity.

Annotate-and-drop: sentences carrying unsupported claims are removed from the
answer and surfaced through flags + per-claim verdicts. Nothing is hard-blocked.
"""

from __future__ import annotations

from app.domain.contracts import RetrievedSource, VerifierClaim, VerificationResult
from app.domain.enums import VerificationConfidence
from app.infrastructure.verification.dosage_claims import (
    claim_grounded,
    extract_claims,
    per_source_normalized,
    sanitize_answer,
)


class HardenedDosageVerifier:
    def verify(self, answer: str, sources: list[RetrievedSource]) -> VerificationResult:
        claims = extract_claims(answer or "")
        source_texts = per_source_normalized(sources)

        verdicts: list[VerifierClaim] = []
        unverified: list[str] = []
        checked = grounded = unsupported_count = 0
        unsupported_starts: set[int] = set()

        for claim in claims:
            if not claim.has_dosage:
                verdicts.append(VerifierClaim(text=claim.sentence, verdict="no_dosage"))
                continue
            checked += 1
            if claim_grounded(claim, source_texts):
                grounded += 1
                verdicts.append(VerifierClaim(text=claim.sentence, verdict="grounded"))
            else:
                unsupported_count += 1
                unsupported_starts.add(claim.start)
                detail = ", ".join(claim.amount_tokens) or "dosage claim"
                if claim.chemicals:
                    detail += f" (রাসায়নিক: {', '.join(claim.chemicals)})"
                unverified.append(detail)
                verdicts.append(
                    VerifierClaim(
                        text=claim.sentence,
                        verdict="unsupported",
                        reason=f"no passage contains {detail}",
                    )
                )

        flags = tuple(f"Unverified dosage claim: {detail}" for detail in unverified)
        sanitized = sanitize_answer(answer or "", claims, unsupported_starts) if unsupported_starts else None

        if unsupported_count:
            confidence = VerificationConfidence.FLAGGED_UNVERIFIED
        elif not sources:
            confidence = VerificationConfidence.LOW_CONFIDENCE
        else:
            confidence = VerificationConfidence.VERIFIED

        return VerificationResult(
            confidence=confidence,
            flags=flags,
            unverified_claims=tuple(unverified),
            claims=tuple(verdicts),
            sanitized_answer=sanitized,
            checked_count=checked,
            grounded_count=grounded,
            unsupported_count=unsupported_count,
        )