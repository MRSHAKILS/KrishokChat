"""T0-01: SQLite storage foundation tests.

Covers: migration applies once, re-run applies nothing, idempotency across
re-opens, WAL mode on, foreign_keys/busy_timeout pragmas, failed-migration
rollback, config path override + default resolution, and the backend/data/
gitignore entry.
"""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from app.core.config import Settings
from app.infrastructure.storage.sqlite import (
    MIGRATIONS,
    apply_migrations,
    db_connect,
    initialize_db,
    open_db,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

MIGRATION_1 = (1, "CREATE TABLE demo_items (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
MIGRATION_2 = (2, "CREATE TABLE demo_notes (id INTEGER PRIMARY KEY, body TEXT NOT NULL)")
MIGRATION_3 = (3, "CREATE TABLE demo_tags (id INTEGER PRIMARY KEY, tag TEXT NOT NULL)")


class SqliteBootstrapTests(unittest.TestCase):
    def test_migration_applies_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "nested" / "krishokchat.db"
            with db_connect(db_path, migrations=[MIGRATION_1]) as conn:
                versions = [
                    row["version"]
                    for row in conn.execute("SELECT version FROM schema_migrations ORDER BY version")
                ]
                tables = [
                    row["name"]
                    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                ]
            self.assertEqual(versions, [1])
            self.assertIn("demo_items", tables)

    def test_rerun_applies_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            conn = open_db(db_path)
            try:
                first = apply_migrations(conn, migrations=[MIGRATION_1])
                second = apply_migrations(conn, migrations=[MIGRATION_1])
                count = conn.execute("SELECT COUNT(*) AS n FROM schema_migrations").fetchone()["n"]
            finally:
                conn.close()
            self.assertEqual(first, 1)
            self.assertEqual(second, 0)
            self.assertEqual(count, 1)

    def test_migrations_idempotent_across_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            with db_connect(db_path, migrations=[MIGRATION_1, MIGRATION_2, MIGRATION_3]):
                pass
            with db_connect(db_path, migrations=[MIGRATION_1, MIGRATION_2, MIGRATION_3]) as conn:
                count = conn.execute("SELECT COUNT(*) AS n FROM schema_migrations").fetchone()["n"]
                tables = [
                    row["name"]
                    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                ]
            self.assertEqual(count, 3)
            for table in ("demo_items", "demo_notes", "demo_tags"):
                self.assertIn(table, tables)

    def test_wal_mode_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conn = open_db(Path(tmp) / "krishokchat.db")
            try:
                journal_mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
            finally:
                conn.close()
            self.assertEqual(journal_mode.lower(), "wal")

    def test_foreign_keys_and_busy_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            conn = open_db(Path(tmp) / "krishokchat.db")
            try:
                fk = conn.execute("PRAGMA foreign_keys").fetchone()[0]
                busy = conn.execute("PRAGMA busy_timeout").fetchone()[0]
            finally:
                conn.close()
            self.assertEqual(fk, 1)
            self.assertEqual(busy, 5000)

    def test_failed_migration_rolls_back_version_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            conn = initialize_db(db_path)
            try:
                with self.assertRaises(sqlite3.OperationalError):
                    apply_migrations(
                        conn,
                        migrations=[
                            (1, "CREATE TABLE demo_items (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"),
                            (2, "THIS IS NOT VALID SQL"),
                        ],
                    )
                versions = [
                    row["version"]
                    for row in conn.execute("SELECT version FROM schema_migrations ORDER BY version")
                ]
            finally:
                conn.close()
            self.assertEqual(versions, [1])

    def test_custom_path_honored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "custom" / "my.db"
            settings = Settings(sqlite_db_path=str(db_path))
            self.assertEqual(settings.resolved_sqlite_db_path, db_path)
            with db_connect(settings.resolved_sqlite_db_path):
                pass
            self.assertTrue(db_path.exists())

    def test_default_path_resolution(self) -> None:
        expected = REPO_ROOT / "backend" / "data" / "krishokchat.db"
        self.assertEqual(Settings().resolved_sqlite_db_path, expected)

    def test_gitignore_contains_backend_data(self) -> None:
        gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("backend/data/", gitignore)

    def test_no_business_migrations_shipped(self) -> None:
        self.assertEqual(MIGRATIONS, [])


if __name__ == "__main__":
    unittest.main()