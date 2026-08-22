"""Auth routes — token verification proof endpoint (P3) + account surface.

`GET /auth/me` returns the verified user claims for a valid Bearer token,
401 otherwise. `GET /api/account` additionally resolves the caller's profile
(role/plan) via the service-role store when configured (amendment 02); when
Supabase is unconfigured it answers with plan=free/role=user labels marked
`profile_available: false` — never an error, never a gate.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.dependencies import AdminServiceDep, RequiredUserDep
from app.application.admin import AdminUnavailableError

router = APIRouter(prefix="/auth", tags=["auth"])

_CLAIM_FIELDS = ("sub", "email", "aud", "role", "app_metadata", "user_metadata")

account_router = APIRouter(prefix="/api/account", tags=["auth"])


@router.get("/me")
def me(claims: RequiredUserDep, admin_service: AdminServiceDep) -> dict[str, Any]:
    user = {field: claims.get(field) for field in _CLAIM_FIELDS if field in claims}
    if "sub" in user:
        user["id"] = user.pop("sub")
    # Amendment 02: include the authoritative profile role/plan when the
    # profile store is configured. Unconfigured → omitted (claims only).
    profile: dict[str, Any] | None = None
    try:
        profile = admin_service.get_profile(user["id"], email=str(user.get("email") or ""))
    except AdminUnavailableError:
        profile = None
    return {"user": user, "profile": profile}


@account_router.get("")
def account(claims: RequiredUserDep, admin_service: AdminServiceDep) -> dict[str, Any]:
    """The caller's plan/role surface for the account page and UI badges."""
    user_id = claims.get("sub")
    email = str(claims.get("email") or "")
    try:
        profile = admin_service.get_profile(user_id, email=email) if user_id else None
    except AdminUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if profile is None:
        # Unconfigured storage or missing row: honest default labels.
        return {
            "user": {"id": user_id, "email": email},
            "plan": "free",
            "role": "user",
            "profile_available": False,
        }
    return {
        "user": {"id": profile.get("id"), "email": profile.get("email") or email},
        "plan": profile.get("plan", "free"),
        "role": profile.get("role", "user"),
        "profile_available": True,
    }