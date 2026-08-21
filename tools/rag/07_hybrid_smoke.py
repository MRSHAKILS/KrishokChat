"""07 — Honest coverage smoke for hybrid retrieval (P3).

Runs the REAL runtime retriever classes (container wiring) over a sample of
the 1,000 real farmer queries. Reports coverage numbers ONLY:
  - non-empty retrieval rate per channel (never "recall" — there are no
    relevance labels yet; P4's golden set adds those)
  - average top-1 score and sources per query
  - dialect-expansion hit rate and active mode (hybrid vs bm25)
No metric here is a quality claim; it exists to catch regressions and to
prove the fused channel returns passages where BM25 alone returns none.
"""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import Settings
from app.infrastructure.retrieval.bm25 import BM25Retriever
from app.infrastructure.retrieval.dense import DenseRetriever
from app.infrastructure.retrieval.expansion import QueryExpander
from app.infrastructure.retrieval.hybrid import HybridRetriever

RAG_ROOT = Path(__file__).resolve().parent.parent
EVAL_QUERIES = RAG_ROOT / "eval" / "farmer_benchmark_1000.jsonl"
SAMPLE_SIZE = 100
TOP_K = 5


def main() -> None:
    settings = Settings()
    queries = []
    with EVAL_QUERIES.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                queries.append(json.loads(line)["question"])
    sample = random.Random(7).sample(queries, min(SAMPLE_SIZE, len(queries)))
    print(f"sample: {len(sample)} queries from {len(queries)}")

    bm25 = BM25Retriever(
        index_path=settings.rag_index_path / "indexes" / "bm25_index.pkl",
        corpus_path=settings.rag_corpus_path,
    )
    dense = DenseRetriever(
        index_path=settings.rag_dense_faiss_path,
        ids_path=settings.rag_dense_ids_path,
        corpus_path=settings.rag_corpus_path,
        api_key=settings.openrouter_api_key,
    )
    expander = QueryExpander(settings.rag_term_map_path, dialect_map_path=settings.rag_dialect_map_path)
    hybrid = HybridRetriever(bm25, dense=dense, expander=expander)

    print(f"dense available: {dense.available}")

    stats = {"bm25": {"non_empty": 0, "top1_sum": 0.0, "sources_sum": 0}, "hybrid": {"non_empty": 0, "top1_sum": 0.0, "sources_sum": 0}}
    expansions = 0
    hybrid_runs = 0
    for query in sample:
        b_results = bm25.retrieve(query, top_k=TOP_K)
        h_results = hybrid.retrieve(query, top_k=TOP_K)
        if b_results:
            stats["bm25"]["non_empty"] += 1
            stats["bm25"]["top1_sum"] += b_results[0].score
            stats["bm25"]["sources_sum"] += len(b_results)
        if h_results:
            stats["hybrid"]["non_empty"] += 1
            stats["hybrid"]["top1_sum"] += h_results[0].score
            stats["hybrid"]["sources_sum"] += len(h_results)
        if hybrid.last_expansion[2]:
            expansions += 1
        if hybrid.mode == "hybrid":
            hybrid_runs += 1

    n = len(sample)
    report = {
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sample_size": n,
        "dense_available": dense.available,
        "top_k": TOP_K,
        "note": "coverage smoke only — recall/quality judgments arrive with the P4 golden set",
        "bm25": {
            "non_empty_rate": round(stats["bm25"]["non_empty"] / n, 3),
            "avg_top1_score": round(stats["bm25"]["top1_sum"] / n, 3),
            "avg_sources": round(stats["bm25"]["sources_sum"] / n, 3),
        },
        "hybrid": {
            "non_empty_rate": round(stats["hybrid"]["non_empty"] / n, 3),
            "avg_top1_score": round(stats["hybrid"]["top1_sum"] / n, 3),
            "avg_sources": round(stats["hybrid"]["sources_sum"] / n, 3),
        },
        "hybrid_active_rate": round(hybrid_runs / n, 3),
        "expansion_hit_rate": round(expansions / n, 3),
    }
    out = RAG_ROOT / "eval" / "hybrid_smoke.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"saved: {out}")


if __name__ == "__main__":
    main()