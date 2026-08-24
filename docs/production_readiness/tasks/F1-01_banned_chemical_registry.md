# F1-01 — BD-Grounded Banned/Restricted Chemical Registry

- **Status:** DONE (2026-08-25)
- **Spine step:** "Safety" node of the §10 flagship spine (`production/future_plan/00_SCOPE_OUTLINE.md`)
- **Novelty served:** N1 (dosage/chemical safety grounded in DAE/PPW data) + N5 (counter pro-chemical bias) — `06_PAPER_NOVELTY.md`
- **Depends on:** nothing (extends the existing deterministic safety precheck)
- **Blocks:** nothing
- **Amendment:** none needed — no hard-rule change; purely expands an existing deterministic rule set with evidence-grounded data.

## Goal

Today `backend/app/domain/safety_policy.py` hard-codes ~5 English + 2 Bengali banned-chemical patterns inline. Replace that inline literal with a **curated, source-attributed registry** of pesticide active ingredients that are **legally cancelled/banned in Bangladesh** (EN + Bengali names), so the `banned_or_restricted_chemical` deterministic gate catches the real national banned list instead of a token sample. This is the grounding that makes the safety pipeline defensibly novel (N1/N5).

## Scope decision (important — read before extending)

Bangladesh's dangerous-pesticide landscape splits into two legally distinct sets:

1. **Legally cancelled / banned actives** (organochlorines etc., 19 actives banned since 1960 + the DAE "cancelled pesticides" list). Advising these is always wrong. → **These are added to the deterministic block.** Near-zero over-block risk (nobody legitimately recommends DDT).
2. **Highly Hazardous Pesticides (HHPs) that remain legally registered** (e.g. Chlorpyrifos, Abamectin — and Paraquat/Glyphosate, which DAE stopped registering new products for in Dec 2024 but ~187 existing products are still on the market — [The Daily Star, 2025-11-25](https://www.thedailystar.net/news/bangladesh/news/17-highly-harmful-pesticides-widely-used-across-country-4043486)).

**This task only expands set (1)** — the definitively banned actives. Blanket-refusing every *mention* of a still-registered HHP would over-block legitimate advice and misstate the law. Nuanced HHP handling (misuse/overdose context + IPM-alternative surfacing) belongs to a later verifier-side task, not a blunt keyword block. The two flagship HHPs already present (paraquat, glyphosate) are retained because they are the live national policy case.

## Sources (evidence, snapshot — not live-fetched)

- DAE "List of Cancelled Pesticides in Bangladesh" (Plant Protection Wing).
- PPW বাতিলকৃত বালাইনাশক তালিকা — `ppw.krishi.gov.bd/pesticide-list-expired`.
- The Pesticides Ordinance 1971 (PTAC authority).
- The Daily Star (2025-11-25): 17 HHPs; 19 actives banned since 1960.

## Invariants (do not break)

- `precheck()` ordering unchanged: self_harm → injection → **banned** → low_confidence. A banned match must still win over a coverage keyword (existing `test_safety_priority_over_coverage`).
- Canned response text + 16123 redirect unchanged.
- Every currently-passing test stays green — especially `প্যারাকোয়াট` / `paraquat` matches and the substring-trap guards in `test_coverage_gate.py`.
- Bengali has no word boundaries → every Bengali entry must be a distinctive transliteration that cannot be a substring of a common word. English entries keep `\b` boundaries.
- Pure domain module, no file IO at import (data lives as an in-code structure, same style as the existing `PATTERNS`).

## Design

- New module `backend/app/domain/chemical_registry.py`: a curated `BANNED_ACTIVES` tuple of records `(canonical_en, bengali_aliases, source_tag)`, plus a `compiled_banned_pattern()` builder returning `(rule_name, re.Pattern)` entries.
- `safety_policy.py` imports the registry and composes its `BANNED_OR_RESTRICTED_CHEMICAL` pattern tuple from it (keeps the two flagship HHP entries). No change to `precheck` logic or ordering.
- Rule names are stable + attributable, e.g. `banned_active:ddt`, so audit `matched_rules` records exactly which banned active fired (feeds the N5 metric).

## Scope — create
- `backend/app/domain/chemical_registry.py`
- `backend/tests/test_chemical_registry.py`

## Scope — modify
- `backend/app/domain/safety_policy.py` (compose banned patterns from the registry; additive)

## Do not touch
- Canned response texts, 16123 messaging, `precheck` ordering
- The LOW_CONFIDENCE coverage gate rules
- `dataset_release/`, `frontend/`, `paper/`

## Verification gate (stop/go)
1. `uv run pytest backend/tests/test_chemical_registry.py backend/tests/test_coverage_gate.py -v` — green.
2. Full suite `uv run pytest` — no regressions vs baseline.
3. Golden replay 50/50 invariants PASS.
4. Spot-check: each newly-added banned active (EN + BN) returns `BANNED_OR_RESTRICTED_CHEMICAL`; a sample of ~15 ordinary farmer queries returns `None` (no over-block).

## Rollback
`git revert` the two files — the inline literal returns. No config, no data migration.

## Completion log (2026-08-25)

- Delivered `backend/app/domain/chemical_registry.py`: 15 `BannedActive` records
  (10 newly added beyond the old inline set) with EN `\b`-bounded aliases,
  distinctive Bengali transliterations, stable `banned_active:<name>:<en|bn>` rule
  tags, and per-entry source attribution (DAE cancelled list, PPW, Import Policy
  Order, Banglapedia, Pesticides Act 2018 base). Scope held to legally
  cancelled/banned actives + the two flagship HHP policy cases (paraquat,
  glyphosate); still-registered HHPs (chlorpyrifos etc.) deliberately NOT blocked.
- `safety_policy.py` composes `BANNED_OR_RESTRICTED_CHEMICAL` from
  `compiled_banned_patterns()` + the generic Bengali catch-alls (now three,
  বালাইনাশক added). `precheck` ordering and canned texts untouched.
- `test_pipeline.py` expectation updated `restricted_chemical_bn` →
  `banned_active:paraquat:bn`.

### Verification evidence
1. Targeted: `pytest tests/test_chemical_registry.py tests/test_coverage_gate.py`
   — 23 passed, 413 subtests.
2. Full `tests/` suite (hang test excluded, see below): **337 passed, 7 skipped,
   2 failed** — both failures pre-existing/environmental (`test_auth::test_me_with_valid_token_returns_claims`
   needs live Supabase JWKS env; `test_soil::test_analyze_is_locked…` documented
   as failing identically on clean HEAD). `scripts/test_live_e2e.py` (5 tests)
   requires a running :8000 server — environmental, not run in this gate.
3. Golden replay: **50/50 invariants PASS** (12/12 unanswerable refused, 4/4
   injection refused, 6/6 eval-flagged carry verifier flags, 0 errors).
4. Spot-check script: all 10 newly-added actives flagged EN+BN via `precheck`;
   16/16 ordinary farmer queries returned `None` — including chlorpyrifos
   (ক্লোরোপাইরিফস), a still-registered HHP, correctly NOT blocked.

### Found during verification (pre-existing, NOT caused by F1-01)
- `tests/test_sse_heartbeat.py::SSEHeartbeatTests::test_keepalive_comment_during_silence`
  hangs indefinitely in this environment (suites before F1-01 showed the same
  "2 pre-existing soil/SSE failures" note). Excluded via `--deselect`; the
  remaining suite runs in ~49s. Candidate follow-up bug fix.
