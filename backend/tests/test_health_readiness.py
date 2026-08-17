"""P0-1: /health + /readyz readiness endpoint tests.

Covers: liveness shape, per-check readiness payload (always 200 by default),
strict mode 503 on failed checks, degraded listing, and that readiness checks
are pure local probes (no network/model work — they return instantly).
"""

from __future__ import annotations

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def _degraded_settings(tmp_path: Path, *, strict: bool) -> Settings:
    """Settings whose ml_assets tree lacks the BM25 index but is otherwise a
    valid app (minimal vision tree so the registry builds, lazy model load)."""
    vision = tmp_path / "vision" / "crop_classifier"
    vision.mkdir(parents=True)
    (vision / "model.pt").write_bytes(b"")  # registry checks existence only
    (vision / "class_names.json").write_text("[]", encoding="utf-8")
    return Settings(ml_assets_dir=str(tmp_path), readiness_strict=strict)


class HealthReadinessTests(unittest.TestCase):
    def test_health_liveness(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "ok")
        self.assertIn("version", body)
        self.assertIn("x-request-id", response.headers)

    def test_readyz_ok_by_default_with_check_list(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/readyz")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("status", body)
        self.assertIn("ready", body)
        self.assertIn("version", body)
        self.assertIn("degraded", body)
        names = {check["name"] for check in body["checks"]}
        self.assertTrue(
            {"bm25_index", "rag_corpus", "dense_index", "sqlite_dir", "audit_dir"}
            <= names,
            f"expected core checks, got {names}",
        )
        for check in body["checks"]:
            self.assertIn("ok", check)
            self.assertIn("detail", check)

    def test_readyz_non_strict_always_200_even_when_degraded(self) -> None:
        """Default behavior is informational: a missing index must not break
        the response code — the demo stays reachable no matter what."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            config = _degraded_settings(Path(tmp), strict=False)
            with TestClient(create_app(config)) as client:
                response = client.get("/readyz")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "degraded")
        self.assertFalse(body["ready"])
        self.assertIn("bm25_index", body["degraded"])

    def test_readyz_strict_503_on_failed_checks(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            config = _degraded_settings(Path(tmp), strict=True)
            with TestClient(create_app(config)) as client:
                response = client.get("/readyz")
        self.assertEqual(response.status_code, 503)
        self.assertFalse(response.json()["ready"])

    def test_readyz_strict_200_when_healthy(self) -> None:
        config = Settings(readiness_strict=True)
        with TestClient(create_app(config)) as client:
            response = client.get("/readyz")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ready"])

    def test_readyz_is_fast_local_probe(self) -> None:
        """No network/model work: the endpoint completes without the container
        being built (build_container is only started by the lifespan)."""
        import time

        start = time.monotonic()
        with TestClient(create_app()) as client:
            response = client.get("/readyz")
        elapsed = time.monotonic() - start
        self.assertEqual(response.status_code, 200)
        self.assertLess(elapsed, 5.0)


if __name__ == "__main__":
    unittest.main()