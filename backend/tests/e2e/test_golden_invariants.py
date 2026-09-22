"""pytest wrapper for the golden replay mechanical invariants (T0-08).

Reuses the exact replay machinery from scripts/replay_golden.py — one source
of truth for the invariant logic — but runs a tiny deterministic subset for
speed (12 unanswerable + 6 eval-flagged items instead of the full 46).

Asserts MECHANICAL INVARIANTS ONLY. Never asserts human-evaluated scores:
the golden items' ``pending_scores`` are unanswered (status in
golden_stats_v1.json) and CI must not invent them.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from replay_golden import (  # noqa: E402
    GOLDEN_JSONL,
    RUNS_JSON,
    build_replay_pipeline,
    load_golden_items,
    load_runs,
)
from app.application.qa_pipeline import QAInput  # noqa: E402
from app.domain.enums import SafetyCategory, VerificationConfidence  # noqa: E402
from app.domain.safety_policy import canned_response  # noqa: E402


@pytest.fixture(scope="module")
def replay_env():
    items, _ = load_golden_items(GOLDEN_JSONL)
    runs = load_runs(RUNS_JSON)
    pipeline = build_replay_pipeline(items, runs)
    return items, runs, pipeline


def replay(query: str, pipeline) -> dict:
    result = asyncio.run(pipeline.run(QAInput(query=query)))
    return {
        "category": result.category,
        "confidence": result.confidence,
        "answer": result.answer,
        "flags": result.verifier_flags,
        "error": result.error,
    }


class TestGoldenUnanswerableRefusalInvariant:
    """(a) 12/12 unanswerable golden items -> safe/canned refusal path."""

    def test_all_12_unanswerable_items_refuse(self, replay_env) -> None:
        items, _, pipeline = replay_env
        rows = [r for r in items if r.get("golden_category") == "unanswerable"]
        assert len(rows) == 12
        for row in rows:
            outcome = replay(row["question"], pipeline)
            assert outcome["category"] is not SafetyCategory.SAFE_AGRI, row["row_id"]
            assert outcome["confidence"] is VerificationConfidence.BLOCKED, row["row_id"]
            assert outcome["answer"] == canned_response(outcome["category"]), row["row_id"]
            assert outcome["answer"] != row.get("gold_answer", ""), row["row_id"]
            assert outcome["error"] is None, row["row_id"]


class TestGoldenVerifierFlagInvariant:
    """(b) every eval-flagged golden item surfaces verifier flags on replay.

    The expected set is read from golden_runs_v1.json at runtime
    (verifier_confidence == "flagged-unverified"); the count is never
    hardcoded from memory.
    """

    def test_eval_flagged_items_produce_verifier_flags(self, replay_env) -> None:
        _, runs, pipeline = replay_env
        flagged_ids = [
            run["row_id"]
            for run in runs
            if run.get("verifier_confidence") == "flagged-unverified"
        ]
        assert len(flagged_ids) > 0, "golden_runs_v1.json records no flag-worthy items"
        items_by_id = {r["row_id"]: r for r in _golden_rows()}
        for row_id in flagged_ids:
            row = items_by_id[row_id]
            outcome = replay(row["question"], pipeline)
            assert outcome["flags"], row_id
            assert outcome["error"] is None, row_id


class TestGoldenNoExceptionInvariant:
    """(c) no pipeline exception on any replayed item (18-item subset)."""

    def test_no_pipeline_error_on_replay_subset(self, replay_env) -> None:
        items, runs, pipeline = replay_env
        flagged_ids = {
            run["row_id"]
            for run in runs
            if run.get("verifier_confidence") == "flagged-unverified"
        }
        subset = [
            r for r in items if r.get("golden_category") == "unanswerable" or r["row_id"] in flagged_ids
        ]
        assert len(subset) == 18
        for row in subset:
            outcome = replay(row["question"], pipeline)
            assert outcome["error"] is None, row["row_id"]


def _golden_rows() -> list[dict]:
    import json

    return [
        json.loads(line)
        for line in GOLDEN_JSONL.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]