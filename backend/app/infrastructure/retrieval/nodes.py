"""Shared node -> RetrievedSource mapping used by every retrieval channel.

Keeps the exact field mapping BM25 already produced; dense and hybrid reuse it
so source metadata is identical across channels.
"""
from __future__ import annotations

from app.domain.contracts import RetrievedSource


def source_from_node(node: dict, score: float) -> RetrievedSource:
    return RetrievedSource(
        id=str(node.get("id", "")),
        score=score,
        title_en=str(node.get("title_en", "")),
        title_bn=str(node.get("title_bn", "")),
        content_en=str(node.get("content_en", "")),
        content_bn=str(node.get("content_bn", "")),
        source=str(node.get("source_document", node.get("source", ""))),
        citation=str(node.get("citation", "")),
        metadata={
            "category": node.get("category", ""),
            "tags": node.get("tags", []),
            "title_en": node.get("title_en", ""),
            "title_bn": node.get("title_bn", ""),
            "section_title": node.get("section_title", ""),
            "publisher": node.get("publisher", ""),
            "citation": node.get("citation", ""),
            "summary": node.get("summary", ""),
            "treatment_summary_bn": node.get("treatment_summary_bn", ""),
            "prevention_bn": node.get("prevention_bn", ""),
        },
    )