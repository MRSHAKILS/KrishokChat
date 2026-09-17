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

    T0  deterministic_guard       — precheck rule matched; 0 LLM calls
    T1  structured_fact           — provenance-carrying fact row; 0 LLM calls  (R4)
    T2  templated_advisory        — template filled from fact rows; 0 LLM calls (R4)
    T3  grounded_generation       — retrieval → LLM → verifier; 1-2 LLM calls
    T4  honest_refusal            — classifier/coverage-gate refusal; 0-1 LLM calls
    T5  interactive_clarification — missing critical slot; dynamic clarification turn
    """

    DETERMINISTIC_GUARD = "deterministic_guard"
    STRUCTURED_FACT = "structured_fact"
    TEMPLATED_ADVISORY = "templated_advisory"
    GROUNDED_GENERATION = "grounded_generation"
    PROGRESSIVE_GUIDANCE = "progressive_guidance"
    HONEST_REFUSAL = "honest_refusal"
    INTERACTIVE_CLARIFICATION = "interactive_clarification"


class AnswerabilityLevel(StrEnum):
    """The 5-Level Answerability Spectrum (KAERA / PRISM).

    A1  fully_supported       — accredited fact row (T1/T2); direct 0-LLM resolution
    A2  strong_evidence       — complete RAG grounding + verified dosage & PHI
    A3  partial_evidence      — missing exact chemical dose; progressive cultural guidance + observation checklist
    A4  missing_critical_info — underspecified query; minimum necessary clarification (single Q + chips)
    A5  unsafe_action         — banned chemical / crisis probe; refuse action + 16123 referral
    """

    A1_FULLY_SUPPORTED = "A1_fully_supported"
    A2_STRONG_EVIDENCE = "A2_strong_evidence"
    A3_PARTIAL_EVIDENCE = "A3_partial_evidence"
    A4_MISSING_CRITICAL_INFO = "A4_missing_critical_info"
    A5_UNSAFE_ACTION = "A5_unsafe_action"

