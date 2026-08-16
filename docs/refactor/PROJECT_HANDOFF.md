# KrishokChat Project Handoff

This is the short file that every future coding agent should read before modifying the
functional system. The detailed contracts live in `ARCHITECTURE.md` and the staged
execution plan lives in `REFACTOR_PLAN.md`.

## Product motive

KrishokChat is a Bangladesh-focused Bengali agricultural advisory research prototype. It
must demonstrate two real capabilities for a capstone paper/demo:

1. grounded, safety-aware Bengali agricultural Q&A;
2. an honest multimodal crop/disease advisory workflow using the supplied vision models.

The UI is replaceable. Functional behavior must not be embedded in React components.

## Source-of-truth files

| Concern | Source of truth |
|---|---|
| Non-negotiable project rules | `agents.md` |
| Paper citation policy (strict) | `docs/PAPER_POLICY.md` |
| Backend architecture and transport contracts | `docs/refactor/ARCHITECTURE.md` |
| Refactor milestones and quality gates | `docs/refactor/REFACTOR_PLAN.md` |
| Backend composition root | `backend/app/main.py` and `backend/app/application/container.py` |
| QA workflow | `backend/app/application/qa_pipeline.py` |
| Public HTTP schemas | `backend/app/models/schemas.py` |
| Vision model artifacts | `backend/ml_assets/vision/**` plus each artifact's `class_names.json`/`metadata.json` |
| Local audit trail | `backend/app/logs/` (ignored by git) |
| Active research execution plan | `paper/system_evolution_plan_2026/execution_planning_2026_08_12/` |
| Local model integration evidence | `paper/system_evolution_plan_2026/execution_planning_2026_08_12/14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md` |

## Invariants future agents must preserve

- Safety classification occurs before retrieval. Any non-`safe_agri` result stops the QA
  path and returns a canned/referral response.
- Provider/model failures fail closed. They must never become permission to answer from
  unsupported model memory.
- `/api/qa` and `/api/qa/stream` call the same application use case.
- The frontend consumes HTTP/SSE contracts; it does not own retrieval, model routing,
  safety, verification, or audit behavior.
- Vision artifacts currently report `task: classify`. Do not call them object detectors,
  invent bounding boxes, or claim localization metrics unless a real detection artifact
  is added and verified.
- Disease-treatment advice must pass through the same grounded retrieval/generation/
  verifier path whenever an advisory answer is requested.
- Every request outcome is locally auditable. Do not add external analytics or telemetry.
- Do not add auth, accounts, admin panels, queues, microservices, or live web retrieval.
- The arXiv v1 paper (`2606.29243`) is deprecated and must never be cited or quoted.
  The only authoritative KrishokChat papers are the files in `paper/done papers/`
  (`KrishokChat__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf`,
  `AgriTrust.pdf`). Never invent an arXiv ID or URL for them.

## Safe extension pattern

1. Add/modify a domain contract.
2. Add a port if an external capability is needed.
3. Implement or replace an infrastructure adapter.
4. Wire it only in `application/container.py`.
5. Keep routes thin and UI-agnostic.
6. Add a negative-path test before declaring the change complete.

## Model replacement examples

For one local model used by both stages:

```dotenv
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=my-finetuned-gemma
```

For separate intent and generation models:

```dotenv
INTENT_MODEL_NAME=my-local-safety-classifier
GENERATION_MODEL_NAME=my-local-bengali-generator
```

No route or frontend component should change for either replacement.

## Current status

- QA pipeline: modularized and tested.
- LLM replacement seam: implemented.
- Vision pipeline: modularized around the actual classification artifacts; see
  `docs/vision-pipeline/PAPER_AND_DEMO_CLAIMS.md` for evidence-safe wording.
- Benchmark endpoint: intentionally still separate; do not fabricate missing metrics.
- Visual design: intentionally deferred to the frontend/design workflow.
- Research execution: the dated execution-planning package supersedes the broader parent plan.
- Local generation: the checked-in `krishokchat.f16.gguf` is truncated and must not be
  served. The verified demo runtime uses the external Q4_K_M base plus KrishokChat LoRA via
  `scripts/start_krishokchat_local.ps1`; scientific performance remains unevaluated.
- T0-01 (SQLite foundation): done — `backend/app/infrastructure/storage/sqlite.py`
  (WAL, foreign_keys, busy_timeout 5000, idempotent `schema_migrations` runner with
  explicit per-migration transactions; no business tables yet), `SQLITE_DB_PATH` +
  `resolved_sqlite_db_path` in config, `backend/data/` gitignored, tests in
  `backend/tests/test_storage_sqlite.py`. Audit/session ports are sync, so stdlib
  sqlite3 — no new dependency.
- T0-04 (request-ID + structured logging): done — pure-ASGI `RequestIDMiddleware`
  (`backend/app/api/middleware/request_id.py`, echoes valid `X-Request-ID` else
  uuid4 hex, contextvar-backed, cleared per request), `JSONFormatter` +
  `setup_logging` (`backend/app/core/logging.py`, stdlib only, attached to
  `logging.getLogger("krishokchat")` in the lifespan), `REQUEST_ID_HEADER` +
  `LOG_LEVEL` in config + `.env.example`, tests in
  `backend/tests/test_request_id_middleware.py`. ASGI chosen over
  BaseHTTPMiddleware because the app serves SSE (`/api/qa/stream`). Full suite
  green (159 passed, 7 skipped).
- T0-08 (pytest + CI + golden gate): done — dev deps (`pytest`, `pytest-asyncio`,
  `httpx`) declared in `backend/pyproject.toml`; `backend/scripts/replay_golden.py`
  replays all 46 golden items offline (stub lane, real pipeline + BM25 index +
  verifier): 12/12 unanswerable refused, 6/6 eval-flagged carry verifier flags,
  zero exceptions; smoke suites converted (bm25 retrieval, qa pipeline, live e2e
  marked `live_llm`); `.github/workflows/ci.yml` runs backend / frontend / golden
  in parallel. Full suite 159 passed, 7 skipped; `pnpm build` green.
