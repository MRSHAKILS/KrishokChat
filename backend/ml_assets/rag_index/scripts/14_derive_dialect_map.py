"""14_derive_dialect_map.py — derive a genuine dialect->standard word map (C3).

The original Gemini-generated 110-word map (phase4_dialect_map.json) is
unrecoverable (absent from workspace and git history). This script rebuilds a
REAL map deterministically from the frozen, reviewed T09 treatment-QA splits
(paper/.../research_artifacts/datasets/frozen/), where each cell_id has the
same question rendered in several dialects plus a standard variant.

Method (no LLM, no fabrication):
  1. Load T09 train/dev/test splits; group records by cell_id.
  2. For each cell containing a `standard` variant, tokenize the standard
     question and each dialect question; align token sequences with
     difflib.SequenceMatcher.
  3. Keep only 1:1 single-token 'replace' blocks (dialect token -> standard
     token); dedupe per (cell, dialect label).
  4. Frequency filter: the pair must appear in >= 2 distinct cells.
  5. Quality filters: both tokens must be pure Bengali script; dialect token
     must not equal or contain the standard token (orthographic variants are
     dropped); drop 1-char dialect tokens (noise).
  6. Emit dataset_release/safety/phase4_dialect_map.json as
     {"map": {"dialect_term": "standard_term"}, "meta": {lineage}} — the
     QueryExpander reads data.get("map", data), so the meta key is ignored
     safely at runtime.

Runtime wiring: expansion.py appends the standard Bengali term to the query
before embedding/BM25 — this is dialect->standard normalization, which lifts
the dense (BGE-M3, multilingual) channel; the claim stays scoped to that.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # backend/ (scripts/rag_index/ml_assets/backend)
ARTIFACTS = (
    ROOT.parent
    / "paper"
    / "system_evolution_plan_2026"
    / "execution_planning_2026_08_12"
    / "research_artifacts"
)
FROZEN = ARTIFACTS / "datasets" / "frozen"
SPLITS = ["T09_treatment_qa_train_v1.jsonl", "T09_treatment_qa_dev_v1.jsonl", "T09_treatment_qa_test_v1.jsonl"]
OUT = ROOT.parent / "dataset_release" / "safety" / "phase4_dialect_map.json"
AUDIT = ROOT / "ml_assets" / "rag_index" / "eval" / "dialect_map_derivation_audit_v1.json"

BENGALI_RE = re.compile(r"^[\u0980-\u09FF]+$")
_TOKEN_RE = re.compile(r"[\u0980-\u09FF]+|[A-Za-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text)


def main() -> int:
    cells: dict[str, dict[str, str]] = {}  # cell_id -> {dialect_label: question}
    standard_tokens: set[str] = set()  # every token seen in any standard question
    for split in SPLITS:
        path = FROZEN / split
        if not path.exists():
            print(f"SKIP missing split: {path}")
            continue
        with open(path, encoding="utf-8") as h:
            for line in h:
                rec = json.loads(line)
                cell = rec.get("cell_id") or ""
                dialect = rec.get("dialect") or ""
                question = rec.get("question") or ""
                if cell and dialect and question:
                    cells.setdefault(cell, {})[dialect] = question
                    if dialect == "standard":
                        standard_tokens.update(tokenize(question))
    print(f"cells loaded: {len(cells)}; distinct standard tokens: {len(standard_tokens)}")

    pair_counts: Counter[tuple[str, str]] = Counter()
    pair_cells: dict[tuple[str, str], list[str]] = defaultdict(list)
    by_dialect: Counter[tuple[str, str, str]] = Counter()
    dropped = Counter()

    for cell, variants in cells.items():
        standard = variants.get("standard")
        if not standard:
            dropped["cell_no_standard"] += 1
            continue
        std_tokens = tokenize(standard)
        for dialect_label, question in variants.items():
            if dialect_label == "standard":
                continue
            dial_tokens = tokenize(question)
            sm = SequenceMatcher(a=std_tokens, b=dial_tokens, autojunk=False)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op != "replace" or (i2 - i1) != 1 or (j2 - j1) != 1:
                    continue
                # Flanking-context rule: the substitution must be local — both
                # neighboring tokens must match identically on each side.
                # Kills reorder artifacts (e.g. "এর -> গাছে" from moved words).
                if not (i1 > 0 and j1 > 0 and i2 < len(std_tokens) and j2 < len(dial_tokens)):
                    dropped["no_flanking_context"] += 1
                    continue
                if std_tokens[i1 - 1] != dial_tokens[j1 - 1] or std_tokens[i2] != dial_tokens[j2]:
                    dropped["no_flanking_context"] += 1
                    continue
                std_tok = std_tokens[i1]
                dial_tok = dial_tokens[j1]
                if not (BENGALI_RE.match(dial_tok) and BENGALI_RE.match(std_tok)):
                    dropped["non_bengali_script"] += 1
                    continue
                if dial_tok == std_tok:
                    dropped["identical"] += 1
                    continue
                if dial_tok in std_tok or std_tok in dial_tok:
                    dropped["substring_orthographic_variant"] += 1
                    continue
                if len(dial_tok) <= 1:
                    dropped["single_char_dialect"] += 1
                    continue
                if dial_tok in standard_tokens:
                    # The "dialect" form is itself standard Bengali elsewhere —
                    # the alignment is cross-cell standard variation, not a
                    # dialect->standard mapping. Drop it.
                    dropped["dialect_token_is_standard"] += 1
                    continue
                key = (dial_tok, std_tok)
                pair_counts[key] += 1
                pair_cells[key].append(cell)
                by_dialect[(dial_tok, std_tok, dialect_label)] += 1

    # Frequency filter: >= 2 distinct cells. Then, per dialect token, keep the
    # top standard target only if it dominates (>= 2x the runner-up) — the map
    # is a dict (one term -> one target), so ambiguous terms are dropped or
    # resolved by dominance, never silently truncated.
    by_term: dict[str, Counter[str]] = defaultdict(Counter)
    term_cells: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    term_dialects: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for (dial_tok, std_tok), count in pair_counts.items():
        cells_used = set(pair_cells[(dial_tok, std_tok)])
        if len(cells_used) < 2:
            continue
        by_term[dial_tok][std_tok] += count
        term_cells[dial_tok][std_tok] |= cells_used
        term_dialects[dial_tok][std_tok] |= {
            d for (d_tok, s_tok, d) in by_dialect if (d_tok, s_tok) == (dial_tok, std_tok)
        }

    kept: dict[tuple[str, str], dict] = {}
    dropped["below_freq_2"] = len(pair_counts) - sum(len(c) for c in by_term.values())
    for dial_tok, targets in by_term.items():
        ranked = targets.most_common()
        best_tok, best_count = ranked[0]
        runner_up = ranked[1][1] if len(ranked) > 1 else 0
        if len(ranked) > 1 and best_count < 2 * runner_up:
            dropped["ambiguous_term_no_dominance"] += len(ranked)
            continue
        key = (dial_tok, best_tok)
        kept[key] = {
            "cells": len(term_cells[dial_tok][best_tok]),
            "occurrences": best_count,
            "dialects": sorted(term_dialects[dial_tok][best_tok]),
        }

    map_dict = {dial: std for (dial, std) in kept}
    meta = {
        "derived_from": [str(FROZEN / s) for s in SPLITS],
        "method": ("difflib 1:1 token replace alignment between dialect and "
                   "standard variants of the same cell_id; pairs require >=2 "
                   "distinct cells; pure Bengali script; no LLM; no fabrication"),
        "pairs": len(map_dict),
        "dialect_labels": sorted({d for v in kept.values() for d in v["dialects"]}),
        "runtime": "QueryExpander appends the standard Bengali term to the query "
                   "before retrieval (dialect->standard normalization for the dense channel).",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"map": map_dict, "meta": meta}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    audit = {
        "input": {"splits": [s for s in SPLITS], "cells": len(cells)},
        "dropped": dict(dropped),
        "kept_pairs": len(kept),
        "output": str(OUT),
    }
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"kept pairs: {len(map_dict)}")
    for (dial, std), info in sorted(kept.items(), key=lambda kv: -kv[1]["occurrences"])[:30]:
        print(f"  {dial} -> {std}  cells={info['cells']} occ={info['occurrences']} dialects={info['dialects']}")
    print(f"dropped: {dict(dropped)}")
    print(f"written: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())