"""Supabase JWT verification via the project JWKS endpoint (ES256).

Lazy by design: no HTTP traffic happens until a token is actually presented,
so the offline demo and the anonymous path never touch the network. Fail
closed: every fetch/decode/expiry problem returns None (no claims) rather
than raising, so callers can only ever *deny* access, never mis-grant it.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

import httpx
import jwt
from jwt import PyJWK

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_CACHE_TTL_SECONDS = 300.0


class SupabaseJWKSVerifier:
    """Verifies Supabase user access tokens against the project JWKS."""

    def __init__(
        self,
        jwks_url: str,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        cache_ttl_seconds: float = DEFAULT_CACHE_TTL_SECONDS,
    ) -> None:
        self._jwks_url = jwks_url
        self._timeout = timeout_seconds
        self._cache_ttl = cache_ttl_seconds
        self._lock = threading.Lock()
        self._keys: dict[str, Any] = {}
        self._fetched_at = 0.0

    # -- JWKS loading -----------------------------------------------------

    def _fetch_jwks(self) -> dict[str, Any]:
        """GET the JWKS document. Raises on any failure (caller handles)."""
        with httpx.Client(timeout=self._timeout) as client:
            response = client.get(self._jwks_url)
            response.raise_for_status()
            return response.json()

    def _load_keys(self, force: bool = False) -> None:
        with self._lock:
            if force or not self._keys or time.monotonic() - self._fetched_at > self._cache_ttl:
                doc = self._fetch_jwks()
                keys = {
                    key["kid"]: PyJWK(key)
                    for key in doc.get("keys", [])
                    if key.get("kid")
                }
                self._keys = keys
                self._fetched_at = time.monotonic()

    # -- Verification -----------------------------------------------------

    def verify(self, token: str) -> dict[str, Any] | None:
        try:
            kid = jwt.get_unverified_header(token).get("kid")
            if not kid:
                return None
            try:
                self._load_keys()
            except Exception:
                logger.warning("Supabase JWKS fetch failed; denying token", exc_info=True)
                return None
            jwk = self._keys.get(kid)
            if jwk is None:
                # Unknown kid: keys may have rotated. One refresh attempt.
                try:
                    self._load_keys(force=True)
                except Exception:
                    logger.warning("Supabase JWKS refresh failed; denying token", exc_info=True)
                    return None
                jwk = self._keys.get(kid)
                if jwk is None:
                    return None
            claims = jwt.decode(
                token,
                jwk.key,
                algorithms=["ES256"],
                options={"verify_aud": False},
            )
            return claims if isinstance(claims, dict) else None
        except jwt.ExpiredSignatureError:
            logger.info("Supabase token rejected: expired")
            return None
        except Exception:
            logger.info("Supabase token rejected: invalid", exc_info=True)
            return None