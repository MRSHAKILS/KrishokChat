"""Pydantic request/response schemas.

These stubs define the contracts that TASK_01, TASK_03, and TASK_04 will implement.
"""

from pydantic import BaseModel, Field


class QARequest(BaseModel):
    query: str = Field(..., description="User's agricultural question in Bengali/Banglish")
    session_id: str | None = Field(None, description="Optional session ID for multi-turn")


class SourceNode(BaseModel):
    id: str
    crop_bn: str | None = None
    crop_en: str | None = None
    disease_bn: str | None = None
    question: str | None = None
    answer: str | None = None
    treatment: str | None = None
    source: str | None = None
    expert_verified: bool = False
    score: float


class AgentStageEvent(BaseModel):
    stage: str = Field(..., description="safety | retrieval | generation | verifier")
    status: str = Field(..., description="start | complete | skip")
    detail: str | None = None


class QAResponse(BaseModel):
    query: str
    category: str = Field(..., description="safe_agri | banned_or_restricted_chemical | ...")
    answer: str
    sources: list[SourceNode] = []
    confidence: str = Field(..., description="verified | flagged-unverified | low_confidence")
    agent_trace: list[AgentStageEvent] = []


class ClassifyRequest(BaseModel):
    pass  # Image uploaded as multipart/form-data


class ClassifyResponse(BaseModel):
    crop: str
    confidence: float
    crop_bn: str | None = None


class DetectionBox(BaseModel):
    x: float  # Fraction of image width (0-1)
    y: float  # Fraction of image height (0-1)
    width: float
    height: float
    label: str
    confidence: float


class DetectResponse(BaseModel):
    crop: str
    crop_confidence: float
    disease: str | None = None
    disease_confidence: float | None = None
    boxes: list[DetectionBox] = []
    treatment_advice: str | None = None
    treatment_confidence: str | None = None


class BenchmarkResponse(BaseModel):
    dataset_stats: dict
    retrieval_benchmarks: dict
    model_comparisons: dict
    safety_metrics: dict


class SafetyLogEntry(BaseModel):
    timestamp: str
    query: str
    category: str
    action: str
    flagged: bool = False
    verifier_flag: str | None = None
