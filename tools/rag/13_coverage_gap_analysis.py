"""13 — Coverage-gap analysis (C1): all 1,000 real farmer queries vs the corpus.

Runs the REAL runtime retrieval classes (container wiring: BM25 + BGE-M3 dense
+ RRF fusion + dialect expansion) over EVERY query in farmer_benchmark_1000.jsonl
and buckets each query by retrieval adequacy:

  no_sources  -> 0 passages returned (hard coverage gap)
  thin        -> 1-2 passages returned (soft gap)
  adequate    -> 3+ passages returned (normal retrieval support)

Honesty rules:
- Coverage only. This measures whether the CORPUS contains retrievable text
  for the query — never answer quality or recall (that is the golden set's job).
- A "thin"/"no_sources" bucket means retrieval returned little — the pipeline
  may still refuse cleanly (REFERRAL / D1a gate). The report separates
  corpus gaps from policy refusals.
- BM25-only numbers are recorded alongside hybrid so the report can show how
  much the dense channel rescues (the gap may be in the corpus, not the
  retriever).

Usage (from `backend/`):
    uv run python ml_assets/rag_index/scripts/13_coverage_gap_analysis.py
"""
from __future__ import annotations

import json
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
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
OUT_JSON = RAG_ROOT / "eval" / "coverage_gaps_v1.json"
TOP_K = 5
WORKERS = 8

# Topic keywords for gap clustering (query may hit several groups).
TOPIC_GROUPS: dict[str, tuple[str, ...]] = {
    "ধান (rice)": ("ধান", "ধানের"),
    "আলু (potato)": ("আলু", "আলুর"),
    "মরিচ (chilli)": ("মরিচ", "মরিচের"),
    "টমেটো (tomato)": ("টমেটো", "টমেটোর"),
    "গম/ভুট্টা (wheat/corn)": ("গম", "ভুট্টা", "গমের", "ভুট্টার"),
    "পেঁয়াজ/রসুন (onion/garlic)": ("পেঁয়াজ", "রসুন", "পেঁয়াজের", "রসুনের"),
    "সবজি/শাক (vegetables)": ("বাঁধাকপি", "ফুলকপি", "সরিষা", "লাউ", "শিম", "বেগুন", "মুলা", "শাক", "পালং", "করলা"),
    "ফল (fruit)": ("আম", "কলা", "লেবু", "পেঁপে", "লিচু", "কমলা", "জাম্বুরা", "ফল"),
    "মাছ (fish)": ("মাছ", "মাছের", "পুকুর", "মৎস্য", "চিংড়ি"),
    "গবাদি/হাঁস-মুরগি (livestock)": ("গরু", "ছাগল", "ভেড়া", "মুরগি", "হাঁস", "গবাদি", "দুধ", "ডিম"),
    "সার (fertilizer)": ("সার", "ইউরিয়া", "টিএসপি", "এমওপি", "জৈব সার", "কম্পোস্ট"),
    "কীটনাশক/রোগ (pesticides/disease)": ("কীটনাশক", "ছত্রাকনাশক", "রোগ", "পোকা", "বালাই", "জীবাণু", "ডোজ"),
    "জাত (variety)": ("জাত", "জাতের", "উন্নত জাত"),
    "সেচ/পানি (irrigation)": ("সেচ", "পানি", "সেচের", "জল"),
    "আবহাওয়া (weather)": ("আবহাওয়া", "বৃষ্টি", "তাপমাত্রা", "খরা", "জলবায়ু"),
    "বাজার/অর্থনীতি (market/economics)": ("বাজার", "দাম", "লাভ", "ঋণ", "ভর্তুকি", "সাবসিডি"),
    "সরকারি/পরামর্শ (govt/extension)": ("সরকারি", "উপসহকারী", "কৃষি অফিসার", "কৃষক কল সেন্টার", "১৬১২৩"),
    "মাটি (soil)": ("মাটি", "মাটির", "মৃত্তিকা", "মাটির উর্বরতা"),
}


def topic_of(query: str) -> list[str]:
    return [name for name, keywords in TOPIC_GROUPS.items() if any(k in query for k in keywords)]


def main() -> None:
    settings = Settings()
    queries = []
    with EVAL_QUERIES.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                queries.append({"row_id": row.get("row_id"), "question": row["question"]})
    print(f"queries: {len(queries)}")

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
    print(f"dense available: {dense.available} | warm-up...")
    hybrid.retrieve(queries[0]["question"], top_k=TOP_K)  # warm lazy loads

    lock = threading.Lock()
    records: list[dict] = []
    progress = {"done": 0}

    def run_one(item: dict) -> dict:
        question = item["question"]
        expanded, matched = expander.expand(question)
        bm25_results = bm25.retrieve(expanded, top_k=TOP_K)
        dense_results = dense.retrieve(expanded, top_k=TOP_K)
        hybrid_results = hybrid.retrieve(question, top_k=TOP_K)
        n = len(hybrid_results)
        bucket = "adequate" if n >= 3 else ("thin" if n >= 1 else "no_sources")
        return {
            "row_id": item["row_id"],
            "question": question,
            "bucket": bucket,
            "hybrid_n": n,
            "hybrid_top1_rrf": round(hybrid_results[0].score, 4) if hybrid_results else None,
            "bm25_top1_score": round(bm25_results[0].score, 4) if bm25_results else None,
            "bm25_n": len(bm25_results),
            "dense_top1_cosine": round(dense_results[0].score, 4) if dense_results else None,
            "dense_n": len(dense_results),
            "expansion_matches": matched,
            "top_ids": [s.id for s in hybrid_results[:3]],
            "topics": topic_of(question),
        }

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(run_one, item): item for item in queries}
        for future in as_completed(futures):
            with lock:
                progress["done"] += 1
                records.append(future.result())
                if progress["done"] % 100 == 0:
                    print(f"  {progress['done']}/{len(queries)}")

    buckets = Counter(r["bucket"] for r in records)
    gap_records = [r for r in records if r["bucket"] != "adequate"]
    gap_topics: Counter = Counter()
    for r in gap_records:
        for topic in r["topics"]:
            gap_topics[topic] += 1
    # Queries with no topic keyword matched (uncategorized gaps)
    uncategorized = sum(1 for r in gap_records if not r["topics"])
    # Dense rescue: hybrid non-empty where bm25 was empty
    rescue = sum(1 for r in records if r["bm25_n"] == 0 and r["hybrid_n"] > 0)
    # Raw channel quality signals (thresholds are set in the REPORT, not here —
    # this artifact records evidence, the report interprets it).
    dense_cosines = [r["dense_top1_cosine"] for r in records if r["dense_top1_cosine"] is not None]
    bm25_scores = [r["bm25_top1_score"] for r in records if r["bm25_top1_score"] is not None]

    n = len(records)
    report = {
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "queries_total": n,
        "top_k": TOP_K,
        "dense_available": dense.available,
        "method": "real runtime retrievers (BM25 + BGE-M3 dense + RRF k=20 + dialect expansion); "
                  "per-query raw channel scores recorded; bucket by returned-passage count is a "
                  "term-overlap proxy, NOT relevance (golden set measures relevance)",
        "buckets": {
            "no_sources": {"count": buckets["no_sources"], "rate": round(buckets["no_sources"] / n, 4)},
            "thin": {"count": buckets["thin"], "rate": round(buckets["thin"] / n, 4)},
            "adequate": {"count": buckets["adequate"], "rate": round(buckets["adequate"] / n, 4)},
        },
        "gap_rate_by_count": round((buckets["no_sources"] + buckets["thin"]) / n, 4),
        "dense_rescue": {"bm25_empty_hybrid_found": rescue},
        "channel_signals": {
            "dense_top1_cosine": {
                "min": round(min(dense_cosines), 4) if dense_cosines else None,
                "median": round(sorted(dense_cosines)[len(dense_cosines) // 2], 4) if dense_cosines else None,
                "p10": round(sorted(dense_cosines)[len(dense_cosines) // 10], 4) if len(dense_cosines) >= 10 else None,
                "max": round(max(dense_cosines), 4) if dense_cosines else None,
            },
            "bm25_top1_score": {
                "min": round(min(bm25_scores), 4) if bm25_scores else None,
                "median": round(sorted(bm25_scores)[len(bm25_scores) // 2], 4) if bm25_scores else None,
                "max": round(max(bm25_scores), 4) if bm25_scores else None,
            },
            "bm25_empty_queries": sum(1 for r in records if r["bm25_top1_score"] is None),
            "dense_empty_queries": sum(1 for r in records if r["dense_top1_cosine"] is None),
            "expansion_hit_queries": sum(1 for r in records if r["expansion_matches"]),
        },
        "gap_topics": dict(gap_topics.most_common(20)),
        "uncategorized_gaps": uncategorized,
        "records": records,
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\n=== coverage gap report ===")
    print(f"no_sources : {buckets['no_sources']:4d} ({buckets['no_sources']/n:.1%})")
    print(f"thin       : {buckets['thin']:4d} ({buckets['thin']/n:.1%})")
    print(f"adequate   : {buckets['adequate']:4d} ({buckets['adequate']/n:.1%})")
    print(f"dense rescue (bm25-empty -> hybrid found): {rescue}")
    print(f"bm25 empty : {sum(1 for r in records if r['bm25_top1_score'] is None)}")
    print(f"dense empty: {sum(1 for r in records if r['dense_top1_cosine'] is None)}")
    print(f"expansion hits: {sum(1 for r in records if r['expansion_matches'])}")
    if dense_cosines:
        print(f"dense top1 cosine: median {sorted(dense_cosines)[len(dense_cosines)//2]:.3f}, "
              f"min {min(dense_cosines):.3f}, p10 {sorted(dense_cosines)[len(dense_cosines)//10]:.3f}")
    if bm25_scores:
        print(f"bm25 top1 raw   : median {sorted(bm25_scores)[len(bm25_scores)//2]:.1f}, min {min(bm25_scores):.1f}")
    print(f"\ntop gap topics (by count-bucket gaps):")
    for topic, count in gap_topics.most_common(20):
        print(f"  {count:4d}  {topic}")
    if uncategorized:
        print(f"  + {uncategorized} gap queries with no topic keyword matched")
    print(f"\nsaved: {OUT_JSON}")


if __name__ == "__main__":
    main()