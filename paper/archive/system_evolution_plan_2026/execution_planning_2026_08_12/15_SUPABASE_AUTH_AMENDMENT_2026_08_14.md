# Supabase Auth Amendment

**Date:** 2026-08-14
**Scope:** Authentication lane for future premium features (P0-P4 plan)
**Research thesis impact:** none

## Decision

Introduce Supabase Auth (hosted project + local CLI) as the authentication layer for
KrishokTech, in preparation for future premium features (user accounts, saved history,
subscriptions). This supersedes the prior "no authentication" prohibitions in:

- Root `AGENTS.md` §2 rule 1 ("No authentication, no user accounts...")
- `execution_planning_2026_08_12/AGENTS.md` rule 10 (auth prohibition)
- `paper/system_evolution_plan_2026/AGENTS.md` rule 16 (auth prohibition)

via the dated-amendment process (precedent: `14_LOCAL_MODEL_RUNTIME_AMENDMENT_2026_08_12.md`).

## Chosen Stack (verified 2026-08-14 against official registries)

| Component | Version | Verified at |
|---|---|---|
| `@supabase/supabase-js` | ^2.112.3 | npm registry (`npm view @supabase/supabase-js version` → 2.112.3) |
| `@supabase/ssr` | ^0.12.4 | npm registry (`npm view @supabase/ssr version` → 0.12.4) |
| `supabase` CLI | ^2.114.0 | npm registry (`npm view supabase version` → 2.114.0) |
| `pyjwt[crypto]` | ^2.13.0 | PyPI (`https://pypi.org/pypi/pyjwt/json` → 2.13.0) |

Node.js v24.11.0 satisfies supabase-js's Node >= 22 requirement (verified locally).
Next.js 16.3.0: `middleware.ts` is renamed `proxy.ts` (export `proxy`); the SSR
session-refresh edge file must follow that convention.

## Invariants (what this amendment does NOT change)

- **Anonymous-first.** With `DEMO_MODE=true` or no signed-in user, every existing route,
  feature, and the QA pipeline behave exactly as before. Auth is additive and optional.
  No route gating in P0-P4. The 3-4 minute investor demo runs offline with no Supabase
  dependency.
- No admin panel, no role-based multi-tenancy, no per-tenant data isolation.
- No new services: one FastAPI backend, one Next.js frontend. Stripe webhook (P4) is a
  FastAPI route, not a service.
- Safety pipeline, retrieval (BM25-only), verifier, audit log, schemas, model IDs,
  vision behavior: unchanged.
- Secrets stay out of source; `.env.example` keeps placeholders with comments.
- New env vars are added to `.env.example` (see P0 deliverables).

## P0 Deliverables (2026-08-14)

1. This amendment document.
2. Root `AGENTS.md` §2 rule 1 replacement + §3 stack table row.
3. `.env.example` Supabase section (placeholders only).
4. Frontend deps `@supabase/supabase-js@2.112.3` + `@supabase/ssr@0.12.4`.
5. Backend dep `pyjwt[crypto]`.
6. `scripts/supabase_test_user.ps1` — repeatable auto test-login script that works
   against any Supabase project URL (local CLI or hosted), enabling test account
   management now and unchanged at deployment.

## Live Verification (2026-08-14, hosted project `xhrcwsmrckfvmfxlltvk`)

Hosted path chosen (researcher provided keys). Live evidence recorded:

- GoTrue `v2.195.0` at `https://xhrcwsmrckfvmfxlltvk.supabase.co`.
- JWKS endpoint serves ES256 EC keys (backend P3 verification path confirmed).
- **Transport discovery:** with the new key system, all GoTrue calls require BOTH
  `apikey` and `Authorization: Bearer` headers. Legacy service-role JWT still
  accepted for `/auth/v1/admin/*`; publishable key (`sb_publishable_...`) accepted
  for client endpoints. Legacy anon JWT alone returns 401 (not used).
- Admin API response shape: `{"users":[...],"aud":"authenticated"}`; admin user
  update is `PUT /auth/v1/admin/users/{id}` (PATCH/POST return 405).
- Test user `test@krishoktech.com` created pre-confirmed via admin API
  (`email_confirm: true`); password grant login succeeds; `/auth/v1/user` session
  verification succeeds. Script run 3x consecutively: create path + reset path
  (idempotent password/confirmation refresh) all `TEST LOGIN SUCCEEDED` (exit 0).
- Backend: `uv run pytest` 19 passed (unchanged). Frontend: `pnpm build` clean,
  18 routes. `git status` shows only intended files; `.env.local` files ignored.
- Keys live only in gitignored `frontend/.env.local` / `backend/.env.local`.
  The `sb_secret_...` key was not required (legacy service-role JWT serves the
  admin API) and is intentionally not stored.

## Open Items

- Local Supabase CLI stack still requires Docker (not installed). Hosted project is
  now the active test target; local CLI remains optional for offline dev.
- Custom domain + brand verification remain future polish items.

## Phase Completion Record (append-only)

**P2 — Auth UI (2026-08-14):**
- `frontend/src/lib/supabase/hooks.ts` (`useSupabaseSession`), `frontend/src/components/auth/session-area.tsx`
  (login pill → account chip + sign-out dropdown; desktop + mobile rows in navbar).
- `frontend/src/app/(marketing)/auth/page.tsx` rewritten: login/register modes (`?mode=register`),
  email+password, Google button gated by `NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED`, demo entry links,
  16123 helpline footer preserved. Anonymous routes unchanged.
- Verification: `pnpm build` clean (19 routes + proxy); live Playwright E2E vs hosted project
  (12/12 checks): form render, register mode, real login → redirect `/`, account chip, sign-out,
  anonymous `/chat` + `/detect` regression.

**P3 — Backend JWT verification (2026-08-14):**
- `backend/app/ports/auth.py` (TokenVerifier protocol), `backend/app/infrastructure/auth/jwks.py`
  (lazy, cached, fail-closed ES256 JWKS verifier — no network until a token is presented),
  `backend/app/application/auth.py` (AuthService), `backend/app/api/dependencies.py`
  (optional_user / require_user deps — used by NOTHING yet; future premium endpoints only),
  `backend/app/api/auth.py` (`GET /auth/me` proof endpoint). Container + router wired.
- New env: `SUPABASE_PUBLISHABLE_KEY` (backend, public value; `.env.example` + `backend/.env.local`).
  Config additions: `supabase_url`, `supabase_publishable_key`, `supabase_service_role_key`,
  derived `supabase_jwks_url`. No new dependencies (httpx, pyjwt[crypto] already present).
- Verification: `uv run pytest` **32 passed** (was 19). New tests: 9 offline JWKS unit tests
  (local ES256 keypair: valid/garbage/tampered/expired/rotation/no-kid/wrong-alg), 3 `/auth/me`
  contract tests, and 2 LIVE integration tests — real token from hosted project verified against
  live JWKS and accepted by `/auth/me`.

**P4 — Premium groundwork, design-only (2026-08-14):**
- `16_PREMIUM_LANE_DESIGN_2026_08_14.md` delivered: data model (profiles, saved_queries,
  subscriptions), additive FastAPI surface (`/api/history`, `/api/account`,
  `/api/billing/webhook`) consuming the P3 auth deps, frontend surfaces (save button,
  `/account`), non-goals, and four open researcher decisions (ship saved history? ship
  Stripe? RLS acceptance? lazy profiles). No code, no env vars, no dependencies added.

**Remaining:** Implementation of any premium feature is contingent on researcher
decisions in `16_PREMIUM_LANE_DESIGN_2026_08_14.md` §8. Google OAuth live button still
blocked on researcher's Google Cloud Console app + dashboard provider enablement.

**Google OAuth ENABLED (2026-08-14):** researcher created the Google Cloud Console
OAuth client and enabled the provider in the Supabase dashboard with the stored
credentials. Live probe (Playwright, click Google button on `/auth`):
`authorize` returned **302** and the browser landed on
`accounts.google.com/v3/signin/identifier` — provider enabled + redirect URI
(`https://xhrcwsmrckfvmfxlltvk.supabase.co/auth/v1/callback`) correctly registered.
Credentials archived in gitignored `backend/.env.local` (`GOOGLE_OAUTH_CLIENT_ID`,
`GOOGLE_OAUTH_CLIENT_SECRET`); `.env.example` placeholders; `Settings` fields added;
`NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED=true` locally. Full sign-in with a real Google
account is a manual/researcher test (not automatable without her Google credentials).

**LIVE SAVED-HISTORY ROUND-TRIP (2026-08-14, backend restarted with current code,
migration applied by researcher):** real GoTrue password-grant token
(799 chars) → `POST /api/history` 201 (uuid row) → `GET /api/history`
count=1, id match → `DELETE /api/history/{id}` ok → `GET` count=0. Anonymous
`GET` → 401. Full auth → JWKS verify → PostgREST → hosted DB chain proven live.

**P4 — Saved history IMPLEMENTED (2026-08-14, decisions 1-4 resolved in
`16_PREMIUM_LANE_DESIGN_2026_08_14.md` §8/§10):** migration
`supabase/migrations/001_saved_history.sql` (profiles + saved_queries + RLS — NOT
yet applied, researcher action), backend `ports/saved_history.py` +
`infrastructure/storage/postgrest.py` + `application/history.py` + `api/history.py`
(`GET/POST /api/history`, `DELETE /api/history/{id}`, ownership enforced, 503 when
unconfigured; no new dependencies), frontend save button in `qa-panel.tsx` (signed-in
only) + `/account` page + "আমার হিসাব" dropdown link. Evidence: backend suite 43
passed (was 32); `pnpm build` clean (20 routes); Playwright E2E 8/8. Stripe: DEFERRED
(design-only per decision 2). Live save round-trip pending migration apply + running
backend.

## Claim Boundary

This amendment establishes that the auth layer exists, is deployment-ready by env
swap, and that a hosted test account can be created, confirmed, logged in, and
session-verified automatically (live-verified 2026-08-14). It does not establish any
research claim about authentication, user behavior, or premium features. As of the
phase completion record above, the UI surface exists (P2) and the backend consumes
tokens via `GET /auth/me` (P3); no existing demo route is gated by auth, and no
premium feature consumes the auth lane yet (P4, design-only).
