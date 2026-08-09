from enum import StrEnum


class SafetyCategory(StrEnum):
    SAFE_AGRI = "safe_agri"
    BANNED_OR_RESTRICTED_CHEMICAL = "banned_or_restricted_chemical"
    SELF_HARM_OR_POISONING_RISK = "self_harm_or_poisoning_risk"
    OFF_TOPIC = "off_topic"
    PROMPT_INJECTION = "prompt_injection"
    LOW_CONFIDENCE = "low_confidence"


class VerificationConfidence(StrEnum):
    VERIFIED = "verified"
    FLAGGED_UNVERIFIED = "flagged-unverified"
    LOW_CONFIDENCE = "low_confidence"
    BLOCKED = "blocked"


class PipelineStage(StrEnum):
    SAFETY = "safety"
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    VERIFIER = "verifier"


class StageStatus(StrEnum):
    START = "start"
    COMPLETE = "complete"
    SKIP = "skip"
    ERROR = "error"
