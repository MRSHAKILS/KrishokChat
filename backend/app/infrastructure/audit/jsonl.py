from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JSONLAuditSink:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()

    def record(self, entry: dict[str, Any]) -> None:
        # T0-05: the entry dict is spread verbatim, so the telemetry fields
        # (stage_timings_ms/tokens/provider/cost_estimate/request_id) serialize
        # additively and pre-T0-05 records (without them) load unchanged.
        payload = {"timestamp": datetime.now(timezone.utc).isoformat(), **entry}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
