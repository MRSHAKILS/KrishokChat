"""Stage 2B: Agricultural Working Memory (PRISM-RAG Module 2B.2).

Maintains a structured agronomic state frame across conversational turns.
Prevents context drift, memory bloat, and prompt injection by retaining
typed slots rather than raw, unbounded conversation transcripts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgriculturalWorkingMemory:
    """Explicit, structured agronomic state frame for an active session."""

    crop: str | None = None
    problem_type: str | None = None  # disease | pest | fertilizer | weather | general
    symptom: str | None = None
    disease_candidate: str | None = None
    growth_stage: str | None = None
    location: str | None = None
    temporal_event: str | None = None  # e.g. "বৃষ্টির পর", "খরার পর"
    actionability: str = "high"        # high (seeking intervention) | informational
    turns_count: int = 0
    candidate_hypotheses: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["candidate_hypotheses"] = list(self.candidate_hypotheses)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> AgriculturalWorkingMemory:
        if not data or not isinstance(data, dict):
            return cls()
        return cls(
            crop=data.get("crop"),
            problem_type=data.get("problem_type"),
            symptom=data.get("symptom"),
            disease_candidate=data.get("disease_candidate"),
            growth_stage=data.get("growth_stage"),
            location=data.get("location"),
            temporal_event=data.get("temporal_event"),
            actionability=data.get("actionability", "high"),
            turns_count=int(data.get("turns_count", 0)),
            candidate_hypotheses=tuple(data.get("candidate_hypotheses") or ()),
        )

    def merge(
        self,
        *,
        crop: str | None = None,
        problem_type: str | None = None,
        symptom: str | None = None,
        disease_candidate: str | None = None,
        growth_stage: str | None = None,
        location: str | None = None,
        temporal_event: str | None = None,
        actionability: str | None = None,
        candidate_hypotheses: tuple[str, ...] | list[str] | None = None,
    ) -> AgriculturalWorkingMemory:
        """Merges new slot observations into the working memory.

        Detects crop topic shifts: if a new non-empty crop is specified and
        differs from the existing crop, the symptom and disease slots are reset.
        """
        is_topic_shift = bool(
            crop
            and self.crop
            and crop.strip().lower() != self.crop.strip().lower()
        )

        new_crop = crop or self.crop
        new_problem_type = None if is_topic_shift else (problem_type or self.problem_type)
        new_symptom = None if is_topic_shift else (symptom or self.symptom)
        new_disease = None if is_topic_shift else (disease_candidate or self.disease_candidate)
        new_growth_stage = None if is_topic_shift else (growth_stage or self.growth_stage)
        new_hypotheses = () if is_topic_shift else (
            tuple(candidate_hypotheses) if candidate_hypotheses is not None else self.candidate_hypotheses
        )

        return AgriculturalWorkingMemory(
            crop=new_crop,
            problem_type=new_problem_type,
            symptom=new_symptom,
            disease_candidate=new_disease,
            growth_stage=new_growth_stage,
            location=location or self.location,
            temporal_event=temporal_event or self.temporal_event,
            actionability=actionability or self.actionability,
            turns_count=self.turns_count + 1,
            candidate_hypotheses=new_hypotheses,
        )

    def as_context_line(self) -> str | None:
        """Produces a clean single-line context string for prompt / retrieval grounding."""
        parts = []
        if self.crop:
            parts.append(f"ফসল: {self.crop}")
        if self.disease_candidate:
            parts.append(f"সমস্যা/রোগ: {self.disease_candidate}")
        elif self.symptom:
            parts.append(f"লক্ষণ: {self.symptom}")
        if self.growth_stage:
            parts.append(f"পর্যায়: {self.growth_stage}")
        if self.location:
            parts.append(f"এলাকা: {self.location}")
        if self.temporal_event:
            parts.append(f"পরিস্থিতি: {self.temporal_event}")

        return " · ".join(parts) if parts else None
