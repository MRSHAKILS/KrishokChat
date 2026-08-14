"""Auth port: verifies Supabase access tokens (JWT, ES256 via JWKS)."""

from __future__ import annotations

from typing import Any, Protocol


class TokenVerifier(Protocol):
    """Verifies a Supabase access-token JWT and returns its claims.

    Implementations must be lazy (no network until a token arrives) and fail
    closed: any fetch/decode/expiry problem yields None, never an exception.
    """

    def verify(self, token: str) -> dict[str, Any] | None: ...