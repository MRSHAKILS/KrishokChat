"""Auth routes — token verification proof endpoint (P3) + account surface.

`GET /auth/me` returns the verified user claims for a valid Bearer token,
401 otherwise. `GET /api/account` additionally resolves the caller's profile
(role/plan) via the service-role store when configured (amendment 02); when
Supabase is unconfigured it answers with plan=free/role=user labels marked
`profile_available: false` — never an error, never a gate.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.api.dependencies import (
    AdminServiceDep,
    CropCalendarsDep,
    FarmProfileServiceDep,
    RequiredUserDep,
)
from app.application.admin import AdminUnavailableError
from app.application.farm_profile import FarmProfileUnavailableError

logger = logging.getLogger("krishokchat.auth")

router = APIRouter(prefix="/auth", tags=["auth"])

_CLAIM_FIELDS = ("sub", "email", "aud", "role", "app_metadata", "user_metadata")

account_router = APIRouter(prefix="/api/account", tags=["auth"])


@router.get("/me")
def me(claims: RequiredUserDep, admin_service: AdminServiceDep) -> dict[str, Any]:
    user = {field: claims.get(field) for field in _CLAIM_FIELDS if field in claims}
    if "sub" in user:
        user["id"] = user.pop("sub")
    # Amendment 02: include the authoritative profile role/plan when the
    # profile store is configured. Unconfigured OR unreachable → omitted
    # (claims only). This endpoint verifies identity; a profile-store outage
    # must never turn it into a 500.
    profile: dict[str, Any] | None = None
    try:
        profile = admin_service.get_profile(user["id"], email=str(user.get("email") or ""))
    except AdminUnavailableError:
        profile = None
    except httpx.HTTPError as exc:
        logger.warning("profile store unreachable on /auth/me: %s", exc)
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


# --- P1+P2: farm profile + stage-aware advice (additive, non-gating) --------


class FarmProfileIn(BaseModel):
    primary_crop: str = Field(..., min_length=1, max_length=40)
    sowing_date: str | None = Field(None, max_length=10)
    upazila: str | None = Field(None, max_length=80)
    note: str | None = Field(None, max_length=500)


def _stage_view(calendars: object | None, profile: dict[str, Any] | None) -> dict[str, Any] | None:
    """Compute the current crop stage for a profile, or None when unavailable.

    Fail-open: no calendars artifact, no profile, or an unresolvable crop/date
    all yield None (the UI simply omits the stage card) — never an error.
    """
    if calendars is None or not profile:
        return None
    crop = profile.get("primary_crop")
    sowing = profile.get("sowing_date")
    if not crop or not sowing:
        return None
    try:
        stage = calendars.compute_stage(crop, sowing)  # type: ignore[attr-defined]
    except Exception:
        return None
    if stage is None:
        return None
    return {
        "crop_key": stage.crop_key,
        "crop_name_bn": stage.crop_name_bn,
        "stage_key": stage.stage_key,
        "stage_name_bn": stage.stage_name_bn,
        "das": stage.das,
        "start_das": stage.start_das,
        "end_das": stage.end_das,
        "advisory_bn": stage.advisory_bn,
        "grounding": stage.grounding,
        "is_approximate": stage.is_approximate,
        "source": stage.source,
        "season_note_bn": stage.season_note_bn,
        "farmer_context_bn": stage.farmer_context_bn,
    }


@account_router.get("/farm-profile")
def get_farm_profile(
    claims: RequiredUserDep,
    farm_service: FarmProfileServiceDep,
    calendars: CropCalendarsDep,
) -> dict[str, Any]:
    """The caller's farm profile + computed stage. Honest empty when unset or
    unconfigured (available:false) — never an error, never a gate."""
    user_id = claims.get("sub")
    if not farm_service.configured:
        return {"available": False, "profile": None, "stage": None}
    try:
        profile = farm_service.get(user_id) if user_id else None
    except FarmProfileUnavailableError:
        return {"available": False, "profile": None, "stage": None}
    return {
        "available": True,
        "profile": profile,
        "stage": _stage_view(calendars, profile),
    }


@account_router.put("/farm-profile")
def put_farm_profile(
    payload: FarmProfileIn,
    claims: RequiredUserDep,
    farm_service: FarmProfileServiceDep,
    calendars: CropCalendarsDep,
) -> dict[str, Any]:
    """Create/update the caller's farm profile. 503 when storage is
    unconfigured/unreachable (matching the account lane's philosophy)."""
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user id in token")
    try:
        saved = farm_service.save(user_id, payload.model_dump())
    except FarmProfileUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "available": True,
        "profile": saved,
        "stage": _stage_view(calendars, saved),
    }