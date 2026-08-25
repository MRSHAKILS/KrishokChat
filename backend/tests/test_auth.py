"""Auth lane tests (P3, amendment 15).

Unit tests use a locally generated ES256 keypair and a stubbed JWKS fetch —
no network. Integration tests hit the real hosted Supabase project when
SUPABASE_URL + SUPABASE_PUBLISHABLE_KEY are present in backend/.env.local
(auto-skipped otherwise; they are present in this repo's .env.local).
"""

from __future__ import annotations

import time
import unittest
from contextlib import contextmanager

import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.application.auth import AuthService
from app.core.config import settings
from app.infrastructure.auth.jwks import SupabaseJWKSVerifier
from app.main import create_app


def _make_keypair():
    """Generate an ES256 keypair + JWKS dict (mirrors Supabase's shape)."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()
    x = numbers.x.to_bytes(32, "big")
    y = numbers.y.to_bytes(32, "big")
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": __import__("base64").urlsafe_b64encode(x).rstrip(b"=").decode(),
        "y": __import__("base64").urlsafe_b64encode(y).rstrip(b"=").decode(),
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


class JWKSVerifierUnitTests(unittest.TestCase):
    """Offline verification behavior: valid, garbage, expired, rotated keys."""

    def setUp(self) -> None:
        self.jwk, self.pem = _make_keypair()

    def _verifier(self, keys_by_kid: dict[str, dict] | None = None) -> SupabaseJWKSVerifier:
        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        keys = keys_by_kid if keys_by_kid is not None else {self.jwk["kid"]: self.jwk}

        def fake_fetch() -> dict:
            return {"keys": list(keys.values())}

        verifier._fetch_jwks = fake_fetch  # type: ignore[method-assign]
        return verifier

    def _token(self, kid: str | None = None, **claims) -> str:
        header = {"alg": "ES256", "typ": "JWT"}
        if kid:
            header["kid"] = kid
        payload = {"sub": "user-1", "email": "u@example.com", "aud": "authenticated"}
        payload.update(claims)
        return jwt.encode(payload, self.pem, algorithm="ES256", headers=header)

    def test_valid_token_yields_claims(self) -> None:
        claims = self._verifier().verify(self._token(kid=self.jwk["kid"]))
        self.assertIsNotNone(claims)
        self.assertEqual(claims["sub"], "user-1")
        self.assertEqual(claims["email"], "u@example.com")

    def test_garbage_token_is_denied(self) -> None:
        self.assertIsNone(self._verifier().verify("not.a.jwt"))

    def test_tampered_token_is_denied(self) -> None:
        token = self._token(kid=self.jwk["kid"])
        tampered = token[:-4] + ("AAAA" if not token.endswith("AAAA") else "BBBB")
        self.assertIsNone(self._verifier().verify(tampered))

    def test_expired_token_is_denied(self) -> None:
        token = self._token(kid=self.jwk["kid"], exp=int(time.time()) - 60)
        self.assertIsNone(self._verifier().verify(token))

    def test_unknown_kid_triggers_refresh(self) -> None:
        rotated_jwk, rotated_pem = _make_keypair()
        rotated_jwk["kid"] = "rotated-1"
        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        # First fetch returns the old key set; refresh (force=True) returns the new one.
        state = {"fetches": 0}

        def fake_fetch() -> dict:
            state["fetches"] += 1
            if state["fetches"] == 1:
                return {"keys": [self.jwk]}
            return {"keys": [rotated_jwk]}

        verifier._fetch_jwks = fake_fetch  # type: ignore[method-assign]
        token = jwt.encode(
            {"sub": "user-2", "aud": "authenticated"},
            rotated_pem,
            algorithm="ES256",
            headers={"kid": "rotated-1"},
        )
        claims = verifier.verify(token)
        self.assertIsNotNone(claims)
        self.assertEqual(claims["sub"], "user-2")
        self.assertEqual(state["fetches"], 2)

    def test_no_kid_header_is_denied(self) -> None:
        verifier = self._verifier()
        token = jwt.encode({"sub": "x"}, self.pem, algorithm="ES256")  # no kid
        self.assertIsNone(verifier.verify(token))

    def test_wrong_algorithm_is_denied(self) -> None:
        token = jwt.encode({"sub": "x"}, "secret", algorithm="HS256")
        self.assertIsNone(self._verifier().verify(token))

    def test_service_without_verifier_denies(self) -> None:
        service = AuthService(verifier=None)
        self.assertIsNone(service.claims_from_authorization("Bearer anything"))
        self.assertIsNone(service.claims_from_authorization(None))


class AuthEndpointTests(unittest.TestCase):
    """/auth/me contract: 401 without token, 200 with a valid one (offline).

    The valid-token case uses a locally generated key via an injected
    AuthService, keeping the endpoint contract test network-free.
    """

    @contextmanager
    def _client_with_verifier(self, verifier: SupabaseJWKSVerifier) -> TestClient:
        from dataclasses import replace

        from app.application.admin import AdminService
        from app.application.auth import AuthService
        from app.application.container import AppContainer

        app = create_app()
        client = TestClient(app)
        with client:
            # Lifespan has now run; swap in the injected auth service. The
            # admin store is also swapped to an unconfigured stub so this
            # contract test stays fully offline even when .env.local carries
            # real Supabase credentials (a fabricated test sub must never
            # reach the live profiles table).
            container: AppContainer = client.app.state.container
            client.app.state.container = replace(
                container,
                auth=AuthService(verifier=verifier),
                admin=AdminService(store=None),
            )
            yield client

    def test_me_without_token_returns_401(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/auth/me")
            self.assertEqual(response.status_code, 401)

    def test_me_with_bad_token_returns_401(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/auth/me", headers={"Authorization": "Bearer garbage"})
            self.assertEqual(response.status_code, 401)

    def test_me_with_valid_token_returns_claims(self) -> None:
        jwk, pem = _make_keypair()
        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        verifier._fetch_jwks = lambda: {"keys": [jwk]}  # type: ignore[method-assign]
        token = jwt.encode(
            {"sub": "user-42", "email": "farmer@example.com", "aud": "authenticated", "role": "authenticated"},
            pem,
            algorithm="ES256",
            headers={"kid": jwk["kid"]},
        )
        with self._client_with_verifier(verifier) as client:
            response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
            self.assertEqual(response.status_code, 200)
            body = response.json()["user"]
            self.assertEqual(body["id"], "user-42")
            self.assertEqual(body["email"], "farmer@example.com")


@unittest.skipUnless(
    settings.supabase_url and settings.supabase_publishable_key,
    "Supabase env not configured; skipping live integration test",
)
class LiveSupabaseIntegrationTests(unittest.TestCase):
    """Real token from the hosted project, verified against its live JWKS."""

    def setUp(self) -> None:
        email = "test@krishokchat.com"
        password = "test-password-123"
        response = httpx.post(
            f"{settings.supabase_url}/auth/v1/token?grant_type=password",
            json={"email": email, "password": password},
            headers={
                "apikey": settings.supabase_publishable_key,
                "Content-Type": "application/json",
            },
            timeout=15.0,
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.access_token = response.json()["access_token"]

    def test_live_token_verifies_against_jwks(self) -> None:
        verifier = SupabaseJWKSVerifier(settings.supabase_jwks_url)
        claims = verifier.verify(self.access_token)
        self.assertIsNotNone(claims)
        self.assertEqual(claims["email"], "test@krishokchat.com")
        self.assertEqual(claims["aud"], "authenticated")

    def test_live_token_accepted_by_auth_me(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get(
                "/auth/me",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["user"]["email"], "test@krishokchat.com")


if __name__ == "__main__":
    unittest.main()