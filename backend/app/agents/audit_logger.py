"""Compatibility shim for the centralized local audit sink."""

from app.core.config import settings
from app.infrastructure.audit.jsonl import JSONLAuditSink


_sink = JSONLAuditSink(settings.resolved_audit_log_path)


def log_safety_decision(query: str, category: str, action: str, flagged: bool, verifier_flag: str | None):
    _sink.record(
        {
            "query": query,
            "category": category,
            "action": action,
            "flagged": flagged,
            "verifier_flag": verifier_flag,
        }
    )
