# Dependency Audit — 2026-08-17

Status: **report-only** (P0-9). No dependencies were changed by this audit;
any remediation is a separate, verified change.

## Backend (Python, `uv` lock)

Command:

    uv pip freeze | Out-File reqs.txt; uvx pip-audit -r reqs.txt --format json

- Tool: `pip-audit` (latest via `uvx`, OSV database, run 2026-08-17)
- Scope: 134 installed packages (production + dev tooling in the single venv)
- Result: **No known vulnerabilities found** (`"fixes": []`)

Notable pinned versions in the audit (all clean as of today): FastAPI 0.141.1,
Starlette 1.4.1, Pydantic 2.13.4, PyJWT 2.13.0, cryptography 50.0.0, httpx
0.28.1, torch 2.13.0, ultralytics 8.4.116, onnxruntime 1.28.0, sentence-
transformers 5.7.0, uvicorn 0.52.1.

## Frontend (npm via pnpm)

Command: `pnpm audit --prod`

- Result: **1 vulnerability (high)** — transitive, build-time only

| Package | Vulnerable | Patched | Path |
|---|---|---|---|
| nanoid | <3.3.18 | >=3.3.18 | `next > postcss > nanoid`, `shadcn > postcss > nanoid` |

Advisory: GHSA-2v37-7h3g-55p8 — "custom generators can loop indefinitely when
size is zero".

### Assessment

- The finding is **transitive via `postcss`**, a build-time toolchain
  dependency; `nanoid` is not in the runtime bundle path for the app routes.
- The described flaw (a custom `random` generator looping when `size=0` with
  `customAlphabet`) is not reachable from this application's usage.
- Neither `next` nor `shadcn` currently resolves `postcss` to a version whose
  `nanoid` range admits >=3.3.18, so a plain `pnpm update` does not clear it.

### Remediation options (NOT applied in P0-9 — tracked for Phase 1)

1. Wait for `next`/`shadcn` to widen the transitive range, then
   `pnpm update postcss nanoid` (zero-risk).
2. Add a `pnpm.overrides` entry pinning `nanoid@>=3.3.18` — verified locally
   against `pnpm build` + the 21-route smoke before commit, and re-run
   `pnpm audit --prod` to confirm zero findings.
3. Accept and re-audit at each release (documented residual risk).

## Re-run

    uvx pip-audit -r <requirements snapshot> --format json   # backend
    pnpm audit --prod                                        # frontend

Re-audit cadence: before every production cut; in CI once a job exists
(Phase 1, W-6).