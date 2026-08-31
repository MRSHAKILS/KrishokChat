"""Thin HTTP adapters for the modular vision advisory workflow."""

from __future__ import annotations

import io

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.api.dependencies import ContainerDep
from app.domain.vision import VisionResult
from app.models.schemas import AgentStageEvent, ClassifyResponse, DetectResponse

router = APIRouter()


async def _read_image(file: UploadFile, *, max_bytes: int) -> Image.Image:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Image file is empty")
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail=f"Image exceeds {max_bytes} byte limit")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
        return image.convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="Image could not be decoded") from exc


def _trace(result: VisionResult) -> list[AgentStageEvent]:
    return [
        AgentStageEvent(stage=event.stage.value, status=event.status, detail=event.detail)
        for event in result.trace
    ]


def _top3(items: tuple[dict[str, str | float], ...]) -> list[dict]:
    return [dict(item) for item in items]


@router.post("/api/classify", response_model=ClassifyResponse)
async def classify_crop(file: UploadFile, container: ContainerDep) -> ClassifyResponse:
    image = await _read_image(file, max_bytes=container.vision.max_image_bytes)
    result = await container.vision.classify(image)
    return ClassifyResponse(
        crop=result.crop or "",
        confidence=result.crop_confidence,
        top3=_top3(result.top3_crops),
        has_disease_model=bool(result.crop and container.vision.registry.disease_candidates(result.crop)),
        status=result.status.value,
        clarification_prompt_bn=result.clarification_prompt_bn,
        suggested_crops=list(result.suggested_crops),
        quality_warnings=list(result.quality.warnings if result.quality else ()),
        agent_trace=_trace(result),
        error=result.error,
    )


@router.post("/api/detect", response_model=DetectResponse)
async def detect_disease(
    file: UploadFile = File(...),
    crop_hint: str | None = Form(default=None),
    container: ContainerDep = None,  # type: ignore[assignment]  # FastAPI injects via Annotated dependency
) -> DetectResponse:
    image = await _read_image(file, max_bytes=container.vision.max_image_bytes)
    result = await container.vision.detect(image, crop_hint=crop_hint)
    return DetectResponse(
        status=result.status.value,
        detection_mode="classification",
        crop=result.crop,
        crop_confidence=result.crop_confidence,
        crop_source=result.crop_source,
        disease=result.disease,
        disease_confidence=result.disease_confidence,
        boxes=[],
        disease_info=result.disease_info,
        top3_crops=_top3(result.top3_crops),
        top3_diseases=_top3(result.top3_diseases),
        treatment_advice=result.treatment_advice,
        treatment_confidence=result.treatment_confidence,
        treatment_sources=list(result.treatment_sources),
        verifier_flags=list(result.verifier_flags),
        clarification_prompt_bn=result.clarification_prompt_bn,
        suggested_crops=list(result.suggested_crops),
        requires_second_image=result.requires_second_image,
        agent_trace=_trace(result),
        quality_warnings=list(result.quality.warnings if result.quality else ()),
        error=result.error,
    )
