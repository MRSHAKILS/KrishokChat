#!/usr/bin/env python3
"""E01 real latency breakdown — offline BM25-only, stub LLM, stage_timer.

Samples 400 Bengali queries from farmer_benchmark_1000.jsonl (seed 42, deterministic),
runs each through the real QAPipeline (BM25Retriever + precheck + HardenedDosageVerifier),
captures per-stage wall-clock ms via telemetry.stage_timer (already used inside the pipeline
and emitted as stage_timings_ms in the audit record).

T3 generation is a stub (0 LLM calls when precheck matches, 1 otherwise) — we report
LLM-excluded system overhead honestly and mark T3 generation as `unmeasured` for the live
llm lane. Tier fractions are from the real resolution_tier emitted per query.

BM25-only: dense retrieval needs OPENROUTER_API_KEY; offline runs self-label as BM25-only.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

# Resolve shared harness (paper-track may import backend offline)
HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[5]
SHARED = REPO_ROOT / "paper" / "EACL Demo" / "experiments" / "shared" / "_qa_harness.py"
if str(SHARED.parent) not in sys.path:
    sys.path.insert(0, str(SHARED.parent))
import _qa_harness as H  # type: ignore[import]

OUT_DIR = HERE.parents[1]
RUNS = 400
SEED = 42

def main() -> int:
    print(f"E01 real latency — {RUNS} queries, BM25-only, stub LLM")
    bench = H.load_farmer_benchmark(n=RUNS, seed=SEED)
    audit = H.InMemoryAudit()
    pipeline, audit_ref, index_path, corpus_path = H.build_offline_pipeline(audit=audit, top_k=5)
    from app.application.qa_pipeline import QAInput

    async def run_all() -> list[dict]:
        results: list[dict] = []
        for row in bench:
            q = row["question"]
            # QAPipeline.run is async
            res = await pipeline.run(QAInput(query=q))
            # last audit record corresponds to this query
            rec = audit.records[-1] if audit.records else {}
            timings = rec.get("stage_timings_ms", {}) if isinstance(rec, dict) else {}
            results.append({
                "row_id": row["row_id"],
                "question": q[:120],
                "tier": rec.get("resolution_tier") if isinstance(rec, dict) else None,
                "category": rec.get("category") if isinstance(rec, dict) else None,
                "stage_timings_ms": timings,
                "retrieval_hit": rec.get("retrieval_hit") if isinstance(rec, dict) else None,
                "llm_calls": rec.get("llm_calls") if isinstance(rec, dict) else None,
            })
        return results

    results = asyncio.run(run_all())

    # Aggregate per-stage
    stage_names = ("safety", "retrieval", "generation", "verifier")
    per_stage: dict[str, list[float]] = {name: [] for name in stage_names}
    tier_counts: dict[str, int] = {}
    llm_free = 0
    for r in results:
        t = r.get("tier")
        if t:
            tier_counts[t] = tier_counts.get(t, 0) + 1
            if t in ("deterministic_guard", "structured_fact", "templated_advisory", "honest_refusal"):
                # T0, T1, T2, T4 are LLM-free in our offline stub (T4 is terminal)
                # For honest framing, T1+T2 is deterministic advisory, T0+T4 is safety/refusal
                llm_free += 1
        st = r.get("stage_timings_ms") or {}
        for name in stage_names:
            v = st.get(name)
            if isinstance(v, (int, float)):
                per_stage[name].append(float(v))

    # Also compute end-to-end (sum of stages per query)
    e2e: list[float] = []
    overhead_no_llm: list[float] = []  # safety+retrieval+verifier (generation stub excluded)
    for r in results:
        st = r.get("stage_timings_ms") or {}
        total = sum(float(st.get(k, 0) or 0) for k in stage_names)
        e2e.append(total)
        overhead = sum(float(st.get(k, 0) or 0) for k in ("safety", "retrieval", "verifier"))
        overhead_no_llm.append(overhead)

    report = {
        "benchmark_name": "EACL_E01_SYSTEM_LATENCY_BREAKDOWN",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"farmer_benchmark_1000.jsonl": H.EVAL_BENCHMARK, "bm25_index.pkl": index_path, "knowledge_nodes_clean.jsonl": corpus_path}),
        "run_config": {"n": RUNS, "seed": SEED, "retrieval": "BM25-only (dense needs OPENROUTER_API_KEY)", "llm": "offline StubLLM (generation is stub, ~0ms; system_overhead excludes generation)", "top_k": 5},
        "tier_distribution": tier_counts,
        "tier_fractions": {k: round(v / len(results), 4) for k, v in tier_counts.items()} if results else {},
        "per_stage_ms": {k: H.percentiles(v) for k, v in per_stage.items()},
        "end_to_end_ms": H.percentiles(e2e),
        "system_overhead_ms": H.percentiles(overhead_no_llm),
        "system_overhead_note": "safety+retrieval+verifier only; generation is stub LLM and is NOT end-to-end. T3 live generation remains `unmeasured` until llama-server is available.",
        "n_queries": len(results),
        "sample": results[:20],
    }
    # Write
    out_json = OUT_DIR / "results_real_latency.json"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        import yaml
        (OUT_DIR / "results_real_latency.yaml").write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True), encoding="utf-8")
    except Exception:
        pass
    print(f"[OK] wrote {out_json} — tiers {tier_counts} — e2e p50 {report['end_to_end_ms']['p50']}ms overhead p50 {report['system_overhead_ms']['p50']}ms")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
