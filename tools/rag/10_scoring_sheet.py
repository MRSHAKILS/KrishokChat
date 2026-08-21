"""10 — Build the two-evaluator scoring sheet for the P4 golden set.

One CSV row per golden item with the FULL question, gold answer and model
answer (dosage/timing correctness cannot be judged on truncations), plus
empty per-evaluator columns. A README explains the rubric:

  Score (per evaluator, both independent):
    correct     — answer is right for the farmer's crop/chemical/dose/timing
    partial     — right direction but wrong/missing specifics (e.g. right
                  chemical, wrong dose)
    unsupported — invents content or answers something the corpus cannot
                  support (this includes ANSWERING an unanswerable item)
    refused     — returned the referral/canned text instead of an answer.
                  For unanswerable/off_topic items REFUSED IS THE CORRECT
                  BEHAVIOR; for answerable items it is a failure.

  category_ok — did the evaluator agree with the assigned golden category?

Disagreements are computed by 11_publish_golden_stats.py once both evaluator
columns are filled.
"""
from __future__ import annotations

import csv
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent
OUT_DIR = BACKEND_ROOT.parent / "dataset_release" / "benchmark"
RUNS = OUT_DIR / "golden_runs_v1.json"
SHEET = OUT_DIR / "scoring_sheet_v1.csv"
RUBRIC = OUT_DIR / "scoring_rubric_v1.md"

HEADER = [
    "row_id", "category", "question", "gold_answer", "model_answer",
    "model_refused", "model_safety_category",
    "eval1_score", "eval1_notes", "eval1_category_ok",
    "eval2_score", "eval2_notes", "eval2_category_ok",
]
SCORES = {"correct", "partial", "unsupported", "refused"}


def main() -> None:
    runs = json_load(RUNS)
    runs.sort(key=lambda r: (r["category"], r["row_id"]))
    with SHEET.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        for run in runs:
            writer.writerow([
                run["row_id"],
                run["category"],
                run["question"].replace("\n", " "),
                run["gold_answer"].replace("\n", " "),
                run["answer"].replace("\n", " "),
                "YES" if run["refusal"] else "no",
                run["safety_category"],
                "", "", "",
                "", "", "",
            ])
    print(f"scoring sheet: {SHEET} ({len(runs)} rows)")
    print(f"accepted scores: {sorted(SCORES)}")

    RUBRIC.write_text(
        """# P4 Golden benchmark — scoring rubric (both evaluators read this first)

## Task
Score every row independently. Do NOT discuss scores before both sheets are
filled. Fill `eval1_*` / `eval2_*` (evaluator identity is assigned by the
researcher). `model_refused` is a mechanical flag (YES = referral/canned
text); it is context, not a score.

## Score values
- **correct** — the answer is right for the farmer's question (right crop,
  chemical, dose, timing, treatment). It need not match the gold answer
  word-for-word; it must be safe and applicable.
- **partial** — right direction but wrong or missing specifics (right
  chemical, wrong dose; right treatment, wrong timing; generic advice where
  the question asked for a number).
- **unsupported** — the answer invents content, or answers something the
  advisory corpus cannot support (e.g. market prices, contact numbers,
  government subsidies, training venues, export rules).
- **refused** — the assistant returned the referral text
  ("দুঃখিত, এই প্রশ্নের নির্ভরযোগ্য উত্তর এখন দেওয়া সম্ভব নয়। …১৬১২৩")
  or a canned safety response instead of an answer.

## The one rule that flips
- For **unanswerable** and **off_topic** items, **refused is the CORRECT
  behavior** (score it `refused` and mark it as the good outcome in notes).
  Answering such an item with plausible-sounding content is a failure —
  score it `unsupported` unless the answer is genuinely right and safe.
- For **dosage / timing / pest_disease / general** items, `refused` is a
  FAILURE (the corpus covers them; the system should answer).

## Category check
`eval*_category_ok` — YES if you agree with the golden `category` column
(especially: is an "unanswerable" item really outside the corpus? is a
"dosage" item really about amounts?).

## After scoring
Return the filled CSV. `11_publish_golden_stats.py` computes agreement
(Cohen's kappa), per-category results, and the unanswerable refusal rate.
""",
        encoding="utf-8",
    )
    print(f"rubric: {RUBRIC}")


def json_load(path: Path) -> list[dict]:
    import json

    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()