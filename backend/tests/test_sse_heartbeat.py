"""P0-2: SSE keep-alive heartbeat tests.

The route must keep a long-silent pipeline connection alive by emitting
SSE comment lines (": keepalive"), and must NOT emit them on a normal fast
stream (the event protocol is unchanged for EventSource clients).
"""

from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import app.api.qa as qa_module
from app.api.dependencies import get_container
from app.core.config import Settings
from app.main import create_app


class _SilentPipelineQA:
    """Worst-case pipeline: produces no event for a long time (cold local
    model, slow provider). An async generator like the real QAPipeline.stream
    (the unreachable yield is what makes it one)."""

    async def stream(self, _input):  # noqa: N803
        while True:
            await asyncio.sleep(3600)
            yield  # pragma: no cover - unreachable


class _StubContainer:
    def __init__(self) -> None:
        self.qa = _SilentPipelineQA()


class SSEHeartbeatTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.mkdtemp()
        self._settings = Settings(audit_log_path=str(Path(tmp) / "audit.jsonl"))

    def test_keepalive_comment_during_silence(self) -> None:
        app = create_app(config=self._settings)
        app.dependency_overrides[get_container] = lambda: _StubContainer()
        qa_module.SSE_HEARTBEAT_SECONDS = 0.2  # fast heartbeat for the test
        try:
            with TestClient(app) as client:
                with client.stream(
                    "POST", "/api/qa/stream", json={"query": "ধান"}
                ) as response:
                    self.assertEqual(response.status_code, 200)
                    lines = list(response.iter_lines())
        finally:
            qa_module.SSE_HEARTBEAT_SECONDS = 15.0
        self.assertIn(": keepalive", lines, "expected an SSE keep-alive comment")

    def test_no_keepalive_on_fast_terminal_stream(self) -> None:
        """A normal fast stream (deterministic safety refusal) must not emit
        heartbeat comments — the protocol stays byte-identical."""
        with TestClient(create_app(config=self._settings)) as client:
            response = client.post(
                "/api/qa/stream",
                json={"query": "paraquat কীভাবে ব্যবহার করব"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(": keepalive", response.text)
        self.assertIn("banned_or_restricted_chemical", response.text)


if __name__ == "__main__":
    unittest.main()