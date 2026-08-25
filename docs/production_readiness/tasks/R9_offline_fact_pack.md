# R9 — Offline Fact Pack + Data-Aware Service Worker

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part F + Part J item R9
- **Depends on:** R4 (T1/T2 resolver + fact base produce the deterministic answers a pack ships)
- **Blocks:** R10 (on-device story builds on the offline pack), R11 (sync-state UI)
- **Amendment:** none — additive offline capability; online path and anon demo unchanged

## Goal

Make the strongest practical-feasibility claim real: **a farmer with no signal
still gets a correct, cited dose for their crop.** Ship the T1/T2 fact rows to
the device as a compact crop-scoped JSON pack, and grow `sw.js` from shell-only
to **data-aware** — caching deterministic (tier ≤ 2) responses keyed by
fact-base version, and answering from the pack when offline. T3 generations are
**never** cached (they are model output, not a fact).

Scope is the **potato spine** pack only (matches R4). Other crops arrive as data
edits under R12.

## Two halves

### Half 1 — Backend: emit the fact pack (offline artifact)

- **Create** `backend/scripts/build_fact_pack.py` — reads the R2 fact base and
  emits per-crop packs: `frontend/public/packs/facts_potato_v<factbaseversion>.json`.
  Compact shape (tens of KB): only the fields the client template needs (crop,
  problem, stage, dose min/max/unit, interval, PHI, IPM alt, citation, tier
  label), plus a `pack_version` == fact-base version and a `built_at`.
- **Create** `GET /api/packs/manifest` — lists available packs + their versions
  so the client knows when a pack is stale (drives R11's "advice pack updated"
  state). Read-only, no auth beyond existing rules.
- The pack is built **offline** (script), committed, and served as a static
  asset — no request-time generation (AGENTS.md rule 2).

### Half 2 — Frontend: data-aware service worker + IndexedDB

> **Frontend note:** this repo runs a modified Next.js — read the guides in
> `node_modules/next/dist/docs/` before touching `sw.js`/PWA wiring, per
> `frontend/AGENTS.md`. The `nextjs-agent-rules` block in that file is
> auto-generated; commit it with your work rather than reverting it.

- **Modify** `frontend/public/sw.js` — today it is shell-only and **explicitly
  never caches `/api/*`** (line 63-71, a hard invariant). R9 refines the
  invariant precisely: still never cache T3 `/api/qa` generations, but **do**
  precache the static fact packs under `/packs/` (cache-first, versioned by
  filename) and the pack manifest (stale-while-revalidate, like the existing
  `/library/*.json` strategy at line 78-96). Add `/packs/facts_potato_v*.json`
  to a versioned precache list; bump `CACHE_NAME` when the pack version changes.
- **Create** a small client fact-lookup module (e.g.
  `frontend/src/lib/offline-facts.ts`) — loads the cached pack from Cache
  Storage / IndexedDB, runs the **same deterministic matcher contract as R4**
  (crop + problem → row), and renders the **same Bengali template** so an offline
  answer is identical to the online T1/T2 answer. Store the farmer's own
  profile/stage + last N advisories in IndexedDB (plan F).
- **Modify** the chat flow so that, **when offline**, a query that the pack can
  answer returns a T1/T2 answer locally with an explicit "offline / from advice
  pack" provenance chip (reuse R3's `resolution-badge`), instead of the current
  offline banner. A query the pack cannot answer still shows the honest offline
  banner (no fabrication offline, same as online T4).

## Design guardrails (the ladder must stay honest offline)

- **Only tier ≤ 2 is cacheable.** The SW rule becomes "cache deterministic
  responses keyed by fact-base version; never cache T3." A T3 answer offline is
  impossible → honest "unavailable offline" (plan F).
- **The offline answer must byte-match the online T1/T2 answer** for the same
  query + same pack version. This is the correctness contract; test it.
- **Staleness is visible.** The pack carries `pack_version` + `built_at`; the UI
  shows a last-synced timestamp and refuses to answer from a pack older than a
  configured window (plan I risk row "offline packs go stale").

## Scope — create
- `backend/scripts/build_fact_pack.py`
- `backend/app/api/packs.py` (`/api/packs/manifest`)
- `frontend/public/packs/facts_potato_v<v>.json` (committed artifact)
- `frontend/src/lib/offline-facts.ts`
- `backend/tests/test_fact_pack.py`
- `frontend/` unit test for the offline matcher (match the repo's frontend test
  setup; see `frontend/AGENTS.md` / package.json for the runner)

## Scope — modify
- `frontend/public/sw.js` (versioned pack precache + manifest SWR; keep the
  no-T3-cache invariant)
- `frontend/src/components/chat/*` (offline T1/T2 answer path + sync state)
- `backend/app/main.py` (mount `/api/packs`)
- `.env.example` — `FACT_PACK_STALE_MAX_DAYS` (client-read config surfaced via
  manifest), if a server-side value is needed.

## Do not touch
- The online QA pipeline, safety, retrieval, generation, verifier.
- The R3 badge component internals (reuse it; don't fork it).
- T3 caching rules — T3 stays network-only, never cached.

## Invariants
- **Online path + anon demo byte-identical** (full suite + golden replay
  unchanged; SW changes only add pack handling).
- Offline T1/T2 answer == online T1/T2 answer for the same query + pack version
  (test-locked).
- The SW **never** caches `/api/qa` T3 responses (the existing hard invariant is
  preserved, only narrowed to allow static `/packs/`).
- No fabrication offline: a pack miss shows the honest offline state, never a
  guessed dose.
- Pack carries version + build date; stale pack beyond the window refuses to
  answer.

## Verification gate (stop/go)
1. `uv run pytest tests/test_fact_pack.py -v` — green (pack schema, version ==
   fact-base version, only cacheable fields present).
2. Frontend unit test: offline matcher returns the same row + rendered text as
   the R4 online template for a curated potato-late-blight query.
3. Full backend `tests/` suite — 410/7/0 baseline held.
4. `pnpm build` green; manual: DevTools offline → potato late-blight dose
   question answers from the pack with an offline provenance chip; an
   unrelated question shows the offline banner.
5. Golden replay 50/50 PASS (online path unchanged).

## Rollback
`git revert`; remove the pack files and the `/packs` route. The SW reverts to
shell-only; the online path is untouched throughout.

## External sources
None — the pack derives from the in-repo R2 fact base.

## Notes for the implementing agent
- The single most important test is the **online == offline byte-match** for
  T1/T2. If the offline template drifts from R4's, a farmer gets two different
  answers to the same question depending on signal — unacceptable for a
  safety-critical dose. Share the template contract; do not re-author it.
- Keep the pack tiny and crop-scoped. A 2–4 GB phone on 3G is the target; the
  pack should be tens of KB, not megabytes.
- Do not attempt offline T3. Generation offline is out of scope and dishonest to
  fake — the whole point of the ladder is that only deterministic tiers ship
  offline.
