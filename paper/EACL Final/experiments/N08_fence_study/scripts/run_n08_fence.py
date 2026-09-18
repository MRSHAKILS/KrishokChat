#!/usr/bin/env python3
"""N08 image-fence scope study (EACL Final, CPU $0).

Paired design on PRISM B/C/D/I (400 rows, all with true_crop):
  OPEN arm:  pipeline-identical retrieval with NO crop context (text as-is).
  FENCED arm: identical construction with context.crop preset to gold
             (simulates perfect vision routing; tests the fence, not the
             classifier — classifier accuracy is N04's job).
Metrics: top-5 wrong-crop-source rate + candidate-depth crop purity, paired
McNemar + Wilson. Frozen map/provenance conventions from N01 (gate0 freeze).

Outputs: experiments/results/n08_fence_<date>.json (+ .jsonl records).
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
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "N01_blind_arm" / "scripts"))

from app.application.adaptive_router import AdaptiveRetrievalRouter, RetrievalRoute  # noqa: E402
from app.application.query_builder import build_retrieval_query  # noqa: E402
from app.domain.concept_normalizer import ConceptNormalizer  # noqa: E402
from app.domain.contracts import QueryContext  # noqa: E402
from app.domain.enums import SafetyCategory  # noqa: E402
from app.domain.query_extractor import QueryExtractor  # noqa: E402
from app.domain.working_memory import AgriculturalWorkingMemory  # noqa: E402
from app.infrastructure.retrieval.bm25 import BM25Retriever  # noqa: E402

import _qa_harness as H  # noqa: E402
from run_n01_blind_arm import (  # noqa: E402
    TOP_K, mcnemar_exact, source_crops, wilson)

PRISM_PATH = WORKSPACE_ROOT / "research_artifacts" / "datasets" / "prism_benchmark" / "prism_benchmark_1000.jsonl"
INDEX_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl"
CORPUS_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
PAIRED_CATS = ("B_colloquial_bengali", "C_dialect", "D_banglish", "I_ambiguous_disease")
DEPTH = 50


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def build_query(query: str, crop_ctx: str | None) -> tuple[str, str]:
    """Pipeline-identical query construction with optional preset crop context."""
    context = QueryContext(crop=crop_ctx, disease=None, history=(), farmer_context=None)
    working_memory = AgriculturalWorkingMemory.from_dict(None)
    info_state = QueryExtractor.extract(query)
    effective_crop = crop_ctx or info_state.crop or working_memory.crop
    concept_res = ConceptNormalizer.normalize(query, crop=effective_crop)
    working_memory = working_memory.merge(
        crop=effective_crop, problem_type=info_state.problem_type,
        symptom=info_state.symptom or concept_res.matched_expression,
        location=info_state.location, temporal_event=info_state.temporal_event,
        candidate_hypotheses=concept_res.retrieval_hypotheses)
    routing = AdaptiveRetrievalRouter.route(query, working_memory=working_memory)
    base = (routing.primary_query
            if routing.route in (RetrievalRoute.ROUTE_C_CONCEPT_HYPOTHESES,
                                 RetrievalRoute.ROUTE_D_CONVERSATIONAL_FOLLOW_UP)
            else query)
    return build_retrieval_query(base, context, SafetyCategory.SAFE_AGRI.value), routing.route.value


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"n08_fence_{stamp}.json"
    rec_path = OUT_DIR / f"n08_fence_{stamp}.jsonl"
    if rec_path.exists():
        rec_path.unlink()

    prism = [json.loads(l) for l in open(PRISM_PATH, encoding="utf-8")]
    rows = [r for r in prism if r.get("category") in PAIRED_CATS]
    assert len(rows) == 400, len(rows)
    retriever = BM25Retriever(INDEX_PATH, CORPUS_PATH)

    b_only = c_only = 0
    open_haz = fenced_haz = 0
    open_pure = fenced_pure = []
    n = len(rows)
    t_start = time.perf_counter()
    for idx, row in enumerate(rows):
        q, gold = row["query"], row["true_crop"]
        q_open, _ = build_query(q, None)
        q_fenced, _ = build_query(q, gold)
        top_open = retriever.retrieve(q_open, top_k=TOP_K)
        top_fenced = retriever.retrieve(q_fenced, top_k=TOP_K)
        deep_open = retriever.candidates(q_open, depth=DEPTH)
        deep_fenced = retriever.candidates(q_fenced, depth=DEPTH)

        def flag(sources):
            sets = []
            for s in sources:
                crops, basis = source_crops(s)
                sets.append((sorted(crops), basis))
            known = [s for s, b in sets if s]
            haz = any(gold not in s for s in known)
            pure = (sum(1 for s in known if s == [gold]) / len(known)) if known else None
            return haz, pure

        oh, op = flag(top_open)
        fh, fp_ = flag(top_fenced)
        open_pure.append(op)
        fenced_pure.append(fp_)
        if oh:
            open_haz += 1
        if fh:
            fenced_haz += 1
        if oh and not fh:
            b_only += 1
        if fh and not oh:
            c_only += 1
        append_jsonl(rec_path, {"id": row.get("id"), "category": row.get("category"),
                                "true_crop": gold, "open_hazard": oh, "fenced_hazard": fh,
                                "open_purity": op, "fenced_purity": fp_})
        if (idx + 1) % 100 == 0:
            print(f"[{idx + 1}/{n}] open={open_haz} fenced={fenced_haz}", flush=True)

    def avg(xs):
        xs = [x for x in xs if x is not None]
        return round(sum(xs) / len(xs), 4) if xs else None

    results = {
        "benchmark_name": "EACL_N08_IMAGE_FENCE_SCOPE",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"prism": PRISM_PATH, "bm25_index": INDEX_PATH}),
        "freeze": "gate0 v3 conventions (crop_map_v1, Wilson, McNemar exact)",
        "design": {"n": n, "categories": list(PAIRED_CATS), "top_k": TOP_K, "depth": DEPTH,
                   "open": "text as-is, no crop context",
                   "fenced": "context.crop preset to gold (perfect-vision simulation; classifier accuracy is N04)"},
        "top5_wrong_crop_rate": {
            "open": round(open_haz / n, 4), "open_ci95": wilson(open_haz, n),
            "fenced": round(fenced_haz / n, 4), "fenced_ci95": wilson(fenced_haz, n),
            "mcnemar_exact_p": mcnemar_exact(b_only, c_only),
            "discordant": {"open_only": b_only, "fenced_only": c_only}},
        "top5_gold_purity_mean": {"open": avg(open_pure), "fenced": avg(fenced_pure)},
        "elapsed_s": round(time.perf_counter() - t_start, 1),
    }
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    print(json.dumps(results["top5_wrong_crop_rate"], indent=2))
    print(json.dumps(results["top5_gold_purity_mean"], indent=2))
    print(f"[OK] wrote {out_path} + {rec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
