"""PostgREST adapter for saved history (P4, decision 1).

Talks to the Supabase REST API with the service-role key (bypasses RLS —
ownership is enforced in application code via verified user claims). Uses
httpx, which is already a project dependency; no new packages.

Additive lane: never called by the QA pipeline, safety, retrieval, verifier,
vision, audit, or sessions. The anonymous demo never reaches these methods.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

TABLE = "saved_queries"
DEFAULT_TIMEOUT_SECONDS = 10.0


class PostgrestSavedHistoryStore:
    """CRUD over PostgREST for the `saved_queries` table."""

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

    def list(self, user_id: str) -> list[dict[str, Any]]:
        with self._client() as client:
            response = client.get(
                f"/{TABLE}",
                params={"user_id": f"eq.{user_id}", "order": "created_at.desc"},
            )
            response.raise_for_status()
            return response.json()

    def create(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        row = {"user_id": user_id, **payload}
        with self._client() as client:
            response = client.post(
                f"/{TABLE}",
                json=row,
                headers={"Prefer": "return=representation"},
            )
            response.raise_for_status()
            return response.json()[0]

    def delete(self, user_id: str, item_id: str) -> bool:
        with self._client() as client:
            response = client.delete(
                f"/{TABLE}",
                params={"id": f"eq.{item_id}", "user_id": f"eq.{user_id}"},
                headers={"Prefer": "return=representation"},
            )
            response.raise_for_status()
            # PostgREST returns the deleted rows; empty list means not owner/absent.
            return bool(response.json())