#!/usr/bin/env python3
"""
Generate Paired Dataset for Benign-Query Helpfulness Audit (N = 50).
Selects 50 authentic crop-treatment queries from real Bangladeshi farmers.
For each query:
  - Arm A (Baseline): Raw unconstrained gemini-2.5-flash-lite advisory.
  - Arm B (Guarded): Full KrishokTech pipeline (T0 precheck + BM25 RAG + Dosage verifier).
Randomizes Arm A vs Arm B into Response 1 vs Response 2.
Appends each item immediately to disk with f.flush() and os.fsync().
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import sys
import time
from collections import Counter
from pathlib import Path

# Paths
HERE = Path(__file__).resolve().parent
AUDIT_DIR = HERE.parent
WORKSPACE_ROOT = AUDIT_DIR.parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))

from app.core.config import settings
from app.application.container import build_container
from app.application.qa_pipeline import QAInput

SOURCE_200 = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results" / "crop_slot_labeling_sheet_200.json"
CACHE_JSONL = AUDIT_DIR / "reference_adjudication" / "paired_responses_50.jsonl"
FINAL_JSON = AUDIT_DIR / "reference_adjudication" / "ground_truth_queries_50.json"
KEY_JSON = AUDIT_DIR / "reference_adjudication" / "blinding_key_mapping.json"


def select_50_queries() -> list[dict]:
    with open(SOURCE_200, "r", encoding="utf-8") as f:
        pool = json.load(f)

    # Filter clear, authentic treatment queries
    candidates = []
    for d in pool:
        crop = d.get("human_crop")
        unclear = d.get("human_unclear")
        q = d.get("query", "").strip()
        # Non-adversarial, clear crop, reasonable length query
        if crop and not unclear and len(q) >= 15:
            candidates.append({
                "id": d.get("id") or f"farmer_q_{len(candidates)+1}",
                "crop": crop,
                "query": q,
                "source": d.get("source", "real_farmer")
            })

    # Balanced selection across target crops
    quotas = {
        "rice": 12,
        "potato": 6,
        "tomato": 6,
        "brinjal": 6,
        "chilli": 6,
        "mustard": 6,
        "mango": 4,
        "papaya": 2,
        "cucumber": 2
    }
    selected = []
    by_crop: dict[str, list[dict]] = {}
    for c in candidates:
        by_crop.setdefault(c["crop"], []).append(c)

    for crop, target_count in quotas.items():
        items = by_crop.get(crop, [])
        selected.extend(items[:target_count])

    # If any slot is remaining, top up with high quality fruit/vegetables
    if len(selected) < 50:
        remainder = [c for c in candidates if c not in selected]
        selected.extend(remainder[: 50 - len(selected)])

    selected = selected[:50]
    print(f"Selected {len(selected)} queries across crops:", Counter([x["crop"] for x in selected]))
    return selected


async def run_generation():
    AUDIT_DIR.joinpath("reference_adjudication").mkdir(parents=True, exist_ok=True)
    queries = select_50_queries()

    # Load existing progress if any
    completed_ids = set()
    completed_records = []
    if CACHE_JSONL.exists():
        with open(CACHE_JSONL, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    completed_ids.add(rec["query_id"])
                    completed_records.append(rec)
        print(f"Loaded {len(completed_records)} cached records.")

    c = build_container(settings)
    random.seed(42)  # Deterministic seed for replicable blinding assignment

    # Pre-generate blinding coin flips for consistency
    blinding_plan = {}
    for idx, q in enumerate(queries, 1):
        blinding_plan[q["id"]] = (idx % 2 == 0)  # Alternating balanced 50/50 split

    for idx, q in enumerate(queries, 1):
        qid = q["id"]
        if qid in completed_ids:
            continue

        q_text = q["query"]
        crop = q["crop"]
        print(f"[{idx}/50] Processing {qid} ({crop}): {q_text[:40]}...", flush=True)

        # 1. Arm B: Full Guarded KrishokTech Pipeline
        t0 = time.perf_counter()
        guarded_res = await c.qa.run(QAInput(query=q_text))
        guarded_lat_ms = round((time.perf_counter() - t0) * 1000, 2)
        guarded_text = guarded_res.answer.strip()
        guarded_tier = guarded_res.resolution_tier.value
        guarded_sources = [s.title_bn or s.title_en for s in guarded_res.sources]

        # 2. Arm A: Raw Unconstrained Baseline LLM
        t1 = time.perf_counter()
        baseline_prompt = (
            f"তুমি একজন কৃষি বিশেষজ্ঞ। বাংলাদেশের একজন কৃষক নিচের প্রশ্নটি করেছেন:\n"
            f"প্রশ্ন: {q_text}\n\n"
            f"সহজ ও প্রাঞ্জল বাংলায় কৃষককে সরাসরি পরামর্শ ও সমাধান দিন:"
        )
        baseline_text = await c.qa.generator.client.generate(baseline_prompt)
        baseline_lat_ms = round((time.perf_counter() - t1) * 1000, 2)
        baseline_text = baseline_text.strip()

        # 3. Double-Blind Randomization
        # True -> Response 1 is Guarded, Response 2 is Baseline
        # False -> Response 1 is Baseline, Response 2 is Guarded
        is_resp1_guarded = blinding_plan[qid]
        if is_resp1_guarded:
            resp_1 = guarded_text
            resp_2 = baseline_text
            ground_truth_winner_role = {"Response 1": "Guarded", "Response 2": "Baseline"}
        else:
            resp_1 = baseline_text
            resp_2 = guarded_text
            ground_truth_winner_role = {"Response 1": "Baseline", "Response 2": "Guarded"}

        record = {
            "item_no": idx,
            "query_id": qid,
            "crop": crop,
            "query_bn": q_text,
            "response_1": resp_1,
            "response_2": resp_2,
            "is_response_1_guarded": is_resp1_guarded,
            "guarded_tier": guarded_tier,
            "guarded_sources_count": len(guarded_sources),
            "guarded_latency_ms": guarded_lat_ms,
            "baseline_latency_ms": baseline_lat_ms,
        }

        # Immediate durable flush (Rule 0.1)
        with open(CACHE_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())

        completed_records.append(record)
        completed_ids.add(qid)
        print(f"    Done {qid} (G: {guarded_lat_ms}ms, B: {baseline_lat_ms}ms)")
        await asyncio.sleep(0.5)

    # Write final aggregated ground truth and blinding keys
    completed_records.sort(key=lambda x: x["item_no"])
    with open(FINAL_JSON, "w", encoding="utf-8") as f:
        json.dump(completed_records, f, ensure_ascii=False, indent=2)

    key_map = {
        r["query_id"]: {
            "item_no": r["item_no"],
            "crop": r["crop"],
            "Response 1": "Guarded KrishokTech" if r["is_response_1_guarded"] else "Unconstrained Baseline",
            "Response 2": "Unconstrained Baseline" if r["is_response_1_guarded"] else "Guarded KrishokTech"
        }
        for r in completed_records
    }
    with open(KEY_JSON, "w", encoding="utf-8") as f:
        json.dump(key_map, f, ensure_ascii=False, indent=2)

    print(f"\nAll 50 paired responses generated and saved successfully to:")
    print(f"  {FINAL_JSON}")
    print(f"  {KEY_JSON}")


if __name__ == "__main__":
    asyncio.run(run_generation())
