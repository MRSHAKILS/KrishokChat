"""Legacy wrapper around the single grounded generation adapter.

New request code must use ``QAPipeline``. Keeping this small wrapper prevents the old
scripts from reintroducing a second Gemini/OpenRouter implementation.
"""

from __future__ import annotations

import asyncio
import os

from app.application.container import build_container
from app.application.generation import GroundedAnswerGenerator
from app.core.config import settings
from app.domain.contracts import QueryContext, RetrievedSource


def get_gemini_keys() -> list[str]:
    return [
        value
        for name, value in os.environ.items()
        if name.startswith("GEMINI_API_KEY") and value
    ]


def compute_confidence_gate(retrieved_nodes, detected_crop, detected_disease, intent, query):
    if not retrieved_nodes:
        return ("REFER_EXPERT" if intent in {"treatment", "prevention"} else "GENERAL_GUIDANCE", 0.1, "no_sources")
    score = float(retrieved_nodes[0].get("score", 0))
    if score > 15:
        return "FULLY_GROUNDED", min(0.95, score / 25), "strong_retrieval"
    if score > 3:
        return "PARTIALLY_GROUNDED", 0.5, "partial_retrieval"
    return "GENERAL_GUIDANCE", 0.3, "weak_retrieval"


def _sources(items: list[dict]) -> list[RetrievedSource]:
    return [
        RetrievedSource(
            id=str(item.get("id", "")),
            score=float(item.get("score", 0)),
            title_en=str(item.get("title_en", "")),
            title_bn=str(item.get("title_bn", "")),
            content_en=str(item.get("content_en", "")),
            content_bn=str(item.get("content_bn", "")),
            source=str(item.get("source", "")),
        )
        for item in items
    ]


def build_prompt(query, detected_crop, detected_disease, intent, retrieved_nodes, disease_details=None, history=None):
    context = QueryContext(
        crop=detected_crop,
        disease=detected_disease,
        history=tuple(history or []),
    )
    sources = _sources(retrieved_nodes or [])
    mode, confidence, reason = compute_confidence_gate(retrieved_nodes or [], detected_crop, detected_disease, intent, query)
    if mode == "REFER_EXPERT":
        return (
            "দুঃখিত, এই রোগের নির্দিষ্ট তথ্য আমাদের ডাটাবেসে নেই। সঠিক পরামর্শের জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।",
            mode,
            confidence,
            reason,
            [],
        )
    return GroundedAnswerGenerator._prompt(query, context, sources), mode, confidence, reason, [source.id for source in sources]


def generate_response(query, detected_crop=None, detected_disease=None, intent=None, retrieved_nodes=None, disease_details=None, model=None, history=None):
    container = build_container(settings)
    generator = GroundedAnswerGenerator(container.qa.generator.client)
    sources = _sources(retrieved_nodes or [])
    result = asyncio.run(
        generator.generate(
            query,
            QueryContext(crop=detected_crop, disease=detected_disease, history=tuple(history or [])),
            sources,
        )
    )
    mode, confidence, reason = compute_confidence_gate(retrieved_nodes or [], detected_crop, detected_disease, intent, query)
    return {
        "response": result.answer,
        "grounded": bool(result.used_source_ids),
        "sources": list(result.used_source_ids),
        "gate_mode": mode,
        "confidence": confidence,
        "gate_reason": reason,
        "model_used": result.model,
        "error": result.error,
    }
