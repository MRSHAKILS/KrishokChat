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


class ResolutionTier(StrEnum):
    """How the answer was produced — the five-tier resolution ladder.

    T0  deterministic_guard   — precheck rule matched; 0 LLM calls
    T1  structured_fact       — provenance-carrying fact row; 0 LLM calls  (R4)
    T2  templated_advisory    — template filled from fact rows; 0 LLM calls (R4)
    T3  grounded_generation   — retrieval → LLM → verifier; 1-2 LLM calls
    T4  honest_refusal        — classifier/coverage-gate refusal; 0-1 LLM calls
    """

    DETERMINISTIC_GUARD = "deterministic_guard"
    STRUCTURED_FACT = "structured_fact"
    TEMPLATED_ADVISORY = "templated_advisory"
    GROUNDED_GENERATION = "grounded_generation"
    HONEST_REFUSAL = "honest_refusal"
