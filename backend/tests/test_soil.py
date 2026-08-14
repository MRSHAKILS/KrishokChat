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
