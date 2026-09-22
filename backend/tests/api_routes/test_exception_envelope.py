"""P0-3: last-resort exception envelope tests.

Any unhandled error must surface as a uniform 500 JSON body with the request
ID and no raw traceback, while the request-ID middleware keeps working.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.api.dependencies import get_container
from app.core.config import Settings
from app.main import create_app


class _BoomQA:
    """Pipeline stub that blows up the same way a real backend failure would
    (e.g. a storage exception inside an endpoint)."""

    async def run(self, _input):  # noqa: N803
        raise RuntimeError("boom: intentional test failure")

    async def stream(self, _input):  # noqa: N803
        yield  # pragma: no cover - never reached


class _BoomContainer:
    def __init__(self) -> None:
        self.qa = _BoomQA()


def _settings() -> Settings:
    tmp = tempfile.mkdtemp()
    return Settings(audit_log_path=str(Path(tmp) / "audit.jsonl"))


class ExceptionEnvelopeTests(unittest.TestCase):
    def _boom_client(self):
        app = create_app(config=_settings())
        app.dependency_overrides[get_container] = lambda: _BoomContainer()
        return TestClient(app, raise_server_exceptions=False)

    def test_unhandled_error_becomes_500_envelope(self) -> None:
        with self._boom_client() as client:
            response = client.post("/api/qa", json={"query": "ধান"})
        self.assertEqual(response.status_code, 500)
        body = response.json()
        self.assertEqual(body["error"], "internal_error")
        self.assertIn("request_id", body)
        self.assertIn("detail", body)

    def test_no_traceback_in_body(self) -> None:
        with self._boom_client() as client:
            response = client.post("/api/qa", json={"query": "ধান"})
        self.assertNotIn("boom", response.text)
        self.assertNotIn("Traceback", response.text)

    def test_request_id_echoed_into_envelope(self) -> None:
        with self._boom_client() as client:
            response = client.post(
                "/api/qa",
                json={"query": "ধান"},
                headers={"X-Request-ID": "test-req-42"},
            )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["request_id"], "test-req-42")
        self.assertEqual(response.headers["X-Request-ID"], "test-req-42")

    def test_generated_request_id_when_absent(self) -> None:
        with self._boom_client() as client:
            response = client.post("/api/qa", json={"query": "ধান"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["request_id"],
            response.headers["X-Request-ID"],
            "envelope ID must match the ID the middleware echoed",
        )

    def test_http_errors_keep_their_own_status(self) -> None:
        """The broad handler must not hijack normal HTTP errors (404/405)."""
        with TestClient(create_app(config=_settings())) as client:
            missing = client.get("/api/definitely-not-a-route")
            wrong_method = client.post("/api/benchmark")
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(wrong_method.status_code, 405)


if __name__ == "__main__":
    unittest.main()