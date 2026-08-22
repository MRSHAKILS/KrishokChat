"""Notification lane tests (amendment 02).

All offline: PostgREST is faked (MockTransport or in-memory stores); tokens
are locally generated ES256 JWTs. Verifies audience scoping (anonymous →
`all`, free → `all|free`, premium → all), read state, honest-empty degradation
when unconfigured, and admin-route authorization (401/403/503 fail-closed).
"""

from __future__ import annotations

import unittest
from contextlib import contextmanager

import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.application.admin import AdminService
from app.application.notifications import (
    NotificationService,
    NotificationsUnavailableError,
)
from app.infrastructure.storage.postgrest_notifications import PostgrestNotificationStore
from app.main import create_app


def _make_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()
    import base64

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


class FakeNotificationStore:
    """In-memory announcements + reads standing in for PostgREST."""

    def __init__(self, rows=None):
        self.rows: dict[str, dict] = {r["id"]: dict(r) for r in (rows or [])}
        self.reads: set[tuple[str, str]] = set()
        self._seq = 0

    def list_live(self, audiences, limit):
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        live = [
            r
            for r in self.rows.values()
            if r.get("published")
            and r.get("audience", "all") in audiences
            and (not r.get("expires_at") or r["expires_at"] > now.isoformat())
        ]
        live.sort(key=lambda r: r.get("published_at") or "", reverse=True)
        return [dict(r) for r in live[:limit]]

    def list_read_ids(self, user_id):
        return {aid for (uid, aid) in self.reads if uid == user_id}

    def mark_read(self, user_id, announcement_id):
        self.reads.add((user_id, announcement_id))

    def create(self, payload):
        self._seq += 1
        row = {"id": f"ann-{self._seq}", "published": False, "published_at": None, **payload}
        self.rows[row["id"]] = row
        return dict(row)

    def get(self, announcement_id):
        row = self.rows.get(announcement_id)
        return dict(row) if row else None

    def list_all(self, limit, offset=0):
        rows = sorted(self.rows.values(), key=lambda r: r["id"], reverse=True)
        return [dict(r) for r in rows[offset : offset + limit]]

    def patch(self, announcement_id, changes):
        row = self.rows.get(announcement_id)
        if row is None:
            return None
        row.update(changes)
        return dict(row)

    def delete(self, announcement_id):
        return self.rows.pop(announcement_id, None) is not None


class FakeAdminStore:
    def __init__(self, profiles=None):
        self.profiles = {
            "admin-1": {"id": "admin-1", "email": "admin@example.com", "role": "admin", "plan": "free"},
            "free-1": {"id": "free-1", "email": "free@example.com", "role": "user", "plan": "free"},
            "prem-1": {"id": "prem-1", "email": "prem@example.com", "role": "user", "plan": "premium"},
            **(profiles or {}),
        }
        self.actions = []

    def get_profile(self, user_id):
        return self.profiles.get(user_id)

    def upsert_profile_defaults(self, user_id, email):
        self.profiles.setdefault(user_id, {"id": user_id, "email": email, "role": "user", "plan": "free"})

    def list_profiles(self, page, page_size, search=""):
        return list(self.profiles.values()), len(self.profiles)

    def patch_profile(self, user_id, changes):
        row = self.profiles.get(user_id)
        if row:
            row.update(changes)
        return dict(row) if row else None

    def record_action(self, actor_id, action, target_type, target_id, payload):
        self.actions.append({"actor_id": actor_id, "action": action})

    def list_actions(self, limit):
        return self.actions[:limit]


def _seed_rows():
    return [
        {"id": "a-all", "kind": "announcement", "severity": "info", "title_bn": "সবার", "body_bn": "...", "audience": "all", "published": True, "published_at": "2026-08-22T10:00:00+00:00"},
        {"id": "a-free", "kind": "announcement", "severity": "info", "title_bn": "ফ্রি", "body_bn": "...", "audience": "free", "published": True, "published_at": "2026-08-22T09:00:00+00:00"},
        {"id": "a-prem", "kind": "disease_alert", "severity": "urgent", "title_bn": "প্রিমিয়াম", "body_bn": "...", "audience": "premium", "published": True, "published_at": "2026-08-22T08:00:00+00:00"},
        {"id": "a-draft", "kind": "announcement", "severity": "info", "title_bn": "খসড়া", "body_bn": "...", "audience": "all", "published": False},
        {"id": "a-expired", "kind": "announcement", "severity": "info", "title_bn": "পুরনো", "body_bn": "...", "audience": "all", "published": True, "published_at": "2026-08-01T10:00:00+00:00", "expires_at": "2026-08-10T10:00:00+00:00"},
    ]


class NotificationServiceTests(unittest.TestCase):
    def test_unconfigured_list_raises(self) -> None:
        service = NotificationService(store=None)
        with self.assertRaises(NotificationsUnavailableError):
            service.list_for("anonymous", None)

    def test_audience_scoping(self) -> None:
        store = FakeNotificationStore(_seed_rows())
        service = NotificationService(store=store)
        anon = service.list_for("anonymous", None)
        self.assertEqual([i["id"] for i in anon["items"]], ["a-all"])
        free = service.list_for("free", "free-1")
        self.assertEqual([i["id"] for i in free["items"]], ["a-all", "a-free"])
        premium = service.list_for("premium", "prem-1")
        self.assertEqual([i["id"] for i in premium["items"]], ["a-all", "a-free", "a-prem"])

    def test_read_state_marks_items(self) -> None:
        store = FakeNotificationStore(_seed_rows())
        service = NotificationService(store=store)
        service.mark_read("free-1", "a-all")
        result = service.list_for("free", "free-1")
        by_id = {i["id"]: i["read"] for i in result["items"]}
        self.assertTrue(by_id["a-all"])
        self.assertFalse(by_id["a-free"])

    def test_create_validates_fields(self) -> None:
        service = NotificationService(store=FakeNotificationStore())
        with self.assertRaises(ValueError):
            service.create({"kind": "gossip", "title_bn": "x", "body_bn": "y"})
        with self.assertRaises(ValueError):
            service.create({"kind": "announcement", "title_bn": "", "body_bn": "y"})


class PostgrestNotificationStoreUnitTests(unittest.TestCase):
    def _store(self, handler) -> PostgrestNotificationStore:
        store = PostgrestNotificationStore("https://x.supabase.co", "svc-key")

        def client():
            return httpx.Client(
                base_url=store._base,
                headers=store._headers,
                timeout=store._timeout,
                transport=httpx.MockTransport(handler),
            )

        store._client = client  # type: ignore[method-assign]
        return store

    def test_list_live_builds_audience_or_and_expiry_filters(self) -> None:
        captured = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured["query"] = request.url.query.decode()
            return httpx.Response(200, json=[{"id": "a-all"}])

        rows = self._store(handler).list_live(["all", "free"], 20)
        self.assertEqual(rows[0]["id"], "a-all")
        from urllib.parse import unquote

        query = unquote(captured["query"])
        self.assertIn("audience=in.(all,free)", query)
        self.assertIn("published=eq.true", query)
        self.assertIn("expires_at.is.null", query)
        self.assertIn("expires_at.gt.", query)

    def test_mark_read_upserts(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            from urllib.parse import unquote

            self.assertEqual(request.url.path, "/rest/v1/announcement_reads")
            self.assertIn("on_conflict=user_id,announcement_id", unquote(request.url.query.decode()))
            self.assertIn('"user_id":"u1"', request.read().decode())
            return httpx.Response(201, json=[])

        self._store(handler).mark_read("u1", "ann-1")

    def test_publish_patch_sets_published_at(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            body = request.read().decode()
            self.assertIn('"published":true', body)
            self.assertIn("published_at", body)
            return httpx.Response(200, json=[{"id": "ann-1", "published": True}])

        row = self._store(handler).patch("ann-1", {"published": True, "published_at": "2026-08-22T00:00:00+00:00"})
        self.assertTrue(row["published"])


class NotificationEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.jwk, self.pem = _make_keypair()
        self.admin_token = self._token("admin-1", "admin@example.com")
        self.free_token = self._token("free-1", "free@example.com")

    def _token(self, user_id: str, email: str) -> str:
        return jwt.encode(
            {"sub": user_id, "email": email, "aud": "authenticated"},
            self.pem,
            algorithm="ES256",
            headers={"kid": self.jwk["kid"]},
        )

    @contextmanager
    def _client(self, notification_store=None, admin_store=None):
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
                admin=AdminService(store=admin_store),
                notifications=NotificationService(store=notification_store),
            )
            yield client

    def test_public_list_anonymous_sees_only_all_audience(self) -> None:
        store = FakeNotificationStore(_seed_rows())
        with self._client(notification_store=store, admin_store=FakeAdminStore()) as client:
            response = client.get("/api/notifications")
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertTrue(body["enabled"])
            self.assertEqual([i["id"] for i in body["items"]], ["a-all"])

    def test_public_list_unconfigured_returns_honest_empty(self) -> None:
        with self._client() as client:
            response = client.get("/api/notifications")
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["items"], [])
            self.assertFalse(body["enabled"])

    def test_free_user_sees_free_audience(self) -> None:
        store = FakeNotificationStore(_seed_rows())
        with self._client(notification_store=store, admin_store=FakeAdminStore()) as client:
            response = client.get(
                "/api/notifications",
                headers={"Authorization": f"Bearer {self.free_token}"},
            )
            ids = [i["id"] for i in response.json()["items"]]
            self.assertIn("a-free", ids)
            self.assertNotIn("a-prem", ids)

    def test_mark_read_requires_auth(self) -> None:
        store = FakeNotificationStore(_seed_rows())
        with self._client(notification_store=store, admin_store=FakeAdminStore()) as client:
            self.assertEqual(client.post("/api/notifications/a-all/read").status_code, 401)
            ok = client.post(
                "/api/notifications/a-all/read",
                headers={"Authorization": f"Bearer {self.free_token}"},
            )
            self.assertEqual(ok.status_code, 204)
            # read flag now visible on next list
            listed = client.get(
                "/api/notifications",
                headers={"Authorization": f"Bearer {self.free_token}"},
            )
            by_id = {i["id"]: i["read"] for i in listed.json()["items"]}
            self.assertTrue(by_id["a-all"])

    def test_admin_routes_fail_closed(self) -> None:
        store = FakeNotificationStore(_seed_rows())
        with self._client(notification_store=store, admin_store=FakeAdminStore()) as client:
            # anonymous → 401
            self.assertEqual(client.get("/api/admin/announcements").status_code, 401)
            # non-admin token → 403
            self.assertEqual(
                client.get(
                    "/api/admin/announcements",
                    headers={"Authorization": f"Bearer {self.free_token}"},
                ).status_code,
                403,
            )

    def test_admin_create_and_publish_flow(self) -> None:
        store = FakeNotificationStore()
        admin_store = FakeAdminStore()
        with self._client(notification_store=store, admin_store=admin_store) as client:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            created = client.post(
                "/api/admin/announcements",
                headers=headers,
                json={
                    "kind": "disease_alert",
                    "severity": "urgent",
                    "title_bn": "ধানে ব্লাস্ট সতর্কতা",
                    "body_bn": "আপনার এলাকায় ব্লাস্ট রোগের প্রাদুর্ভাব দেখা দিয়েছে...",
                    "crop": "ধান",
                },
            )
            self.assertEqual(created.status_code, 201)
            ann_id = created.json()["id"]
            self.assertFalse(created.json()["published"])

            published = client.post(f"/api/admin/announcements/{ann_id}/publish", headers=headers)
            self.assertEqual(published.status_code, 200)
            self.assertTrue(published.json()["published"])

            # anonymous farmers now see the urgent alert
            public = client.get("/api/notifications")
            self.assertEqual(public.json()["items"][0]["id"], ann_id)

            # audit trail got the create action
            self.assertEqual(admin_store.actions[0]["action"], "create_announcement")

    def test_admin_delete_missing_returns_404(self) -> None:
        store = FakeNotificationStore()
        with self._client(notification_store=store, admin_store=FakeAdminStore()) as client:
            response = client.delete(
                "/api/admin/announcements/ghost",
                headers={"Authorization": f"Bearer {self.admin_token}"},
            )
            self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
