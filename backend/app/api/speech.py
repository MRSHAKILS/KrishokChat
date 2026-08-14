"""P5 voice lane — read-aloud (TTS) and optional server-side transcription.

TTS: edge-tts (https://pypi.org/project/edge-tts/, version verified 7.2.8)
synthesizes MP3 through Microsoft Edge's Read Aloud service — free, no API
key, real Bengali bn-BD neural voices. The demo machine has no Bengali
system voice, so this endpoint is what makes the "শুনুন" button read real
Bengali instead of English-phoneme gibberish.

Design rules (Phase 1 of the P5 lane):
- Strictly additive: this router never touches the QA pipeline, safety
  policy, retrieval, or audit log.
- Failure contract: any TTS failure returns 503; the frontend falls back to
  the browser speechSynthesis, then to text-only. A broken voice lane must
  never degrade the typed chat.
- Answers are short (<2000 chars), so we synthesize per request and cache
  in memory. Canned refusal/helpline messages hit the cache on repeat reads.

ASR: /api/transcribe is an optional server-side fallback via Groq's Whisper
free tier (openai-compatible endpoint, https://console.groq.com/docs/rate-limits:
whisper-large-v3-turbo free tier 20 RPM / 2,000 RPD). Requires GROQ_API_KEY;
without the key it answers 501 and the browser Web Speech mic remains the
only voice input. Honest limit: standard Bengali only — regional dialects
are out of scope (Ben-10, AACL 2025).
"""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import io
import re
from collections import OrderedDict
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.api.dependencies import SettingsDep

router = APIRouter()

# Real Bengali (bn-BD) neural voices served by the Edge Read Aloud service.
# bn-BD-NabanitaNeural is the default (female); bn-BD-PradeepNeural (male)
# is available as an alternative. Anything else is rejected.
TTS_VOICES = ("bn-BD-NabanitaNeural", "bn-BD-PradeepNeural")
TTS_MAX_CHARS = 2000

# In-memory MP3 cache: key = sha256(voice|cleaned_text). OrderedDict so we
# can evict oldest-first when the cap is reached.
_cache: OrderedDict[str, bytes] = OrderedDict()


def _cache_get(key: str) -> bytes | None:
    value = _cache.get(key)
    if value is not None:
        _cache.move_to_end(key)
    return value


def _cache_put(key: str, value: bytes, max_entries: int) -> None:
    _cache[key] = value
    _cache.move_to_end(key)
    while len(_cache) > max_entries:
        _cache.popitem(last=False)


async def _synthesize_once(text: str, voice: str) -> bytes:
    """Single synthesis attempt via edge-tts.

    edge_tts is imported lazily so the app still boots (and the rest of the
    demo still works) even if the package is missing or the network is down.
    The defensive await handles both stream() APIs across edge-tts versions.
    """
    import edge_tts

    buffer = io.BytesIO()
    communicate = edge_tts.Communicate(text, voice)
    stream = communicate.stream()
    if inspect.isawaitable(stream):
        stream = await stream
    async for chunk in stream:
        if chunk["type"] == "audio":
            buffer.write(chunk["data"])
    data = buffer.getvalue()
    if not data:
        raise RuntimeError("edge-tts returned no audio")
    return data


async def _synthesize(text: str, voice: str) -> bytes:
    """Synthesize with bounded retries.

    The Edge Read Aloud service intermittently refuses audio (known upstream
    flakiness, edge-tts issue #460). A couple of short backoffs turn most
    transient refusals into successes; the endpoint-level timeout is the
    final guard. A failure here is a graceful 503 → browser fallback.
    """
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            return await _synthesize_once(text, voice)
        except Exception as exc:  # noqa: BLE001 — retry any transport/synthesis error
            last_error = exc
            if attempt < 2:
                await asyncio.sleep(1.0 * (attempt + 1))
    assert last_error is not None
    raise last_error


def _clean_text(raw: str) -> str:
    """Strip [SOURCE_ID] citation tags and collapse whitespace before reading."""
    return re.sub(r"\s+", " ", re.sub(r"\[[A-Za-z0-9_]+\]", "", raw)).strip()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=TTS_MAX_CHARS, description="Bengali text to read aloud")
    voice: str | None = Field(default=None, description="Voice id from the bn-BD allowlist")


@router.get("/api/tts/voices")
async def list_tts_voices(app_settings: SettingsDep) -> dict:
    """Allowlisted voices + the active default. Cheap probe for the UI and
    the demo script; no network synthesis is attempted."""
    return {
        "service": "edge-tts",
        "voices": list(TTS_VOICES),
        "default": app_settings.tts_default_voice,
    }


@router.post("/api/tts")
async def synthesize_speech(payload: TTSRequest, app_settings: SettingsDep) -> Response:
    """Synthesize MP3 for a short Bengali answer (read-aloud lane)."""
    voice = payload.voice or app_settings.tts_default_voice
    if voice not in TTS_VOICES:
        raise HTTPException(
            status_code=400,
            detail=f"voice must be one of: {', '.join(TTS_VOICES)}",
        )

    text = _clean_text(payload.text)
    if not text:
        raise HTTPException(status_code=400, detail="text is empty after citation cleanup")

    key = hashlib.sha256(f"{voice}|{text}".encode("utf-8")).hexdigest()
    cached = _cache_get(key)
    if cached is not None:
        return Response(content=cached, media_type="audio/mpeg", headers={"X-TTS-Cache": "hit"})

    try:
        audio = await asyncio.wait_for(
            _synthesize(text, voice),
            timeout=app_settings.tts_timeout_seconds,
        )
    except asyncio.TimeoutError as exc:
        raise HTTPException(status_code=503, detail="tts timeout") from exc
    except Exception as exc:  # noqa: BLE001 — any edge-tts failure is a graceful 503
        raise HTTPException(status_code=503, detail=f"tts unavailable: {type(exc).__name__}") from exc

    _cache_put(key, audio, app_settings.tts_cache_max_entries)
    return Response(content=audio, media_type="audio/mpeg", headers={"X-TTS-Cache": "miss"})


class TranscribeResponse(BaseModel):
    text: str
    service: str  # "groq-whisper"


class TTSWarmRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=10, description="Demo answers to synthesize ahead of time")
    voice: str | None = Field(default=None, description="Voice id from the bn-BD allowlist")


@router.post("/api/tts/prewarm")
async def prewarm_tts(payload: TTSWarmRequest, app_settings: SettingsDep) -> dict:
    """Synthesize the demo's exact answers into the cache before the live run.

    The Edge Read Aloud service rate-limits by time window (known flakiness,
    edge-tts issue #460): rapid requests get no audio. Prewarming the exact
    demo texts ~2-3 minutes before the demo — spaced 10s apart — turns every
    live "শুনুন" click into an instant cache hit, immune to the rate window.

    Failures are reported per text, never raised: a missed warm-up item only
    means that one answer pays the normal (retried) synthesis cost live.
    """
    voice = payload.voice or app_settings.tts_default_voice
    if voice not in TTS_VOICES:
        raise HTTPException(
            status_code=400,
            detail=f"voice must be one of: {', '.join(TTS_VOICES)}",
        )

    results: list[dict] = []
    for idx, raw in enumerate(payload.texts):
        text = _clean_text(raw)
        if not text:
            results.append({"index": idx, "ok": False, "error": "empty after cleanup"})
            continue

        key = hashlib.sha256(f"{voice}|{text}".encode("utf-8")).hexdigest()
        if _cache_get(key) is not None:
            results.append({"index": idx, "ok": True, "cached": True})
            continue

        try:
            audio = await asyncio.wait_for(
                _synthesize(text, voice),
                timeout=app_settings.tts_timeout_seconds,
            )
            _cache_put(key, audio, app_settings.tts_cache_max_entries)
            results.append({"index": idx, "ok": True, "cached": False})
        except Exception as exc:  # noqa: BLE001 — report, never raise
            results.append({"index": idx, "ok": False, "error": type(exc).__name__})

        # Respect the upstream rate window between syntheses.
        if idx < len(payload.texts) - 1:
            await asyncio.sleep(app_settings.tts_prewarm_spacing_seconds)

    return {"voice": voice, "results": results}


@router.post("/api/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    file: Annotated[UploadFile, File(...)],
    app_settings: SettingsDep,
) -> TranscribeResponse:
    """Server-side ASR fallback (Groq Whisper free tier).

    Requires GROQ_API_KEY in the environment. Without it the endpoint answers
    501 and the browser Web Speech mic (no key, Chrome/Edge) remains the
    primary voice input. The audio passes through this server to the Groq
    OpenAI-compatible endpoint; nothing is stored locally.
    """
    if not app_settings.groq_api_key:
        raise HTTPException(
            status_code=501,
            detail="server-side transcription is not configured (GROQ_API_KEY is empty)",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="empty audio file")
    if len(content) > 25 * 1024 * 1024:  # Groq free tier file cap
        raise HTTPException(status_code=413, detail="audio file too large (max 25 MB)")

    import httpx

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {app_settings.groq_api_key}"},
                data={
                    "model": app_settings.groq_whisper_model,
                    "language": "bn",
                    "temperature": "0",
                },
                files={
                    "file": (
                        file.filename or "voice.webm",
                        content,
                        file.content_type or "audio/webm",
                    )
                },
            )
        if resp.status_code != 200:
            raise RuntimeError(f"groq transcription failed: {resp.status_code}")
        text = (resp.json().get("text") or "").strip()
        if not text:
            raise RuntimeError("groq returned empty transcript")
        return TranscribeResponse(text=text, service="groq-whisper")
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001 — graceful 502 for any ASR failure
        raise HTTPException(status_code=502, detail=f"transcription unavailable: {type(exc).__name__}") from exc
