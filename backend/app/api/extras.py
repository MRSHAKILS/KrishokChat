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
