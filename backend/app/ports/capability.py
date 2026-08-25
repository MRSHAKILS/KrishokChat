"""R6: Capability port — the modular extension seam for KrishokChat.

Features (QA, disease, soil, weather, stage, irrigation, market, drone) register
as Capabilities behind this port instead of branching inside the orchestrator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from app.domain.contracts import QueryContext
from app.domain.enums import ResolutionTier
from app.domain.intent import Intent


class CapabilityUnavailable(Exception):
    """Raised when resolve() is called on an unavailable capability."""


@dataclass(frozen=True)
class CapabilityContext:
    """Input payload passed to Capability.resolve()."""

    query: str
    intent: Intent | None = None
    query_context: QueryContext = field(default_factory=QueryContext)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CapabilityResult:
    """Standardized output produced by any Capability."""

    capability_id: str
    answer: str
    resolution_tier: ResolutionTier
    provenance: dict[str, Any] = field(default_factory=dict)
    cost_estimate_usd: float | None = None
    stage_timings_ms: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CapabilityDescriptor:
    """Introspection metadata exposed via GET /api/capabilities."""

    id: str
    name_bn: str
    name_en: str
    description_bn: str
    requires: frozenset[str]
    available: bool
    status: str  # "active" | "replay_only" | "reserved_stub"


@runtime_checkable
class Capability(Protocol):
    """Protocol that all advisory modules must implement."""

    id: str
    name_bn: str
    name_en: str
    description_bn: str
    requires: frozenset[str]
    status: str

    @property
    def available(self) -> bool:
        """True only when all required backend assets/services are active."""
        ...

    def descriptor(self) -> CapabilityDescriptor:
        """Return introspection descriptor for UI and metadata panels."""
        ...

    def can_handle(self, intent: Intent | None) -> float:
        """Claim strength (0.0 to 1.0) indicating suitability for this intent."""
        ...

    async def resolve(self, ctx: CapabilityContext) -> CapabilityResult:
        """Resolve the advisory request. Raises CapabilityUnavailable if available is False."""
        ...
