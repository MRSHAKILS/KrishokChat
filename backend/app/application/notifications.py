"""Application-layer notification service (amendment 02).

Public reads are audience-scoped: anonymous visitors see `all`; signed-in
free users see `all|free`; premium users see all three. Admin writes require
the admin role (enforced by `require_admin` at the route) and are audited to
`admin_actions` through the admin store.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.storage.postgrest_notifications import PostgrestNotificationStore

VALID_KINDS = frozenset({"announcement", "disease_alert", "maintenance"})
VALID_SEVERITIES = frozenset({"info", "warning", "urgent"})
VALID_AUDIENCES = frozenset({"all", "free", "premium"})

AUDIENCES_BY_PLAN: dict[str, list[str]] = {
    "anonymous": ["all"],
    "free": ["all", "free"],
    "premium": ["all", "free", "premium"],
}


class NotificationsUnavailableError(RuntimeError):
    """Raised when notification storage is not configured (no Supabase env)."""


class NotificationService:
    """Audience-scoped announcement reads + admin composition."""

    def __init__(
        self,
        store: PostgrestNotificationStore | None = None,
    ) -> None:
        self._store = store

    def _require_store(self) -> PostgrestNotificationStore:
        if self._store is None:
            raise NotificationsUnavailableError("Notifications are not configured on this server")
        return self._store

    # -- public reads ----------------------------------------------------------

    def list_for(
        self,
        plan: str | None,
        user_id: str | None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Live announcements for the caller's plan + their read ids."""
        store = self._require_store()
        audiences = AUDIENCES_BY_PLAN.get(plan or "anonymous", ["all"])
        items = store.list_live(audiences, limit)
        read_ids: set[str] = set()
        if user_id:
            read_ids = store.list_read_ids(user_id)
        for item in items:
            item["read"] = item["id"] in read_ids
        return {"items": items, "enabled": True}

    def mark_read(self, user_id: str, announcement_id: str) -> None:
        self._require_store().mark_read(user_id, announcement_id)

    # -- admin composition -------------------------------------------------------

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        kind = payload.get("kind", "announcement")
        severity = payload.get("severity", "info")
        audience = payload.get("audience", "all")
        if kind not in VALID_KINDS:
            raise ValueError(f"Invalid kind: {kind}")
        if severity not in VALID_SEVERITIES:
            raise ValueError(f"Invalid severity: {severity}")
        if audience not in VALID_AUDIENCES:
            raise ValueError(f"Invalid audience: {audience}")
        if not str(payload.get("title_bn") or "").strip():
            raise ValueError("title_bn is required")
        if not str(payload.get("body_bn") or "").strip():
            raise ValueError("body_bn is required")
        row = {k: v for k, v in payload.items() if v is not None}
        return self._require_store().create(row)

    def publish(
        self,
        announcement_id: str,
        publish: bool,
    ) -> dict[str, Any] | None:
        from datetime import datetime, timezone

        changes: dict[str, Any] = {"published": publish}
        if publish:
            changes["published_at"] = datetime.now(timezone.utc).isoformat()
        return self._require_store().patch(announcement_id, changes)

    def update(self, announcement_id: str, changes: dict[str, Any]) -> dict[str, Any] | None:
        allowed = {"kind", "severity", "title_bn", "body_bn", "crop", "audience", "cta_url", "expires_at"}
        clean = {k: v for k, v in changes.items() if k in allowed}
        if not clean:
            raise ValueError("Nothing to update")
        return self._require_store().patch(announcement_id, clean)

    def delete(self, announcement_id: str) -> bool:
        return self._require_store().delete(announcement_id)

    def list_all(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        return self._require_store().list_all(limit, offset)
