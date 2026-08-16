# T0-07 — API Versioning + API Keys + Rate Limits + Pagination

- **Status:** NOT STARTED
- **Tier:** 0 (demo-safe, pre-capstone)
- **Depends on:** nothing (pairs naturally with T0-02's DB; keys may be stored in SQLite once T0-01 exists)
- **Blocks:** nothing
- **Amendment:** none required — MUST remain additive and default-off so the demo is untouched (AGENTS.md §2.1)

## Goal

Three additive API capabilities: (1) a versioned `/api/v1/*` surface that mirrors every existing route, leaving old paths as compatibility aliases; (2) optional API-key auth + per-key rate limiting, **disabled by default** so anonymous demo traffic is identical; (3) optional pagination on history/audit endpoints with defaults equal to today's full behavior. This is the groundwork for the API-licensing lane of the business model.

## Read first

- `backend/app/main.py` — enumerate every router mounted under `/api/*` (qa, classify, detect, benchmark, safety, history, audit, speech, tts, auth — whatever exists today).
- `backend/app/api/` — each router's routes; note which return lists (history/audit) that would benefit from pagination.
- `backend/app/core/config.py` — settings style.
- `backend/app/application/container.py` — dependency wiring (keys can be validated via a FastAPI dependency).

## Invariants (do not break)

- Every existing path, payload, and response stays **byte-identical**.
- Demo mode / anonymous visitors: no redirects, no popups, no 401s, no degradation (AGENTS.md §2.1) — enforced by default-off switches.
- Rate limiting must be a simple in-memory sliding-window (stdlib only) — no new dependency unless justified; if a package is chosen (e.g. `slowapi`), internet version check (AGENTS.md §2.7) + `uv add`.
- Keys are never logged in full; logs carry a key label/hash only.
- No secrets in source; keys come from env or the SQLite store (T0-01+), never hardcoded.

## Design

- **Versioning:** in `main.py`, add `include_router(router, prefix="/api/v1")` for the same router objects already mounted at their current paths (e.g. `/api/v1/qa`, `/api/v1/classify`, `/api/v1/benchmark/stats`, `/api/v1/safety/metrics`, ...). Both surfaces work; document `/api/v1` as the stable contract in a short comment. No route code changes.
- **API keys:** settings `API_KEY_ENABLED=false` (default) + `API_KEYS` (comma-separated literal for demo/testing) — the SQLite-backed store (keys table, migration v4) becomes the source when `API_KEYS_DB=true` and T0-01 exists. A FastAPI dependency (`require_api_key`) applies only to v1 routes; returns 401 with `WWW-Authenticate` on failure. Key label recorded on audit records (nullable field — see T0-05).
- **Rate limits:** `RATE_LIMIT_PER_MINUTE` default `60` per key (and per IP for anonymous when `RATE_LIMIT_ANON_ENABLED=false` — default off). In-memory sliding window; 429 response with `Retry-After`.
- **Pagination:** on history/audit list endpoints only: `page` (1-based, default 1) + `page_size` (default = current full behavior; e.g. `page_size=0` or a high default that returns everything so existing clients see no change). Response gains `total` count; existing fields unchanged.

## Scope — create

- `backend/app/api/middleware/api_key.py` (dependency + rate limiter) — or `backend/app/api/deps.py` if a deps module exists; follow repo layout
- `backend/tests/test_api_versioning_keys_ratelimit.py` (aliases identical; v1 routes respond; keys enabled → no key = 401, bad key = 401, over-limit = 429; anonymous defaults unaffected; pagination returns same total)

## Scope — modify

- `backend/app/main.py` (v1 mounts — additive block with comment)
- history/audit router files (pagination params only)
- `backend/app/core/config.py` (new settings)
- `.env.example`

## Do not touch

- Route logic inside qa/classify/detect/benchmark/safety/speech/tts
- The safety pipeline, orchestration, ports
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`, `frontend/`

## Rollback

1. Config rollback: `API_KEY_ENABLED=false`, `RATE_LIMIT_ANON_ENABLED=false` → anonymous demo identical.
2. Commit revert: `git revert <commit>`.

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_api_versioning_keys_ratelimit.py -v` — green.
2. Manual: every old path returns the exact same body as before (spot-check all routers); `/api/v1/*` equivalents match.
3. With keys enabled: no key → 401; wrong key → 401; correct key → 200; 61 requests/min → 429 on the 61st.
4. Pagination: `page=1&page_size=10` on history returns 10 + correct `total`; default call returns the full list (identical to today).
5. Defaults: fresh `.env` with no new vars → demo works exactly as before.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. `.env.example` updated; commit message notes open questions; completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Which endpoints currently return unbounded lists (enumerate in `Read first`; paginate only those).
- Whether the DB-backed key store ships now (T0-01) or env-only keys first (acceptable — DB store is a follow-up; document the decision).