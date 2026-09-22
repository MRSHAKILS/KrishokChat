"""T0-03: SQLite session store tests.

Covers: append/get round-trip; history preservation and order; max-messages
trimming parity with the in-memory adapter; TTL expiry on read (including a
direct parity check against the memory adapter's eviction); TTL refresh on
append only (never on get); restart persistence (fresh adapter instance /
fresh TestClient over the same DB file); lazy purge of expired rows on
append and on adapter init; migration v3 registration via the adapter's own
MIGRATIONS list (shared list stays empty); and container backend selection
with memory as the default.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from app.application.container import build_container
from app.core.config import Settings
from app.infrastructure.sessions.memory import InMemorySessionStore
from app.infrastructure.sessions.sqlite import SqliteSessionStore
from app.infrastructure.storage.sqlite import MIGRATIONS, db_connect
from app.main import create_app


def _old_iso(seconds: int) -> str:
    """UTC ISO-8601 string ``seconds`` in the past (same format the adapter writes)."""
    return (datetime.now(timezone.utc) - timedelta(seconds=seconds)).isoformat()


def _last_active(store: SqliteSessionStore, session_id: str) -> str:
    with db_connect(store.db_path, migrations=store.MIGRATIONS) as conn:
        row = conn.execute(
            "SELECT last_active_at FROM sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
    return row["last_active_at"] if row else None


class SqliteSessionStoreTests(unittest.TestCase):
    def test_append_then_get_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteSessionStore(db_path=Path(tmp) / "krishokchat.db")
            store.append("s1", "user", "ধান রোগ কীভাবে কমাব?")
            store.append("s1", "assistant", "পরিষ্কার পানি ব্যবহার করুন।")

            self.assertEqual(
                store.get("s1"),
                [
                    {"role": "user", "content": "ধান রোগ কীভাবে কমাব?"},
                    {"role": "assistant", "content": "পরিষ্কার পানি ব্যবহার করুন।"},
                ],
            )

    def test_get_unknown_session_returns_empty_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteSessionStore(db_path=Path(tmp) / "krishokchat.db")
            self.assertEqual(store.get("missing"), [])

    def test_append_preserves_history_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteSessionStore(db_path=Path(tmp) / "krishokchat.db")
            for i in range(5):
                store.append("s1", "user", f"q{i}")
                store.append("s1", "assistant", f"a{i}")
            roles = [m["role"] for m in store.get("s1")]
            self.assertEqual(
                roles,
                ["user", "assistant", "user", "assistant", "user", "assistant", "user", "assistant", "user", "assistant"],
            )
            self.assertEqual(store.get("s1")[0], {"role": "user", "content": "q0"})
            self.assertEqual(store.get("s1")[-1], {"role": "assistant", "content": "a4"})

    def test_max_messages_truncation_matches_memory_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sqlite_store = SqliteSessionStore(
                db_path=Path(tmp) / "krishokchat.db", max_turns=1  # max_messages = 2
            )
            memory_store = InMemorySessionStore(max_turns=1)
            for i in range(5):
                for store in (sqlite_store, memory_store):
                    store.append("s1", "user", f"q{i}")
                    store.append("s1", "assistant", f"a{i}")

            self.assertEqual(sqlite_store.get("s1"), memory_store.get("s1"))
            self.assertEqual(
                sqlite_store.get("s1"),
                [
                    {"role": "user", "content": "q4"},
                    {"role": "assistant", "content": "a4"},
                ],
            )

    def test_ttl_expiry_on_read_returns_miss_like_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteSessionStore(
                db_path=Path(tmp) / "krishokchat.db", ttl_seconds=1800
            )
            store.append("s1", "user", "ধান রোগ")
            # Age the row far beyond the TTL, then read.
            with db_connect(store.db_path, migrations=store.MIGRATIONS) as conn:
                conn.execute(
                    "UPDATE sessions SET last_active_at = ? WHERE session_id = ?",
                    ("2020-01-01T00:00:00+00:00", "s1"),
                )
                conn.commit()

            self.assertEqual(store.get("s1"), [])
            # The expired row is physically purged by the read-side TTL check.
            with db_connect(store.db_path, migrations=store.MIGRATIONS) as conn:
                count = conn.execute(
                    "SELECT COUNT(*) AS n FROM sessions WHERE session_id = ?", ("s1",)
                ).fetchone()["n"]
            self.assertEqual(count, 0)

            # Memory adapter parity: same input -> same miss. The memory store
            # uses private internals (time.time() floats); ageing it the same
            # way must evict identically.
            memory_store = InMemorySessionStore(ttl_seconds=1800)
            memory_store.append("s1", "user", "ধান রোগ")
            memory_store._timestamps["s1"] = 0.0  # far beyond the TTL
            self.assertEqual(memory_store.get("s1"), [])

    def test_get_does_not_refresh_ttl_but_append_does(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteSessionStore(
                db_path=Path(tmp) / "krishokchat.db", ttl_seconds=1800
            )
            store.append("s1", "user", "q1")
            aged = _old_iso(900)  # old but not expired
            with db_connect(store.db_path, migrations=store.MIGRATIONS) as conn:
                conn.execute(
                    "UPDATE sessions SET last_active_at = ? WHERE session_id = ?",
                    (aged, "s1"),
                )
                conn.commit()

            store.get("s1")
            self.assertEqual(_last_active(store, "s1"), aged)  # get never touches TTL

            store.append("s1", "assistant", "a1")
            refreshed = datetime.fromisoformat(_last_active(store, "s1"))
            self.assertGreater(refreshed, datetime.fromisoformat(aged))  # append refreshes

    def test_restart_persistence_across_connections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            first = SqliteSessionStore(db_path=db_path)
            first.append("s1", "user", "ধান রোগ")
            first.append("s1", "assistant", "পরিষ্কার পানি ব্যবহার করুন।")
            # The first instance is gone; a fresh adapter opens the same file.
            second = SqliteSessionStore(db_path=db_path)
            self.assertEqual(
                second.get("s1"),
                [
                    {"role": "user", "content": "ধান রোগ"},
                    {"role": "assistant", "content": "পরিষ্কার পানি ব্যবহার করুন।"},
                ],
            )
            # And it keeps appending to the same history.
            second.append("s1", "user", "আরেকটি প্রশ্ন")
            self.assertEqual(len(second.get("s1")), 3)

    def test_lazy_purge_on_append_removes_only_expired_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteSessionStore(
                db_path=Path(tmp) / "krishokchat.db", ttl_seconds=1800
            )
            store.append("fresh", "user", "নতুন প্রশ্ন")
            store.append("stale", "user", "পুরনো প্রশ্ন")
            with db_connect(store.db_path, migrations=store.MIGRATIONS) as conn:
                conn.execute(
                    "UPDATE sessions SET last_active_at = ? WHERE session_id = ?",
                    ("2020-01-01T00:00:00+00:00", "stale"),
                )
                conn.commit()

            store.append("fresh", "assistant", "উত্তর")  # write triggers the purge

            self.assertEqual(len(store.get("stale")), 0)
            self.assertEqual(
                store.get("fresh"),
                [
                    {"role": "user", "content": "নতুন প্রশ্ন"},
                    {"role": "assistant", "content": "উত্তর"},
                ],
            )

    def test_lazy_purge_on_adapter_init_removes_expired_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            first = SqliteSessionStore(db_path=db_path, ttl_seconds=1800)
            first.append("stale", "user", "পুরনো প্রশ্ন")
            with db_connect(db_path, migrations=first.MIGRATIONS) as conn:
                conn.execute(
                    "UPDATE sessions SET last_active_at = ? WHERE session_id = ?",
                    ("2020-01-01T00:00:00+00:00", "stale"),
                )
                conn.commit()

            # The "restart" adapter purges expired rows at construction.
            second = SqliteSessionStore(db_path=db_path, ttl_seconds=1800)
            self.assertEqual(second.get("stale"), [])

    def test_migration_v3_and_index_registered_via_adapter_migrations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            SqliteSessionStore(db_path=db_path)
            with db_connect(db_path, migrations=SqliteSessionStore.MIGRATIONS) as conn:
                versions = [
                    r["version"]
                    for r in conn.execute("SELECT version FROM schema_migrations ORDER BY version")
                ]
                tables = [
                    r["name"]
                    for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                ]
                indexes = [
                    r["name"]
                    for r in conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
                ]
                columns = {
                    c["name"] for c in conn.execute("PRAGMA table_info(sessions)")
                }
            self.assertEqual(versions, [3])
            self.assertIn("sessions", tables)
            self.assertIn("idx_sessions_last_active_at", indexes)
            self.assertEqual(
                columns,
                {"session_id", "data_json", "created_at", "last_active_at"},
            )
            # The shared T0-01 migration list stays empty (its own test asserts this).
            self.assertEqual(MIGRATIONS, [])

    def test_data_json_column_holds_the_message_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SqliteSessionStore(db_path=Path(tmp) / "krishokchat.db")
            store.append("s1", "user", "ধান")
            with db_connect(store.db_path, migrations=store.MIGRATIONS) as conn:
                row = conn.execute(
                    "SELECT data_json, created_at, last_active_at FROM sessions WHERE session_id = ?",
                    ("s1",),
                ).fetchone()
            self.assertEqual(json.loads(row["data_json"]), [{"role": "user", "content": "ধান"}])
            self.assertEqual(row["created_at"], row["last_active_at"])
            self.assertIn("+00:00", row["created_at"])  # UTC ISO-8601


class SqliteSessionContainerTests(unittest.TestCase):
    def test_container_selects_sqlite_backend_when_configured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(
                session_backend="sqlite",
                sqlite_db_path=str(Path(tmp) / "krishokchat.db"),
                audit_log_path=str(Path(tmp) / "audit.jsonl"),
            )
            container = build_container(settings)
            self.assertIsInstance(container.qa.sessions, SqliteSessionStore)

            # The wiring really writes to the shared DB (not the memory adapter).
            container.qa.sessions.append("s1", "user", "ধান রোগ")
            self.assertEqual(container.qa.sessions.get("s1")[0]["role"], "user")

    def test_container_defaults_to_memory_backend(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(audit_log_path=str(Path(tmp) / "audit.jsonl"))
            self.assertEqual(settings.session_backend, "memory")
            container = build_container(settings)
            self.assertIsInstance(container.qa.sessions, InMemorySessionStore)


class SqliteSessionRestartViaHttpTests(unittest.TestCase):
    def test_chat_session_survives_backend_restart(self) -> None:
        """Gate 3: a chat request under SESSION_BACKEND=sqlite creates a
        session that a fresh app (new container over the same DB file) still
        reads, with history intact and continued."""
        demo_cache_path = (
            Path(__file__).resolve().parent.parent.parent.parent / "demo-assets" / "cached_responses.json"
        )
        if not demo_cache_path.exists():
            self.skipTest("demo cache file missing")
        query = None
        cache_data = json.loads(demo_cache_path.read_text(encoding="utf-8"))
        for key, entry in cache_data.items():
            parts = key.split("|")
            # Plain chat lane: no crop/disease/model parts. Corpus-aware keys
            # are "|||<corpus>|<query>"; legacy keys are "|||<query>".
            if (
                len(parts) in (4, 5)
                and all(part == "" for part in parts[:3])
                and isinstance(entry, dict)
                and entry.get("category") == "safe_agri"
            ):
                candidate = parts[-1]
                if "Carbendazim" not in candidate and "carbendazim" not in candidate:
                    query = candidate
                    break
        if not query:
            self.skipTest("no plain chat-lane query in the demo cache")

        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(
                session_backend="sqlite",
                sqlite_db_path=str(Path(tmp) / "krishokchat.db"),
                audit_log_path=str(Path(tmp) / "audit.jsonl"),
            )
            session_id = "gate3-session"

            with TestClient(create_app(config=settings)) as client:
                response = client.post(
                    "/api/qa", json={"query": query, "session_id": session_id}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["category"], "safe_agri")

            # "Server stopped." A new app instance = new container over the same DB.
            with TestClient(create_app(config=settings)) as client:
                container = client.app.state.container
                history = container.qa.sessions.get(session_id)
                self.assertEqual(
                    [m["role"] for m in history], ["user", "assistant"]
                )
                self.assertEqual(history[0]["content"], query)

                # The conversation continues across the restart.
                client.post("/api/qa", json={"query": query, "session_id": session_id})
                continued = container.qa.sessions.get(session_id)
                self.assertEqual(
                    [m["role"] for m in continued],
                    ["user", "assistant", "user", "assistant"],
                )


if __name__ == "__main__":
    unittest.main()