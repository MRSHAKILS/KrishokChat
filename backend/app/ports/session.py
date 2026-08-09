from __future__ import annotations

from typing import Protocol


class SessionStore(Protocol):
    def get(self, session_id: str) -> list[dict[str, str]]: ...

    def append(self, session_id: str, role: str, content: str) -> None: ...
