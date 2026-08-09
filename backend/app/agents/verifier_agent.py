"""Compatibility shim for the language-aware verifier."""

from app.domain.contracts import RetrievedSource
from app.infrastructure.verification.dosage import DosageVerifier


def verify(answer: str, sources: list[dict]) -> dict:
    typed_sources = [
        RetrievedSource(
            id=str(source.get("id", "")),
            score=float(source.get("score", 0)),
            content_bn=str(source.get("content_bn", "")),
            content_en=str(source.get("content_en", "")),
        )
        for source in sources
    ]
    result = DosageVerifier().verify(answer, typed_sources)
    return {
        "confidence": result.confidence.value,
        "flags": list(result.flags),
        "flagged_unverified": list(result.unverified_claims),
    }
