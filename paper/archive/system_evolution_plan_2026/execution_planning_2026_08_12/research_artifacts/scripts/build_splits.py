#!/usr/bin/env python3
"""T09 split builder v2 — frozen train/dev/test splits for the Treatment QA track.

Grouping rule (T07 protocol immutable): group by source document, intent family,
and transformation lineage. All dialect/Banglish/adversarial forms of one intent
stay in ONE split.

Grouping unit (v2, leakage-driven revision):
  union-find over records where two records join the same group when they share
  (a) the same base intent  = cell_id minus the qtype suffix (`<16hex>` part),
  (b) the same exact question text, or
  (c) the same normalized question text (NFKC + casefold + whitespace collapse).
This keeps same-intent records (qtype variants, dialect variants, and exact
source-data duplicates across node ids) in ONE split.

Method: deterministic stratified group-level split.
  - Stratum = (majority category_group, chemical_bearing) at group level.
  - Groups sorted by stratum key then group id; seeded shuffle; proportional
    assignment to train/dev/test.
  - Re-running with same input + seed reproduces identical output (dry-run
    reconstruction gate).

Outputs in --out-dir (default research_artifacts/datasets/frozen):
  T09_treatment_qa_{train,dev,test}_v1.jsonl   (records + t09_split/t09_group metadata)
  T09_split_manifest_v1.json                   (machine-readable run manifest)
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

TOOL_VERSION = "build_splits.py v2"
SCHEMA_GUIDELINE = {"schema_version": "T07_claim_schema_v1", "guideline_version": "T07_label_manual_v1"}
CATEGORY_GROUPS = {
    "disease": "disease", "pest": "pest", "fertilizer": "fertilizer",
    "ipm": "other", "seed_tech": "other", "food_safety": "other", "herbicide": "other",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_chemicals(rec: dict) -> list[str]:
    ct = rec.get("chemical_trace")
    if not ct:
        return []
    if isinstance(ct, list):
        return [str(c) for c in ct]
    if isinstance(ct, str) and ct.strip():
        try:
            parsed = json.loads(ct)
            if isinstance(parsed, list):
                return [str(c) for c in parsed]
        except json.JSONDecodeError:
            return [ct]
    return []


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


class UnionFind:
    def __init__(self, keys: list[str]):
        self.parent = {k: k for k in keys}

    def find(self, x: str) -> str:
        p = self.parent
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def main() -> int:
    ap = argparse.ArgumentParser(description="T09 frozen split builder v2.")
    ap.add_argument("--input", type=Path, required=True, help="treatment_full.jsonl path")
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--seed", type=int, default=20260813, help="documented split seed")
    ap.add_argument("--train", type=float, default=0.6)
    ap.add_argument("--dev", type=float, default=0.2)
    ap.add_argument("--test", type=float, default=0.2)
    args = ap.parse_args()

    if abs((args.train + args.dev + args.test) - 1.0) > 1e-9:
        print("error: train+dev+test proportions must sum to 1.0", file=sys.stderr)
        return 2

    out_dir = args.out_dir or (Path(__file__).resolve().parents[1] / "datasets" / "frozen")
    out_dir.mkdir(parents=True, exist_ok=True)

    records = []
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    if not records:
        print("error: empty input", file=sys.stderr)
        return 2

    # ---- build union-find groups ----
    for r in records:
        cell = str(r.get("cell_id", ""))
        base = cell.rsplit("_", 1)[0] if "_" in cell else cell
        r["_base"] = base

    uf = UnionFind([str(r["_base"]) for r in records] +
                   ["Q:" + str(r.get("question", "")) for r in records] +
                   ["N:" + norm(str(r.get("question", ""))) for r in records])
    for r in records:
        uf.union(str(r["_base"]), "Q:" + str(r.get("question", "")))
        uf.union(str(r["_base"]), "N:" + norm(str(r.get("question", ""))))

    groups: dict[str, list[int]] = collections.defaultdict(list)
    for idx, r in enumerate(records):
        root = uf.find(str(r["_base"]))
        groups[root].append(idx)

    # ---- group metadata ----
    group_meta = {}
    for root, idxs in groups.items():
        recs = [records[i] for i in idxs]
        bases = sorted({r["_base"] for r in recs})
        cats = collections.Counter(r.get("category") for r in recs)
        cat = cats.most_common(1)[0][0]
        chem = any(len(normalize_chemicals(r)) > 0 for r in recs)
        sources = {str(r.get("source_document")) for r in recs if r.get("source_document")}
        group_meta[root] = {
            "bases": bases,
            "qtypes": sorted({str(r.get("qtype")) for r in recs}),
            "category": cat,
            "category_group": CATEGORY_GROUPS.get(cat or "", "other"),
            "chemical": chem,
            "sources": sorted(sources),
            "n_records": len(idxs),
            "n_cells": len({str(r.get("cell_id")) for r in recs}),
        }

    # ---- stratified deterministic assignment ----
    strata: dict[tuple[str, bool], list[str]] = collections.defaultdict(list)
    for root, m in group_meta.items():
        strata[(m["category_group"], m["chemical"])].append(root)

    rng = random.Random(args.seed)
    assignment: dict[str, str] = {}
    stratum_report = {}
    for key in sorted(strata):
        roots = sorted(strata[key])
        rng.shuffle(roots)
        n = len(roots)
        n_train = round(n * args.train)
        n_dev = round(n * args.dev)
        for i, root in enumerate(roots):
            if i < n_train:
                assignment[root] = "train"
            elif i < n_train + n_dev:
                assignment[root] = "dev"
            else:
                assignment[root] = "test"
        stratum_report[f"{key[0]}|chem={int(key[1])}"] = {
            "groups": n, "train": sum(1 for r in roots[:n_train]),
            "dev": sum(1 for r in roots[n_train:n_train + n_dev]),
            "test": n - n_train - n_dev,
        }

    # ---- write split files ----
    split_buckets = {s: [] for s in ("train", "dev", "test")}
    for idx, r in enumerate(records):
        root = uf.find(str(r["_base"]))
        split = assignment[root]
        rec = dict(r)
        rec["t09_split"] = split
        rec["t09_group"] = root
        rec["t09_group_key"] = f"{root}|{split}"
        rec["schema_version"] = SCHEMA_GUIDELINE["schema_version"]
        rec["guideline_version"] = SCHEMA_GUIDELINE["guideline_version"]
        split_buckets[split].append(rec)

    artifacts_root = Path(__file__).resolve().parents[1]  # research_artifacts/
    manifest = {
        "manifest_version": "1",
        "tool": TOOL_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": {"path": str(args.input), "sha256": sha256_file(args.input), "records": len(records)},
        "method": ("stratified group-level split; union-find group = base intent (cell_id minus qtype suffix) "
                   "∪ exact-question ∪ normalized-question; stratum=(category_group, chemical_bearing)"),
        "seed": args.seed,
        "proportions": {"train": args.train, "dev": args.dev, "test": args.test},
        "grouping": {
            "unit": "union-find {base_intent, exact_question, norm_question}",
            "groups_total": len(groups),
            "groups_with_multiple_bases": sum(1 for m in group_meta.values() if len(m["bases"]) > 1),
            "groups_with_multiple_sources": sum(1 for m in group_meta.values() if len(m["sources"]) > 1),
            "source_documents": len({doc for m in group_meta.values() for doc in m["sources"]}),
        },
        "strata": stratum_report,
        "splits": {},
        "schema_guideline": SCHEMA_GUIDELINE,
    }
    for s in ("train", "dev", "test"):
        p = out_dir / f"T09_treatment_qa_{s}_v1.jsonl"
        with open(p, "w", encoding="utf-8") as f:
            for rec in split_buckets[s]:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        try:
            rel_path = str(p.relative_to(artifacts_root))
        except ValueError:
            rel_path = str(p)
        manifest["splits"][s] = {
            "path": rel_path,
            "records": len(split_buckets[s]),
            "groups": len({r["t09_group"] for r in split_buckets[s]}),
            "sha256": sha256_file(p),
            "size_bytes": p.stat().st_size,
        }

    manifest_path = out_dir / "T09_split_manifest_v1.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"input: records={len(records)} sha256={manifest['input']['sha256'][:12]}...")
    print(f"groups: {len(groups)} total; multi-base groups: {manifest['grouping']['groups_with_multiple_bases']}; "
          f"multi-source groups: {manifest['grouping']['groups_with_multiple_sources']}")
    for s in ("train", "dev", "test"):
        m = manifest["splits"][s]
        print(f"  {s}: records={m['records']} groups={m['groups']} sha256={m['sha256'][:12]}...")
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
