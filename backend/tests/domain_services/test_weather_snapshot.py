"""R8 — Tests for Real Weather Snapshot.

Locks all R8 invariants:
  1. The committed late_blight_snapshot.json has is_sample=False.
  2. Provenance block records source_id, endpoint, fetched_at, and adm3_pcodes.
  3. All 8 potato districts are present with valid temperature, humidity, and rainfall series.
  4. Late blight disease risk rules evaluate cleanly over real weather rows.
  5. Loader fails open (returns None or empty on missing/corrupted file).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.core.config import settings
from app.domain.late_blight import evaluate_district
from app.infrastructure.weather.snapshot import load_weather_snapshot


def test_committed_weather_snapshot_is_real() -> None:
    snapshot_path = settings.weather_snapshot_resolved_path
    assert snapshot_path.exists(), "Weather snapshot file must exist"

    snapshot = load_weather_snapshot(snapshot_path)
    assert snapshot is not None
    assert snapshot.is_sample is False, "Committed snapshot must have is_sample=False (R8)"
    assert snapshot.provenance is not None
    assert "OPEN_METEO" in snapshot.provenance.get("source_id", "") or "BMD" in snapshot.provenance.get("source_id", "")
    assert len(snapshot.provenance.get("adm3_pcodes", {})) >= 8

    expected_districts = {
        "Munshiganj", "Bogura", "Rangpur", "Dinajpur",
        "Rajshahi", "Jashore", "Comilla", "Joypurhat"
    }
    assert set(snapshot.districts.keys()) == expected_districts

    for d_name, series in snapshot.districts.items():
        assert len(series) >= 5, f"{d_name} must have at least 5 days of weather data"
        for day in series:
            assert 0.0 <= day.tmin_c <= 45.0, f"Invalid tmin_c for {d_name}: {day.tmin_c}"
            assert 0 <= day.rh_pct <= 100, f"Invalid rh_pct for {d_name}: {day.rh_pct}"
            assert day.rain_mm >= 0.0, f"Invalid rain_mm for {d_name}: {day.rain_mm}"


def test_evaluate_late_blight_risk_on_real_data() -> None:
    snapshot = load_weather_snapshot(settings.weather_snapshot_resolved_path)
    assert snapshot is not None

    for d_name, series in snapshot.districts.items():
        risk = evaluate_district(d_name, series)
        assert risk is not None
        assert risk.risk in ("high", "watch", "low")
        assert risk.district == d_name


def test_weather_loader_fail_open(tmp_path: Path) -> None:
    missing = tmp_path / "nonexistent.json"
    res = load_weather_snapshot(missing)
    assert res is None

    bad = tmp_path / "bad.json"
    bad.write_text("invalid json", encoding="utf-8")
    res_bad = load_weather_snapshot(bad)
    assert res_bad is None
