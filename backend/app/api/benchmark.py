"""GET /api/benchmark — serve precomputed retrieval-benchmark numbers.

Stub for research/benchmark panel.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/benchmark")
async def benchmark_endpoint():
    """Placeholder. Will serve precomputed stats from backend/ml_assets/rag_index/."""
    return {
        "status": "not_implemented",
        "message": "Will serve precomputed retrieval benchmarks and dataset stats",
    }
