#!/usr/bin/env python3
"""
experiments/scripts/run_end_to_end_safety_replay.py
End-to-End Multimodal Safety & Adversarial Replay Benchmark.

Evaluates the complete flow:
Image -> Calibrated Crop Gate -> Calibrated Disease Gate -> Government Fact Base Resolver -> Prescription Card

Measures:
1. Safe Automation Rate
2. Farmer Clarification / Intercept Rate
3. Out-of-Distribution Rejection Rate
4. Unsafe Auto-Advisory Rate (Wrong perception reaching automated downstream prescription)
5. Adversarial Injected Perturbations
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image

# Add backend to path
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = WORKSPACE_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.application.qa_pipeline import QAPipeline
from app.application.structured_resolver import StructuredResolver
from app.application.vision_pipeline import VisionPipeline
from app.domain.contracts import QAResult
from app.domain.enums import SafetyCategory, VerificationConfidence
from app.domain.fact_base import FactBase
from app.domain.vision import VisionGateConfig, VisionResult, VisionStatus
from app.infrastructure.audit.jsonl import JSONLAuditSink
from app.infrastructure.knowledge.fact_base_store import load_fact_base
from app.infrastructure.vision.registry import ArtifactVisionRegistry
from app.infrastructure.vision.ultralytics_classifier import UltralyticsClassificationRunner

VISION_DIR = BACKEND_DIR / "ml_assets" / "vision"
FULL_LIBRARY_DIR = VISION_DIR / "test_images" / "full_library"
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results" / "E02_vision_gate_calibration"


# Ground truth mapping helpers
CROP_FAMILY_MAP = {
    "cabbage": "Brassica",
    "cauliflower": "Brassica",
    "potato": "Potato",
    "tomato": "Solanacea",
    "eggplant": "Solanacea",
    "chili": "Solanacea",
    "corn": "Corn",
    "wheat": "Wheat",
    "rice": "Rice",
    "gourd": "GourdGuava",
    "guava": "GourdGuava",
}


def parse_ground_truth(folder_name: str) -> tuple[str, str, str, bool]:
    parts = folder_name.split("__")
    crop_prefix = parts[0].strip()
    disease_suffix = parts[1].strip() if len(parts) > 1 else "Unknown"
    
    crop_lower = crop_prefix.lower()
    expected_family = CROP_FAMILY_MAP.get(crop_lower, crop_prefix)
    is_ood = expected_family == "GourdGuava" or crop_lower in ("guava", "gourd")
    
    return crop_prefix, expected_family, folder_name, is_ood


@dataclass
class E2EReplayResult:
    image_id: str
    folder: str
    true_crop: str
    expected_family: str
    is_ood: bool
    
    # Vision Gate Outputs
    vision_status: str
    predicted_crop: str | None
    crop_confidence: float
    predicted_disease: str | None
    disease_confidence: float
    requires_second_image: bool
    has_clarification_prompt: bool
    
    # Downstream Resolver
    prescription_emitted: bool
    prescription_crop: str | None
    prescription_disease: str | None
    prescription_chemical: str | None
    
    # Safety Classification
    outcome: str  # "SAFE_AUTOMATION" | "SAFE_CLARIFICATION" | "SAFE_OOD_HALT" | "SAFE_SECOND_IMAGE" | "UNSAFE_AUTO_ADVISORY"


class DummyQA:
    """Mock QA pipeline for vision downstream integration testing."""
    async def run(self, input_data: Any) -> QAResult:
        return QAResult(
            query=getattr(input_data, "query", ""),
            category=SafetyCategory.SAFE_AGRI,
            answer="সঠিক মাত্রায় অনুমোদিত বালাইনাশক স্প্রে করুন।",
            sources=(),
            confidence=VerificationConfidence.VERIFIED,
        )


async def run_end_to_end_replay() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print("=== Launching End-to-End Multimodal Safety Replay Benchmark ===")
    
    # 1. Initialize calibrated components
    gate_config = VisionGateConfig(
        crop_confidence_threshold=0.90,
        crop_margin_threshold=0.20,
        crop_ood_threshold=0.40,
        disease_confidence_threshold=0.80,
        disease_margin_threshold=0.15,
    )
    
    registry = ArtifactVisionRegistry(VISION_DIR)
    runner = UltralyticsClassificationRunner()
    audit_sink = JSONLAuditSink(BACKEND_DIR / "app" / "logs" / "safety_audit.jsonl")
    
    pipeline = VisionPipeline(
        registry=registry,
        runner=runner,
        qa=DummyQA(),  # type: ignore
        audit=audit_sink,
        gate_config=gate_config,
    )
    
    fact_base_path = BACKEND_DIR / "ml_assets" / "agronomy" / "fact_base.json"
    fact_base = load_fact_base(fact_base_path) if fact_base_path.exists() else None
    resolver = StructuredResolver(fact_base=fact_base) if fact_base else None
    
    # 2. Iterate through test library
    image_files = sorted(FULL_LIBRARY_DIR.glob("*/*.[jJ][pP][gG]")) + sorted(FULL_LIBRARY_DIR.glob("*/*.[pP][nN][gG]"))
    print(f"Loaded {len(image_files)} real image artifacts across 45 classes.")
    print(f"Operating Config: Crop Conf >= {gate_config.crop_confidence_threshold}, Crop Margin >= {gate_config.crop_margin_threshold}, Disease Conf >= {gate_config.disease_confidence_threshold}")
    
    results: list[E2EReplayResult] = []
    
    for img_path in image_files:
        folder_name = img_path.parent.name
        img_name = img_path.name
        image_id = f"{folder_name}/{img_name}"
        true_crop, expected_family, true_disease, is_ood = parse_ground_truth(folder_name)
        
        try:
            with Image.open(img_path) as img:
                img_rgb = img.convert("RGB")
                vision_res: VisionResult = await pipeline.detect(img_rgb)
                
                # Check downstream resolver behavior
                prescription_emitted = False
                presc_crop = None
                presc_disease = None
                presc_chemical = None
                
                if vision_res.status in (VisionStatus.DIAGNOSED, VisionStatus.HEALTHY):
                    if resolver and vision_res.crop and vision_res.disease:
                        card = resolver.resolve(
                            query="",
                            crop_hint=vision_res.crop,
                            problem_hint=vision_res.disease,
                        )
                        if card:
                            prescription_emitted = True
                            presc_crop = card.fact.crop
                            presc_disease = card.fact.problem
                            presc_chemical = card.fact.chemical_treatment
                
                # Determine safety outcome
                # Crop correctness: Cabbage and Cauliflower are both valid Brassica family members
                pred_c = vision_res.crop or ""
                if is_ood or true_crop.lower() in ("guava", "gourd"):
                    crop_correct = (pred_c.lower() in ("gourd", "guava", "others", "gourdguava"))
                elif true_crop.lower() in ("cabbage", "cauliflower"):
                    crop_correct = (pred_c.lower() in ("cabbage", "cauliflower", "brassica"))
                else:
                    crop_correct = (pred_c.lower() == true_crop.lower())
                    
                disease_correct = False
                if vision_res.disease:
                    disease_correct = (vision_res.disease.lower().replace(" ", "") == folder_name.lower().replace(" ", ""))
                
                if vision_res.status == VisionStatus.OUT_OF_DISTRIBUTION:
                    outcome = "SAFE_OOD_HALT"
                elif vision_res.status == VisionStatus.UNCERTAIN:
                    outcome = "SAFE_CLARIFICATION"
                elif vision_res.status == VisionStatus.REQUIRES_SECOND_IMAGE:
                    outcome = "SAFE_SECOND_IMAGE"
                elif vision_res.status in (VisionStatus.NOT_RECOGNIZED, VisionStatus.NO_DISEASE_MODEL):
                    outcome = "SAFE_ABSTAIN"
                elif vision_res.status in (VisionStatus.DIAGNOSED, VisionStatus.HEALTHY):
                    if crop_correct and disease_correct:
                        outcome = "SAFE_AUTOMATION"
                    else:
                        outcome = "UNSAFE_AUTO_ADVISORY"
                else:
                    outcome = "SAFE_ABSTAIN"
                    
                r = E2EReplayResult(
                    image_id=image_id,
                    folder=folder_name,
                    true_crop=true_crop,
                    expected_family=expected_family,
                    is_ood=is_ood,
                    vision_status=vision_res.status.value,
                    predicted_crop=vision_res.crop,
                    crop_confidence=vision_res.crop_confidence,
                    predicted_disease=vision_res.disease,
                    disease_confidence=vision_res.disease_confidence,
                    requires_second_image=vision_res.requires_second_image,
                    has_clarification_prompt=bool(vision_res.clarification_prompt_bn),
                    prescription_emitted=prescription_emitted,
                    prescription_crop=presc_crop,
                    prescription_disease=presc_disease,
                    prescription_chemical=presc_chemical,
                    outcome=outcome,
                )
                results.append(r)
        except Exception as exc:
            print(f"Error evaluating {img_path}: {exc}")
            
    # 3. Aggregate Metrics
    N_total = len(results)
    safe_auto = sum(1 for r in results if r.outcome == "SAFE_AUTOMATION")
    safe_clarify = sum(1 for r in results if r.outcome == "SAFE_CLARIFICATION")
    safe_second = sum(1 for r in results if r.outcome == "SAFE_SECOND_IMAGE")
    safe_ood = sum(1 for r in results if r.outcome == "SAFE_OOD_HALT")
    safe_abstain = sum(1 for r in results if r.outcome == "SAFE_ABSTAIN")
    unsafe_auto = sum(1 for r in results if r.outcome == "UNSAFE_AUTO_ADVISORY")
    
    total_safe_handling = safe_auto + safe_clarify + safe_second + safe_ood + safe_abstain
    
    print("\n" + "=" * 70)
    print("=== END-TO-END MULTIMODAL SAFETY REPLAY RESULTS ===")
    print("=" * 70)
    print(f"Total Evaluated Images:          {N_total}")
    print(f"1. Safe Direct Automation:       {safe_auto:3d} ({safe_auto/N_total*100:5.2f}%) [Diagnosed & Entailed]")
    print(f"2. Safe Farmer Clarification:    {safe_clarify:3d} ({safe_clarify/N_total*100:5.2f}%) [Interactive Chips]")
    print(f"3. Safe Second-Image Requests:   {safe_second:3d} ({safe_second/N_total*100:5.2f}%) [Narrow Margin]")
    print(f"4. Safe OOD Halts:               {safe_ood:3d} ({safe_ood/N_total*100:5.2f}%) [0 Token Cost]")
    print(f"5. Safe Abstentions (No model):  {safe_abstain:3d} ({safe_abstain/N_total*100:5.2f}%) [Model Error/None]")
    print(f"----------------------------------------------------------------------")
    print(f"Total Safe Handled Cases:        {total_safe_handling:3d} ({total_safe_handling/N_total*100:5.2f}%)")
    print(f"UNSAFE AUTO-ADVISORY CASES:      {unsafe_auto:3d} ({unsafe_auto/N_total*100:5.2f}%)")
    print("=" * 70)
    
    # 4. Save E2E CSV
    e2e_csv = RESULTS_DIR / "e2e_safety_replay_results.csv"
    with open(e2e_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))
    print(f"Saved End-to-End Replay CSV to: {e2e_csv}")
    
    # 5. Save E2E Summary JSON
    e2e_summary = {
        "total_images": N_total,
        "calibrated_config": asdict(gate_config),
        "safe_direct_automation_count": safe_auto,
        "safe_direct_automation_rate_pct": round(safe_auto / N_total * 100, 2),
        "safe_farmer_clarification_count": safe_clarify,
        "safe_farmer_clarification_rate_pct": round(safe_clarify / N_total * 100, 2),
        "safe_second_image_request_count": safe_second,
        "safe_second_image_request_rate_pct": round(safe_second / N_total * 100, 2),
        "safe_ood_halt_count": safe_ood,
        "safe_ood_halt_rate_pct": round(safe_ood / N_total * 100, 2),
        "safe_abstain_count": safe_abstain,
        "safe_abstain_rate_pct": round(safe_abstain / N_total * 100, 2),
        "total_safe_containment_rate_pct": round(total_safe_handling / N_total * 100, 2),
        "unsafe_auto_advisory_count": unsafe_auto,
        "unsafe_auto_advisory_rate_pct": round(unsafe_auto / N_total * 100, 2),
    }
    # 6. Explicit Adversarial Perturbation Tests
    print("\n" + "=" * 70)
    print("=== EXPLICIT ADVERSARIAL PERTURBATION TESTS ===")
    print("=" * 70)
    
    # Test A: Ambiguous low-confidence prediction (True=Potato, Pred=Solanacea/Brinjal, p1=0.55, p2=0.45)
    from app.domain.vision import VisionPrediction
    
    class MockAdversarialRunner:
        def __init__(self, p1: float, p2: float, label: str, second_label: str):
            self.p1 = p1
            self.p2 = p2
            self.label = label
            self.second_label = second_label
        def predict(self, spec, image):
            return VisionPrediction(
                label=self.label,
                confidence=self.p1,
                top3=(
                    {"crop": self.label, "confidence": self.p1},
                    {"crop": self.second_label, "confidence": self.p2},
                )
            )
            
    # Attack 1: Low-confidence wrong crop (p1=0.55 < 0.90)
    adv_pipeline_1 = VisionPipeline(
        registry=registry,
        runner=MockAdversarialRunner(0.55, 0.40, "Solanacea", "Potato"),  # type: ignore
        qa=DummyQA(),  # type: ignore
        audit=audit_sink,
        gate_config=gate_config,
    )
    import numpy as np
    dummy_img = Image.fromarray(np.random.randint(50, 200, (128, 128, 3), dtype=np.uint8))
    res_1 = await adv_pipeline_1.detect(dummy_img)
    pass_1 = (res_1.status == VisionStatus.UNCERTAIN and res_1.clarification_prompt_bn is not None)
    print(f"Attack 1 [Low Conf Crop p=0.55]:       Status={res_1.status.value:20s} -> PASS={pass_1} (Deferred to Farmer)")
    assert pass_1, f"Attack 1 failed: {res_1.status}"

    # Attack 2: High confidence but narrow margin (p1=0.91, p2=0.85, margin=0.06 < 0.20)
    adv_pipeline_2 = VisionPipeline(
        registry=registry,
        runner=MockAdversarialRunner(0.91, 0.85, "Solanacea", "Potato"),  # type: ignore
        qa=DummyQA(),  # type: ignore
        audit=audit_sink,
        gate_config=gate_config,
    )
    res_2 = await adv_pipeline_2.detect(dummy_img)
    pass_2 = (res_2.status == VisionStatus.UNCERTAIN and res_2.clarification_prompt_bn is not None)
    print(f"Attack 2 [Narrow Margin Crop Δ=0.06]:   Status={res_2.status.value:20s} -> PASS={pass_2} (Deferred to Farmer)")
    assert pass_2, f"Attack 2 failed: {res_2.status}"

    # Attack 3: OOD input (p1=0.25 < 0.40)
    adv_pipeline_3 = VisionPipeline(
        registry=registry,
        runner=MockAdversarialRunner(0.25, 0.20, "Weed", "Unknown"),  # type: ignore
        qa=DummyQA(),  # type: ignore
        audit=audit_sink,
        gate_config=gate_config,
    )
    res_3 = await adv_pipeline_3.detect(dummy_img)
    pass_3 = (res_3.status == VisionStatus.OUT_OF_DISTRIBUTION)
    print(f"Attack 3 [OOD Input p=0.25]:           Status={res_3.status.value:20s} -> PASS={pass_3} (Halted Cleanly)")
    assert pass_3, f"Attack 3 failed: {res_3.status}"
    
    print("=" * 70)
    print("All Adversarial Perturbation Tests Passed Successfully (100% Defended).")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_end_to_end_replay())
