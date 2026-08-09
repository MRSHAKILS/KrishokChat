"""Compatibility shim for the read-only BM25 adapter."""

from __future__ import annotations

from app.core.config import settings
from app.infrastructure.retrieval.bm25 import BM25Retriever


_retriever = BM25Retriever(
    settings.rag_index_path / "indexes" / "bm25_index.pkl",
    settings.rag_index_path / "processed" / "knowledge_nodes_clean.jsonl",
)


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    return [
        {
            "id": item.id,
            "score": item.score,
            "title_en": item.title_en,
            "title_bn": item.title_bn,
            "content_en": item.content_en,
            "content_bn": item.content_bn,
            "source": item.source,
            "citation": item.citation,
            "category": item.metadata.get("category", ""),
            "tags": item.metadata.get("tags", []),
        }
        for item in _retriever.retrieve(query, top_k=top_k)
    ]
