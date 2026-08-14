"""Saved-history port: per-user storage of chat Q&A pairs (premium lane, P4)."""

from __future__ import annotations

from typing import Any, Protocol


class SavedHistoryStore(Protocol):
    """Persists saved Q&A pairs for a user. Implementations must be additive:
    never affect the QA pipeline, safety, retrieval, or audit behavior."""

    def list(self, user_id: str) -> list[dict[str, Any]]: ...

    def create(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]: ...

    def delete(self, user_id: str, item_id: str) -> bool: ...