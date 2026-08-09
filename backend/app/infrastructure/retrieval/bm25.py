"""Read-only BM25 adapter over the precomputed local corpus."""

from __future__ import annotations

import json
import pickle
import threading
from pathlib import Path

import numpy as np

from app.domain.contracts import RetrievedSource


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

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        if top_k <= 0:
            return []
        try:
            index, corpus = self._load()
            if index is None or not corpus:
                return []
            scores = index.get_scores(self._tokenize(query))
        except (OSError, pickle.PickleError, ValueError, AttributeError, TypeError):
            return []

        if len(scores) == 0:
            return []
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
            results.append(
                RetrievedSource(
                    id=str(node.get("id", f"doc_{index_position}")),
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
            )
            if len(results) == top_k:
                break
        return results
