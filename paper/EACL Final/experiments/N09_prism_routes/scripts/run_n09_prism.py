#!/usr/bin/env python3
"""N09 PRISM-1000 route-conformance scoring (EACL Final, CPU $0).

Design-conformance (NOT independent accuracy): the generator assigned
expected_route by template arm, so agreement = "live system behaves as
designed across 1000 register-varied queries." See prism_audit.md.

Per row: full frozen offline pipeline (tier for clarify/guard/refusal/fact)
PLUS AdaptiveRetrievalRouter.route for B/C/D distinction, with working memory
seeded from the row's gold fields (tests route SELECTION given context, not
context inference — disclosed).
Outcome mapping: INTERACTIVE_CLARIFICATION->clarification;
DETERMINISTIC_GUARD/HONEST_REFUSAL on J rows->safety_gate;
fact-source->fact_base; else router route (document_rag/concept_hypotheses/
conversational_follow_up).

Outputs: experiments/results/n09_prism_<date>.json (+ .jsonl records).
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

from app.application.adaptive_router import AdaptiveRetrievalRouter  # noqa: E402
from app.application.qa_pipeline import QAInput  # noqa: E402
from app.domain.enums import ResolutionTier  # noqa: E402
from app.domain.working_memory import AgriculturalWorkingMemory  # noqa: E402

import _qa_harness as H  # noqa: E402

PRISM_PATH = WORKSPACE_ROOT / "research_artifacts" / "datasets" / "prism_benchmark" / "prism_benchmark_1000.jsonl"
OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def outcome_of(res, route_enum) -> str:
    t = res.resolution_tier
    if t == ResolutionTier.INTERACTIVE_CLARIFICATION:
        return "clarification"
    if t in (ResolutionTier.DETERMINISTIC_GUARD, ResolutionTier.HONEST_REFUSAL):
        if res.category.value != "safe_agri":
            return "safety_gate"
        return "honest_refusal_other"
    if res.sources and any((getattr(s, "metadata", {}) or {}).get("grounding") == "fact_base"
                           for s in res.sources):
        return "fact_base"
    return {"fact_base": "fact_base", "document_rag": "document_rag",
            "concept_hypotheses": "concept_hypotheses",
            "conversational_follow_up": "conversational_follow_up"}.get(route_enum, route_enum)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n09_prism_{stamp}.json"
    rec_path = OUT_DIR / f"n09_prism_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    prism = [json.loads(l) for l in open(PRISM_PATH, encoding="utf-8")]
    assert len(prism) == 1000, len(prism)
    pipeline, _, _, _ = H.build_offline_pipeline(audit=H.InMemoryAudit())

    async def run_all():
        out = []
        for idx, row in enumerate(prism):
            mem = AgriculturalWorkingMemory(
                crop=row.get("true_crop"), symptom=row.get("true_symptom"),
                temporal_event=row.get("true_temporal_event"))
            decision = AdaptiveRetrievalRouter.route(row["query"], working_memory=mem)
            t0 = time.perf_counter()
            res = await pipeline.run(QAInput(query=row["query"]))
            latency_ms = round((time.perf_counter() - t0) * 1000, 3)
            got = outcome_of(res, decision.route.value)
            append_jsonl(rec_path, {"id": row.get("id"), "category": row.get("category"),
                                    "expected": row.get("expected_route"), "predicted": got,
                                    "router_route": decision.route.value,
                                    "tier": res.resolution_tier.value,
                                    "latency_ms": latency_ms})
            out.append((row.get("expected_route"), got, latency_ms))
            if (idx + 1) % 200 == 0:
                print(f"[{idx + 1}/1000] done", flush=True)
        return out

    scored = asyncio.run(run_all())
    conf: dict[str, Counter] = {}
    lat: dict[str, list] = {}
    for exp, got, latency_ms in scored:
        conf.setdefault(exp, Counter())[got] += 1
        lat.setdefault(exp, []).append(latency_ms)
    agree = sum(c.get(e, 0) for e, c in conf.items())
    per_cat = {}
    for exp, counter in sorted(conf.items()):
        n = sum(counter.values())
        per_cat[exp] = {"n": n, "agree": counter.get(exp, 0),
                        "rate": round(counter.get(exp, 0) / n, 4) if n else None,
                        "predicted_dist": dict(counter)}
    results = {
        "benchmark_name": "EACL_N09_PRISM_ROUTE_CONFORMANCE",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"prism": PRISM_PATH}),
        "design": {"n": 1000, "memory": "seeded from gold fields (tests route selection, not context inference)",
                   "mapping": "pipeline tier for clarify/guard/refusal/fact; router route otherwise",
                   "circularity": "expected_route assigned by generator template arm — conformance, not independent accuracy (see prism_audit.md)"},
        "overall_agreement": round(agree / 1000, 4),
        "per_expected_route": per_cat,
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps({"overall": results["overall_agreement"],
                      "per_route": {k: v["rate"] for k, v in per_cat.items()}}, indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
