"""T0-04: request-ID middleware + JSON structured logging tests.

Covers: valid header echoed, generated when absent, malformed/oversized/empty
headers regenerated, max-length header accepted, no leakage between requests,
log records emitted inside a request carry the request ID, and the formatter
emits exactly one JSON object per record (ts/level/logger/msg/request_id +
serializable extras).
"""

from __future__ import annotations

import json
import logging
import sys
import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.middleware.request_id import RequestIDMiddleware
from app.core.logging import JSONFormatter, request_id_var
from app.main import create_app

UUID4_HEX = r"^[0-9a-f]{32}$"


class _CaptureHandler(logging.Handler):
    """Collects pre-formatted JSON lines; format() runs in the emitter's
    context so the request-scoped request_id contextvar is visible."""

    def __init__(self) -> None:
        super().__init__()
        self.lines: list[str] = []
        self.setFormatter(JSONFormatter())

    def emit(self, record: logging.LogRecord) -> None:
        self.lines.append(self.format(record))


def _minimal_app() -> FastAPI:
    """Test-only app: middleware + a route that logs from inside the request."""
    app = FastAPI()
    app.add_middleware(RequestIDMiddleware, header_name="X-Request-ID")

    @app.get("/echo")
    async def echo() -> dict[str, str]:
        logging.getLogger("krishokchat").info("marker from request handler")
        return {"ok": "true"}

    return app


class RequestIDMiddlewareTests(unittest.TestCase):
    def test_valid_header_echoed(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/health", headers={"X-Request-ID": "abc-123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-request-id"], "abc-123")

    def test_missing_header_generates_and_echoes(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/health")
        self.assertRegex(response.headers["x-request-id"], UUID4_HEX)

    def test_malformed_header_regenerated(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/health", headers={"X-Request-ID": "bad id!!"})
        self.assertRegex(response.headers["x-request-id"], UUID4_HEX)

    def test_oversized_header_regenerated(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/health", headers={"X-Request-ID": "a" * 129})
        self.assertRegex(response.headers["x-request-id"], UUID4_HEX)

    def test_empty_header_regenerated(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/health", headers={"X-Request-ID": ""})
        self.assertRegex(response.headers["x-request-id"], UUID4_HEX)

    def test_max_length_valid_header_accepted(self) -> None:
        header = "a" * 128
        with TestClient(create_app()) as client:
            response = client.get("/health", headers={"X-Request-ID": header})
        self.assertEqual(response.headers["x-request-id"], header)

    def test_no_leakage_between_requests(self) -> None:
        """Contextvar is cleared after each response: the second request must
        not inherit the first request's ID."""
        with TestClient(create_app()) as client:
            first = client.get("/health", headers={"X-Request-ID": "abc-123"})
            second = client.get("/health")
        self.assertEqual(first.headers["x-request-id"], "abc-123")
        self.assertRegex(second.headers["x-request-id"], UUID4_HEX)
        self.assertNotEqual(second.headers["x-request-id"], "abc-123")

    def test_invalid_header_does_not_break_demo_routes(self) -> None:
        """Pure pass-through: a garbage header still yields a normal response."""
        with TestClient(create_app()) as client:
            response = client.post(
                "/api/qa",
                json={"query": "paraquat কীভাবে ব্যবহার করব"},
                headers={"X-Request-ID": "!!!garbage!!!"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["category"], "banned_or_restricted_chemical")


class StructuredLoggingTests(unittest.TestCase):
    def test_formatter_emits_single_json_object_with_extras(self) -> None:
        token = request_id_var.set("abc-123")
        try:
            record = logging.LogRecord(
                "krishokchat.qa", logging.INFO, __file__, 1, "hello %s", ("world",), None
            )
            record.extra_field = 42
            line = JSONFormatter().format(record)
        finally:
            request_id_var.reset(token)
        self.assertNotIn("\n", line)
        payload = json.loads(line)
        self.assertIn("ts", payload)
        self.assertEqual(payload["level"], "INFO")
        self.assertEqual(payload["logger"], "krishokchat.qa")
        self.assertEqual(payload["msg"], "hello world")
        self.assertEqual(payload["request_id"], "abc-123")
        self.assertEqual(payload["extra_field"], 42)

    def test_log_records_inside_request_carry_request_id(self) -> None:
        logger = logging.getLogger("krishokchat")
        logger.setLevel(logging.INFO)
        handler = _CaptureHandler()
        logger.addHandler(handler)
        try:
            with TestClient(_minimal_app()) as client:
                response = client.get("/echo", headers={"X-Request-ID": "req-42"})
            request_id = response.headers["x-request-id"]
        finally:
            logger.removeHandler(handler)
        self.assertEqual(request_id, "req-42")
        self.assertTrue(handler.lines, "expected at least one captured log line")
        for line in handler.lines:
            payload = json.loads(line)
            self.assertEqual(payload["request_id"], "req-42")
        self.assertEqual(payload["msg"], "marker from request handler")

    def test_exception_records_include_traceback(self) -> None:
        token = request_id_var.set("exc-1")
        try:
            try:
                raise ValueError("boom")
            except ValueError:
                record = logging.LogRecord(
                    "krishokchat.vision", logging.ERROR, __file__, 1,
                    "classify failed", (), sys.exc_info(),
                )
                line = JSONFormatter().format(record)
        finally:
            request_id_var.reset(token)
        payload = json.loads(line)
        self.assertEqual(payload["request_id"], "exc-1")
        self.assertIn("ValueError: boom", payload["traceback"])


if __name__ == "__main__":
    unittest.main()