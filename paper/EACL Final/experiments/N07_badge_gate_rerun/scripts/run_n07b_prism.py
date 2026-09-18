#!/usr/bin/env python3
"""N07b badge-gate expansion on PRISM mapped rows (EACL Final, CPU $0).

Same user-path measurement as N07 (QAInput(query, crop=*) cross-modal halt),
but on PRISM B/C/D/I rows (400, all with true_crop): mismatch arm
(crop=rotated-different) + matched control arm (crop=gold).
Combined with N07 farmer pairs in analysis (54 + 400).

Outputs: experiments/results/n07b_prism_<date>.json (+ .jsonl records).
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

from app.application.qa_pipeline import QAInput  # noqa: E402
from app.domain.enums import ResolutionTier  # noqa: E402

import _qa_harness as H  # noqa: E402

OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
PRISM_PATH = WORKSPACE_ROOT / "research_artifacts" / "datasets" / "prism_benchmark" / "prism_benchmark_1000.jsonl"
CATS = ("B_colloquial_bengali", "C_dialect", "D_banglish", "I_ambiguous_disease")


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n07b_prism_{stamp}.json"
    rec_path = OUT_DIR / f"n07b_prism_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    prism = [json.loads(l) for l in open(PRISM_PATH, encoding="utf-8")]
    rows = [r for r in prism if r.get("category") in CATS]
    assert len(rows) == 400, len(rows)
    pipeline, _, _, _ = H.build_offline_pipeline(audit=H.InMemoryAudit())

    async def run_all():
        out = []
        for idx, row in enumerate(rows):
            gold = row["true_crop"]
            # deterministic rotation: next crop alphabetically (guaranteed different)
            crops = ["brinjal", "chilli", "maize", "potato", "rice", "tomato", "wheat"]
            wrong = crops[(crops.index(gold) + 1) % len(crops)] if gold in crops else "rice"
            for arm, crop in (("mismatch", wrong), ("control", gold)):
                t0 = time.perf_counter()
                res = await pipeline.run(QAInput(query=row["query"], crop=crop))
                latency_ms = round((time.perf_counter() - t0) * 1000, 3)
                halted = (res.resolution_tier == ResolutionTier.INTERACTIVE_CLARIFICATION
                          and len(res.sources) == 0)
                out.append({"id": row.get("id"), "arm": arm, "gold": gold,
                            "crop_arg": crop, "halted": halted,
                            "tier": res.resolution_tier.value,
                            "n_sources": len(res.sources), "latency_ms": latency_ms})
            if (idx + 1) % 100 == 0:
                print(f"[{idx + 1}/{len(rows)}] done", flush=True)
        return out

    recs = asyncio.run(run_all())
    for r in recs:
        append_jsonl(rec_path, r)
    mm = [r for r in recs if r["arm"] == "mismatch"]
    ct = [r for r in recs if r["arm"] == "control"]
    mh = sum(1 for r in mm if r["halted"])
    ch = sum(1 for r in ct if r["halted"])

    def wilson(k, n):
        import math
        if n == 0:
            return [0.0, 0.0]
        z, p = 1.95996, k / n
        d = 1 + z * z / n
        c = (p + z * z / (2 * n)) / d
        m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
        return [round(max(0.0, c - m) * 100, 2), round(min(1.0, c + m) * 100, 2)]

    results = {
        "benchmark_name": "EACL_N07B_BADGE_PRISM",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"prism": PRISM_PATH}),
        "design": {"n_pairs": len(rows), "arms": ["mismatch", "control"],
                   "mismatch_rule": "next-crop-alphabetical rotation (deterministic, always different)",
                   "path": "QAInput cross-modal halt (same as N07)"},
        "mismatch_halt_rate": round(mh / len(mm), 4),
        "mismatch_ci95": wilson(mh, len(mm)),
        "control_false_halt_rate": round(ch / len(ct), 4),
        "control_ci95": wilson(ch, len(ct)),
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results, indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
