"""12 — Probe raw retrieval scores on the 46 golden queries.

Research for the abstention gate (P4 follow-up): RRF fusion scores are
quantized (1/(k+rank) steps), so a top1 RRF threshold cannot separate
unanswerable from answerable queries. This probe records the CONTINUOUS
per-channel signals — dense cosine (IndexFlatIP) and BM25 raw score — for
each golden query, so a threshold design can be grounded in data.

Cost: 46 OpenRouter embedding calls (one per query), ~pennies. BM25 is local.
Read-only; writes `ml_assets/rag_index/eval/golden_retrieval_probe.json`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import settings  # noqa: E402
from app.infrastructure.retrieval.bm25 import BM25Retriever  # noqa: E402
from app.infrastructure.retrieval.dense import DenseRetriever  # noqa: E402

GOLDEN = BACKEND_ROOT.parent / "dataset_release" / "benchmark" / "golden_qa_v1.jsonl"
OUT = BACKEND_ROOT / "ml_assets" / "rag_index" / "eval" / "golden_retrieval_probe.json"


def main() -> None:
    rows = [json.loads(line) for line in GOLDEN.read_text(encoding="utf-8").splitlines() if line.strip()]
    dense = DenseRetriever(
        index_path=settings.rag_dense_faiss_path,
        ids_path=settings.rag_dense_ids_path,
        corpus_path=settings.rag_corpus_path,
        api_key=settings.openrouter_api_key,
    )
    bm25 = BM25Retriever(
        index_path=settings.rag_index_path / "indexes" / "bm25_index.pkl",
        corpus_path=settings.rag_corpus_path,
    )
    if not dense.available:
        raise SystemExit("dense channel unavailable — key/index missing; study cannot run")

    probe = []
    for i, row in enumerate(rows, 1):
        q = row["question"]
        d_top = dense.retrieve(q, top_k=1)
        b_top = bm25.retrieve(q, top_k=1)
        probe.append({
            "row_id": row["row_id"],
            "category": row["golden_category"],
            "dense_top1_sim": round(d_top[0].score, 4) if d_top else None,
            "dense_top1_id": d_top[0].id if d_top else None,
            "bm25_top1_score": round(b_top[0].score, 4) if b_top else None,
            "bm25_top1_id": b_top[0].id if b_top else None,
        })
        print(f"[{i}/{len(rows)}] {row['row_id']} dense={probe[-1]['dense_top1_sim']} bm25={probe[-1]['bm25_top1_score']}")

    OUT.write_text(json.dumps(probe, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()