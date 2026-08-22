"""PostgREST adapter for announcements & read state (amendment 02).

Service-role access for admin writes; the public read path also goes through
the backend so audience filtering (caller's plan) can be applied server-side.
Uses httpx, already a project dependency. Additive lane: the anonymous demo
never depends on these methods — when Supabase is unreachable the
notification endpoints answer honestly (empty list / 503 on admin writes).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx

logger = logging.getLogger(__name__)

ANNOUNCEMENTS_TABLE = "announcements"
READS_TABLE = "announcement_reads"
DEFAULT_TIMEOUT_SECONDS = 10.0


class PostgrestNotificationStore:
    """Announcements + per-user read state over PostgREST."""

    def __init__(
        self,
        supabase_url: str,
        service_role_key: str,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._base = f"{supabase_url.rstrip('/')}/rest/v1"
        self._headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        }
        self._timeout = timeout_seconds

    def _client(self) -> httpx.Client:
        return httpx.Client(base_url=self._base, headers=self._headers, timeout=self._timeout)

    # -- public reads ---------------------------------------------------------

    def list_live(self, audiences: list[str], limit: int) -> list[dict[str, Any]]:
        """Published, unexpired rows visible to any of `audiences`, newest first."""
        now_iso = datetime.now(timezone.utc).isoformat()
        with self._client() as client:
            response = client.get(
                f"/{ANNOUNCEMENTS_TABLE}",
                params={
                    "audience": f"in.({','.join(audiences)})",
                    "published": "eq.true",
                    # unexpired = no expiry set OR expiry in the future
                    "or": f"(expires_at.is.null,expires_at.gt.{now_iso})",
                    "order": "published_at.desc",
                    "limit": str(limit),
                    "select": "*",
                },
            )
            response.raise_for_status()
            return response.json()

    def list_read_ids(self, user_id: str) -> set[str]:
        with self._client() as client:
            response = client.get(
                f"/{READS_TABLE}",
                params={"user_id": f"eq.{user_id}", "select": "announcement_id"},
            )
            response.raise_for_status()
            return {row["announcement_id"] for row in response.json()}

    def mark_read(self, user_id: str, announcement_id: str) -> None:
        with self._client() as client:
            response = client.post(
                f"/{READS_TABLE}",
                json={"user_id": user_id, "announcement_id": announcement_id},
                params={"on_conflict": "user_id,announcement_id"},
                headers={"Prefer": "resolution=merge-duplicates"},
            )
            response.raise_for_status()

    # -- admin writes -----------------------------------------------------------

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        with self._client() as client:
            response = client.post(
                f"/{ANNOUNCEMENTS_TABLE}",
                json=payload,
                headers={"Prefer": "return=representation"},
            )
            response.raise_for_status()
            return response.json()[0]

    def get(self, announcement_id: str) -> dict[str, Any] | None:
        with self._client() as client:
            response = client.get(
                f"/{ANNOUNCEMENTS_TABLE}",
                params={"id": f"eq.{announcement_id}", "select": "*"},
            )
            response.raise_for_status()
            rows = response.json()
            return rows[0] if rows else None

    def list_all(self, limit: int, offset: int = 0) -> list[dict[str, Any]]:
        """Admin listing incl. drafts, newest first."""
        with self._client() as client:
            response = client.get(
                f"/{ANNOUNCEMENTS_TABLE}",
                params={"order": "created_at.desc", "limit": str(limit), "offset": str(offset)},
            )
            response.raise_for_status()
            return response.json()

    def patch(self, announcement_id: str, changes: dict[str, Any]) -> dict[str, Any] | None:
        with self._client() as client:
            response = client.patch(
                f"/{ANNOUNCEMENTS_TABLE}",
                params={"id": f"eq.{announcement_id}"},
                json=changes,
                headers={"Prefer": "return=representation"},
            )
            response.raise_for_status()
            rows = response.json()
            return rows[0] if rows else None

    def delete(self, announcement_id: str) -> bool:
        with self._client() as client:
            response = client.delete(
                f"/{ANNOUNCEMENTS_TABLE}",
                params={"id": f"eq.{announcement_id}"},
                headers={"Prefer": "return=representation"},
            )
            response.raise_for_status()
            return bool(response.json())
