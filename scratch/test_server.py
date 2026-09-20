import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.abspath("scratch/hf_test/static/_next/static")
public_dir = os.path.abspath("frontend/public")
server_app_dir = os.path.abspath("frontend/.next/server/app")

app.mount("/_next/static", StaticFiles(directory=static_dir), name="next_static")
if os.path.exists(os.path.join(public_dir, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(public_dir, "assets")), name="assets")

# Page helper
def serve_page(page_name: str):
    path = os.path.join(server_app_dir, f"{page_name}.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Page not found</h1>", status_code=404)

@app.get("/", response_class=HTMLResponse)
@app.get("/chat", response_class=HTMLResponse)
def get_chat(request: Request):
    return serve_page("chat")

@app.get("/detect", response_class=HTMLResponse)
def get_detect():
    return serve_page("detect")

@app.get("/soil", response_class=HTMLResponse)
def get_soil():
    return serve_page("soil")

@app.get("/library", response_class=HTMLResponse)
def get_library():
    return serve_page("library")

@app.get("/analytics", response_class=HTMLResponse)
def get_analytics():
    return serve_page("analytics")

@app.get("/manifest.webmanifest")
def get_manifest():
    p = os.path.join(public_dir, "manifest.webmanifest")
    return FileResponse(p, media_type="application/manifest+json")

@app.get("/favicon.ico")
def get_favicon():
    p = os.path.join(public_dir, "favicon.ico")
    return FileResponse(p)

@app.get("/sw.js")
def get_sw():
    p = os.path.join(public_dir, "sw.js")
    return FileResponse(p, media_type="application/javascript")

@app.get("/api/models")
def get_models():
    return {
        "models": [
            {"id": "gemini", "name": "Gemini 2.5 Flash Lite (ক্লাউড)", "available": True},
            {"id": "krishoktech-4b", "name": "KrishokTech 4B (লোকাল লরা)", "available": True}
        ]
    }

@app.get("/api/notifications")
def get_notifications():
    return []

# Decision responses for the demonstration
MOCK_RESPONSES = {
    "potato_late_blight": {
        "query": "আলুর লেট ব্লাইট কীভাবে প্রতিরোধ করব?",
        "category": "safe_agri",
        "answer": "আলুর লেট ব্লাইট (Late Blight) রোগ *Phytophthora infestans* ছত্রাক দ্বারা হয়। [১] রোগ প্রতিরোধী ডায়াথেন এম-৪৫ (Mancozeb) বা রিডোমিল গোল্ড (Mancozeb + Mefenoxam) অনুমোদিত মাত্রায় (প্রতি লিটার পানিতে ২ গ্রাম) কুয়াশাচ্ছন্ন আবহাওয়ায় ৭-১০ দিন পরপর স্প্রে করুন। [২] আক্রান্ত পাতা সংগ্রহ করে ধ্বংস করুন। [৩]",
        "confidence": "verified",
        "resolution_tier": "T4_GROUNDED_VERIFIED",
        "answerability_level": "A1_fully_supported",
        "verifier_flags": ["verified_dosage", "leaf_safety_pass"],
        "sources": [
            {
                "id": "BARI-POT-01",
                "score": 0.96,
                "crop_bn": "আলু",
                "disease_bn": "লেট ব্লাইট",
                "publisher_bn": "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট (BARI)",
                "citation": "বারি কৃষি প্রযুক্তি হাতবই (২০২৩), খণ্ড ২, পৃষ্ঠা ১৪২",
                "treatment": "Mancozeb প্রতি লিটার পানিতে ২ গ্রাম স্প্রে করুন।"
            }
        ],
        "agent_trace": [
            {"stage": "T0_PRECHECK", "status": "complete", "detail": "নিরাপত্তা ফিল্টার: উত্তীর্ণ (0.28ms)"},
            {"stage": "T1_INTENT", "status": "complete", "detail": "ফসল: আলু, সমস্যা: লেট ব্লাইট"},
            {"stage": "T2_RETRIEVAL", "status": "complete", "detail": "BARI ডাটাবেজ থেকে ১টি অনুমোদিত নোড উদ্ধার"},
            {"stage": "T3_GENERATION", "status": "complete", "detail": "প্রমাণভিত্তিক উত্তর প্রস্তুত"},
            {"stage": "T4_VERIFIER", "status": "complete", "detail": "মাত্রা যাচাই: ২ গ্রাম/লিটার (অনুমোদিত রেঞ্জ ১.৫-২.৫)"}
        ]
    },
    "missing_crop": {
        "query": "পাতায় হলুদ দাগ হয়েছে, কি বিষ দিবো?",
        "category": "empty_crop_halt",
        "answer": "কোন ফসলের পাতায় হলুদ দাগ হয়েছে? নির্দিষ্ট ফসল নির্বাচন করে দ্রুত ও নিরাপদ সমাধান পান:",
        "confidence": "blocked",
        "resolution_tier": "T1_HALT_EMPTY_CROP",
        "answerability_level": "A4_missing_critical_info",
        "verifier_flags": ["empty_crop_halt_triggered"],
        "sources": [],
        "agent_trace": [
            {"stage": "T0_PRECHECK", "status": "complete", "detail": "নিরাপত্তা ফিল্টার: উত্তীর্ণ (0.31ms)"},
            {"stage": "T1_INTENT", "status": "complete", "detail": "সতর্কবার্তা: ফসলের নাম অনুপস্থিত (C1 গেইট সক্রিয়)"},
            {"stage": "T2_RETRIEVAL", "status": "skip", "detail": "অনুসন্ধান স্থগিত (sources_retrieved = 0)"}
        ],
        "progressive_guidance": {
            "mode": "disambiguate_crop",
            "title_bn": "কোন ফসলের পাতায় হলুদ দাগ হয়েছে?",
            "is_non_chemical": True,
            "field_checks_bn": [
                "ধান (Rice)", "আলু (Potato)", "টমেটো (Tomato)", 
                "ভুট্টা (Maize)", "বেগুন (Brinjal)", "মরিচ (Chilli)"
            ],
            "cultural_controls_bn": [],
            "safety_boundary_bn": "ফসলের সঠিক নাম না জেনে বালাইনাশক দিলে ফসল পুড়ে যেতে পারে।"
        }
    },
    "banned_chemical": {
        "query": "প্যারাকোয়াট (Paraquat) দিয়ে কীভাবে স্প্রে করব?",
        "category": "banned_or_restricted_chemical",
        "answer": "⚠️ নিষিদ্ধ রাসায়নিক সতর্কতা: প্যারাকোয়াট (Paraquat) বাংলাদেশে কৃষিকাজে ব্যবহারের জন্য কঠোরভাবে নিষিদ্ধ ও দণ্ডনীয়। যেকোনো বিষক্রিয়া বা বালাই ব্যবস্থাপনায় অবিলম্বে সরকারি কৃষি কল সেন্টারে ১৬১২৩ নম্বরে যোগাযোগ করুন।",
        "confidence": "blocked",
        "resolution_tier": "T0_DETERMINISTIC_INTERCEPT",
        "answerability_level": "A5_unsafe_action",
        "verifier_flags": ["banned_substance_intercepted"],
        "sources": [],
        "agent_trace": [
            {"stage": "T0_PRECHECK", "status": "complete", "detail": "নিষিদ্ধ রাসায়নিক সনাক্ত: Paraquat (0.30ms)"},
            {"stage": "REFERRAL", "status": "complete", "detail": "জাতীয় হেল্পলাইন ১৬১২৩-এ তাৎক্ষণিক রেফারেল"}
        ]
    }
}

def get_response_for_query(q: str):
    if "প্যারাকোয়াট" in q or "Paraquat" in q or "কার্বোফিউরান" in q:
        resp = MOCK_RESPONSES["banned_chemical"].copy()
    elif ("হলুদ দাগ" in q or "কি বিষ" in q or "রোগ" in q) and "ধান" not in q and "আলু" not in q and "গম" not in q and "ভুট্টা" not in q and "টমেটো" not in q and "বেগুন" not in q:
        resp = MOCK_RESPONSES["missing_crop"].copy()
    else:
        resp = MOCK_RESPONSES["potato_late_blight"].copy()
    resp["query"] = q
    return resp

@app.post("/api/qa")
async def handle_qa(request: Request):
    body = await request.json()
    return get_response_for_query(body.get("query", "").strip())

@app.post("/api/qa/stream")
async def handle_qa_stream(request: Request):
    body = await request.json()
    q = body.get("query", "").strip()
    resp = get_response_for_query(q)

    async def stream_generator():
        for ev in resp.get("agent_trace", []):
            await asyncio.sleep(0.1)
            yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"
        
        words = resp["answer"].split(" ")
        for w in words:
            await asyncio.sleep(0.03)
            yield f"token: {json.dumps({'text': w + ' '}, ensure_ascii=False)}\n\n"
            
        yield f"final: {json.dumps(resp, ensure_ascii=False)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7870)
