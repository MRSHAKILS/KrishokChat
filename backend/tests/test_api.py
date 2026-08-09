from __future__ import annotations

import unittest
from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import create_app


class APIContractTests(unittest.TestCase):
    def test_health_and_terminal_qa_contract(self) -> None:
        with TestClient(create_app()) as client:
            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json()["status"], "ok")

            response = client.post("/api/qa", json={"query": "paraquat কীভাবে ব্যবহার করব"})
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["category"], "banned_or_restricted_chemical")
            self.assertEqual(body["confidence"], "blocked")
            self.assertEqual(len(body["sources"]), 0)

            image_buffer = BytesIO()
            Image.new("RGB", (128, 128), "black").save(image_buffer, format="PNG")
            vision = client.post(
                "/api/detect",
                files={"file": ("black.png", image_buffer.getvalue(), "image/png")},
            )
            self.assertEqual(vision.status_code, 200)
            self.assertEqual(vision.json()["status"], "invalid_image")
            self.assertEqual(vision.json()["detection_mode"], "classification")


if __name__ == "__main__":
    unittest.main()
