"""GET /api/benchmark — serve PRECOMPUTED golden-benchmark numbers.

Hard rule 2 (AGENTS.md): nothing here is computed live. The payload is the
static golden-stats artifact produced offline by
`ml_assets/rag_index/scripts/11_publish_golden_stats.py` from real pipeline
runs (`golden_runs_v1.json`) and the two evaluators' filled scoring sheet.
Before the evaluators score, the artifact honestly reports
`status: pending_scores` — no invented numbers.
"""

from __future__ import annotations

import json

from fastapi import APIRouter

from app.core.config import PROJECT_ROOT

router = APIRouter()

STATS_FILE = PROJECT_ROOT.parent / "dataset_release" / "benchmark" / "golden_stats_v1.json"


@router.get("/api/benchmark")
async def benchmark_endpoint() -> dict:
    """Precomputed golden-set stats (runs + human scores), never live-computed."""
    if not STATS_FILE.exists():
        return {
            "status": "not_built",
            "message": "Golden benchmark artifact missing — run ml_assets/rag_index/scripts/08..11",
            "items": None,
        }
    return json.loads(STATS_FILE.read_text(encoding="utf-8"))
