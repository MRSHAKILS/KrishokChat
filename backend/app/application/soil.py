"""Soil moisture application service.

Two responsibilities:
1. ``dataset()`` — serve the frozen dataset info (never computed live).
2. ``analyze()`` — hard-locked. No moisture estimate can be produced until a
   validated regression artifact exists. The lock lives here, in the
   application layer, so no route or UI can bypass it.
"""

from __future__ import annotations

import logging

from PIL import Image

from app.application.vision_pipeline import image_quality
from app.domain.soil import (
    SoilDatasetInfo,
    SoilResult,
    SoilStage,
    SoilStatus,
    SoilTraceEvent,
)
from app.ports.audit import AuditSink

logger = logging.getLogger("krishokchat.soil")

LOCKED_MESSAGE = (
    "মাটির আর্দ্রতা নির্ণয় মডেলটি এখনো উন্নয়নে রয়েছে। "
    "ডেটাসেট প্রকাশিত হয়েছে; মডেল যাচাই হয়ে গেলে এই সুবিধা চালু হবে। "
    "আপাতত ডেটাসেট ও কৃষি পরামর্শ চ্যাট ব্যবহার করুন।"
)


class SoilService:
    def __init__(self, *, info: SoilDatasetInfo, audit: AuditSink) -> None:
        self.info = info
        self.audit = audit

    def dataset(self) -> SoilDatasetInfo:
        return self.info

    def analyze(self, image: Image.Image) -> SoilResult:
        """Validate the image, then refuse with an honest locked status.

        The quality gate still runs so the response explains *image* problems
        correctly (invalid_image) instead of blaming the missing model.
        """
        quality = image_quality(image)
        trace = (
            SoilTraceEvent(SoilStage.INTAKE, "complete", f"{quality.width}x{quality.height}"),
            SoilTraceEvent(SoilStage.MOISTURE_REGRESSION, "skip", "মডেল উন্নয়নে"),
            SoilTraceEvent(SoilStage.SOIL_CLASSIFICATION, "skip", "মডেল উন্নয়নে"),
            SoilTraceEvent(SoilStage.ADVISORY, "skip", "মডেল উন্নয়নে"),
        )
        if not quality.accepted:
            self._audit("invalid_image", error="; ".join(quality.warnings))
            return SoilResult(
                status=SoilStatus.INVALID_IMAGE,
                info=self.info,
                error="; ".join(quality.warnings),
                trace=trace,
            )

        self._audit("locked")
        return SoilResult(
            status=SoilStatus.LOCKED,
            info=self.info,
            error=LOCKED_MESSAGE,
            trace=trace,
        )

    def _audit(self, action: str, *, error: str | None = None) -> None:
        try:
            self.audit.record(
                {
                    "channel": "soil",
                    "action": action,
                    "status": self.info.model_status,
                    "model_releaseable": self.info.available,
                    "error": error,
                }
            )
        except Exception:  # noqa: BLE001 - auditing must never break the response
            logger.exception("soil audit write failed")