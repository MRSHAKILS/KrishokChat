# AGENTS.md — Agent Instructions for Bangladesh Agri-AI Capstone

Read this file fully before doing any work. This is a **7-day capstone demo prototype**, not a production system. Every instruction below exists to protect a 3–4 minute live investor demo. When in doubt, choose the simpler option.

> **Mandatory handoff:** Before changing code, read `docs/refactor/PROJECT_HANDOFF.md`,
> then consult `docs/refactor/ARCHITECTURE.md` for contracts and
> `docs/refactor/REFACTOR_PLAN.md` for staged work. These files are the persistent
> implementation memory for future agents; do not replace them with a new ad-hoc plan.
>
> **Next-phase roadmap (post-refactor):** the architecture-refinement work (the
> five-tier resolution ladder, fact base, structured resolver, real weather) is
> planned in `docs/production_readiness/tasks/R_SERIES_EXECUTION_INDEX.md`. That
> index is the single entry point: it gives the execution order, dependencies,
> external inputs, and the fair-vs-paper track split. The "why" lives in
> `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md`. Execute one `R#`
> task per branch; each must hold the standing baseline (full suite
> **410 passed / 7 skipped / 0 failed**, golden replay **50/50**, `pnpm build`
> green) before the next starts.
>
> **Research/paper trace (added 2026-08-27):** `experiments/registry.yaml` is the
> canonical experiment-layer trace (completed battery E02–E13 + planned CEA-pivot
> layers E14–E26; it resolves all conflicting E-numbering used by older review
> docs). `paper/manifest.yaml` traces every file in the paper folder. New
> experiments follow `experiments/specs/*.spec.yaml` → runner in
> `experiments/scripts/<layer>/` → frozen YAML in `experiments/results/<layer>/`
> → registry status update, under `experiments/ACCEPTANCE_PROTOCOL.md` (run →
> verify → real-application check → freeze → author signs acceptance). Targets
> written in specs are hypotheses, never results (rule 5 applies).
>
> **Two-track map (production vs paper — keep them separated):**
> - **Production track** = `backend/` + `frontend/` + `supabase/` + `deploy/`, governed by the
>   R-series index (`docs/production_readiness/tasks/R_SERIES_EXECUTION_INDEX.md`; R1–R13 done —
>   R13 grounded chunk fallback dark-launched 2026-08-27 under Amendment 03, flag
>   `CHUNK_FALLBACK_ENABLED` default-off until experiment E26 is accepted) with standing gates:
>   full suite green (no new failures vs. baseline; the 5 `scripts/test_live_e2e.py` failures are
>   environmental, they need a live server), golden replay 50/50, `pnpm build` green.
>   App code must never read `paper/`, `research_artifacts/`, or `experiments/` at runtime.
> - **Paper track** = `paper/` + `experiments/` + `research_artifacts/`, governed by
>   `paper/manifest.yaml`, `experiments/registry.yaml`, and the frozen claim ledger
>   (`paper/manuscript/CLAIM_LEDGER_FREEZE.md`). Research harnesses may import `backend/app`
>   offline (documented scripts only), never the reverse.
> - **External research data root** `E:\CSE498R\Agri-LLM\KrishokChat` is the read-only origin of
>   datasets/chunks/processed MDs. The application must depend only on mirrored copies under
>   `backend/ml_assets/` (e.g. the 2,946 institutional MDs in `backend/ml_assets/rag_index/source_md/`).

---

## 1. What this project is

A full-stack showcase for existing, already-trained Bengali agriculture AI research:
- A **Bengali agri Q&A assistant** — RAG (BM25 + dense retrieval, already built) feeding a fine-tuned **Gemma-4 4-bit** model.
- A **crop disease advisory workflow** — a crop classifier first identifies the crop in an uploaded photo, then routes to a crop-specific Ultralytics model. The currently checked-in models are verified as `task: classify`; do not claim bounding-box object detection unless a real detection artifact is later added.
- A **research/benchmark panel** — precomputed stats from the author's existing retrieval-benchmark and evaluation work, displayed as credibility content, never computed live.
- A **safety-aware agentic pipeline** wrapping the Q&A assistant (see Section 4) — this is a headline feature for the poster/demo, so build it for real, not as decoration.

The person you're working for is the researcher and sole engineer. She will review every agent's output for visual and behavioral consistency before it's considered done.

---

## 2. Hard rules — do not violate these

1. **Authentication is additive and optional; it may never gate the demo.** Supabase Auth (approved by amendment `paper/archive/system_evolution_plan_2026/execution_planning_2026_08_12/15_SUPABASE_AUTH_AMENDMENT_2026_08_14.md`) provides sign-in for future premium features. The single-session demo remains the default path: with `DEMO_MODE=true` or with no signed-in user, every existing route and feature must behave exactly as before and remain fully offline-capable. A single-platform admin console, free/premium tiers (no feature gating by default), and broadcast announcements are permitted under amendment `docs/production_readiness/amendments/02_ADMIN_TIERS_BROADCAST_AMENDMENT_2026_08_22.md` — admin APIs verify the caller's `profiles.role='admin'` server-side (fail-closed) on every request. Still forbidden: role-based multi-tenancy, per-tenant data isolation, paywalls, runtime index rebuilding. Auth surfaces (login, register, account menu) must never force redirects, popups, or degradation on anonymous visitors.
2. **No live web scraping or live index-building.** All retrieval indexes and benchmark numbers are precomputed and loaded from disk.
3. **No Kubernetes, no Docker Compose with 6 services, no message queues.** One FastAPI backend process, one Next.js frontend process. That's it.
4. **Do not hardcode secrets/API keys in source.** Use `.env` files, and always create/update `.env.example` alongside any new required variable.
5. **Do not fabricate data.** If a benchmark number, model metric, or dataset stat isn't available in the provided files, leave a clearly marked `TODO` / placeholder rather than inventing a plausible-looking number.
6. **Do not silently change the tech stack** decided in Section 3. If something in Section 3 seems wrong for a task, stop and flag it instead of substituting your own choice.
7. **Before installing any dependency, search the internet for the current stable/recommended version** rather than relying on training data — package ecosystems move fast and pinned versions go stale. Prefer official docs, official GitHub releases, or the official package registry page as the source of truth. Note the version you chose and where you confirmed it (one line in the relevant `README.md` or commit message is enough).
8. **One task, one agent, one clear deliverable.** If a task description is ambiguous, do the smallest reasonable interpretation and leave a note rather than guessing big.
9. **The arXiv v1 paper (`arXiv:2606.29243`, "Citation-Grounded Dataset and Benchmark") is DEPRECATED and INVALID.** Never cite it, link it, summarize it, or reuse any number/claim from it. The authoritative papers live in `paper/done papers/` (`KrishokChat__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf`, `AgriTrust.pdf`). Reference them by filename/path only; never invent a new arXiv ID or URL. Full policy: `docs/PAPER_POLICY.md`.

---

## 3. Locked tech stack (do not deviate)

| Layer | Choice |
|---|---|
| Frontend framework | Next.js (App Router), TypeScript |
| Styling / components | Tailwind CSS + shadcn/ui |
| Animation | Motion (formerly Framer Motion) |
| LLM chat UX | Vercel AI SDK (streaming) |
| Backend | FastAPI (Python), single service |
| LLM serving | Ollama by default; llama.cpp OpenAI-compatible serving is approved for the verified local base+LoRA demo runtime |
| Object detection | Ultralytics YOLO, `.pt` weights exported to ONNX for inference |
| Retrieval index | FAISS or Chroma, loaded in-process from a precomputed index on disk |
| Package managers | `pnpm` for frontend, `uv` (or `venv` + `pip` if `uv` unavailable) for backend |
| Authentication | Supabase Auth (hosted + local CLI); `@supabase/supabase-js` ^2.112.3 + `@supabase/ssr` ^0.12.4 (frontend); PyJWT ES256 JWKS verification (backend) |

**Artifact reality note:** the current checked-in Ultralytics artifacts report
`task: classify`; the vision implementation must preserve the locked Ultralytics/ONNX
direction for future real detection artifacts, but must not claim boxes from these
classification weights.

**Local-model runtime amendment (2026-08-12):** `scripts/start_krishokchat_local.ps1`
may serve the verified external Q4_K_M base plus trained KrishokChat LoRA through
`llama-server` under the existing `krishokchat-4b` model ID. This narrow exception must
continue to use the shared QA pipeline and may not change safety, retrieval, verification,
audit, routes, or schemas. Evidence and claim limits are recorded in
`paper/system_evolution_plan_2026/execution_planning_2026_08_12/14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`.

Design system (colors, type, spacing, component conventions) will arrive later as a `DESIGN.md` file generated via Google Stitch. Until that file exists, use plain, unstyled-but-functional shadcn defaults — do not invent a visual identity yourself.

---

## 4. Safety-aware agentic pipeline — build this for real

This is a genuine architectural feature, not a poster prop, though it is also meant to be visually explainable on a poster/demo. The Q&A flow is a small multi-step agent pipeline, not a single LLM call:

```
User query
   │
   ▼
[1] Safety / Router Agent  →  classifies the query BEFORE any retrieval happens
   │
   ├─ unsafe / out-of-scope → return a canned safe response immediately, log it, stop
   │
   ▼ (safe agri query)
[2] Retrieval Agent  →  BM25 + dense retrieval over the precomputed index
   │
   ▼
[3] Generation Agent  →  Gemma-4 4-bit, answers grounded in retrieved passages, streamed to UI
   │
   ▼
[4] Verifier Agent  →  checks the generated answer against retrieved sources before it's shown;
                        flags/annotates claims (esp. chemical dosages, treatment amounts)
                        that aren't clearly grounded in retrieved passages
```

**Safety/Router Agent — classification categories** (this can be implemented as a small structured-output prompt to the same Gemma model, or a lightweight separate call — pick whichever is faster; do not build a separate trained classifier for this in 7 days):
- `safe_agri` — normal agriculture question → proceed to retrieval
- `banned_or_restricted_chemical` — asks about agrochemicals not approved for use in Bangladesh, or unsafe overdose/misuse of pesticides/fertilizers
- `self_harm_or_poisoning_risk` — any framing suggesting intent to harm a person, animal, or water source, or that reads as a personal crisis
- `off_topic` — unrelated to agriculture
- `prompt_injection` — attempts to override system instructions
- `low_confidence` — agriculture-related but outside what the retrieval corpus can support

**Canned safe responses**: for `banned_or_restricted_chemical` and `self_harm_or_poisoning_risk`, do not attempt to answer normally. Respond with a short, calm redirect and point to a real escalation contact: the Bangladesh government's **Krishi Call Center — dial 16123** (a real, currently active national agricultural helpline, verified). For `self_harm_or_poisoning_risk` specifically, keep the tone supportive and non-judgmental, and still include the 16123 redirect plus a note to seek in-person medical help if it's an emergency. Do not write a long safety essay — one short, clear message.

**Audit trail**: every classification decision (query, category, action taken, timestamp) gets appended to a local log (simple JSON lines file or SQLite table under `backend/app/logs/`). This log is what powers the "safety metrics" panel on the demo/poster (e.g., a small breakdown of how many queries were classified into each category during testing). Never log this to an external service — local file only, this is a prototype.

**Frontend**: surface this pipeline visually. When a query comes in, show a brief "agent trace" — e.g., a small stepper or chip sequence (Checking safety → Retrieving sources → Generating answer) — animated with Motion. This is cheap to build and is exactly the kind of thing that reads well to non-technical judges as "this isn't just a chatbot wrapper."

---

## 5. Folder structure to create

See `TASK_00_bootstrap.md` for the exact ordered task list. The target structure:

```
agri-ai-capstone/
├── AGENTS.md
├── README.md
├── .env.example
├── .gitignore
├── docs/
│   ├── masterplan.md
│   ├── DESIGN.md                 (added later, from Google Stitch)
│   ├── demo-script.md
│   └── safety-architecture.md
├── demo-assets/
│   ├── qa-demo-questions.md
│   └── images/
│       ├── <crop-1>/
│       ├── <crop-2>/
│       └── ...
├── frontend/                     (Next.js app)
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── qa.py
│   │   │   ├── classify.py
│   │   │   ├── detect.py
│   │   │   └── benchmark.py
│   │   ├── agents/
│   │   │   ├── orchestrator.py
│   │   │   ├── safety_agent.py
│   │   │   ├── retrieval_agent.py
│   │   │   ├── generation_agent.py
│   │   │   └── verifier_agent.py
│   │   ├── core/                 (config, model warm-loading on startup)
│   │   ├── models/                (pydantic request/response schemas)
│   │   ├── services/              (ollama_client.py, yolo_service.py, rag_index.py)
│   │   └── logs/                  (audit trail output, gitignored)
│   ├── ml_assets/
│   │   ├── yolo/                  (per-crop .pt and exported .onnx files)
│   │   ├── classifier/            (crop classifier weights)
│   │   └── rag_index/             (precomputed FAISS/Chroma index files)
│   ├── tests/
│   └── pyproject.toml (or requirements.txt)
└── scripts/
    ├── export_yolo_models.py      (batch .pt → .onnx export)
    └── build_rag_index.py         (offline index build, run once, not at request time)
```

### 5.1 Persistent architecture rule

The functional source of truth is now under `backend/app/application/`,
`backend/app/domain/`, `backend/app/ports/`, and `backend/app/infrastructure/`. The
legacy `agents/` and `services/advisory/` imports are compatibility shims only. Do not
create a second active pipeline in those directories.

---

## 6. Definition of done, per task

A task is done when:
1. It runs locally without errors (`uv run` / `pnpm dev` as applicable).
2. It matches the locked tech stack in Section 3 — no substitutions.
3. Any new dependency's version was confirmed via a fresh internet search, not assumed from memory.
4. Any new required env var is added to `.env.example` with a one-line comment.
5. A short note (commit message or a line in the relevant `README.md`) says what was built and any open questions for review.

Do not mark a task done if you had to guess at something architecturally significant — flag it instead.
