"""R6: Capability Registry and Router — manages modular capabilities."""

from __future__ import annotations

import logging
from typing import Iterator

from app.domain.intent import Intent
from app.ports.capability import Capability, CapabilityDescriptor, CapabilityUnavailable

logger = logging.getLogger("krishokchat.capabilities")


class CapabilityRegistry:
    """Registry maintaining active and reserved advisory capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        """Register a new capability."""
        self._capabilities[capability.id] = capability
        logger.debug("Registered capability: %s (available=%s)", capability.id, capability.available)

    def get(self, capability_id: str) -> Capability | None:
        """Retrieve capability by ID."""
        return self._capabilities.get(capability_id)

    def list_descriptors(self) -> list[CapabilityDescriptor]:
        """Return descriptors for all registered capabilities."""
        return [cap.descriptor() for cap in self._capabilities.values()]

    def __len__(self) -> int:
        return len(self._capabilities)

    def __iter__(self) -> Iterator[Capability]:
        return iter(self._capabilities.values())


class CapabilityRouter:
    """Routes advisory inquiries to the best matching capability when enabled."""

    def __init__(self, registry: CapabilityRegistry, enabled: bool = False) -> None:
        self._registry = registry
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    def route(self, intent: Intent | None) -> Capability | None:
        """Pick the best available capability for this intent.

        Returns None if capability routing is disabled or no available capability matches.
        """
        if not self._enabled:
            return None

        best_cap: Capability | None = None
        best_score = 0.0

        for cap in self._registry:
            if not cap.available:
                continue
            score = cap.can_handle(intent)
            if score > best_score:
                best_score = score
                best_cap = cap

        return best_cap if best_score > 0.0 else None
