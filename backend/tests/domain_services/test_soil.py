from __future__ import annotations

import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from app.core.config import Settings
from app.main import create_app


def _isolated_app():
    # Test runs must never write audit entries into the live demo log.
    return create_app(Settings(audit_log_path=str(Path(tempfile.mkdtemp()) / "audit.jsonl")))


def _textured_image() -> Image.Image:
    """Noise + gradient image that passes the quality gate."""
    base = Image.new("RGB", (320, 320))
    px = base.load()
    for y in range(320):
        for x in range(320):
            px[x, y] = ((x * 37) % 256, (y * 29) % 256, ((x + y) * 17) % 256)
    return base


class SoilAPIContractTests(unittest.TestCase):
    def test_dataset_endpoint_returns_frozen_stats(self) -> None:
        with TestClient(_isolated_app()) as client:
            response = client.get("/api/soil/dataset")
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertTrue(body["available"])
            self.assertEqual(body["total_images"], 722)
            self.assertEqual(body["series_count"], 46)
            self.assertEqual(body["model_status"], "in_development")
            self.assertEqual(body["splits"], {"train": 472, "val": 119, "test": 131})
            # 6 soil types, each with usda + count.
            self.assertEqual(len(body["soil_types"]), 6)
            self.assertTrue(any(t["key"] == "Doash" and t["usda"] == "Loam" for t in body["soil_types"]))
            # Honest model table is present and every model has negative RÂ².
            self.assertGreaterEqual(len(body["model_results"]), 5)
            self.assertTrue(all(m["r2"] < 0 for m in body["model_results"]))
            # 12 stratified sample thumbnails.
            self.assertEqual(len(body["samples"]), 12)

    def test_analyze_is_locked_even_with_valid_image(self) -> None:
        with TestClient(_isolated_app()) as client:
            image_buffer = BytesIO()
            # A textured image (noise + gradient) passes the quality gate,
            # proving the lock is about the model, not the image.
            base = Image.new("RGB", (320, 320))
            px = base.load()
            for y in range(320):
                for x in range(320):
                    px[x, y] = ((x * 37) % 256, (y * 29) % 256, ((x + y) * 17) % 256)
            base.save(image_buffer, format="JPEG")
            response = client.post(
                "/api/soil/analyze",
                files={"file": ("soil.jpg", image_buffer.getvalue(), "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["status"], "locked")
            self.assertIsNotNone(body["error"])
            self.assertIsNotNone(body["dataset"])
            self.assertEqual(body["dataset"]["total_images"], 722)
            # No diagnosis fields may be set for a locked (unknown) image.
            self.assertIsNone(body["kpa"])
            self.assertIsNone(body["soil_type"])
            self.assertIsNone(body["sample_id"])

    def test_analyze_replays_known_sample_record(self) -> None:
        """A released sample ID replays its real measured record, verbatim."""
        with TestClient(_isolated_app()) as client:
            image_buffer = BytesIO()
            _textured_image().save(image_buffer, format="JPEG")
            response = client.post(
                "/api/soil/analyze",
                files={"file": ("P0406_Atel_16.5kpa.jpg", image_buffer.getvalue(), "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["status"], "analyzed")
            # Values must match samples_manifest.json exactly (no invention).
            self.assertEqual(body["sample_id"], "P0406")
            self.assertEqual(body["kpa"], 16.5)
            self.assertEqual(body["soil_type"], "Atel")
            self.assertEqual(body["soil_type_bn"], "এঁটেল মাটি")
            self.assertEqual(body["moisture_status"], "Dry")
            # Replay has no model confidence — it is a measurement, not a guess.
            self.assertIsNone(body["confidence"])
            # Honesty note must be part of the advisory.
            self.assertIn("পরিমাপিত", body["advisory_bn"])
            self.assertIn("মডেল নির্ণয় নয়", body["advisory_bn"])

    def test_analyze_unknown_id_stays_locked(self) -> None:
        """A P-shaped but unreleased ID must NOT fall back to any values."""
        with TestClient(_isolated_app()) as client:
            image_buffer = BytesIO()
            _textured_image().save(image_buffer, format="JPEG")
            response = client.post(
                "/api/soil/analyze",
                files={"file": ("P9999_Bele_3.3kpa.jpg", image_buffer.getvalue(), "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["status"], "locked")
            self.assertIsNone(body["sample_id"])
            self.assertIsNone(body["kpa"])

    def test_analyze_rejects_black_image_with_invalid_image_status(self) -> None:
        with TestClient(_isolated_app()) as client:
            image_buffer = BytesIO()
            Image.new("RGB", (320, 320), "black").save(image_buffer, format="JPEG")
            response = client.post(
                "/api/soil/analyze",
                files={"file": ("soil.jpg", image_buffer.getvalue(), "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["status"], "invalid_image")

    def test_analyze_rejects_non_image_file(self) -> None:
        with TestClient(_isolated_app()) as client:
            response = client.post(
                "/api/soil/analyze",
                files={"file": ("notes.txt", b"not an image", "text/plain")},
            )
            self.assertEqual(response.status_code, 400)

    def test_analyze_rejects_empty_file(self) -> None:
        with TestClient(_isolated_app()) as client:
            response = client.post(
                "/api/soil/analyze",
                files={"file": ("soil.jpg", b"", "image/jpeg")},
            )
            self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
