#!/usr/bin/env python3
"""N01b hazard delta on team-labeled real farmer queries (EACL Final).

Same frozen recipe as N01a (pipeline-identical blind construction, crop_map_v1,
top-5, McNemar + Wilson) applied to 200 real farmer queries with team crop labels:
  - hazard stratum: human_crop in the 9-crop source-mapping space, unclear=false
  - behavior stratum: all 200 rows (halt/pass/refuse rates by tier)
  - extractor audit: extractor crop vs team crop (agreement + false-positive list)

Freeze: gate0 v5 (this file's header) + REAL_DATA_DOCTRINE. $0 API (offline only).
Outputs: experiments/results/n01b_farmer_YYYYMMDD.json (+ .jsonl records).
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
sys.path.insert(0, str(HERE.parent))

from app.application.qa_pipeline import QAInput  # noqa: E402
from app.infrastructure.retrieval.bm25 import BM25Retriever  # noqa: E402

import _qa_harness as H  # noqa: E402
from run_n01_blind_arm import (  # noqa: E402
    TOP_K,
    blind_retrieve,
    mcnemar_exact,
    source_crops,
    wilson,
)

SHEET_PATH = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results" / "crop_slot_labeling_sheet_200.json"
INDEX_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl"
CORPUS_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
MAPPED_CROPS = {"rice", "potato", "tomato", "brinjal", "chilli", "wheat", "maize", "cabbage", "cauliflower"}


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    records_path = OUT_DIR / f"n01b_records_{stamp}.jsonl"
    results_path = OUT_DIR / f"n01b_farmer_{stamp}.json"
    if records_path.exists():
        records_path.unlink()

    sheet = json.loads(SHEET_PATH.read_text(encoding="utf-8"))
    assert len(sheet) == 200, len(sheet)
    assert all(r.get("labeler") for r in sheet), "sheet not labeled yet"
    # extractor audit reads the POSTFIX column (current code); pre-fix column kept for history
    for r in sheet:
        r["_ext_now"] = r.get("extractor_crop_postfix", r.get("extractor_crop"))

    retriever = BM25Retriever(INDEX_PATH, CORPUS_PATH)
    pipeline, _, _, _ = H.build_offline_pipeline(audit=H.InMemoryAudit())
    safety = H.DeterministicSafety()

    async def run_all():
        out = []
        for idx, row in enumerate(sheet):
            q = row["query"]
            blind = await blind_retrieve(q, retriever, safety)
            t0 = time.perf_counter()
            res = await pipeline.run(QAInput(query=q))
            latency_ms = round((time.perf_counter() - t0) * 1000, 3)
            out.append((row, blind, res, latency_ms))
            if (idx + 1) % 50 == 0:
                print(f"[{idx + 1}/{len(sheet)}] done", flush=True)
        return out

    rows = asyncio.run(run_all())

    # hazard stratum + behavior + extractor audit
    b_disc = c_disc = blind_haz = gated_haz = 0
    n_haz = 0
    gated_halted = 0
    behavior = {"halted": 0, "passed": 0, "refused": 0}
    ext_agree = ext_fp = ext_fn = 0
    fp_list: list[dict] = []
    known_src = unknown_src = multi_src = 0

    for row, blind, res, latency_ms in rows:
        gold = row.get("human_crop") or None
        unclear = bool(row.get("human_unclear"))
        ext = row.get("_ext_now")
        halted = len(res.sources) == 0
        tier = res.resolution_tier.value
        if halted:
            gated_halted += 1
            behavior["halted"] += 1
        elif "REFUS" in tier.upper() or "GUARD" in tier.upper():
            behavior["refused"] += 1
        else:
            behavior["passed"] += 1
        # extractor audit (normalize: extractor None vs human EMPTY both mean absent)
        if (ext or None) == gold:
            ext_agree += 1
        elif ext and ext != gold:
            ext_fp += 1
            fp_list.append({"id": row["id"], "extractor": ext, "human": gold or "EMPTY"})
        elif not ext and gold:
            ext_fn += 1

        record: dict = {
            "id": row["id"], "source": row["source"], "true_crop": gold,
            "unclear": unclear, "extractor_crop": ext,
            "blind_terminal": blind["terminal"],
            "blind_retrieval_query": blind["retrieval_query"],
            "gated_tier": tier, "gated_halted": halted,
            "gated_latency_ms": latency_ms,
            "gated_answer_preview": (res.answer or "")[:120],
        }
        if gold in MAPPED_CROPS and not unclear and not blind["terminal"]:
            n_haz += 1
            cand = retriever.candidates(blind["retrieval_query"], depth=10)
            by_id = {s.id: s for s in cand}
            b_ids = [sid for sid, _ in blind["sources"]]
            b_sources = [by_id[i] for i in b_ids if i in by_id]
            g_sources = list(res.sources[:TOP_K])

            def sets_of(sources):
                out = []
                for src in sources:
                    crops, basis = source_crops(src)
                    out.append((sorted(crops), basis))
                return out

            b_sets, g_sets = sets_of(b_sources), sets_of(g_sources)
            for _, basis in b_sets:
                if basis == "unknown":
                    unknown_src += 1
                elif basis == "multi":
                    multi_src += 1
                else:
                    known_src += 1
            b_flag = any(s and gold not in s for s, _ in b_sets if s)
            g_flag = any(s and gold not in s for s, _ in g_sets if s)
            record["blind_hazard"] = bool(b_flag)
            record["gated_hazard"] = bool(g_flag)
            record["blind_top5_crop_sets"] = [s for s, _ in b_sets]
            record["gated_top5_crop_sets"] = [s for s, _ in g_sets]
            if b_flag:
                blind_haz += 1
            if g_flag:
                gated_haz += 1
            if b_flag and not g_flag:
                b_disc += 1
            if g_flag and not b_flag:
                c_disc += 1
        append_jsonl(records_path, record)

    results = {
        "benchmark_name": "EACL_N01B_HAZARD_FARMER_LABELED",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"sheet": SHEET_PATH, "bm25_index": INDEX_PATH}),
        "freeze": "gate0 v5: N01a recipe + team single-reviewer labels (agent, 2026-09-17, disclosed)",
        "labels": {"n": 200, "reviewer": "agent-single-review",
                   "upgrade": "second human reviewer on disagreements + unclear set if time allows"},
        "behavior_all_200": {**behavior, "halt_rate": round(behavior["halted"] / 200, 4)},
        "extractor_audit": {
            "agreement": round(ext_agree / 200, 4),
            "false_positive": round(ext_fp / 200, 4),
            "false_negative_miss": round(ext_fn / 200, 4),
            "fp_cases": fp_list,
        },
        "hazard_mapped_stratum": {
            "n": n_haz,
            "blind_overall": round(blind_haz / n_haz, 4) if n_haz else None,
            "blind_ci95": wilson(blind_haz, n_haz),
            "gated_overall": round(gated_haz / n_haz, 4) if n_haz else None,
            "gated_ci95": wilson(gated_haz, n_haz),
            "mcnemar_exact_p": mcnemar_exact(b_disc, c_disc),
            "discordant": {"blind_only": b_disc, "gated_only": c_disc},
            "mapping_coverage": {"known_single": known_src, "multi": multi_src, "unknown": unknown_src},
        },
    }
    tmp = results_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(results_path)
    print(json.dumps({k: v for k, v in results.items() if k in ("behavior_all_200", "extractor_audit", "hazard_mapped_stratum")}, indent=2, ensure_ascii=False)[:2200])
    print(f"[OK] wrote {results_path} + {records_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
