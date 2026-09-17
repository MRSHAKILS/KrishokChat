"""T0-03: SQLite-backed session store.

Same contract as the in-memory adapter (``infrastructure/sessions/memory.py``):
``get`` + ``append`` only (that is the whole SessionStore port). Semantics
match the memory adapter exactly:

- Per session, a list of ``{"role": str, "content": str}`` messages, capped at
  ``max_turns * 2`` messages (trimmed on append).
- TTL checked on every read AND write: a session whose ``last_active_at`` is
  older than ``ttl_seconds`` reads as a miss (empty list), exactly like the
  memory adapter's ``_evict``.
- TTL is refreshed on ``append`` only — ``get`` never touches the timestamp
  (same as memory).
- ``get`` returns a fresh list (memory returns a copy); a missing or expired
  session returns ``[]``.

Rows live in the shared T0-01 SQLite database (table ``sessions``, migration
v3 registered on this adapter's own ``MIGRATIONS`` list — the shared list in
``storage/sqlite.py`` is asserted empty by the T0-01 test and is out of scope
to extend).

Cleanup is lazy, exactly as the task handbook requires: expired rows are
purged (``DELETE ... WHERE last_active_at < now - ttl``, indexed) on adapter
init and on every ``get``/``append``. No background threads or processes.

The T0-01 migration runner executes exactly one statement per migration
version, so the ``last_active_at`` index cannot ride inside migration v3; it
is created idempotently (``CREATE INDEX IF NOT EXISTS``) on the first
connection per adapter instance — the same pattern T0-02's audit sink uses
for its indexes.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.infrastructure.storage.sqlite import db_connect

SESSIONS_DDL = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    data_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_active_at TEXT NOT NULL
)
"""

INDEXES_DDL = """
CREATE INDEX IF NOT EXISTS idx_sessions_last_active_at ON sessions (last_active_at);
"""


class SqliteSessionStore:
    """SessionStore implementation: sessions persisted in the shared SQLite DB.

    Timestamps are UTC ISO-8601 strings (the audit adapter's convention).
    All writes use ``datetime.now(timezone.utc).isoformat()``, so the string
    comparison ``last_active_at < cutoff`` is a true time comparison.
    """

    MIGRATIONS: list[tuple[int, str]] = [(3, SESSIONS_DDL)]

    def __init__(
        self,
        *,
        db_path: str | Path,
        max_turns: int = 10,
        ttl_seconds: int = 1800,
        retention_days: int | None = None,
    ) -> None:
        self.db_path = db_path
        self.max_messages = max_turns * 2
        self.ttl_seconds = ttl_seconds
        # T1-04: explicit retention override (tests); None = read global settings.
        self._retention_days: int | None = retention_days
        self._lock = threading.Lock()
        self._indexed_dbs: set[str] = set()
        self._working_memory: dict[str, dict[str, Any]] = {}
        self._init_schema_and_purge()

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _cutoff_iso(self) -> str:
        return (
            datetime.now(timezone.utc) - timedelta(seconds=self.ttl_seconds)
        ).isoformat()

    def _retention_cutoff_iso(self) -> str | None:
        # T1-04: optional days-based retention for sessions (0 = off).
        try:
            from app.core.config import settings

            days = int(getattr(settings, "session_retention_days", 0))
        except Exception:
            days = 0
        # Explicit constructor arg wins over global settings.
        if hasattr(self, "_retention_days") and self._retention_days is not None:
            days = int(self._retention_days)
        if days <= 0:
            return None
        return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    def _prepare(self, conn: Any) -> None:
        if str(self.db_path) not in self._indexed_dbs:
            conn.executescript(INDEXES_DDL)
            self._indexed_dbs.add(str(self.db_path))

    def _purge(self, conn: Any) -> None:
        conn.execute(
            "DELETE FROM sessions WHERE last_active_at < ?", (self._cutoff_iso(),)
        )
        conn.commit()
        # T1-04: days-based retention (bounded, idempotent). Runs on every
        # get/append/init alongside the TTL purge — no background thread.
        cutoff = self._retention_cutoff_iso()
        if cutoff:
            conn.execute("DELETE FROM sessions WHERE last_active_at < ?", (cutoff,))
            conn.commit()

    def _init_schema_and_purge(self) -> None:
        """Adapter init: apply migration v3, create the index, purge expired rows."""
        with db_connect(self.db_path, migrations=self.MIGRATIONS) as conn:
            self._prepare(conn)
            self._purge(conn)

    def get(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            with db_connect(self.db_path, migrations=self.MIGRATIONS) as conn:
                self._prepare(conn)
                self._purge(conn)
                row = conn.execute(
                    "SELECT data_json FROM sessions WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
        if row is None:
            return []
        return list(json.loads(row["data_json"]))

    def append(self, session_id: str, role: str, content: str) -> None:
        now = self._now_iso()
        with self._lock:
            with db_connect(self.db_path, migrations=self.MIGRATIONS) as conn:
                self._prepare(conn)
                self._purge(conn)
                row = conn.execute(
                    "SELECT data_json FROM sessions WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
                if row is None:
                    history = [{"role": role, "content": content}]
                    conn.execute(
                        "INSERT INTO sessions (session_id, data_json, created_at, last_active_at) "
                        "VALUES (?, ?, ?, ?)",
                        (
                            session_id,
                            json.dumps(history, ensure_ascii=False),
                            now,
                            now,
                        ),
                    )
                else:
                    history = json.loads(row["data_json"])
                    history.append({"role": role, "content": content})
                    history = history[-self.max_messages :]
                    conn.execute(
                        "UPDATE sessions SET data_json = ?, last_active_at = ? "
                        "WHERE session_id = ?",
                        (json.dumps(history, ensure_ascii=False), now, session_id),
                    )
                conn.commit()

    def get_working_memory(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            with db_connect(self.db_path, migrations=self.MIGRATIONS) as conn:
                self._prepare(conn)
                self._purge(conn)
                row = conn.execute(
                    "SELECT 1 FROM sessions WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
            if row is None:
                self._working_memory.pop(session_id, None)
                return None
            mem = self._working_memory.get(session_id)
            return dict(mem) if mem is not None else None

    def update_working_memory(self, session_id: str, memory_dict: dict[str, Any]) -> None:
        with self._lock:
            self._working_memory[session_id] = dict(memory_dict)