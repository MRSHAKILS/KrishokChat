"""R6: Capability registry and modular implementations."""

from app.application.capabilities.qa_capability import QACapability
from app.application.capabilities.registry import CapabilityRegistry, CapabilityRouter
from app.application.capabilities.stubs import (
    DiseaseAdvisoryCapability,
    SafetyEscalationCapability,
    SoilAdvisoryCapability,
    StageAdviceCapability,
    StubCapability,
    WeatherRiskCapability,
)

__all__ = [
    "CapabilityRegistry",
    "CapabilityRouter",
    "QACapability",
    "DiseaseAdvisoryCapability",
    "SoilAdvisoryCapability",
    "WeatherRiskCapability",
    "StageAdviceCapability",
    "SafetyEscalationCapability",
    "StubCapability",
]
