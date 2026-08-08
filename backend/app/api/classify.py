"""POST /api/classify — crop classifier inference.

Stub for TASK_04 to implement.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/api/classify")
async def classify_endpoint():
    """Placeholder. TASK_04 will implement crop classification via ONNX."""
    return {"status": "not_implemented", "message": "TASK_04 will implement this endpoint"}
