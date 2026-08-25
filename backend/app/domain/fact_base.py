"""R2 — Fact-base domain objects.

Pure data classes: no I/O, no LLM.  The loader lives in
``app.infrastructure.knowledge.fact_base_store``.

A ``Fact`` is one validated, provenance-carrying answer row:
  crop × problem × stage → active_ingredient + dose band + IPM alternatives.

A ``FactBase`` holds a collection of facts and exposes a single pure
``lookup(crop, problem, stage) -> list[Fact]`` query.  Stage is optional —
passing ``stage=None`` returns all facts for the crop/problem pair.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Fact:
    """One validated, provenance-carrying fact row.

    All numeric fields are correct-by-construction (the builder validates them;
    see ``scripts/build_fact_base.py``). None of them should ever be None once
    loaded from a validated artifact — but callers must treat the object as
    read-only (frozen=True).
    """

    # ------------------------------------------------------------------
    # Identity keys (used by FactBase.lookup)
    # ------------------------------------------------------------------
    crop: str                       # e.g. "potato"
    crop_bn: str                    # e.g. "আলু"
    problem: str                    # e.g. "late_blight"
    problem_bn: str                 # e.g. "নাবি ধ্বসা / লেট ব্লাইট"
    problem_type: str               # disease | pest | deficiency | abiotic
    stage: str                      # must be a key from crop_calendars_v1.json

    # ------------------------------------------------------------------
    # Answer payload
    # ------------------------------------------------------------------
    active_ingredient: str          # normalised EN name (mancozeb, …)
    dose_min: float
    dose_max: float
    dose_unit: str                  # g/l | ml/l | g/ha | kg/ha
    application_interval_days: int
    pre_harvest_interval_days: int
    ipm_alternatives_bn: tuple[str, ...] = field(default_factory=tuple)

    # ------------------------------------------------------------------
    # Provenance
    # ------------------------------------------------------------------
    banned_flag: bool = False
    severity: str = "high"          # high | medium | low
    source_node_id: str = ""        # corpus node ID (empty = curated-approximation)
    source_doc: str = ""
    citation: str = ""
    grounding: str = "curated-approximation"   # corpus-extracted | curated-approximation
    confidence: float = 0.0

    @classmethod
    def from_dict(cls, row: dict) -> "Fact":
        """Deserialise one validated row from the fact-base artifact."""
        return cls(
            crop=str(row["crop"]),
            crop_bn=str(row.get("crop_bn", "")),
            problem=str(row["problem"]),
            problem_bn=str(row.get("problem_bn", "")),
            problem_type=str(row.get("problem_type", "disease")),
            stage=str(row["stage"]),
            active_ingredient=str(row["active_ingredient"]),
            dose_min=float(row["dose_min"]),
            dose_max=float(row["dose_max"]),
            dose_unit=str(row["dose_unit"]),
            application_interval_days=int(row["application_interval_days"]),
            pre_harvest_interval_days=int(row["pre_harvest_interval_days"]),
            ipm_alternatives_bn=tuple(str(s) for s in (row.get("ipm_alternatives_bn") or [])),
            banned_flag=bool(row.get("banned_flag", False)),
            severity=str(row.get("severity", "high")),
            source_node_id=str(row.get("source_node_id", "")),
            source_doc=str(row.get("source_doc", "")),
            citation=str(row.get("citation", "")),
            grounding=str(row.get("grounding", "curated-approximation")),
            confidence=float(row.get("confidence", 0.0)),
        )


@dataclass
class FactBase:
    """In-memory collection of validated fact rows.

    Built once at startup (R4 wires this into the container when
    STRUCTURED_RESOLVER_ENABLED=true); kept in-process, no I/O after load.

    lookup() is the only public query surface; it is intentionally simple
    to keep the T1/T2 resolver deterministic and unit-testable.
    """

    facts: tuple[Fact, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> "FactBase":
        return cls(facts=())

    @classmethod
    def from_artifact(cls, payload: dict) -> "FactBase":
        """Build a FactBase from the validated JSON payload."""
        rows = []
        for row in payload.get("facts", []):
            try:
                rows.append(Fact.from_dict(row))
            except (KeyError, TypeError, ValueError):
                # Corrupted rows are skipped — the builder should have caught them.
                continue
        return cls(facts=tuple(rows))

    def lookup(
        self,
        crop: str,
        problem: str,
        stage: str | None = None,
    ) -> list[Fact]:
        """Return facts matching crop and problem, optionally filtered by stage.

        Matching is case-insensitive on crop and problem.  Stage comparison is
        exact (stage keys are controlled vocabulary from crop_calendars_v1.json).

        Returns an empty list when no facts match — never raises.
        """
        crop_l = crop.lower()
        problem_l = problem.lower()
        results = [
            f for f in self.facts
            if f.crop.lower() == crop_l and f.problem.lower() == problem_l
        ]
        if stage is not None:
            results = [f for f in results if f.stage == stage]
        return sorted(results, key=lambda f: -f.confidence)

    def __len__(self) -> int:
        return len(self.facts)
