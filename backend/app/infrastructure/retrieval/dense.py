"""Dense retrieval channel (P3): FAISS IndexFlatIP over BGE-M3 embeddings.

Passages were embedded offline (scripts/03_build_embeddings_api.py) with the
"passage: " prefix; the query is embedded at request time via the same
OpenRouter endpoint with the "query: " prefix, then L2-normalized (matching
the offline build). Any failure (no key, index missing, API error) returns
[] — the hybrid retriever then falls back to BM25-only, keeping the demo
offline-capable.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

try:
    import faiss  # type: ignore[import-untyped]  # optional: not installed on Render Free
except ImportError:  # pragma: no cover
    faiss = None  # type: ignore[assignment]
import httpx
import numpy as np

from app.domain.contracts import RetrievedSource
from app.infrastructure.retrieval.nodes import source_from_node

EMBEDDING_URL = "https://openrouter.ai/api/v1/embeddings"
DEFAULT_MODEL = "BAAI/bge-m3"


class DenseRetriever:
    def __init__(
        self,
        index_path: Path,
        ids_path: Path,
        corpus_path: Path,
        api_key: str | None = None,
        base_url: str = EMBEDDING_URL,
        model: str = DEFAULT_MODEL,
        timeout: float = 30.0,
    ) -> None:
        self.index_path = index_path
        self.ids_path = ids_path
        self.corpus_path = corpus_path
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self._index = None
        self._ids: list[str] = []
        self._corpus: list[dict] = []
        self._lock = threading.Lock()

    @property
    def available(self) -> bool:
        return (
            faiss is not None
            and bool(self.api_key)
            and self.index_path.exists()
            and self.ids_path.exists()
        )

    def _load(self) -> tuple[object, list[str], list[dict]]:
        if self._index is None or not self._ids or not self._corpus:
            with self._lock:
                if self._index is None:
                    self._index = faiss.read_index(str(self.index_path))
                    self._ids = json.loads(self.ids_path.read_text(encoding="utf-8"))
                    with self.corpus_path.open(encoding="utf-8") as handle:
                        self._corpus = [json.loads(line) for line in handle if line.strip()]
        return self._index, self._ids, self._corpus

    def _embed(self, text: str) -> np.ndarray:
        """Query embedding via OpenRouter (same model/prep as the offline build)."""
        payload = {"model": self.model, "input": ["query: " + text[:2000]]}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()["data"][0]["embedding"]
        vec = np.asarray(data, dtype=np.float32).reshape(1, -1)
        norms = np.linalg.norm(vec, axis=1, keepdims=True)
        return (vec / np.maximum(norms, 1e-9)).astype(np.float32)

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        if top_k <= 0 or not self.available:
            return []
        try:
            index, ids, corpus = self._load()
            vector = self._embed(query)
            scores, positions = index.search(vector, top_k)
        except Exception:
            return []
        results: list[RetrievedSource] = []
        for pos, score in zip(positions[0], scores[0]):
            if pos < 0 or pos >= len(corpus):
                continue
            node = corpus[pos]
            if ids and pos < len(ids):
                node = dict(node, id=ids[pos])
            results.append(source_from_node(node, float(score)))
        return results