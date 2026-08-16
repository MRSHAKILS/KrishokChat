# T1-03 — Deployment Kit (Container, Supervisor, Proxy, Backups)

- **Status:** BLOCKED — amendment review required (see below)
- **Tier:** 1 (post-capstone)
- **Depends on:** T0-01 (SQLite), T0-02 (audit DB), T1-02 (serving separation) — for realistic sizing
- **Blocks:** nothing (deployment readiness / market-readiness story)
- **Amendment:** REVIEW REQUIRED — must confirm the container count against AGENTS.md §2.3 ("one backend + one frontend process"). The intended shape is exactly ONE backend container + ONE frontend container + the already-sanctioned local-LLM sidecar (amendment `14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`). If more containers are needed, that is a new amendment.

## Goal

A real deployment kit: single-container Dockerfiles (backend, frontend), a supervisor config (systemd example), a Caddy reverse-proxy example with TLS, a backup script for the SQLite databases, and a health endpoint that actually probes dependencies. Nothing runs until the researcher picks a target host — this task produces the kit and proves it locally.

## Read first

- `backend/pyproject.toml` (uv-managed), `frontend/package.json` (pnpm)
- `backend/app/main.py` — current `/health` (returns static ok; must become dependency-probing)
- `backend/app/core/config.py` — env surface for containerization
- `docs/production_readiness/tasks/T1-02_model_serving_separation.md` — expected container contents (no torch in chat path)

## Invariants (do not break)

- One backend container, one frontend container, optional local-LLM sidecar (already sanctioned) — no microservices, no compose with 6 services (AGENTS.md §2.3).
- Docker is a local-development artifact here; the demo on the researcher's laptop must keep running exactly as today (`uv run` / `pnpm dev` unchanged).
- Health endpoint: 200 only when all dependencies probe OK (RAG index loaded, LLM lane reachable or stub-configured, DB writable); returns per-dependency detail. **Warning, not failure**, for optional lanes (TTS/ASR).
- No secrets in images: all env via `.env` / secrets mount; `.env.example` documents every variable used.
- Backups go to a configurable path, never into the repo.

## Design

- `backend/Dockerfile` — multi-stage: builder (uv) → runtime (python slim, non-root user); copies `backend/app`, `backend/ml_assets` (read-only), `backend/pyproject.toml`; runs the same uvicorn command as the local dev setup.
- `frontend/Dockerfile` — multi-stage: `pnpm` build → static/standalone output; runs with `NEXT_PUBLIC_*` build args documented in `.env.example` (frontend already has its own).
- `deploy/systemd/krishokchat-backend.service` + `krishokchat-frontend.service` examples; `deploy/caddy/Caddyfile` example (reverse proxy + TLS + gzip).
- `deploy/backup.sqlite.ps1` + `.sh` — `sqlite3 .backup` of audit/session DB + rotation (keep N daily copies).
- Health: extend `/health` → `/health` (summary) + `/health/deps` (detail); no auth (additive; frontend contract unchanged for other endpoints).
- README section under `deploy/README.md` — runbook: build, run, backup, restore, rollback to laptop-demo mode.

## Scope — create

- `backend/Dockerfile`, `frontend/Dockerfile`, `.dockerignore` files
- `deploy/` (systemd, Caddyfile, backup scripts, README.md)
- `backend/tests/test_health_deps.py` (health 200 when deps OK; detail lists each dep; optional lanes warn)

## Scope — modify

- `backend/app/main.py` (health endpoints only)
- `.env.example` (any new vars; document existing ones used by the kit)
- No other runtime code

## Do not touch

- QA/safety/vision/soil pipelines, ports, adapters
- `backend/app/agents/`, `backend/app/services/advisory/`
- `capstone/`, `paper/`, `dataset_release/`

## Rollback

Commit revert (bounded). Containers are additive — the laptop demo never uses them.

## Verification gate (stop/go)

1. `uv run pytest backend/tests/test_health_deps.py -v` — green.
2. `docker build` backend + frontend succeed (record image sizes in the commit).
3. `docker run` backend in demo mode → health 200, QA smoke works (stub lane, no secrets).
4. Backup script: run → SQLite backup file created; restore works on a fresh DB path.
5. Laptop demo (`uv run` + `pnpm dev`) — unchanged, verified by full smoke.

Gate fails ⇒ STOP and report exact output.

## Definition of done

Per AGENTS.md §6 + task handbook. Commit message lists open questions (host choice, TLS provider); completion line in `docs/refactor/PROJECT_HANDOFF.md`.

## Open questions

- Target host: VPS vs container host vs cloud (researcher's call; kit is host-agnostic).
- Whether the frontend uses Next standalone output or static export (verify `next.config`; standalone preferred).