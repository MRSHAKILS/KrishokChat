"""Composition root. Routes receive this container; adapters never leak into routes."""

from dataclasses import dataclass
from pathlib import Path

from app.application.auth import AuthService
from app.application.generation import GroundedAnswerGenerator
from app.application.history import HistoryService
from app.application.qa_pipeline import QAPipeline
from app.application.safety import SafetyClassifier
from app.application.soil import SoilService
from app.application.vision_pipeline import VisionPipeline
from app.core.config import Settings
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.auth.jwks import SupabaseJWKSVerifier
from app.infrastructure.llm.factory import create_llm_client
from app.infrastructure.retrieval.bm25 import BM25Retriever
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
    retriever = BM25Retriever(
        index_path=settings.rag_index_path / "indexes" / "bm25_index.pkl",
        corpus_path=settings.rag_index_path / "processed" / "knowledge_nodes_clean.jsonl",
    )
    sessions = InMemorySessionStore(
        max_turns=settings.session_max_turns,
        ttl_seconds=settings.session_ttl_seconds,
    )
    audit = JSONLAuditSink(settings.resolved_audit_log_path)
    # Local generation client for the KrishokChat selector option. The endpoint
    # is OpenAI-compatible (llama.cpp or Ollama) and remains configuration-driven.
    local_settings = Settings(
        llm_provider="ollama",
        llm_base_url=settings.local_llm_base_url,
        generation_model_name=settings.local_llm_model_name,
    )
    local_client = create_llm_client(local_settings, role="generation")
    pipeline = QAPipeline(
        safety=SafetyClassifier(intent_llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(generation_llm),
        verifier=HardenedDosageVerifier(),
        audit=audit,
        sessions=sessions,
        top_k=settings.retrieval_top_k,
        generation_clients={LOCAL_MODEL_NAME: local_client},
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
