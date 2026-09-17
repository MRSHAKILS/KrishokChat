#!/usr/bin/env python3
"""N02 token metering on real strings (EACL Final).

Metering set (frozen): PRISM B/C/D/I (400) + F (100) through the frozen offline
pipeline, capturing FULL strings (no truncation):
  - clarification answer text (halted turns)
  - retrieval_query + retrieved source contents (retrieval context)
  - stub generated answer text (T3 turns)
Tokenizer: tiktoken 0.14.0 cl100k_base (disclosed: not the Gemini tokenizer).
Live-API sides report provider-exact usage separately (G5/SMS-live runs).

Outputs (experiments/results/): n02_metering_YYYYMMDD.json
"""
from __future__ import annotations

import asyncio
import json
import math
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

import tiktoken  # noqa: E402

from app.application.qa_pipeline import QAInput  # noqa: E402
from app.domain.enums import ResolutionTier  # noqa: E402

import _qa_harness as H  # noqa: E402

PRISM_PATH = WORKSPACE_ROOT / "research_artifacts" / "datasets" / "prism_benchmark" / "prism_benchmark_1000.jsonl"
OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
CATS = ("B_colloquial_bengali", "C_dialect", "D_banglish", "I_ambiguous_disease", "F_underspecified")
ENC = tiktoken.get_encoding("cl100k_base")


def toks(text: str) -> int:
    return len(ENC.encode(text or ""))


def pct(values: list[int], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    k = (len(ordered) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return round(ordered[lo] + (ordered[hi] - ordered[lo]) * (k - lo), 1)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n02_metering_{stamp}.json"

    with open(PRISM_PATH, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if json.loads(line).get("category") in CATS]
    assert len(rows) == 500, f"expected 500 rows, got {len(rows)}"

    pipeline, _, index_path, corpus_path = H.build_offline_pipeline(audit=H.InMemoryAudit())

    async def run_all():
        out = []
        for idx, row in enumerate(rows):
            res = await pipeline.run(QAInput(query=row["query"]))
            # audited retrieval query: last audit record carries it (see qa_pipeline audit)
            out.append((row, res))
            if (idx + 1) % 100 == 0:
                print(f"[{idx + 1}/{len(rows)}] done", flush=True)
        return out

    pairs = asyncio.run(run_all())

    clar, retctx, gen = [], [], []
    by_tier: dict[str, int] = {}
    for row, res in pairs:
        tier = res.resolution_tier.value
        by_tier[tier] = by_tier.get(tier, 0) + 1
        answer = res.answer or ""
        if res.resolution_tier == ResolutionTier.INTERACTIVE_CLARIFICATION:
            clar.append(toks(answer))
        else:
            ctx_len = sum(toks((s.content_bn or s.content_en or "")) for s in res.sources)
            retctx.append(ctx_len)
            gen.append(toks(answer))

    def summ(values: list[int]) -> dict:
        if not values:
            return {"n": 0}
        return {"n": len(values), "p50": pct(values, 0.5), "p95": pct(values, 0.95),
                "mean": round(statistics.mean(values), 1)}

    results = {
        "benchmark_name": "EACL_N02_TOKEN_METERING_REAL_STRINGS",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"prism": PRISM_PATH}),
        "tokenizer": "tiktoken 0.14.0 cl100k_base (disclosed approximation; live sides use provider-exact usage)",
        "design": {"n": len(rows), "categories": list(CATS), "tiers": by_tier},
        "metered_cl100k": {
            "clarification_answer": summ(clar),
            "retrieval_context": summ(retctx),
            "stub_generated_answer": summ(gen),
        },
        "modeled_vs_metered": {
            "modeled_assumption": {"clarification": 150, "full_generation": 1250, "saving_pct": 88.0},
            "note": "compared in analysis after results land; stub answers stand in for live generation length pending G5 provider-exact counts",
        },
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results["metered_cl100k"], indent=2))
    print(json.dumps(results["design"], indent=2))
    print(f"[OK] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
