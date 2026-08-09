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
        payload = {"timestamp": datetime.now(timezone.utc).isoformat(), **entry}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
