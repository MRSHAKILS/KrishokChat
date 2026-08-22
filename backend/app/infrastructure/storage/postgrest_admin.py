"""PostgREST adapter for admin operations (amendment 02).

Talks to the Supabase REST API with the service-role key (bypasses RLS —
authorization is enforced in application code via the verified caller's
profile role). Uses httpx, already a project dependency.

Additive lane: never called by the QA pipeline, safety, retrieval, verifier,
vision, audit, or sessions. The anonymous demo never reaches these methods.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

PROFILES_TABLE = "profiles"
ACTIONS_TABLE = "admin_actions"
DEFAULT_TIMEOUT_SECONDS = 10.0


class PostgrestAdminStore:
    """Profiles + admin-action audit over PostgREST (service-role)."""

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

    def get_profile(self, user_id: str) -> dict[str, Any] | None:
        with self._client() as client:
            response = client.get(
                f"/{PROFILES_TABLE}",
                params={"id": f"eq.{user_id}", "select": "*"},
            )
            response.raise_for_status()
            rows = response.json()
            return rows[0] if rows else None

    def upsert_profile_defaults(self, user_id: str, email: str) -> None:
        """Ensure a profile row exists (lazy creation, mirrors 001 design).

        Inserts with `on conflict do nothing` so an existing row (and its
        role/plan) is never overwritten.
        """
        with self._client() as client:
            response = client.post(
                f"/{PROFILES_TABLE}",
                json={"id": user_id, "email": email},
                params={"on_conflict": "id"},
                headers={"Prefer": "resolution=ignore-duplicates"},
            )
            response.raise_for_status()

    def list_profiles(
        self,
        page: int,
        page_size: int,
        search: str = "",
    ) -> tuple[list[dict[str, Any]], int]:
        """One page of profiles (newest first) plus the exact total count."""
        params: dict[str, str] = {
            "select": "*",
            "order": "created_at.desc",
        }
        if search:
            params["email"] = f"ilike.*{search}*"
        start = (page - 1) * page_size
        end = start + page_size - 1
        with self._client() as client:
            response = client.get(
                f"/{PROFILES_TABLE}",
                params=params,
                # count=exact gives the full total in content-range even though
                # the body only carries the requested page.
                headers={"Prefer": "count=exact", "Range": f"{start}-{end}"},
            )
            response.raise_for_status()
            rows = response.json()
            content_range = response.headers.get("content-range", "")
            total = int(content_range.split("/")[-1]) if "/" in content_range else len(rows)
            return rows, total

    def patch_profile(
        self,
        user_id: str,
        changes: dict[str, Any],
    ) -> dict[str, Any] | None:
        with self._client() as client:
            response = client.patch(
                f"/{PROFILES_TABLE}",
                params={"id": f"eq.{user_id}"},
                json=changes,
                headers={"Prefer": "return=representation"},
            )
            response.raise_for_status()
            rows = response.json()
            return rows[0] if rows else None

    def record_action(
        self,
        actor_id: str,
        action: str,
        target_type: str,
        target_id: str,
        payload: dict[str, Any],
    ) -> None:
        with self._client() as client:
            response = client.post(
                f"/{ACTIONS_TABLE}",
                json={
                    "actor_id": actor_id,
                    "action": action,
                    "target_type": target_type,
                    "target_id": target_id,
                    "payload": payload,
                },
            )
            response.raise_for_status()

    def list_actions(self, limit: int) -> list[dict[str, Any]]:
        with self._client() as client:
            response = client.get(
                f"/{ACTIONS_TABLE}",
                params={"order": "created_at.desc", "limit": str(limit)},
            )
            response.raise_for_status()
            return response.json()
