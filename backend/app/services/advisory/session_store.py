"""In-memory session store with TTL eviction for multi-turn chat."""
import time
import threading
from collections import OrderedDict


class SessionStore:
    def __init__(self, max_turns: int = 10, ttl_seconds: int = 1800):
        self._store: OrderedDict[str, list[dict]] = OrderedDict()
        self._timestamps: dict[str, float] = {}
        self._max_turns = max_turns
        self._ttl = ttl_seconds
        self._lock = threading.Lock()

    def get(self, session_id: str) -> list[dict]:
        with self._lock:
            self._evict_expired()
            return list(self._store.get(session_id, []))

    def append(self, session_id: str, role: str, content: str):
        with self._lock:
            self._evict_expired()
            if session_id not in self._store:
                self._store[session_id] = []
            history = self._store[session_id]
            history.append({"role": role, "content": content})
            if len(history) > self._max_turns * 2:
                self._store[session_id] = history[-self._max_turns * 2:]
            self._timestamps[session_id] = time.time()

    def clear(self, session_id: str):
        with self._lock:
            self._store.pop(session_id, None)
            self._timestamps.pop(session_id, None)

    def _evict_expired(self):
        now = time.time()
        expired = [sid for sid, ts in self._timestamps.items() if now - ts > self._ttl]
        for sid in expired:
            self._store.pop(sid, None)
            self._timestamps.pop(sid, None)


session_store = SessionStore()
