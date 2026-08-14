"""Application-layer auth service (P3, amendment 15).

P3 scope: the backend can consume Supabase access tokens. This is ADDITIVE
and OPTIONAL — the FastAPI dependency helpers live in `api/dependencies.py`;
nothing here touches the web layer. The anonymous demo path never presents
a token and therefore never triggers network I/O.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.auth.jwks import SupabaseJWKSVerifier


class AuthService:
    """Parses Bearer tokens and verifies them against the Supabase JWKS."""

    def __init__(self, verifier: SupabaseJWKSVerifier | None = None) -> None:
        self._verifier = verifier

    def claims_from_authorization(self, authorization: str | None) -> dict[str, Any] | None:
        """Extract and verify a Bearer token; None when absent/invalid."""
        if not authorization or self._verifier is None:
            return None
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            return None
        return self._verifier.verify(token.strip())