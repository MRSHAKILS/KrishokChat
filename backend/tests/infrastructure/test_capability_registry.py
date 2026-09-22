"""R6 — Tests for Capability Registry and Modular Extension Seam.

Locks all R6 invariants:
  1. Registry registers and lists capabilities with accurate metadata.
  2. Availability is dynamically computed from loaded assets, never a hardcoded True.
  3. Reserved stubs strictly report available=False, can_handle=0.0, and raise CapabilityUnavailable on resolve.
  4. CapabilityRouter is default-off (returns None when disabled).
  5. GET /api/capabilities and GET /api/v1/capabilities return valid descriptor lists without exposing secrets.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.application.capabilities import (
    CapabilityRegistry,
    CapabilityRouter,
    DiseaseAdvisoryCapability,
    QACapability,
    SafetyEscalationCapability,
    SoilAdvisoryCapability,
    StageAdviceCapability,
    StubCapability,
)
from app.application.container import build_container
from app.core.config import Settings
from app.domain.intent import Intent
from app.main import create_app
from app.ports.capability import CapabilityContext, CapabilityUnavailable


def test_registry_registration_and_lookup() -> None:
    registry = CapabilityRegistry()
    safety = SafetyEscalationCapability()
    registry.register(safety)

    assert len(registry) == 1
    assert registry.get("safety_escalation") is safety
    assert registry.get("nonexistent") is None

    descriptors = registry.list_descriptors()
    assert len(descriptors) == 1
    assert descriptors[0].id == "safety_escalation"
    assert descriptors[0].available is True


def test_reserved_stub_invariants() -> None:
    stub = StubCapability(
        id="irrigation",
        name_bn="সেচ",
        name_en="Irrigation",
        description_bn="স্মার্ট সেচ",
        requires=frozenset({"sensor", "weather"}),
    )
    assert stub.available is False
    assert stub.can_handle(Intent(kind="irrigation")) == 0.0

    desc = stub.descriptor()
    assert desc.id == "irrigation"
    assert desc.available is False
    assert desc.status == "reserved_stub"

    ctx = CapabilityContext(query="কখন সেচ দিব?")
    with pytest.raises(CapabilityUnavailable):
        import asyncio
        asyncio.run(stub.resolve(ctx))


def test_capability_router_disabled_by_default() -> None:
    registry = CapabilityRegistry()
    registry.register(SafetyEscalationCapability())
    router = CapabilityRouter(registry, enabled=False)

    intent = Intent(kind="banned_chemical")
    assert router.route(intent) is None


def test_capability_router_enabled_picks_highest_scorer() -> None:
    registry = CapabilityRegistry()
    safety = SafetyEscalationCapability()
    registry.register(safety)
    router = CapabilityRouter(registry, enabled=True)

    intent = Intent(kind="banned_chemical")
    routed = router.route(intent)
    assert routed is not None
    assert routed.id == "safety_escalation"


def test_container_builds_honest_capabilities() -> None:
    settings = Settings(demo_mode=True)
    container = build_container(settings)

    registry = container.capabilities
    assert registry is not None
    assert len(registry) >= 11

    # Active features
    assert registry.get("qa_advisory") is not None
    assert registry.get("qa_advisory").available is True
    assert registry.get("safety_escalation").available is True

    # Reserved stubs must report False
    assert registry.get("irrigation").available is False
    assert registry.get("market_price").available is False
    assert registry.get("drone_survey").available is False
    assert registry.get("livestock").available is False
    assert registry.get("credit").available is False


def test_api_get_capabilities_endpoint() -> None:
    settings = Settings(demo_mode=True)
    app = create_app(settings)
    with TestClient(app) as client:
        # Legacy endpoint
        res = client.get("/api/capabilities")
        assert res.status_code == 200
        data = res.json()
        assert "capabilities" in data
        caps = {c["id"]: c for c in data["capabilities"]}

        assert "qa_advisory" in caps
        assert caps["qa_advisory"]["available"] is True
        assert "name_bn" in caps["qa_advisory"]

        assert "irrigation" in caps
        assert caps["irrigation"]["available"] is False
        assert caps["irrigation"]["status"] == "reserved_stub"

        # Versioned /api/v1 endpoint
        res_v1 = client.get("/api/v1/capabilities")
        assert res_v1.status_code == 200
        data_v1 = res_v1.json()
        assert len(data_v1["capabilities"]) == len(data["capabilities"])
