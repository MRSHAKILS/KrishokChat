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
    local_llm_base_url: str = "http://127.0.0.1:11435/v1"
    local_llm_model_name: str = "krishokchat-4b"
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
    # B1: cap for the demo answer cache (exact-replay of curated questions).
    demo_cache_max_entries: int = 100

    session_max_turns: int = Field(default=10, ge=1, le=100)
    session_ttl_seconds: int = Field(default=1800, ge=60)
    audit_log_path: str = "backend/app/logs/safety_audit.jsonl"

    # P3 hybrid retrieval: force the BM25-only fallback even when the dense
    # (FAISS/BGE-M3) index exists. The dense channel also falls back to BM25
    # automatically whenever the OpenRouter key or index is unavailable.
    retrieval_bm25_only: bool = False

    # A1: rewrite follow-up queries into standalone retrieval queries using
    # conversation history (one cheap LLM call, only when a follow-up marker
    # is present AND history exists). Disable to always search raw queries.
    query_rewrite_enabled: bool = True

    vision_crop_confidence_threshold: float = Field(default=0.60, ge=0.0, le=1.0)
    vision_disease_confidence_threshold: float = Field(default=0.55, ge=0.0, le=1.0)
    vision_max_image_bytes: int = Field(default=10_000_000, ge=100_000)

    ml_assets_dir: str = str(PROJECT_ROOT / "ml_assets")
    soil_release_dir: str = str(PROJECT_ROOT.parent / "dataset_release" / "soil_moisture")

    gemini_key_cooldown_seconds: float = 6.0
    env_file_path: str = str(PROJECT_ROOT.parent / ".env")

    # P5 voice lane — read-aloud (TTS). edge-tts (keyless, free) synthesizes
    # through Microsoft Edge's Read Aloud service; the demo machine has no
    # Bengali system voice, so this is what makes শুনুন read real Bengali.
    tts_default_voice: str = "bn-BD-NabanitaNeural"
    tts_timeout_seconds: float = 15.0
    tts_cache_max_entries: int = 256
    # Spacing between /api/tts/prewarm items (upstream rate window safety).
    tts_prewarm_spacing_seconds: float = 10.0

    # P5 voice lane — optional server-side ASR fallback (Groq Whisper free
    # tier, no credit card). Leave empty to keep the browser Web Speech mic
    # as the only voice input; /api/transcribe answers 501 without a key.
    groq_api_key: str | None = None
    groq_whisper_model: str = "whisper-large-v3-turbo"

    # Supabase Auth (amendment 15) — all optional. The anonymous demo never
    # uses these; they only enable the additive auth lane.
    supabase_url: str | None = None
    supabase_publishable_key: str | None = None
    supabase_service_role_key: str | None = None

    # Google OAuth (archived for deployment + future server-side Google token
    # checks). The live provider config lives in the Supabase dashboard.
    google_oauth_client_id: str | None = None
    google_oauth_client_secret: str | None = None

    @property
    def supabase_jwks_url(self) -> str | None:
        if not self.supabase_url:
            return None
        return f"{self.supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origin.split(",") if origin.strip()]

    @property
    def resolved_audit_log_path(self) -> Path:
        path = Path(self.audit_log_path)
        return path if path.is_absolute() else PROJECT_ROOT.parent / path

    @property
    def resolved_demo_cache_path(self) -> Path:
        path = Path(self.demo_cache_path)
        return path if path.is_absolute() else PROJECT_ROOT.parent / path

    @property
    def rag_index_path(self) -> Path:
        return Path(self.ml_assets_dir) / "rag_index"

    @property
    def rag_corpus_path(self) -> Path:
        return self.rag_index_path / "processed" / "knowledge_nodes_clean.jsonl"

    @property
    def rag_dense_faiss_path(self) -> Path:
        return self.rag_index_path / "indexes" / "nodes.faiss"

    @property
    def rag_dense_ids_path(self) -> Path:
        return self.rag_index_path / "indexes" / "node_ids.json"

    @property
    def rag_term_map_path(self) -> Path:
        return self.rag_index_path / "indexes" / "term_map.json"

    @property
    def rag_dialect_map_path(self) -> Path:
        # Restored dataset_release/safety/phase4_dialect_map.json is merged
        # automatically when present; absence degrades nothing.
        return PROJECT_ROOT.parent / "dataset_release" / "safety" / "phase4_dialect_map.json"

    @property
    def resolved_llm_model(self) -> str:
        if self.llm_provider == "openrouter":
            return self.generation_model_name or self.openrouter_model
        if self.llm_provider == "gemini":
            return self.generation_model_name or self.gemini_model
        return self.generation_model_name or self.llm_model_name


settings = Settings()
