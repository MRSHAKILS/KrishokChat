from __future__ import annotations

import json
import pickle
import tempfile
import unittest
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

from app.domain.contracts import RetrievedSource
from app.infrastructure.retrieval.bm25 import BM25Retriever
from app.infrastructure.retrieval.dense import DenseRetriever
from app.infrastructure.retrieval.expansion import QueryExpander
from app.infrastructure.retrieval.hybrid import HybridRetriever


def make_bm25(tmp: Path, nodes: list[dict]) -> BM25Retriever:
    index_path = tmp / "bm25.pkl"
    corpus_path = tmp / "corpus.jsonl"
    corpus_path.write_text(
        "\n".join(json.dumps(n, ensure_ascii=False) for n in nodes) + "\n",
        encoding="utf-8",
    )
    bm25 = BM25Okapi([n["bm25_text"].lower().split() for n in nodes])
    with index_path.open("wb") as handle:
        pickle.dump({"bm25": bm25, "nodes": nodes}, handle)
    return BM25Retriever(index_path, corpus_path)


def node(nid: str, text: str, score: float) -> dict:
    return {"id": nid, "bm25_text": text, "content_bn": text, "score": score, "source": "test"}


class FakeDense:
    def __init__(self, sources: list[RetrievedSource], available: bool = True, fail: bool = False) -> None:
        self.sources = sources
        self.available = available
        self.fail = fail
        self.calls = 0
        self.last_query = ""

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        self.calls += 1
        self.last_query = query
        if self.fail:
            raise RuntimeError("dense channel down")
        return self.sources[:top_k]


def source(nid: str, text: str, score: float) -> RetrievedSource:
    return RetrievedSource(id=nid, content_bn=text, score=score, source="test")


class BM25CandidatesTests(unittest.TestCase):
    def test_candidates_keep_zero_idf_matches_that_retrieve_drops(self) -> None:
        # "rice" appears in 2 of 3 docs -> idf 0 -> BM25 scores are 0 and the
        # 0.2*max threshold drops everything in `retrieve`; `candidates` (the
        # RRF channel input) keeps them for rank fusion.
        with tempfile.TemporaryDirectory() as tmp:
            bm25 = make_bm25(
                Path(tmp),
                [
                    node("A", "rice rice rice rice rice rice rice rice rice rice", 0.0),
                    node("B", "rice", 0.0),
                    node("C", "wheat wheat wheat", 0.0),
                ],
            )
            retrieved = bm25.retrieve("rice", top_k=3)
            candidates = bm25.candidates("rice", depth=3)
            self.assertEqual(retrieved, [])
            # Zero-idf matches survive as RRF candidates even though the
            # thresholded `retrieve` drops them.
            self.assertLessEqual({"A", "B"}, {r.id for r in candidates})


class QueryExpanderTests(unittest.TestCase):
    def _expander(self, tmp: Path) -> QueryExpander:
        term_path = tmp / "term_map.json"
        term_path.write_text(
            json.dumps({"map": [{"bn": "ধান", "en": "Rice"}, {"bn": "ম্যানকোজেব", "en": "Mancozeb"}]}, ensure_ascii=False),
            encoding="utf-8",
        )
        return QueryExpander(term_path, dialect_map_path=None)

    def test_expand_appends_english_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expander = self._expander(Path(tmp))
            expanded, matched = expander.expand("ধান গাছে ম্যানকোজেব কত মিলি দিতে হবে?")
            self.assertIn("Rice", expanded)
            self.assertIn("Mancozeb", expanded)
            self.assertEqual(len(matched), 2)
            self.assertTrue(matched[0].startswith("ধান→") or matched[1].startswith("ধান→"))

    def test_no_match_returns_query_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expander = self._expander(Path(tmp))
            expanded, matched = expander.expand("how to irrigate wheat")
            self.assertEqual(expanded, "how to irrigate wheat")
            self.assertEqual(matched, [])

    def test_missing_map_is_graceful(self) -> None:
        expander = QueryExpander(Path("_missing_term_map"), dialect_map_path=None)
        expanded, matched = expander.expand("ধান চাষ")
        self.assertEqual(expanded, "ধান চাষ")
        self.assertEqual(matched, [])


class HybridRetrieverTests(unittest.TestCase):
    def _hybrid(self, tmp: Path, bm25: BM25Retriever, dense: FakeDense | None = None, bm25_only: bool = False) -> HybridRetriever:
        expander = QueryExpander(tmp / "term_map.json", dialect_map_path=None)
        return HybridRetriever(bm25, dense=dense, expander=expander, k=20, candidate_depth=10, bm25_only=bm25_only)

    def test_rrf_merges_both_channels_and_dedups(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # "disease" has df=1 (only in A) so BM25 ranks A first; "blast" is
            # rescued by the dense channel (B, D) — exactly the fusion case.
            bm25 = make_bm25(
                tmp_path,
                [node("A", "rice disease leaf", 0.0), node("B", "rice blast", 0.0), node("C", "wheat", 0.0)],
            )
            dense = FakeDense([source("B", "rice blast", 0.9), source("D", "leaf blast", 0.7)])
            hybrid = self._hybrid(tmp_path, bm25, dense)
            results = hybrid.retrieve("rice disease", top_k=3)
            ids = [r.id for r in results]
            self.assertEqual(len(ids), 3)
            # Dedup: B appears in both channels but once in results.
            self.assertEqual(len(set(ids)), 3)
            self.assertIn("A", ids)
            self.assertIn("B", ids)
            self.assertIn("D", ids)
            # RRF scores are fusion weights, strictly decreasing.
            self.assertTrue(results[0].score >= results[-1].score)
            self.assertEqual(hybrid.mode, "hybrid")

    def test_bm25_only_flag_never_calls_dense(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bm25 = make_bm25(tmp_path, [node("A", "rice leaf", 0.0), node("B", "wheat", 0.0), node("C", "barley", 0.0)])
            dense = FakeDense([source("A", "rice leaf", 0.9)])
            hybrid = self._hybrid(tmp_path, bm25, dense, bm25_only=True)
            results = hybrid.retrieve("rice", top_k=5)
            self.assertEqual(dense.calls, 0)
            self.assertEqual([r.id for r in results], ["A"])
            self.assertEqual(hybrid.mode, "bm25")

    def test_dense_unavailable_falls_back_to_bm25(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bm25 = make_bm25(tmp_path, [node("A", "rice leaf", 0.0), node("B", "wheat", 0.0), node("C", "barley", 0.0)])
            dense = FakeDense([], available=False)
            hybrid = self._hybrid(tmp_path, bm25, dense)
            results = hybrid.retrieve("rice", top_k=5)
            self.assertEqual([r.id for r in results], ["A"])
            self.assertEqual(hybrid.mode, "bm25")
            self.assertEqual(dense.calls, 0)

    def test_dense_empty_result_falls_back_to_bm25(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bm25 = make_bm25(tmp_path, [node("A", "rice leaf", 0.0), node("B", "wheat", 0.0), node("C", "barley", 0.0)])
            dense = FakeDense([], available=True)
            hybrid = self._hybrid(tmp_path, bm25, dense)
            results = hybrid.retrieve("rice", top_k=5)
            self.assertEqual([r.id for r in results], ["A"])
            self.assertEqual(hybrid.mode, "bm25")

    def test_expansion_is_applied_to_both_channels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            term_path = tmp_path / "term_map.json"
            term_path.write_text(
                json.dumps({"map": [{"bn": "ধান", "en": "Rice"}]}, ensure_ascii=False),
                encoding="utf-8",
            )
            bm25 = make_bm25(tmp_path, [node("A", "rice leaf", 0.0), node("B", "wheat", 0.0), node("C", "barley", 0.0)])
            dense = FakeDense([source("A", "rice leaf", 0.9)])
            hybrid = HybridRetriever(bm25, dense=dense, expander=QueryExpander(term_path), k=20, candidate_depth=10)
            hybrid.retrieve("ধান গাছে রোগ", top_k=3)
            self.assertIn("Rice", dense.last_query)
            self.assertEqual(hybrid.last_expansion[0], "ধান গাছে রোগ")
            self.assertEqual(hybrid.last_expansion[2], ["ধান→Rice"])

    def test_no_match_expansion_surfaces_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bm25 = make_bm25(tmp_path, [node("A", "rice leaf", 0.0), node("B", "wheat", 0.0), node("C", "barley", 0.0)])
            hybrid = HybridRetriever(bm25, dense=None, expander=QueryExpander(tmp_path / "term_map.json"))
            hybrid.retrieve("how to farm", top_k=3)
            self.assertEqual(hybrid.last_expansion[2], [])


class DenseIndexLoadTests(unittest.TestCase):
    """Offline FAISS load check against the real built index (no API calls)."""

    @unittest.skipUnless(
        Path("ml_assets/rag_index/indexes/nodes.faiss").exists(),
        "dense index not built — run scripts/03/05/06 first",
    )
    def test_real_index_loads_with_expected_size(self) -> None:
        retriever = DenseRetriever(
            index_path=Path("ml_assets/rag_index/indexes/nodes.faiss"),
            ids_path=Path("ml_assets/rag_index/indexes/node_ids.json"),
            corpus_path=Path("ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl"),
            api_key=None,
        )
        # No key -> unavailable -> retrieve short-circuits without any API call.
        self.assertFalse(retriever.available)
        index, ids, corpus = retriever._load()
        self.assertEqual(index.ntotal, 2135)
        self.assertEqual(len(ids), 2135)
        self.assertEqual(len(corpus), 2135)
        self.assertEqual(retriever.retrieve("ধান গাছে রোগ", top_k=3), [])


if __name__ == "__main__":
    unittest.main()