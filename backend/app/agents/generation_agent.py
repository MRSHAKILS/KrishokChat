"""Compatibility shim for the injected grounded generator."""

from __future__ import annotations

import asyncio

from app.application.container import build_container
from app.application.generation import GroundedAnswerGenerator
from app.core.config import settings
from app.domain.contracts import QueryContext, RetrievedSource


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


def generate_answer(query: str, sources: list[dict]) -> dict:
    generator = GroundedAnswerGenerator(build_container(settings).qa.generator.client)
    result = asyncio.run(generator.generate(query, QueryContext(), _sources(sources)))
    return {
        "answer": result.answer,
        "used_source_ids": list(result.used_source_ids),
        "confidence": "verified" if result.used_source_ids else "low_confidence",
        "note": result.error or result.mode,
    }
