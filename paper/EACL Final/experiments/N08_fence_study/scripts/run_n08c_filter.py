#!/usr/bin/env python3
"""N08c: open vs crop-bound vs crop-bound + post-retrieval crop filter.

Same 400 PRISM B/C/D/I queries, BM25 index and query construction as N08.
Arms:  open        retrieve(q_open, 5)
       bound       retrieve(q_bound, 5)                       (= frozen N08 fenced arm)
       bound+filt  filter_by_crop(retrieve(q_bound, 20), gold, 5)   (app.domain.crop_scope)
Metrics: cross-crop rate (N08 definition), coverage, gold purity (separate lists),
disease hit@5 (independent of the crop rule: gold disease string in any passage),
exact McNemar, and a 30-query spot-check sheet for manual review.

Usage: python run_n08c_filter.py --prism <prism_benchmark_1000.jsonl>
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
from audit_n08_residual import (ROOT, INDEX, CORPUS, CATS, build_query,  # noqa: E402
                                source_crops, BM25Retriever)
from app.domain.crop_scope import filter_by_crop  # noqa: E402

OUT = HERE.parents[1] / "results_n08c_filter.json"
SPOT = HERE.parents[1] / "n08c_spotcheck.md"


def mcnemar_exact(b, c):
    from math import comb
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def wilson(k, n, z=1.95996):
    import math
    if n == 0:
        return [0.0, 0.0]
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0, c - h) * 100, 2), round(min(1, c + h) * 100, 2)]


def text_of(s):
    return " ".join(str(x or "") for x in (s.title_en, s.title_bn, s.content_en, s.content_bn)).lower()


def score(srcs, gold, disease):
    sets = [source_crops(s) for s in srcs]
    known = [c for c in sets if c]
    haz = any(gold not in c for c in known)
    pure = (sum(1 for c in known if c == {gold}) / len(known)) if known else None
    hit = None
    if disease:
        d = disease.lower().replace("রোগ", "").strip()
        hit = any(d and d in text_of(s) for s in srcs)
    return haz, pure, hit


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prism", required=True); a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.prism, encoding="utf-8")]
    rows = [r for r in rows if r.get("category") in CATS]
    assert len(rows) == 400
    ret = BM25Retriever(INDEX, CORPUS)
    arms = {k: {"haz": [], "pure": [], "hit": [], "n_src": []} for k in ("open", "bound", "filter")}
    removed_total, per = 0, []
    for r in rows:
        q, gold, dis = r["query"], r["true_crop"], r.get("true_disease_if_known")
        qo, _ = build_query(q, None)
        qb, _ = build_query(q, gold)
        res = {"open": ret.retrieve(qo, top_k=5), "bound": ret.retrieve(qb, top_k=5)}
        res["filter"], rm = filter_by_crop(ret.retrieve(qb, top_k=20), gold, 5)
        removed_total += rm
        rec = {"id": r["id"], "gold": gold, "query": q}
        for k, srcs in res.items():
            h, p, t = score(srcs, gold, dis)
            A = arms[k]; A["haz"].append(h); A["pure"].append(p); A["hit"].append(t); A["n_src"].append(len(srcs))
            rec[k] = {"haz": h, "n": len(srcs), "titles": [(s.title_en or s.title_bn or s.id)[:70] for s in srcs]}
        per.append(rec)

    def summ(A):
        n = len(A["haz"]); k = sum(A["haz"])
        pv = [x for x in A["pure"] if x is not None]
        hv = [x for x in A["hit"] if x is not None]
        return {"cross_crop": f"{k}/{n}", "cross_crop_pct": round(100 * k / n, 2), "ci95": wilson(k, n),
                "coverage_ge1": sum(1 for x in A["n_src"] if x > 0), "coverage_ge3": sum(1 for x in A["n_src"] if x >= 3),
                "mean_sources": round(sum(A["n_src"]) / n, 2),
                "gold_purity_mean": round(sum(pv) / len(pv), 4) if pv else None, "gold_purity_n": len(pv),
                "disease_hit5": f"{sum(hv)}/{len(hv)}", "disease_hit5_pct": round(100 * sum(hv) / len(hv), 2) if hv else None}

    def disc(x, y):
        b = sum(1 for i, j in zip(arms[x]["haz"], arms[y]["haz"]) if i and not j)
        c = sum(1 for i, j in zip(arms[x]["haz"], arms[y]["haz"]) if j and not i)
        return {"fixed": b, "broken": c, "mcnemar_exact_p": mcnemar_exact(b, c)}

    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out = {"experiment": "N08c_crop_filter", "provenance": {"git_head": head, "index": INDEX.name, "model_calls": 0},
           "arms": {k: summ(v) for k, v in arms.items()},
           "open_vs_bound": disc("open", "bound"), "bound_vs_filter": disc("bound", "filter"),
           "open_vs_filter": disc("open", "filter"), "passages_removed_by_filter": removed_total,
           "notes": "Cross-crop uses the same alias rule as the filter, so it is ~0 by construction for the filter arm; "
                    "coverage, disease hit@5 and the manual spot check are the independent checks."}
    OUT.write_text(json.dumps({**out, "per_query": per}, ensure_ascii=False, indent=1), encoding="utf-8")
    rnd = random.Random(42); sample = rnd.sample(per, 30)
    with open(SPOT, "w", encoding="utf-8") as f:
        f.write("# N08c spot check (seed 42, 30 queries, bound+filter arm)\n\n"
                "For each query mark: OK = every passage is about the gold crop or general; X = at least one other-crop passage.\n\n")
        for i, s in enumerate(sample, 1):
            f.write(f"## {i}. {s['id']} (gold: {s['gold']}) — mark: [ ]\n\n{s['query']}\n\n")
            for t in s["filter"]["titles"]:
                f.write(f"- {t}\n")
            f.write("\n")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
