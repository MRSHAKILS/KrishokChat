"""T0-07: API-key auth + in-memory rate limiting for the /api/v1 surface.

Two FastAPI dependencies, attached ONLY to the versioned surface in
``app/main.py`` (per-include dependencies on the v1 mounts — the legacy
``/api/*`` routers never carry them):

- ``require_api_key``: pass-through while ``API_KEY_ENABLED=false`` (the
  anonymous demo is untouched — AGENTS.md §2.1); otherwise the request must
  present a configured key (``Authorization: Bearer <key>`` or
  ``X-API-Key: <key>``) or it receives 401 with ``WWW-Authenticate``.
- ``rate_limit``: pass-through when neither switch is on. When a key
  authenticated, the identity is the key's sha256 hash (per-key cap);
  otherwise the identity is the client IP, and anonymous IP limiting is
  active ONLY when ``RATE_LIMIT_ANON_ENABLED=true``. Over the cap -> 429
  with ``Retry-After``.

The key store and the limiter are built once per app in ``create_app`` and
live on ``app.state`` so every request shares the same sliding window.

Keys are never logged in full: log lines carry a label (``env-key-<n>`` for
the env-literal store) and the first 12 hex chars of the key's sha256.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import math
import threading
import time
from collections import deque
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.api.dependencies import SettingsDep
from app.core.config import Settings

logger = logging.getLogger("krishokchat")

KEY_LABEL = "env-key"
_DIGEST_LEN = 12


class KeyStore:
    """Configured literal keys from the environment (comma-separated).

    Each entry is a bare secret; the label is derived from its position so
    logs and (future) audit records can name a key without revealing it.
    Matching is constant-time. The SQLite-backed store (T0-01, keys table)
    is a documented follow-up that swaps this class, not the dependency.
    """

    def __init__(self, raw: str) -> None:
        self._secrets: list[tuple[str, str]] = []
        for idx, token in enumerate((raw or "").split(",")):
            token = token.strip()
            if token:
                self._secrets.append((f"{KEY_LABEL}-{idx + 1}", token))

    def __bool__(self) -> bool:
        return bool(self._secrets)

    def __len__(self) -> int:
        return len(self._secrets)

    def authenticate(self, presented: str | None) -> tuple[str, str] | None:
        """Return ``(label, digest)`` for a valid key, else ``None``."""
        if not presented:
            return None
        for label, secret in self._secrets:
            if hmac.compare_digest(secret, presented):
                digest = hashlib.sha256(secret.encode("utf-8")).hexdigest()
                return label, digest[:_DIGEST_LEN]
        return None


class SlidingWindowRateLimiter:
    """Stdlib-only in-memory sliding-window limiter (no new dependency).

    Tracks request timestamps per identity in a deque; the window slides by
    pruning stamps older than ``window_seconds`` before checking the cap.
    """

    def __init__(self, limit: int, window_seconds: float = 60.0) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def allow(self, key: str) -> tuple[bool, float]:
        """Return ``(allowed, retry_after_seconds)`` for one request."""
        if self.limit <= 0:
            return True, 0.0
        now = time.monotonic()
        with self._lock:
            stamps = self._hits.get(key)
            if stamps is None:
                stamps = deque()
                self._hits[key] = stamps
            cutoff = now - self.window_seconds
            while stamps and stamps[0] <= cutoff:
                stamps.popleft()
            if len(stamps) >= self.limit:
                retry_after = math.ceil(self.window_seconds - (now - stamps[0]))
                return False, max(1, retry_after)
            stamps.append(now)
            return True, 0.0


def _presented_key(request: Request) -> str | None:
    authorization = request.headers.get("authorization", "")
    if authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    api_key = request.headers.get("x-api-key")
    if api_key:
        return api_key.strip()
    return None


async def require_api_key(
    request: Request,
    settings: SettingsDep = None,  # type: ignore[assignment]  # FastAPI injects via Annotated
) -> None:
    """v1-only guard: pass-through when disabled, 401 otherwise.

    On success the authenticated key's digest (never the key itself) is
    stashed on ``request.state`` for the rate limiter and future audit use.
    """
    if not settings.api_key_enabled:
        request.state.authenticated_api_key = None
        request.state.api_key_label = None
        return
    store = getattr(request.app.state, "api_key_store", None)
    if store is None:
        store = KeyStore(settings.api_keys)
    matched = store.authenticate(_presented_key(request))
    if matched is None:
        logger.debug("api key rejected for /api/v1 request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    label, digest = matched
    request.state.authenticated_api_key = digest
    request.state.api_key_label = label
    logger.debug(
        "api key accepted for /api/v1 request",
        extra={"key_label": label, "key_hash": digest},
    )


async def rate_limit(
    request: Request,
    settings: SettingsDep = None,  # type: ignore[assignment]  # FastAPI injects via Annotated
) -> None:
    """v1-only limiter: per-key when a key authenticated, per-IP for
    anonymous requests only when ``RATE_LIMIT_ANON_ENABLED=true``. With both
    switches off this is a pure pass-through (demo-identical)."""
    limiter = getattr(request.app.state, "rate_limiter", None)
    if limiter is None:
        return
    key_digest = getattr(request.state, "authenticated_api_key", None)
    if key_digest is not None:
        identity = f"key:{key_digest}"
    elif settings.rate_limit_anon_enabled:
        client = request.client
        identity = f"ip:{client.host if client else 'unknown'}"
    else:
        return
    allowed, retry_after = limiter.allow(identity)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)},
        )


V1GuardDep = Annotated[None, Depends(require_api_key)]
V1RateLimitDep = Annotated[None, Depends(rate_limit)]


def build_v1_guard_state(settings: Settings) -> dict:
    """App-state pieces for the v1 guard, built once in ``create_app``."""
    return {
        "api_key_store": KeyStore(settings.api_keys),
        "rate_limiter": (
            SlidingWindowRateLimiter(settings.rate_limit_per_minute)
            if settings.rate_limit_per_minute > 0
            else None
        ),
    }