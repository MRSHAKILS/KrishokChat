"""Hybrid retrieval (P3): reciprocal-rank fusion of BM25 + dense channels.

RRF: score(doc) = sum over channels of 1 / (k + rank_in_channel), k=20 per the
manifest's fusion spec. The BM25-only fallback flag (settings.retrieval_bm25_only)
plus automatic fallback whenever the dense channel is unavailable or errors
keep the demo offline-capable. `last_expansion` surfaces the dialect expansion
for the agent trace.
"""
from __future__ import annotations

from pathlib import Path

from app.domain.contracts import RetrievedSource
from app.infrastructure.retrieval.expansion import QueryExpander

RRF_K = 20


class HybridRetriever:
    def __init__(
        self,
        bm25: object,
        dense: object | None = None,
        expander: QueryExpander | None = None,
        k: int = RRF_K,
        candidate_depth: int = 50,
        bm25_only: bool = False,
    ) -> None:
        self.bm25 = bm25
        self.dense = dense
        self.expander = expander or QueryExpander(Path("_nonexistent_term_map"))
        self.k = k
        self.candidate_depth = candidate_depth
        self.bm25_only = bm25_only
        self.mode = "bm25"
        self.last_expansion: tuple[str, str, list[str]] = ("", "", [])

    def _expanded(self, query: str) -> tuple[str, list[str]]:
        if self.expander is None:
            return query, []
        try:
            return self.expander.expand(query)
        except Exception:
            return query, []

    def retrieve(self, query: str, *, top_k: int) -> list[RetrievedSource]:
        expanded, matched = self._expanded(query)
        self.last_expansion = (query, expanded, matched)

        if top_k <= 0:
            return []

        def bm25_only_path() -> list[RetrievedSource]:
            self.mode = "bm25"
            return self.bm25.retrieve(expanded, top_k=top_k)

        dense_ok = (
            not self.bm25_only
            and self.dense is not None
            and getattr(self.dense, "available", False)
        )
        if not dense_ok:
            return bm25_only_path()

        bm25_candidates = self.bm25.candidates(expanded, depth=self.candidate_depth)
        dense_candidates = self.dense.retrieve(expanded, top_k=self.candidate_depth)
        if not dense_candidates:
            return bm25_only_path()

        # RRF fusion, dedup by node id keeping the best fused weight.
        fused: dict[str, tuple[float, RetrievedSource]] = {}
        for rank, source in enumerate(bm25_candidates, start=1):
            weight = 1.0 / (self.k + rank)
            current = fused.get(source.id)
            if current is None or weight > current[0]:
                fused[source.id] = (weight, source)
        for rank, source in enumerate(dense_candidates, start=1):
            weight = 1.0 / (self.k + rank)
            current = fused.get(source.id)
            if current is None or weight > current[0]:
                fused[source.id] = (weight, source)

        ranked = sorted(fused.values(), key=lambda item: item[0], reverse=True)[:top_k]
        self.mode = "hybrid"
        return [
            RetrievedSource(
                id=source.id,
                score=round(weight, 4),
                title_en=source.title_en,
                title_bn=source.title_bn,
                content_en=source.content_en,
                content_bn=source.content_bn,
                source=source.source,
                citation=source.citation,
                metadata=source.metadata,
            )
            for weight, source in ranked
        ]