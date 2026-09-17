#!/usr/bin/env python3
"""N01 blind-RAG hazard arm + gated-arm pair (EACL Final, real-data).

Paired design on PRISM B/C/D/I (400 rows, all with true_crop):
  BLIND arm: pipeline-identical query construction, gate SKIPPED ->
             BM25 retrieve(top_k=5) over frozen 2,135-node index.
  GATED arm: frozen offline pipeline per row (halt => no retrieval possible).
F rows (100, no true_crop): blind top-5 distinct-crop spread (descriptive only).

Frozen recipe: plans/experiments/results/gate0_freeze_N01N02.md (v3).
Money: $0 API (offline stub + deterministic safety only).
Disk: per-record JSONL append with flush+fsync (AGENTS.md zero-buffering).

Outputs (paper/EACL Final/experiments/results/):
  n01_records_YYYYMMDD.jsonl, n01_results_YYYYMMDD.json
"""
from __future__ import annotations

import asyncio
import json
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE_ROOT = HERE.parents[5]
sys.path.insert(0, str(WORKSPACE_ROOT / "backend"))
sys.path.insert(0, str(WORKSPACE_ROOT / "paper" / "EACL Demo" / "experiments" / "shared"))

from app.application.adaptive_router import AdaptiveRetrievalRouter, RetrievalRoute  # noqa: E402
from app.application.qa_pipeline import QAInput  # noqa: E402
from app.application.query_builder import build_retrieval_query  # noqa: E402
from app.domain.concept_normalizer import ConceptNormalizer  # noqa: E402
from app.domain.contracts import QueryContext  # noqa: E402
from app.domain.enums import ResolutionTier, SafetyCategory  # noqa: E402
from app.domain.intent import _CROP_ALIASES  # noqa: E402
from app.domain.query_extractor import QueryExtractor, _ROMAN_CROP_ALIASES  # noqa: E402
from app.domain.working_memory import AgriculturalWorkingMemory  # noqa: E402
from app.infrastructure.retrieval.bm25 import BM25Retriever  # noqa: E402

import _qa_harness as H  # noqa: E402

PRISM_PATH = WORKSPACE_ROOT / "research_artifacts" / "datasets" / "prism_benchmark" / "prism_benchmark_1000.jsonl"
INDEX_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl"
CORPUS_PATH = WORKSPACE_ROOT / "backend" / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
OUT_DIR = WORKSPACE_ROOT / "paper" / "EACL Final" / "experiments" / "results"
PAIRED_CATS = ("B_colloquial_bengali", "C_dialect", "D_banglish", "I_ambiguous_disease")
TOP_K = 5


def build_crop_map() -> list[tuple[str, str]]:
    """crop_map_v1: (alias_lower, crop_id), longest alias first (frozen)."""
    pairs: list[tuple[str, str]] = []
    for crop_id, aliases in _CROP_ALIASES.items():
        for alias in aliases:
            alias = str(alias).strip()
            if alias:
                pairs.append((alias.lower(), crop_id))
    for word, crop_id in _ROMAN_CROP_ALIASES.items():
        word = str(word).strip()
        if word:
            pairs.append((word.lower(), crop_id))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    seen: set[str] = set()
    deduped: list[tuple[str, str]] = []
    for alias, crop in pairs:
        if alias not in seen:
            seen.add(alias)
            deduped.append((alias, crop))
    return deduped


CROP_MAP = build_crop_map()
CROP_TOKEN_RE = re.compile(r"[\w\u0980-\u09FF]+")


def source_crops(source) -> tuple[set[str], str]:
    """Map one RetrievedSource to crop set. Returns (crops, basis)."""
    texts: list[str] = [
        str(getattr(source, "title_en", "") or ""),
        str(getattr(source, "title_bn", "") or ""),
        str(getattr(source, "source", "") or ""),
        str(getattr(source, "citation", "") or ""),
        str(getattr(source, "content_en", "") or ""),
        str(getattr(source, "content_bn", "") or ""),
    ]
    meta = getattr(source, "metadata", {}) or {}
    for key in ("section_title", "title_en", "title_bn", "category", "publisher"):
        value = meta.get(key, "")
        if isinstance(value, str) and value:
            texts.append(value)
    tags = meta.get("tags", [])
    if isinstance(tags, list):
        texts.extend(str(t) for t in tags if isinstance(t, str))
    blob = "\n".join(texts).lower()
    tokens = set(CROP_TOKEN_RE.findall(blob))
    found: set[str] = set()
    for alias, crop in CROP_MAP:
        if " " in alias:
            if alias in blob:
                found.add(crop)
        elif alias in tokens:
            found.add(crop)
    if len(found) == 1:
        return found, "single"
    if len(found) >= 2:
        return found, "multi"
    return set(), "unknown"


def wilson(k: int, n: int, z: float = 1.95996) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(max(0.0, center - half) * 100, 2), round(min(1.0, center + half) * 100, 2)]


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return round(2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n), 6)


def append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


async def blind_retrieve(query: str, retriever: BM25Retriever, safety) -> dict:
    """Pipeline-identical retrieval construction, gate skipped. Returns detail."""
    context = QueryContext(crop=None, disease=None, history=(), farmer_context=None)
    working_memory = AgriculturalWorkingMemory.from_dict(None)
    info_state = QueryExtractor.extract(query)
    effective_crop = info_state.crop or working_memory.crop
    concept_res = ConceptNormalizer.normalize(query, crop=effective_crop)
    working_memory = working_memory.merge(
        crop=effective_crop,
        problem_type=info_state.problem_type,
        symptom=info_state.symptom or concept_res.matched_expression,
        location=info_state.location,
        temporal_event=info_state.temporal_event,
        candidate_hypotheses=concept_res.retrieval_hypotheses,
    )
    if not context.crop and working_memory.crop:
        context = QueryContext(crop=working_memory.crop, disease=context.disease,
                               history=context.history, farmer_context=context.farmer_context)
    decision = await safety.classify(query, context)
    terminal = bool(getattr(decision, "terminal", decision.category is not SafetyCategory.SAFE_AGRI))
    if terminal:
        return {"terminal": True, "category": decision.category.value, "retrieval_query": None, "sources": []}
    routing = AdaptiveRetrievalRouter.route(query, working_memory=working_memory)
    base = (routing.primary_query
            if routing.route in (RetrievalRoute.ROUTE_C_CONCEPT_HYPOTHESES,
                                 RetrievalRoute.ROUTE_D_CONVERSATIONAL_FOLLOW_UP)
            else query)
    retrieval_query = build_retrieval_query(base, context, decision.category.value)
    sources = retriever.retrieve(retrieval_query, top_k=TOP_K)
    return {"terminal": False, "category": decision.category.value,
            "route": routing.route.value, "retrieval_query": retrieval_query,
            "sources": [(s.id, s.score) for s in sources], "raw_sources": sources}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    records_path = OUT_DIR / f"n01_records_{stamp}.jsonl"
    results_path = OUT_DIR / f"n01_results_{stamp}.json"
    if records_path.exists():
        records_path.unlink()

    with open(PRISM_PATH, encoding="utf-8") as f:
        prism = [json.loads(line) for line in f]
    paired = [r for r in prism if r.get("category") in PAIRED_CATS]
    descriptive = [r for r in prism if r.get("category") == "F_underspecified"]
    assert len(paired) == 400, f"expected 400 paired rows, got {len(paired)}"
    assert len(descriptive) == 100, f"expected 100 F rows, got {len(descriptive)}"

    retriever = BM25Retriever(INDEX_PATH, CORPUS_PATH)
    pipeline, _, _, _ = H.build_offline_pipeline(audit=H.InMemoryAudit())
    safety = H.DeterministicSafety()

    async def run_all():
        out = []
        work = [("paired", r) for r in paired] + [("descriptive", r) for r in descriptive]
        for idx, (kind, row) in enumerate(work):
            q = row["query"]
            gold = row.get("true_crop")
            blind = await blind_retrieve(q, retriever, safety)
            t0 = time.perf_counter()
            res = await pipeline.run(QAInput(query=q))
            latency_ms = round((time.perf_counter() - t0) * 1000, 3)
            halted = len(res.sources) == 0
            record: dict = {
                "id": row.get("id"), "kind": kind, "category": row.get("category"),
                "true_crop": gold, "query": q,
                "blind_terminal": blind["terminal"],
                "blind_category": blind["category"],
                "blind_retrieval_query": blind["retrieval_query"],
                "blind_source_ids": [sid for sid, _ in blind["sources"]] if not blind["terminal"] else [],
                "gated_tier": res.resolution_tier.value,
                "gated_category": res.category.value,
                "gated_halted": halted,
                "gated_source_ids": [s.id for s in res.sources],
                "gated_answer_preview": res.answer[:120],
                "gated_latency_ms": latency_ms,
            }
            # hazard scoring needs source objects: recompute sets from stored ids
            record["_blind_sets"] = None  # filled below (source objects not JSON-serializable here)
            out.append((record, blind, res))
            if (idx + 1) % 100 == 0:
                print(f"[{idx + 1}/{len(work)}] done", flush=True)
        return out

    # NOTE: hazard mapping needs source objects; score inline in second pass below.
    rows = asyncio.run(run_all())

    # Re-derive source objects deterministically for scoring (same frozen calls).
    async def score_all():
        scored = []
        for record, blind, res in rows:
            if record["kind"] == "paired":
                b_sources = []
                if not blind["terminal"]:
                    # re-run identical blind retrieval to recover source objects
                    b2 = await blind_retrieve(record["query"], retriever, safety)
                    # fetch full objects via candidates on stored retrieval query
                    cand = retriever.candidates(b2["retrieval_query"] or record["query"], depth=10)
                    by_id = {s.id: s for s in cand}
                    b_sources = [by_id[i] for i in record["blind_source_ids"] if i in by_id]
                g_sources = list(res.sources[:TOP_K])
                scored.append((record, b_sources, g_sources, None))
            else:
                detail = await blind_retrieve(record["query"], retriever, safety)
                cand_sets = []
                if not detail["terminal"]:
                    cand_sets = retriever.candidates(detail["retrieval_query"], depth=10)[:TOP_K]
                scored.append((record, [], [], (detail, cand_sets)))
        return scored

    scored = asyncio.run(score_all())

    b_disc = c_disc = blind_haz = gated_haz = 0
    gated_halted = gated_retrieved = gated_cond_haz = 0
    blind_terminals = 0
    known_src = unknown_src = multi_src = 0
    blind_spread_counts: list[int] = []
    n_paired = len(paired)

    for record, b_sources, g_sources, extra in scored:
        def sets_of(sources):
            out = []
            for src in sources:
                crops, basis = source_crops(src)
                out.append((sorted(crops), basis))
            return out

        if record["kind"] == "paired":
            gold = record["true_crop"]
            b_sets = sets_of(b_sources)
            for _, basis in b_sets:
                if basis == "unknown":
                    unknown_src += 1
                elif basis == "multi":
                    multi_src += 1
                else:
                    known_src += 1
            if record["blind_terminal"]:
                blind_terminals += 1
                b_flag = False
            else:
                b_flag = any(s and gold not in s for s, _ in b_sets if s)
            g_sets = sets_of(g_sources)
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
            if record["gated_halted"]:
                gated_halted += 1
            else:
                gated_retrieved += 1
                if g_flag:
                    gated_cond_haz += 1
        else:
            # Descriptive F rows (no gold crop): distinct-crop spread of blind top-5.
            _, cand_sets = extra
            distinct: set[str] = set()
            if cand_sets:
                allsets = sets_of(cand_sets)
                distinct = {c for s, _ in allsets for c in s}
                for _, basis in allsets:
                    if basis == "unknown":
                        unknown_src += 1
                    elif basis == "multi":
                        multi_src += 1
                    else:
                        known_src += 1
            blind_spread_counts.append(len(distinct))
            record["blind_distinct_crop_count"] = len(distinct)
        record.pop("_blind_sets", None)
        append_jsonl(records_path, record)

    results = {
        "benchmark_name": "EACL_N01_BLIND_RAG_HAZARD_PAIRED",
        "execution_status": "DONE_REAL",
        "provenance": H.provenance(HERE, inputs={"prism": PRISM_PATH, "bm25_index": INDEX_PATH}),
        "freeze": "plans/experiments/results/gate0_freeze_N01N02.md (v3: pipeline-identical blind recipe, crop_map_v1)",
        "design": {"n_paired": n_paired, "categories": list(PAIRED_CATS), "top_k": TOP_K,
                   "blind": "pipeline-identical construction, gate SKIPPED",
                   "gated": "frozen offline pipeline (deterministic safety, stub LLM)"},
        "mapping_coverage": {
            "known_single": known_src, "multi": multi_src, "unknown": unknown_src,
            "unknown_frac": round(unknown_src / max(1, known_src + multi_src + unknown_src), 4),
        },
        "blind_terminals": blind_terminals,
        "gated_behavior": {
            "halt_rate": round(gated_halted / n_paired, 4),
            "retrieved_rate": round(gated_retrieved / n_paired, 4),
        },
        "hazard": {
            "blind_overall": round(blind_haz / n_paired, 4),
            "blind_ci95": wilson(blind_haz, n_paired),
            "gated_overall": round(gated_haz / n_paired, 4),
            "gated_ci95": wilson(gated_haz, n_paired),
            "gated_conditional_on_retrieved": round(gated_cond_haz / max(1, gated_retrieved), 4),
            "mcnemar_exact_p": mcnemar_exact(b_disc, c_disc),
            "discordant": {"blind_only": b_disc, "gated_only": c_disc},
        },
        "descriptive_F_spread": {
            "n": len(descriptive),
            "mean_distinct_crops_blind_top5": round(sum(blind_spread_counts) / max(1, len(blind_spread_counts)), 2),
        },
    }
    tmp = results_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(results_path)
    print(json.dumps(results["hazard"], indent=2))
    print(json.dumps(results["gated_behavior"], indent=2))
    print(f"[OK] wrote {results_path} + {records_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
