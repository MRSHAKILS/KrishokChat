"""T0-05: stage-latency + token/provider/cost telemetry in audit records.

Covers: a stubbed pipeline run produces an audit record with all four stage
timings (keys exactly safety/retrieval/generation/verifier); tokens/provider
are present when the lane exposes them and null otherwise; cost_estimate stays
null while no price table exists; request_id rides the T0-04 contextvar; old
(pre-T0-05) records remain readable by every consumer and the metrics
aggregates are unchanged by the new fields; the SQLite adapter fills its
reserved columns (token_usage mapped from ``tokens``).
"""

from __future__ import annotations

import asyncio
import json
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.safety import SafetyClassifier
from app.application.telemetry import (
    STAGE_NAMES,
    capture_tokens,
    current_request_id,
    estimate_cost,
    serving_provider,
    stage_timer,
)
from app.core.config import Settings
from app.core.logging import request_id_var
from app.domain.contracts import RetrievedSource
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.audit.sqlite import AuditSqliteSink
from app.infrastructure.storage.sqlite import db_connect
from app.infrastructure.verification.dosage import DosageVerifier
from app.main import create_app
from tests.test_pipeline import FakeAudit, FakeLLM, FakeRetriever, FakeSessions


class UsageAwareFakeLLM(FakeLLM):
    """FakeLLM plus the T0-05 lane conventions (last_usage / provider)."""

    def __init__(
        self,
        *,
        usage: dict[str, int] | None = None,
        provider: str | None = "fake-provider",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.last_usage = usage if usage is not None else {"input": 120, "output": 45}
        self.provider = provider


def make_pipeline(llm: FakeLLM, retriever: FakeRetriever, audit: FakeAudit) -> QAPipeline:
    return QAPipeline(
        safety=SafetyClassifier(llm),
        retriever=retriever,
        generator=GroundedAnswerGenerator(llm),
        verifier=DosageVerifier(),
        audit=audit,
        sessions=FakeSessions(),
        top_k=5,
    )


def one_source() -> list[RetrievedSource]:
    return [
        RetrievedSource(
            id="SRC-1",
            score=10.0,
            title_bn="ধানের পরিচর্যা",
            content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।",
        )
    ]


class TelemetryHelpersTests(unittest.TestCase):
    def test_stage_timer_records_elapsed_ms(self) -> None:
        timings = {name: 0.0 for name in STAGE_NAMES}
        with stage_timer("safety", timings):
            time.sleep(0.01)
        self.assertEqual(set(timings.keys()), {"safety", "retrieval", "generation", "verifier"})
        self.assertGreater(timings["safety"], 0.0)
        self.assertEqual(timings["retrieval"], 0.0)

    def test_capture_tokens_accepts_only_well_formed_usage(self) -> None:
        self.assertEqual(
            capture_tokens(UsageAwareFakeLLM(usage={"input": 10, "output": 20})),
            {"input": 10, "output": 20},
        )
        # Absent attribute, non-dict, missing keys, wrong types -> None, never guessed.
        self.assertIsNone(capture_tokens(object()))
        self.assertIsNone(capture_tokens(UsageAwareFakeLLM(usage="nope")))
        self.assertIsNone(capture_tokens(UsageAwareFakeLLM(usage={"input": 10})))
        self.assertIsNone(capture_tokens(UsageAwareFakeLLM(usage={"input": "ten", "output": 20})))

    def test_serving_provider_lane_attribute_wins_over_fallback(self) -> None:
        self.assertEqual(
            serving_provider(UsageAwareFakeLLM(provider="lane-provider"), "fallback"),
            "lane-provider",
        )
        self.assertEqual(serving_provider(object(), "fallback"), "fallback")

    def test_cost_estimate_null_without_price_table(self) -> None:
        # No price table exists anywhere in the codebase; estimate_cost must
        # never fabricate a number for any input.
        self.assertIsNone(estimate_cost({"input": 10, "output": 20}, "openrouter"))
        self.assertIsNone(estimate_cost(None, None))

    def test_request_id_contextvar(self) -> None:
        self.assertIsNone(current_request_id())
        token = request_id_var.set("req-telemetry-123")
        try:
            self.assertEqual(current_request_id(), "req-telemetry-123")
        finally:
            request_id_var.reset(token)
        self.assertIsNone(current_request_id())


class StageTimingsAuditTests(unittest.TestCase):
    def test_safe_run_records_all_four_stage_timings_and_lane_telemetry(self) -> None:
        llm = UsageAwareFakeLLM(usage={"input": 100, "output": 50}, provider="fake-provider")
        retriever = FakeRetriever(one_source())
        audit = FakeAudit()
        token = request_id_var.set("req-pipeline-1")
        try:
            asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ধানের রোগ কীভাবে কমাব?")))
        finally:
            request_id_var.reset(token)

        entry = audit.entries[0]
        timings = entry["stage_timings_ms"]
        self.assertEqual(set(timings.keys()), set(STAGE_NAMES))
        for name in STAGE_NAMES:
            self.assertIsInstance(timings[name], float)
        # Safety/retrieval/generation/verifier all really ran.
        for name in STAGE_NAMES:
            self.assertGreaterEqual(timings[name], 0.0)
        self.assertGreater(timings["safety"], 0.0)
        self.assertGreater(timings["retrieval"], 0.0)
        self.assertGreater(timings["generation"], 0.0)
        self.assertGreater(timings["verifier"], 0.0)
        # Lane telemetry: usage exposed -> tokens recorded; provider exposed -> recorded.
        self.assertEqual(entry["tokens"], {"input": 100, "output": 50})
        self.assertEqual(entry["provider"], "fake-provider")
        # No price table -> null, and the T0-04 request ID rode the contextvar.
        self.assertIsNone(entry["cost_estimate"])
        self.assertEqual(entry["request_id"], "req-pipeline-1")

    def test_tokens_null_when_lane_exposes_no_usage(self) -> None:
        llm = FakeLLM()  # no last_usage / provider attributes
        retriever = FakeRetriever(one_source())
        audit = FakeAudit()
        asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ধানের রোগ কীভাবে কমাব?")))

        entry = audit.entries[0]
        self.assertIsNone(entry["tokens"])
        # No lane-declared provider: falls back to the configured LLM_PROVIDER
        # (the honest "who serves generation today" answer — no failover yet).
        self.assertEqual(entry["provider"], Settings().llm_provider)
        self.assertIsNone(entry["cost_estimate"])

    def test_terminal_path_records_zero_timings_for_skipped_stages(self) -> None:
        llm = UsageAwareFakeLLM()
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(
            make_pipeline(llm, retriever, audit).run(QAInput(query="পরাকুয়াট কীভাবে বেশি খাব?"))
        )

        self.assertEqual(result.category.value, "banned_or_restricted_chemical")
        entry = audit.entries[0]
        timings = entry["stage_timings_ms"]
        self.assertEqual(set(timings.keys()), set(STAGE_NAMES))
        self.assertGreater(timings["safety"], 0.0)
        # Retrieval/generation/verifier never ran -> 0.0 (trace shows SKIP).
        for name in ("retrieval", "generation", "verifier"):
            self.assertEqual(timings[name], 0.0)
        # Nothing was generated -> no tokens/provider.
        self.assertIsNone(entry["tokens"])
        self.assertIsNone(entry["provider"])
        self.assertIsNone(entry["cost_estimate"])

    def test_exception_path_still_records_timings(self) -> None:
        llm = FakeLLM(classification={"not_category": "safe_agri"})  # classifier failure path
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ধান চাষ")))

        self.assertEqual(result.category.value, "low_confidence")
        entry = audit.entries[0]
        self.assertEqual(set(entry["stage_timings_ms"].keys()), set(STAGE_NAMES))
        self.assertGreater(entry["stage_timings_ms"]["safety"], 0.0)
        self.assertIsNone(entry["tokens"])


class OldRecordCompatibilityTests(unittest.TestCase):
    """Pre-T0-05 records (no telemetry fields) must load and aggregate unchanged."""

    def _old_entries(self) -> list[dict]:
        return [
            {
                "pipeline_version": 2,
                "query": "পরাকুয়াট ব্যবহার",
                "category": "banned_or_restricted_chemical",
                "action": "blocked-canned-response",
                "flagged": False,
                "safety_confidence": 1.0,
                "safety_reason": "Deterministic safety rule matched",
                "safety_matched_rules": ["paraquat"],
                "retrieved_count": 0,
                "retrieval_top1_score": None,
                "retrieval_hit": False,
                "verifier_passed": None,
                "verifier_checked": 0,
                "verifier_grounded": 0,
                "verifier_unsupported": 0,
                "answered_without_sources": False,
            },
            {
                "pipeline_version": 2,
                "query": "ধান গাছে ম্যানকোজেব কত দিতে হবে?",
                "category": "safe_agri",
                "action": "answered",
                "flagged": False,
                "safety_confidence": 0.99,
                "safety_reason": "agriculture",
                "safety_matched_rules": [],
                "retrieved_count": 2,
                "retrieval_top1_score": 0.81,
                "retrieval_hit": True,
                "verifier_passed": True,
                "verifier_checked": 2,
                "verifier_grounded": 2,
                "verifier_unsupported": 0,
                "answered_without_sources": False,
            },
        ]

    def _write(self, path: Path, entries: list[dict]) -> None:
        path.write_text(
            "\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n",
            encoding="utf-8",
        )

    def test_old_records_load_and_new_fields_do_not_change_aggregates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "audit.jsonl"
            old = self._old_entries()
            self._write(log_path, old)
            settings = Settings(audit_log_path=str(log_path))

            with TestClient(create_app(config=settings)) as client:
                before = client.get("/api/safety/metrics").json()
            # New-format record appended: the telemetry fields must be inert to
            # aggregation — the new record contributes exactly the same counts
            # as its telemetry-free twin would.
            with TestClient(create_app(config=settings)) as client:
                new = dict(old[1])
                new["stage_timings_ms"] = {"safety": 1.0, "retrieval": 2.0, "generation": 3.0, "verifier": 4.0}
                new["tokens"] = {"input": 10, "output": 5}
                new["provider"] = "fake-provider"
                new["cost_estimate"] = None
                new["request_id"] = "req-new"
                container = client.app.state.container
                container.qa.audit.record(new)
            with TestClient(create_app(config=settings)) as client:
                after = client.get("/api/safety/metrics").json()

            self.assertEqual(after["total_queries"], before["total_queries"] + 1)
            self.assertEqual(after["pipeline_queries"], before["pipeline_queries"] + 1)
            # Aggregates = before + the appended record's unchanged evidence fields.
            self.assertEqual(after["verifier"]["checked"], before["verifier"]["checked"] + new["verifier_checked"])
            self.assertEqual(after["verifier"]["grounded"], before["verifier"]["grounded"] + new["verifier_grounded"])
            self.assertEqual(after["verifier"]["unsupported"], before["verifier"]["unsupported"])
            self.assertEqual(after["verifier"]["pass_rate"], 1.0)
            self.assertEqual(after["router"]["blocked"], before["router"]["blocked"])
            self.assertEqual(after["router"]["refusal_rules"], before["router"]["refusal_rules"])
            self.assertEqual(after["retrieval"]["answered"], before["retrieval"]["answered"] + 1)
            self.assertEqual(after["retrieval"]["hit_rate"], 1.0)
            self.assertEqual(after["retrieval"]["avg_top1_score"], before["retrieval"]["avg_top1_score"])
            self.assertEqual(after["refusals"], before["refusals"])
            # The new record surfaces in `recent` with its telemetry fields intact.
            newest = after["recent"][0]
            self.assertEqual(newest["stage_timings_ms"]["generation"], 3.0)
            self.assertEqual(newest["tokens"], {"input": 10, "output": 5})
            self.assertEqual(newest["provider"], "fake-provider")

    def test_jsonl_adapter_writes_and_reads_old_and_new_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.jsonl"
            sink = JSONLAuditSink(path)
            old = self._old_entries()[1]
            new = dict(old)
            new["stage_timings_ms"] = {"safety": 1.0, "retrieval": 2.0, "generation": 3.0, "verifier": 4.0}
            new["tokens"] = {"input": 10, "output": 5}
            new["provider"] = "fake-provider"
            new["cost_estimate"] = None
            new["request_id"] = "req-1"
            sink.record(old)
            sink.record(new)

            lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(len(lines), 2)
            self.assertNotIn("stage_timings_ms", lines[0])  # old record unchanged
            self.assertNotIn("tokens", lines[0])
            self.assertEqual(lines[1]["stage_timings_ms"], new["stage_timings_ms"])
            self.assertEqual(lines[1]["tokens"], {"input": 10, "output": 5})
            self.assertIsNone(lines[1]["cost_estimate"])

    def test_sqlite_adapter_fills_reserved_columns_and_tolerates_old_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sink = AuditSqliteSink(path=Path(tmp) / "audit.jsonl", db_path=Path(tmp) / "krishokchat.db")
            new = dict(self._old_entries()[1])
            new["stage_timings_ms"] = {"safety": 1.0, "retrieval": 2.0, "generation": 3.0, "verifier": 4.0}
            new["tokens"] = {"input": 10, "output": 5}
            new["provider"] = "fake-provider"
            new["request_id"] = "req-1"
            new["cost_estimate"] = None  # no price table -> null, but present
            sink.record(new)
            sink.record(self._old_entries()[0])  # old-format record -> NULL columns

            with db_connect(Path(tmp) / "krishokchat.db", migrations=AuditSqliteSink.MIGRATIONS) as conn:
                rows = conn.execute(
                    "SELECT request_id, stage_timings_ms, token_usage, provider FROM audit_records ORDER BY id"
                ).fetchall()

                self.assertEqual(rows[0]["request_id"], "req-1")
                self.assertEqual(json.loads(rows[0]["stage_timings_ms"]), new["stage_timings_ms"])
                self.assertEqual(json.loads(rows[0]["token_usage"]), {"input": 10, "output": 5})
                self.assertEqual(rows[0]["provider"], "fake-provider")
                # Old record: reserved columns stay NULL; nothing is dropped.
                self.assertIsNone(rows[1]["request_id"])
                self.assertIsNone(rows[1]["stage_timings_ms"])
                self.assertIsNone(rows[1]["token_usage"])
                self.assertIsNone(rows[1]["provider"])
                # cost_estimate survives in record_json even without a dedicated column.
                payload = json.loads(
                    conn.execute("SELECT record_json FROM audit_records ORDER BY id LIMIT 1").fetchone()["record_json"]
                )
                self.assertIn("cost_estimate", payload)


if __name__ == "__main__":
    unittest.main()