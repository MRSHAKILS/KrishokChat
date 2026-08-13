"""Thin HTTP adapters for the soil moisture workflow (dataset + locked analyzer)."""

from __future__ import annotations

import io

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.api.dependencies import ContainerDep
from app.domain.soil import SoilDatasetInfo, SoilResult
from app.models.schemas import AgentStageEvent, SoilAnalyzeResponse, SoilDatasetResponse

router = APIRouter()


def _dataset_response(info: SoilDatasetInfo) -> SoilDatasetResponse:
    return SoilDatasetResponse(
        available=info.available,
        total_images=info.total_images,
        kpa_range=list(info.kpa_range),
        kpa_bins=info.kpa_bins,
        soil_types=[dict(t.__dict__) for t in info.soil_types],
        land_types=info.land_types,
        crops=info.crops,
        growth_stages=info.growth_stages,
        series_count=info.series_count,
        splits=info.splits,
        metadata_matched=info.metadata_matched,
        metadata_inferred=info.metadata_inferred,
        corrections=info.corrections,
        collection=info.collection,
        model_status=info.model_status,
        model_results=[dict(m.__dict__) for m in info.model_results],
        samples=[dict(s.__dict__) for s in info.samples],
    )


@router.get("/api/soil/dataset", response_model=SoilDatasetResponse)
async def soil_dataset(container: ContainerDep) -> SoilDatasetResponse:
    return _dataset_response(container.soil.dataset())


@router.post("/api/soil/analyze", response_model=SoilAnalyzeResponse)
async def soil_analyze(file: UploadFile = File(...), container: ContainerDep = None) -> SoilAnalyzeResponse:  # type: ignore[assignment]  # FastAPI injects via Annotated dependency
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Image file is empty")
    if len(data) > container.vision.max_image_bytes:
        raise HTTPException(status_code=413, detail=f"Image exceeds {container.vision.max_image_bytes} byte limit")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
        image = image.convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="Image could not be decoded") from exc

    result: SoilResult = container.soil.analyze(image)
    return SoilAnalyzeResponse(
        status=result.status.value,
        error=result.error,
        agent_trace=[
            AgentStageEvent(stage=event.stage.value, status=event.status, detail=event.detail)
            for event in result.trace
        ],
        dataset=(
            _dataset_response(result.info)
            if result.info is not None
            else SoilDatasetResponse(available=False, total_images=0, kpa_range=[0.0, 0.0])
        ),
    )