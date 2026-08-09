from __future__ import annotations

import os

from app.core.config import Settings
from app.infrastructure.llm.gemini import GeminiClient
from app.infrastructure.llm.openai_compatible import OpenAICompatibleClient, UnavailableLLMClient


def _first_gemini_key() -> str | None:
    for index in range(1, 30):
        value = os.getenv(f"GEMINI_API_KEY_{index}")
        if value:
            return value
    return os.getenv("GEMINI_API_KEY")


def _resolve_provider(settings: Settings) -> str:
    """Resolve ``auto`` without ever turning an unavailable provider into safe_agri."""
    configured = settings.llm_provider.lower().strip()
    if configured != "auto":
        return configured
    if settings.openrouter_api_key:
        return "openrouter"
    if settings.llm_api_key and settings.llm_base_url:
        return "ollama"
    if settings.gemini_api_key or _first_gemini_key():
        return "gemini"
    return "ollama"


def create_llm_client(settings: Settings, *, role: str = "generation"):
    provider = _resolve_provider(settings)
    model_override = settings.intent_model_name if role == "intent" else settings.generation_model_name
    if provider == "ollama":
        base_url = settings.llm_base_url or f"{settings.ollama_base_url.rstrip('/')}/v1"
        return OpenAICompatibleClient(
            base_url=base_url,
            model=model_override or settings.llm_model_name,
            api_key=settings.llm_api_key,
            timeout=settings.llm_timeout_seconds,
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_output_tokens,
        )
    if provider == "openrouter":
        return OpenAICompatibleClient(
            base_url=settings.llm_base_url or "https://openrouter.ai/api/v1",
            model=model_override or settings.openrouter_model,
            api_key=settings.llm_api_key or settings.openrouter_api_key,
            timeout=settings.llm_timeout_seconds,
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_output_tokens,
        )
    if provider == "gemini":
        key = settings.llm_api_key or settings.gemini_api_key or _first_gemini_key()
        if key:
            return GeminiClient(
                api_key=key,
                model=model_override or settings.resolved_llm_model,
                temperature=settings.llm_temperature,
                max_output_tokens=settings.llm_max_output_tokens,
            )
    return UnavailableLLMClient()
