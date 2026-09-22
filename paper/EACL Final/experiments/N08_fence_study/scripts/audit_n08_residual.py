#!/usr/bin/env python3
"""N08b: audit of the residual cross-crop retrieval under gold-crop binding.

Re-runs the frozen N08 design (same PRISM rows, same BM25 index, same query
construction and crop-mapping rule) and, for every query still flagged in the
fenced arm, records which top-5 passages trigger the flag and why.

Crop-mapping rule (copied verbatim from N01/N08): a passage's crop set is every
crop whose alias appears in its title/content/metadata text. A query is flagged
when any top-5 passage has a non-empty crop set that excludes the gold crop.

Usage: python audit_n08_residual.py --prism <prism_benchmark_1000.jsonl>
Output: N08_fence_study/results_residual_audit.json
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
sys.path.insert(0, str(ROOT / "backend"))

from app.application.adaptive_router import AdaptiveRetrievalRouter, RetrievalRoute  # noqa: E402
from app.application.query_builder import build_retrieval_query  # noqa: E402
from app.domain.concept_normalizer import ConceptNormalizer  # noqa: E402
from app.domain.contracts import QueryContext  # noqa: E402
from app.domain.enums import SafetyCategory  # noqa: E402
from app.domain.intent import _CROP_ALIASES  # noqa: E402
from app.domain.query_extractor import QueryExtractor  # noqa: E402
from app.domain.working_memory import AgriculturalWorkingMemory  # noqa: E402
from app.infrastructure.retrieval.bm25 import BM25Retriever  # noqa: E402

INDEX = ROOT / "backend/ml_assets/rag_index/indexes/bm25_index.pkl"
CORPUS = ROOT / "backend/ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl"
OUT = HERE.parents[1] / "results_residual_audit.json"
CATS = ("B_colloquial_bengali", "C_dialect", "D_banglish", "I_ambiguous_disease")
TOP_K = 5


def build_crop_map():  # verbatim from run_n01_blind_arm.py
    pairs = []
    for crop_id, aliases in _CROP_ALIASES.items():
        for alias in aliases:
            alias = str(alias).strip()
            if alias:
                pairs.append((alias.lower(), crop_id))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    seen, out = set(), []
    for a, c in pairs:
        if a not in seen:
            seen.add(a)
            out.append((a, c))
    return out


CROP_MAP = build_crop_map()
TOK = re.compile(r"[\wঀ-৿]+")


def source_crops(s):  # verbatim from run_n01_blind_arm.py
    texts = [str(getattr(s, k, "") or "") for k in
             ("title_en", "title_bn", "source", "citation", "content_en", "content_bn")]
    meta = getattr(s, "metadata", {}) or {}
    for k in ("section_title", "title_en", "title_bn", "category", "publisher"):
        v = meta.get(k, "")
        if isinstance(v, str) and v:
            texts.append(v)
    tags = meta.get("tags", [])
    if isinstance(tags, list):
        texts.extend(str(t) for t in tags if isinstance(t, str))
    blob = "\n".join(texts).lower()
    toks = set(TOK.findall(blob))
    found = set()
    for alias, crop in CROP_MAP:
        if (" " in alias and alias in blob) or alias in toks:
            found.add(crop)
    return found


def build_query(query, crop_ctx):  # verbatim from run_n08_fence.py
    context = QueryContext(crop=crop_ctx, disease=None, history=(), farmer_context=None)
    wm = AgriculturalWorkingMemory.from_dict(None)
    info = QueryExtractor.extract(query)
    eff = crop_ctx or info.crop or wm.crop
    cr = ConceptNormalizer.normalize(query, crop=eff)
    wm = wm.merge(crop=eff, problem_type=info.problem_type,
                  symptom=info.symptom or cr.matched_expression, location=info.location,
                  temporal_event=info.temporal_event, candidate_hypotheses=cr.retrieval_hypotheses)
    r = AdaptiveRetrievalRouter.route(query, working_memory=wm)
    base = r.primary_query if r.route in (RetrievalRoute.ROUTE_C_CONCEPT_HYPOTHESES,
                                           RetrievalRoute.ROUTE_D_CONVERSATIONAL_FOLLOW_UP) else query
    return build_retrieval_query(base, context, SafetyCategory.SAFE_AGRI.value), info.crop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prism", required=True)
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.prism, encoding="utf-8")]
    rows = [r for r in rows if r.get("category") in CATS]
    assert len(rows) == 400
    ret = BM25Retriever(INDEX, CORPUS)

    open_flag = fenced_flag = 0
    cases = []
    for r in rows:
        q, gold = r["query"], r["true_crop"]
        q_open, _ = build_query(q, None)
        q_fen, text_crop = build_query(q, gold)
        top_open = ret.retrieve(q_open, top_k=TOP_K)
        top_fen = ret.retrieve(q_fen, top_k=TOP_K)
        oflag = any(c and gold not in c for c in (source_crops(s) for s in top_open))
        open_flag += oflag
        off = []
        for rank, s in enumerate(top_fen, 1):
            c = source_crops(s)
            if c and gold not in c:
                off.append({"rank": rank, "node": getattr(s, "id", None) or getattr(s, "node_id", None),
                            "crops": sorted(c), "title": (getattr(s, "title_en", "") or "")[:90]})
        if off:
            fenced_flag += 1
            cases.append({"id": r.get("id"), "category": r["category"], "gold": gold,
                          "text_crop": text_crop, "offending": off})

    # Breakdown of residual cases
    n_res = len(cases)
    by_cat = collections.Counter(c["category"] for c in cases)
    by_gold = collections.Counter(c["gold"] for c in cases)
    text_names_other = sum(1 for c in cases if c["text_crop"] and c["text_crop"] != c["gold"])
    only_rank5_or_4 = sum(1 for c in cases if min(o["rank"] for o in c["offending"]) >= 4)
    rank1 = sum(1 for c in cases if min(o["rank"] for o in c["offending"]) == 1)
    n_off = [len(c["offending"]) for c in cases]
    one_off = sum(1 for k in n_off if k == 1)
    all_off = [o for c in cases for o in c["offending"]]
    multi = sum(1 for o in all_off if len(o["crops"]) >= 2)
    off_crop = collections.Counter(cr for o in all_off for cr in o["crops"])
    pair = collections.Counter((c["gold"], cr) for c in cases for o in c["offending"] for cr in o["crops"])
    node_freq = collections.Counter((o["node"], o["title"]) for o in all_off)
    denom_by_cat = collections.Counter(r["category"] for r in rows)

    result = {
        "experiment": "N08b_residual_audit",
        "reproduction": {"open_flagged": open_flag, "fenced_flagged": fenced_flag, "n": 400,
                         "matches_N08": open_flag == 145 and fenced_flag == 120},
        "residual_cases": n_res,
        "by_category": {k: f"{by_cat.get(k, 0)}/{denom_by_cat[k]}" for k in CATS},
        "by_gold_crop": dict(by_gold.most_common()),
        "query_text_names_other_crop": text_names_other,
        "first_offending_rank_1": rank1,
        "first_offending_rank_4_or_5": only_rank5_or_4,
        "cases_with_single_offending_passage": one_off,
        "offending_passages_total": len(all_off),
        "offending_passages_multi_crop_without_gold": multi,
        "offending_crop_counts": dict(off_crop.most_common()),
        "top_gold_offending_pairs": [[g, o, k] for (g, o), k in pair.most_common(12)],
        "distinct_offending_nodes": len(node_freq),
        "most_frequent_offending_nodes": [[n, t, k] for (n, t), k in node_freq.most_common(10)],
        "cases": cases,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
