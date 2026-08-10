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

# Display labels for user-selected crops. Keys must match registry disease keys.
CROP_DISPLAY = {
    "rice": "Rice",
    "wheat": "Wheat",
    "corn": "Corn",
    "potato": "Potato",
    "brassica": "Brassica",
}


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

    async def detect(self, image: Image.Image, *, crop_hint: str | None = None) -> VisionResult:
        quality = image_quality(image)
        trace = [VisionTraceEvent(VisionStage.INTAKE, "complete", f"{quality.width}x{quality.height}")]
        if not quality.accepted:
            result = VisionResult(status=VisionStatus.INVALID_IMAGE, quality=quality, trace=tuple(trace))
            self._audit(result)
            return result

        crop_label: str | None = None
        crop_confidence = 0.0
        crop_source = "model"
        top3_crops: tuple[dict[str, str | float], ...] = ()
        candidates: tuple[VisionModelSpec, ...] = ()

        # A user-verified crop (farmers know what they grow) bypasses the 6-class
        # crop classifier, which was trained without Rice. This is the only way a
        # rice leaf photo can reach the rice disease model today.
        if crop_hint:
            hinted = self.registry.disease_candidates(crop_hint)
            if hinted:
                crop_label = CROP_DISPLAY.get(crop_hint.strip().lower(), hinted[0].key.title())
                crop_source = "user"
                candidates = hinted
                trace.append(
                    VisionTraceEvent(VisionStage.CROP_CLASSIFICATION, "skip", f"{crop_label} (নির্বাচিত)")
                )

        if crop_label is None:
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
            crop_label = crop_prediction.label
            crop_confidence = crop_prediction.confidence
            top3_crops = crop_prediction.top3
            candidates = self.registry.disease_candidates(crop_label)
            # Documented mitigation (live-verified 2026-08-08): the 6-class crop
            # classifier has no Rice class and classifies rice leaves as Wheat.
            # Run the rice disease model alongside wheat and let the higher
            # confidence win, so a rice leaf still reaches the rice model.
            if crop_label == "Wheat":
                for extra in self.registry.disease_candidates("rice"):
                    if not any(candidate.key == extra.key for candidate in candidates):
                        candidates = candidates + (extra,)

        if not candidates:
            result = VisionResult(
                status=VisionStatus.NO_DISEASE_MODEL,
                crop=crop_label,
                crop_confidence=crop_confidence,
                crop_source=crop_source,
                top3_crops=top3_crops,
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
            logger.error("vision detect: all disease models failed for crop=%s — %s", crop_label, detail)
            result = VisionResult(
                status=VisionStatus.MODEL_ERROR,
                crop=crop_label,
                crop_confidence=crop_confidence,
                crop_source=crop_source,
                top3_crops=top3_crops,
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
                crop=crop_label,
                crop_confidence=crop_confidence,
                crop_source=crop_source,
                disease=disease_prediction.label,
                disease_confidence=disease_prediction.confidence,
                top3_crops=top3_crops,
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
                crop=crop_label,
                crop_confidence=crop_confidence,
                crop_source=crop_source,
                disease=disease_prediction.label,
                disease_confidence=disease_prediction.confidence,
                top3_crops=top3_crops,
                top3_diseases=disease_prediction.top3,
                disease_info=info,
                quality=quality,
                trace=tuple(trace),
            )
            self._audit(result)
            return result

        # When the wheat/rice ambiguity set was used and the rice model won,
        # report the winning crop family instead of the classifier's Wheat guess
        # (the rice disease model is what actually identified the leaf). Only
        # applied for a real disease diagnosis — for healthy/uncertain verdicts
        # the crop-family claim stays with the crop classifier.
        if crop_source == "model" and len(candidates) > 1:
            winner_label = CROP_DISPLAY.get(disease_spec.key, disease_spec.key.title())
            if winner_label != crop_label:
                crop_label = winner_label
                crop_confidence = disease_prediction.confidence

        seed_sources = self._disease_source(disease_spec.key, disease_prediction.label, info)
        advisory = None
        try:
            advisory = await self.qa.run(
                QAInput(
                    query=f"{crop_label} {disease_prediction.label} রোগের লক্ষণ, কারণ ও নিরাপদ ব্যবস্থাপনা কী?",
                    crop=crop_label,
                    disease=disease_prediction.label,
                    seed_sources=seed_sources,
                    channel="vision_advisory",
                )
            )
        except Exception as exc:  # noqa: BLE001 - advisory must never kill a valid diagnosis
            logger.error("vision detect: advisory failed for %s/%s: %s", crop_label, disease_prediction.label, exc)

        treatment_advice: str | None = None
        treatment_confidence: str | None = None
        treatment_sources: tuple[str, ...] = ()
        verifier_flags: tuple[str, ...] = ()

        if advisory is not None:
            trace.append(VisionTraceEvent(VisionStage.ADVISORY, "complete", advisory.confidence.value))
            treatment_advice = advisory.answer
            treatment_confidence = advisory.confidence.value
            treatment_sources = tuple(source.id for source in advisory.sources)
            verifier_flags = advisory.verifier_flags
            # If the advisory LLM is unavailable (safety fails closed → blocked /
            # low confidence), fall back to the knowledge-base solution so the
            # farmer still receives real, grounded treatment content.
            if advisory.confidence.value in {"blocked", "low_confidence"} and info and info.get("solution_bn"):
                treatment_advice = str(info["solution_bn"])
                treatment_confidence = "verified"
                treatment_sources = ()
            elif advisory.confidence.value in {"blocked", "low_confidence"}:
                treatment_confidence = "low_confidence"
        else:
            trace.append(VisionTraceEvent(VisionStage.ADVISORY, "skip", "knowledge-base fallback"))
            if info and info.get("solution_bn"):
                treatment_advice = str(info["solution_bn"])
                treatment_confidence = "verified"

        result = VisionResult(
            status=VisionStatus.DIAGNOSED,
            crop=crop_label,
            crop_confidence=crop_confidence,
            crop_source=crop_source,
            disease=disease_prediction.label,
            disease_confidence=disease_prediction.confidence,
            top3_crops=top3_crops,
            top3_diseases=disease_prediction.top3,
            disease_info=info,
            treatment_advice=treatment_advice,
            treatment_confidence=treatment_confidence,
            treatment_sources=treatment_sources,
            verifier_flags=verifier_flags,
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
