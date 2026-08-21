#!/usr/bin/env python3
"""T08 pilot item sampler — deterministic stratified sample for the annotation pilot.

Pool: DEVELOPMENT and TRAIN groups only. TEST data is never touched by piloting
(no test-informed label tuning). One record per chosen group (records inside a
group are near-duplicate variants, so one representative keeps the pilot items
independent). Prefers a 'standard' dialect record when the group has one.

Strata (24 items):
  disease+chem   6
  pest+chem      6
  fertilizer+chem 6
  non-chem (disease/pest/ipm/fertilizer without chemical_trace) 4
  other (seed_tech/food_safety/herbicide)                       2

Evidence: reads the record's source_md file if reachable and attaches the first
EVIDENCE_CHARS chars with a content SHA-256 so each pilot item is self-contained
(labelers do not need the full corpus).

Output: research_artifacts/annotations/pilot/T08_pilot_items_v1.jsonl
Every item requires later annotation per T07_label_manual_v1; labels keep
annotator ID, timestamps, and adjudication lineage (T07 section 6).
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import sys
from pathlib import Path

TOOL_VERSION = "sample_pilot_items.py v1"
EVIDENCE_CHARS = 4000
STRATA = [
    ("disease+chem", "disease", True, 6),
    ("pest+chem", "pest", True, 6),
    ("fertilizer+chem", "fertilizer", True, 6),
    ("non-chem", None, False, 4),
    ("other", None, None, 2),  # seed_tech/food_safety/herbicide, chem irrelevant
]
NONCHEM_CATEGORIES = {"disease", "pest", "ipm", "fertilizer"}
OTHER_CATEGORIES = {"seed_tech", "food_safety", "herbicide"}
PREFERRED_DIALECT = "standard"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def chemicals(rec: dict) -> list[str]:
    ct = rec.get("chemical_trace")
    if not ct:
        return []
    if isinstance(ct, list):
        return [str(c) for c in ct]
    if isinstance(ct, str) and ct.strip():
        try:
            parsed = json.loads(ct)
            return [str(c) for c in parsed] if isinstance(parsed, list) else [ct]
        except json.JSONDecodeError:
            return [ct]
    return []


def stratum_of(rec: dict) -> str | None:
    cat = str(rec.get("category") or "")
    chem = bool(chemicals(rec))
    if cat in OTHER_CATEGORIES:
        return "other"
    if cat == "disease" and chem:
        return "disease+chem"
    if cat == "pest" and chem:
        return "pest+chem"
    if cat == "fertilizer" and chem:
        return "fertilizer+chem"
    if cat in NONCHEM_CATEGORIES and not chem:
        return "non-chem"
    return None  # e.g., disease without chem is already handled; anything else skipped


def pick_representative(recs: list[dict]) -> dict:
    std = [r for r in recs if r.get("dialect") == PREFERRED_DIALECT]
    pool = std or recs
    return sorted(pool, key=lambda r: (str(r.get("cell_id", "")), str(r.get("dialect", ""))))[0]


def main() -> int:
    ap = argparse.ArgumentParser(description="T08 pilot item sampler.")
    ap.add_argument("--train", type=Path, default=None)
    ap.add_argument("--dev", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--seed", type=int, default=20260813)
    args = ap.parse_args()

    splits_dir = (Path(__file__).resolve().parents[1] / "datasets" / "frozen")
    train_p = args.train or (splits_dir / "T09_treatment_qa_train_v1.jsonl")
    dev_p = args.dev or (splits_dir / "T09_treatment_qa_dev_v1.jsonl")
    out_dir = args.out_dir or (Path(__file__).resolve().parents[1] / "annotations" / "pilot")
    out_dir.mkdir(parents=True, exist_ok=True)

    dev_recs, train_recs = load(dev_p), load(train_p)
    rng = random.Random(args.seed)

    # group records by stratum; dev first, train as fallback
    def buckets(recs):
        b = collections.defaultdict(list)
        for r in recs:
            s = stratum_of(r)
            if s:
                b[s].append(r)
        return b

    dev_b, train_b = buckets(dev_recs), buckets(train_recs)

    items = []
    summary = {}
    for (sname, cat, chem, quota) in STRATA:
        dev = sorted(set(r["t09_group"] for r in dev_b.get(sname, []) if r["t09_group"]))
        train_extra = sorted(set(r["t09_group"] for r in train_b.get(sname, []) if r["t09_group"]) - set(dev))
        dev_order, train_extra_order = dev[:], train_extra[:]
        rng.shuffle(dev_order)
        rng.shuffle(train_extra_order)
        order = dev_order + train_extra_order  # strict dev-first; train only as fallback
        picked = 0
        for g in order:
            pool_dev = [r for r in dev_b.get(sname, []) if r["t09_group"] == g] if g in dev else []
            pool_train = [r for r in train_b.get(sname, []) if r["t09_group"] == g] if not pool_dev else []
            if not pool_dev and not pool_train:
                continue
            rec = pick_representative(pool_dev or pool_train)
            items.append((rec, sname))
            picked += 1
            if picked >= quota:
                break
        summary[sname] = {"available_groups_dev": len(dev), "available_groups_train": len(train_extra), "picked": picked}

    # ---- build output items ----
    out_items = []
    for idx, (rec, sname) in enumerate(sorted(items, key=lambda t: (t[1], t[0]["t09_group"])), start=1):
        smd = rec.get("source_md")
        evidence_status, evidence_text, content_hash, ev_path = "missing", "", None, None
        if smd:
            p = Path(str(smd))
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8", errors="replace") as f:
                        body = f.read()
                    evidence_text = body[:EVIDENCE_CHARS]
                    content_hash = sha256_file(p)
                    evidence_status = "attached"
                    ev_path = str(p)
                except OSError as e:
                    evidence_status = f"unreadable: {type(e).__name__}"
            else:
                evidence_status = "missing_file"

        item = {
            "item_id": f"PILOT-{idx:04d}",
            "pilot_version": "T08_pilot_v1",
            "schema_version": "T07_claim_schema_v1",
            "guideline_version": "T07_label_manual_v1",
            "split_pool": "dev" if rec["t09_split"] == "dev" else "train",
            "stratum": sname,
            "t09_group": rec["t09_group"],
            "cell_id": rec.get("cell_id"),
            "node_id": rec.get("node_id"),
            "dialect": rec.get("dialect"),
            "category": rec.get("category"),
            "qtype": rec.get("qtype"),
            "query": rec.get("question"),
            "answer": rec.get("answer"),
            "chemical_trace": chemicals(rec),
            "evidence": {
                "source_id": str(rec.get("source_document")),
                "source_document": rec.get("source_document"),
                "source_md": ev_path,
                "citation": rec.get("citation"),
                "publisher": rec.get("publisher"),
                "evidence_status": evidence_status,
                "content_hash": content_hash,
                "evidence_text": evidence_text,
            },
            "annotators": {"annotator_a": None, "annotator_b": None, "adjudicator": None},
        }
        out_items.append(item)

    out_path = out_dir / "T08_pilot_items_v1.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for item in out_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"items written: {out_path}  ({len(out_items)})")
    for sname in [s[0] for s in STRATA]:
        print(f"  {sname}: picked={summary[sname]['picked']} (dev_groups={summary[sname]['available_groups_dev']}, "
              f"train_only_groups={summary[sname]['available_groups_train']})")
    statuses = collections.Counter(i["evidence"]["evidence_status"] for i in out_items)
    print("evidence status:", dict(statuses))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())