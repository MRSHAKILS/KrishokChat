"""T0-02: backfill the existing JSONL audit log into the shared SQLite DB.

Idempotent by the (timestamp, query_hash) UNIQUE index on ``audit_records``:
a re-run inserts nothing new. ``--force`` truncates the table and reloads
every line.

Usage (from backend/):
    uv run python scripts/backfill_audit_jsonl_to_sqlite.py
    uv run python scripts/backfill_audit_jsonl_to_sqlite.py --force
    uv run python scripts/backfill_audit_jsonl_to_sqlite.py --db path.db --log path.jsonl

Output is one JSON object with run stats: lines_read, inserted, invalid,
total_rows.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import Settings  # noqa: E402
from app.infrastructure.audit.sqlite import AuditSqliteSink, ensure_schema, insert_record  # noqa: E402
from app.infrastructure.storage.sqlite import db_connect  # noqa: E402


def backfill(
    jsonl_path: Path,
    db_path: Path,
    *,
    force: bool = False,
) -> dict[str, int]:
    """Copy every valid JSONL line into audit_records; returns run stats.

    A line counts as invalid (skipped, not counted as a duplicate) when it is
    blank, not JSON, not a dict, or has no ``timestamp``.
    """
    lines_read = 0
    invalid = 0
    inserted = 0
    with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS) as conn:
        ensure_schema(conn)
        if force:
            conn.execute("DELETE FROM audit_records")
            conn.commit()
        if jsonl_path.exists():
            with jsonl_path.open(encoding="utf-8") as handle:
                for line in handle:
                    lines_read += 1
                    stripped = line.strip()
                    if not stripped:
                        invalid += 1
                        continue
                    try:
                        payload: Any = json.loads(stripped)
                    except json.JSONDecodeError:
                        invalid += 1
                        continue
                    if not isinstance(payload, dict) or "timestamp" not in payload:
                        invalid += 1
                        continue
                    inserted += insert_record(conn, payload)
        total = conn.execute("SELECT COUNT(*) AS n FROM audit_records").fetchone()["n"]
    return {
        "lines_read": lines_read,
        "inserted": inserted,
        "invalid": invalid,
        "total_rows": total,
    }


def main(argv: list[str] | None = None) -> int:
    settings = Settings()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="truncate audit_records and reload every line",
    )
    parser.add_argument(
        "--db",
        default=str(settings.resolved_sqlite_db_path),
        help="SQLite DB path (default: from settings)",
    )
    parser.add_argument(
        "--log",
        default=str(settings.resolved_audit_log_path),
        help="JSONL audit log path (default: from settings)",
    )
    args = parser.parse_args(argv)
    stats = backfill(Path(args.log), Path(args.db), force=args.force)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())