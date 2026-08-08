# KrishokChat Advisory System

A safety-aware, grounded, multimodal Bangla agricultural advisory system targeting smallholder farmers in Bangladesh.

## What This Is

- A **Bengali agri Q&A assistant** — RAG (BM25 + dense retrieval) feeding a fine-tuned Gemma-4 4-bit model
- A **crop disease detector** — crop classifier → per-crop YOLO model → annotated diagnosis
- A **research/benchmark panel** — precomputed retrieval-benchmark numbers displayed as credibility content
- A **safety-aware agentic pipeline** wrapping the Q&A assistant (Safety → Retrieval → Generation → Verification)

## Quick Start

### Prerequisites
- Node.js v24 LTS, pnpm v11+
- Python 3.12, uv v0.11+
- Ollama (for local LLM inference)

### Backend
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
# → http://localhost:8000/health
```

### Frontend
```bash
cd frontend
pnpm install
pnpm dev
# → http://localhost:3000
```

## Project Structure
See `AGENTS.md` Section 5 for the full folder layout.

## Tech Stack
See `AGENTS.md` Section 3 (locked, do not deviate).

## Documentation
- `AGENTS.md` — Agent instructions, hard rules, locked stack
- `docs/high_level_plan.md` — 7-day roadmap, latency engineering, demo tactics
- `docs/ui_ux_design_plan.md` — Design system, page specs, component vocabulary
- `docs/00_preprocessing_plan.md` — This setup task
- `docs/01_chatbot_rag_plan.md` — Core RAG + chatbot pipeline
- `docs/03_safety_aware_agentic_pipeline.md` — Four-stage agent pipeline
- `docs/04_router.md` — Crop classifier + YOLO detection pipeline
- `SETUP_REPORT.md` — Environment bootstrap report (versions, verification)

## Safety
This system classifies every query before retrieval. Unsafe queries (banned chemicals, self-harm, prompt injection) receive a canned response redirecting to **Krishi Call Center — dial 16123**. Every classification is logged to a local audit trail (`backend/app/logs/`).

## License
Research prototype — not for production use.
