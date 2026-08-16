"""Shared SQLite storage foundation (T0-01).

Opens one database file with WAL mode + foreign keys, runs an idempotent
schema-migration runner, and hands out safe per-call connections. Nothing in
the application reads or writes this database yet — T0-02 (audit) and T0-03
(sessions) swap their adapters onto it later. Stdlib sqlite3 only: the
audit/session ports are synchronous (ports/audit.py, ports/session.py).
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

MIGRATIONS_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
)
"""

# Ordered list of (version, sql) schema migrations. T0-01 ships no business
# tables; T0-02 / T0-03 append their own migrations here.
MIGRATIONS: list[tuple[int, str]] = []


def open_db(path: str | Path) -> sqlite3.Connection:
    """Open (creating if needed) a WAL-mode SQLite connection with safety pragmas."""
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def apply_migrations(
    conn: sqlite3.Connection,
    migrations: list[tuple[int, str]] | None = None,
) -> int:
    """Apply every missing migration in version order, one transaction each.

    Idempotent: versions already recorded in ``schema_migrations`` are skipped,
    so a re-run applies nothing and returns 0.
    """
    migrations = MIGRATIONS if migrations is None else migrations
    conn.execute(MIGRATIONS_TABLE_DDL)
    applied = {row["version"] for row in conn.execute("SELECT version FROM schema_migrations").fetchall()}
    pending = [m for m in sorted(migrations, key=lambda item: item[0]) if m[0] not in applied]
    for version, sql in pending:
        # Explicit transaction: legacy sqlite3 only auto-begins on DML, so DDL
        # migrations would otherwise commit outside the transaction.
        conn.execute("BEGIN")
        try:
            conn.execute(sql)
            conn.execute(
                "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                (version, datetime.now(timezone.utc).isoformat()),
            )
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        else:
            conn.execute("COMMIT")
    return len(pending)


def initialize_db(
    path: str | Path,
    migrations: list[tuple[int, str]] | None = None,
) -> sqlite3.Connection:
    """Open the DB and apply pending migrations; returns the open connection."""
    conn = open_db(path)
    apply_migrations(conn, migrations)
    return conn


@contextmanager
def db_connect(
    path: str | Path,
    migrations: list[tuple[int, str]] | None = None,
) -> Iterator[sqlite3.Connection]:
    """Connection-per-call helper: yields a fresh, migrated connection and closes it."""
    conn = initialize_db(path, migrations)
    try:
        yield conn
    finally:
        conn.close()