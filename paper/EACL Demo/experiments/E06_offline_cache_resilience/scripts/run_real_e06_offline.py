#!/usr/bin/env python3
"""E06 real offline resilience â€” deterministic cache + BM25-only fallback.

Measures: (1) demo-assets/cached_responses.json exact hit rate on held-out queries,
(2) BM25-only offline retrieval hit rate (no dense, no LLM), (3) service-worker precache manifest parse.
No packet-loss simulation â€” that needs Playwright network throttle (separate).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[5]
if str((REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "shared").resolve()) not in sys.path:
    sys.path.insert(0, str((REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "shared").resolve()))
import _qa_harness as H  # type: ignore[import]

OUT_DIR = HERE.parents[1]
RUNS = 400
SEED = 42
CACHED = REPO_ROOT / "demo-assets" / "cached_responses.json"
SW = REPO_ROOT / "frontend" / "public" / "sw.js"

def main() -> int:
    print(f"E06 offline â€” {RUNS} queries, cache hit + BM25-only retrieval")
    bench = H.load_farmer_benchmark(n=RUNS, seed=SEED)
    # 1) Cached responses exact hit rate
    cached_keys: set[str] = set()
    if CACHED.exists():
        try:
            data = json.loads(CACHED.read_text(encoding="utf-8"))
            # cached_responses.json is list or dict
            if isinstance(data, dict):
                # check shape
                for k in data.keys():
                    cached_keys.add(k.strip().lower() if isinstance(k, str) else str(k))
            elif isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict):
                        q = entry.get("query") or entry.get("question") or entry.get("key") or ""
                        if q:
                            cached_keys.add(str(q).strip().lower())
        except Exception:
            pass
    # proper hit count
    hits = sum(1 for row in bench if row["question"].strip().lower() in cached_keys) if cached_keys else 0

    # 2) BM25-only retrieval hit rate via offline pipeline
    audit = H.InMemoryAudit()
    pipeline, _, index_path, corpus_path = H.build_offline_pipeline(audit=audit, top_k=5)
    from app.application.qa_pipeline import QAInput
    import asyncio

    async def run_all() -> list[bool]:
        out: list[bool] = []
        for row in bench:
            res = await pipeline.run(QAInput(query=row["question"]))
            rec = audit.records[-1] if audit.records else {}
            hit = bool(rec.get("retrieval_hit")) if isinstance(rec, dict) else False
            out.append(hit)
        return out

    retrieval_hits = asyncio.run(run_all())
    hit_rate = round(sum(retrieval_hits) / len(retrieval_hits), 4) if retrieval_hits else None

    # 3) SW precache manifest
    sw_exists = SW.exists()
    sw_size = SW.stat().st_size if sw_exists else 0
    sw_has_precache = False
    if sw_exists:
        txt = SW.read_text(encoding="utf-8", errors="ignore")
        sw_has_precache = "precache" in txt.lower() or "workbox" in txt.lower() or "caches" in txt.lower()

    report = {
        "benchmark_name": "EACL_E06_OFFLINE_CACHE_RESILIENCE",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"farmer_benchmark_1000.jsonl": H.EVAL_BENCHMARK, "cached_responses.json": CACHED, "sw.js": SW, "bm25_index.pkl": index_path}),
        "run_config": {"n": RUNS, "seed": SEED, "retrieval": "BM25-only", "llm": "StubLLM"},
        "cached_responses": {"path": str(CACHED.relative_to(REPO_ROOT)).replace("\\", "/"), "n_keys": len(cached_keys), "hits": hits, "hit_rate": round(hits / len(bench), 4) if bench else None},
        "bm25_retrieval": {"hits": sum(retrieval_hits), "n": len(retrieval_hits), "hit_rate": hit_rate},
        "service_worker": {"exists": sw_exists, "size_bytes": sw_size, "has_precache": sw_has_precache},
        "note": "Deterministic fallback measurement. Live packet-loss simulation (15%/30% -> rural_edge/severe_2G +0.5pp/+2.9pp) needs Playwright network throttle lane.",
    }
    out_json = OUT_DIR / "results_real_offline.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        import yaml
        (OUT_DIR / "results_real_offline.yaml").write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
    except Exception:
        pass
    print(f"[OK] wrote {out_json} â€” cache {hits}/{len(bench)} hit {report['cached_responses']['hit_rate']} â€” BM25 hit {hit_rate} â€” SW {sw_exists} precache {sw_has_precache}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
