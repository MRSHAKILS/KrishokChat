"""Saved-history lane tests (P4 decision 1).

All offline: PostgREST calls are faked with httpx MockTransport; the auth
dependency is satisfied with a locally generated ES256 token (see test_auth
for the shared pattern). Live end-to-end requires the migration
`supabase/migrations/001_saved_history.sql` applied to the hosted project.
"""

from __future__ import annotations

import unittest
from contextlib import contextmanager

import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.application.history import HistoryService, HistoryUnavailableError
from app.infrastructure.storage.postgrest import PostgrestSavedHistoryStore
from app.main import create_app


def _make_keypair():
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


def _user_token(user_id: str = "user-1") -> str:
    jwk, pem = _make_keypair()
    return (
        jwt.encode(
            {"sub": user_id, "aud": "authenticated"},
            pem,
            algorithm="ES256",
            headers={"kid": jwk["kid"]},
        ),
        jwk,
    )


class PostgrestStoreUnitTests(unittest.TestCase):
    """Store behavior against a faked PostgREST transport."""

    def _store(self, handler) -> PostgrestSavedHistoryStore:
        store = PostgrestSavedHistoryStore("https://x.supabase.co", "svc-key")

        def client():
            # Reuse the store's base/headers/timeout; only the transport is faked.
            return httpx.Client(
                base_url=store._base,
                headers=store._headers,
                timeout=store._timeout,
                transport=httpx.MockTransport(handler),
            )

        store._client = client  # type: ignore[method-assign]
        return store

    def test_list_builds_query_and_parses_rows(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.url.path, "/rest/v1/saved_queries")
            self.assertIn("user_id=eq.user-1", request.url.query.decode())
            self.assertIn("order=created_at.desc", request.url.query.decode())
            self.assertEqual(request.headers["apikey"], "svc-key")
            self.assertEqual(request.headers["authorization"], "Bearer svc-key")
            return httpx.Response(200, json=[{"id": "a", "query_text": "q"}])

        items = self._store(handler).list("user-1")
        self.assertEqual(items[0]["id"], "a")

    def test_create_posts_payload_with_user_id(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.method, "POST")
            self.assertEqual(request.headers["prefer"], "return=representation")
            body = request.read()
            self.assertIn('"user_id":"user-1"', body.decode())
            return httpx.Response(201, json=[{"id": "n1", "query_text": "q", "user_id": "user-1"}])

        row = self._store(handler).create("user-1", {"query_text": "q", "answer_text": "a"})
        self.assertEqual(row["id"], "n1")

    def test_delete_owner_match_returns_true(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.method, "DELETE")
            self.assertIn("id=eq.item-9", request.url.query.decode())
            self.assertIn("user_id=eq.user-1", request.url.query.decode())
            return httpx.Response(200, json=[{"id": "item-9"}])

        self.assertTrue(self._store(handler).delete("user-1", "item-9"))

    def test_delete_non_owner_returns_false(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=[])

        self.assertFalse(self._store(handler).delete("user-1", "item-9"))


class HistoryServiceTests(unittest.TestCase):
    def test_unconfigured_service_raises_503_error(self) -> None:
        service = HistoryService(store=None)
        with self.assertRaises(HistoryUnavailableError):
            service.list("user-1")
        with self.assertRaises(HistoryUnavailableError):
            service.create("user-1", {"query_text": "q"})
        with self.assertRaises(HistoryUnavailableError):
            service.delete("user-1", "id")


class HistoryEndpointTests(unittest.TestCase):
    """Route contract: 401 without token; 200/201/204/404/503 flows."""

    def setUp(self) -> None:
        self.token, self.jwk = _user_token()

    @contextmanager
    def _client(self, store=None):
        from dataclasses import replace

        from app.application.auth import AuthService
        from app.application.history import HistoryService
        from app.infrastructure.auth.jwks import SupabaseJWKSVerifier

        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        verifier._fetch_jwks = lambda: {"keys": [self.jwk]}  # type: ignore[method-assign]

        app = create_app()
        with TestClient(app) as client:
            container = client.app.state.container
            client.app.state.container = replace(
                container,
                auth=AuthService(verifier=verifier),
                history=HistoryService(store=store),
            )
            yield client

    def _auth(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def test_without_token_returns_401(self) -> None:
        with self._client() as client:
            for method, url in [
                ("GET", "/api/history"),
                ("POST", "/api/history"),
                ("DELETE", "/api/history/x"),
            ]:
                response = getattr(client, method.lower())(url)
                self.assertEqual(response.status_code, 401, f"{method} {url}")

    def test_unconfigured_returns_503(self) -> None:
        with self._client() as client:
            response = client.get("/api/history", headers=self._auth())
            self.assertEqual(response.status_code, 503)

    def test_list_flow(self) -> None:
        class FakeStore:
            def list(self, user_id):
                return [{"id": "s1", "query_text": "q", "answer_text": "a", "sources": [], "category": "safe_agri", "created_at": "2026-08-14T00:00:00Z"}]

            def create(self, user_id, payload):
                raise NotImplementedError

            def delete(self, user_id, item_id):
                raise NotImplementedError

        with self._client(FakeStore()) as client:
            response = client.get("/api/history", headers=self._auth())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["items"][0]["id"], "s1")

    def test_create_flow(self) -> None:
        class FakeStore:
            def list(self, user_id):
                raise NotImplementedError

            def create(self, user_id, payload):
                return {**payload, "id": "n1", "user_id": user_id, "created_at": "2026-08-14T00:00:00Z"}

            def delete(self, user_id, item_id):
                raise NotImplementedError

        with self._client(FakeStore()) as client:
            response = client.post(
                "/api/history",
                headers=self._auth(),
                json={"query_text": "ধানের রোগ", "answer_text": "উত্তর", "sources": [], "category": "safe_agri"},
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["id"], "n1")

    def test_delete_owner_flow(self) -> None:
        class FakeStore:
            def list(self, user_id):
                raise NotImplementedError

            def create(self, user_id, payload):
                raise NotImplementedError

            def delete(self, user_id, item_id):
                return True

        with self._client(FakeStore()) as client:
            response = client.delete("/api/history/s1", headers=self._auth())
            self.assertEqual(response.status_code, 204)

    def test_delete_foreign_row_returns_404(self) -> None:
        class FakeStore:
            def list(self, user_id):
                raise NotImplementedError

            def create(self, user_id, payload):
                raise NotImplementedError

            def delete(self, user_id, item_id):
                return False

        with self._client(FakeStore()) as client:
            response = client.delete("/api/history/s1", headers=self._auth())
            self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()