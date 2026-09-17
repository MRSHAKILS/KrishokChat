from __future__ import annotations

import time
from collections import OrderedDict
from threading import Lock
from typing import Any


class InMemorySessionStore:
    def __init__(self, *, max_turns: int = 10, ttl_seconds: int = 1800) -> None:
        self.max_messages = max_turns * 2
        self.ttl_seconds = ttl_seconds
        self._items: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
        self._working_memory: dict[str, dict[str, Any]] = {}
        self._timestamps: dict[str, float] = {}
        self._lock = Lock()

    def _evict(self) -> None:
        now = time.time()
        for session_id, timestamp in list(self._timestamps.items()):
            if now - timestamp > self.ttl_seconds:
                self._timestamps.pop(session_id, None)
                self._items.pop(session_id, None)
                self._working_memory.pop(session_id, None)

    def get(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            self._evict()
            return list(self._items.get(session_id, []))

    def append(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            self._evict()
            history = self._items.setdefault(session_id, [])
            history.append({"role": role, "content": content})
            self._items[session_id] = history[-self.max_messages :]
            self._timestamps[session_id] = time.time()

    def get_working_memory(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            self._evict()
            mem = self._working_memory.get(session_id)
            return dict(mem) if mem is not None else None

    def update_working_memory(self, session_id: str, memory_dict: dict[str, Any]) -> None:
        with self._lock:
            self._evict()
            self._working_memory[session_id] = dict(memory_dict)
            self._timestamps[session_id] = time.time()
