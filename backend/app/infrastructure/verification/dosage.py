"""Conservative, language-aware post-generation verification."""

from __future__ import annotations

import re

from app.domain.contracts import RetrievedSource, VerificationResult
from app.domain.enums import VerificationConfidence


_BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
_CLAIM_RE = re.compile(
    r"(?P<amount>\d+(?:[.]\d+)?)\s*(?P<unit>mg|ml|gm|g|kg|l|চামচ|কাপ)(?=\s|$|[.,!?;:।)])"
    r"|(?P<fraction>আধা|অর্ধেক)\s*(?P<funit>চামচ|কাপ|লিটার|l)(?=\s|$|[.,!?;:।)])",
    re.IGNORECASE,
)
_UNIT_ALIASES = {
    "মিলিলিটার": "ml", "মিলি": "ml", "মি.লি": "ml", "ml": "ml",
    "মিলিগ্রাম": "mg", "mg": "mg", "গ্রাম": "g", "gm": "g", "g": "g",
    "কেজি": "kg", "kg": "kg", "লিটার": "l", "liter": "l", "litre": "l", "l": "l",
    "চামচ": "চামচ", "কাপ": "কাপ",
}


def _normalize(text: str) -> str:
    normalized = " ".join(text.translate(_BN_DIGITS).lower().replace(",", ".").split())
    # Canonicalize Bengali and English unit spellings before comparing evidence.
    for alias, canonical in sorted(_UNIT_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias.isascii():
            normalized = re.sub(rf"\b{re.escape(alias.lower())}\b", canonical, normalized)
        else:
            normalized = normalized.replace(alias.lower(), canonical)
    return " ".join(normalized.split())


def _claims(text: str) -> list[str]:
    claims: list[str] = []
    for match in _CLAIM_RE.finditer(_normalize(text)):
        if match.group("fraction"):
            claims.append(f"{match.group('fraction')} {_UNIT_ALIASES.get(match.group('funit').lower(), match.group('funit').lower())}")
        else:
            amount = match.group("amount")
            unit = _UNIT_ALIASES.get(match.group("unit").lower(), match.group("unit").lower())
            claims.append(f"{amount} {unit}")
    return claims


class DosageVerifier:
    def verify(self, answer: str, sources: list[RetrievedSource]) -> VerificationResult:
        normalized_sources = _normalize(" ".join(f"{source.content_bn} {source.content_en}" for source in sources))
        unverified = tuple(claim for claim in _claims(answer) if claim not in normalized_sources)
        flags = tuple(f"Unverified dosage claim: {claim}" for claim in unverified)
        if unverified:
            return VerificationResult(
                confidence=VerificationConfidence.FLAGGED_UNVERIFIED,
                flags=flags,
                unverified_claims=unverified,
            )
        if not sources:
            return VerificationResult(
                confidence=VerificationConfidence.LOW_CONFIDENCE,
                flags=("No retrieved source available for verification",),
            )
        return VerificationResult(confidence=VerificationConfidence.VERIFIED)
