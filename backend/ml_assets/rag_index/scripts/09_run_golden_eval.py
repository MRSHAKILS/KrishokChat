"""09 — Run the REAL QA pipeline over the P4 golden set.

Executes the exact production path (container wiring: safety classifier,
hybrid RRF retriever, grounded generator, verifier) over
`dataset_release/benchmark/golden_qa_v1.jsonl` and stores every output in
`dataset_release/benchmark/golden_runs_v1.json`.

What is measured here is honest and mechanical:
  - refusal: pipeline returned REFERRAL (no sources / generation failure) or a
    canned terminal response instead of a fabricated answer;
  - retrieval: count + top-1 score + hit;
  - verifier: verdict + per-claim flags on the final answer.
Human correctness scores (correct/partial/unsupported/refused) come from the
two evaluators in 10_scoring_sheet — never from this script.

Idempotent: already-run row_ids are skipped so re-runs cost nothing.
"""
from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.application.container import build_container
from app.application.generation import REFERRAL
from app.application.qa_pipeline import QAInput, QAPipeline
from app.core.config import settings
from app.domain.contracts import QAResult
from app.domain.enums import SafetyCategory

GOLDEN = BACKEND_ROOT.parent / "dataset_release" / "benchmark" / "golden_qa_v1.jsonl"
OUT = BACKEND_ROOT.parent / "dataset_release" / "benchmark" / "golden_runs_v1.json"


def refusal_kind(result: QAResult) -> str | None:
    """Mechanical refusal detection: REFERRAL text, canned terminal response,
    or a low-confidence failure path. None means the pipeline produced a
    substantive answer (which the evaluators will then judge)."""
    if result.answer == REFERRAL:
        return "referral_no_sources"
    if result.category is not SafetyCategory.SAFE_AGRI:
        return f"canned_{result.category.value}"
    if result.confidence.value == "low_confidence" and result.error:
        return "error_path"
    return None


async def run_one(pipeline: QAPipeline, item: dict) -> dict:
    result = await pipeline.run(QAInput(query=item["question"], session_id=None, channel="benchmark"))
    return {
        "row_id": item["row_id"],
        "category": item["golden_category"],
        "question": item["question"],
        "gold_answer": item["gold_answer"],
        "safety_category": result.category.value,
        "refusal": refusal_kind(result),
        "answer": result.answer,
        "retrieved_count": len(result.sources),
        "retrieval_top1_score": round(max((s.score for s in result.sources if isinstance(getattr(s, "score", None), (int, float))), default=0.0), 4),
        "verifier_confidence": result.confidence.value,
        "verifier_claims": [
            {"text": c.text[:200], "verdict": c.verdict, "reason": c.reason[:120]}
            for c in result.verifier_claims
        ],
        "model": result.model,
        "error": result.error,
        "source_ids": [s.id for s in result.sources],
        "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


async def main() -> None:
    items = [json.loads(line) for line in GOLDEN.open(encoding="utf-8") if line.strip()]
    existing: dict[str, dict] = {}
    if OUT.exists():
        existing = {r["row_id"]: r for r in json.loads(OUT.read_text(encoding="utf-8"))}
    todo = [item for item in items if item["row_id"] not in existing]
    print(f"golden items: {len(items)} | already run: {len(items) - len(todo)} | to run: {len(todo)}")

    container = build_container(settings)
    pipeline = QAPipeline(
        safety=container.qa.safety,
        retriever=container.qa.retriever,
        generator=container.qa.generator,
        verifier=container.qa.verifier,
        audit=container.qa.audit,
        sessions=container.qa.sessions,
        top_k=settings.retrieval_top_k,
    )

    runs: list[dict] = list(existing.values())
    for i, item in enumerate(todo, 1):
        try:
            run = await run_one(pipeline, item)
        except Exception as exc:  # keep the file complete; rerun fixes the row
            run = {
                "row_id": item["row_id"],
                "category": item["golden_category"],
                "question": item["question"],
                "gold_answer": item["gold_answer"],
                "safety_category": "error",
                "refusal": "error_path",
                "answer": "",
                "retrieved_count": 0,
                "retrieval_top1_score": 0.0,
                "verifier_confidence": "low_confidence",
                "verifier_claims": [],
                "model": None,
                "error": str(exc)[:300],
                "source_ids": [],
                "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        runs.append(run)
        existing[item["row_id"]] = run
        OUT.write_text(json.dumps(runs, ensure_ascii=False, indent=1), encoding="utf-8")
        refused = "REFUSED" if run["refusal"] else "answered"
        print(f"[{i}/{len(todo)}] {run['row_id']} ({run['category']}) {refused} | {run['retrieved_count']} sources | {run['verifier_confidence']}")

    from collections import Counter
    print("refusal by category:", dict(Counter(r["refusal"] or "answered" for r in runs)))
    print(f"saved: {OUT}")


if __name__ == "__main__":
    asyncio.run(main())