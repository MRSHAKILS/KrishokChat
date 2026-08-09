"""Evidence-honest multimodal advisory workflow.

The checked-in artifacts are classification models. The workflow therefore reports
classification confidence and never manufactures bounding boxes. A future real detection
adapter can be added behind the vision port without changing the HTTP route.
"""

from __future__ import annotations

import asyncio
import logging

from PIL import Image, ImageStat

from app.application.qa_pipeline import QAInput, QAPipeline
from app.domain.contracts import RetrievedSource
from app.domain.vision import (
    ImageQuality,
    VisionResult,
    VisionStage,
    VisionStatus,
    VisionTraceEvent,
)
from app.ports.audit import AuditSink
from app.ports.vision import VisionInferenceError, VisionModelRegistry, VisionRunner

logger = logging.getLogger("krishokchat.vision")


def image_quality(image: Image.Image, *, min_dimension: int = 64) -> ImageQuality:
    width, height = image.size
    warnings: list[str] = []
    if width < min_dimension or height < min_dimension:
        warnings.append(f"Image is too small; minimum dimension is {min_dimension}px")
    gray = image.convert("L")
    mean = ImageStat.Stat(gray).mean[0]
    variance = ImageStat.Stat(gray).var[0]
    if mean < 8:
        warnings.append("Image is extremely dark")
    if mean > 247:
        warnings.append("Image is extremely bright")
    if variance < 4:
        warnings.append("Image has very little visual detail")
    return ImageQuality(accepted=not warnings, width=width, height=height, warnings=tuple(warnings))


class VisionPipeline:
    def __init__(
        self,
        *,
        registry: VisionModelRegistry,
        runner: VisionRunner,
        qa: QAPipeline,
        audit: AuditSink,
        crop_threshold: float = 0.60,
        disease_threshold: float = 0.55,
        max_image_bytes: int = 10_000_000,
    ) -> None:
        self.registry = registry
        self.runner = runner
        self.qa = qa
        self.audit = audit
        self.crop_threshold = crop_threshold
        self.disease_threshold = disease_threshold
        self.max_image_bytes = max_image_bytes

    async def classify(self, image: Image.Image) -> VisionResult:
        quality = image_quality(image)
        trace = [VisionTraceEvent(VisionStage.INTAKE, "complete", f"{quality.width}x{quality.height}")]
        if not quality.accepted:
            result = VisionResult(
                status=VisionStatus.INVALID_IMAGE,
                quality=quality,
                trace=tuple(trace),
            )
            self._audit(result)
            return result
        try:
            prediction = await asyncio.to_thread(self.runner.predict, self.registry.crop_classifier, image)
        except VisionInferenceError as exc:
            logger.error("vision classify: crop classifier failed: %s", exc)
            result = VisionResult(status=VisionStatus.MODEL_ERROR, quality=quality, trace=tuple(trace), error=str(exc))
            self._audit(result)
            return result
        trace.append(VisionTraceEvent(VisionStage.CROP_CLASSIFICATION, "complete", prediction.label))
        status = VisionStatus.DIAGNOSED if prediction.confidence >= self.crop_threshold else VisionStatus.NOT_RECOGNIZED
        result = VisionResult(
            status=status,
            crop=prediction.label,
            crop_confidence=prediction.confidence,
            top3_crops=prediction.top3,
            quality=quality,
            trace=tuple(trace),
        )
        self._audit(result)
        return result

    async def detect(self, image: Image.Image) -> VisionResult:
        quality = image_quality(image)
        trace = [VisionTraceEvent(VisionStage.INTAKE, "complete", f"{quality.width}x{quality.height}")]
        if not quality.accepted:
            result = VisionResult(status=VisionStatus.INVALID_IMAGE, quality=quality, trace=tuple(trace))
            self._audit(result)
            return result

        try:
            crop_prediction = await asyncio.to_thread(self.runner.predict, self.registry.crop_classifier, image)
        except VisionInferenceError as exc:
            logger.error("vision detect: crop classifier failed: %s", exc)
            result = VisionResult(status=VisionStatus.MODEL_ERROR, quality=quality, trace=tuple(trace), error=str(exc))
            self._audit(result)
            return result
        trace.append(VisionTraceEvent(VisionStage.CROP_CLASSIFICATION, "complete", crop_prediction.label))
        if crop_prediction.confidence < self.crop_threshold:
            result = VisionResult(
                status=VisionStatus.NOT_RECOGNIZED,
                crop=crop_prediction.label,
                crop_confidence=crop_prediction.confidence,
                top3_crops=crop_prediction.top3,
                quality=quality,
                trace=tuple(trace),
            )
            self._audit(result)
            return result

        candidates = self.registry.disease_candidates(crop_prediction.label)
        if not candidates:
            result = VisionResult(
                status=VisionStatus.NO_DISEASE_MODEL,
                crop=crop_prediction.label,
                crop_confidence=crop_prediction.confidence,
                top3_crops=crop_prediction.top3,
                quality=quality,
                trace=tuple(trace),
            )
            self._audit(result)
            return result

        predictions = []
        errors: list[str] = []
        for spec in candidates:
            try:
                prediction = await asyncio.to_thread(self.runner.predict, spec, image)
                predictions.append((spec, prediction))
            except VisionInferenceError as exc:
                # Never swallow the failure silently — surface the real cause
                # so the API response / logs can explain what actually happened.
                errors.append(f"{spec.key}: {exc}")
        if not predictions:
            detail = "; ".join(errors) if errors else "no disease model candidates"
            logger.error("vision detect: all disease models failed for crop=%s — %s", crop_prediction.label, detail)
            result = VisionResult(
                status=VisionStatus.MODEL_ERROR,
                crop=crop_prediction.label,
                crop_confidence=crop_prediction.confidence,
                top3_crops=crop_prediction.top3,
                quality=quality,
                trace=tuple(trace),
                error=f"No routed disease model produced a prediction ({detail})",
            )
            self._audit(result)
            return result

        disease_spec, disease_prediction = max(predictions, key=lambda item: item[1].confidence)
        trace.append(VisionTraceEvent(VisionStage.DISEASE_CLASSIFICATION, "complete", disease_prediction.label))
        info = self.registry.disease_info(disease_spec.key, disease_prediction.label)
        if disease_prediction.confidence < self.disease_threshold:
            result = VisionResult(
                status=VisionStatus.NOT_RECOGNIZED,
                crop=crop_prediction.label,
                crop_confidence=crop_prediction.confidence,
                disease=disease_prediction.label,
                disease_confidence=disease_prediction.confidence,
                top3_crops=crop_prediction.top3,
                top3_diseases=disease_prediction.top3,
                disease_info=info,
                quality=quality,
                trace=tuple(trace),
            )
            self._audit(result)
            return result

        if self.registry.is_healthy(disease_prediction.label):
            result = VisionResult(
                status=VisionStatus.HEALTHY,
                crop=crop_prediction.label,
                crop_confidence=crop_prediction.confidence,
                disease=disease_prediction.label,
                disease_confidence=disease_prediction.confidence,
                top3_crops=crop_prediction.top3,
                top3_diseases=disease_prediction.top3,
                disease_info=info,
                quality=quality,
                trace=tuple(trace),
            )
            self._audit(result)
            return result

        seed_sources = self._disease_source(disease_spec.key, disease_prediction.label, info)
        advisory = await self.qa.run(
            QAInput(
                query=f"{crop_prediction.label} {disease_prediction.label} রোগের লক্ষণ, কারণ ও নিরাপদ ব্যবস্থাপনা কী?",
                crop=crop_prediction.label,
                disease=disease_prediction.label,
                seed_sources=seed_sources,
                channel="vision_advisory",
            )
        )
        trace.append(VisionTraceEvent(VisionStage.ADVISORY, "complete", advisory.confidence.value))

        # If the advisory LLM is unavailable (safety fails closed → blocked /
        # low confidence), fall back to the knowledge-base solution so the
        # farmer still receives real, grounded treatment content instead of
        # only a referral notice.
        treatment_advice = advisory.answer
        treatment_confidence = advisory.confidence.value
        if advisory.confidence.value in {"blocked", "low_confidence"} and info and info.get("solution_bn"):
            treatment_advice = str(info["solution_bn"])
            treatment_confidence = "verified"
        elif advisory.confidence.value in {"blocked", "low_confidence"}:
            treatment_confidence = "low_confidence"

        result = VisionResult(
            status=VisionStatus.DIAGNOSED,
            crop=crop_prediction.label,
            crop_confidence=crop_prediction.confidence,
            disease=disease_prediction.label,
            disease_confidence=disease_prediction.confidence,
            top3_crops=crop_prediction.top3,
            top3_diseases=disease_prediction.top3,
            disease_info=info,
            treatment_advice=treatment_advice,
            treatment_confidence=treatment_confidence,
            treatment_sources=tuple(source.id for source in advisory.sources),
            verifier_flags=advisory.verifier_flags,
            quality=quality,
            trace=tuple(trace),
        )
        self._audit(result)
        return result

    @staticmethod
    def _disease_source(model_key: str, label: str, info: dict | None) -> list[RetrievedSource]:
        if not info:
            return []
        content = "\n".join(
            value for value in (
                info.get("description_bn", ""),
                info.get("cause_bn", ""),
                info.get("solution_bn", ""),
            ) if value
        )
        if not content:
            return []
        return [
            RetrievedSource(
                id=f"vision-details:{model_key}:{label}",
                score=100.0,
                title_bn=str(info.get("class_name", label)),
                content_bn=content,
                source=f"vision/{model_key}/disease_details.json",
            )
        ]

    def _audit(self, result: VisionResult) -> None:
        self.audit.record(
            {
                "channel": "vision",
                "action": "vision_advisory",
                "status": result.status.value,
                "crop": result.crop,
                "crop_confidence": result.crop_confidence,
                "disease": result.disease,
                "disease_confidence": result.disease_confidence,
                "treatment_confidence": result.treatment_confidence,
                "verifier_flag": "; ".join(result.verifier_flags) or None,
                "detection_mode": "classification",
                "error": result.error,
            }
        )
