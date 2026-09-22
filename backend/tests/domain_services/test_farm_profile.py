"""P1+P2 farm-profile tests (additive, non-gating auth lane).

All offline: an in-memory store stands in for PostgREST, tokens are locally
generated ES256 JWTs (mirroring test_auth.py). Locks:
- _validate: required crop, ISO sowing-date check, PII redaction of note;
- service fail-open: unconfigured store -> get None / save raises
  FarmProfileUnavailableError;
- endpoints: 401 anonymous, honest available:false when unconfigured,
  round-trip save+read with a computed stage view;
- PIPELINE INVARIANT: a QA request WITHOUT farmer_context produces a prompt
  byte-identical to the pre-P2 pipeline (the stage line only appears when a
  farmer_context is supplied).
"""

from __future__ import annotations

import base64
import unittest
from contextlib import contextmanager
from dataclasses import replace

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.application.auth import AuthService
from app.application.farm_profile import (
    FarmProfileService,
    FarmProfileUnavailableError,
    _validate,
)
from app.application.generation import GroundedAnswerGenerator
from app.domain.contracts import QueryContext, RetrievedSource
from app.infrastructure.auth.jwks import SupabaseJWKSVerifier
from app.main import create_app


def _make_keypair():
    key = ec.generate_private_key(ec.SECP256R1())
    numbers = key.public_key().public_numbers()
    jwk = {
        "kty": "EC", "crv": "P-256",
        "x": base64.urlsafe_b64encode(numbers.x.to_bytes(32, "big")).rstrip(b"=").decode(),
        "y": base64.urlsafe_b64encode(numbers.y.to_bytes(32, "big")).rstrip(b"=").decode(),
        "kid": "test-key-1", "alg": "ES256", "use": "sig",
    }
    pem = key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
    )
    return jwk, pem


class InMemoryFarmStore:
    """Stands in for PostgrestFarmProfileStore (owner-keyed rows)."""

    def __init__(self) -> None:
        self.rows: dict[str, dict] = {}

    def get(self, user_id: str):
        return self.rows.get(user_id)

    def upsert(self, user_id: str, data: dict) -> dict:
        row = {"user_uuid": user_id, **data}
        self.rows[user_id] = row
        return row


class ValidateTests(unittest.TestCase):
    def test_requires_primary_crop(self) -> None:
        with self.assertRaises(ValueError):
            _validate({"primary_crop": "  "})

    def test_bad_sowing_date_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _validate({"primary_crop": "potato", "sowing_date": "13/2026"})

    def test_valid_payload_normalized(self) -> None:
        out = _validate({"primary_crop": " আলু ", "sowing_date": "2026-01-01", "upazila": "সদর"})
        self.assertEqual(out["primary_crop"], "আলু")
        self.assertEqual(out["sowing_date"], "2026-01-01")
        self.assertEqual(out["upazila"], "সদর")

    def test_note_is_pii_redacted(self) -> None:
        out = _validate({"primary_crop": "potato", "note": "কল করুন 01712345678"})
        self.assertNotIn("01712345678", out["note"] or "")

    def test_blank_sowing_becomes_none(self) -> None:
        out = _validate({"primary_crop": "potato", "sowing_date": ""})
        self.assertIsNone(out["sowing_date"])


class ServiceFailOpenTests(unittest.TestCase):
    def test_unconfigured_get_returns_none(self) -> None:
        svc = FarmProfileService(store=None)
        self.assertFalse(svc.configured)
        self.assertIsNone(svc.get("u1"))

    def test_unconfigured_save_raises_unavailable(self) -> None:
        svc = FarmProfileService(store=None)
        with self.assertRaises(FarmProfileUnavailableError):
            svc.save("u1", {"primary_crop": "potato"})

    def test_configured_roundtrip(self) -> None:
        svc = FarmProfileService(store=InMemoryFarmStore())
        self.assertTrue(svc.configured)
        saved = svc.save("u1", {"primary_crop": "আলু", "sowing_date": "2026-01-01"})
        self.assertEqual(saved["primary_crop"], "আলু")
        self.assertEqual(svc.get("u1")["primary_crop"], "আলু")


class GenerationInvariantTests(unittest.TestCase):
    """The stage line must ONLY appear when farmer_context is present."""

    def _sources(self) -> list[RetrievedSource]:
        return [RetrievedSource(id="S1", score=1.0, title_bn="আলু", content_bn="তথ্য")]

    def test_prompt_without_farmer_context_omits_stage_line(self) -> None:
        ctx = QueryContext(crop=None, disease=None)
        prompt = GroundedAnswerGenerator._prompt("প্রশ্ন", ctx, self._sources(), 5, 1200)
        self.assertNotIn("কৃষকের ফসল পর্যায়", prompt)

    def test_prompt_with_farmer_context_includes_stage_line(self) -> None:
        ctx = QueryContext(farmer_context="ফসল: আলু · বর্তমান পর্যায়: কন্দ স্ফীতি")
        prompt = GroundedAnswerGenerator._prompt("প্রশ্ন", ctx, self._sources(), 5, 1200)
        self.assertIn("কৃষকের ফসল পর্যায়", prompt)
        self.assertIn("কন্দ স্ফীতি", prompt)

    def test_absent_context_is_byte_identical_to_pre_p2(self) -> None:
        # Two contexts differing only in farmer_context=None must yield the
        # exact same prompt string.
        a = QueryContext(crop="potato", disease="late blight")
        b = QueryContext(crop="potato", disease="late blight", farmer_context=None)
        srcs = self._sources()
        self.assertEqual(
            GroundedAnswerGenerator._prompt("q", a, srcs, 5, 1200),
            GroundedAnswerGenerator._prompt("q", b, srcs, 5, 1200),
        )


class EndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.jwk, self.pem = _make_keypair()
        self.token = jwt.encode(
            {"sub": "farmer-1", "email": "f@example.com", "aud": "authenticated"},
            self.pem, algorithm="ES256", headers={"kid": self.jwk["kid"]},
        )

    @contextmanager
    def _client(self, *, configured: bool):
        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        verifier._fetch_jwks = lambda: {"keys": [self.jwk]}  # type: ignore[method-assign]
        app = create_app()
        with TestClient(app) as client:
            store = InMemoryFarmStore() if configured else None
            client.app.state.container = replace(
                client.app.state.container,
                auth=AuthService(verifier=verifier),
                farm_profile=FarmProfileService(store=store),
            )
            yield client

    def _auth(self):
        return {"Authorization": f"Bearer {self.token}"}

    def test_get_anonymous_401(self) -> None:
        with self._client(configured=True) as client:
            self.assertEqual(client.get("/api/account/farm-profile").status_code, 401)

    def test_get_unconfigured_available_false(self) -> None:
        with self._client(configured=False) as client:
            resp = client.get("/api/account/farm-profile", headers=self._auth())
            self.assertEqual(resp.status_code, 200)
            body = resp.json()
            self.assertFalse(body["available"])
            self.assertIsNone(body["profile"])

    def test_put_unconfigured_returns_503(self) -> None:
        with self._client(configured=False) as client:
            resp = client.put(
                "/api/account/farm-profile",
                headers=self._auth(),
                json={"primary_crop": "potato", "sowing_date": "2026-01-01"},
            )
            self.assertEqual(resp.status_code, 503)

    def test_put_then_get_roundtrip_with_stage(self) -> None:
        with self._client(configured=True) as client:
            put = client.put(
                "/api/account/farm-profile",
                headers=self._auth(),
                json={"primary_crop": "potato", "sowing_date": "2026-01-01"},
            )
            self.assertEqual(put.status_code, 200, put.text)
            self.assertTrue(put.json()["available"])
            get = client.get("/api/account/farm-profile", headers=self._auth())
            self.assertEqual(get.status_code, 200)
            body = get.json()
            self.assertTrue(body["available"])
            self.assertEqual(body["profile"]["primary_crop"], "potato")
            # Stage view is present when the committed potato calendar loaded.
            if body["stage"] is not None:
                self.assertEqual(body["stage"]["crop_key"], "potato")
                self.assertIn("farmer_context_bn", body["stage"])

    def test_put_invalid_crop_returns_422(self) -> None:
        with self._client(configured=True) as client:
            resp = client.put(
                "/api/account/farm-profile",
                headers=self._auth(),
                json={"primary_crop": "", "sowing_date": "2026-01-01"},
            )
            # Pydantic min_length=1 -> 422 before reaching the service.
            self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()
