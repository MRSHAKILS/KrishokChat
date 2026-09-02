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
    VisionGateConfig,
    VisionModelSpec,
    VisionPrediction,
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
    "chilli": "Chilli",
}


def image_quality(
    image: Image.Image,
    *,
    min_dimension: int = 64,
    min_brightness: float = 20.0,
    max_brightness: float = 240.0,
    min_variance: float = 16.0,
) -> ImageQuality:
    width, height = image.size
    warnings: list[str] = []
    if width < min_dimension or height < min_dimension:
        warnings.append(f"Image is too small; minimum dimension is {min_dimension}px")
    gray = image.convert("L")
    mean = ImageStat.Stat(gray).mean[0]
    variance = ImageStat.Stat(gray).var[0]
    if mean < min_brightness:
        warnings.append("Image is too dark / underexposed")
    if mean > max_brightness:
        warnings.append("Image is too bright / overexposed")
    if variance < min_variance:
        warnings.append("Image is blurry or lacks sufficient foliar detail")
    return ImageQuality(accepted=not warnings, width=width, height=height, warnings=tuple(warnings))


class VisionPipeline:
    def __init__(
        self,
        *,
        registry: VisionModelRegistry,
        runner: VisionRunner,
        qa: QAPipeline,
        audit: AuditSink,
        max_image_bytes: int = 10_000_000,
        gate_config: VisionGateConfig | None = None,
        crop_threshold: float | None = None,
        disease_threshold: float | None = None,
    ) -> None:
        self.registry = registry
        self.runner = runner
        self.qa = qa
        self.audit = audit
        if gate_config is not None:
            self.gate_config = gate_config
        else:
            kwargs = {}
            if crop_threshold is not None:
                kwargs["crop_confidence_threshold"] = crop_threshold
            if disease_threshold is not None:
                kwargs["disease_confidence_threshold"] = disease_threshold
            self.gate_config = VisionGateConfig(**kwargs)
        self.crop_threshold = self.gate_config.crop_confidence_threshold
        self.disease_threshold = self.gate_config.disease_confidence_threshold
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

    async def detect(
        self,
        image: Image.Image,
        *,
        crop_hint: str | None = None,
        recovery_attempt: int = 0,
    ) -> VisionResult:
        quality = image_quality(
            image,
            min_dimension=self.gate_config.min_dimension,
            min_brightness=self.gate_config.min_brightness,
            max_brightness=self.gate_config.max_brightness,
            min_variance=self.gate_config.min_variance,
        )
        trace = [VisionTraceEvent(VisionStage.INTAKE, "complete", f"{quality.width}x{quality.height}")]
        if not quality.accepted:
            prompt_bn = "ছবিটি যথেষ্ট পরিষ্কার নয় বা আলো পর্যাপ্ত নেই। অনুগ্রহ করে ভালো আলোতে আক্রান্ত পাতার কাছে থেকে আরেকটি পরিষ্কার ছবি দিন।"
            result = VisionResult(
                status=VisionStatus.INVALID_IMAGE,
                quality=quality,
                trace=tuple(trace),
                clarification_prompt_bn=prompt_bn,
                recovery_attempt=recovery_attempt,
                can_retry=(recovery_attempt < self.gate_config.max_recovery_attempts),
            )
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
            
            # Calibrated Tri-State Crop Gate
            p1 = crop_prediction.confidence
            p2 = float(crop_prediction.top3[1].get("confidence", 0.0)) if len(crop_prediction.top3) > 1 else 0.0
            margin = p1 - p2
            top_crops = tuple(str(item.get("crop", "")) for item in crop_prediction.top3[:3] if item.get("crop"))

            # State C: Out of distribution / Unknown crop
            if p1 < self.gate_config.crop_ood_threshold:
                result = VisionResult(
                    status=VisionStatus.OUT_OF_DISTRIBUTION,
                    crop=crop_prediction.label,
                    crop_confidence=crop_prediction.confidence,
                    top3_crops=crop_prediction.top3,
                    quality=quality,
                    trace=tuple(trace),
                    clarification_prompt_bn="ছবিটি আমাদের সমর্থিত ফসলের সাথে পর্যাপ্ত মিলছে না। অনুগ্রহ করে আক্রান্ত ফসলের পরিষ্কার ছবি দিন।",
                    suggested_crops=top_crops,
                )
                self._audit(result)
                return result

            # Module 1B: Known botanical confusion pair risk check
            is_confusion_risk = False
            if self.gate_config.enable_confusion_risk_gating and len(crop_prediction.top3) > 1:
                c1 = str(crop_prediction.top3[0].get("crop") or crop_prediction.top3[0].get("class") or "").lower()
                c2 = str(crop_prediction.top3[1].get("crop") or crop_prediction.top3[1].get("class") or "").lower()
                solanaceae_foliar = {"potato", "solanacea", "tomato", "eggplant"}
                poaceae = {"rice", "wheat", "corn"}
                if (c1 in solanaceae_foliar and c2 in solanaceae_foliar) or (c1 in poaceae and c2 in poaceae):
                    is_confusion_risk = True

            # State B: Uncertain crop prediction (margin too small, below confidence threshold, or known confusion risk)
            if p1 < self.gate_config.crop_confidence_threshold or margin < self.gate_config.crop_margin_threshold or is_confusion_risk:
                label_lower = crop_prediction.label.lower()
                if label_lower in ("potato", "solanacea"):
                    prompt_bn = "ছবিটি দেখে আলু বা টমেটো/বেগুন গোত্রের গাছ মনে হচ্ছে। নিচে আপনার সঠিক ফসলটি নির্বাচন করুন।"
                    suggested = ("Potato", "Tomato", "Eggplant", "Chili")
                elif label_lower in ("wheat", "corn"):
                    prompt_bn = "ছবিটি দেখে ধান বা গম/ভুট্টা গোত্রের গাছ মনে হচ্ছে। নিচে আপনার সঠিক ফসলটি নির্বাচন করুন।"
                    suggested = ("Rice", "Wheat", "Corn")
                else:
                    prompt_bn = f"ছবিটি দেখে নিশ্চিত হওয়া যায়নি। এটি কি {crop_prediction.label} গাছ? নিচে সঠিক ফসল নির্বাচন করুন।"
                    suggested = top_crops

                result = VisionResult(
                    status=VisionStatus.UNCERTAIN,
                    crop=crop_prediction.label,
                    crop_confidence=crop_prediction.confidence,
                    top3_crops=crop_prediction.top3,
                    quality=quality,
                    trace=tuple(trace),
                    clarification_prompt_bn=prompt_bn,
                    suggested_crops=suggested,
                )
                self._audit(result)
                return result

            # State A: Confident standalone prediction
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
        
        # Model-specific calibrated operating thresholds (Stage 1 Step 5 & 6)
        conf_thresh, margin_thresh = self.gate_config.get_disease_threshold(disease_spec.key)

        # Check disease confidence margin
        d_p1 = disease_prediction.confidence
        d_p2 = float(disease_prediction.top3[1].get("confidence", 0.0)) if len(disease_prediction.top3) > 1 else 0.0
        d_margin = d_p1 - d_p2
        is_narrow_margin = d_margin < margin_thresh and d_p1 < conf_thresh
        can_attempt_recovery = recovery_attempt < self.gate_config.max_recovery_attempts
        requires_second = is_narrow_margin and can_attempt_recovery

        if disease_prediction.confidence < conf_thresh or is_narrow_margin:
            if requires_second:
                status = VisionStatus.REQUIRES_SECOND_IMAGE
                prompt_bn = "ছবিতে রোগটি নিশ্চিতভাবে আলাদা করা যায়নি। অনুগ্রহ করে আক্রান্ত পাতার আরও স্পষ্ট ও কাছ থেকে ছবি দিন।"
            elif not can_attempt_recovery and is_narrow_margin:
                # Stage 1 Step 8: Strict one-shot recovery limit exceeded -> Escalate / Abstain cleanly
                status = VisionStatus.NOT_RECOGNIZED
                prompt_bn = "একাধিক ছবিতেও রোগটি নিশ্চিতভাবে নির্ণয় করা যায়নি। অপ্রয়োজনীয় বালাইনাশক ব্যবহার না করে কৃষি কল সেন্টার ১৬১২৩-এ যোগাযোগ করুন বা স্থানীয় কৃষি কর্মকর্তার পরামর্শ নিন।"
            else:
                status = VisionStatus.NOT_RECOGNIZED
                prompt_bn = None

            result = VisionResult(
                status=status,
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
                requires_second_image=requires_second,
                recovery_attempt=recovery_attempt,
                can_retry=can_attempt_recovery and requires_second,
                clarification_prompt_bn=prompt_bn,
            )
            self._audit(result)
            return result

        if disease_prediction.label.lower() in ("others", "unknown", "other"):
            prompt_bn = "ছবিটি কোনো পরিচিত রোগের সাথে পর্যাপ্ত মিলছে না। অনুগ্রহ করে আক্রান্ত পাতার আরও স্পষ্ট ও কাছ থেকে ছবি দিন অথবা কৃষি কল সেন্টার ১৬১২৩-এ যোগাযোগ করুন।"
            result = VisionResult(
                status=VisionStatus.NOT_RECOGNIZED,
                crop=crop_label,
                crop_confidence=crop_confidence,
                crop_source=crop_source,
                disease=disease_prediction.label,
                disease_confidence=disease_prediction.confidence,
                top3_crops=top3_crops,
                top3_diseases=disease_prediction.top3,
                quality=quality,
                trace=tuple(trace),
                clarification_prompt_bn=prompt_bn,
                can_retry=False,
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
                treatment_confidence = "low_confidence"
                treatment_sources = ()
            elif advisory.confidence.value in {"blocked", "low_confidence"}:
                treatment_confidence = "low_confidence"
        else:
            trace.append(VisionTraceEvent(VisionStage.ADVISORY, "skip", "knowledge-base fallback"))
            if info and info.get("solution_bn"):
                treatment_advice = str(info["solution_bn"])
                treatment_confidence = "low_confidence"

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
