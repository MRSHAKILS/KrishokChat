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
- T0-02 (audit → SQLite adapter): done — `AuditSqliteSink` (`backend/app/infrastructure/audit/sqlite.py`)
  stores every record in the T0-01 SQLite DB (`audit_records`, migration v2
  registered on the adapter's own MIGRATIONS list — the shared T0-01 list stays
  empty per its test — plus idempotent indexes via `ensure_schema`) and mirrors
  each line to the JSONL path `/api/safety/metrics` reads, so metrics are
  identical under both backends without touching the route. `AUDIT_BACKEND=jsonl|sqlite`
  (default jsonl) in config + `.env.example`; container switch in
  `application/container.py`. Backfill `backend/scripts/backfill_audit_jsonl_to_sqlite.py`
  is idempotent via a UNIQUE (timestamp, query_hash) index; `--force` reloads.
  Full suite 170 passed, 7 skipped. Open question: the sqlite sink's JSONL mirror
  is required only because the metrics endpoint reads `audit.path` directly — a
  future route refactor could read the DB instead and drop the mirror.
- T0-03 (sessions → SQLite adapter): done — `SqliteSessionStore`
  (`backend/app/infrastructure/sessions/sqlite.py`) implements the exact
  SessionStore port (`get` + `append`) with memory-adapter-identical
  semantics: `{"role","content"}` message lists capped at `max_turns * 2`,
  TTL strictly `>` on read AND write, refreshed on `append` only, `get`
  returns a fresh list. Rows live in the T0-01 DB (`sessions` table,
  migration v3 on the adapter's own MIGRATIONS list; `last_active_at` index
  via idempotent `CREATE INDEX IF NOT EXISTS` on first connection, same
  pattern as T0-02's `ensure_schema`). Cleanup is lazy: purge on init and on
  every get/append — no threads. `SESSION_BACKEND=memory|sqlite` (default
  memory) in config + `.env.example`; container switch in
  `application/container.py`, separate block beside the audit switch. Tests
  in `backend/tests/test_session_sqlite.py` (14) incl. restart persistence
  over the same DB file and an HTTP-level restart simulation via TestClient.
  Full suite 184 passed, 7 skipped.
- T0-05 (stage latency + token/cost telemetry in audit records): done —
  `backend/app/application/telemetry.py` (new: `stage_timer` context manager
  over the four stage keys, `capture_tokens`/`serving_provider` lane
  conventions, `estimate_cost` — always null, no price table exists
  anywhere, `current_request_id` from the T0-04 contextvar); the four stages
  in `qa_pipeline.py` are wrapped (not edited) and `_audit` now emits the
  optional `stage_timings_ms` / `tokens` / `provider` / `cost_estimate` /
  `request_id` fields; jsonl serializes them additively; the sqlite adapter
  fills its reserved columns (with `tokens` mapped onto the reserved
  `token_usage` column; `cost_estimate` lives in `record_json` only — no
  migration added, T0-02's `versions == [2]` test locks MIGRATIONS). Today
  NO LLM lane exposes usage/provider (adapters discard them;
  `infrastructure/llm/` is T0-06's scope), so `tokens` is null in production
  and `provider` falls back to the configured `LLM_PROVIDER`; the local
  registry lane may mislabel until a per-lane `provider` attribute lands.
  Tests in `backend/tests/test_audit_telemetry.py` (12). Full suite 196
  passed, 7 skipped; golden replay 46/46 invariants PASS.
- T0-06 (provider failover chain + circuit breaker): done —
  `backend/app/infrastructure/llm/failover.py` (`CircuitBreaker` —
  trips after `max_failures` consecutive failures, probe after cooldown,
  resets on success; `FailoverLLMClient` — same LLMClient port as every
  adapter, ordered `(provider_name, client, breaker)` entries, skips
  tripped breakers, falls to next on failure, `AllProvidersFailed(LLMError)`
  when all fail so the app's existing fail-closed path (safety →
  LOW_CONFIDENCE, generation → referral) applies unchanged; `provider`
  attribute feeds T0-05 `serving_provider`). `LLM_FAILOVER_CHAIN`
  (comma-separated fallback order; "auto" is never a chain entry),
  `LLM_CIRCUIT_MAX_FAILURES=3`, `LLM_CIRCUIT_COOLDOWN_SECONDS=30` in
  config + `.env.example`. Container wraps generation + rewrite lane only
  when the chain has ≥2 valid providers (lazy import; unknown names are
  warned and skipped, never a startup crash); the safety classifier keeps
  its direct factory client, never part of the chain. Open question: the
  wrapper sets `name`/`provider` to the last-serving client, so audit
  `model` reflects the provider that actually answered — the local
  registry lane still reports the global configured provider. Full suite
  216 passed, 7 skipped.
- T0-07 (API versioning + API keys + rate limits + pagination): done —
  every router under `/api/*` is mirrored under `/api/v1/*` (stable
  contract; legacy paths are byte-identical compatibility aliases) via
  `_mount_v1` in `main.py` (FastAPI cannot prefix-rewrite absolute paths,
  so each APIRoute is re-registered with the `/api` segment replaced).
  Optional guard `backend/app/api/middleware/api_key.py`: `require_api_key`
  (Bearer or X-API-Key; 401 + WWW-Authenticate; constant-time compare;
  label `env-key-<n>` + sha256 hash logged, never the key) and `rate_limit`
  (stdlib `SlidingWindowRateLimiter`, per-key or per-anonymous-IP, 429 +
  Retry-After) attach ONLY to the v1 mounts via per-include dependencies.
  `API_KEY_ENABLED=false`, `API_KEYS=` (comma-separated env literal — the
  SQLite-backed key store is a documented follow-up), `RATE_LIMIT_PER_MINUTE=60`,
  `RATE_LIMIT_ANON_ENABLED=false` in config + `.env.example`; both switches
  off = limiter pass-through, anonymous demo untouched. Pagination on
  `/api/history` GET only (the sole list endpoint; no audit list route
  exists): `page` (1-based, default 1) + `page_size` (default 0 = full list,
  identical to today) + additive `total`. Tests in
  `backend/tests/test_api_versioning_keys_ratelimit.py` (30). Full suite
  246 passed, 7 skipped. Open questions: key label is stashed on
  `request.state` but not yet written into audit records (T0-05 emit lives
  in qa_pipeline.py — out of this task's scope); `RATE_LIMIT_ANON_ENABLED`
  is opt-in only (spec wording "=false — default off" read as the default).
