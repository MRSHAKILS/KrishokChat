# TASK 00 — Environment Bootstrap & Folder Scaffolding

**Read `AGENTS.md` in the repo root first — it governs everything below.**

This is a preprocessing task: create the folder skeleton and get every tool installed and verified. **Do not write application logic yet.** Do not integrate the design system yet (`DESIGN.md` doesn't exist). Stop at "everything installed, folders exist, hello-world runs" and report back.

Work through the steps in order. For every install step marked 🔎, search the internet first to confirm the current recommended stable version before installing — do not rely on memorized version numbers, they go stale. After each numbered step, verify it worked before moving to the next.

---

## Step 1 — Create the repo and folder structure

1. Create the root folder `agri-ai-capstone/` and `cd` into it.
2. Initialize git (`git init`).
3. Create the full folder tree exactly as specified in `AGENTS.md` Section 5 (frontend/, backend/ with its subfolders, docs/, demo-assets/, scripts/). Empty folders are fine for now — add a `.gitkeep` where needed so git tracks them.
4. Create a root `.gitignore` covering at minimum: `node_modules/`, `.next/`, `__pycache__/`, `*.pyc`, `.venv/`, `.env`, `backend/app/logs/*` (but keep the folder via `.gitkeep`), `backend/ml_assets/` large binary weight files (these should NOT go into git — flag this and instead note in `README.md` where the real weight files should be manually copied from).
5. Create an empty `.env.example` at root — will be filled in as later steps add variables.
6. Copy the existing masterplan content into `docs/masterplan.md` if provided, otherwise create a placeholder noting it will be added.

**Verify:** `tree -L 3` (or equivalent) shows the structure matching AGENTS.md Section 5.

---

## Step 2 — System-level prerequisites

🔎 For each tool below, search for "current stable/LTS version [tool name] 2026" and confirm compatibility with the others before installing.

1. **Node.js** — install the current LTS version. Verify with `node -v`.
2. **pnpm** — install via corepack (`corepack enable pnpm`) or the official install script. Verify with `pnpm -v`.
3. **Python** — install a current stable 3.x version compatible with PyTorch/Ultralytics/FastAPI (check Ultralytics' and PyTorch's stated supported Python versions first — don't just grab the newest Python, confirm the ML libraries support it). Verify with `python3 --version`.
4. **uv** (Python package/env manager) — install via the official install script. Verify with `uv --version`. If `uv` cannot be installed in this environment, fall back to standard `venv` + `pip` and note that in `README.md`.
5. **Ollama** — install via the official method for this OS. Verify with `ollama --version`.
6. **git**, **curl** — confirm already present (`git --version`, `curl --version`); install if missing.

**Verify:** every version command above runs and prints a version with no errors.

---

## Step 3 — Frontend scaffold

1. Inside `frontend/`, scaffold a new Next.js app (App Router, TypeScript, Tailwind CSS) using the current official `create-next-app` flow. 🔎 confirm current recommended flags/prompts for Next.js before running, since defaults change between versions.
2. Initialize shadcn/ui in the project using its official CLI init command. 🔎 confirm the current shadcn CLI command (it has changed across versions — verify against the official shadcn/ui docs, not memory).
3. Add the Vercel AI SDK package(s) needed for streaming chat. 🔎 confirm current package name(s) — the AI SDK has had major version changes; check official Vercel AI SDK docs for the current install command.
4. Add Motion (`motion` package, formerly `framer-motion`). 🔎 confirm current package name — it was renamed; installing the old name may pull a deprecated package.
5. Run `pnpm dev` and confirm the default Next.js starter page loads in a browser at `localhost:3000` with no console errors.
6. Do not add any custom styling, pages, or components yet — this step only proves the toolchain works.

**Verify:** app boots cleanly, shadcn CLI successfully added at least one test component (e.g. `button`) without errors, no TypeScript errors on build (`pnpm build`).

---

## Step 4 — Backend scaffold

1. Inside `backend/`, initialize a Python project with `uv init` (or `venv` fallback).
2. Add core dependencies: `fastapi`, an ASGI server (`uvicorn`), `pydantic`. 🔎 confirm current stable versions and that they're mutually compatible.
3. Add ML dependencies: `ultralytics` (YOLO), `torch` (🔎 confirm the correct install command for the available hardware — CPU-only vs CUDA build differ; check the official PyTorch install-selector page for the current command), `onnxruntime` (or `onnxruntime-gpu` if a CUDA GPU is confirmed available).
4. Add retrieval dependencies: `faiss-cpu` (or `chromadb` — pick one; 🔎 check current recommended install method for whichever is chosen, `faiss` in particular has OS-specific install quirks).
5. Add an Ollama Python client, or plan to call Ollama's local REST API directly with `httpx` — 🔎 check whether an official/well-maintained Ollama Python client currently exists and is actively maintained before adding it as a dependency; if not, just use `httpx` against the local Ollama API.
6. Create a minimal `backend/app/main.py` with a single `GET /health` route returning `{"status": "ok"}`. No other routes yet.
7. Run the dev server and confirm `GET /health` responds correctly from a browser or `curl`.

**Verify:** `uv run uvicorn app.main:app --reload` (or equivalent) starts cleanly, `/health` returns 200.

---

## Step 5 — Ollama + Gemma model check

1. Confirm the fine-tuned Gemma-4 4-bit model files/weights are available (from the existing research work). Copy or symlink them into a sensible location for Ollama to load — do not commit large weight files to git.
2. 🔎 Confirm the current correct method to load a custom/fine-tuned GGUF model into Ollama (this typically involves a `Modelfile` — check current Ollama docs for the exact syntax, it has evolved).
3. Load the model into Ollama and run one test prompt from the CLI (`ollama run <model-name>`) to confirm it responds.
4. Confirm Ollama's local REST API (default `http://localhost:11434`) responds to a basic `curl` request against the loaded model.

**Verify:** one successful CLI generation, one successful REST API call, both using the actual fine-tuned model (not a stock Gemma).

---

## Step 6 — YOLO + classifier weight check

1. Confirm all existing trained YOLO `.pt` files (one per crop) and the crop classifier weights are placed under `backend/ml_assets/yolo/` and `backend/ml_assets/classifier/` respectively (copy from wherever they currently live — do not retrain anything in this task).
2. Write and run `scripts/export_yolo_models.py`: loads each `.pt` file with Ultralytics and exports to ONNX, saving alongside the original. 🔎 confirm current Ultralytics export syntax/arguments before writing this script.
3. Run one test inference per exported model against any single sample image to confirm the export didn't break anything (this can be a throwaway script, doesn't need to be production code yet).

**Verify:** every crop YOLO model has a corresponding `.onnx` file, and at least one test inference succeeds per model.

---

## Step 7 — Retrieval index check

1. Confirm the existing precomputed retrieval artifacts (embeddings, BM25 index, or raw corpus to rebuild from) are available.
2. Write and run `scripts/build_rag_index.py`: builds/loads the FAISS or Chroma index from the existing data and saves it under `backend/ml_assets/rag_index/`. This should be a one-time offline build, not something that runs per-request.
3. Run one test query against the loaded index to confirm retrieval returns sensible results.

**Verify:** index files exist on disk, one test retrieval query returns results.

---

## Step 8 — Report back

Write a short `SETUP_REPORT.md` at the repo root summarizing:
- Every tool/package installed and the version actually installed (from the 🔎 checks).
- Any step that had to deviate from these instructions, and why.
- Any step that could not be completed (e.g. missing model weight files, no GPU available) — flag clearly, don't silently skip.
- Confirmation that Steps 1–7's verify criteria all passed.
- **Hardware & Software Configuration Log:** Document GPU/CPU, RAM, model quantization, inference engine, tokenizer/chat template, ONNX export settings, and retrieval index version for reproducibility.
- **Reproducibility Artifacts:** Ensure model cards, data cards, versioning documentation, and checksum files for weights are created or explicitly linked in the documentation.

**Stop here.** Do not begin building actual application routes, UI screens, or the agentic pipeline logic — those are separate tasks that come after the design system (`DESIGN.md`) is ready.