"""T0-07: API versioning + API keys + rate limits + pagination tests.

Covers: every legacy /api/* path stays byte-identical on its /api/v1/*
mirror (same endpoint functions, same bodies); v1 routes respond with the
guard off; API_KEY_ENABLED=true -> no key = 401, wrong key = 401, correct
key = 200 (and legacy paths stay open); over-limit = 429 with Retry-After;
anonymous defaults unaffected (both switches off = limiter pass-through);
pagination on /api/history returns the same totals with page/page_size
while the default call returns the full list exactly as before.

All offline: no network calls. QA terminal cases hit deterministic safety
rules before any LLM; vision cases are rejected on content-type before any
model load; history uses a faked store + locally generated ES256 token
(same pattern as test_history).
"""

from __future__ import annotations

import base64
import tempfile
import unittest
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.application.auth import AuthService
from app.application.history import HistoryService
from app.core.config import Settings
from app.infrastructure.auth.jwks import SupabaseJWKSVerifier
from app.main import create_app

BANNED_QUERY = "paraquat কীভাবে ব্যবহার করব"


def _make_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()
    x = numbers.x.to_bytes(32, "big")
    y = numbers.y.to_bytes(32, "big")
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": base64.urlsafe_b64encode(x).rstrip(b"=").decode(),
        "y": base64.urlsafe_b64encode(y).rstrip(b"=").decode(),
        "kid": "test-key-1",
        "alg": "ES256",
        "use": "sig",
    }
    pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    return jwk, pem


def _user_token(user_id: str = "user-1"):
    jwk, pem = _make_keypair()
    token = jwt.encode(
        {"sub": user_id, "aud": "authenticated"},
        pem,
        algorithm="ES256",
        headers={"kid": jwk["kid"]},
    )
    return token, jwk


def _settings(**overrides) -> Settings:
    """Isolated settings: temp audit file, never the live demo log."""
    tmp = tempfile.mkdtemp()
    base = {"audit_log_path": str(Path(tmp) / "audit.jsonl")}
    base.update(overrides)
    return Settings(**base)


class AliasSurfaceTests(unittest.TestCase):
    """Every legacy path returns a byte-identical body on its /api/v1 mirror."""

    def _client(self, settings: Settings):
        return TestClient(create_app(config=settings))

    def test_legacy_and_v1_health(self) -> None:
        with self._client(_settings()) as client:
            legacy = client.get("/health")
            self.assertEqual(legacy.status_code, 200)
            self.assertNotIn("v1", legacy.json()["status"])

    def test_qa_terminal_alias_identical(self) -> None:
        with self._client(_settings()) as client:
            legacy = client.post("/api/qa", json={"query": BANNED_QUERY})
            v1 = client.post("/api/v1/qa", json={"query": BANNED_QUERY})
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1.status_code, 200)
        self.assertEqual(legacy.json(), v1.json())
        self.assertEqual(v1.json()["category"], "banned_or_restricted_chemical")

    def test_qa_stream_alias_identical(self) -> None:
        with self._client(_settings()) as client:
            legacy = client.post("/api/qa/stream", json={"query": BANNED_QUERY})
            v1 = client.post("/api/v1/qa/stream", json={"query": BANNED_QUERY})
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1.status_code, 200)
        self.assertEqual(legacy.text, v1.text)
        self.assertIn("banned_or_restricted_chemical", v1.text)

    def test_benchmark_alias_identical(self) -> None:
        with self._client(_settings()) as client:
            legacy = client.get("/api/benchmark")
            v1 = client.get("/api/v1/benchmark")
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1.status_code, 200)
        self.assertEqual(legacy.json(), v1.json())

    def test_safety_metrics_alias_identical(self) -> None:
        with self._client(_settings()) as client:
            client.post("/api/qa", json={"query": BANNED_QUERY})
            legacy = client.get("/api/safety/metrics")
            v1 = client.get("/api/v1/safety/metrics")
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1.status_code, 200)
        self.assertEqual(legacy.json(), v1.json())

    def test_tts_voices_alias_identical(self) -> None:
        with self._client(_settings()) as client:
            legacy = client.get("/api/tts/voices")
            v1 = client.get("/api/v1/tts/voices")
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1.status_code, 200)
        self.assertEqual(legacy.json(), v1.json())

    def test_soil_dataset_alias_identical(self) -> None:
        with self._client(_settings()) as client:
            legacy = client.get("/api/soil/dataset")
            v1 = client.get("/api/v1/soil/dataset")
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1.status_code, 200)
        self.assertEqual(legacy.json(), v1.json())

    def test_classify_rejects_non_image_identically(self) -> None:
        files = {"file": ("notes.txt", b"not an image", "text/plain")}
        with self._client(_settings()) as client:
            legacy = client.post("/api/classify", files=files)
            v1 = client.post("/api/v1/classify", files=files)
        self.assertEqual(legacy.status_code, 400)
        self.assertEqual(legacy.json(), v1.json())

    def test_detect_rejects_non_image_identically(self) -> None:
        files = {"file": ("notes.txt", b"not an image", "text/plain")}
        with self._client(_settings()) as client:
            legacy = client.post("/api/detect", files=files)
            v1 = client.post("/api/v1/detect", files=files)
        self.assertEqual(legacy.status_code, 400)
        self.assertEqual(legacy.json(), v1.json())

    def test_helpline_register_alias_identical(self) -> None:
        payload = {"name": "রহিম", "phone": "01711111111", "district": "রংপুর"}
        with self._client(_settings()) as client:
            legacy = client.post("/api/helpline/register", json=payload)
            v1 = client.post("/api/v1/helpline/register", json=payload)
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1.status_code, 200)
        self.assertEqual(legacy.json(), v1.json())

    def test_transcribe_unconfigured_alias_identical(self) -> None:
        # Pin groq_api_key=None: backend/.env.local may set a real key, and
        # the 501 path must be guaranteed offline (no network in tests).
        settings = _settings(groq_api_key=None)
        files = {"file": ("voice.webm", b"audio", "audio/webm")}
        with self._client(settings) as client:
            legacy = client.post("/api/transcribe", files=files)
            v1 = client.post("/api/v1/transcribe", files=files)
        self.assertEqual(legacy.status_code, 501)
        self.assertEqual(legacy.json(), v1.json())

    def test_auth_me_401_alias_identical(self) -> None:
        # The auth router mounts at /auth/me (no /api segment); its v1
        # mirror lands at /api/v1/auth/me.
        with self._client(_settings()) as client:
            legacy = client.get("/auth/me")
            v1 = client.get("/api/v1/auth/me")
        self.assertEqual(legacy.status_code, 401)
        self.assertEqual(v1.status_code, 401)
        self.assertEqual(legacy.json(), v1.json())

    def test_history_401_alias_identical(self) -> None:
        with self._client(_settings()) as client:
            legacy = client.get("/api/history")
            v1 = client.get("/api/v1/history")
        self.assertEqual(legacy.status_code, 401)
        self.assertEqual(v1.status_code, 401)
        self.assertEqual(legacy.json(), v1.json())

    def test_request_id_middleware_still_covers_v1(self) -> None:
        # T0-04 preserved: the v1 surface runs under the same middleware stack.
        with self._client(_settings()) as client:
            response = client.get(
                "/api/v1/tts/voices", headers={"X-Request-ID": "v1-req-1"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-request-id"], "v1-req-1")


class ApiKeyTests(unittest.TestCase):
    def test_guard_off_anonymous_v1_works(self) -> None:
        # Fresh defaults: no keys configured -> v1 open, no 401s.
        with TestClient(create_app(config=_settings())) as client:
            response = client.get("/api/v1/benchmark")
        self.assertEqual(response.status_code, 200)

    def test_keys_enabled_no_key_401_with_www_authenticate(self) -> None:
        settings = _settings(api_key_enabled=True, api_keys="alpha-key,beta-key")
        with TestClient(create_app(config=settings)) as client:
            response = client.get("/api/v1/benchmark")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Bearer", response.headers["www-authenticate"])

    def test_keys_enabled_wrong_key_401(self) -> None:
        settings = _settings(api_key_enabled=True, api_keys="alpha-key,beta-key")
        with TestClient(create_app(config=settings)) as client:
            response = client.get(
                "/api/v1/benchmark", headers={"Authorization": "Bearer wrong-key"}
            )
        self.assertEqual(response.status_code, 401)

    def test_keys_enabled_correct_key_200(self) -> None:
        settings = _settings(api_key_enabled=True, api_keys="alpha-key,beta-key")
        with TestClient(create_app(config=settings)) as client:
            for key in ("alpha-key", "beta-key"):
                response = client.get(
                    "/api/v1/benchmark",
                    headers={"Authorization": f"Bearer {key}"},
                )
                self.assertEqual(response.status_code, 200, key)

    def test_keys_enabled_x_api_key_header_accepted(self) -> None:
        settings = _settings(api_key_enabled=True, api_keys="alpha-key")
        with TestClient(create_app(config=settings)) as client:
            response = client.get(
                "/api/v1/benchmark", headers={"X-API-Key": "alpha-key"}
            )
        self.assertEqual(response.status_code, 200)

    def test_keys_enabled_legacy_paths_stay_open(self) -> None:
        # Keys gate ONLY the v1 surface; anonymous demo paths unchanged.
        settings = _settings(api_key_enabled=True, api_keys="alpha-key")
        with TestClient(create_app(config=settings)) as client:
            legacy = client.get("/api/benchmark")
            v1_without_key = client.get("/api/v1/benchmark")
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(v1_without_key.status_code, 401)

    def test_keys_enabled_post_and_stream_also_gated(self) -> None:
        settings = _settings(api_key_enabled=True, api_keys="alpha-key")
        with TestClient(create_app(config=settings)) as client:
            no_key = client.post("/api/v1/qa", json={"query": BANNED_QUERY})
            with_key = client.post(
                "/api/v1/qa",
                json={"query": BANNED_QUERY},
                headers={"Authorization": "Bearer alpha-key"},
            )
        self.assertEqual(no_key.status_code, 401)
        self.assertEqual(with_key.status_code, 200)
        self.assertEqual(with_key.json()["category"], "banned_or_restricted_chemical")


class RateLimitTests(unittest.TestCase):
    def test_over_limit_429_with_retry_after(self) -> None:
        settings = _settings(
            api_key_enabled=True, api_keys="k1", rate_limit_per_minute=3
        )
        with TestClient(create_app(config=settings)) as client:
            headers = {"Authorization": "Bearer k1"}
            for _ in range(3):
                self.assertEqual(
                    client.get("/api/v1/benchmark", headers=headers).status_code, 200
                )
            limited = client.get("/api/v1/benchmark", headers=headers)
        self.assertEqual(limited.status_code, 429)
        self.assertGreaterEqual(int(limited.headers["retry-after"]), 1)

    def test_limit_is_per_key(self) -> None:
        settings = _settings(
            api_key_enabled=True, api_keys="k1,k2", rate_limit_per_minute=2
        )
        with TestClient(create_app(config=settings)) as client:
            for _ in range(2):
                self.assertEqual(
                    client.get(
                        "/api/v1/benchmark", headers={"Authorization": "Bearer k1"}
                    ).status_code,
                    200,
                )
            self.assertEqual(
                client.get(
                    "/api/v1/benchmark", headers={"Authorization": "Bearer k1"}
                ).status_code,
                429,
            )
            # A different key has its own window.
            for _ in range(2):
                self.assertEqual(
                    client.get(
                        "/api/v1/benchmark", headers={"Authorization": "Bearer k2"}
                    ).status_code,
                    200,
                )

    def test_legacy_paths_not_rate_limited(self) -> None:
        settings = _settings(
            api_key_enabled=True, api_keys="k1", rate_limit_per_minute=2
        )
        with TestClient(create_app(config=settings)) as client:
            for _ in range(5):
                response = client.get("/api/benchmark")
                self.assertEqual(response.status_code, 200)

    def test_anonymous_defaults_unaffected(self) -> None:
        # Both switches off (fresh defaults): limiter is a pass-through even
        # though a limiter object exists with the default 60/min cap.
        with TestClient(create_app(config=_settings())) as client:
            for _ in range(70):
                self.assertEqual(client.get("/api/v1/benchmark").status_code, 200)

    def test_anonymous_ip_limited_when_enabled(self) -> None:
        settings = _settings(rate_limit_anon_enabled=True, rate_limit_per_minute=3)
        with TestClient(create_app(config=settings)) as client:
            for _ in range(3):
                self.assertEqual(client.get("/api/v1/benchmark").status_code, 200)
            limited = client.get("/api/v1/benchmark")
        self.assertEqual(limited.status_code, 429)
        self.assertIn("retry-after", limited.headers)


class PaginationTests(unittest.TestCase):
    """History list pagination: default returns everything (today's
    behavior); page/page_size slice with the same total."""

    def setUp(self) -> None:
        self.token, self.jwk = _user_token()
        self.items = [
            {"id": f"item-{i:02d}", "query_text": f"q{i}", "answer_text": "a",
             "sources": [], "category": "safe_agri",
             "created_at": f"2026-08-14T00:00:{i:02d}Z"}
            for i in range(25)
        ]

        class FakeStore:
            def __init__(self, owner):
                self.owner = owner

            def list(self, user_id):
                return list(self.owner.items)

            def create(self, user_id, payload):
                raise NotImplementedError

            def delete(self, user_id, item_id):
                raise NotImplementedError

        self.store = FakeStore(self)

    @contextmanager
    def _client(self, v1: bool = False):
        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        verifier._fetch_jwks = lambda: {"keys": [self.jwk]}  # type: ignore[method-assign]
        app = create_app(config=_settings())
        with TestClient(app) as client:
            container = client.app.state.container
            client.app.state.container = replace(
                container,
                auth=AuthService(verifier=verifier),
                history=HistoryService(store=self.store),
            )
            yield client

    def _auth(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def test_default_call_returns_full_list_identical_to_today(self) -> None:
        with self._client() as client:
            response = client.get("/api/history", headers=self._auth())
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body["items"]), 25)
        self.assertEqual(body["total"], 25)
        self.assertEqual(body["items"][0]["id"], "item-00")

    def test_paginated_call_returns_page_and_same_total(self) -> None:
        with self._client() as client:
            response = client.get(
                "/api/history", headers=self._auth(), params={"page": 1, "page_size": 10}
            )
        body = response.json()
        self.assertEqual(len(body["items"]), 10)
        self.assertEqual(body["total"], 25)
        self.assertEqual([item["id"] for item in body["items"]][0], "item-00")
        self.assertEqual([item["id"] for item in body["items"]][-1], "item-09")

    def test_last_page_returns_remainder(self) -> None:
        with self._client() as client:
            response = client.get(
                "/api/history", headers=self._auth(), params={"page": 3, "page_size": 10}
            )
        body = response.json()
        self.assertEqual(len(body["items"]), 5)
        self.assertEqual(body["total"], 25)
        self.assertEqual(body["items"][0]["id"], "item-20")

    def test_v1_history_pagination_identical(self) -> None:
        with self._client() as client:
            full = client.get("/api/v1/history", headers=self._auth())
            paged = client.get(
                "/api/v1/history",
                headers=self._auth(),
                params={"page": 2, "page_size": 10},
            )
        self.assertEqual(full.json()["total"], 25)
        self.assertEqual(len(paged.json()["items"]), 10)
        self.assertEqual(paged.json()["total"], 25)
        self.assertEqual(paged.json()["items"][0]["id"], "item-10")


if __name__ == "__main__":
    unittest.main()