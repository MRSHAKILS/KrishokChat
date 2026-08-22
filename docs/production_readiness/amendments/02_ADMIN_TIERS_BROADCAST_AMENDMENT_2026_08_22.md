# Admin Console, User Tiers & Broadcast Announcements Amendment (APPROVED 2026-08-22)

**Date:** 2026-08-22
**Status:** APPROVED 2026-08-22 — via researcher-approved implementation plan ("KrishokChat → Government-Ready: UI Refinement + User Tiers + Admin Panel & Broadcast Alerts")
**Tier:** 1 (post-capstone, government-handoff lane)
**Depends on:** Supabase Auth amendment 15 (`paper/archive/system_evolution_plan_2026/execution_planning_2026_08_12/15_SUPABASE_AUTH_AMENDMENT_2026_08_14.md`), premium-lane design 16, P0 hardening (API versioning `/api/v1`, API keys, error envelope)
**Blocks:** admin ops console, free/premium tier management, broadcast announcements & disease alerts
**Precedent:** `14_LOCAL_MODEL_RUNTIME_AMENDMENT`, `15_SUPABASE_AUTH_AMENDMENT`, `01_PRIVACY_GOVERNANCE`

---

## 1. Decision (what this amendment approves)

Approves a bounded carve-out to AGENTS.md §2 rule 1's "no admin panel" clause for the
government-handoff lane. Specifically:

- **A single-platform admin console** at `/admin` in the existing Next.js app, for
  platform operators (starting with the researcher as sole admin). NOT multi-tenancy.
- **Free/premium user tiers** stored on `profiles` (`plan` column) with admin-set
  values. **No feature is gated by tier by default** — every existing feature stays
  available to anonymous, free, and premium users alike (researcher decision
  2026-08-22: "no gating now"). Gating may be enabled later by a future amendment
  without schema changes.
- **A `role` column** on `profiles` (`user` | `admin`) as the authorization source of
  truth (roles-table pattern, checked server-side via service-role lookup; never
  trusted from the client).
- **Broadcast announcements & disease alerts**: admin-composed Bengali notifications
  stored in Supabase Postgres, surfaced in-app (navbar bell + urgent banners on
  farmer surfaces). In-app only in this amendment; **Web Push is design-deferred**
  (Phase D) and requires no new approval to implement exactly as sketched in §5.
- **Admin action audit**: every admin mutation logged to an `admin_actions` table
  (actor, action, target, payload, timestamp) — mirrors the project's audit culture.

## 2. Rule being changed

**AGENTS.md §2 rule 1** currently reads (in part):

> "… No admin panel, no role-based multi-tenancy, no per-tenant data isolation."

**New wording (additive carve-out, effective with this amendment):**

> Authentication remains additive and optional and may never gate the demo. A
> **single-platform admin console** (`/admin`) and **per-user free/premium tier
> management** are permitted for the government-handoff lane, provided: (a) with
> `DEMO_MODE=true` or no signed-in user, every existing route and feature behaves
> exactly as before and remains fully offline-capable; (b) admin surfaces are
> role-gated server-side (fail-closed) and invisible to non-admins; (c) no feature
> is gated by tier unless a future amendment approves specific gating; (d) no
> multi-tenancy, no per-tenant data isolation, no tenant UI (T1-01 stays BLOCKED
> and separate); (e) no payment/billing code (Stripe stays deferred per design 16 §8).

## 3. Why now

- The researcher is preparing the system for handoff to a government partner
  (stated 2026-08-22). Operating a citizen-facing advisory service requires: the
  ability to broadcast disease alerts (real-world precedent: Texas A&M AgriLife
  statewide alert system; EcoFarmer Zimbabwe; USSD early-warning frameworks), manage
  user plans, and observe safety metrics — none of which is possible today.
- The auth lane (amendment 15) and premium schema groundwork (design 16) exist and
  are verified; this amendment is the minimal unlock that reuses them.
- Zero-budget constraint: everything approved here runs on the existing Supabase
  free tier and the existing two processes (one FastAPI, one Next.js). No new
  services, no paid dependencies.

## 4. What stays forbidden (invariants — do not break)

- **Demo never gates.** With `DEMO_MODE=true` or no signed-in user, every existing
  route behaves exactly as before, fully offline-capable. Notifications with
  `audience='all'` are visible to anonymous visitors (that is additive content, not
  gating); when Supabase is unreachable the notification surfaces render nothing
  and never block the page.
- **No multi-tenancy / per-tenant isolation / tenant UI.** T1-01 remains BLOCKED
  and is not implemented by this amendment. Roles are `user`/`admin` only — no
  dealer/SAAO/tenant roles.
- **No billing.** No Stripe, no payments, no paywalls (design 16 decision 2 stands).
- **No runtime index building or artifact mutation.** The admin console cannot
  rebuild the RAG index or swap vision models at runtime (AGENTS.md §2 rule 2
  unchanged). Content management beyond announcements is out of scope here.
- **Server-side fail-closed authorization.** Every `/api/v1/admin/*` route verifies
  the caller's profile `role='admin'` via the service-role key (or equivalent port
  implementation) on every request. UI guards are cosmetic only. 401/403 use the
  existing error envelope.
- **Safety pipeline, retrieval, verifier, audit log, schemas, model IDs: unchanged.**
- **No fabricated data.** Admin overview shows only real counts from real tables
  and the existing `/api/safety/metrics` endpoint. Unconfigured features show
  honest empty states, never placeholder numbers.
- **No new always-on services.** One FastAPI process, one Next.js process
  (AGENTS.md §2 rule 3 unchanged).

## 5. Scope (additive, bounded, reversible)

**Create (backend):**
- `supabase/migrations/002_roles_plans.sql` — `profiles.role`, `profiles.plan`,
  `admin_actions` table, RLS updates
- `supabase/migrations/003_notifications.sql` — `announcements`,
  `announcement_reads` tables, RLS (published rows readable by all incl. `anon`;
  writes service-role only)
- `backend/app/application/admin.py` (or equivalent) — admin profile lookup,
  user list/patch use cases, announcement CRUD/publish use cases
- `backend/app/api/admin.py` — `/api/v1/admin/users`, `/api/v1/admin/announcements`
- `backend/app/api/notifications.py` — `GET /api/notifications` (optional auth,
  audience-filtered), `POST /api/notifications/{id}/read`
- `backend/tests/test_admin_authz.py`, `backend/tests/test_notifications.py`

**Create (frontend):**
- `frontend/src/app/admin/*` route group (overview, users, announcements composer)
  with server-side role guard rendering a 404-style page for non-admins
- Notification bell component + slide-over panel; urgent-alert banner component
- Dev-only test-user switcher on `/auth` behind `NEXT_PUBLIC_DEV_USER_SWITCHER`
  (default `false`; documented as never-set-in-production)

**Modify (additive only):**
- `backend/app/api/dependencies.py` — add `require_admin` (reuses `require_user`)
- `backend/app/api/auth.py` — extend `/auth/me` response with `role`/`plan`
- `backend/app/api/qa.py` — optional `limit`/`window` params on
  `/api/safety/metrics` (response shape unchanged when omitted)
- `frontend/src/components/navbar.tsx` — bell entry (additive)
- `frontend/src/app/(app)/account/page.tsx` — plan badge
- `.env.example` — new vars with one-line comments
- `tools/ops/supabase_test_user.ps1` — provision/verify free/premium/admin test users

**Do not touch:** QA/safety pipeline, retrieval, verifier, `backend/app/agents/`,
`backend/app/services/advisory/`, demo cache lane, port signatures of existing
stores, `dataset_release/`, `paper/`.

**Deferred (Phase D, design-record only, no approval needed to build later exactly
as sketched):** Web Push (pywebpush + VAPID, `push_subscriptions` table, service
worker handler — free, no Firebase); content-library management; artifact version
viewer.

## 6. Settings — defaults are today's behavior

| Setting | Default | Meaning |
|---|---|---|
| `NEXT_PUBLIC_DEV_USER_SWITCHER` | `false` | When `true`, `/auth` shows one-click test-persona sign-in (dev/testing only) |
| `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` (backend) | unset | Already documented in `.env.example`; when unset, all admin/notification APIs return honest 503s and the demo is unchanged |
| `NOTIFICATIONS_POLL_SECONDS` (frontend) | `180` | Bell refresh cadence; offline-tolerant |

No tier-gating setting exists because **no gating ships** (researcher decision).

## 7. Revert condition

- **Config rollback:** remove backend Supabase env vars → all admin/notification
  endpoints return 503 (unconfigured), UI surfaces render nothing; demo identical.
- **Commit revert:** each phase lands as a bounded commit (`git revert` per phase).
- **Trigger:** any demo regression under `DEMO_MODE=true` / anonymous, or gate failure.

## 8. Verification gate (stop/go)

1. `uv run pytest -q` green, including new `test_admin_authz.py` (401 anonymous,
   403 non-admin, 200 admin, fail-closed when Supabase unconfigured) and
   `test_notifications.py` (audience filtering: anon→`all`, free→`all|free`,
   premium→all; read state; expiry).
2. `pnpm build` green; `/admin` route present; non-admin sees 404-style page.
3. Anonymous smoke: every existing route byte-identical (updated
   `frontend/smoke-check.js` passes desktop + 390px).
4. Live round-trip (when Supabase env set): test-admin creates announcement →
   test-free sees it in bell → mark-read persists → `admin_actions` row exists.
5. 3-server invariant after each phase (backend :8000, frontend :3000, llama :11435).

## 9. Researcher decisions recorded (2026-08-22, plan approval)

1. **Tier gating:** NONE now — tiers exist in schema, admin can set them, nothing
   is blocked for any user. (Recommended option chosen.)
2. **Notification reach:** in-app first (bell + banners); Web Push as Phase D.
3. **Admin v1 scope:** ops console only (overview, users, announcements/alerts);
   content management deferred.
4. **UI direction:** polish the existing Field Notebook design system; no visual
   refresh; no DESIGN.md regeneration needed.

## 10. Approval

- [x] **APPROVED** — 2026-08-22, via researcher approval of the implementation plan
      containing exactly this scope ("KrishokChat → Government-Ready…"). Options
      chosen are recorded in §9. Any scope growth beyond §5 requires a new
      amendment or a recorded researcher decision.

## 11. Claim boundary

This amendment approves code, not claims. The existence of an admin console does
not claim production certification; the absence of gating does not claim a
monetization strategy; notifications in-app do not claim push delivery. Government
handoff readiness claims remain governed by `docs/PRODUCTION_ROLLOUT_PLAN.md`.
