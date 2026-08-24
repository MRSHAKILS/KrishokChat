"""Admin routes (amendment 02) — user management for the ops console.

Every route goes through `require_admin`: a verified token whose profile row
(role='admin') is looked up server-side with the service-role key on every
request. UI guards are cosmetic only; these endpoints are the enforcement.
All mutating operations are audited to `admin_actions`.
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.api.dependencies import AdminServiceDep, RequiredAdminDep, SettingsDep
from app.application.admin import AdminUnavailableError

router = APIRouter(prefix="/api/admin", tags=["admin"])


class UserPatchIn(BaseModel):
    role: Literal["user", "admin"] | None = None
    plan: Literal["free", "premium"] | None = None


def _unavailable(exc: Exception) -> HTTPException:
    return HTTPException(status_code=503, detail=str(exc))


@router.get("/users", response_model=dict)
def list_users(
    _: RequiredAdminDep,
    service: AdminServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    q: str = Query(default="", max_length=120),
) -> dict[str, Any]:
    """One page of user profiles, optionally filtered by email substring."""
    try:
        return service.list_users(page, page_size, search=q.strip())
    except AdminUnavailableError as exc:
        raise _unavailable(exc) from exc


@router.patch("/users/{user_id}", response_model=dict)
def patch_user(
    user_id: str,
    payload: UserPatchIn,
    claims: RequiredAdminDep,
    service: AdminServiceDep,
) -> dict[str, Any]:
    """Change a user's role and/or plan (audited)."""
    try:
        return service.update_user(
            acting_admin_id=claims["sub"],
            target_user_id=user_id,
            role=payload.role,
            plan=payload.plan,
        )
    except AdminUnavailableError as exc:
        raise _unavailable(exc) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/actions", response_model=dict)
def list_actions(
    _: RequiredAdminDep,
    service: AdminServiceDep,
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    """Recent admin actions (audit trail), newest first."""
    try:
        return {"items": service.list_actions(limit)}
    except AdminUnavailableError as exc:
        raise _unavailable(exc) from exc


@router.get("/advisory/late-blight-risk", response_model=dict)
def late_blight_risk(
    _: RequiredAdminDep,
    settings: SettingsDep,
) -> dict[str, Any]:
    """PR1: per-district potato late-blight risk from the offline snapshot.

    Read-only: the snapshot is an operator-maintained JSON on disk (never
    fetched live). The response carries a composer prefill per district; the
    admin reviews, edits, and publishes through the normal announcements lane
    (human-in-the-loop, audited). No snapshot -> ``available: false``, not 500.
    """
    from app.domain.late_blight import RISK_LABELS_BN, draft_advisory, evaluate_district
    from app.infrastructure.weather.snapshot import load_weather_snapshot

    snapshot = load_weather_snapshot(settings.weather_snapshot_resolved_path)
    if snapshot is None:
        return {
            "available": False,
            "reason": "আবহাওয়া স্ন্যাপশট পাওয়া যায়নি — WEATHER_SNAPSHOT_PATH যাচাই করুন।",
            "districts": [],
        }

    districts = []
    for name in sorted(snapshot.districts):
        result = evaluate_district(name, snapshot.districts[name])
        if result is None:
            continue
        districts.append(
            {
                "district": result.district,
                "risk": result.risk,
                "risk_label_bn": RISK_LABELS_BN.get(result.risk, result.risk),
                "favourable_days": result.favourable_days,
                "latest_date": result.latest_date,
                "in_season": result.in_season,
                "last_days": [
                    {"date": d.date, "tmin_c": d.tmin_c, "rh_pct": d.rh_pct, "rain_mm": d.rain_mm}
                    for d in result.detail[-3:]
                ],
                "draft": draft_advisory(result, sample=snapshot.is_sample),
            }
        )
    order = {"high": 0, "watch": 1, "low": 2}
    districts.sort(key=lambda d: (order[d["risk"]], d["district"]))
    return {
        "available": True,
        "sample": snapshot.is_sample,
        "source_note": snapshot.source_note,
        "latest_date": snapshot.latest_date,
        "rule": "Smith-period approximation: tmin>=10C and RH>=85% on >=2 consecutive days (>=1 = watch)",
        "districts": districts,
    }
