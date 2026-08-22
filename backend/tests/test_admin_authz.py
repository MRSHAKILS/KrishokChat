"""Admin-console authorization tests (amendment 02).

All offline: PostgREST calls are faked with httpx MockTransport; tokens are
locally generated ES256 JWTs (same pattern as test_history/test_auth).
Verifies the fail-closed contract: no token → 401; non-admin (or missing
profile, or unconfigured storage) → 403/503 — never an implicit grant.
"""

from __future__ import annotations

import unittest
from contextlib import contextmanager

import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.application.admin import (
    AdminService,
    AdminUnavailableError,
    NotAdminError,
)
from app.infrastructure.storage.postgrest_admin import PostgrestAdminStore
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


def _user_token(user_id: str = "user-1", email: str = "u@example.com"):
    jwk, pem = _make_keypair()
    token = jwt.encode(
        {"sub": user_id, "email": email, "aud": "authenticated"},
        pem,
        algorithm="ES256",
        headers={"kid": jwk["kid"]},
    )
    return token, jwk


class FakeAdminStore:
    """In-memory store standing in for PostgrestAdminStore in route tests."""

    def __init__(self, profiles: dict[str, dict] | None = None) -> None:
        self.profiles: dict[str, dict] = {
            "admin-1": {"id": "admin-1", "email": "admin@example.com", "role": "admin", "plan": "free"},
            "user-1": {"id": "user-1", "email": "u@example.com", "role": "user", "plan": "free"},
            **(profiles or {}),
        }
        self.actions: list[dict] = []

    def get_profile(self, user_id):
        return self.profiles.get(user_id)

    def upsert_profile_defaults(self, user_id, email):
        if user_id not in self.profiles:
            self.profiles[user_id] = {
                "id": user_id,
                "email": email,
                "role": "user",
                "plan": "free",
            }
        return None

    def list_profiles(self, page, page_size, search=""):
        rows = sorted(self.profiles.values(), key=lambda p: p["id"])
        if search:
            rows = [p for p in rows if search.lower() in p["email"].lower()]
        total = len(rows)
        start = (page - 1) * page_size
        return rows[start : start + page_size], total

    def patch_profile(self, user_id, changes):
        row = self.profiles.get(user_id)
        if row is None:
            return None
        row.update(changes)
        return dict(row)

    def record_action(self, actor_id, action, target_type, target_id, payload):
        self.actions.append(
            {
                "actor_id": actor_id,
                "action": action,
                "target_type": target_type,
                "target_id": target_id,
                "payload": payload,
            }
        )
        return None

    def list_actions(self, limit):
        return self.actions[:limit]


class PostgrestAdminStoreUnitTests(unittest.TestCase):
    def _store(self, handler) -> PostgrestAdminStore:
        store = PostgrestAdminStore("https://x.supabase.co", "svc-key")

        def client():
            return httpx.Client(
                base_url=store._base,
                headers=store._headers,
                timeout=store._timeout,
                transport=httpx.MockTransport(handler),
            )

        store._client = client  # type: ignore[method-assign]
        return store

    def test_get_profile_builds_query(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.url.path, "/rest/v1/profiles")
            self.assertIn("id=eq.user-1", request.url.query.decode())
            return httpx.Response(200, json=[{"id": "user-1", "role": "admin"}])

        profile = self._store(handler).get_profile("user-1")
        self.assertEqual(profile["role"], "admin")

    def test_get_profile_missing_returns_none(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=[])

        self.assertIsNone(self._store(handler).get_profile("ghost"))

    def test_list_profiles_uses_range_and_exact_count(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.headers["prefer"], "count=exact")
            self.assertEqual(request.headers["range"], "0-19")
            return httpx.Response(
                206,
                json=[{"id": "user-1"}],
                headers={"content-range": "0-0/57"},
            )

        rows, total = self._store(handler).list_profiles(page=1, page_size=20)
        self.assertEqual(rows[0]["id"], "user-1")
        self.assertEqual(total, 57)

    def test_patch_profile_returns_representation(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.method, "PATCH")
            self.assertIn("id=eq.user-2", request.url.query.decode())
            self.assertIn('"plan":"premium"', request.read().decode())
            return httpx.Response(200, json=[{"id": "user-2", "plan": "premium"}])

        row = self._store(handler).patch_profile("user-2", {"plan": "premium"})
        self.assertEqual(row["plan"], "premium")

    def test_record_action_posts_audit_row(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertEqual(request.url.path, "/rest/v1/admin_actions")
            body = request.read().decode()
            self.assertIn('"actor_id":"admin-1"', body)
            self.assertIn('"action":"update_user"', body)
            return httpx.Response(201, json=[])

        self._store(handler).record_action(
            "admin-1", "update_user", "profile", "user-2", {"plan": "premium"}
        )


class AdminServiceTests(unittest.TestCase):
    def test_unconfigured_fails_closed(self) -> None:
        service = AdminService(store=None)
        with self.assertRaises(AdminUnavailableError):
            service.require_admin("admin-1")
        with self.assertRaises(AdminUnavailableError):
            service.list_users(1, 20)
        with self.assertRaises(AdminUnavailableError):
            service.update_user("admin-1", "user-2", plan="premium")

    def test_require_admin_denies_non_admin(self) -> None:
        service = AdminService(store=FakeAdminStore())
        with self.assertRaises(NotAdminError):
            service.require_admin("user-1")

    def test_require_admin_denies_missing_profile(self) -> None:
        service = AdminService(store=FakeAdminStore())
        with self.assertRaises(NotAdminError):
            service.require_admin("ghost")

    def test_require_admin_allows_admin(self) -> None:
        service = AdminService(store=FakeAdminStore())
        profile = service.require_admin("admin-1")
        self.assertEqual(profile["role"], "admin")

    def test_update_user_validates_and_audits(self) -> None:
        store = FakeAdminStore()
        service = AdminService(store=store)
        row = service.update_user("admin-1", "user-1", plan="premium")
        self.assertEqual(row["plan"], "premium")
        self.assertEqual(len(store.actions), 1)
        self.assertEqual(store.actions[0]["payload"], {"plan": "premium"})

    def test_update_user_rejects_invalid_values(self) -> None:
        service = AdminService(store=FakeAdminStore())
        with self.assertRaises(ValueError):
            service.update_user("admin-1", "user-1", role="superadmin")
        with self.assertRaises(ValueError):
            service.update_user("admin-1", "user-1", plan="enterprise")
        with self.assertRaises(ValueError):
            service.update_user("admin-1", "user-1")

    def test_get_profile_lazily_creates_missing_row(self) -> None:
        store = FakeAdminStore()
        service = AdminService(store=store)
        profile = service.get_profile("new-user", email="new@example.com")
        self.assertEqual(profile["plan"], "free")
        self.assertEqual(profile["email"], "new@example.com")


class AdminEndpointTests(unittest.TestCase):
    """Route contract: 401 anonymous, 403 non-admin, 503 unconfigured, 200 admin."""

    def setUp(self) -> None:
        # One keypair signs every token; the verifier only trusts this jwk.
        self.jwk, self.pem = _make_keypair()
        self.admin_token = self._token("admin-1", "admin@example.com")
        self.user_token = self._token("user-1", "u@example.com")

    def _token(self, user_id: str, email: str) -> str:
        return jwt.encode(
            {"sub": user_id, "email": email, "aud": "authenticated"},
            self.pem,
            algorithm="ES256",
            headers={"kid": self.jwk["kid"]},
        )

    @contextmanager
    def _client(self, store=None):
        from dataclasses import replace

        from app.application.auth import AuthService
        from app.infrastructure.auth.jwks import SupabaseJWKSVerifier

        verifier = SupabaseJWKSVerifier("http://unused.invalid/jwks")
        verifier._fetch_jwks = lambda: {"keys": [self.jwk]}  # type: ignore[method-assign]

        app = create_app()
        with TestClient(app) as client:
            container = client.app.state.container
            client.app.state.container = replace(
                container,
                auth=AuthService(verifier=verifier),
                admin=AdminService(store=store),
            )
            yield client

    def test_without_token_returns_401(self) -> None:
        with self._client() as client:
            for method, url in [
                ("GET", "/api/admin/users"),
                ("PATCH", "/api/admin/users/user-1"),
                ("GET", "/api/admin/actions"),
                ("GET", "/api/account"),
            ]:
                response = getattr(client, method.lower())(url)
                self.assertEqual(response.status_code, 401, f"{method} {url}")

    def test_unconfigured_returns_503_fail_closed(self) -> None:
        with self._client() as client:
            for url in ["/api/admin/users", "/api/admin/actions"]:
                response = client.get(url, headers={"Authorization": f"Bearer {self.admin_token}"})
                self.assertEqual(response.status_code, 503, url)

    def test_non_admin_gets_403_even_with_valid_token(self) -> None:
        store = FakeAdminStore()
        with self._client(store) as client:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            self.assertEqual(client.get("/api/admin/users", headers=headers).status_code, 403)
            self.assertEqual(
                client.patch(
                    "/api/admin/users/admin-1",
                    headers=headers,
                    json={"plan": "premium"},
                ).status_code,
                403,
            )

    def test_admin_list_users_flow(self) -> None:
        store = FakeAdminStore()
        with self._client(store) as client:
            response = client.get(
                "/api/admin/users",
                headers={"Authorization": f"Bearer {self.admin_token}"},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["total"], 2)
            self.assertEqual(body["page"], 1)

    def test_admin_patch_user_flow_audits(self) -> None:
        store = FakeAdminStore()
        with self._client(store) as client:
            response = client.patch(
                "/api/admin/users/user-1",
                headers={"Authorization": f"Bearer {self.admin_token}"},
                json={"plan": "premium", "role": "user"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["plan"], "premium")
            self.assertEqual(len(store.actions), 1)
            # audit trail endpoint reflects it
            actions = client.get(
                "/api/admin/actions",
                headers={"Authorization": f"Bearer {self.admin_token}"},
            )
            self.assertEqual(actions.status_code, 200)
            self.assertEqual(actions.json()["items"][0]["action"], "update_user")

    def test_admin_patch_invalid_body_returns_400(self) -> None:
        store = FakeAdminStore()
        with self._client(store) as client:
            response = client.patch(
                "/api/admin/users/user-1",
                headers={"Authorization": f"Bearer {self.admin_token}"},
                json={"plan": "enterprise"},  # Literal validation rejects it
            )
            self.assertEqual(response.status_code, 422)
            response = client.patch(
                "/api/admin/users/user-1",
                headers={"Authorization": f"Bearer {self.admin_token}"},
                json={},  # nothing to update
            )
            self.assertEqual(response.status_code, 400)

    def test_account_returns_plan_and_role(self) -> None:
        store = FakeAdminStore()
        with self._client(store) as client:
            response = client.get(
                "/api/account",
                headers={"Authorization": f"Bearer {self.user_token}"},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["plan"], "free")
            self.assertEqual(body["role"], "user")
            self.assertTrue(body["profile_available"])

    def test_account_lazily_creates_profile(self) -> None:
        token = self._token("brand-new-user", "new@example.com")
        store = FakeAdminStore()
        with self._client(store) as client:
            response = client.get("/api/account", headers={"Authorization": f"Bearer {token}"})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()["profile_available"])

    def test_auth_me_includes_profile_when_configured(self) -> None:
        store = FakeAdminStore()
        with self._client(store) as client:
            response = client.get(
                "/auth/me",
                headers={"Authorization": f"Bearer {self.admin_token}"},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["user"]["email"], "admin@example.com")
            self.assertEqual(body["profile"]["role"], "admin")

    def test_v1_mirror_requires_admin_too(self) -> None:
        store = FakeAdminStore()
        with self._client(store) as client:
            response = client.get("/api/v1/admin/users")  # anonymous
            self.assertEqual(response.status_code, 401)
            response = client.get(
                "/api/v1/admin/users",
                headers={"Authorization": f"Bearer {self.user_token}"},
            )
            self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
