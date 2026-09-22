from __future__ import annotations

import asyncio
import unittest
from pathlib import Path

from PIL import Image

from app.application.vision_pipeline import VisionPipeline
from app.core.config import settings
from app.domain.contracts import QAResult, RetrievedSource
from app.domain.enums import SafetyCategory, VerificationConfidence
from app.domain.vision import VisionModelSpec, VisionPrediction, VisionStatus
from app.infrastructure.vision.registry import ArtifactVisionRegistry


class FakeRegistry:
    crop_spec = VisionModelSpec(key="crop_classifier", path=Path("crop.pt"), class_names=("Potato",))
    disease_spec = VisionModelSpec(key="potato", path=Path("potato.pt"), class_names=("Potato__Early_Blight",))

    @property
    def crop_classifier(self):
        return self.crop_spec

    def disease_candidates(self, crop: str):
        return (self.disease_spec,) if crop == "Potato" else ()

    def disease_info(self, model_key: str, label: str):
        return {
            "class_name": "Early Blight (আগাম ব্লাইট)",
            "description_bn": "পাতায় বাদামী দাগ দেখা যায়।",
            "cause_bn": "ছত্রাকের কারণে হয়।",
            "solution_bn": "পরিষ্কার পরিচর্যা করুন।",
        }

    def is_healthy(self, label: str):
        return "healthy" in label.lower()


class FakeRunner:
    def predict(self, spec, image):
        if spec.key == "crop_classifier":
            return VisionPrediction("Potato", 0.98, ({"class": "Potato", "confidence": 0.98},))
        return VisionPrediction("Potato__Early_Blight", 0.95, ({"class": "Potato__Early_Blight", "confidence": 0.95},))


class FakeQA:
    async def run(self, request):
        return QAResult(
            query=request.query,
            category=SafetyCategory.SAFE_AGRI,
            answer="উৎসভিত্তিক নিরাপদ ব্যবস্থাপনা।",
            sources=(RetrievedSource(id="vision-details:potato:Potato__Early_Blight", score=100),),
            confidence=VerificationConfidence.VERIFIED,
        )


class FakeQAFailsClosed:
    """Safety blocks the advisory (e.g. LLM unavailable) — no sources ever."""

    async def run(self, request):
        return QAResult(
            query=request.query,
            category=SafetyCategory.SAFE_AGRI,
            answer="",
            sources=(),
            confidence=VerificationConfidence.BLOCKED,
        )


class FakeQAErrors:
    """The advisory LLM call itself raises — pipeline must not crash the diagnosis."""

    async def run(self, request):
        raise RuntimeError("simulated advisory outage")


class FakeQANoInfoRegistry(FakeRegistry):
    """Disease info exists but carries no solution — no knowledge-base fallback."""

    def disease_info(self, model_key: str, label: str):
        return {
            "class_name": "Early Blight (আগাম ব্লাইট)",
            "description_bn": "পাতায় বাদামী দাগ দেখা যায়।",
            "cause_bn": "ছত্রাকের কারণে হয়।",
            "solution_bn": "",
        }


class FakeAudit:
    def __init__(self):
        self.entries = []

    def record(self, entry):
        self.entries.append(entry)


class VisionPipelineTests(unittest.TestCase):
    def test_artifact_registry_uses_real_class_maps_and_matches_details(self):
        registry = ArtifactVisionRegistry(Path(settings.ml_assets_dir) / "vision")
        self.assertIn("potato", registry.disease_models)
        self.assertIn("Potato__Early_Blight", registry.disease_models["potato"].class_names)
        self.assertIsNotNone(registry.disease_info("potato", "Potato__Early_Blight"))

    def test_low_detail_image_stops_before_model_inference(self):
        audit = FakeAudit()
        pipeline = VisionPipeline(
            registry=FakeRegistry(), runner=FakeRunner(), qa=FakeQA(), audit=audit
        )
        result = asyncio.run(pipeline.detect(Image.new("RGB", (128, 128), "black")))
        self.assertEqual(result.status, VisionStatus.INVALID_IMAGE)
        self.assertEqual(len(audit.entries), 1)

    def test_classification_routes_to_advisory_workflow_without_boxes(self):
        audit = FakeAudit()
        pipeline = VisionPipeline(
            registry=FakeRegistry(), runner=FakeRunner(), qa=FakeQA(), audit=audit
        )
        image = Image.new("RGB", (128, 128), "white")
        # Add visual variance so the lightweight quality gate accepts the fixture.
        for x in range(0, 128, 2):
            for y in range(0, 128, 2):
                image.putpixel((x, y), (20, 120, 40))
        result = asyncio.run(pipeline.detect(image))
        self.assertEqual(result.status, VisionStatus.DIAGNOSED)
        self.assertEqual(result.disease, "Potato__Early_Blight")
        self.assertEqual(result.treatment_confidence, "verified")
        self.assertTrue(result.treatment_advice)
        self.assertEqual(len(audit.entries), 1)

    # --- T21 regression: source-empty treatment must never be marked verified ---

    def _textured_image(self):
        image = Image.new("RGB", (128, 128), "white")
        for x in range(0, 128, 2):
            for y in range(0, 128, 2):
                image.putpixel((x, y), (20, 120, 40))
        return image

    def test_advisory_fails_closed_kb_fallback_is_low_confidence_with_empty_sources(self):
        """QA blocks (safety fail-closed) -> KB fallback: never 'verified', no sources."""
        audit = FakeAudit()
        pipeline = VisionPipeline(
            registry=FakeRegistry(), runner=FakeRunner(), qa=FakeQAFailsClosed(), audit=audit
        )
        result = asyncio.run(pipeline.detect(self._textured_image()))
        self.assertEqual(result.status, VisionStatus.DIAGNOSED)
        self.assertEqual(result.treatment_confidence, "low_confidence")
        self.assertNotEqual(result.treatment_confidence, "verified")
        self.assertEqual(result.treatment_sources, ())
        self.assertIn("পরিচর্যা", result.treatment_advice)  # KB solution text served
        self.assertTrue(any(event.stage.value == "advisory" for event in result.trace))
        self.assertEqual(len(audit.entries), 1)

    def test_advisory_error_kb_fallback_is_low_confidence_with_empty_sources(self):
        """QA raises -> advisory skipped -> KB fallback: still never 'verified'."""
        audit = FakeAudit()
        pipeline = VisionPipeline(
            registry=FakeRegistry(), runner=FakeRunner(), qa=FakeQAErrors(), audit=audit
        )
        result = asyncio.run(pipeline.detect(self._textured_image()))
        self.assertEqual(result.status, VisionStatus.DIAGNOSED)
        self.assertEqual(result.treatment_confidence, "low_confidence")
        self.assertNotEqual(result.treatment_confidence, "verified")
        self.assertEqual(result.treatment_sources, ())
        self.assertIn("পরিচর্যা", result.treatment_advice)
        self.assertEqual(len(audit.entries), 1)

    def test_no_kb_solution_marks_no_claim_at_all(self):
        """Disease info without a solution: no treatment claim, no verified status."""
        audit = FakeAudit()
        pipeline = VisionPipeline(
            registry=FakeQANoInfoRegistry(), runner=FakeRunner(), qa=FakeQAErrors(), audit=audit
        )
        result = asyncio.run(pipeline.detect(self._textured_image()))
        self.assertEqual(result.status, VisionStatus.DIAGNOSED)
        self.assertIsNone(result.treatment_confidence)
        self.assertIsNone(result.treatment_advice)
        self.assertEqual(result.treatment_sources, ())
        self.assertEqual(len(audit.entries), 1)

    def test_crop_calibrated_tri_state_uncertain(self):
        """When crop confidence or margin is low, status is UNCERTAIN with Bengali prompt."""
        class UncertainRunner:
            def predict(self, spec, image):
                if spec.key == "crop_classifier":
                    return VisionPrediction(
                        "Potato", 0.52, (
                            {"crop": "Potato", "confidence": 0.52},
                            {"crop": "Tomato", "confidence": 0.44},
                        )
                    )
                return VisionPrediction("Potato__Early_Blight", 0.90)

        pipeline = VisionPipeline(registry=FakeRegistry(), runner=UncertainRunner(), qa=FakeQA(), audit=FakeAudit())
        result = asyncio.run(pipeline.detect(self._textured_image()))
        self.assertEqual(result.status, VisionStatus.UNCERTAIN)
        self.assertIsNotNone(result.clarification_prompt_bn)
        self.assertIn("Potato", result.suggested_crops)

    def test_crop_calibrated_tri_state_out_of_distribution(self):
        """When crop confidence is < 0.40, status is OUT_OF_DISTRIBUTION and disease model halts."""
        class OODRunner:
            def predict(self, spec, image):
                if spec.key == "crop_classifier":
                    return VisionPrediction(
                        "Potato", 0.28, (
                            {"crop": "Potato", "confidence": 0.28},
                            {"crop": "Wheat", "confidence": 0.25},
                        )
                    )
                raise AssertionError("Disease model should not be invoked for OOD crops")

        pipeline = VisionPipeline(registry=FakeRegistry(), runner=OODRunner(), qa=FakeQA(), audit=FakeAudit())
        result = asyncio.run(pipeline.detect(self._textured_image()))
        self.assertEqual(result.status, VisionStatus.OUT_OF_DISTRIBUTION)
        self.assertIn("সমর্থিত ফসলের সাথে পর্যাপ্ত মিলছে না", result.clarification_prompt_bn)

    def test_disease_requires_second_image_on_ambiguous_margin(self):
        """When disease prediction has low margin below threshold, request second image."""
        class AmbiguousDiseaseRunner:
            def predict(self, spec, image):
                if spec.key == "crop_classifier":
                    return VisionPrediction("Potato", 0.95, ({"crop": "Potato", "confidence": 0.95},))
                return VisionPrediction(
                    "Potato__Early_Blight", 0.48, (
                        {"disease": "Potato__Early_Blight", "confidence": 0.48},
                        {"disease": "Potato__Late_Blight", "confidence": 0.42},
                    )
                )

        pipeline = VisionPipeline(registry=FakeRegistry(), runner=AmbiguousDiseaseRunner(), qa=FakeQA(), audit=FakeAudit())
        result = asyncio.run(pipeline.detect(self._textured_image()))
        self.assertEqual(result.status, VisionStatus.REQUIRES_SECOND_IMAGE)
        self.assertTrue(result.requires_second_image)
        self.assertTrue(result.can_retry)
        self.assertIn("কাছ থেকে", result.clarification_prompt_bn)

        # Stage 1 Step 8: When recovery_attempt >= 1, second image request is blocked and redirected to 16123
        result_retry = asyncio.run(pipeline.detect(self._textured_image(), recovery_attempt=1))
        self.assertEqual(result_retry.status, VisionStatus.NOT_RECOGNIZED)
        self.assertFalse(result_retry.requires_second_image)
        self.assertFalse(result_retry.can_retry)
        self.assertIn("১৬১২৩", result_retry.clarification_prompt_bn)

    def test_disease_hint_bypasses_runner_for_client_side_inference(self):
        """When disease_hint is provided (from on-device WASM), runner is never invoked."""
        class FailIfCalledRunner:
            def predict(self, spec, image):
                raise AssertionError("Runner must not be called when disease_hint is supplied")

        pipeline = VisionPipeline(
            registry=FakeRegistry(),
            runner=FailIfCalledRunner(),
            qa=FakeQA(),
            audit=FakeAudit(),
        )
        result = asyncio.run(
            pipeline.detect(
                self._textured_image(),
                crop_hint="Potato",
                disease_hint="Potato__Early_Blight",
            )
        )
        self.assertEqual(result.status, VisionStatus.DIAGNOSED)
        self.assertEqual(result.crop, "Potato")
        self.assertEqual(result.disease, "Potato__Early_Blight")
        self.assertIsNotNone(result.treatment_advice)
        self.assertEqual(result.treatment_advice, "উৎসভিত্তিক নিরাপদ ব্যবস্থাপনা।")
        self.assertEqual(result.disease_info["class_name"], "Early Blight (আগাম ব্লাইট)")


if __name__ == "__main__":
    unittest.main()

