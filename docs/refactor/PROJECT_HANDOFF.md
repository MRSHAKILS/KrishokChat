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
| Active research execution plan | `paper/archive/system_evolution_plan_2026/execution_planning_2026_08_12/` (moved to `archive/` 2026-08-21) |
| Local model integration evidence | `paper/archive/system_evolution_plan_2026/execution_planning_2026_08_12/14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md` |

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
- Auth/accounts and a single-platform admin console are permitted only under their
  approved amendments (15 — Supabase Auth; 02 — Admin/Tiers/Broadcast,
  `docs/production_readiness/amendments/`). Auth stays additive and never gates the
  demo; no multi-tenancy, no per-tenant isolation, no billing. Do not add queues,
  microservices, or live web retrieval.
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
- Phase 0 (production hardening, `docs/PRODUCTION_ROLLOUT_PLAN.md`): done —
  P0-1 `/readyz` (informational by default; `READINESS_STRICT=true` → 503;
  local file/dir probes only, `_dir_writable_or_creatable` accepts lazy
  SQLite dirs; `backend/tests/test_health_readiness.py`); P0-2 SSE keep-alive
  (`SSE_HEARTBEAT_SECONDS=15.0`, `: keepalive` comment on silence,
  `backend/tests/test_sse_heartbeat.py`); P0-3 uniform 500 envelope
  (`{"error","request_id","detail"}`, tracebacks to JSON logs only; request
  ID survives via ASGI scope state because ServerErrorMiddleware runs
  outside the request-ID middleware and its 500 bypasses the middleware's
  send wrapper, so the handler echoes the header itself;
  `backend/tests/test_exception_envelope.py`); P0-4 `.env.example` sync +
  advisory bootstrap checks (`core/bootstrap_checks.py`, warnings only,
  never fails boot; `backend/tests/test_bootstrap_checks.py`); P0-5
  `DOCS_ENABLED=false` hides docs routes; P0-6 local-lane concurrency guard
  (lazy `asyncio.Semaphore`, `LOCAL_LLM_MAX_CONCURRENCY=2` 1..16, wait-queued
  not 429, no-op for non-local lanes; `backend/tests/test_local_lane_concurrency.py`);
  P0-7 `CORPUS_VERSION` in demo-cache keys (bump after index rebuild);
  P0-8 frontend security headers (no custom Cache-Control — Next 16 serves
  its own immutable static headers; verified live on dev server); P0-9
  dependency audit report (backend: 0 vulns/134 pkgs; frontend: 1 high
  transitive build-time `nanoid` via postcss — unreachable, remediation
  tracked for Phase 1); P0-10 golden set extended to 50 items with 4
  prompt-injection cases (`golden_category=injection`, recorded
  `prompt_injection` categories, terminal-refusal invariants in
  `replay_golden.py`; `scripts/extend_golden_injection.py` one-shot adder);
  P0-11 no-op with justification (all 10 `print()` live in legacy CLI
  build/smoke scripts under `services/advisory/`; request-path code is
  logger-only); P0-12 `scripts/start_prod.ps1` (uvicorn `--proxy-headers
  --timeout-graceful-shutdown 30 --limit-concurrency 32` + `pnpm start`,
   never kills existing listeners) + `logrotate.krishokchat` sample + README
   production section; P0-13 `docs/production_readiness/retention_policy.md`
   (`AUDIT_RETENTION_DAYS=90`; app never auto-deletes; operator runbooks);
   P0-14 this entry. Full suite 273 passed, 7 skipped, 79 subtests; golden
   replay 50/50 invariants PASS; `pnpm build` clean (21 routes). Open
   questions: user's live demo backend on :8000 predates P0 code (changes
   take effect on next restart); llama-server on :11435 still running from
   the model-selector verification; `nanoid` override decision (Phase 1 W-6);
   `READINESS_STRICT` remains default-off.
- T1-04 (privacy, retention, licensing): done — `backend/app/core/redaction.py`
  (BD phone `+880`/`01` + Bengali digits `০-৯`, email, name-adjacent
  `নাম:`/`name:` — best-effort regex, never claimed perfect) + 14-test
  `backend/tests/test_redaction.py` (Bengali digits covered); SQLite audit
  `purge_expired_audit` + `AuditSqliteSink` startup + on-write `DELETE WHERE
  timestamp < now() - AUDIT_RETENTION_DAYS` when >0 (bounded, no thread) +
  `JSONLAuditSink` prune on startup + `SqliteSessionStore` retention cut-off for
  `SESSION_RETENTION_DAYS`; `qa_pipeline._audit` write-time hook (stored query +
  retrieval_query_used) gated by `PII_REDACTION_ENABLED`; config
  `AUDIT_RETENTION_DAYS=0` (keep forever, default off), `SESSION_RETENTION_DAYS=30`,
  `PII_REDACTION_ENABLED=false` in `config.py` + `.env.example` (reversible);
  `frontend/src/app/privacy/page.tsx` static bilingual policy + footer link;
  `LICENSE` MIT (code) + `pyproject.toml`/`package.json` license metadata;
  `deploy/DPA_template.md` plain-language B2B DPA (what data, purpose,
  retention, deletion, subprocessors: none). `pnpm build` green (22 routes incl.
  `/privacy`); `uv run pytest` 296 passed, 7 skipped (2 pre-existing soil/SSE
  failures excluded) + 14 redaction green; retention purge verified (1 day
  correctly deletes old row); live QA with redaction on scrubs stored query;
  golden replay 50/50 PASS; `/health` + `/readyz` + `/privacy` 200. Demo
  identical with defaults. Rollback: config flip or `git revert`.
- G0–G9 (government-handoff lane, amendment
  `docs/production_readiness/amendments/02_ADMIN_TIERS_BROADCAST_AMENDMENT_2026_08_22.md`):
  done — farmer-UI refinement (de-English farmer surfaces incl. eyebrows,
  tracking-* removed from Bengali nodes, 9/10/11px→12px floor across 26
  farmer-facing files, offline-aware read-aloud error chip, mobile-visible
  login pill + avatar chip, desktop 16123 navbar pill, reproducible PWA icons
  `frontend/scripts/generate_pwa_icons.py` + manifest 192/512 maskable,
  landing stats + ModelComparisonInspector lazy-loaded, smoke-check.js
  un-staled to assert OPTIONAL auth); free/premium tiers with NO gating
  (researcher decision 2026-08-22): migration `002_roles_plans.sql`
  (profiles.role/plan + `is_admin()` SECURITY DEFINER + `admin_actions` +
  updated_at trigger), `require_admin` dependency (fail-closed 401/403/503,
  service-role profile lookup per request), `/api/account` + `/auth/me`
  profile, admin users list/patch (audited); broadcast notifications:
  migration `003_notifications.sql` (announcements + reads; published rows
  readable by anon), `/api/notifications` audience-scoped (anon→all,
  free→all|free, premium→all), read state (server for signed-in,
  localStorage anon), admin announcements CRUD/publish (audited);
  `/admin` console (server guard → Bengali 404-style page for non-admins —
  HTTP 200 with not-found UI due to streamed-layout notFound(), real
  enforcement is the 401/403 on every admin API): ওভারভিউ (live safety
  metrics + user/plan counts + audit trail), ব্যবহারকারী (search/pagination/
  confirm-changes), ঘোষণা ও সতর্কতা (composer + live farmer-view preview);
  navbar bell + urgent banners on /detect+/chat (render nothing when lane
  disabled); dev persona switcher on /auth behind
  `NEXT_PUBLIC_DEV_USER_SWITCHER` (default false) + `-Personas` mode in
  `tools/ops/supabase_test_user.ps1`. Tests: +36 (22 admin authz + 14
  notifications) green; suite 272 passed (test_soil analyze-locked fails
  identically on clean HEAD — pre-existing, already documented above);
  golden replay 50/50 PASS; `pnpm build` green (24 routes); anonymous
  smoke 1440px+390px PASSED; 3-server probe: backend/frontend up, llama
  lane not running (optional). Researcher actions outstanding: apply
  migrations 002+003 to the hosted project, run `-Personas` with the
  service-role key, set backend `SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY`
  in `backend/.env.local` (auth lane inert without them), visually review
  `/admin` as the admin persona.
- F1-01 (BD-grounded banned-chemical registry, first task of the
  `production/future_plan/00_SCOPE_OUTLINE.md` §10 "Safety" node): done —
  `backend/app/domain/chemical_registry.py` (15 source-attributed
  `BannedActive` records, EN `\b`-bounded + distinctive Bengali aliases,
  stable `banned_active:<name>:<en|bn>` audit tags feeding `matched_rules`);
  `safety_policy.py` now composes `BANNED_OR_RESTRICTED_CHEMICAL` from
  `compiled_banned_patterns()` + generic Bengali catch-alls — `precheck`
  ordering, canned texts, and coverage gate untouched. Scope: legally
  cancelled/banned actives only (chlorpyrifos & other still-registered HHPs
  deliberately not blocked — nuanced HHP handling is a later verifier task).
  Verified: targeted 23+413 subtests green; `tests/` suite 337 passed /
  7 skipped / 2 pre-existing env failures (auth JWKS, soil — both documented);
  golden replay 50/50 PASS; spot-check 10 new actives EN+BN flagged, 16/16
  ordinary queries clean. Pre-existing found: `test_sse_heartbeat.py
  ::test_keepalive_comment_during_silence` hangs indefinitely in this
  environment — deselect it in local runs; candidate quick-fix follow-up.
  The `production/future_plan/` planning package (7 docs) is research-only;
  nothing in it changes code until a task executes it.
- F1-02 (corpus-derived registered-dose reference for the verifier): done —
  `backend/app/infrastructure/verification/dose_reference.py` + thin CLI
  `backend/scripts/build_dose_reference.py` + committed artifact
  `ml_assets/rag_index/derived/dose_reference_v1.json` (71 cited entries,
  15 actives, extracted offline from DAE registered-pesticide pages + BARC
  hand book nodes; deterministic; no fabricated data). `HardenedDosageVerifier`
  takes an optional `dose_reference`: a dosage claim that passes passage
  entailment but exceeds the referenced band max by ≥ `DOSE_OUTLIER_FACTOR`
  (default 3.0, same unit, explicit per-litre/per-hectare context; একর ≠ ha)
  becomes unsupported → flag naming active+amount+referenced max, and the
  sentence is annotate-and-dropped. Default-constructed verifier behavior is
  byte-identical to pre-F1-02. `DOSE_REFERENCE_PATH` +
  `dose_reference_resolved_path` in config + `.env.example`; missing file ⇒
  warning + disabled (demo can never break). Known caveat: a few proximity
  misbindings in table text inflate band maxima only (fail-safe direction),
  every entry auditable via snippet+citation. Verified:
  `tests/test_dose_reference.py` 20 green; suite 358 passed / 7 skipped /
  2 pre-existing env failures; golden replay 50/50 PASS with unchanged flag
  counts. This is the N1 verifier-side piece F1-01 deferred.
- PR1 (weather-triggered potato late-blight risk alert, spine step 3): done —
  `backend/app/domain/late_blight.py` (Smith-period approximation on daily
  aggregates: tmin ≥10°C + RH ≥85% on ≥2 consecutive days = high, 1 = watch;
  season window Nov 1–Mar 15 derived from the snapshot's own latest date),
  `backend/app/infrastructure/weather/snapshot.py` (fail-open loader),
  committed SAMPLE snapshot `ml_assets/weather/late_blight_snapshot.json`
  (8 potato districts, is_sample: true, 5 high / 1 watch / 2 low),
  `GET /api/admin/advisory/late-blight-risk` (require_admin; risk-ordered
  payload + per-district composer prefill; missing snapshot → available:
  false, never 500), `WEATHER_SNAPSHOT_PATH` in config + `.env.example`.
  `/admin/announcements` gained an "আবহাওয়া ঝুঁকি" card with sample badge and
  one-click composer prefill — human-in-the-loop publish via the audited
  announcements lane unchanged. The drafted advisory cites CABI corpus nodes
  and deliberately carries NO fungicide dose (dose advice stays in the F1-02
  QA lane / 16123). Researcher outstanding: replace the sample snapshot with
  real BMD/BAMIS rows before any real broadcast. Verified: 18 new tests;
  suite 376 passed / 7 skipped / 2 pre-existing env failures; golden 50/50
  PASS; pnpm build green; live anon 401 on both /api and /api/v1 mounts.
- F4 (Bengali font optimization): done — dropped the Noto Serif Bengali
  family (3 weight files) that sat behind Tiro Bangla in the display fallback
  chain and never rendered; `adjustFontFallback: false` on the remaining two
  families (the automatic Times/Arial metric adjustment is meaningless for
  Bengali and adds swap-time layout shift); display chain now Tiro →
  "Tiro Bangla" → Georgia. Visual output identical when fonts load (serif
  never rendered), 3 fewer font downloads on rural 3G. `pnpm build` green,
  no dangling references.
- P1+P2 (farm profile + stage-aware advice, spine step 4; task doc
  `docs/production_readiness/tasks/P1_P2_farm_profile_stage_advice.md`):
  done — migration `004_farm_profiles.sql` (owner-only RLS, service-role
  writes from the backend); data-driven crop-stage calendars
  (`domain/crop_calendar.py` calculator + `infrastructure/agronomy/
  calendar_store.py` fail-open loader + committed artifact
  `ml_assets/agronomy/crop_calendars_v1.json`, built offline by
  `scripts/build_crop_calendars.py` from `curated_calendars_v1.json`;
  adding a crop = edit curated JSON + re-run builder, NO code changes —
  test-locked); `application/farm_profile.py`
  (PostgREST store, PII-redacted free text, honest `available: false` when
  unconfigured); `GET/PUT /api/account/farm-profile`; optional
  `farmer_context` threaded `schemas → QAInput → QueryContext → prompt`
  (stage line appears ONLY when present — anonymous prompts byte-identical,
  regression-locked); frontend `/account` profile form + stage card
  ("আনুমানিক" badge on approximations) + chat auto-attach via
  `streamQuestion({ farmerContext })`. `CROP_CALENDARS_PATH` in config +
  `.env.example`. Researcher action: apply migration 004 (DONE 2026-08-25,
  verified via PostgREST schema probe). Full suite 410 passed / 7 skipped /
  0 failed.
- Soil honesty fix + hermetic auth contract test (2026-08-25): commit
  eb0d4eb had rewritten `SoilService.analyze()` into a filename-substring
  fake that diagnosed ANY uploaded image with hardcoded kPa/soil-type values
  (rule 5 violation), and its demo flow even sent Bengali button labels as
  filenames so all three samples fell into one default branch. Fixed:
  `analyze()` now REPLAYS known sample records only (image ID regex
  `[Pp]\d{4}(?!\d)` matched against `info.samples` loaded from the frozen
  `samples_manifest.json` — every value from the release package, nothing
  hardcoded); unknown images get the honest locked response again;
  replay results carry `sample_id` (new optional schema field) and
  `confidence=None` (a measurement has no model confidence);
  `soil/page.tsx` keeps the real dataset filename on sample upload;
  `soil-locked-card.tsx` badges replays as "ডেটাসেট নমুনা <ID> · পরিমাপিত"
  and drops fabricated fallbacks (`?? 8.0`, `?? 94%`). Separately,
  `test_auth.py::test_me_with_valid_token_returns_claims` leaked its
  fabricated sub into the live profiles table once `.env.local` gained real
  credentials — `_client_with_verifier` now injects an unconfigured
  `AdminService(store=None)` so the contract test is offline by design, and
  `/auth/me` catches `httpx.HTTPError` around the profile lookup (identity
  endpoint must never 500 on a store outage). Both failures were pre-existing
  on clean HEAD before this session's P1+P2 work (verified by stash). Full
  suite 410 passed / 7 skipped / 0 failed; `pnpm build` green.
