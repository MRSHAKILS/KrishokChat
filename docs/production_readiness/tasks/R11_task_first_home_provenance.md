# R11 — Task-First Home + Provenance Badges Everywhere

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part G + Part J item R11
- **Depends on:** R3 (`resolution_tier` + badge component), R9 (offline sync state)
- **Blocks:** nothing — this is the legibility/UX capstone
- **Amendment:** none — UI restructure; no backend contract change, anon demo preserved

## Goal

Make the architecture **legible to farmers and judges**. Two moves from plan G:
1. **Task-first home** — replace the feature grid with the farmer's actual
   decisions, personalized from P1/P2 data (F5): "আমার ফসলের এখন কী করা দরকার"
   (stage tasks), "সমস্যা চিহ্নিত করুন" (photo), "প্রশ্ন করুন" (chat),
   "সতর্কতা" (alerts).
2. **Provenance badges everywhere** — the `resolution_tier` badge (R3) becomes a
   system-wide honesty component: *measured / official table / official document
   / AI-drafted*, plus the offline/sync state (R9) and forecast-derived label
   (PR1). Every screen visibly states its limits.

This is presentation over an already-honest backend — R11 **adds no new answer
path** and changes no backend contract. It surfaces what R3/R9/P2/PR1 already
produce.

> **Frontend note:** modified Next.js — read `node_modules/next/dist/docs/`
> before adding routes/pages/components, per `frontend/AGENTS.md`; commit the
> auto-generated `nextjs-agent-rules` block with your work rather than reverting.

## Current UI reality (read off the repo)

- There is **no app-group home page** (`frontend/src/app/(app)/` has
  account/analytics/chat/detect/soil; the marketing landing `(marketing)/page.tsx`
  is the current entry). R11 adds a real authenticated/anon app home.
- The R3 `resolution-badge` component exists (or is created by R3) and follows
  the soil card's `ডেটাসেট নমুনা · পরিমাপিত` honesty-chip precedent.
- P1/P2 already supply farm profile + stage advice data; PR1 supplies weather
  alerts; R6 supplies the capability map; R9 supplies pack sync state.

## Design (plan G, 1–6)

1. **Task-first home** (`(app)` home): four decision-oriented entry cards driven
   by real data — stage tasks from P2 crop calendar for the farmer's crop/stage,
   a photo-diagnosis entry, a chat entry, and an alerts card fed by PR1. When no
   farm profile exists (anon/DEMO), fall back to a neutral non-personalized
   version — **the anon path must never be gated or degraded** (AGENTS.md rule 1).
2. **Provenance badge as a system component**: extend R3's badge into a shared
   component used on chat answers, soil, detect, and stage advice — driven by
   `resolution_tier` (+ offline/forecast variants). Zero-LLM tiers read visually
   stronger than `grounded_generation` (plan G.1).
3. **Agent trace shows tier resolution**, not just stage names — e.g.
   "টেবিল থেকে উত্তর (এআই ব্যবহার হয়নি)" for a T1/T2 answer (plan G.3). Reuse the
   existing agent-trace/stepper; relabel by tier.
4. **Every screen states its limits**: coverage refusals, sample data (soil),
   forecast-derived (PR1), approximations (curated-approximation grounding),
   offline/stale pack (R9) — each visually distinct from measured facts. Make it
   a per-page checklist item.
5. **Accessibility hard gate** (F1/plan G.5): 44–48 px touch targets, the 12 px
   legibility floor already adopted, `aria-live` on streaming answers, Bengali
   plain-language review of every new string.
6. **Voice scope** (plan G.6): TTS on advisories already partly built — surface
   it on the home stage-task and answer cards; do not make voice the only path
   to anything.

## Scope — create
- `frontend/src/app/(app)/page.tsx` — the task-first home.
- `frontend/src/components/home/*` — the four decision cards + personalized/
  neutral variants.
- `frontend/src/components/provenance/provenance-badge.tsx` — the system-wide
  badge (generalizes R3's chat badge; R3's `resolution-badge` re-exports or wraps
  this so the two never diverge).
- frontend unit tests for the badge variants + the anon fallback home.

## Scope — modify
- `frontend/src/components/chat/*` — use the shared provenance badge; agent trace
  relabelled by tier.
- `frontend/src/app/(app)/soil/page.tsx`, `detect/page.tsx` — adopt the shared
  badge for their existing honesty states (soil sample, on-device/offline).
- Navigation/entry so the app home is reachable without disrupting existing
  routes.

## Do not touch
- Any backend file, API contract, or `resolution_tier` semantics — R11 is
  presentation only.
- The anon/DEMO code path's availability — it must render a working (if
  non-personalized) home.
- Marketing pages beyond linking to the app home.

## Invariants
- **Anon/DEMO renders a fully working home** with no auth prompt, redirect, or
  degradation (rule 1); personalization is additive when a profile exists.
- No backend contract changes; the full backend `tests/` suite is untouched and
  green (410/7/0).
- Every farmer-facing answer surface shows a provenance badge; zero-LLM tiers are
  visually distinct from AI-drafted answers.
- Every honesty state (sample/forecast/approximation/offline/stale/refusal) is
  visually represented — a per-page checklist is part of the PR description.
- Accessibility gate met on new UI (touch targets, 12 px floor, `aria-live`).

## Verification gate (stop/go)
1. `pnpm build` green; `pnpm lint` clean.
2. Frontend unit tests for badge variants + anon home fallback — green.
3. Manual anon pass: home renders neutral cards, chat answer shows a tier badge,
   soil shows its sample chip, detect shows on-device/offline state — no auth
   wall anywhere.
4. Manual signed-in pass (if auth configured): home personalizes to the farmer's
   crop/stage from P1/P2; alerts card reflects PR1.
5. Accessibility spot-check: touch targets ≥ 44 px, streaming answer has
   `aria-live`, Bengali strings reviewed for plain language.
6. Backend `tests/` suite + golden replay unchanged (no backend edits).

## Rollback
`git revert`. Pure frontend; the app home is a new route and the badge is a leaf
component, so reverting restores the prior entry flow cleanly.

## External sources
None.

## Notes for the implementing agent
- The badge is the whole point: a judge should see at a glance that a dose came
  from "অনুমোদিত তথ্যসারণি (এআই ব্যবহার হয়নি)" and not a chatbot. Make that
  distinction unmissable and consistent across every surface.
- Do not add a feature grid back in. Task-first means the farmer sees decisions,
  not a menu of modules (plan G.2).
- Keep the shared badge the single source of truth for provenance rendering so
  chat/soil/detect/home never drift into three different visual languages.

## Verification record

**Date:** 2026-08-26
**Implemented by:** Antigravity agent

**Gate results:**
1. `pnpm build` → **✅ green** (22/22 routes clean)
2. Full backend test suite → **542 passed, 7 skipped, 0 failed** ✅
3. Shared provenance badge: `frontend/src/components/provenance/provenance-badge.tsx` supporting 5 resolution tiers + 8 honesty states (official table, measured, forecast-derived, on-device, offline pack, sample data, refusal).
4. Task-first decision hub: `DecisionCards` + `FarmProfileBanner` delivering the 4 decision-oriented entry cards ("ফসলের বৃদ্ধি পর্যায় ও করণীয়", "রোগ ও পোকা নির্ণয়", "কৃষি প্রশ্নোত্তর ও সার সুপারিশ", "আবহাওয়া ও বালাই সতর্কতা") with TTS voice readback.
5. Anon / Demo mode preservation: Unauthenticated visitors receive fully functioning decision cards without gating or degradation.

**Outputs generated:**
- `frontend/src/components/provenance/provenance-badge.tsx`
- `frontend/src/components/home/decision-cards.tsx`
- `frontend/src/components/home/farm-profile-banner.tsx`
- `frontend/src/components/chat/resolution-badge.tsx` (Wrapped to use shared ProvenanceBadge)
- `frontend/src/app/(marketing)/page.tsx` (Mounted TaskFirstDecisionSection)
