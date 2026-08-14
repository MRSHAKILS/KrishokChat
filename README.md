# KrishokChat Advisory System

A safety-aware, retrieval-grounded, Bengali agricultural advisory system for smallholder
farmers in Bangladesh. The system answers farming questions in Bengali through a
four-stage agent pipeline (safety screening, retrieval, grounded generation,
verification) and diagnoses crop diseases from photos using a crop-classifier +
per-crop vision model workflow. It is a research capstone demo prototype, not a
production service.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Repository Layout](#repository-layout)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Data & Models](#data--models)
- [Frontend Routes](#frontend-routes)
- [Testing & Verification](#testing--verification)
- [Known Limitations](#known-limitations)
- [Documentation](#documentation)
- [Status & License](#status--license)

---

## Overview

KrishokChat combines three already-trained research artifacts into one demo system:

1. **Bengali agri Q&A assistant** — hybrid retrieval (BM25 sparse + FAISS dense)
   over a precomputed corpus of 2,120 knowledge nodes, feeding a fine-tuned LLM
   with grounded, source-cited answers.
2. **Crop disease advisory workflow** — a crop classifier routes an uploaded photo to
   a crop-specific disease model, which returns a Bengali diagnosis and treatment
   advice.
3. **Safety-aware agentic pipeline** — every query is classified before retrieval.
   Unsafe queries are stopped with a canned redirect to the government Krishi Call
   Center (16123); every classification decision is written to a local audit log.

A research/benchmark panel in the frontend displays precomputed retrieval-evaluation
stats from the author's prior work. No numbers are computed live, and no claim is made
that the system itself is evaluated beyond the verified checks in
`backend/ml_assets/vision/verification_report_live.md`.

## Features

- **Hybrid RAG in Bengali** — BM25Okapi (k1=2.2, b=0.4) + FAISS `IndexFlatIP` over
  mE5-small (384-dim) dense embeddings, with per-query top-k fusion.
- **Four-stage agent pipeline** — Safety/Router -> Retrieval -> Generation ->
  Verifier. Each stage emits a trace event consumed by the frontend stepper UI.
- **Six-way safety classification** — `safe_agri`, `banned_or_restricted_chemical`,
  `self_harm_or_poisoning_risk`, `off_topic`, `prompt_injection`, `low_confidence`.
  Terminal categories stop the pipeline before any retrieval happens.
- **Local audit trail** — every query, category, action, and timestamp appended to
  `backend/app/logs/safety_audit.jsonl`; surfaced via `GET /api/safety/metrics`.
- **Streaming chat** — SSE transport (`POST /api/qa/stream`) emitting stage events,
  token chunks, and a final typed response.
- **Photo-based diagnosis** — `POST /api/classify` (crop) and `POST /api/detect`
  (crop -> disease -> treatment advice, with confidence and quality warnings).
  Current artifacts are classification models; the API reports
  `detection_mode: "classification"` and never claims bounding boxes.
- **Weather + helpline extras** — token-efficient Bengali weather summary with a
  one-line agri tip, and a local-only helpline registration endpoint (no external
  telemetry).
- **Replaceable LLM adapters** — the pipeline depends on a small `LLMClient` port,
  not a provider SDK. Switching between OpenRouter, Gemini, Ollama, or a stub is a
  configuration change (`LLM_PROVIDER`), not a code change.

## Architecture

The backend is organized as a layered composition root, not a script of module calls:

```
HTTP routers (app/api)                    -- transport only, no business logic
        |
        v
application use cases (app/application)   -- QA pipeline, vision pipeline
        |
        v
ports / protocols (app/ports)             -- LLM, retriever, verifier, vision,
                                             audit, session contracts
        |
        v
infrastructure adapters (app/infrastructure)
      -- OpenRouter/Gemini/Ollama client, BM25/FAISS retriever,
         Ultralytics inference, JSONL audit sink, in-memory sessions
```

Rules enforced by the refactor contract (`docs/refactor/ARCHITECTURE.md`):

- The application layer never imports `google.genai`, `httpx`, `ultralytics`,
  pickle, or filesystem paths directly. Those belong in infrastructure.
- The legacy `app/agents/` and `app/services/advisory/` directories are
  compatibility shims for offline scripts. No new behavior may be added there.
- One FastAPI process, one Next.js process. No auth, queues, microservices, or
  live index building.

### QA pipeline

```
QARequest
  -> SafetyClassifier.classify          (deterministic pre-check, then LLM; parse
                                         failure => low_confidence, stop)
  -> QueryBuilder.build                 (only for safe_agri)
  -> Retriever.retrieve                 (BM25 + dense, top-k)
  -> GenerationModel.generate           (streamed or one-shot)
  -> Verifier.verify                    (grounding check; flags ungrounded claims,
                                         esp. chemical dosages)
  -> SessionStore.append / AuditSink.record (exactly once)
  -> QAResponse | SSE event stream
```

`off_topic`, `prompt_injection`, `banned_or_restricted_chemical`,
`self_harm_or_poisoning_risk`, and `low_confidence` are terminal outcomes. They
receive a canned response (for harmful categories: a calm redirect to the Krishi
Call Center at 16123, plus a note to seek in-person medical help for
self-harm/poisoning framings) and never reach retrieval or generation.

### Vision pipeline

```
uploaded image
  -> crop classifier (6 families)
  -> route to crop-specific disease model (rice 8 / corn 4 / potato 3 /
     brassica 11 / wheat 11 classes)
  -> disease + Bengali info + treatment advice (grounded in the disease
     knowledge map, `backend/ml_assets/advisory/disease_knowledge_map.json`)
  -> verifier flags + agent trace returned to the UI
```

All checked-in `.pt` weights are verified `task: classify`. The ONNX export path
exists for future detection artifacts but nothing in the UI or API claims
bounding boxes today.

## Tech Stack

| Layer          | Choice |
|----------------|--------|
| Frontend       | Next.js 16 (App Router), React 19, TypeScript 5.9 |
| Styling        | Tailwind CSS 4 + shadcn/ui |
| Animation      | Motion 13 (formerly Framer Motion) |
| Chat UX        | Vercel AI SDK 7 (streaming) |
| Backend        | FastAPI 0.141 (Python 3.11-3.12), single service |
| LLM serving    | Ollama (local fine-tuned Gemma 4-bit); OpenRouter/Gemini adapters available |
| Vision         | Ultralytics YOLO (classify), ONNX Runtime |
| Retrieval      | rank-bm25 + FAISS (CPU), loaded in-process from disk |
| Package mgmt   | pnpm (frontend), uv (backend) |
| Lang tooling   | bnunicodenormalizer (Bengali Unicode normalization) |

## Repository Layout

```
├── AGENTS.md                  Agent instructions, hard rules, locked stack
├── .env.example               All backend/frontend env vars, documented
├── backend/
│   ├── app/
│   │   ├── api/               HTTP transport: qa, vision, benchmark, extras
│   │   ├── application/       Use cases: qa_pipeline, vision_pipeline, container
│   │   ├── domain/            Enums, contracts, safety policy
│   │   ├── ports/             Provider protocols (LLM, retriever, verifier, ...)
│   │   ├── infrastructure/    Adapters: llm, retrieval, vision, audit, sessions
│   │   ├── agents/            Compatibility shims (legacy, do not extend)
│   │   ├── services/          Compatibility shims (legacy, do not extend)
│   │   ├── logs/              Audit trail output (gitignored)
│   │   └── main.py            App factory + composition root
│   ├── ml_assets/
│   │   ├── rag_index/         Corpus, indexes, provenance, eval results
│   │   ├── vision/            Crop classifier + per-crop disease weights
│   │   ├── advisory/          Disease knowledge map (Bengali)
│   │   └── gemma/             GGUF target for local inference
│   ├── scripts/               Offline build/eval/test scripts
│   └── tests/                 test_api, test_pipeline, test_vision
├── frontend/
│   └── src/
│       ├── app/               (app) chat/detect/analytics, (marketing) pages
│       ├── components/        chat, detect, layout, ui
│       └── lib/               api client, Bengali helpers, constants
├── demo-assets/               Demo images for the live investor demo
├── docs/                      Plans, architecture, vision-pipeline docs
└── scripts/                   Offline build/eval/test scripts (repo root)
```

## Getting Started

### Prerequisites

Verified on Windows 11 (see `SETUP_REPORT.md`):

| Tool         | Version          |
|--------------|------------------|
| Node.js      | v24 LTS          |
| pnpm         | 11.x             |
| Python       | 3.12             |
| uv           | 0.11+            |
| Ollama       | optional (only if using the `ollama` LLM provider) |

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Health check: `http://localhost:8000/health` returns `{"status": "ok", ...}`.
The FastAPI docs (Swagger) are served at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

Open `http://localhost:3000`. In dev, `next.config.ts` rewrites `/api/*` and
`/health` to the backend, so the frontend and backend share an origin.

### First run notes

1. Copy `.env.example` to `.env` in the repo root and set `LLM_API_KEY` (or
   install Ollama and switch `LLM_PROVIDER=ollama` with `OLLAMA_MODEL_NAME`
   pointing at your local tag).
2. Without a key, run with `LLM_PROVIDER=stub`: intent classification fails
   closed (safe behavior for tests) and generation returns stub output. Useful
   for API contract work, not for a real answer.
3. RAG indexes are precomputed and loaded from
   `backend/ml_assets/rag_index/` at startup. Nothing is built at request time.

## Configuration

Settings are read from the repo-root `.env`, then overridden by
`backend/.env.local` (local secrets win). See `.env.example` for the full list.

| Variable | Default | Purpose |
|---|---|---|
| `LLM_PROVIDER` | `openrouter` | Adapter: `openrouter`, `gemini`, `ollama`, `stub` |
| `LLM_MODEL_NAME` | `krishokchat-4b` | Model for both stages unless overridden |
| `LLM_BASE_URL` | *(empty)* | Endpoint override for HTTP-compatible servers |
| `LLM_API_KEY` | *(empty)* | Provider key (prefer local secret file) |
| `LLM_TIMEOUT_SECONDS` | `30` | Request bound for remote adapters |
| `LLM_TEMPERATURE` | `0.2` | Generation temperature |
| `LLM_MAX_OUTPUT_TOKENS` | `1000` | Max tokens per generation call |
| `INTENT_MODEL_NAME` / `GENERATION_MODEL_NAME` | *(empty)* | Role-specific model overrides |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL_NAME` | `krishokchat-4b` | Ollama model tag |
| `OPENROUTER_MODEL` | `google/gemini-2.5-flash-lite` | OpenRouter model |
| `GEMINI_MODEL` | `gemini-2.5-flash-lite` | Gemini model |
| `BACKEND_HOST` / `BACKEND_PORT` | `0.0.0.0` / `8000` | Uvicorn bind address |
| `FRONTEND_ORIGIN` | `http://localhost:3000,...` | CORS allow-list (comma-separated) |
| `RETRIEVAL_TOP_K` | `5` | Passages fused per query |
| `RAG_BACKEND` | `FAISS` | Retrieval store (Chroma supported by contract) |
| `AUDIT_LOG_PATH` | `backend/app/logs/safety_audit.jsonl` | Audit trail location |
| `SESSION_MAX_TURNS` | `10` | History length cap |
| `SESSION_TTL_SECONDS` | `1800` | Session expiry |
| `VISION_CROP_CONFIDENCE_THRESHOLD` | `0.60` | Minimum crop-class confidence |
| `VISION_DISEASE_CONFIDENCE_THRESHOLD` | `0.55` | Minimum disease-class confidence |
| `VISION_MAX_IMAGE_BYTES` | `10000000` | Upload size limit (10 MB) |
| `DEMO_MODE` | `true` | Enables the demo answer cache (exact-replay lane) |
| `DEMO_CACHE_PATH` | `demo-assets/cached_responses.json` | Cached demo responses (verified pipeline outputs only) |
| `DEMO_CACHE_MAX_ENTRIES` | `100` | Max entries kept in the demo answer cache |
| `QUERY_REWRITE_ENABLED` | `true` | Follow-up queries rewritten into standalone retrieval queries (history-aware) |
| `NEXT_PUBLIC_BACKEND_URL` | `http://localhost:8000` | Frontend -> backend URL |

The frontend additionally reads `frontend/.env.local`
(`NEXT_PUBLIC_API_BASE`), though in dev the rewrite proxy makes it unnecessary.

## API Reference

Base URL: `http://localhost:8000`. All request/response payloads are UTF-8;
Bengali is preserved with `ensure_ascii=False`.

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness + app version |
| POST | `/api/qa` | Full QA pipeline, single JSON response |
| POST | `/api/qa/stream` | QA pipeline as SSE stream (stages, tokens, final) |
| GET | `/api/models` | Generation model availability (gemini / krishokchat-4b) |
| GET | `/api/safety/metrics` | Audit-derived counts by category (no fabrication) |
| POST | `/api/classify` | Crop classification of an uploaded image |
| POST | `/api/detect` | Crop -> disease -> treatment advisory for an image |
| GET | `/api/benchmark` | Precomputed retrieval-benchmark stats (see Limitations) |
| POST | `/api/weather` | Bengali weather summary + agri tip for a district |
| GET | `/api/soil/dataset` | Frozen soil-moisture dataset stats (722 imgs, 6 soil types) |
| POST | `/api/soil/analyze` | Soil photo analysis — locked until model verification, returns honest trace |
| POST | `/api/helpline/register` | Local-only helpline registration (JSONL) |

### POST /api/qa

Request:

```json
{
  "query": "ধান গাছের পাতা হলুদ হয়ে যাচ্ছে কেন?",
  "session_id": "demo-1",
  "crop": null,
  "disease": null,
  "history": []
}
```

Response shape: `query`, `category`, `answer`, `sources[]` (id, crop, disease,
question, score, answer excerpt, treatment, source, `expert_verified`),
`confidence` (`verified` / `flagged-unverified` / `low_confidence` / `blocked`),
`agent_trace[]` (stage, status, detail), `verifier_flags[]`, `model`.

### POST /api/qa/stream (SSE)

Events are lines of the form `<event>: <json>\n\n`:

- `data:` — `AgentStageEvent` (`{"stage": "safety", "status": "complete", ...}`)
- `token:` — `{"text": "..."}` partial generation chunks
- `final:` — the complete `QAResponse` object

The frontend renders the stage events as the "agent trace" stepper
(Checking safety -> Retrieving sources -> Generating answer -> Verifying).

## Data & Models

### Local model — KrishokChat-4B (optional)

The chat UI offers two generation models: **Gemini 2.5 Flash-Lite** (online,
default) and **KrishokChat-4B** (local, via Ollama). The local option is
disabled in the UI until the model is actually registered in Ollama.

Activate it in one command once you have the fine-tuned GGUF:

```powershell
# GGUF at backend\ml_assets\gemma\model.gguf (default location)
powershell -ExecutionPolicy Bypass -File scripts\local_model.ps1

# Or: point at a GGUF elsewhere / download it automatically
powershell -ExecutionPolicy Bypass -File scripts\local_model.ps1 -GgufPath "D:\models\krishokchat-4b-q4.gguf"
powershell -ExecutionPolicy Bypass -File scripts\local_model.ps1 -DownloadUrl "https://huggingface.co/<org>/<repo>/resolve/main/<file>.gguf"
```

What it does: ensures the GGUF exists, starts Ollama if needed, registers the
tag `krishokchat-4b` from `scripts/Modelfile`, restarts the backend, and
verifies via `GET /api/models`. Manual equivalent:

```powershell
ollama serve   # or start the Ollama app
cd backend\ml_assets\gemma
ollama create krishokchat-4b -f ..\..\..\scripts\Modelfile
```

Until the tag exists, choosing the local option in the UI fails closed: the
pipeline returns the 16123 referral with `low_confidence` instead of a
plausible-but-fake answer.

### RAG corpus (`backend/ml_assets/rag_index/`)

| Item | Value |
|---|---|
| Knowledge nodes | 2,120 (cleaned, normalized, Gemini-refined) |
| Source documents | 2,946 markdown files |
| Source institutions | 13 Bangladeshi agricultural bodies (BARC, BARI, DAE, CABI, ...) |
| Sparse index | BM25Okapi, k1=2.2, b=0.4 |
| Dense index | mE5-small embeddings (384-dim), FAISS `IndexFlatIP` (exact) |
| Provenance | Node-to-QA and MD-to-QA mapping manifests under `provenance/` |

### Vision models (`backend/ml_assets/vision/`)

All weights verified against the actual artifact metadata (see
`backend/ml_assets/vision/verification_report_live.md`):

| Model | Task | Classes |
|---|---|---|
| crop_classifier | classify | 6 families (Brassica, Corn, GourdGuava, Potato, Solanacea, Wheat) |
| rice_disease | classify | 8 (BLB, Brown Spot, Healthy, Leaf Blast, Leaf Scald, Narrow Brown Spot, Rice Hispa, Sheath Blight) |
| corn_disease | classify | 4 |
| potato_disease | classify | 3 (Early Blight, Healthy, Late Blight) |
| brassica_disease | classify | 11 (cabbage x4, cauliflower x7) |
| wheat_disease | classify | 11 |

Verified live results: wheat 11-class sweep 44/50 (88%) correct with 100%
Bengali treatment info; 437-image crop-library sweep returned Bengali disease
info for 436/437 images (99.8%).

### Safety dataset

A 20,112-record Bengali safety evaluation dataset (refusal + requery splits,
6 dialects, 12 categories) lives in `KrishokChat/dataset_release/safety/`
alongside generation scripts and a design doc in `docs/pipeline/scripts/`.

## Frontend Routes

| Path | Page |
|---|---|
| `/` | Marketing home |
| `/chat` | Q&A assistant with agent-trace stepper |
| `/detect` | Photo upload -> crop/disease/advisory |
| `/soil` | Soil moisture field console — dataset showcase + locked analyzer |
| `/analytics` | Safety metrics panel (from audit log) |
| `/research`, `/research/benchmark`, `/research/methodology`, `/research/safety` | Research/benchmark panel |
| `/about`, `/team`, `/data`, `/library`, `/contact`, `/auth` | Marketing/support pages |

## Testing & Verification

Backend smoke checks (no external services required):

```bash
cd backend
uv run python -m compileall -q app
uv run python -c "from app.main import app; print(app.title, app.version)"
```

Integration tests live in `backend/tests/` (`test_api.py`, `test_pipeline.py`,
`test_vision.py`). Run the offline scripts under `backend/scripts/` for
retrieval, classifier, and pipeline checks (e.g. `test_qa_pipeline.py`,
`test_bm25_retrieval.py`). `pytest` is not a declared dependency yet; the tests
are runnable with the venv's interpreter once added.

Frontend checks:

```bash
cd frontend
pnpm lint
pnpm build
```

## Known Limitations

- `GET /api/benchmark` is a placeholder returning
  `{"status": "not_implemented"}`. Precomputed stats exist under
  `backend/ml_assets/rag_index/eval/` and are wired into frontend copy, but the
  endpoint itself is not filled in.
- The demo answer cache (`demo-assets/cached_responses.json`) is populated by
  `uv run python scripts/prewarm_demo_cache.py` or self-populates on the first
  live ask in DEMO_MODE; until prewarmed, first-time curated questions run the
  live pipeline (5–15 s) exactly as before.
- Vision artifacts are classification-only. Object detection (bounding boxes)
  is supported by the ONNX export path but no detection weights are checked in,
  so nothing claims boxes.
- `pytest` is not in `backend/pyproject.toml`; add it as a dev dependency
  before treating `backend/tests/` as a runnable suite.
- Ollama is not installed in the dev environment; the default adapter is
  OpenRouter.

## Documentation

| Document | Content |
|---|---|
| `AGENTS.md` | Hard rules, locked tech stack, demo constraints |
| `docs/high_level_plan.md` | 7-day roadmap, latency engineering, demo tactics |
| `docs/00_preprocessing_plan.md` | Corpus preprocessing |
| `docs/01_chatbot_rag_plan.md` | RAG + chatbot pipeline |
| `docs/03_safety_aware_agentic_pipeline.md` | Four-stage agent pipeline |
| `docs/04_router.md` | Crop classifier + YOLO pipeline |
| `docs/refactor/ARCHITECTURE.md` | Backend contracts, dependency direction |
| `docs/refactor/REFACTOR_PLAN.md` | Refactor milestones and gates |
| `docs/refactor/PROJECT_HANDOFF.md` | Persistent handoff for future agents |
| `docs/vision-pipeline/` | Vision architecture, API reference, verified stats |
| `docs/advisory_workflow/` | Advisory workflow plans |
| `backend/README.md` | Backend run/replacement details |
| `SETUP_REPORT.md` | Environment bootstrap report (versions, verification) |

## Status & License

Version 0.2.0. Research prototype built for a 7-day capstone demo; not intended
for production use. No license is declared. Related research assets are
referenced from the frontend (`frontend/src/lib/constants.ts`): the dataset on
Hugging Face (`RaiyanKhaan/krishokChat`). The authoritative research papers are
the local files in `paper/done papers/` (see `docs/PAPER_POLICY.md` — the old
arXiv listing is deprecated and must not be cited).
