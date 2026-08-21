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
    # P0-5: docs toggle. DOCS_ENABLED=true (default) keeps /docs, /redoc and
    # /openapi.json as before; when false the FastAPI app is created without
    # those routes so a production box can avoid exposing the API surface.
    docs_enabled: bool = True
    debug: bool = False

    ollama_base_url: str = "http://localhost:11434"
    ollama_model_name: str = "krishokchat-4b"
    local_llm_base_url: str = "http://127.0.0.1:11434/v1"
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
    llm_max_retries: int = 3
    intent_model_name: str | None = None
    generation_model_name: str | None = None

    # Local (llama-server/Ollama CPU) model tuning — separate from the remote
    # client because CPU inference at ~5 tok/s cannot fit a 30s budget. These
    # apply only to the local_llm_* endpoint wired into the model selector.
    local_llm_timeout_seconds: float = 300.0
    local_llm_max_output_tokens: int = 250
    local_llm_max_retries: int = 1
    # Prompt-size caps for the local lane: fewer, shorter sources cut the
    # CPU prompt-eval phase (the dominant cost on this machine).
    local_llm_source_limit: int = 3
    local_llm_source_chars: int = 800
    # P0-6: local-lane concurrency ceiling. llama.cpp serves requests
    # serially per slot; concurrent queries queue on a pipeline semaphore
    # instead of stacking up inside the inference process. 1..16, default 2.
    local_llm_max_concurrency: int = Field(default=2, ge=1, le=16)
    # P0-7: corpus generation tag baked into demo-cache keys. Bump this after
    # rebuilding the retrieval index so stale cached demo answers are never
    # replayed against a different knowledge base (old entries stay in the
    # JSON file but become unreachable, and are pruned by size cap).
    corpus_version: str = "2026-08"

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
    # T0-01: shared SQLite database for the future audit/sessions adapters.
    # Resolved relative to project root the same way resolved_audit_log_path is.
    sqlite_db_path: str = "backend/data/krishokchat.db"
    # T0-02: audit adapter backend — "jsonl" (default; the original adapter
    # and metrics-panel contract) or "sqlite" (same records in the shared
    # SQLite DB, mirroring each line to the JSONL path the metrics endpoint
    # reads). Any unknown value falls back to jsonl in the container.
    audit_backend: str = "jsonl"
    # T0-03: session store backend — "memory" (default; the original adapter)
    # or "sqlite" (sessions persisted in the shared SQLite DB, surviving
    # backend restarts; same TTL/max-turns semantics). Any unknown value
    # falls back to memory in the container. Reuses session_ttl_seconds.
    session_backend: str = "memory"

    # T0-04: request-ID header echoed by the middleware (and expected on
    # inbound requests), plus the log level for the JSON app logger.
    request_id_header: str = "X-Request-ID"
    log_level: str = "INFO"
    # P0-13: audit retention window in days. The retention job documented in
    # docs/production_readiness/retention_policy.md purges entries older than
    # this (jsonl rotate + sqlite DELETE); the app itself never auto-deletes.
    # T1-04: 0 = keep forever (today's behavior, off by default). Set 90 to
    # enforce the 90-day PDP-aligned window.
    audit_retention_days: int = Field(default=0, ge=0)
    # T1-04: session retention window (days) for the SQLite session store.
    # 0 = keep forever; 30 aligns with SESSION_TTL_SECONDS and is the default
    # when retention is enabled. The store purges lazily on startup/on-write.
    session_retention_days: int = Field(default=30, ge=0)
    # T1-04: write-time PII redaction for stored audit query text. false =
    # verbatim (today); true = phone/email/name redacted before persist.
    # The user-visible answer is never altered.
    pii_redaction_enabled: bool = False

    # P0-1: readiness gate. /readyz always reports per-check status and always
    # answers 200 by default (a load balancer may still scrape it); when this
    # flag is true a failed check returns 503 so orchestrators can restart the
    # box. Default false keeps the demo behavior identical.
    readiness_strict: bool = False

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

    # T0-06: provider failover chain — comma-separated provider names in
    # fallback order (openrouter,gemini,ollama; "auto" is never a chain
    # entry). Empty (default) = today's single-provider behavior, no wrapper.
    # Only chains with >= 2 valid providers activate the FailoverLLMClient;
    # unknown names are logged and skipped, never a startup crash.
    llm_failover_chain: str = ""
    # T0-06: circuit-breaker bounds per provider in the failover chain.
    llm_circuit_max_failures: int = 3
    llm_circuit_cooldown_seconds: float = 30.0

    # T0-07: API-key auth + rate limits for the /api/v1 surface. All default
    # off — the anonymous demo never presents keys and is never limited
    # (AGENTS.md §2.1). Keys come from the environment as a comma-separated
    # literal (the SQLite-backed key store is a documented follow-up on
    # T0-01); they are never logged in full — only a label + sha256 hash.
    api_key_enabled: bool = False
    api_keys: str = ""
    # Per-key (and per-anonymous-IP, see rate_limit_anon_enabled) sliding
    # window cap on /api/v1/* requests per minute. 0 disables the limiter.
    rate_limit_per_minute: int = 60
    rate_limit_anon_enabled: bool = False

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
    def resolved_sqlite_db_path(self) -> Path:
        path = Path(self.sqlite_db_path)
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
