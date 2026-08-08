# SETUP_REPORT.md — Environment Bootstrap

**Date:** 2026-08-07
**Task:** TASK_00 — Environment Bootstrap & Folder Scaffolding
**Status:** Phases 1-5 complete. Phases 6-8 pending user-provided model/corpus files.

---

## 1. Installed Tools & Versions

| Tool | Version | Installed Via | Confirmed Working |
|---|---|---|---|
| Node.js | v24.11.0 LTS | Pre-existing | ✅ |
| pnpm | 11.1.1 | corepack | ✅ |
| Python | 3.12.0 | Pre-existing | ✅ |
| uv | 0.11.28 | Pre-existing (latest is 0.12.2) | ⚠️ Functional, not latest |
| git | 25.2.0 | Pre-existing | ✅ |
| Ollama | NOT INSTALLED | — | ❌ Needs `winget install Ollama` |

## 2. Frontend Stack (Verified)

| Package | Version | Source |
|---|---|---|
| next | 16.3.0 | npm (latest, released Aug 3 2026) |
| react | 19.2.8 | npm (canary via Next.js 16) |
| typescript | 5.9.3 | npm (7.0 available but not yet stable with typescript-eslint) |
| tailwindcss | 4.3.3 | npm (v4 stable) |
| ai (Vercel AI SDK) | 7.0.55 | npm (v7 released Jun 25 2026) |
| motion | 13.0.0 | npm (formerly framer-motion) |
| shadcn/ui | 4.16.2 + base-nova preset | CLI init |
| lucide-react | 1.29.0 | npm (via shadcn) |

**Verification:** `pnpm build` succeeds (TypeScript compiled, static pages generated). `pnpm dev` serves on :3000 (HTTP 200). Playwright screenshot confirms render.

## 3. Backend Stack (Verified)

| Package | Version | Source |
|---|---|---|
| fastapi | 0.141.1 | PyPI (latest, Jul 29 2026) |
| pydantic | 2.13.4 | PyPI (via FastAPI) |
| uvicorn | 0.52.1 | PyPI (via FastAPI standard) |
| torch | 2.13.0+cpu | PyPI (CPU wheel) |
| torchvision | 0.28.0 | PyPI |
| ultralytics | 8.4.116 | PyPI (YOLO26 support) |
| onnxruntime | 1.28.0 | PyPI |
| faiss-cpu | 1.15.0 | PyPI |
| httpx | 0.28.1 | PyPI |

**Verification:** All packages import successfully via `uv run python -c "import ..."`. `GET /health` returns 200.

## 4. Hardware & Software Configuration

| Attribute | Value |
|---|---|
| OS | Windows 11 |
| CPU | x86_64 (AVX2) |
| GPU | None detected (CPU-only PyTorch installed) |
| RAM | Unknown |
| Python | 3.12.0 (constrained to >=3.11,<3.13 in pyproject.toml) |
| Inference engine | Ollama (not yet installed) |
| Retrieval | FAISS (CPU) |

## 5. Folder Structure Created

```
agri-ai-capstone/
├── .gitignore                     ✅ (node_modules, .next, __pycache__, ml_assets)
├── .env.example                   ✅ (12 env vars documented)
├── SETUP_REPORT.md                ✅ (this file)
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                ✅ (FastAPI app + /health + CORS)
│   │   ├── api/                   (empty, awaiting route stubs)
│   │   ├── agents/                (empty, awaiting TASK_03)
│   │   ├── core/
│   │   │   ├── config.py          ✅ (pydantic-settings)
│   │   ├── models/                (empty, awaiting schemas)
│   │   ├── services/              (empty, awaiting TASK_01)
│   │   └── logs/
│   │       └── .gitkeep           ✅
│   ├── ml_assets/
│   │   ├── yolo/.gitkeep          ❌ Waiting for .pt files
│   │   ├── classifier/.gitkeep    ❌ Waiting for classifier weights
│   │   ├── gemma/.gitkeep         ❌ Waiting for GGUF
│   │   └── rag_index/.gitkeep     ❌ Waiting for corpus JSON
│   ├── pyproject.toml             ✅ (all deps pinned)
│   └── tests/                     (empty)
├── frontend/
│   ├── src/app/
│   │   ├── layout.tsx             ⚠️ Default (needs Bengali font + metadata)
│   │   ├── page.tsx               ⚠️ Default (needs real landing page)
│   │   └── globals.css            ✅ (Tailwind v4 + shadcn theme)
│   ├── components/ui/             ✅ (button, card, input, badge, avatar, separator, skeleton, tabs, alert-dialog, dialog)
│   ├── lib/                       (utils.ts via shadcn)
│   ├── public/                    ✅ (Next.js defaults)
│   ├── components.json            ✅ (base-nova, RSC enabled)
│   ├── package.json               ✅
│   └── tsconfig.json              ✅
├── demo-assets/
│   └── images/.gitkeep            ❌ Waiting for demo images
└── scripts/                       (empty)
```

## 6. Completed Steps

- [x] Full folder tree per AGENTS.md Section 5
- [x] git init + .gitignore (ML assets excluded)
- [x] .env.example (all vars documented with comments)
- [x] Backend: `uv init` + FastAPI + all ML deps
- [x] Backend: `app/main.py` with `/health` + CORS middleware
- [x] Backend: `app/core/config.py` (pydantic-settings)
- [x] Frontend: `create-next-app` (Next.js 16.3, TS, Tailwind v4, App Router)
- [x] Frontend: shadcn/ui init (base-nova preset, RSC, Tailwind v4)
- [x] Frontend: shadcn components (button, card, input, badge, avatar, separator, skeleton, tabs, alert-dialog, dialog)
- [x] Frontend: Vercel AI SDK v7 + Motion v13
- [x] All verify criteria passed

## 7. Blocked / Pending

| Step | Blocked On | Action Required |
|---|---|---|
| Ollama install | None | Run `winget install Ollama` |
| Gemma GGUF loading | GGUF file | Place in `backend/ml_assets/gemma/` |
| YOLO export | .pt weight files | Place in `backend/ml_assets/yolo/` |
| Crop classifier | Classifier weights | Place in `backend/ml_assets/classifier/` |
| RAG index build | `knowledge_nodes.json` | Place in `backend/ml_assets/rag_index/` |
| Demo images | Sample leaf photos | Place in `demo-assets/images/` |

## 8. Deviations from Plan

| Deviation | Reason |
|---|---|
| Python constrained to `>=3.11,<3.13` | PyTorch CPU wheels unavailable for 3.14+ via PyPI default index |
| `next lint` not available | Next.js 16 removed it; use `eslint` directly |
| TypeScript 5.9 instead of 7.0 | typescript-eslint doesn't fully support TS 7 yet (per research) |
| Playwright added as devDep | For visual verification during setup |

## 9. Reproducibility Notes

- To reproduce backend: `cd backend && uv sync && uv run uvicorn app.main:app --reload`
- To reproduce frontend: `cd frontend && pnpm install && pnpm dev`
- All large weight files are in `.gitignore` — document checksums separately
