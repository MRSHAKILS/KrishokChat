"""Smoke conversion of scripts/test_bm25_retrieval.py (kept as-is).

Modernized to load the precomputed BM25 index through the functional
infrastructure layer (app.infrastructure.retrieval.bm25.BM25Retriever) and
assert the same disease-treatment queries the smoke script exercised still
return sources. Fully offline — CI loads the index from disk (tracked in git).

Deterministic asserts only: every corpus query must return at least one
source with a positive score; scores must come back sorted descending.
"""

from __future__ import annotations

from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parent.parent
INDEX = BACKEND / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl"
CORPUS = BACKEND / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"

DISEASE_QUERIES = [
    "wheat black point disease treatment",
    "fusarium foot rot wheat",
    "cauliflower bacterial soft rot",
    "potato late blight treatment",
    "rice blast disease",
    "brassica downy mildew",
    "corn common rust",
]


@pytest.fixture(scope="module")
def retriever():
    if not INDEX.exists() or not CORPUS.exists():
        pytest.skip("precomputed BM25 index not present in ml_assets/rag_index")
    from app.infrastructure.retrieval.bm25 import BM25Retriever

    return BM25Retriever(index_path=INDEX, corpus_path=CORPUS)


class TestSmokeBM25Retrieval:
    def test_all_disease_queries_return_sources(self, retriever) -> None:
        for query in DISEASE_QUERIES:
            sources = retriever.retrieve(query, top_k=3)
            assert sources, f"no sources for '{query}'"
            assert all(s.score > 0 for s in sources), f"non-positive score for '{query}'"

    def test_results_sorted_descending_by_score(self, retriever) -> None:
        sources = retriever.retrieve("rice blast disease", top_k=5)
        assert sources
        scores = [s.score for s in sources]
        assert scores == sorted(scores, reverse=True)

    def test_off_corpus_english_query_returns_empty(self, retriever) -> None:
        sources = retriever.retrieve("zzzqqx nonexistent token", top_k=3)
        assert sources == []