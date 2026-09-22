"""Speech endpoint tests (P5 voice lane).

All synthesis is mocked — these tests must never hit the network. They pin
the failure contract: unknown voices/empty text → 4xx, edge-tts failures →
503, cache hit behavior, and the Groq transcribe gate (501 without key).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.api import speech as speech_module
from app.core.config import Settings
from app.main import create_app

FAKE_MP3 = b"\xff\xf3fake-mp3-bytes"


class SpeechEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        # Module-level cache persists across tests in one process; clear it so
        # each test sees a cold cache.
        speech_module._cache.clear()

    def _client(self, settings: Settings | None = None):
        if settings is None:
            settings = Settings()
        return TestClient(create_app(config=settings))

    def _tmp_settings(self, **overrides) -> Settings:
        return Settings(
            audit_log_path=str(Path(tempfile.mkdtemp()) / "audit.jsonl"),
            **overrides,
        )

    # ---- TTS: voices contract -------------------------------------------

    def test_tts_voices_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(audit_log_path=str(Path(tmp) / "audit.jsonl"))
            with self._client(settings) as client:
                resp = client.get("/api/tts/voices")
                self.assertEqual(resp.status_code, 200)
                body = resp.json()
                self.assertEqual(body["service"], "edge-tts")
                self.assertIn("bn-BD-NabanitaNeural", body["voices"])
                self.assertIn("bn-BD-PradeepNeural", body["voices"])
                self.assertEqual(body["default"], "bn-BD-NabanitaNeural")

    def test_tts_rejects_unknown_voice(self) -> None:
        with self._client(self._tmp_settings()) as client:
            resp = client.post("/api/tts", json={"text": "নমস্কার", "voice": "en-US-JennyNeural"})
            self.assertEqual(resp.status_code, 400)

    def test_tts_rejects_oversized_text(self) -> None:
        with self._client(self._tmp_settings()) as client:
            resp = client.post("/api/tts", json={"text": "ক" * 2001})
            self.assertEqual(resp.status_code, 422)

    # ---- TTS: synthesis + cache ----------------------------------------

    def test_tts_synthesizes_and_caches(self) -> None:
        calls = {"n": 0}

        async def fake_synthesize(text: str, voice: str) -> bytes:  # noqa: ARG001
            calls["n"] += 1
            return FAKE_MP3

        with patch.object(speech_module, "_synthesize", side_effect=fake_synthesize), \
                tempfile.TemporaryDirectory() as tmp:
            settings = Settings(audit_log_path=str(Path(tmp) / "audit.jsonl"))
            with self._client(settings) as client:
                r1 = client.post("/api/tts", json={"text": "ধান গাছের যত্ন নিন"})
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r1.headers["content-type"], "audio/mpeg")
                self.assertEqual(r1.headers["x-tts-cache"], "miss")
                self.assertEqual(r1.content, FAKE_MP3)

                r2 = client.post("/api/tts", json={"text": "ধান গাছের যত্ন নিন"})
                self.assertEqual(r2.status_code, 200)
                self.assertEqual(r2.headers["x-tts-cache"], "hit")
                self.assertEqual(r2.content, FAKE_MP3)
                self.assertEqual(calls["n"], 1, "cache must serve the second identical request")

    def test_tts_strips_citation_tags_before_synthesis(self) -> None:
        captured: dict[str, str] = {}

        async def fake_synthesize(text: str, voice: str) -> bytes:  # noqa: ARG001
            captured["text"] = text
            return FAKE_MP3

        with patch.object(speech_module, "_synthesize", side_effect=fake_synthesize), \
                tempfile.TemporaryDirectory() as tmp:
            settings = Settings(audit_log_path=str(Path(tmp) / "audit.jsonl"))
            with self._client(settings) as client:
                resp = client.post("/api/tts", json={"text": "আমন ধান [CABI_RICE_1] সার দিন"})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(captured["text"], "আমন ধান সার দিন")

    def test_tts_failure_returns_503(self) -> None:
        async def boom(text: str, voice: str) -> bytes:  # noqa: ARG001
            raise RuntimeError("edge down")

        with patch.object(speech_module, "_synthesize", side_effect=boom), \
                tempfile.TemporaryDirectory() as tmp:
            settings = Settings(audit_log_path=str(Path(tmp) / "audit.jsonl"))
            with self._client(settings) as client:
                resp = client.post("/api/tts", json={"text": "ধান"})
                self.assertEqual(resp.status_code, 503)
                self.assertIn("tts unavailable", resp.json()["detail"])

    def test_synthesize_retries_then_succeeds(self) -> None:
        """Transient upstream refusals (edge-tts #460-style) are retried."""
        import asyncio

        attempts = {"n": 0}

        async def flaky(text: str, voice: str) -> bytes:  # noqa: ARG001
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise RuntimeError("no audio received")
            return FAKE_MP3

        async def run() -> bytes:
            with patch.object(speech_module, "_synthesize_once", side_effect=flaky):
                return await speech_module._synthesize("ধান", "bn-BD-NabanitaNeural")

        data = asyncio.run(run())
        self.assertEqual(data, FAKE_MP3)
        self.assertEqual(attempts["n"], 3, "must retry transient failures")

    def test_synthesize_gives_up_after_three_attempts(self) -> None:
        import asyncio

        attempts = {"n": 0}

        async def always_fails(text: str, voice: str) -> bytes:  # noqa: ARG001
            attempts["n"] += 1
            raise RuntimeError("no audio received")

        async def run() -> bytes:
            with patch.object(speech_module, "_synthesize_once", side_effect=always_fails):
                return await speech_module._synthesize("ধান", "bn-BD-NabanitaNeural")

        with self.assertRaises(RuntimeError):
            asyncio.run(run())
        self.assertEqual(attempts["n"], 3)

    # ---- Prewarm --------------------------------------------------------

    def test_prewarm_caches_each_text_and_reports_failures(self) -> None:
        """Prewarm fills the cache and reports per-text results, never raising."""
        calls = {"n": 0}

        async def fake_synthesize(text: str, voice: str) -> bytes:  # noqa: ARG001
            calls["n"] += 1
            if text == "বিস্ফোরক":  # simulate one upstream refusal
                raise RuntimeError("no audio received")
            return FAKE_MP3

        with patch.object(speech_module, "_synthesize", side_effect=fake_synthesize), \
                tempfile.TemporaryDirectory() as tmp:
            settings = Settings(
                audit_log_path=str(Path(tmp) / "audit.jsonl"),
                tts_prewarm_spacing_seconds=0.0,
            )
            with self._client(settings) as client:
                resp = client.post(
                    "/api/tts/prewarm",
                    json={"texts": ["ধান গাছের যত্ন নিন", "বিস্ফোরক", "ধান গাছের যত্ন নিন"]},
                )
                self.assertEqual(resp.status_code, 200)
                results = resp.json()["results"]
                self.assertEqual(len(results), 3)
                self.assertTrue(results[0]["ok"])
                self.assertFalse(results[1]["ok"])
                # Third text was already cached by the first item.
                self.assertTrue(results[2]["ok"])
                self.assertTrue(results[2]["cached"])
                self.assertEqual(calls["n"], 2, "duplicate text must not be synthesized twice")

    def test_prewarm_rejects_unknown_voice_and_too_many_texts(self) -> None:
        with self._client(self._tmp_settings()) as client:
            bad_voice = client.post(
                "/api/tts/prewarm",
                json={"texts": ["ধান"], "voice": "en-US-JennyNeural"},
            )
            self.assertEqual(bad_voice.status_code, 400)
            too_many = client.post(
                "/api/tts/prewarm",
                json={"texts": [f"প্রশ্ন {i}" for i in range(11)]},
            )
            self.assertEqual(too_many.status_code, 422)

    def test_tts_empty_after_cleanup_returns_400(self) -> None:
        with self._client(self._tmp_settings()) as client:
            resp = client.post("/api/tts", json={"text": "[CABI_RICE_1]"})
            self.assertEqual(resp.status_code, 400)

    # ---- ASR: Groq gate ------------------------------------------------

    def test_transcribe_501_without_key(self) -> None:
        with self._client(self._tmp_settings(groq_api_key=None)) as client:
            resp = client.post(
                "/api/transcribe",
                files={"file": ("voice.webm", b"fake-webm-bytes", "audio/webm")},
            )
            self.assertEqual(resp.status_code, 501)
            self.assertIn("GROQ_API_KEY", resp.json()["detail"])

    def test_transcribe_413_oversized(self) -> None:
        with self._client(self._tmp_settings(groq_api_key="dummy")) as client:
            resp = client.post(
                "/api/transcribe",
                files={"file": ("voice.webm", b"x" * (25 * 1024 * 1024 + 1), "audio/webm")},
            )
            self.assertEqual(resp.status_code, 413)

    def test_transcribe_success_with_key(self) -> None:
        async def fake_post(*args, **kwargs):  # noqa: ARG001
            return SimpleNamespace(status_code=200, json=lambda: {"text": "ধান গাছে পানি দেব?"})

        with patch("httpx.AsyncClient") as mock_cls, \
                tempfile.TemporaryDirectory() as tmp:
            mock_client = mock_cls.return_value.__aenter__.return_value
            mock_client.post = AsyncMock(side_effect=fake_post)
            settings = Settings(
                audit_log_path=str(Path(tmp) / "audit.jsonl"),
                groq_api_key="dummy-key",
            )
            with self._client(settings) as client:
                resp = client.post(
                    "/api/transcribe",
                    files={"file": ("voice.webm", b"fake-webm-bytes", "audio/webm")},
                )
                self.assertEqual(resp.status_code, 200)
                body = resp.json()
                self.assertEqual(body["text"], "ধান গাছে পানি দেব?")
                self.assertEqual(body["service"], "groq-whisper")

    def test_transcribe_upstream_failure_returns_502(self) -> None:
        async def fake_post(*args, **kwargs):  # noqa: ARG001
            return SimpleNamespace(status_code=401, json=lambda: {"error": "bad key"})

        with patch("httpx.AsyncClient") as mock_cls, \
                tempfile.TemporaryDirectory() as tmp:
            mock_client = mock_cls.return_value.__aenter__.return_value
            mock_client.post = AsyncMock(side_effect=fake_post)
            settings = Settings(
                audit_log_path=str(Path(tmp) / "audit.jsonl"),
                groq_api_key="dummy-key",
            )
            with self._client(settings) as client:
                resp = client.post(
                    "/api/transcribe",
                    files={"file": ("voice.webm", b"fake-webm-bytes", "audio/webm")},
                )
                self.assertEqual(resp.status_code, 502)


if __name__ == "__main__":
    unittest.main()
