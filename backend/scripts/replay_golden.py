"""Mechanical golden regression replay — offline stub LLM lane, no network.

Loads the 46-item golden set (dataset_release/benchmark/) and replays every
item through the real QA pipeline (app.application.qa_pipeline.QAPipeline)
with a fully deterministic, offline stub lane:

- safety: the real deterministic precheck runs first (same as production);
  the LLM-dependent part replays the ``safety_category`` the existing eval
  recorded in golden_runs_v1.json (no model call, no network, no API key).
- generation: the stub emits the item's reference gold answer from
  golden_qa_v1.jsonl so the deterministic verifier actually runs. It is a
  port-shaped test double (same protocol the composition root wires), never
  production code.
- retrieval / verifier / audit / sessions: real offline components (precomputed
  BM25 index on disk, HardenedDosageVerifier, JSONL audit to a temp dir,
  in-memory session store).

Asserts MECHANICAL INVARIANTS ONLY. Human-evaluated scores are never asserted:
the golden items' ``pending_scores`` are unanswered and CI must not invent them.

  (a) all 12 unanswerable golden items take the safe/canned refusal path
      (terminal category, blocked confidence, canned response — no normal
      answer, never the reference answer);
  (b) every item the existing eval marked flag-worthy (``verifier_confidence
      == "flagged-unverified"`` in golden_runs_v1.json — 6 of 46 today, read
      from the file at runtime) surfaces verifier flags on replay;
  (c) no pipeline exception / error on any replay.

Usage:
    uv run python scripts/replay_golden.py [--assert-invariants] [--limit N]

Output is machine-readable: one JSON object per replayed item, then a final
summary JSON line. With ``--assert-invariants`` the exit code is non-zero on
any invariant failure; without it the script only reports.

Note on the "stub/offline lane": backend/app/core/config.py has no provider
enum — the offline lane that exists in code is ``UnavailableLLMClient``
(fail-closed; every query would be refused before retrieval, so the verifier
would never run). This script therefore uses a deterministic stub instead,
which is what makes invariants (b) reachable while staying fully offline.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import tempfile
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_ROOT = REPO_ROOT / "backend"
BENCHMARK = REPO_ROOT / "dataset_release" / "benchmark"
GOLDEN_JSONL = BENCHMARK / "golden_qa_v1.jsonl"
RUNS_JSON = BENCHMARK / "golden_runs_v1.json"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.application.generation import REFERRAL, GenerationResult  # noqa: E402
from app.application.qa_pipeline import QAInput, QAPipeline  # noqa: E402
from app.domain.contracts import QueryContext, SafetyDecision  # noqa: E402
from app.domain.enums import SafetyCategory  # noqa: E402
from app.domain.safety_policy import canned_response, precheck  # noqa: E402
from app.infrastructure.audit.jsonl import JSONLAuditSink  # noqa: E402
from app.infrastructure.retrieval.bm25 import BM25Retriever  # noqa: E402
from app.infrastructure.sessions.memory import InMemorySessionStore  # noqa: E402
from app.application.verifier import HardenedDosageVerifier  # noqa: E402

TERMINAL_ESCALATION = {
    SafetyCategory.BANNED_OR_RESTRICTED_CHEMICAL,
    SafetyCategory.SELF_HARM_OR_POISONING_RISK,
}


class StubSafetyClassifier:
    """Offline safety classifier: real deterministic precheck, then a replay
    of the eval-recorded ``safety_category`` (golden_runs_v1.json)."""

    def __init__(self, decisions_by_query: dict[str, SafetyDecision]) -> None:
        self.decisions_by_query = decisions_by_query

    async def classify(self, query: str, context: QueryContext) -> SafetyDecision:
        match = precheck(query)
        if match:
            category, rules = match
            return SafetyDecision(
                category=category,
                confidence=1.0,
                reason="Deterministic safety rule matched",
                matched_rules=rules,
                requires_escalation=category in TERMINAL_ESCALATION,
                response=canned_response(category),
            )
        decision = self.decisions_by_query.get(query)
        if decision is None:
            return SafetyDecision(
                category=SafetyCategory.LOW_CONFIDENCE,
                confidence=0.0,
                reason="No recorded eval decision for query",
                requires_escalation=True,
                response=canned_response(SafetyCategory.LOW_CONFIDENCE),
            )
        return decision


class StubGenerator:
    """Deterministic AnswerGenerator port double keyed by query text.

    Emits the item's reference gold answer so the deterministic verifier
    really runs. Mirrors GroundedAnswerGenerator's no-sources behavior.
    """

    name = "golden-stub"

    def __init__(self, answers_by_query: dict[str, str]) -> None:
        self.answers_by_query = answers_by_query

    async def generate(
        self, query: str, context: QueryContext, sources: list[Any]
    ) -> GenerationResult:
        if not sources:
            return GenerationResult(
                answer=REFERRAL, model=self.name, mode="no_sources", error="No sources"
            )
        answer = self.answers_by_query.get(query)
        if not answer:
            return GenerationResult(
                answer=REFERRAL,
                model=self.name,
                mode="no_reference_answer",
                error="No reference answer for query",
            )
        return GenerationResult(
            answer=answer,
            used_source_ids=tuple(source.id for source in sources),
            model=self.name,
            mode="grounded",
        )

    async def stream(
        self, query: str, context: QueryContext, sources: list[Any]
    ) -> AsyncIterator[str]:
        yield self.answers_by_query.get(query) or REFERRAL

    async def generate_from_text(
        self, answer: str, sources: list[Any], *, mode: str
    ) -> GenerationResult:
        return GenerationResult(
            answer=answer.strip() or REFERRAL,
            used_source_ids=tuple(source.id for source in sources),
            model=self.name,
            mode=mode,
        )


def load_golden_items(path: Path) -> tuple[list[dict], dict[str, str]]:
    items: list[dict] = []
    answers: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        items.append(item)
        answers[item["question"]] = item.get("gold_answer", "")
    if len(answers) != len(items):
        raise ValueError(f"duplicate questions in {path.name}")
    return items, answers


def load_runs(path: Path) -> list[dict]:
    runs = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(runs, list):
        raise ValueError(f"{path.name} must be a JSON list")
    return runs


def build_replay_pipeline(items: list[dict], runs: list[dict]) -> QAPipeline:
    _, answers = load_golden_items(GOLDEN_JSONL)
    decisions: dict[str, SafetyDecision] = {}
    for run in runs:
        query = run.get("question")
        label = run.get("safety_category")
        if not query or not label:
            continue
        try:
            category = SafetyCategory(label)
        except ValueError:
            continue
        decisions[query] = SafetyDecision(
            category=category,
            confidence=0.99 if category is SafetyCategory.SAFE_AGRI else 1.0,
            reason="Recorded eval safety category (offline replay)",
            matched_rules=(),
            requires_escalation=category in TERMINAL_ESCALATION,
            response=None if category is SafetyCategory.SAFE_AGRI else canned_response(category),
        )
    audit_dir = Path(tempfile.gettempdir()) / "krishokchat_golden_replay"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit = JSONLAuditSink(audit_dir / "golden_replay_audit.jsonl")
    retriever = BM25Retriever(
        index_path=BACKEND_ROOT / "ml_assets" / "rag_index" / "indexes" / "bm25_index.pkl",
        corpus_path=(
            BACKEND_ROOT / "ml_assets" / "rag_index" / "processed" / "knowledge_nodes_clean.jsonl"
        ),
    )
    return QAPipeline(
        safety=StubSafetyClassifier(decisions),
        retriever=retriever,
        generator=StubGenerator(answers),
        verifier=HardenedDosageVerifier(),
        audit=audit,
        sessions=InMemorySessionStore(max_turns=10, ttl_seconds=1800),
        top_k=5,
    )


async def _replay(query: str, pipeline: QAPipeline) -> dict:
    result = await pipeline.run(QAInput(query=query))
    return {
        "category": result.category.value,
        "confidence": result.confidence.value,
        "answer_is_canned": result.answer == canned_response(result.category),
        "flags": list(result.verifier_flags),
        "error": result.error,
    }


def replay_one(query: str, pipeline: QAPipeline) -> dict:
    return asyncio.run(_replay(query, pipeline))


def check_invariants(
    items: list[dict],
    runs: list[dict],
    outcomes: dict[str, dict],
    expected_ids: set[str] | None = None,
) -> tuple[bool, list[str]]:
    """Check invariants over the replayed subset.

    ``expected_ids`` restricts "not replayed" complaints to the items the
    caller intended to replay (so ``--limit`` runs stay meaningful).
    """
    expected = outcomes.keys() if expected_ids is None else expected_ids
    failures: list[str] = []
    flagged_ids = [
        run["row_id"]
        for run in runs
        if run.get("verifier_confidence") == "flagged-unverified"
    ]
    unanswerable_ids = [
        item["row_id"] for item in items if item.get("golden_category") == "unanswerable"
    ]

    refused = 0
    for row_id in unanswerable_ids:
        if row_id not in expected:
            continue
        outcome = outcomes.get(row_id)
        if outcome is None:
            failures.append(f"{row_id}: not replayed")
            continue
        if outcome["category"] == "safe_agri":
            failures.append(f"{row_id}: unanswerable item produced a normal answer")
        if outcome["confidence"] != "blocked":
            failures.append(f"{row_id}: unanswerable item confidence is not blocked")
        if not outcome["answer_is_canned"]:
            failures.append(f"{row_id}: unanswerable item did not take the canned refusal path")
        if outcome["error"]:
            failures.append(f"{row_id}: unanswerable item errored: {outcome['error']}")
        if outcome["confidence"] == "blocked":
            refused += 1

    flagged_with_flags = 0
    for row_id in flagged_ids:
        if row_id not in expected:
            continue
        outcome = outcomes.get(row_id)
        if outcome is None:
            failures.append(f"{row_id}: not replayed")
            continue
        if not outcome["flags"]:
            failures.append(f"{row_id}: eval-flagged item surfaced no verifier flags")
        else:
            flagged_with_flags += 1
        if outcome["error"]:
            failures.append(f"{row_id}: eval-flagged item errored: {outcome['error']}")

    errored = sum(1 for outcome in outcomes.values() if outcome["error"])
    if errored:
        failures.append(f"{errored} replay(s) carried a pipeline error")

    summary = {
        "replayed": len(outcomes),
        "unanswerable": len(unanswerable_ids),
        "unanswerable_refused": refused,
        "flag_worthy": len(flagged_ids),
        "flag_worthy_with_flags": flagged_with_flags,
        "errors": errored,
        "invariants": "PASS" if not failures else "FAIL",
    }
    for failure in failures:
        print(f"INVARIANT FAILURE: {failure}")
    print(json.dumps({"summary": summary}, ensure_ascii=False))
    return not failures, failures


def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to cp1252 and cannot encode the Bengali output;
    # reconfigure so the golden gate runs identically on any platform.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--assert-invariants",
        action="store_true",
        help="exit non-zero when any mechanical invariant fails",
    )
    parser.add_argument("--limit", type=int, default=None, help="replay at most N items")
    args = parser.parse_args(argv)

    items, _ = load_golden_items(GOLDEN_JSONL)
    runs = load_runs(RUNS_JSON)
    pipeline = build_replay_pipeline(items, runs)

    selected = items if args.limit is None else items[: args.limit]
    outcomes: dict[str, dict] = {}
    for item in selected:
        outcome = replay_one(item["question"], pipeline)
        outcomes[item["row_id"]] = outcome
        print(
            json.dumps(
                {
                    "row_id": item["row_id"],
                    "golden_category": item.get("golden_category"),
                    **outcome,
                },
                ensure_ascii=False,
            )
        )

    ok, _ = check_invariants(items, runs, outcomes, expected_ids={item["row_id"] for item in selected})
    if args.assert_invariants and not ok:
        return 1
    if not ok:
        print("NOTE: invariants would fail under --assert-invariants")
    return 0


if __name__ == "__main__":
    sys.exit(main())