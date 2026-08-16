# T0-04 — Request-ID + Structured Logging Middleware

- **Status:** DONE (2026-08-17)
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** nothing
- **Blocks:** T0-05
- **Amendment:** none required

## Goal

Add a request-ID middleware (echo an incoming `X-Request-ID`, else generate a `uuid4` hex) and structured, JSON-parseable application logging that carries the request ID. Every log line becomes greppable by one ID, which is what makes T0-05 telemetry and any future debugging possible. **No route behavior changes.**

## Read first

- `backend/app/main.py` — middleware order, lifespan, existing logging setup.
- `backend/app/core/config.py` — whether `LOG_LEVEL` or similar exists already (reuse if present).
- `backend/app/api/` — confirm no existing middleware module.
- Note the backend must stay stdlib-only for this task if possible: `contextvars` + `logging` + a small JSON formatter class. If `structlog` is chosen instead, it is a new dependency → internet version check (AGENTS.md §2.7) + `uv add`.

## Invariants (do not break)

- All existing routes and responses byte-identical except the added response header.
- Middleware must be pure pass-through for everything (no rejection, no redirects, no auth).
- uvicorn access logs untouched (or optionally mirrored through the formatter — do not alter their content).
- Demo mode and anonymous visitors unaffected (AGENTS.md §2.1).

## Design

- `backend/app/api/middleware/request_id.py`:
  - `RequestIDMiddleware(BaseHTTPMiddleware)` — or pure ASGI middleware; prefer the lighter option. Reads header `X-Request-ID` (configurable), validates it is ≤ 128 chars of `[A-Za-z0-9-]` (else regenerate — never trust client garbage), stores in a `contextvars.ContextVar`, sets the response header, clears the contextvar after response.
- `backend/app/core/logging.py`:
  - `JSONFormatter(logging.Formatter)` — emits one JSON object per record: `ts`, `level`, `logger`, `msg`, `request_id` (from the contextvar), plus any extra kwargs.
  - `setup_logging(level)` — attaches the formatter to the app logger (`logging.getLogger("krishokchat")`), called in the lifespan.
- Config: `REQUEST_ID_HEADER` default `X-Request-ID`; `LOG_LEVEL` default `INFO` (add only if absent).
- `.env.example` entries with one-line comments.

## Scope — create

- `backend/app/api/middleware/__init__.py` + `request_id.py`
- `backend/app/core/logging.py`
- `backend/tests/test_request_id_middleware.py` (via `TestClient`: header echoed when provided; generated when absent; malformed header regenerated; log records captured by a `caplog`-style handler contain `request_id`)

## Scope — modify

- `backend/app/main.py` (register middleware; call `setup_logging` in lifespan — two small, clearly commented blocks)
- `backend/app/core/config.py` (settings, only if missing)
- `.env.example`

## Do not touch

- Any route handler, any application-layer service, the safety pipeline
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`, `frontend/`

## Rollback

Single bounded commit revert (`git revert <commit>`). If you must revert fast without git: remove the middleware registration lines from `main.py` — they are the only functional change.

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_request_id_middleware.py -v` — green.
2. Manual: `curl -i -H "X-Request-ID: abc-123" <qa endpoint>` → response contains `X-Request-ID: abc-123`; request without header → generated ID echoed.
3. Console log for one request is a single JSON line containing `"request_id"`.
4. Full smoke of QA + classify + benchmark + safety metrics — all responses identical to before (diff against a pre-change capture if you made one).
5. `uv run python -m compileall -q backend/app` — clean.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. `.env.example` updated; commit message notes open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- BaseHTTPMiddleware vs pure ASGI (resolve by reading how the app is built; keep it minimal).
- Whether `LOG_LEVEL` already exists in settings (reuse or add).