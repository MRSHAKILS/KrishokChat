"""Public HTTP contracts. Internal pipeline objects live in ``app.domain``."""

from pydantic import BaseModel, Field, field_validator


class QARequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000, description="User's agricultural question in Bengali/Banglish")
    session_id: str | None = Field(None, description="Optional session ID for multi-turn")
    crop: str | None = Field(None, description="Detected crop from image (optional context)")
    disease: str | None = Field(None, description="Detected disease from image (optional context)")
    history: list[dict[str, str]] = Field(default_factory=list, description="Conversation history [{role, content}]")
    model: str | None = Field(None, description="Generation model choice: 'gemini' (default) or 'krishokchat-4b' (local Ollama)")

    @field_validator("query")
    @classmethod
    def strip_query(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("query must not be blank")
        return value


class SourceNode(BaseModel):
    id: str
    crop_bn: str | None = None
    crop_en: str | None = None
    disease_bn: str | None = None
    question: str | None = None
    answer: str | None = None
    treatment: str | None = None
    source: str | None = None
    publisher: str | None = None
    publisher_bn: str | None = None
    title_bn: str | None = None
    title_en: str | None = None
    citation: str | None = None
    expert_verified: bool = False
    score: float


class AgentStageEvent(BaseModel):
    stage: str = Field(..., description="safety | retrieval | generation | verifier")
    status: str = Field(..., description="start | complete | skip | error")
    detail: str | None = None


class QAResponse(BaseModel):
    query: str
    category: str = Field(..., description="safe_agri | banned_or_restricted_chemical | ...")
    answer: str
    sources: list[SourceNode] = Field(default_factory=list)
    confidence: str = Field(..., description="verified | flagged-unverified | low_confidence")
    agent_trace: list[AgentStageEvent] = Field(default_factory=list)
    verifier_flags: list[str] = Field(default_factory=list)
    model: str | None = None


class ClassifyRequest(BaseModel):
    pass  # Image uploaded as multipart/form-data


class ClassifyResponse(BaseModel):
    crop: str
    confidence: float
    crop_bn: str | None = None
    status: str = "diagnosed"
    top3: list[dict] = Field(default_factory=list)
    has_disease_model: bool = False
    quality_warnings: list[str] = Field(default_factory=list)
    agent_trace: list[AgentStageEvent] = Field(default_factory=list)
    error: str | None = None


class DetectionBox(BaseModel):
    x: float  # Fraction of image width (0-1)
    y: float  # Fraction of image height (0-1)
    width: float
    height: float
    label: str
    confidence: float


class DetectResponse(BaseModel):
    status: str = Field(..., description="diagnosed | healthy | not_recognized | no_disease_model | model_error | invalid_image")
    detection_mode: str = Field(default="classification", description="classification; boxes are empty until a real detector is added")
    crop: str | None = None
    crop_confidence: float = 0.0
    crop_source: str = Field(default="model", description="model | user — how the crop was determined")
    disease: str | None = None
    disease_confidence: float = 0.0
    boxes: list[DetectionBox] = Field(default_factory=list)
    disease_info: dict | None = None
    top3_crops: list[dict] = Field(default_factory=list)
    top3_diseases: list[dict] = Field(default_factory=list)
    treatment_advice: str | None = None
    treatment_confidence: str | None = None
    treatment_sources: list[str] = Field(default_factory=list)
    verifier_flags: list[str] = Field(default_factory=list)
    agent_trace: list[AgentStageEvent] = Field(default_factory=list)
    quality_warnings: list[str] = Field(default_factory=list)
    error: str | None = None


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
