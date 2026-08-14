"""Application-layer saved-history service (premium lane, P4 decision 1).

Additive and optional: routes using this service are new and never gate the
demo. When the store is unavailable (no Supabase configuration) the service
fails with a clear 503 instead of raising confusing errors.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.storage.postgrest import PostgrestSavedHistoryStore


class HistoryUnavailableError(RuntimeError):
    """Raised when saved history is not configured (no Supabase env)."""


class HistoryService:
    """Ownership-aware saved-history operations keyed by verified user id."""

    def __init__(self, store: PostgrestSavedHistoryStore | None = None) -> None:
        self._store = store

    def _require_store(self) -> PostgrestSavedHistoryStore:
        if self._store is None:
            raise HistoryUnavailableError("Saved history is not configured on this server")
        return self._store

    def list(self, user_id: str) -> list[dict[str, Any]]:
        return self._require_store().list(user_id)

    def create(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._require_store().create(user_id, payload)

    def delete(self, user_id: str, item_id: str) -> bool:
        return self._require_store().delete(user_id, item_id)