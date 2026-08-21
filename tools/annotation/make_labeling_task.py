"""Stage A3 helper: generate blind per-annotator labeling tasks from a pilot JSONL.

Reads the frozen T08 pilot items and writes one task file per annotator with
identical item sets in independently shuffled orders (so annotators cannot
align on row position), an empty label field, and no answer-key leakage.

Usage:
  python tools/annotation/make_labeling_task.py \
      --pilot research_artifacts/annotations/pilot/T08_pilot_items_v1.jsonl \
      --out-dir research_artifacts/annotations/labels \
      --annotators annotator_A,annotator_B \
      [--label-field label] [--seed 20260813]

The output rows keep every pilot field except `annotators`, plus
"<label-field>": null for the annotator to fill in.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--annotators", default="annotator_A,annotator_B")
    parser.add_argument("--label-field", default="label")
    parser.add_argument("--seed", type=int, default=20260813)
    args = parser.parse_args()

    items = [
        json.loads(line)
        for line in open(args.pilot, encoding="utf-8")
        if line.strip()
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for offset, name in enumerate(a.strip() for a in args.annotators.split(",")):
        rng = random.Random(args.seed + offset)
        rows = []
        for item in items:
            row = {k: v for k, v in item.items() if k != "annotators"}
            row[args.label_field] = None
            rows.append(row)
        rng.shuffle(rows)
        out = args.out_dir / f"task_{name}.jsonl"
        with open(out, "w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"wrote {out} ({len(rows)} items)")

    ids_per_annotator = []
    for name in (a.strip() for a in args.annotators.split(",")):
        path = args.out_dir / f"task_{name}.jsonl"
        ids = [json.loads(line)["item_id"] for line in open(path, encoding="utf-8")]
        ids_per_annotator.append(set(ids))
    assert all(s == ids_per_annotator[0] for s in ids_per_annotator), "item sets diverged"
    print(f"verified: identical item sets across {len(ids_per_annotator)} tasks")


if __name__ == "__main__":
    main()
