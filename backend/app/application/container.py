"""Composition root. Routes receive this container; adapters never leak into routes."""

from dataclasses import dataclass
from pathlib import Path

from app.application.auth import AuthService
from app.application.generation import GroundedAnswerGenerator
from app.application.history import HistoryService
from app.application.qa_pipeline import QAPipeline
from app.application.rewrite import ConversationalQueryRewriter
from app.application.safety import SafetyClassifier
from app.application.soil import SoilService
from app.application.vision_pipeline import VisionPipeline
from app.core.config import Settings
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.auth.jwks import SupabaseJWKSVerifier
from app.infrastructure.cache.demo import DemoAnswerCache
from app.infrastructure.llm.factory import create_llm_client
from app.infrastructure.retrieval.bm25 import BM25Retriever
from app.infrastructure.retrieval.dense import DenseRetriever
from app.infrastructure.retrieval.expansion import QueryExpander
from app.infrastructure.retrieval.hybrid import HybridRetriever
from app.infrastructure.sessions.memory import InMemorySessionStore
from app.infrastructure.soil.dataset_loader import load_soil_dataset
from app.infrastructure.storage.postgrest import PostgrestSavedHistoryStore
from app.application.verifier import HardenedDosageVerifier
from app.infrastructure.vision.registry import ArtifactVisionRegistry
from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner


LOCAL_MODEL_NAME = "krishokchat-4b"


@dataclass
class AppContainer:
    qa: QAPipeline
    vision: VisionPipeline
    soil: SoilService
    auth: AuthService
    history: HistoryService
    llm_name: str


def build_container(settings: Settings) -> AppContainer:
    intent_llm = create_llm_client(settings, role="intent")
    generation_llm = create_llm_client(settings, role="generation")
    # T0-06: provider failover chain. With LLM_FAILOVER_CHAIN naming >= 2 valid
    # providers, generation and the rewrite lane ride a FailoverLLMClient
    # (skip tripped breakers, fall to the next provider; total failure raises
    # AllProvidersFailed, which the app maps to its existing fail-closed path).
    # The safety classifier always keeps the direct factory client — a fallback
    # chain must never influence a safety decision. Config rollback:
    # LLM_FAILOVER_CHAIN= (empty) → the exact single-provider client built today.
    intent_rewrite_llm = intent_llm
    if settings.llm_failover_chain.strip():
        # Lazy import: keeps the failover module independently revertable.
        from app.infrastructure.llm.failover import build_failover_client

        failover_intent = build_failover_client(settings, role="intent")
        if failover_intent is not None:
            intent_rewrite_llm = failover_intent
            # Same settings/chain as above, so this is never None here.
            generation_llm = build_failover_client(settings, role="generation")
    bm25_retriever = BM25Retriever(
        index_path=settings.rag_index_path / "indexes" / "bm25_index.pkl",
        corpus_path=settings.rag_corpus_path,
    )
    # P3: dense (FAISS + BGE-M3) channel + RRF fusion. The dense channel uses
    # the same OpenRouter key as generation; without a key or index it is
    # unavailable and the hybrid falls back to BM25-only automatically.
    dense_retriever = DenseRetriever(
        index_path=settings.rag_dense_faiss_path,
        ids_path=settings.rag_dense_ids_path,
        corpus_path=settings.rag_corpus_path,
        api_key=settings.openrouter_api_key,
    )
    expander = QueryExpander(
        term_map_path=settings.rag_term_map_path,
        dialect_map_path=settings.rag_dialect_map_path,
    )
    retriever = HybridRetriever(
        bm25=bm25_retriever,
        dense=dense_retriever,
        expander=expander,
        bm25_only=settings.retrieval_bm25_only,
    )
    # T0-03: session backend switch (config rollback: SESSION_BACKEND=memory).
    # sqlite persists sessions in the shared T0-01 DB across backend restarts
    # (same get/append semantics incl. TTL and max-turns trimming, lazy purge
    # only, no threads); memory (default) is the original adapter and keeps
    # the demo behavior byte-for-byte. Any unknown value falls back to memory.
    if settings.session_backend == "sqlite":
        # Lazy import: keeps the T0-03 adapter commit independently revertable
        # (a revert removes the module; the memory default still boots).
        from app.infrastructure.sessions.sqlite import SqliteSessionStore

        sessions = SqliteSessionStore(
            db_path=settings.resolved_sqlite_db_path,
            max_turns=settings.session_max_turns,
            ttl_seconds=settings.session_ttl_seconds,
        )
    else:
        sessions = InMemorySessionStore(
            max_turns=settings.session_max_turns,
            ttl_seconds=settings.session_ttl_seconds,
        )
    # T0-02: audit backend switch (config rollback: AUDIT_BACKEND=jsonl).
    # sqlite stores the same records in the shared SQLite DB and mirrors each
    # line to the JSONL path /api/safety/metrics reads, so the metrics panel
    # is identical under both backends; jsonl (default) is the original adapter.
    if settings.audit_backend == "sqlite":
        # Lazy import: keeps the T0-02 adapter commit independently revertable
        # (a revert removes the module; the jsonl default still boots).
        from app.infrastructure.audit.sqlite import AuditSqliteSink

        audit = AuditSqliteSink(
            path=settings.resolved_audit_log_path,
            db_path=settings.resolved_sqlite_db_path,
        )
    else:
        audit = JSONLAuditSink(settings.resolved_audit_log_path)
    # Local generation client for the KrishokChat selector option. The endpoint
    # is OpenAI-compatible (llama.cpp or Ollama) and remains configuration-driven.
    # It gets its own timeout/output/retry bounds: CPU inference (~5 tok/s)
    # cannot fit the remote 30s budget, and retrying a slow local generation is
    # pointless (the server is still working, not dropping the connection).
    local_settings = Settings(
        llm_provider="ollama",
        llm_base_url=settings.local_llm_base_url,
        generation_model_name=settings.local_llm_model_name,
        llm_timeout_seconds=settings.local_llm_timeout_seconds,
        llm_max_output_tokens=settings.local_llm_max_output_tokens,
        llm_max_retries=settings.local_llm_max_retries,
    )
    local_client = create_llm_client(local_settings, role="generation")
    # B1: demo answer cache — wired ONLY in demo mode. Loads the precomputed
    # cached_responses.json at startup (or an empty dict) and stores verified
    # safe answers for exact replay. With DEMO_MODE=false the pipeline runs
    # live with no cache at all.
    answer_cache = (
        DemoAnswerCache(
            settings.resolved_demo_cache_path,
            max_entries=settings.demo_cache_max_entries,
        )
        if settings.demo_mode
        else None
    )
    pipeline = QAPipeline(
        safety=SafetyClassifier(intent_llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(generation_llm),
        verifier=HardenedDosageVerifier(),
        audit=audit,
        sessions=sessions,
        top_k=settings.retrieval_top_k,
        generation_clients={LOCAL_MODEL_NAME: local_client},
        generation_tuning={
            LOCAL_MODEL_NAME: {
                "max_sources": settings.local_llm_source_limit,
                "max_source_chars": settings.local_llm_source_chars,
            }
        },
        answer_cache=answer_cache,
        # A1: follow-ups -> standalone retrieval queries (same cheap intent
        # model; fires only on follow-up markers with history present).
        rewriter=(
            ConversationalQueryRewriter(intent_rewrite_llm)
            if settings.query_rewrite_enabled
            else None
        ),
    )
    vision = VisionPipeline(
        registry=ArtifactVisionRegistry(Path(settings.ml_assets_dir) / "vision"),
        runner=UltralyticsClassificationRunner(),
        qa=pipeline,
        audit=audit,
        crop_threshold=settings.vision_crop_confidence_threshold,
        disease_threshold=settings.vision_disease_confidence_threshold,
        max_image_bytes=settings.vision_max_image_bytes,
    )
    soil = SoilService(
        info=load_soil_dataset(Path(settings.soil_release_dir)),
        audit=audit,
    )
    # P3: additive auth lane. Constructing the verifier performs NO network I/O
    # (lazy JWKS fetch on first presented token). Without SUPABASE_URL the
    # service denies everything — anonymous demo is untouched either way.
    auth = AuthService(
        verifier=(
            SupabaseJWKSVerifier(settings.supabase_jwks_url)
            if settings.supabase_jwks_url
            else None
        ),
    )
    # P4 decision 1 (saved history): additive lane. Store construction does
    # zero network I/O (httpx lazily connects per request). Without Supabase
    # configuration the service answers 503 — demo routes never call it.
    history = HistoryService(
        store=(
            PostgrestSavedHistoryStore(
                settings.supabase_url,
                settings.supabase_service_role_key,
            )
            if settings.supabase_url and settings.supabase_service_role_key
            else None
        ),
    )
    return AppContainer(
        qa=pipeline,
        vision=vision,
        soil=soil,
        auth=auth,
        history=history,
        llm_name=generation_llm.name,
    )
