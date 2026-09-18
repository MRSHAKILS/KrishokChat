#!/usr/bin/env python3
"""N07 badge-gate measurement on the user-facing cross-modal path (EACL Final, CPU $0).

Design (local, deterministic, no CEA dependency): 100 real labeled farmer
queries x mismatched image-crop labels through QAInput(query, crop=B) on the
frozen offline pipeline. Expectation: cross-modal clarification halt.
Control: same 100 queries with crop=gold (expect NO halt).
The halt measured here IS the S3 badge path (qa_pipeline cross-modal check).

Outputs: experiments/results/n07_badge_<date>.json (+ .jsonl records).
"""
from __future__ import annotations

import asyncio
import json
import os
import random
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
SHEET_PATH = OUT_DIR / "crop_slot_labeling_sheet_200.json"
CROPS = ["rice", "potato", "tomato", "brinjal", "chilli", "wheat", "maize"]


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n07_badge_{stamp}.json"
    rec_path = OUT_DIR / f"n07_badge_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    sheet = json.loads(SHEET_PATH.read_text(encoding="utf-8"))
    pool = [r for r in sheet if (r.get("human_crop") or None) in CROPS
            and not r.get("human_unclear")]
    rnd = random.Random(42)
    rows = rnd.sample(pool, min(100, len(pool)))
    # mismatched crop: deterministic rotation to a different crop
    pairs = []
    for r in rows:
        gold = r["human_crop"]
        others = [c for c in CROPS if c != gold]
        pairs.append((r, gold, others[rnd.randrange(len(others))]))

    pipeline, _, _, _ = H.build_offline_pipeline(audit=H.InMemoryAudit())

    async def run_all():
        out = []
        for row, gold, wrong in pairs:
            for arm, crop in (("mismatch", wrong), ("control", gold)):
                t0 = time.perf_counter()
                res = await pipeline.run(QAInput(query=row["query"], crop=crop))
                latency_ms = round((time.perf_counter() - t0) * 1000, 3)
                halted = (res.resolution_tier == ResolutionTier.INTERACTIVE_CLARIFICATION
                          and len(res.sources) == 0)
                out.append({"id": row["id"], "arm": arm, "gold": gold, "crop_arg": crop,
                            "halted": halted, "tier": res.resolution_tier.value,
                            "n_sources": len(res.sources), "latency_ms": latency_ms})
        return out

    recs = asyncio.run(run_all())
    for r in recs:
        append_jsonl(rec_path, r)
    mm = [r for r in recs if r["arm"] == "mismatch"]
    ct = [r for r in recs if r["arm"] == "control"]
    mh = sum(1 for r in mm if r["halted"])
    ch = sum(1 for r in ct if r["halted"])
    results = {
        "benchmark_name": "EACL_N07_BADGE_GATE_USER_PATH",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"sheet": SHEET_PATH}),
        "design": {"n_pairs": len(pairs), "arms": ["mismatch", "control"],
                   "path": "QAInput(query, crop=*) cross-modal check (S3 badge path)"},
        "mismatch_halt_rate": round(mh / len(mm), 4) if mm else None,
        "mismatch_n": len(mm),
        "control_false_halt_rate": round(ch / len(ct), 4) if ct else None,
        "control_n": len(ct),
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results, indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
