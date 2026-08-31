"""Public HTTP contracts. Internal pipeline objects live in ``app.domain``."""

from pydantic import BaseModel, Field, field_validator


class QARequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000, description="User's agricultural question in Bengali/Banglish")
    session_id: str | None = Field(None, description="Optional session ID for multi-turn")
    crop: str | None = Field(None, description="Detected crop from image (optional context)")
    disease: str | None = Field(None, description="Detected disease from image (optional context)")
    history: list[dict[str, str]] = Field(default_factory=list, description="Conversation history [{role, content}]")
    model: str | None = Field(None, description="Generation model choice: 'gemini' (default) or 'krishokchat-4b' (local Ollama)")
    farmer_context: str | None = Field(None, max_length=400, description="Optional stage-aware farmer context (P2); ignored when absent")

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


class VerifierClaimOut(BaseModel):
    claim: str
    verdict: str = Field(..., description="grounded | unsupported | no_dosage")
    reason: str = ""


class QAResponse(BaseModel):
    query: str
    category: str = Field(..., description="safe_agri | banned_or_restricted_chemical | ...")
    answer: str
    sources: list[SourceNode] = Field(default_factory=list)
    confidence: str = Field(..., description="verified | flagged-unverified | low_confidence")
    agent_trace: list[AgentStageEvent] = Field(default_factory=list)
    verifier_flags: list[str] = Field(default_factory=list)
    verifier_claims: list[VerifierClaimOut] = Field(default_factory=list)
    model: str | None = None
    # P5: refusal transparency (present when a deterministic rule refused).
    matched_rules: list[str] = Field(default_factory=list)
    safety_reason: str | None = None
    # R3: how the answer was produced (five-tier resolution ladder).
    # Values: deterministic_guard | structured_fact | templated_advisory
    #         | grounded_generation | honest_refusal
    resolution_tier: str = Field(
        default="grounded_generation",
        description=(
            "How the answer was produced. "
            "deterministic_guard: precheck rule matched, 0 LLM calls. "
            "structured_fact / templated_advisory: answered from fact rows, 0 LLM calls (R4). "
            "grounded_generation: retrieval → LLM → verifier, 1-2 LLM calls. "
            "honest_refusal: classifier or coverage-gate refused."
        ),
    )


class ClassifyRequest(BaseModel):
    pass  # Image uploaded as multipart/form-data


class ClassifyResponse(BaseModel):
    crop: str
    confidence: float
    crop_bn: str | None = None
    status: str = "diagnosed"
    top3: list[dict] = Field(default_factory=list)
    has_disease_model: bool = False
    clarification_prompt_bn: str | None = None
    suggested_crops: list[str] = Field(default_factory=list)
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
    status: str = Field(..., description="diagnosed | healthy | not_recognized | uncertain | out_of_distribution | requires_second_image | no_disease_model | model_error | invalid_image")
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
    clarification_prompt_bn: str | None = None
    suggested_crops: list[str] = Field(default_factory=list)
    requires_second_image: bool = False
    agent_trace: list[AgentStageEvent] = Field(default_factory=list)
    quality_warnings: list[str] = Field(default_factory=list)
    error: str | None = None


class SoilDatasetResponse(BaseModel):
    available: bool = False
    total_images: int = 0
    kpa_range: list[float] = Field(default_factory=list)
    kpa_bins: dict[str, int] = Field(default_factory=dict)
    soil_types: list[dict] = Field(default_factory=list)
    land_types: dict[str, int] = Field(default_factory=dict)
    crops: dict[str, int] = Field(default_factory=dict)
    growth_stages: dict[str, int] = Field(default_factory=dict)
    series_count: int = 0
    splits: dict[str, int] = Field(default_factory=dict)
    metadata_matched: int = 0
    metadata_inferred: int = 0
    corrections: int = 0
    collection: dict[str, str] = Field(default_factory=dict)
    model_status: str = "in_development"
    model_results: list[dict] = Field(default_factory=list)
    samples: list[dict] = Field(default_factory=list)


class SoilAnalyzeResponse(BaseModel):
    status: str = Field(..., description="locked | invalid_image | analyzed")
    error: str | None = None
    dataset: SoilDatasetResponse | None = None
    agent_trace: list[AgentStageEvent] = Field(default_factory=list)
    sample_id: str | None = Field(None, description="Released sample ID when the result is a measured-record replay; never set for live diagnosis")
    soil_type: str | None = None
    soil_type_bn: str | None = None
    kpa: float | None = None
    moisture_status: str | None = None
    moisture_status_bn: str | None = None
    advisory_bn: str | None = None
    confidence: float | None = None



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


class SavedQueryIn(BaseModel):
    query_text: str = Field(..., min_length=1, max_length=4000)
    answer_text: str = Field(..., min_length=1, max_length=20_000)
    sources: list[dict] = Field(default_factory=list)
    category: str = Field(default="", max_length=100)


class SavedQueryOut(BaseModel):
    id: str
    query_text: str
    answer_text: str
    sources: list[dict] = Field(default_factory=list)
    category: str = ""
    created_at: str
