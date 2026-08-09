from __future__ import annotations

from typing import Any, Protocol


class AuditSink(Protocol):
    def record(self, entry: dict[str, Any]) -> None: ...
