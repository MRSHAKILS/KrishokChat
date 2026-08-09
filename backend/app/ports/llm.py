from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Protocol


class LLMClient(Protocol):
    name: str

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        """Return a parsed structured classification or raise LLMError."""

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        """Generate text from the supplied prompt."""

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        """Yield answer text chunks. Adapters may yield one chunk if streaming is unavailable."""
