from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.application.qa_pipeline import QAInput, QAPipeline
from app.application.generation import GroundedAnswerGenerator
from app.application.safety import SafetyClassifier
from app.core.config import Settings
from app.domain.contracts import RetrievedSource
from app.infrastructure.verification.dosage import DosageVerifier
from app.main import create_app
from tests.test_pipeline import FakeAudit, FakeLLM, FakeRetriever, FakeSessions


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


def scored_sources() -> list[RetrievedSource]:
    return [
        RetrievedSource(
            id="SRC-1",
            content_bn="ধান গাছে ম্যানকোজেব ২ মিলি প্রতি লিটার জলে মেশান।",
            score=0.81,
            source="pest",
        ),
        RetrievedSource(
            id="SRC-2",
            content_bn="সেচের আগে মাটি পরীক্ষা করুন।",
            score=0.64,
            source="soil",
        ),
    ]


class AuditPerStepValidityTests(unittest.TestCase):
    """P2 dual-view: every logged stage decision must be exactly the evidence
    the UI stepper renders — router (decision fields), retrieval (hit/top-1),
    verifier (pass verdict)."""

    def test_safe_answered_entry_records_all_stage_evidence(self) -> None:
        llm = FakeLLM()
        retriever = FakeRetriever(scored_sources())
        audit = FakeAudit()
        asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ধান গাছে ম্যানকোজেব কত দিতে হবে?")))

        entry = audit.entries[0]
        # Router evidence
        self.assertEqual(entry["action"], "answered")
        self.assertEqual(entry["safety_confidence"], 0.99)
        self.assertEqual(entry["safety_reason"], "agriculture")
        self.assertEqual(entry["safety_matched_rules"], [])
        # Retrieval evidence: hit + top-1 score from the real returned passages
        self.assertEqual(entry["retrieved_count"], 2)
        self.assertEqual(entry["retrieval_top1_score"], 0.81)
        self.assertTrue(entry["retrieval_hit"])
        # Verifier evidence
        self.assertTrue(entry["verifier_passed"])

    def test_blocked_entry_records_rule_decision_and_skipped_stages(self) -> None:
        llm = FakeLLM()
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(
            make_pipeline(llm, retriever, audit).run(QAInput(query="পরাকুয়াট কীভাবে বেশি খাব?"))
        )

        self.assertEqual(result.category.value, "banned_or_restricted_chemical")
        entry = audit.entries[0]
        self.assertEqual(entry["action"], "blocked-canned-response")
        self.assertEqual(entry["safety_confidence"], 1.0)
        self.assertTrue(entry["safety_matched_rules"])
        self.assertEqual(entry["retrieved_count"], 0)
        self.assertFalse(entry["retrieval_hit"])
        self.assertIsNone(entry["retrieval_top1_score"])
        self.assertIsNone(entry["verifier_passed"])
        self.assertEqual(entry["verifier_checked"], 0)

    def test_exception_path_keeps_evidence_fields_typed(self) -> None:
        llm = FakeLLM(classification={"not_category": "safe_agri"})  # classifier failure path
        retriever = FakeRetriever([])
        audit = FakeAudit()
        result = asyncio.run(make_pipeline(llm, retriever, audit).run(QAInput(query="ধান চাষ")))

        self.assertEqual(result.category.value, "low_confidence")
        entry = audit.entries[0]
        self.assertEqual(entry["safety_confidence"], 0.0)
        self.assertEqual(entry["retrieved_count"], 0)
        self.assertFalse(entry["verifier_passed"])


class SafetyMetricsEndpointTests(unittest.TestCase):
    """Aggregates must be computed from the same logged decisions the panel
    renders — no fabricated numbers."""

    def test_metrics_endpoint_aggregates_per_step_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "audit.jsonl"
            entries = [
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
                # Legacy row (pre-P2): visible in `recent` but must NOT count
                # toward the live pipeline aggregates.
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
            log_path.write_text(
                "\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n",
                encoding="utf-8",
            )

            settings = Settings(audit_log_path=str(log_path))
            with TestClient(create_app(config=settings)) as client:
                body = client.get("/api/safety/metrics").json()

            self.assertEqual(body["total_queries"], 3)
            self.assertEqual(body["pipeline_queries"], 2)
            # Verifier: pass_rate from logged verdicts (legacy row excluded)
            self.assertEqual(body["verifier"]["checked"], 2)
            self.assertEqual(body["verifier"]["grounded"], 2)
            self.assertEqual(body["verifier"]["unsupported"], 0)
            self.assertEqual(body["verifier"]["pass_rate"], 1.0)
            # Router: refusal rate from blocked-canned-response actions
            self.assertEqual(body["router"]["blocked"], 1)
            self.assertEqual(body["router"]["refusal_rate"], 0.5)
            # Retrieval: hit-rate and top-1 mean from logged safe answers
            self.assertEqual(body["retrieval"]["answered"], 1)
            self.assertEqual(body["retrieval"]["hit_rate"], 1.0)
            self.assertEqual(body["retrieval"]["avg_top1_score"], 0.81)
            self.assertEqual(body["retrieval"]["avg_sources"], 2.0)
            self.assertEqual(body["refusals"]["answered_without_sources"], 0)


if __name__ == "__main__":
    unittest.main()