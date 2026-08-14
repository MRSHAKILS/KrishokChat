"""Auth routes — proof endpoint for token verification (P3, additive).

`GET /auth/me` returns the verified user claims for a valid Bearer token,
401 otherwise. No existing demo route is gated by auth; this endpoint only
proves the backend can consume Supabase access tokens (amendment 15, P3).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.api.dependencies import RequiredUserDep

router = APIRouter(prefix="/auth", tags=["auth"])

_CLAIM_FIELDS = ("sub", "email", "aud", "role", "app_metadata", "user_metadata")


@router.get("/me")
def me(claims: RequiredUserDep) -> dict[str, Any]:
    user = {field: claims.get(field) for field in _CLAIM_FIELDS if field in claims}
    if "sub" in user:
        user["id"] = user.pop("sub")
    return {"user": user}