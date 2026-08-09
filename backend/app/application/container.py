"""Composition root. Routes receive this container; adapters never leak into routes."""

from dataclasses import dataclass
from pathlib import Path

from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAPipeline
from app.application.safety import SafetyClassifier
from app.application.vision_pipeline import VisionPipeline
from app.core.config import Settings
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.llm.factory import create_llm_client
from app.infrastructure.retrieval.bm25 import BM25Retriever
from app.infrastructure.sessions.memory import InMemorySessionStore
from app.infrastructure.verification.dosage import DosageVerifier
from app.infrastructure.vision.registry import ArtifactVisionRegistry
from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner


@dataclass
class AppContainer:
    qa: QAPipeline
    vision: VisionPipeline
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
    pipeline = QAPipeline(
        safety=SafetyClassifier(intent_llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(generation_llm),
        verifier=DosageVerifier(),
        audit=audit,
        sessions=sessions,
        top_k=settings.retrieval_top_k,
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
    return AppContainer(qa=pipeline, vision=vision, llm_name=generation_llm.name)
