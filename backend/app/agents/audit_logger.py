"""Audit logger — appends safety decisions to a local JSONL file."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "safety_audit.jsonl"


def log_safety_decision(query: str, category: str, action: str, flagged: bool, verifier_flag: str | None):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "category": category,
        "action": action,
        "flagged": flagged,
        "verifier_flag": verifier_flag,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
