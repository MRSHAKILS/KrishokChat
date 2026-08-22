"""Notification routes (amendment 02) — farmer-facing reads + admin composition.

Public endpoints (anonymous welcome — disease alerts must reach farmers who
never sign up):
  GET  /api/notifications            — live announcements (audience-scoped)
  POST /api/notifications/{id}/read  — mark read (signed-in; anon uses localStorage)

Admin endpoints (require_admin on every request; mutations audited to
admin_actions):
  GET/POST /api/admin/announcements, PATCH/DELETE /api/admin/announcements/{id},
  POST /api/admin/announcements/{id}/publish|/unpublish
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.api.dependencies import (
    AdminServiceDep,
    NotificationServiceDep,
    OptionalUserDep,
    RequiredAdminDep,
    RequiredUserDep,
)
from app.application.notifications import NotificationsUnavailableError

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
admin_router = APIRouter(prefix="/api/admin/announcements", tags=["admin"])


def _caller_plan(claims: dict[str, Any] | None, admin_service: AdminServiceDep) -> str:
    """Resolve the caller's plan for audience scoping (fail-open to anonymous).

    A signed-in user whose profile can't be resolved still gets `all` content —
    tier labels never block access to public alerts (no gating, amendment 02 §9).
    """
    if not claims:
        return "anonymous"
    from app.application.admin import AdminUnavailableError

    try:
        profile = admin_service.get_profile(claims["sub"], email=str(claims.get("email") or ""))
    except AdminUnavailableError:
        return "anonymous"
    if profile is None:
        return "anonymous"
    return str(profile.get("plan") or "free")


@router.get("", response_model=dict)
def list_notifications(
    claims: OptionalUserDep,
    service: NotificationServiceDep,
    admin_service: AdminServiceDep,
    limit: int = Query(default=20, ge=1, le=50),
) -> dict[str, Any]:
    """Live announcements for this visitor (bell + banners)."""
    plan = _caller_plan(claims, admin_service)
    try:
        return service.list_for(plan, claims.get("sub") if claims else None, limit)
    except NotificationsUnavailableError:
        # Honest empty state — farmer surfaces render nothing, never block.
        return {"items": [], "enabled": False}


@router.post("/{announcement_id}/read", status_code=204)
def mark_read(
    announcement_id: str,
    claims: RequiredUserDep,
    service: NotificationServiceDep,
) -> None:
    """Persist read state for a signed-in user (anonymous uses localStorage)."""
    try:
        service.mark_read(claims["sub"], announcement_id)
    except NotificationsUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


class AnnouncementIn(BaseModel):
    kind: Literal["announcement", "disease_alert", "maintenance"] = "announcement"
    severity: Literal["info", "warning", "urgent"] = "info"
    title_bn: str
    body_bn: str
    crop: str = ""
    audience: Literal["all", "free", "premium"] = "all"
    cta_url: str = ""
    expires_at: datetime | None = None


class AnnouncementPatchIn(BaseModel):
    kind: Literal["announcement", "disease_alert", "maintenance"] | None = None
    severity: Literal["info", "warning", "urgent"] | None = None
    title_bn: str | None = None
    body_bn: str | None = None
    crop: str | None = None
    audience: Literal["all", "free", "premium"] | None = None
    cta_url: str | None = None
    expires_at: datetime | None = None


def _unavailable(exc: Exception) -> HTTPException:
    return HTTPException(status_code=503, detail=str(exc))


@admin_router.get("", response_model=dict)
def admin_list(
    _: RequiredAdminDep,
    service: NotificationServiceDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, Any]:
    """All announcements incl. drafts, newest first."""
    try:
        return {"items": service.list_all(limit)}
    except NotificationsUnavailableError as exc:
        raise _unavailable(exc) from exc


@admin_router.post("", status_code=201)
def admin_create(
    payload: AnnouncementIn,
    claims: RequiredAdminDep,
    service: NotificationServiceDep,
    admin_service: AdminServiceDep,
) -> dict[str, Any]:
    """Create an announcement (draft until /publish). Audited."""
    try:
        row = service.create({**payload.model_dump(mode="json"), "created_by": claims["sub"]})
        admin_service.audit(
            actor_id=claims["sub"],
            action="create_announcement",
            target_type="announcement",
            target_id=str(row.get("id")),
            payload={"kind": payload.kind, "severity": payload.severity, "audience": payload.audience},
        )
        return row
    except NotificationsUnavailableError as exc:
        raise _unavailable(exc) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@admin_router.patch("/{announcement_id}")
def admin_update(
    announcement_id: str,
    payload: AnnouncementPatchIn,
    claims: RequiredAdminDep,
    service: NotificationServiceDep,
) -> dict[str, Any]:
    try:
        row = service.update(announcement_id, payload.model_dump(mode="json", exclude_none=True))
    except NotificationsUnavailableError as exc:
        raise _unavailable(exc) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if row is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return row


@admin_router.post("/{announcement_id}/publish", response_model=dict)
def admin_publish(
    announcement_id: str,
    claims: RequiredAdminDep,
    service: NotificationServiceDep,
) -> dict[str, Any]:
    try:
        row = service.publish(announcement_id, publish=True)
    except NotificationsUnavailableError as exc:
        raise _unavailable(exc) from exc
    if row is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return row


@admin_router.post("/{announcement_id}/unpublish", response_model=dict)
def admin_unpublish(
    announcement_id: str,
    claims: RequiredAdminDep,
    service: NotificationServiceDep,
) -> dict[str, Any]:
    try:
        row = service.publish(announcement_id, publish=False)
    except NotificationsUnavailableError as exc:
        raise _unavailable(exc) from exc
    if row is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return row


@admin_router.delete("/{announcement_id}", status_code=204)
def admin_delete(
    announcement_id: str,
    claims: RequiredAdminDep,
    service: NotificationServiceDep,
) -> None:
    try:
        deleted = service.delete(announcement_id)
    except NotificationsUnavailableError as exc:
        raise _unavailable(exc) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Announcement not found")
