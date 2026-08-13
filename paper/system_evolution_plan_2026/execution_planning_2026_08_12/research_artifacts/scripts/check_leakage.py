#!/usr/bin/env python3
"""T09 leakage checker v2 — near-duplicate report across frozen splits.

Checks, for every pair of records in DIFFERENT splits:
  1. exact_question           — byte equality of question
  2. norm_question            — NFKC + casefold + whitespace-collapse equality
  3. norm_nodigits_question   — norm_question with digits masked (#)
  4. exact_answer             — byte equality of answer
  5. norm_answer              — normalized answer equality

GATE (STOP on leakage): any shared text under exact_question or norm_question.
Those are intent-level checks: per the frozen split rule all forms of one intent
must stay in one split. Answer-templating matches (exact_answer/norm_answer) are
reported as a data-quality finding for expert sign-off, not an auto-stop.

Counting: DISTINCT shared texts, plus per-text record coverage per split (not
pair-wise), so numbers are interpretable.

Outputs:
  - JSON:     research_artifacts/reports/T09_leakage_report_v1.json
  - Markdown: research_artifacts/reports/T09_leakage_report_v1.md
Exit code 0 = no intent leakage; 1 = intent leakage (STOP per T09 gate).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

DIGIT_RE = re.compile(r"\d")
INTENT_CHECKS = ("exact_question", "norm_question")


def load(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def main() -> int:
    ap = argparse.ArgumentParser(description="T09 leakage checker v2.")
    ap.add_argument("--splits", nargs="+", type=Path, required=True, help="train/dev/test jsonl files")
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()

    out_dir = args.out_dir or (Path(__file__).resolve().parents[1] / "reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    loaded = [(p.name, load(p)) for p in args.splits]
    report = {
        "tool": "check_leakage.py v2",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": {name: len(recs) for name, recs in loaded},
        "checks": {},
        "intent_leakage_found": False,
        "samples": {},
    }

    def fingerprint(recs):
        f = {"exact_question": {}, "norm_question": {}, "norm_nodigits_question": {},
             "exact_answer": {}, "norm_answer": {}}
        for idx, r in enumerate(recs):
            q, a = r.get("question", ""), r.get("answer", "")
            nq = norm(q)
            cell = r.get("t09_group")
            f["exact_question"].setdefault(q, []).append((idx, cell))
            f["norm_question"].setdefault(nq, []).append((idx, cell))
            f["norm_nodigits_question"].setdefault(DIGIT_RE.sub("#", nq), []).append((idx, cell))
            f["exact_answer"].setdefault(a, []).append((idx, cell))
            f["norm_answer"].setdefault(norm(a), []).append((idx, cell))
        return f

    for i in range(len(loaded)):
        for j in range(i + 1, len(loaded)):
            name_i, recs_i = loaded[i]
            name_j, recs_j = loaded[j]
            key = f"{name_i} vs {name_j}"
            fp_a, fp_b = fingerprint(recs_i), fingerprint(recs_j)

            for check in ("exact_question", "norm_question", "norm_nodigits_question",
                          "exact_answer", "norm_answer"):
                shared = sorted(set(fp_a[check]) & set(fp_b[check]))
                if "" in shared:
                    shared.remove("")
                entries = []
                for text in shared:
                    entries.append({
                        "text": text[:160],
                        "records_in_a": len(fp_a[check][text]),
                        "records_in_b": len(fp_b[check][text]),
                        "cells_in_a": len({c for _, c in fp_a[check][text]}),
                        "cells_in_b": len({c for _, c in fp_b[check][text]}),
                    })
                report["checks"].setdefault(key, {})[check] = {
                    "distinct_texts": len(entries),
                    "records_a_covered": sum(e["records_in_a"] for e in entries),
                    "records_b_covered": sum(e["records_in_b"] for e in entries),
                }
                if check in INTENT_CHECKS and entries:
                    report["intent_leakage_found"] = True
                    report["samples"].setdefault(key, {})[check] = entries[:5]
                elif entries:
                    report["samples"].setdefault(key, {})[check] = entries[:5]

    report_path = out_dir / "T09_leakage_report_v1.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    md_path = out_dir / "T09_leakage_report_v1.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# T09 Leakage Report v1\n\n")
        f.write(f"- Tool: `check_leakage.py v2`\n- Generated (UTC): {report['generated_at_utc']}\n")
        f.write(f"- **Intent-level leakage (exact/norm question across splits): "
                f"{report['intent_leakage_found']}**\n\n")
        f.write("| Split pair | Check | Distinct texts | Records covered (A/B) |\n")
        f.write("|---|---|---|---|\n")
        for key, checks in sorted(report["checks"].items()):
            for check, c in checks.items():
                if c["distinct_texts"]:
                    f.write(f"| {key} | {check} | {c['distinct_texts']} | "
                            f"{c['records_a_covered']}/{c['records_b_covered']} |\n")
        f.write("\nSamples (up to 5 per check):\n\n")
        for key, checks in sorted(report.get("samples", {}).items()):
            for check, samples in checks.items():
                for s in samples:
                    f.write(f"- `{key}` [{check}] in A={s['records_in_a']} recs / B={s['records_in_b']} recs: "
                            f"`{s['text'][:100]}`\n")
        f.write("\nNotes:\n- Intent checks (exact/norm question) gate the split: any hit = STOP.\n"
                "- Answer-templating matches are reported as a data-quality finding for expert sign-off.\n"
                "- Same-group variants (qtype/dialect forms of one intent) are intentionally in one split.\n")

    print(f"intent_leakage_found={report['intent_leakage_found']}")
    for key, checks in sorted(report["checks"].items()):
        lines = ", ".join(f"{c}: {v['distinct_texts']} texts" for c, v in sorted(checks.items()) if v["distinct_texts"])
        print(f"  {key}: {lines or 'clean'}")
    print(f"report: {report_path}")
    return 1 if report["intent_leakage_found"] else 0


if __name__ == "__main__":
    raise SystemExit(main())