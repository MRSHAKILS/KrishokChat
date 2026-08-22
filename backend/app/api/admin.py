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

from app.api.dependencies import AdminServiceDep, RequiredAdminDep
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
