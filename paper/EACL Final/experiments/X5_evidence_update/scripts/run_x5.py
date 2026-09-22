#!/usr/bin/env python3
"""X5: knowledge update without retraining (leave-one-out, retrieval only).

For 10 real guideline passages (fixed selection rule, seed 42):
  before = index rebuilt WITHOUT the passage  -> is it retrievable?  (must be absent)
  after  = index WITH the passage (update)     -> rank for its query
No guidance is invented and no model is loaded: the generator is untouched by
construction, because an update only rebuilds the BM25 index.

Step 0 (equivalence): rebuilding BM25 from the frozen index's own tokenized
corpus must reproduce the frozen top-5 for all 400 PRISM B/C/D/I queries.

Usage: python run_x5.py --prism <prism_benchmark_1000.jsonl> [--tmp DIR]
Output: results/x5_update_<date>.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import random
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
N08 = HERE.parents[2] / "N08_fence_study" / "scripts"
sys.path.insert(0, str(N08))
from audit_n08_residual import ROOT, INDEX, CORPUS, CATS, build_query, source_crops, BM25Retriever  # noqa: E402
from rank_bm25 import BM25Okapi  # noqa: E402

DOSE = re.compile(r"[0-9০-৯]+(?:[.,][0-9০-৯]+)?\s*(?:ml|g|kg|মিলি|গ্রাম|কেজি|লিটার)\b", re.I)
OUT = HERE.parents[1] / "results"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_index(data: dict, keep: list[int], path: Path) -> float:
    t = time.perf_counter()
    corpus = [data["corpus"][i] for i in keep]
    new = {"bm25": BM25Okapi([doc.lower().split() for doc in corpus]), "nodes": [data["nodes"][i] for i in keep],
           "corpus": corpus, "ids": [data["ids"][i] for i in keep]}
    with path.open("wb") as f:
        pickle.dump(new, f)
    return time.perf_counter() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prism", required=True)
    ap.add_argument("--tmp", default=None)
    a = ap.parse_args()
    tmp = Path(a.tmp or tempfile.mkdtemp(prefix="x5_"))
    tmp.mkdir(parents=True, exist_ok=True)
    data = pickle.load(open(INDEX, "rb"))
    n_all = len(data["ids"])
    rows = [json.loads(l) for l in open(a.prism, encoding="utf-8")]
    rows = [r for r in rows if r.get("category") in CATS]
    queries = [(r["id"], r["true_crop"], build_query(r["query"], r["true_crop"])[0]) for r in rows]

    # Step 0: equivalence of a rebuilt full index with the frozen one.
    frozen = BM25Retriever(INDEX, CORPUS)
    full_p = tmp / "x5_full.pkl"
    full_build_s = write_index(data, list(range(n_all)), full_p)
    full = BM25Retriever(full_p, CORPUS)
    mism = [qid for qid, _, q in queries
            if [s.id for s in frozen.retrieve(q, top_k=5)] != [s.id for s in full.retrieve(q, top_k=5)]]
    assert not mism, f"rebuilt index differs on {len(mism)} queries"

    # Target selection (fixed rule): rank-1 passage for a query, carrying a dose
    # pattern and naming the query's gold crop; one target per distinct passage.
    cands, seen = [], set()
    for qid, gold, q in queries:
        top = full.retrieve(q, top_k=5)
        if not top:
            continue
        s = top[0]
        text = " ".join(str(x or "") for x in (s.title_en, s.title_bn, s.content_en, s.content_bn))
        if s.id in seen or not DOSE.search(text) or gold not in source_crops(s):
            continue
        seen.add(s.id)
        cands.append((qid, gold, q, s.id))
    random.Random(42).shuffle(cands)
    targets = cands[:10]

    id_to_pos = {nid: i for i, nid in enumerate(data["ids"])}
    results = []
    for qid, gold, q, nid in targets:
        pos = id_to_pos[nid]
        minus_p = tmp / f"x5_minus_{pos}.pkl"
        build_s = write_index(data, [i for i in range(n_all) if i != pos], minus_p)
        before = [s.id for s in BM25Retriever(minus_p, CORPUS).retrieve(q, top_k=5)]
        after = [s.id for s in full.retrieve(q, top_k=5)]
        results.append({"query_id": qid, "gold_crop": gold, "node_id": nid,
                        "retrieved_before": nid in before,
                        "rank_after": after.index(nid) + 1 if nid in after else None,
                        "top5_before": before, "top5_after": after,
                        "rebuild_seconds": round(build_s, 2)})
        minus_p.unlink()

    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    ok = sum(1 for r in results if not r["retrieved_before"] and r["rank_after"] == 1)
    out = {"experiment": "X5_evidence_update_leave_one_out",
           "provenance": {"git_head": head, "frozen_index_sha256": sha(INDEX), "model_calls": 0, "tokenizer": "str.lower().split() (BM25Retriever._tokenize)",
                          "generator_loaded": False},
           "equivalence": {"queries": len(queries), "top5_mismatches": 0, "full_rebuild_seconds": round(full_build_s, 2)},
           "candidates": len(cands), "targets": len(results),
           "absent_before_and_rank1_after": f"{ok}/{len(results)}",
           "median_rebuild_seconds": sorted(r["rebuild_seconds"] for r in results)[len(results) // 2] if results else None,
           "results": results}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"x5_update_{stamp}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    full_p.unlink()
    print(json.dumps({k: v for k, v in out.items() if k != "results"}, indent=1))
    for r in results:
        print(r["query_id"], r["node_id"], "before:", r["retrieved_before"], "after rank:", r["rank_after"], f"{r['rebuild_seconds']}s")


if __name__ == "__main__":
    main()
