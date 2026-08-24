"""F1-02 offline extractor: build the dose-reference artifact from the corpus.

Deterministic — same corpus yields a byte-identical JSON (sorted, no
timestamps). Run once after a corpus rebuild:

    uv run python scripts/build_dose_reference.py [--output PATH] [--print]

Every entry is extracted from a corpus node and carries its citation
(AGENTS.md §2.5: no fabricated data). The runtime loader lives in
``app.infrastructure.verification.dose_reference``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.infrastructure.verification.dose_reference import (  # noqa: E402
    build_dose_reference_entries,
)

DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1] / "ml_assets" / "rag_index" / "derived" / "dose_reference_v1.json"
)
DEFAULT_CORPUS = (
    Path(__file__).resolve().parents[1]
    / "ml_assets"
    / "rag_index"
    / "processed"
    / "knowledge_nodes_clean.jsonl"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--print", action="store_true", help="print every entry for review")
    args = parser.parse_args()

    entries = build_dose_reference_entries(args.corpus)
    payload = {
        "version": 1,
        "generator": "backend/scripts/build_dose_reference.py",
        "source_corpus": "processed/knowledge_nodes_clean.jsonl",
        "notes": (
            "Entries extracted offline from corpus nodes that pair a pesticide "
            "active with a numeric spray/field rate. Rates are crop- and "
            "product-specific recommendations from the cited source; the "
            "runtime check only flags gross outliers (>=3x the band max)."
        ),
        "entries": [e.as_dict() for e in entries],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    by_active: dict[str, int] = {}
    for e in entries:
        by_active[e.active] = by_active.get(e.active, 0) + 1
    print(f"wrote {len(entries)} entries for {len(by_active)} actives -> {args.output}")
    for active in sorted(by_active):
        print(f"  {active}: {by_active[active]}")
    if args.print:
        for e in entries:
            print(f"[{e.active}] {e.rate:g} {e.band} | {e.snippet} | {e.citation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
