"""POST /api/detect — crop classifier + YOLO disease detection combined.

Stub for TASK_04 to implement.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/api/detect")
async def detect_endpoint():
    """Placeholder. TASK_04 will implement classifier→YOLO→treatment pipeline."""
    return {"status": "not_implemented", "message": "TASK_04 will implement this endpoint"}
