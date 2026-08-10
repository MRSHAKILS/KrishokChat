from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root is 2 levels up from this file (backend/app/core/ -> backend/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # .env.local (backend-local secrets) takes priority over root .env.
        env_file=(str(PROJECT_ROOT.parent / ".env"), str(PROJECT_ROOT / ".env.local")),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "KrishokChat Advisory System"
    app_version: str = "0.2.0"
    environment: str = "development"
    debug: bool = False

    ollama_base_url: str = "http://localhost:11434"
    ollama_model_name: str = "krishokchat-4b"
    gguf_path: str = "backend/ml_assets/gemma/model.gguf"

    # Both intent classification and generation use the same OpenRouter model for
    # this demo. Explicit provider values remain available for tests/replacement.
    llm_provider: str = "openrouter"
    llm_model_name: str = "krishokchat-4b"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_timeout_seconds: float = 30.0
    llm_temperature: float = 0.2
    llm_max_output_tokens: int = 1000
    intent_model_name: str | None = None
    generation_model_name: str | None = None

    openrouter_api_key: str | None = None
    openrouter_model: str = "google/gemini-2.5-flash-lite"
    gemini_model: str = "gemini-2.5-flash-lite"
    gemini_api_key: str | None = None

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_origin: str = "http://localhost:3000,http://localhost:3100,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3100"

    retrieval_top_k: int = 5
    rag_backend: str = "FAISS"

    demo_mode: bool = True
    demo_cache_path: str = "demo-assets/cached_responses.json"

    session_max_turns: int = Field(default=10, ge=1, le=100)
    session_ttl_seconds: int = Field(default=1800, ge=60)
    audit_log_path: str = "backend/app/logs/safety_audit.jsonl"

    vision_crop_confidence_threshold: float = Field(default=0.60, ge=0.0, le=1.0)
    vision_disease_confidence_threshold: float = Field(default=0.55, ge=0.0, le=1.0)
    vision_max_image_bytes: int = Field(default=10_000_000, ge=100_000)

    ml_assets_dir: str = str(PROJECT_ROOT / "ml_assets")

    gemini_key_cooldown_seconds: float = 6.0
    env_file_path: str = str(PROJECT_ROOT.parent / ".env")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origin.split(",") if origin.strip()]

    @property
    def resolved_audit_log_path(self) -> Path:
        path = Path(self.audit_log_path)
        return path if path.is_absolute() else PROJECT_ROOT.parent / path

    @property
    def rag_index_path(self) -> Path:
        return Path(self.ml_assets_dir) / "rag_index"

    @property
    def resolved_llm_model(self) -> str:
        if self.llm_provider == "openrouter":
            return self.generation_model_name or self.openrouter_model
        if self.llm_provider == "gemini":
            return self.generation_model_name or self.gemini_model
        return self.generation_model_name or self.llm_model_name


settings = Settings()
