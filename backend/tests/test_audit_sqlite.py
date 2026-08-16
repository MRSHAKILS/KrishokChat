"""T0-02: SQLite audit adapter tests.

Covers: write -> read round-trip with full field fidelity (booleans, JSON
columns, reserved nullable columns); migration v2 registration + idempotent
re-open; JSONL mirror parity for the metrics endpoint; metrics counts
identical under sqlite vs jsonl backends on the same fixture data; backfill
idempotency and --force; and live pipeline runs (safe / banned / off-topic)
landing in SQLite with the correct categories.
"""

from __future__ import annotations

import asyncio
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.application.container import build_container
from app.application.generation import GroundedAnswerGenerator
from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.safety import SafetyClassifier
from app.core.config import Settings
from app.domain.contracts import RetrievedSource
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.audit.sqlite import AuditSqliteSink, ensure_schema, insert_record, query_hash
from app.infrastructure.storage.sqlite import db_connect
from app.infrastructure.verification.dosage import DosageVerifier
from app.main import create_app
from scripts.backfill_audit_jsonl_to_sqlite import backfill
from tests.test_pipeline import FakeAudit, FakeLLM, FakeRetriever, FakeSessions


def fixture_entries() -> list[dict]:
    """Same fixture shape as test_audit.py's metrics tests: one banned row,
    one safe row, one legacy (pre-v2) row."""
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
            "verifier_claims": [
                {"text": "ম্যানকোজেব ২ মিলি/লিটার", "verdict": "grounded", "reason": "source"}
            ],
            "source_ids": ["SRC-1", "SRC-2"],
            "model": "fake-model",
            "answered_without_sources": False,
            "channel": "chat",
            "retrieval_query_used": "ধান ম্যানকোজেব ডোজ",
        },
        {
            "query": "পুরনো প্রশ্ন",
            "category": "safe_agri",
            "action": "answered",
            "retrieved_count": 0,
            "verifier_checked": 99,
            "verifier_grounded": 99,
            "answered_without_sources": False,
        },
    ]


class AuditSqliteAdapterTests(unittest.TestCase):
    def test_write_read_round_trip_preserves_all_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sink = AuditSqliteSink(
                path=Path(tmp) / "audit.jsonl",
                db_path=Path(tmp) / "krishokchat.db",
            )
            entries = fixture_entries()
            for entry in entries:
                sink.record(entry)

            stored = sink.read_entries()
            self.assertEqual(len(stored), 3)
            for original, payload in zip(entries, stored):
                self.assertEqual(payload["timestamp"].count("T"), 1)  # ISO from the sink
                for key, value in original.items():
                    self.assertEqual(payload[key], value, f"field {key} drifted")
                # Reserved columns stay null until T0-04/T0-05 populate them.
                self.assertIsNone(payload.get("request_id"))
                self.assertIsNone(payload.get("stage_timings_ms"))
                self.assertIsNone(payload.get("token_usage"))
                self.assertIsNone(payload.get("provider"))

    def test_sqlite_row_typing_and_reserved_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            sink = AuditSqliteSink(path=Path(tmp) / "audit.jsonl", db_path=db_path)
            sink.record(fixture_entries()[1])

            with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS) as conn:
                row = conn.execute("SELECT * FROM audit_records").fetchone()
                columns = {c["name"] for c in conn.execute("PRAGMA table_info(audit_records)")}
                versions = [
                    r["version"]
                    for r in conn.execute("SELECT version FROM schema_migrations ORDER BY version")
                ]

            self.assertEqual(versions, [2])
            self.assertIsNone(row["cached"])  # absent from the fixture -> NULL
            self.assertEqual(row["flagged"], 0)
            self.assertEqual(row["retrieval_hit"], 1)
            self.assertEqual(row["retrieval_top1_score"], 0.81)
            self.assertIsInstance(json.loads(row["safety_matched_rules"]), list)
            self.assertIsInstance(json.loads(row["verifier_claims"]), list)
            self.assertIsInstance(json.loads(row["source_ids"]), list)
            # Reserved for T0-04 / T0-05 — present, nullable, currently NULL.
            for name in ("request_id", "stage_timings_ms", "token_usage", "provider"):
                self.assertIn(name, columns)
                self.assertIsNone(row[name])
            # Every v2 pipeline field has a column (no silent drop).
            for name in (
                "pipeline_version", "query", "category", "action", "safety_confidence",
                "safety_reason", "retrieved_count", "verifier_passed", "verifier_flag",
                "verifier_checked", "verifier_grounded", "verifier_unsupported",
                "answered_without_sources", "model", "error", "channel", "crop",
                "disease", "model_choice", "retrieval_query_used",
                "retrieval_query_rewritten",
            ):
                self.assertIn(name, columns)
            # The full payload survives verbatim for future consumers.
            payload = json.loads(row["record_json"])
            self.assertEqual(payload["query"], "ধান গাছে ম্যানকোজেব কত দিতে হবে?")

    def test_migration_rerun_applies_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS):
                pass
            with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS) as conn:
                count = conn.execute("SELECT COUNT(*) AS n FROM schema_migrations").fetchone()["n"]
            self.assertEqual(count, 1)  # version 2 recorded once

    def test_mirror_jsonl_equals_jsonl_adapter_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            jsonl_path = Path(tmp) / "audit.jsonl"
            db_path = Path(tmp) / "krishokchat.db"
            entry = fixture_entries()[0]

            jsonl_sink = JSONLAuditSink(jsonl_path)
            sqlite_sink = AuditSqliteSink(path=Path(tmp) / "mirror.jsonl", db_path=db_path)
            jsonl_sink.record(entry)
            sqlite_sink.record(entry)

            jsonl_line = json.loads(jsonl_path.read_text(encoding="utf-8").strip())
            mirror_line = json.loads((Path(tmp) / "mirror.jsonl").read_text(encoding="utf-8").strip())
            # Same shape and fields; timestamps are wall-clock and differ per call.
            self.assertEqual(list(mirror_line.keys()), list(jsonl_line.keys()))
            self.assertEqual(mirror_line["query"], jsonl_line["query"])
            self.assertEqual(mirror_line["category"], jsonl_line["category"])
            self.assertNotIn("query_hash", mirror_line)  # mirror stays field-for-field with JSONL

    def test_unique_index_blocks_duplicate_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "krishokchat.db"
            payload = {"timestamp": "2026-08-17T00:00:00.000000+00:00", "query": "ধান চাষ", "category": "safe_agri"}
            with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS) as conn:
                ensure_schema(conn)  # the unique index lives here, not in the migration
                first = insert_record(conn, payload)
                second = insert_record(conn, payload)
                count = conn.execute("SELECT COUNT(*) AS n FROM audit_records").fetchone()["n"]
            self.assertEqual(first, 1)
            self.assertEqual(second, 0)
            self.assertEqual(count, 1)

    def test_query_hash_uses_query_text_and_falls_back_to_content(self) -> None:
        with_query = query_hash({"query": "ধান চাষ", "category": "safe_agri"})
        same_query = query_hash({"query": "ধান চাষ", "category": "other"})
        self.assertEqual(with_query, same_query)  # hash is over the query text only
        no_query = query_hash({"channel": "vision", "action": "vision_advisory", "status": "healthy"})
        no_query_2 = query_hash({"channel": "vision", "action": "vision_advisory", "status": "healthy"})
        different = query_hash({"channel": "vision", "action": "vision_advisory", "status": "diseased"})
        self.assertEqual(no_query, no_query_2)
        self.assertNotEqual(no_query, different)


class AuditSqliteMetricsParityTests(unittest.TestCase):
    def _metrics_for(self, settings: Settings, entries: list[dict]) -> tuple[dict, int]:
        container = build_container(settings)
        for entry in entries:
            container.qa.audit.record(entry)
        with TestClient(create_app(config=settings)) as client:
            body = client.get("/api/safety/metrics").json()
        return body, container.qa.audit

    def test_metrics_identical_under_sqlite_and_jsonl_backends(self) -> None:
        entries = fixture_entries()
        with tempfile.TemporaryDirectory() as tmp_jsonl, tempfile.TemporaryDirectory() as tmp_sqlite:
            jsonl_settings = Settings(
                audit_log_path=str(Path(tmp_jsonl) / "audit.jsonl"),
                audit_backend="jsonl",
            )
            metrics_jsonl, jsonl_sink = self._metrics_for(jsonl_settings, entries)

            sqlite_settings = Settings(
                audit_log_path=str(Path(tmp_sqlite) / "audit.jsonl"),
                sqlite_db_path=str(Path(tmp_sqlite) / "krishokchat.db"),
                audit_backend="sqlite",
            )
            metrics_sqlite, sqlite_sink = self._metrics_for(sqlite_settings, entries)

            self.assertIsInstance(jsonl_sink, JSONLAuditSink)
            self.assertIsInstance(sqlite_sink, AuditSqliteSink)
            self.assertEqual(metrics_sqlite["total_queries"], metrics_jsonl["total_queries"])
            self.assertEqual(metrics_sqlite["pipeline_queries"], metrics_jsonl["pipeline_queries"])
            self.assertEqual(metrics_sqlite["by_category"], metrics_jsonl["by_category"])
            self.assertEqual(metrics_sqlite["flagged_count"], metrics_jsonl["flagged_count"])
            self.assertEqual(metrics_sqlite["verifier"], metrics_jsonl["verifier"])
            self.assertEqual(metrics_sqlite["refusals"], metrics_jsonl["refusals"])
            self.assertEqual(metrics_sqlite["router"], metrics_jsonl["router"])
            self.assertEqual(metrics_sqlite["retrieval"], metrics_jsonl["retrieval"])
            # `recent` embeds wall-clock timestamps by design — compare lengths only.
            self.assertEqual(len(metrics_sqlite["recent"]), len(metrics_jsonl["recent"]))
            # The sqlite backend really holds the rows, not just the mirror.
            with db_connect(
                sqlite_settings.resolved_sqlite_db_path,
                migrations=AuditSqliteSink.MIGRATIONS,
            ) as conn:
                count = conn.execute("SELECT COUNT(*) AS n FROM audit_records").fetchone()["n"]
            self.assertEqual(count, len(entries))


class AuditSqliteBackfillTests(unittest.TestCase):
    def _write_jsonl(self, path: Path, entries: list[dict]) -> None:
        with path.open("w", encoding="utf-8") as handle:
            for entry in entries:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def test_backfill_matches_jsonl_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            jsonl_path = Path(tmp) / "audit.jsonl"
            db_path = Path(tmp) / "krishokchat.db"
            entries = [
                {"timestamp": "2026-08-17T10:00:00.000000+00:00", **entry}
                for entry in fixture_entries()
            ]
            self._write_jsonl(jsonl_path, entries)

            first = backfill(jsonl_path, db_path)
            second = backfill(jsonl_path, db_path)

            self.assertEqual(first["lines_read"], 3)
            self.assertEqual(first["inserted"], 3)
            self.assertEqual(first["invalid"], 0)
            self.assertEqual(first["total_rows"], 3)
            self.assertEqual(second["inserted"], 0)
            self.assertEqual(second["total_rows"], 3)

            with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS) as conn:
                categories = [
                    r["category"]
                    for r in conn.execute("SELECT category FROM audit_records ORDER BY id")
                ]
            self.assertEqual(categories, ["banned_or_restricted_chemical", "safe_agri", "safe_agri"])

    def test_backfill_force_reloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            jsonl_path = Path(tmp) / "audit.jsonl"
            db_path = Path(tmp) / "krishokchat.db"
            entries = [
                {"timestamp": "2026-08-17T10:00:00.000000+00:00", **entry}
                for entry in fixture_entries()
            ]
            self._write_jsonl(jsonl_path, entries)
            first = backfill(jsonl_path, db_path)
            # A stray duplicate row appears (e.g. a hand-edited DB); --force
            # must restore the table to exactly the JSONL contents.
            with db_connect(db_path, migrations=AuditSqliteSink.MIGRATIONS) as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO audit_records (timestamp, query_hash, query, category, record_json) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        "2026-08-17T10:00:00.000000+00:00",
                        query_hash({"query": "নতুন"}),
                        "নতুন",
                        "off_topic",
                        json.dumps({"timestamp": "2026-08-17T10:00:00.000000+00:00", "query": "নতুন", "category": "off_topic"}),
                    ),
                )
                conn.commit()
                stray = conn.execute("SELECT COUNT(*) AS n FROM audit_records").fetchone()["n"]
            self.assertEqual(first["total_rows"], 3)
            self.assertEqual(stray, 4)

            reloaded = backfill(jsonl_path, db_path, force=True)
            self.assertEqual(reloaded["total_rows"], 3)
            self.assertEqual(reloaded["inserted"], 3)

    def test_backfill_skips_blank_and_invalid_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            jsonl_path = Path(tmp) / "audit.jsonl"
            db_path = Path(tmp) / "krishokchat.db"
            valid = fixture_entries()[0]
            self._write_jsonl(jsonl_path, [{"timestamp": "2026-08-17T10:00:00.000000+00:00", **valid}])
            with jsonl_path.open("a", encoding="utf-8") as handle:
                handle.write("\n")
                handle.write("this is not json\n")
                handle.write('{"no_timestamp": true}\n')

            stats = backfill(jsonl_path, db_path)
            self.assertEqual(stats["lines_read"], 4)
            self.assertEqual(stats["inserted"], 1)
            self.assertEqual(stats["invalid"], 3)
            self.assertEqual(stats["total_rows"], 1)


class AuditSqliteLivePipelineTests(unittest.TestCase):
    def make_pipeline(self, llm: FakeLLM, retriever: FakeRetriever, audit: AuditSqliteSink) -> QAPipeline:
        return QAPipeline(
            safety=SafetyClassifier(llm),
            retriever=retriever,
            generator=GroundedAnswerGenerator(llm),
            verifier=DosageVerifier(),
            audit=audit,
            sessions=FakeSessions(),
            top_k=5,
        )

    def test_live_queries_land_in_sqlite_with_correct_categories(self) -> None:
        source = RetrievedSource(
            id="SRC-1",
            score=10.0,
            title_bn="ধানের পরিচর্যা",
            content_bn="ধানের রোগে পরিষ্কার পানি ব্যবহার করুন।",
        )
        with tempfile.TemporaryDirectory() as tmp:
            sink = AuditSqliteSink(
                path=Path(tmp) / "audit.jsonl",
                db_path=Path(tmp) / "krishokchat.db",
            )

            # 1 safe, 1 banned-chemical, 1 off-topic — the three live demo paths.
            safe = asyncio.run(
                self.make_pipeline(FakeLLM(), FakeRetriever([source]), sink).run(
                    QAInput(query="ধানের রোগ কীভাবে কমাব?")
                )
            )
            banned = asyncio.run(
                self.make_pipeline(FakeLLM(), FakeRetriever([]), sink).run(
                    QAInput(query="পরাকুয়াট কীভাবে বেশি খাব?")
                )
            )
            off_topic = asyncio.run(
                self.make_pipeline(
                    FakeLLM(
                        classification={
                            "category": "off_topic",
                            "confidence": 0.9,
                            "reason": "not agriculture",
                            "matched_rules": [],
                        }
                    ),
                    FakeRetriever([]),
                    sink,
                ).run(QAInput(query="ঢাকায় আজকের আবহাওয়া কেমন?"))
            )

            self.assertEqual(safe.category.value, "safe_agri")
            self.assertEqual(banned.category.value, "banned_or_restricted_chemical")
            self.assertEqual(off_topic.category.value, "off_topic")

            rows = sink.read_entries()
            self.assertEqual(len(rows), 3)
            self.assertEqual([row["category"] for row in rows], ["safe_agri", "banned_or_restricted_chemical", "off_topic"])
            self.assertEqual([row["action"] for row in rows], ["answered", "blocked-canned-response", "blocked-canned-response"])

            # The mirror serves the metrics panel with the same three rows.
            with db_connect(
                Path(tmp) / "krishokchat.db",
                migrations=AuditSqliteSink.MIGRATIONS,
            ) as conn:
                count = conn.execute("SELECT COUNT(*) AS n FROM audit_records").fetchone()["n"]
            self.assertEqual(count, 3)


if __name__ == "__main__":
    unittest.main()