from __future__ import annotations

from typing import Protocol

from app.domain.contracts import RetrievedSource, VerificationResult


class Verifier(Protocol):
    def verify(self, answer: str, sources: list[RetrievedSource]) -> VerificationResult: ...
