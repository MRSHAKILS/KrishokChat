"""Soil moisture application service.

Two responsibilities:
1. ``dataset()`` — serve the frozen dataset info (never computed live).
2. ``analyze()`` — quality gate + measured-sample replay ONLY.

No validated moisture model exists yet (all candidate artifacts report
negative R²), so ``analyze()`` can never invent a diagnosis. It may only
REPLAY a known sample record from the frozen release package
(``samples_manifest.json``, loaded once into ``info.samples``) when the
uploaded filename carries that sample's image ID. Any other image — no
matter how clean — receives the honest locked response. Fabricating kPa /
soil-type values for unknown images would violate the project's
no-fabrication rule (AGENTS.md §2 rule 5).
"""

from __future__ import annotations

import logging
import re

from PIL import Image

from app.application.vision_pipeline import image_quality
from app.domain.soil import (
    SoilDatasetInfo,
    SoilResult,
    SoilSample,
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

# Matches e.g. "P0406_Atel_16.5kpa.jpg" -> "P0406". Uses a digit lookahead
# rather than \b: filenames continue with "_", which is a word character.
_SAMPLE_ID_RE = re.compile(r"[Pp](\d{4})(?!\d)")

# Bengali display names for the released soil series.
_SOIL_TYPE_BN = {
    "Doash": "দোআঁশ মাটি",
    "Atel": "এঁটেল মাটি",
    "Bele": "বেলে মাটি",
    "Poli": "পলি মাটি",
    "Bele_Doash": "বেলে-দোআঁশ মাটি",
    "Atel_Doash": "এঁটেল-দোআঁশ মাটি",
}

# Moisture-tension bands (kPa), mirroring the console UI thresholds.
_DRY_KPA = 12.0
_SATURATED_KPA = 2.0


def _moisture_band(kpa: float) -> tuple[str, str]:
    """Return (moisture_status, status_bn) for a measured tension."""
    if kpa >= _DRY_KPA:
        return "Dry", "শুষ্ক / আর্দ্রতার ঘাটতি"
    if kpa <= _SATURATED_KPA:
        return "Saturated", "সম্পূর্ণ সমৃক্ত / অতি-আর্দ্র"
    return "Optimum", "পরিমিত আর্দ্রতা (ফিল্ড ক্যাপাসিটি)"


def _band_advisory_bn(sample_id: str, kpa: float) -> str:
    base = (
        f"এটি পাবনা ডেটাসেট নমুনা {sample_id}-এর মাঠে পরিমাপিত রেকর্ড "
        f"(মডেল নির্ণয় নয়) — আর্দ্রতা টান {kpa:.1f} kPa। "
    )
    if kpa >= _DRY_KPA:
        return base + "এই মান ফসলের জন্য আর্দ্রতার ঘাটতি নির্দেশ করে; শিকড় অঞ্চলে পরিমিত সেচ প্রয়োগ করুন।"
    if kpa <= _SATURATED_KPA:
        return base + "মাটিতে অতিরিক্ত পানি রয়েছে; নিষ্কাশনের ব্যবস্থা করুন এবং সেচ সাময়িকভাবে স্থগিত রাখুন।"
    return base + "বর্তমান অবস্থা ফসলের জন্য আদর্শ — এই মুহূর্তে অতিরিক্ত সেচ প্রয়োজন নেই।"


class SoilService:
    def __init__(self, *, info: SoilDatasetInfo, audit: AuditSink) -> None:
        self.info = info
        self.audit = audit
        # Replay table straight from the frozen release manifest — every kPa /
        # soil-type value below comes from the released measurement record,
        # never hardcoded here.
        self._replay_by_id: dict[str, SoilSample] = {
            s.image_id.strip().upper(): s for s in info.samples if s.image_id
        }

    def dataset(self) -> SoilDatasetInfo:
        return self.info

    def analyze(self, image: Image.Image, filename: str | None = None) -> SoilResult:
        """Quality-gate the image, then replay a known sample or honestly lock."""
        quality = image_quality(image)
        if not quality.accepted:
            trace = (
                SoilTraceEvent(SoilStage.INTAKE, "error", f"{quality.width}x{quality.height}"),
                SoilTraceEvent(SoilStage.MOISTURE_REGRESSION, "skip", "ছবি ত্রুটিযুক্ত"),
                SoilTraceEvent(SoilStage.SOIL_CLASSIFICATION, "skip", "ছবি ত্রুটিযুক্ত"),
                SoilTraceEvent(SoilStage.ADVISORY, "skip", "ছবি ত্রুটিযুক্ত"),
            )
            self._audit("invalid_image", error="; ".join(quality.warnings))
            return SoilResult(
                status=SoilStatus.INVALID_IMAGE,
                info=self.info,
                error="; ".join(quality.warnings),
                trace=trace,
            )

        fn = filename or ""
        match = _SAMPLE_ID_RE.search(fn)
        sample = self._replay_by_id.get(match.group(0).upper()) if match else None

        if sample is None:
            # Honest lock: unknown images get NO diagnosis until a validated
            # model ships. Trace shows where the pipeline stopped and why.
            skip_reason = "মডেল উন্নয়নে — নমুনা রেকর্ড শনাক্ত নয়" if match else "মডেল উন্নয়নে"
            trace = (
                SoilTraceEvent(SoilStage.INTAKE, "complete", f"{quality.width}x{quality.height}"),
                SoilTraceEvent(SoilStage.MOISTURE_REGRESSION, "skip", skip_reason),
                SoilTraceEvent(SoilStage.SOIL_CLASSIFICATION, "skip", skip_reason),
                SoilTraceEvent(SoilStage.ADVISORY, "skip", skip_reason),
            )
            self._audit("locked")
            return SoilResult(
                status=SoilStatus.LOCKED,
                info=self.info,
                error=LOCKED_MESSAGE,
                trace=trace,
            )

        # Measured-sample replay: every displayed value is the released record.
        kpa = float(sample.kpa)
        moisture_status, moisture_status_bn = _moisture_band(kpa)
        soil_type_bn = _SOIL_TYPE_BN.get(sample.soil_type, sample.soil_type)
        trace = (
            SoilTraceEvent(SoilStage.INTAKE, "complete", f"{quality.width}x{quality.height}"),
            SoilTraceEvent(SoilStage.MOISTURE_REGRESSION, "complete", f"{kpa:.1f} kPa (পরিমাপিত)"),
            SoilTraceEvent(SoilStage.SOIL_CLASSIFICATION, "complete", soil_type_bn),
            SoilTraceEvent(SoilStage.ADVISORY, "complete", "সেচ সুপারিশ প্রস্তুত"),
        )
        self._audit("analyzed")
        return SoilResult(
            status=SoilStatus.ANALYZED,
            info=self.info,
            trace=trace,
            sample_id=sample.image_id,
            soil_type=sample.soil_type,
            soil_type_bn=soil_type_bn,
            kpa=kpa,
            moisture_status=moisture_status,
            moisture_status_bn=moisture_status_bn,
            advisory_bn=_band_advisory_bn(sample.image_id, kpa),
            # A replayed measurement has no model confidence; leaving this None
            # keeps the UI from showing an invented percentage.
            confidence=None,
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
