"""T0-02: SQLite-backed audit sink.

Stores every audit record in the shared T0-01 SQLite database (table
``audit_records``, migration v2 registered on this adapter's own
``MIGRATIONS`` list — the shared list in ``storage/sqlite.py`` is asserted
empty by the T0-01 test and is out of scope to extend) AND mirrors the exact
JSONL line to ``path``.

Why the mirror: ``GET /api/safety/metrics`` reads ``container.qa.audit.path``
as JSONL (api/qa.py; the route file is out of scope for T0-02). The mirror is
what keeps the metrics panel identical under both backends. SQLite is the
durable store for later tiers (T0-05 telemetry, failover analysis).

Deduplication: a UNIQUE index on ``(timestamp, query_hash)`` makes writes
idempotent; both the sink and the backfill script insert with ``INSERT OR
IGNORE`` so a duplicate can never raise through the pipeline. ``query_hash``
is the SHA-256 of the query text, or of the canonical record JSON when the
record has no ``query`` (vision/soil events).
"""

from __future__ import annotations

import hashlib
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.infrastructure.storage.sqlite import db_connect

# T1-04: retention defaults — 0 = keep forever (today's behavior). The sink
# reads the live Settings at call time so a config flip is effective on the
# next write/startup without a code change. Tests may pass an explicit
# retention_days to the sink to avoid mutating global state.


def _retention_cutoff_iso(retention_days: int) -> str:
    from datetime import timedelta

    return (datetime.now(timezone.utc) - timedelta(days=retention_days)).isoformat()


def purge_expired_audit(db_path: Path, retention_days: int) -> int:
    """Delete audit_records older than retention_days. Returns rows deleted.

    retention_days <=0 is a no-op (keep forever). Idempotent and bounded —
    a single DELETE statement, no background thread.
    """
    if retention_days <= 0:
        return 0
    cutoff = _retention_cutoff_iso(retention_days)
    with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS) as conn:
        ensure_schema(conn)
        cur = conn.execute("DELETE FROM audit_records WHERE timestamp < ?", (cutoff,))
        conn.commit()
        return cur.rowcount


AUDIT_RECORDS_DDL = """
CREATE TABLE IF NOT EXISTS audit_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    query_hash TEXT NOT NULL,
    pipeline_version INTEGER,
    cached INTEGER,
    query TEXT,
    category TEXT,
    action TEXT,
    flagged INTEGER,
    safety_confidence REAL,
    safety_reason TEXT,
    safety_matched_rules TEXT,
    retrieved_count INTEGER,
    retrieval_top1_score REAL,
    retrieval_hit INTEGER,
    verifier_passed INTEGER,
    verifier_flag TEXT,
    verifier_checked INTEGER,
    verifier_grounded INTEGER,
    verifier_unsupported INTEGER,
    verifier_claims TEXT,
    answered_without_sources INTEGER,
    model TEXT,
    source_ids TEXT,
    error TEXT,
    channel TEXT,
    crop TEXT,
    disease TEXT,
    model_choice TEXT,
    retrieval_query_used TEXT,
    retrieval_query_rewritten INTEGER,
    request_id TEXT,
    stage_timings_ms TEXT,
    token_usage TEXT,
    provider TEXT,
    record_json TEXT NOT NULL
)
"""

# The T0-01 migration runner executes exactly one statement per migration
# version (conn.execute), so the indexes cannot ride in migration v2; they are
# created idempotently right after the first connection per sink instance.
INDEXES_DDL = """
CREATE INDEX IF NOT EXISTS idx_audit_records_timestamp ON audit_records (timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_records_category ON audit_records (category);
CREATE UNIQUE INDEX IF NOT EXISTS idx_audit_records_dedup ON audit_records (timestamp, query_hash);
"""

# Every field the JSONL adapter writes today (flat scalar columns where the
# value is scalar, JSON text columns where it is nested), plus the nullable
# reserved columns for T0-04 (request_id) and T0-05 (stage_timings_ms,
# token_usage, provider). Anything not in this list still survives in
# record_json (full original payload), so no record is ever lost.
# NOTE: the JSONL record field is ``tokens`` (dict, keys input/output);
# insert_record maps it onto the reserved ``token_usage`` column. T0-05's
# ``cost_estimate`` has no reserved column (migrations are locked by the
# T0-02 tests) and is preserved in record_json only.
_KNOWN_COLUMNS = (
    "timestamp",
    "query_hash",
    "pipeline_version",
    "cached",
    "query",
    "category",
    "action",
    "flagged",
    "safety_confidence",
    "safety_reason",
    "safety_matched_rules",
    "retrieved_count",
    "retrieval_top1_score",
    "retrieval_hit",
    "verifier_passed",
    "verifier_flag",
    "verifier_checked",
    "verifier_grounded",
    "verifier_unsupported",
    "verifier_claims",
    "answered_without_sources",
    "model",
    "source_ids",
    "error",
    "channel",
    "crop",
    "disease",
    "model_choice",
    "retrieval_query_used",
    "retrieval_query_rewritten",
    "request_id",
    "stage_timings_ms",
    "token_usage",
    "provider",
)


def query_hash(payload: dict[str, Any]) -> str:
    """SHA-256 hex dedup key: the query text when present, otherwise the
    canonical JSON of the record (minus timestamp) so query-less vision/soil
    events still dedup on their content."""
    query = payload.get("query")
    if query:
        return hashlib.sha256(str(query).encode("utf-8")).hexdigest()
    canonical = json.dumps(
        {key: value for key, value in payload.items() if key != "timestamp"},
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _cell(value: Any) -> Any:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def ensure_schema(conn: Any) -> None:
    """Idempotently create the audit_records indexes on a migrated connection.

    The migration runner executes one statement per version, so the indexes
    cannot ride inside migration v2; this runs the same guarded statements
    (IF NOT EXISTS) on first use.
    """
    conn.executescript(INDEXES_DDL)


def insert_record(conn: Any, payload: dict[str, Any]) -> int:
    """Insert one record into audit_records; returns 1 when inserted, 0 when a
    (timestamp, query_hash) duplicate was ignored. Commits immediately —
    legacy sqlite3 keeps implicit transactions open, so a commit per row is
    required for the row to survive the connection closing."""
    values = {name: _cell(payload[name]) for name in _KNOWN_COLUMNS if name in payload}
    # T0-05: the JSONL record carries ``tokens`` (dict with input/output); the
    # reserved column is named ``token_usage`` — map it here so the column is
    # filled and the mirror JSONL keeps the spec'd field name.
    if "tokens" in payload and "token_usage" not in values:
        values["token_usage"] = _cell(payload["tokens"])
    values.setdefault("query_hash", query_hash(payload))
    values["record_json"] = json.dumps(payload, ensure_ascii=False)
    columns = ", ".join(values)
    placeholders = ", ".join("?" * len(values))
    cursor = conn.execute(
        f"INSERT OR IGNORE INTO audit_records ({columns}) VALUES ({placeholders})",
        tuple(values.values()),
    )
    conn.commit()
    return cursor.rowcount


class AuditSqliteSink:
    """AuditSink implementation: SQLite rows + JSONL mirror (see module doc)."""

    MIGRATIONS: list[tuple[int, str]] = [(2, AUDIT_RECORDS_DDL)]

    def __init__(self, path: Path, db_path: Path, retention_days: int | None = None) -> None:
        self.path = path
        self.db_path = db_path
        self._lock = threading.Lock()
        self._indexed_dbs: set[str] = set()
        # T1-04: optional explicit retention (tests may pass 1); None = read
        # live Settings (0 = keep forever, no purge). Purge on startup when
        # enabled — idempotent, bounded, no background thread.
        self._retention_days = retention_days
        if self._effective_retention() > 0:
            try:
                purge_expired_audit(self.db_path, self._effective_retention())
            except Exception:
                pass

    def _effective_retention(self) -> int:
        if self._retention_days is not None:
            return int(self._retention_days)
        try:
            from app.core.config import settings

            return int(settings.audit_retention_days)
        except Exception:
            return 0

    def purge(self) -> int:
        """Explicit purge using the effective retention. Returns rows deleted."""
        return purge_expired_audit(self.db_path, self._effective_retention())

    def record(self, entry: dict[str, Any]) -> None:
        payload = {"timestamp": datetime.now(timezone.utc).isoformat(), **entry}
        # T1-04: on-write purge when retention is enabled (bounded DELETE).
        if self._effective_retention() > 0:
            try:
                purge_expired_audit(self.db_path, self._effective_retention())
            except Exception:
                pass
        # Mirror first: the metrics panel is the live demo surface and reads
        # this file; SQLite is the durable copy. A mirror failure must be
        # visible (raise) exactly like the JSONL adapter's write failure.
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        with db_connect(self.db_path, migrations=self.MIGRATIONS) as conn:
            if str(self.db_path) not in self._indexed_dbs:
                ensure_schema(conn)
                self._indexed_dbs.add(str(self.db_path))
            insert_record(conn, payload)

    def read_entries(self) -> list[dict[str, Any]]:
        """Every stored record, oldest first, as the original dict payloads."""
        with db_connect(self.db_path, migrations=self.MIGRATIONS) as conn:
            if str(self.db_path) not in self._indexed_dbs:
                ensure_schema(conn)
                self._indexed_dbs.add(str(self.db_path))
            rows = conn.execute(
                "SELECT record_json FROM audit_records ORDER BY id"
            ).fetchall()
        return [json.loads(row["record_json"]) for row in rows]