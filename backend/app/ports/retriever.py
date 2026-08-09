from __future__ import annotations

from typing import Protocol

from app.domain.contracts import RetrievedSource


class Retriever(Protocol):
    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]: ...
