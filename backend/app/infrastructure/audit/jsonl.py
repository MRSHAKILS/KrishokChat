from __future__ import annotations

import json
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _retention_cutoff_iso(retention_days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=retention_days)).isoformat()


def purge_expired_jsonl(path: Path, retention_days: int) -> int:
    """Prune JSONL entries older than retention_days. Returns rows deleted.

    retention_days <=0 is a no-op. Idempotent — rewrites the file keeping only
    entries with timestamp >= cutoff. Malformed lines are dropped.
    """
    if retention_days <= 0 or not path.exists():
        return 0
    cutoff = _retention_cutoff_iso(retention_days)
    kept: list[str] = []
    deleted = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                deleted += 1
                continue
            ts = payload.get("timestamp")
            if isinstance(ts, str) and ts >= cutoff:
                kept.append(line if line.endswith("\n") else line + "\n")
            else:
                # Missing or old timestamp -> drop when retention is active
                if isinstance(ts, str):
                    deleted += 1
                else:
                    deleted += 1
    # Rewrite only if something was deleted
    if deleted:
        with path.open("w", encoding="utf-8") as handle:
            handle.writelines(kept)
    return deleted


class JSONLAuditSink:
    def __init__(self, path: Path, retention_days: int | None = None) -> None:
        self.path = path
        self._lock = threading.Lock()
        self._retention_days = retention_days
        if self._effective_retention() > 0:
            try:
                with self._lock:
                    purge_expired_jsonl(self.path, self._effective_retention())
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
        with self._lock:
            return purge_expired_jsonl(self.path, self._effective_retention())

    def record(self, entry: dict[str, Any]) -> None:
        # T0-05: the entry dict is spread verbatim, so the telemetry fields
        # (stage_timings_ms/tokens/provider/cost_estimate/request_id) serialize
        # additively and pre-T0-05 records (without them) load unchanged.
        payload = {"timestamp": datetime.now(timezone.utc).isoformat(), **entry}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
