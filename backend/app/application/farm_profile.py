"""P1: farm-profile application service (additive auth lane).

Storage is a Supabase ``farm_profiles`` row per user (migration 004) written
via PostgREST with the service-role key — same lazy rules as the admin and
notification lanes: zero network I/O at startup, unconfigured → honest
unavailability, never a gate on any existing feature. Free-text fields are
PII-redacted on write (T1-04 redactor); authorization is "caller owns own
row" (the user id comes from the VERIFIED token, never the payload).
"""

from __future__ import annotations

import logging
import re
from datetime import date
from typing import Any

import httpx

from app.core.redaction import redact_pii as redact

logger = logging.getLogger(__name__)

FARM_TABLE = "farm_profiles"
DEFAULT_TIMEOUT_SECONDS = 10.0

_MAX_CROP = 40
_MAX_UPAZILA = 80
_MAX_NOTE = 500


class FarmProfileUnavailableError(Exception):
    """Raised when the profile store is not configured or unreachable."""


class PostgrestFarmProfileStore:
    """farm_profiles over PostgREST (service-role; RLS also enforces owner-only)."""

    def __init__(self, supabase_url: str, service_role_key: str, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> None:
        self._base = f"{supabase_url.rstrip('/')}/rest/v1"
        self._headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        }
        self._timeout = timeout_seconds

    def _client(self) -> httpx.Client:
        return httpx.Client(base_url=self._base, headers=self._headers, timeout=self._timeout)

    def get(self, user_id: str) -> dict[str, Any] | None:
        with self._client() as client:
            response = client.get(f"/{FARM_TABLE}", params={"user_uuid": f"eq.{user_id}", "select": "*"})
            response.raise_for_status()
            rows = response.json()
            return rows[0] if rows else None

    def upsert(self, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        row = {"user_uuid": user_id, **data, "updated_at": "now()"}
        with self._client() as client:
            response = client.post(
                f"/{FARM_TABLE}",
                params={"on_conflict": "user_uuid"},
                headers={**self._headers, "Prefer": "resolution=merge-duplicates,return=representation"},
                json=row,
            )
            response.raise_for_status()
            rows = response.json()
            return rows[0] if rows else row


class FarmProfileService:
    def __init__(self, store: PostgrestFarmProfileStore | None) -> None:
        self._store = store

    @property
    def configured(self) -> bool:
        return self._store is not None

    def get(self, user_id: str) -> dict[str, Any] | None:
        if self._store is None or not user_id:
            return None
        try:
            return self._store.get(user_id)
        except httpx.HTTPError as exc:
            logger.warning("farm profile fetch failed for %s: %s", user_id[:8], exc)
            raise FarmProfileUnavailableError("profile store unreachable") from exc

    def save(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self._store is None or not user_id:
            raise FarmProfileUnavailableError("profile storage not configured")
        cleaned = _validate(payload)
        try:
            return self._store.upsert(user_id, cleaned)
        except httpx.HTTPError as exc:
            logger.warning("farm profile save failed for %s: %s", user_id[:8], exc)
            raise FarmProfileUnavailableError("profile store unreachable") from exc


def _validate(payload: dict[str, Any]) -> dict[str, Any]:
    crop = _clean(payload.get("primary_crop"), _MAX_CROP)
    if not crop:
        raise ValueError("primary_crop is required")
    sowing = str(payload.get("sowing_date") or "").strip()[:10]
    if sowing:
        try:
            date.fromisoformat(sowing)
        except ValueError as exc:
            raise ValueError("sowing_date must be an ISO date (YYYY-MM-DD)") from exc
    else:
        sowing = None
    upazila = _clean(payload.get("upazila"), _MAX_UPAZILA) or None
    # PII redaction on free text (best-effort; never claimed perfect).
    note = redact(str(payload.get("note") or "").strip()[:_MAX_NOTE]) or None
    return {"primary_crop": crop, "sowing_date": sowing, "upazila": upazila, "note": note}


def _clean(value: object, limit: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "").strip())
    return text[:limit]
