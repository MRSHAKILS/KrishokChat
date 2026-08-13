"""Soil dataset loader — reads the frozen release package from disk.

The release folder (dataset_release/soil_moisture/) is the single source of
truth. This loader never computes anything: it only parses precomputed JSON.
If the folder is missing, it returns an empty-but-valid info object so the app
starts and the API explains the absence instead of crashing.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from app.domain.soil import SoilDatasetInfo, SoilModelResult, SoilSample, SoilTypeStat

logger = logging.getLogger("krishokchat.soil")

SOIL_TYPE_USDA = {
    "Doash": "Loam",
    "Atel": "Clay",
    "Bele": "Sandy",
    "Poli": "Silt",
    "Bele_Doash": "Sandy Loam",
    "Atel_Doash": "Clay Loam",
}


def load_soil_dataset(release_dir: Path) -> SoilDatasetInfo:
    """Parse the frozen release package into a domain object."""
    if not release_dir.is_dir():
        logger.warning("soil release folder missing: %s", release_dir)
        return SoilDatasetInfo(total_images=0, kpa_range=(0.0, 0.0), available=False)

    summary: dict = _read_json(release_dir / "dataset_summary.json") or {}
    status: dict = _read_json(release_dir / "model_status.json") or {}
    samples_manifest: dict = _read_json(release_dir / "samples_manifest.json") or {}

    # Soil types — summary keys are "USDA (Key)" e.g. "Loam (Doash)".
    soil_counts: dict[str, int] = summary.get("soil_types", {}).get("with_usda_equivalents", {})
    soil_types = tuple(
        SoilTypeStat(
            key=name.split("(")[-1].rstrip(")").strip() if "(" in name else name,
            usda=name.split("(")[0].strip(),
            count=count,
        )
        for name, count in soil_counts.items()
    )

    kpa_range_raw = summary.get("kPa_range", "0.0 - 21.5")
    try:
        lo, hi = (float(part.strip()) for part in kpa_range_raw.split("-"))
    except (ValueError, TypeError):
        lo, hi = 0.0, 0.0

    collection = {
        "site": summary.get("collection_site", "Pabna District"),
        "dates": summary.get("collection_dates", "2026-05-29 to 2026-05-31"),
        "instrument": summary.get("instrument", "Field tensiometer (TraceData.xlsx)"),
    }

    samples = tuple(
        SoilSample(
            image_id=str(s.get("image_id", "")),
            filename=str(s.get("filename", "")),
            soil_type=str(s.get("soil_type", "")),
            kpa=float(s.get("kpa", 0.0)),
            land_type=str(s.get("land_type", "")),
            crop=str(s.get("crop", "")),
            growth_stage=str(s.get("growth_stage", "")),
        )
        for s in samples_manifest.get("samples", [])
    )

    model_results = tuple(
        SoilModelResult(model=str(m.get("model", "")), rmse_kpa=float(m.get("rmse_kpa", 0.0)), r2=float(m.get("r2", 0.0)))
        for m in status.get("models", [])
    )

    return SoilDatasetInfo(
        total_images=int(summary.get("total_images", 0)),
        kpa_range=(lo, hi),
        kpa_bins={str(k): int(v) for k, v in (summary.get("kPa_bins") or {}).items()},
        soil_types=soil_types,
        land_types={str(k): int(v) for k, v in (summary.get("land_types") or {}).items()},
        crops={str(k): int(v) for k, v in (summary.get("crops") or {}).items()},
        growth_stages={str(k): int(v) for k, v in (summary.get("growth_stages") or {}).items()},
        series_count=int(summary.get("series_count", 0)),
        splits={str(k): int(v) for k, v in (summary.get("split_counts") or {}).items()},
        metadata_matched=int(summary.get("metadata_matched", 0)),
        metadata_inferred=int(summary.get("metadata_inferred", 0)),
        corrections=int(summary.get("kPa_corrections_from_raw", 0)),
        collection=collection,
        model_status=str(status.get("status", "in_development")),
        model_results=model_results,
        samples=samples,
        available=True,
    )


def _read_json(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("soil dataset file unreadable %s: %s", path, exc)
        return None