# Premium Features Lane — Design Document (P4)

**Date:** 2026-08-14
**Scope:** Design-only groundwork for the premium lane (P4 of the P0-P4 Supabase Auth plan)
**Research thesis impact:** none
**Implementation status:** DESIGN ONLY — no code changes. Nothing here is built yet.

## 1. Purpose

Amendment 15 built the auth lane (P0-P3). This document defines *how* future premium
features will consume it, so that when the researcher approves any feature, the
implementation is mechanical. Per amendment 15:

- **No route gating in P0-P4.** Every existing route, the QA pipeline, and the offline
  investor demo keep working with `DEMO_MODE=true` or no signed-in user.
- **No new services.** Stripe integration (if approved) is a FastAPI route + httpx calls,
  not a service. One backend, one frontend.
- **No admin panel, no role-based multi-tenancy.** Premium features are per-user additive
  surfaces only.
- Safety pipeline, retrieval (BM25-only), verifier, audit log, schemas, model IDs,
  vision behavior: unchanged.

## 2. Candidate premium features (in priority order)

| Feature | Auth consumption (built in P3) | Build cost | Demo value | Decision needed |
|---|---|---|---|---|
| **Saved query history** | `require_user` on `/api/history/*`; `optional_user` in chat UI | Low (2 tables, 3 routes, 1 UI surface) | Medium — real personalization story | Ship? (recommended: yes, if any premium work ships) |
| **Subscriptions (Stripe)** | `require_user` on billing/account routes; signed webhook | Medium (Stripe test mode + webhook + 1 table) | Low for a 3-4 min demo; high credibility as "future roadmap" | Ship now or design-only? (recommended: defer) |
| **Saved history sync across devices** | Automatic via Supabase (server-side storage) | Zero extra work beyond #1 | Low | N/A |

Recommendation: implement **saved history** as the first (and only, for the demo) premium
feature if any code ships; keep subscriptions as an approved design.

## 3. Data model (Supabase Postgres)

All tables live in the existing hosted project `xhrcwsmrckfvmfxlltvk` (or a future
project at deployment — schema is env-agnostic).

### 3.1 `profiles`

| column | type | notes |
|---|---|---|
| `id` | uuid PK | `references auth.users(id) on delete cascade` — no separate user table |
| `email` | text | copied from auth on first use (display only) |
| `display_name` | text nullable | user-set; never fabricated |
| `created_at` | timestamptz default now() | |

Row is created **lazily** on first authenticated API call (no DB trigger, no auth hook).

### 3.2 `saved_queries`

| column | type | notes |
|---|---|---|
| `id` | uuid PK default `gen_random_uuid()` | |
| `user_id` | uuid not null | `references auth.users(id) on delete cascade` |
| `query_text` | text not null | the user's own question |
| `answer_text` | text not null | the assistant answer as streamed |
| `sources` | jsonb | retrieved source IDs / metadata snapshot |
| `category` | text | safety category of the query (from the existing safety agent) |
| `created_at` | timestamptz default now() | |

**RLS note:** enable row-level security with a single policy
`user_id = auth.uid()` (select/insert/delete for owner). This is per-user data
isolation inherent to "saved history" — it is NOT per-tenant/org isolation, which
remains out of scope (amendment 15 §Invariants).

### 3.3 `subscriptions` (only if Stripe ships)

| column | type | notes |
|---|---|---|
| `id` | uuid PK default `gen_random_uuid()` | |
| `user_id` | uuid not null unique | `references auth.users(id)` |
| `stripe_customer_id` | text unique | from Stripe Checkout |
| `stripe_subscription_id` | text unique | from webhook |
| `status` | text | `trialing / active / past_due / canceled / unpaid` |
| `plan` | text | `demo` placeholder — no invented pricing |
| `current_period_end` | timestamptz nullable | webhook-updated |

## 4. API surface (FastAPI, additive)

All routes below are **new**; none modify existing endpoints.

| Method + path | Auth | Behavior |
|---|---|---|
| `GET /api/history` | `require_user` | list current user's saved queries, newest first |
| `POST /api/history` | `require_user` | save `{query_text, answer_text, sources, category}`; returns row |
| `DELETE /api/history/{id}` | `require_user` | delete own row; 404 if not owner |
| `GET /api/account` | `require_user` | profile + subscription status (e.g., `{"plan": "free"}`) |
| `POST /api/billing/webhook` | none (Stripe signature) | verifies `Stripe-Signature` with webhook secret; updates `subscriptions` |

Implementation notes:
- New router file `backend/app/api/history.py` (+ optional `billing.py`), registered in
  `main.py` exactly like `auth.py`. Dependencies imported from
  `app/api/dependencies.py` (P3).
- Ownership check: `DELETE` loads row by `id` and asserts `row.user_id == claims["sub"]`.
- Webhook body must be consumed as `bytes` (raw) for signature verification; signature
  verification with `stripe` lib would be a NEW dependency — see §6.

## 5. Frontend surface (additive, never blocking)

- **Chat save button**: in the chat page, a small "সংরক্ষণ" (save) action appears on
  completed answers **only when signed in** (`useSupabaseSession`, P2). Anonymous
  visitors see no button — the demo is unchanged.
- **History page** `/account` (new route): lists saved queries, delete buttons, and
  shows login state. Anonymous visitors see a login CTA (link to `/auth`), never a
  redirect.
- **Upgrade prompt**: NOT built. If subscriptions ship, a single "premium coming soon"
  card may appear on `/account` — no modals, no popups (amendment 15 invariant).

## 6. Dependency & environment impact (IF Stripe ships)

- New Python dep would be `stripe` (version verified via PyPI at implementation time,
  per AGENTS.md §2 rule 7) OR raw httpx signature verification using
  `stripe`'s published HMAC scheme (avoid new dep — preferred for this prototype).
- New env vars (placeholders in `.env.example` at implementation time):
  `STRIPE_SECRET_KEY` (test mode), `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_ID`.
  No secret ever in source; local files remain gitignored.
- Saved history alone needs **zero** new env vars and **zero** new dependencies.

## 7. Explicit non-goals (P4 and beyond)

- No route gating, no paywalls on existing features, no demo-mode changes.
- No admin panel, no orgs/workspaces, no roles beyond `authenticated`.
- No billing without explicit researcher approval (payments have legal/compliance
  weight; the demo does not need them).
- No changes to safety, retrieval, verifier, vision, audit, or model wiring.

## 8. Open decisions (researcher review required)

1. **Ship saved history?** Recommended yes — it is the only feature that adds real
   user value and costs nothing to demo. Requires: run the two `CREATE TABLE` +
   RLS statements in the hosted project (or accept a Supabase migration file).
2. **Ship Stripe now or defer?** Recommended defer — this doc plus amendment 15 is the
   design record; enabling payments is a product/business decision.
3. **RLS acceptance:** confirm per-user RLS policies (see §3.2 note) are acceptable.
4. **Profile laziness:** accept lazy profile creation (no auth hooks) — recommended.

### Decision record (2026-08-14)

| # | Decision | Resolution |
|---|---|---|
| 1 | Ship saved history? | **YES — implemented.** See §10 implementation record. |
| 2 | Ship Stripe now or defer? | **DEFER.** This doc remains the design record; no billing code. |
| 3 | Per-user RLS policies acceptable? | **YES** (implicit — required for #1; recorded in migration). |
| 4 | Lazy profile creation? | **YES** (implicit — recorded; no auth hooks, profiles unused so far). |

## 10. Implementation record (2026-08-14, decision 1)

- **Migration:** `supabase/migrations/001_saved_history.sql` — `profiles` +
  `saved_queries` tables, indexes, RLS (idempotent; apply via dashboard SQL editor).
  **NOT YET APPLIED to the hosted project — researcher action required.**
- **Backend:** `ports/saved_history.py`, `infrastructure/storage/postgrest.py`
  (httpx, service-role key, no new dependencies), `application/history.py`
  (503 when unconfigured), `api/history.py` (`GET/POST /api/history`,
  `DELETE /api/history/{id}` with ownership enforcement), container + router wired.
  Tests: `tests/test_history.py` — 11 offline tests (store contract with faked
  PostgREST transport, service, endpoint 401/503/200/201/204/404 flows).
  Full backend suite: **43 passed** (was 32).
- **Frontend:** `src/lib/api.ts` (Bearer-token helpers), save button in
  `qa-panel.tsx` (visible only when signed in; idle/saving/saved/error states),
  `/account` page (`src/app/(app)/account/page.tsx`: login CTA for anonymous,
  profile card + history list + delete for signed-in, graceful retry on failure),
  "আমার হিসাব" entry in the session dropdown. `pnpm build` clean (20 routes).
  Playwright E2E 8/8 (anonymous CTA, login, dropdown link, account page, graceful
  fetch failure, chat regression).
- **Verification limits:** live save/delete round-trip needs (a) migration applied,
  (b) backend running. Both pending researcher action; UI degrades gracefully.

## 9. Definition of done for this phase

Design document delivered and reviewed; no application code changed; no new env vars;
no new dependencies; amendment 15 invariants intact. Remaining work is contingent on
researcher decisions in §8.
