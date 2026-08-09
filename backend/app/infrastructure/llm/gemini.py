"""Transitional Gemini adapter behind the same application-level LLM port."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any

from app.infrastructure.llm.openai_compatible import LLMError, parse_json_object


class GeminiClient:
    def __init__(self, *, api_key: str, model: str, temperature: float, max_output_tokens: int) -> None:
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.name = model

    def _client(self):
        try:
            from google import genai
        except ImportError as exc:  # pragma: no cover - dependency is project-managed
            raise LLMError("google-genai is not installed") from exc
        return genai.Client(api_key=self.api_key)

    async def _generate_sync(self, prompt: str, *, json_mode: bool = False) -> str:
        def call() -> str:
            from google import genai

            config = genai.types.GenerateContentConfig(
                temperature=0.0 if json_mode else self.temperature,
                max_output_tokens=180 if json_mode else self.max_output_tokens,
                response_mime_type="application/json" if json_mode else None,
            )
            response = self._client().models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            text = getattr(response, "text", None)
            if not isinstance(text, str) or not text.strip():
                raise LLMError("Gemini returned an empty response")
            return text.strip()

        try:
            return await asyncio.to_thread(call)
        except LLMError:
            raise
        except Exception as exc:
            raise LLMError(f"Gemini request failed: {exc}") from exc

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        return parse_json_object(await self._generate_sync(prompt, json_mode=True))

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        return await self._generate_sync(prompt)

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        yield await self.generate(prompt, metadata=metadata)
