"""11 — Publish P4 golden-benchmark stats (kappa, per-category, refusal rate).

Reads golden_runs_v1.json (mechanical pipeline outputs) and, when both
evaluators have filled scoring_sheet_v1.csv, computes:

  - inter-evaluator agreement: raw agreement + Cohen's kappa on the 4-value
    score (correct/partial/unsupported/refused);
  - per-category results (n, score counts, correct rate);
  - unanswerable refusal rate: mechanical (pipeline refused) and
    evaluator-validated (both evaluators scored the item "refused");
  - disagreement log (rows where evaluator scores differ).

Before scores exist it emits an honest `pending_scores` state — no invented
numbers, ever. The same payload is written to
`frontend/src/lib/golden_stats.json` for the static research panel.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent
OUT_DIR = BACKEND_ROOT.parent / "dataset_release" / "benchmark"
FRONTEND_LIB = BACKEND_ROOT.parent / "frontend" / "src" / "lib"
RUNS = OUT_DIR / "golden_runs_v1.json"
SHEET = OUT_DIR / "scoring_sheet_v1.csv"
STATS = OUT_DIR / "golden_stats_v1.json"
FRONTEND_STATS = FRONTEND_LIB / "golden_stats.json"

SCORES = ("correct", "partial", "unsupported", "refused")


def cohens_kappa(a: list[str], b: list[str]) -> float:
    """Cohen's kappa for two raters over the fixed score set."""
    n = len(a)
    if n == 0:
        return 0.0
    ca, cb = Counter(a), Counter(b)
    p_o = sum(1 for x, y in zip(a, b) if x == y) / n
    p_e = sum((ca[s] / n) * (cb[s] / n) for s in SCORES)
    if p_e >= 1.0:  # both raters used a single category — agreement is trivial
        return 1.0 if p_o >= 1.0 else 0.0
    return (p_o - p_e) / (1 - p_e)


def load_scores() -> list[dict]:
    rows: list[dict] = []
    with SHEET.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            e1 = row.get("eval1_score", "").strip().lower()
            e2 = row.get("eval2_score", "").strip().lower()
            if e1 or e2:
                if e1 not in SCORES or e2 not in SCORES:
                    raise SystemExit(f"invalid score in row {row['row_id']}: {e1!r}/{e2!r}")
                rows.append({
                    "row_id": row["row_id"],
                    "category": row["category"],
                    "refused_mechanical": row.get("model_refused", "no").strip().upper() == "YES",
                    "e1": e1, "e2": e2,
                    "cat_ok": (row.get("eval1_category_ok", "").strip().upper(), row.get("eval2_category_ok", "").strip().upper()),
                })
    return rows


def mechanical_stats(runs: list[dict]) -> dict:
    by_cat: dict[str, Counter] = {}
    for run in runs:
        by_cat.setdefault(run["category"], Counter())["n"] += 1
        by_cat[run["category"]]["refused"] += 1 if run["refusal"] else 0
        by_cat[run["category"]]["verified"] += 1 if run["verifier_confidence"] == "verified" else 0
    unans = by_cat.get("unanswerable", Counter())
    n_un = unans["n"]
    return {
        "per_category": {k: dict(v) for k, v in sorted(by_cat.items())},
        "unanswerable_refusal_rate": round(unans["refused"] / n_un, 3) if n_un else None,
        "note": "mechanical pipeline behavior; human scores are the authoritative judgment",
    }


def main() -> None:
    runs = json.loads(RUNS.read_text(encoding="utf-8"))
    base = {
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "items": len(runs),
        "source": "dataset_release/benchmark/golden_qa_v1.jsonl (46 real farmer queries, 3-pass human-reviewed categories)",
        "evaluators": 2,
        "mechanical": mechanical_stats(runs),
    }
    scored = load_scores()
    if not scored:
        payload = {
            **base,
            "status": "pending_scores",
            "note": "Scoring sheet not filled yet — the two evaluators score each item (correct/partial/unsupported/refused) per scoring_rubric_v1.md; this file then updates automatically.",
        }
        for path in (STATS, FRONTEND_STATS):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"pending state -> {STATS} and {FRONTEND_STATS}")
        return

    per_cat: dict[str, Counter] = {}
    disagreements: list[dict] = []
    refusal_validated = 0
    unans_n = 0
    for row in scored:
        cat = row["category"]
        per_cat.setdefault(cat, Counter())["n"] += 1
        per_cat[cat][row["e1"]] += 1
        per_cat[cat][row["e2"]] += 1
        if row["e1"] != row["e2"]:
            disagreements.append({"row_id": row["row_id"], "e1": row["e1"], "e2": row["e2"]})
        if cat in ("unanswerable", "off_topic"):
            unans_n += 1
            if row["e1"] == "refused" and row["e2"] == "refused":
                refusal_validated += 1

    e1 = [r["e1"] for r in scored]
    e2 = [r["e2"] for r in scored]
    kappa = cohens_kappa(e1, e2)
    raw_agreement = sum(1 for x, y in zip(e1, e2) if x == y) / len(scored)

    category_results = {}
    for cat, counts in sorted(per_cat.items()):
        n = counts["n"]
        correct = counts["correct"] + counts["partial"]  # useful+correct content
        safe = counts["correct"] + counts["partial"] + (counts["refused"] if cat in ("unanswerable", "off_topic") else 0)
        category_results[cat] = {
            "n": n,
            **{s: counts[s] for s in SCORES},
            "correct_rate": round(correct / n, 3),
            "acceptable_rate": round(safe / n, 3),
        }

    payload = {
        **base,
        "status": "scored",
        "kappa": round(kappa, 3),
        "raw_agreement": round(raw_agreement, 3),
        "category_results": category_results,
        "unanswerable_refusal_rate_mechanical": base["mechanical"]["unanswerable_refusal_rate"],
        "unanswerable_refusal_rate_validated": round(refusal_validated / unans_n, 3) if unans_n else None,
        "disagreements": disagreements,
        "disagreement_count": len(disagreements),
    }
    for path in (STATS, FRONTEND_STATS):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"saved -> {STATS} and {FRONTEND_STATS}")


if __name__ == "__main__":
    main()