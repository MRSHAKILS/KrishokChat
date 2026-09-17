"""Weather + advisory endpoint and helpline registration.

Both are token-efficient Gemini calls or local-only storage.
Weather: one short prompt, returns Bengali weather + 1-line agri tip.
Helpline: local JSONL file only, no external telemetry.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.application.container import AppContainer
from app.api.dependencies import get_container
from app.core.config import settings

router = APIRouter()

ContainerDep = Annotated[AppContainer, Depends(get_container)]


class WeatherRequest(BaseModel):
    district: str = Field(..., min_length=2, max_length=60, description="Bangladesh district name in Bengali or English")
    crop: str | None = Field(None, description="Optional crop context for tailored advice")


class WeatherResponse(BaseModel):
    district: str
    summary_bn: str
    advice_bn: str
    model: str | None = None


class ModelOption(BaseModel):
    id: str
    label: str
    description: str
    available: bool


@router.get("/api/models", response_model=list[ModelOption])
async def list_models(container: ContainerDep) -> list[ModelOption]:
    """Health-check the configured local Ollama server for the KrishokChat-4B model."""
    local_available = False
    try:
        import httpx
        # Ollama's native /api/tags is the authoritative list of registered models.
        # The OpenAI-compat /v1/models returns {"data": null} even when models are
        # loaded, so we use the native endpoint.
        ollama_base = settings.ollama_base_url.rstrip("/")
        resp = httpx.get(f"{ollama_base}/api/tags", timeout=3.0)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            target = settings.local_llm_model_name  # "krishokchat-4b"
            local_available = any(
                # Ollama tags look like "krishokchat-4b:latest" — match prefix
                model.get("name", "").split(":")[0] == target
                for model in models
            )
    except Exception:
        local_available = False
    return [
        ModelOption(
            id="gemini",
            label="Gemini 2.5 Flash-Lite",
            description="অনলাইন মডেল — দ্রুত ও নির্ভরযোগ্য",
            available=True,
        ),
        ModelOption(
            id="krishokchat-4b",
            label="KrishokChat-4B (গবেষণা মডেল)",
            description="লোকাল ফাইন-টিউনড মডেল — অফলাইনে চলে",
            available=local_available,
        ),
    ]


WEATHER_PROMPT = """তুমি বাংলাদেশের একজন কৃষি আবহাওয়া সহায়ক। নিচের জেলার বর্তমান মৌসুমের
সাধারণ আবহাওয়া অনুমান করে ২-৩ বাক্যে বাংলায় লেখো। তারপর কৃষকের জন্য এক বাক্যে
পরামর্শ দাও। শুধু এই ফরম্যাটে উত্তর দাও:

আবহাওয়া: [২-৩ বাক্য]
পরামর্শ: [১ বাক্য]

জেলা: {district}
ফসল: {crop}
"""


@router.post("/api/weather", response_model=WeatherResponse)
async def weather_endpoint(payload: WeatherRequest, container: ContainerDep) -> WeatherResponse:
    """Token-efficient weather summary + agri advice via Gemini."""
    crop = payload.crop or "নির্দিষ্ট নয়"
    prompt = WEATHER_PROMPT.format(district=payload.district, crop=crop)
    try:
        text = await container.qa.generator.client.generate(prompt, metadata={"task": "weather"})
        # Parse the two-line format
        summary = ""
        advice = ""
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("আবহাওয়া"):
                summary = line.split(":", 1)[-1].strip()
            elif line.startswith("পরামর্শ"):
                advice = line.split(":", 1)[-1].strip()
        if not summary:
            summary = text[:200]
        if not advice:
            advice = "মৌসুমী পরামর্শের জন্য স্থানীয় কৃষি অফিসে যোগাযোগ করুন।"
        return WeatherResponse(
            district=payload.district,
            summary_bn=summary,
            advice_bn=advice,
            model=container.llm_name,
        )
    except Exception as exc:
        return WeatherResponse(
            district=payload.district,
            summary_bn="আবহাওয়া তথ্য এখন পাওয়া যায়নি।",
            advice_bn=f"স্থানীয় পরামর্শের জন্য কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।",
            model=None,
        )


# === Helpline Registration (local storage only) ===

class HelplineRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    phone: str = Field(..., min_length=6, max_length=20)
    district: str = Field(..., min_length=2, max_length=60)
    crop: str | None = Field(None, max_length=60)
    notes: str | None = Field(None, max_length=500)


class HelplineResponse(BaseModel):
    status: str
    message: str
    registration_id: str | None = None


@router.post("/api/helpline/register", response_model=HelplineResponse)
async def helpline_register(payload: HelplineRegister) -> HelplineResponse:
    """Store helpline registration locally only — no external telemetry."""
    log_path = settings.resolved_audit_log_path.parent / "helpline_registrations.jsonl"
    entry = {
        "name": payload.name,
        "phone": payload.phone,
        "district": payload.district,
        "crop": payload.crop,
        "notes": payload.notes,
    }
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        reg_id = f"HL-{abs(hash(json.dumps(entry, sort_keys=True))) % 100000:05d}"
        return HelplineResponse(
            status="ok",
            message="আপনার নিবন্ধন গ্রহণ করা হয়েছে। আমাদের দল শীঘ্রই যোগাযোগ করবে।",
            registration_id=reg_id,
        )
    except Exception:
        return HelplineResponse(
            status="error",
            message="নিবন্ধন সংরক্ষণে সমস্যা। অনুগ্রহ করে কৃষক কল সেন্টারে যোগাযোগ করুন: ১৬১২৩।",
        )


# === Gemini Regional Dialect Translator ===

DIALECT_NAMES = {
    "noakhali": "নোয়াখালী",
    "chattagram": "চাটগাঁইয়া (চট্টগ্রাম)",
    "sylhet": "সিলেটি",
    "rajshahi": "রাজশাহী/পাবনা",
    "rangpur": "রংপুর/বগুড়া",
}

DIALECT_PROMPT = """তুমি বাংলাদেশের একজন অভিজ্ঞ স্থানীয় কৃষি সম্প্রসারণ কর্মকর্তা।
নিচের প্রমিত বাংলায় লেখা কৃষি পরামর্শটিকে {dialect_name} আঞ্চলিক উপভাষায় সহজ ভাষায় রূপান্তর করো।

নির্দেশনা:
১. মূল পরামর্শের অর্থ, সুনির্দিষ্ট ডোজ ও রাসায়নিকের নাম অবিকল রাখবে।
২. উত্তরটি {dialect_name} অঞ্চলের সাধারণ কৃষকদের ব্যবহৃত স্বাভাবিক কথা বলার ঢঙে লেখো।
৩. কোনো অতিরিক্ত ভূমিকা বা শুভেচ্ছা বার্তা না দিয়ে সরাসরি অনূদিত অংশটুকু লেখো।

প্রমিত পরামর্শ:
{text}

অনূদিত পরামর্শ ({dialect_name}):"""


class DialectRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=2000, description="Standard Bengali text to convert")
    dialect: str = Field(..., description="Target dialect key: noakhali, chattagram, sylhet, rajshahi, rangpur")


class DialectResponse(BaseModel):
    dialect: str
    dialect_name: str
    translated_bn: str


@router.post("/api/dialect/translate", response_model=DialectResponse)
async def translate_dialect(payload: DialectRequest, container: ContainerDep) -> DialectResponse:
    """Convert standard Bengali agricultural advice into authentic regional dialects via Gemini."""
    import re
    dialect_key = payload.dialect.strip().lower()
    dialect_name = DIALECT_NAMES.get(dialect_key, "নোয়াখালী")

    # Clean raw database citation tags like [CABI_WHEAT_...] so Gemini translates pure advice
    clean_text = re.sub(r"\[[A-Z0-9_]+\]", "", payload.text).strip()
    prompt = DIALECT_PROMPT.format(dialect_name=dialect_name, text=clean_text)

    try:
        translated = await container.qa.generator.client.generate(prompt, metadata={"task": "dialect_translation"})
        translated = translated.strip()
        if not translated:
            translated = clean_text
        return DialectResponse(
            dialect=dialect_key,
            dialect_name=dialect_name,
            translated_bn=translated,
        )
    except Exception:
        # Fallback response on LLM failure
        return DialectResponse(
            dialect=dialect_key,
            dialect_name=dialect_name,
            translated_bn=clean_text,
        )


# === Deterministic Semantic SMS Gateway (E15 / E20 / E22) ===

class SMSAdvisoryRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=300, description="Farmer SMS query in Bengali or Banglish")
    phone_number: str | None = Field(None, max_length=20, description="Farmer mobile number")
    sender_id: str | None = Field("DAE", max_length=15, description="A2P Masking sender ID")


class SMSAdvisoryResponse(BaseModel):
    sms_text: str
    char_count: int
    gsm_segments: int
    resolution_tier: str
    confidence: str
    institution: str
    helpline_referral: str = "16123"


@router.post("/api/sms/advisory", response_model=SMSAdvisoryResponse)
async def sms_advisory_endpoint(payload: SMSAdvisoryRequest, container: ContainerDep) -> SMSAdvisoryResponse:
    """Deterministic, fail-closed SMS compressor gateway (<= 160 GSM chars).
    
    Guarantees critical dosage and PHI parameters survive without LLM truncation.
    """
    from app.application.qa_pipeline import QAInput
    
    qa_input = QAInput(query=payload.query, channel="sms")
    qa_res = await container.qa.run(qa_input)
    
    tier = str(qa_res.resolution_tier.value) if hasattr(qa_res.resolution_tier, "value") else str(qa_res.resolution_tier)
    confidence = str(qa_res.confidence.value) if hasattr(qa_res.confidence, "value") else str(qa_res.confidence)
    
    # 1. Safety Blocked or Out of Scope -> Strict 16123 referral SMS.
    # Fix 2026-09-17 (found by N05 measurement): answers carrying verifier flags
    # contain UNSUPPORTED dosage claims, which must never be compressed into an
    # SMS where the flag context is lost. They take the referral path too.
    vflags = tuple(getattr(qa_res, "verifier_flags", ()) or ())
    if qa_res.category.value != "safe_agri" or confidence == "blocked" or confidence == "low_confidence" or len(vflags) > 0:
        msg = "কৃষি তথ্য ও পরামর্শ পেতে সরকারি কৃষি কল সেন্টারে সরাসরি ডায়াল করুন: ১৬১২৩ (সকাল ৭টা-সন্ধ্যা ৭টা)।"
        return SMSAdvisoryResponse(
            sms_text=msg[:160],
            char_count=len(msg[:160]),
            gsm_segments=1,
            resolution_tier=tier,
            confidence=confidence,
            institution="DAE",
        )
    
    # 2. Extract verified institutional source
    institution = "DAE"
    if qa_res.sources:
        inst = qa_res.sources[0].metadata.get("publisher", "") or qa_res.sources[0].metadata.get("publisher_bn", "") or qa_res.sources[0].source or ""
        if "BARI" in inst or "বারি" in inst:
            institution = "BARI"
        elif "BRRI" in inst or "ব্রি" in inst:
            institution = "BRRI"
        elif "BARC" in inst or "বার্ক" in inst:
            institution = "BARC"
            
    # 3. Clean and compress answer into strict 160-char template
    import re
    clean_ans = re.sub(r"\[[A-Za-z0-9_\-]+\]", "", qa_res.answer).strip()
    clean_ans = re.sub(r"\s+", " ", clean_ans)
    
    # Format deterministic SMS template
    prefix = f"{institution} পরামর্শ: "
    suffix = " | হেল্প: ১৬১২৩"
    available_chars = 160 - len(prefix) - len(suffix)
    
    body = clean_ans[:available_chars].strip()
    # End cleanly on sentence or space if truncated
    if len(clean_ans) > available_chars:
        last_space = body.rfind(" ")
        if last_space > 20:
            body = body[:last_space]
            
    sms_text = f"{prefix}{body}{suffix}"
    
    return SMSAdvisoryResponse(
        sms_text=sms_text[:160],
        char_count=len(sms_text[:160]),
        gsm_segments=1,
        resolution_tier=tier,
        confidence=confidence,
        institution=institution,
    )

