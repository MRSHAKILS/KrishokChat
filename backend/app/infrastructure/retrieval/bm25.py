"""Read-only BM25 adapter over the precomputed local corpus."""

from __future__ import annotations

import json
import pickle
import threading
from pathlib import Path

import numpy as np

from app.domain.contracts import RetrievedSource
from app.infrastructure.retrieval.nodes import source_from_node


class BM25Retriever:
    def __init__(self, index_path: Path, corpus_path: Path) -> None:
        self.index_path = index_path
        self.corpus_path = corpus_path
        self._index = None
        self._corpus: list[dict] = []
        self._lock = threading.Lock()

    def _load(self) -> tuple[object | None, list[dict]]:
        if self._index is not None and self._corpus:
            return self._index, self._corpus
        with self._lock:
            if self._index is None:
                with self.index_path.open("rb") as handle:
                    data = pickle.load(handle)
                if isinstance(data, dict):
                    self._index = data.get("bm25", data.get("index"))
                    embedded = data.get("nodes", data.get("corpus", data.get("docs", [])))
                    if isinstance(embedded, list):
                        self._corpus = embedded
                else:
                    self._index = data
            if not self._corpus and self.corpus_path.exists():
                with self.corpus_path.open(encoding="utf-8") as handle:
                    self._corpus = [json.loads(line) for line in handle if line.strip()]
        return self._index, self._corpus

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()

    def _scores(self, query: str) -> np.ndarray | None:
        try:
            index, corpus = self._load()
            if index is None or not corpus:
                return None
            return index.get_scores(self._tokenize(query))
        except (OSError, pickle.PickleError, ValueError, AttributeError, TypeError):
            return None

    def candidates(self, query: str, *, depth: int) -> list[RetrievedSource]:
        """Raw top-`depth` scored documents (no threshold) — the RRF channel
        input. `retrieve` keeps its thresholded behavior unchanged."""
        if depth <= 0:
            return []
        scores = self._scores(query)
        if scores is None or len(scores) == 0:
            return []
        corpus = self._corpus or []
        results: list[RetrievedSource] = []
        for position in np.argsort(scores)[::-1][:depth]:
            index_position = int(position)
            if index_position >= len(corpus):
                continue
            node = corpus[index_position]
            results.append(source_from_node(node, float(scores[index_position])))
        return results

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        if top_k <= 0:
            return []
        scores = self._scores(query)
        if scores is None or len(scores) == 0:
            return []
        corpus = self._corpus or []
        max_score = float(max(scores))
        threshold = max_score * 0.2 if max_score > 0 else 0.0
        results: list[RetrievedSource] = []
        for position in np.argsort(scores)[::-1][: top_k * 2]:
            index_position = int(position)
            if index_position >= len(corpus):
                continue
            score = float(scores[index_position])
            if score <= threshold:
                continue
            node = corpus[index_position]
            results.append(source_from_node(node, score))
            if len(results) == top_k:
                break
        return results
