"""Retrieval Agent — BM25 over the precomputed index."""
from __future__ import annotations

import pickle
from pathlib import Path

from app.core.config import settings

_index = None
_corpus = None


def _load():
    global _index, _corpus
    if _index is not None:
        return _index, _corpus
    idx_path = Path(settings.ml_assets_dir) / "rag_index" / "indexes" / "bm25_index.pkl"
    with open(idx_path, "rb") as f:
        data = pickle.load(f)
    if isinstance(data, dict):
        _index = data.get("index", data.get("bm25"))
        _corpus = data.get("docs", data.get("corpus", []))
    else:
        _index = data
        _corpus = []
    if not _corpus:
        corpus_path = Path(settings.ml_assets_dir) / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
        if corpus_path.exists():
            import json
            with open(corpus_path, encoding="utf-8") as f:
                _corpus = [json.loads(line) for line in f]
    return _index, _corpus


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    index, corpus = _load()
    if index is None or not corpus:
        return []
    tokens = _tokenize(query)
    try:
        scores = index.get_scores(tokens)
    except Exception:
        return []
    import numpy as np
    top_idx = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_idx:
        if i >= len(corpus):
            continue
        doc = corpus[i]
        score = float(scores[i])
        if score <= 0:
            continue
        results.append({
            "id": doc.get("id", f"doc_{i}"),
            "score": score,
            "title_en": doc.get("title_en", ""),
            "title_bn": doc.get("title_bn", ""),
            "content_en": doc.get("content_en", ""),
            "content_bn": doc.get("content_bn", ""),
            "source": doc.get("source_document", ""),
            "citation": doc.get("citation", ""),
            "category": doc.get("category", ""),
        })
    return results
