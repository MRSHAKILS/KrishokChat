"""Async adapter for Ollama and OpenAI-compatible gateways such as OpenRouter."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any

import httpx


class LLMError(RuntimeError):
    """Raised when an LLM adapter cannot provide a valid response."""


def parse_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
    try:
        value = json.loads(cleaned.strip())
    except json.JSONDecodeError as exc:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise LLMError("LLM returned invalid JSON") from exc
        try:
            value = json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError as nested_exc:
            raise LLMError("LLM returned invalid JSON") from nested_exc
    if not isinstance(value, dict):
        raise LLMError("LLM JSON response must be an object")
    return value


class OpenAICompatibleClient:
    def __init__(
        self,
        *,
        base_url: str,
        model: str,
        api_key: str | None,
        timeout: float = 30.0,
        temperature: float = 0.2,
        max_output_tokens: int = 1000,
        max_retries: int = 3,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key or "ollama"
        self.timeout = timeout
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.max_retries = max_retries
        self.name = model

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    async def _request(self, payload: dict[str, Any]) -> httpx.Response:
        """POST with bounded retries so transient network drops do not fail closed."""
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=self._headers(),
                        json=payload,
                    )
                response.raise_for_status()
                return response
            except (httpx.HTTPError, OSError) as exc:
                last_error = exc
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1.0 + attempt)
        raise LLMError(f"LLM request failed: {last_error}") from last_error

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        base_payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 180,
        }
        # Prefer structured JSON mode; fall back to plain text parsing if the
        # gateway drops the connection or rejects response_format.
        for payload in (
            {**base_payload, "response_format": {"type": "json_object"}},
            base_payload,
        ):
            try:
                response = await self._request(payload)
                content = response.json()["choices"][0]["message"]["content"]
            except (LLMError, KeyError, IndexError, TypeError, ValueError):
                continue
            try:
                return parse_json_object(content)
            except LLMError:
                continue
        raise LLMError("LLM classification request failed after retries")

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        response = await self._request(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "max_tokens": self.max_output_tokens,
            }
        )
        try:
            content = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMError("LLM response did not contain chat content") from exc
        if not isinstance(content, str) or not content.strip():
            raise LLMError("LLM returned an empty answer")
        return content.strip()

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        # The application contract supports chunks; the adapter keeps transport details
        # private. Ollama/OpenAI gateways can be upgraded to true chunk streaming later.
        yield await self.generate(prompt, metadata=metadata)


class UnavailableLLMClient:
    name = "unavailable"

    async def classify_json(self, prompt: str) -> dict[str, Any]:
        raise LLMError("No LLM provider is configured")

    async def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        raise LLMError("No LLM provider is configured")

    async def stream(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> AsyncIterator[str]:
        raise LLMError("No LLM provider is configured")
        yield ""
