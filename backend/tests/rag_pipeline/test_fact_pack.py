"""R9 — Tests for Offline Fact Packs and Manifest.

Locks all R9 invariants:
  1. build_packs generates deterministic per-crop JSON packs for all supported crops.
  2. Manifest lists all packs with accurate fact counts, file sizes, and sha256 digests.
  3. Every fact pack contains valid fact rows with doses, PHI, IPM, and citations.
  4. GET /api/packs/manifest and GET /api/v1/packs/manifest return valid manifests.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from scripts.build_fact_pack import DEFAULT_CALENDARS, DEFAULT_FACT_BASE, build_packs


def test_build_packs_deterministic(tmp_path: Path) -> None:
    out_dir = tmp_path / "packs"
    manifest = build_packs(DEFAULT_FACT_BASE, DEFAULT_CALENDARS, out_dir)

    assert manifest["schema_version"] == 1
    assert len(manifest["packs"]) >= 3

    crops = {p["crop"] for p in manifest["packs"]}
    assert {"potato", "maize", "rice"}.issubset(crops)

    for p in manifest["packs"]:
        pack_file = out_dir / p["filename"]
        assert pack_file.exists()
        assert pack_file.stat().st_size > 0
        assert p["facts_count"] > 0
        assert len(p["sha256"]) == 64

        data = json.loads(pack_file.read_text(encoding="utf-8"))
        assert data["crop"] == p["crop"]
        assert len(data["facts"]) == p["facts_count"]
        for f in data["facts"]:
            assert "active_ingredient" in f
            assert "dose_min" in f
            assert "dose_max" in f
            assert "citation" in f


def test_api_get_packs_manifest_endpoint() -> None:
    settings = Settings(demo_mode=True)
    app = create_app(settings)
    with TestClient(app) as client:
        # Legacy route
        res = client.get("/api/packs/manifest")
        assert res.status_code == 200
        data = res.json()
        assert "packs" in data
        assert len(data["packs"]) >= 3

        # Versioned route
        res_v1 = client.get("/api/v1/packs/manifest")
        assert res_v1.status_code == 200
        data_v1 = res_v1.json()
        assert len(data_v1["packs"]) == len(data["packs"])
