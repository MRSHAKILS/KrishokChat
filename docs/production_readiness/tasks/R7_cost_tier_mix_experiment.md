# R7 — Cost + Latency Contract & Tier-Mix Experiment

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part E + Part H + Part J item R7
- **Depends on:** R4 (T1/T2 must exist to have a non-trivial tier mix to measure)
- **Blocks:** the funder cost slide + paper claim N6 result
- **Amendment:** none — adds a price artifact, a real `estimate_cost`, an optional budget guard, and an offline experiment

## Goal

Produce **the one number the whole architecture reduces to**: the fraction of
real farmer queries that resolve at T0–T2 (zero LLM), with measured cost per
1,000 queries and p95 latency per tier. This is simultaneously the paper result
(N6), the funder slide, and the ops KPI (plan E.2).

Three concrete pieces:
1. **Price table artifact** → make `estimate_cost` return a real number instead
   of `None` (`telemetry.py:78-87` currently always returns `None`, honestly, for
   lack of a price basis).
2. **Per-request budget guard** (soft/hard ceilings) — optional, default-off.
3. **The tier-mix experiment**: an offline script over
   `farmer_benchmark_1000.jsonl` that reports resolution %, latency, LLM calls,
   and measured cost per tier, written to a versioned report artifact.

## Piece 1 — Price table (unblocks real cost)

`estimate_cost(tokens, provider)` returns `None` today **by design** — its
docstring says "when a real price basis lands (a checked-in price table per
provider/model), add it HERE with a one-line comment citing its source — never
invent a number." R7 lands exactly that basis.

- **Create** `backend/config/model_prices.json` — per `provider/model`:
  `input_usd_per_1k`, `output_usd_per_1k`, `fetched_at`, `source_url`. Versioned
  like any artifact (prices change). **Verify each price against the provider's
  live pricing page at implementation time** (AGENTS.md rule 7) and record the
  URL + date in the file — do not trust training-data prices.
- **Modify** `telemetry.py:estimate_cost` to join `tokens × price` for the
  serving provider; still returns `None` when tokens are unknown (no fabrication)
  or the model is absent from the table.
- The token capture seam already exists (`capture_tokens`, `serving_provider`);
  R7 does not need to change adapters, but note in the report which lanes
  currently expose `last_usage` (today: none in production → cost is measured in
  the experiment via a token *estimate* clearly labelled as such, see Piece 3).

## Piece 2 — Budget guard (optional, default-off)

Per plan E.1.2: a soft per-request ceiling and a hard daily ceiling per API
key/user. Exceeding soft → force a cheaper tier (T3 with fewer sources) or T4
refusal, **never silent overspend**. Default **off** so the demo path is
unchanged. Reuse the existing per-key rate-limit plumbing (T0-07) rather than a
new store.

## Piece 3 — The tier-mix experiment (the deliverable that matters)

- **Create** `backend/scripts/tier_mix_experiment.py`:
  - Input: `ml_assets/rag_index/eval/farmer_benchmark_1000.jsonl` (exists, 1000
    queries) + optionally the 20,112-record safety set for the refusal-tier view.
  - For each query, run it through the pipeline (flag R4 **on**) and record its
    `resolution_tier`, latency (p50/p95 per tier from `stage_timer` data),
    `llm_calls`, and token estimate → cost.
  - **Token estimate honesty**: since production adapters do not yet expose
    `last_usage`, the experiment estimates tokens with a documented tokenizer/
    char-ratio method and **labels every cost number as estimate-based**, citing
    the method. When adapters expose real usage later, rerun for measured cost.
  - Output: `docs/production_readiness/reports/tier_mix_<date>.md` +
    a machine-readable `tier_mix_<date>.json` with the per-tier table and cost
    per 1,000 queries at **three mixes** (pessimistic / measured / fact-base-
    expanded), per plan E.2.
- **Rule (plan E.2, non-negotiable):** the report must never state a projected
  cost without the measured tier mix it came from, and must label estimate-based
  vs measured tokens explicitly.

## Piece 4 — Latency budget assertions (light)

Encode the plan E.3 targets (T0/T1/T2 < 100 ms, T3 first token < 2.5 s, full
< 8 s) as **report annotations**, not hard test gates (real latency is
environment-dependent). The experiment flags any tier exceeding its target so
regressions are visible, but does not fail CI on a slow machine.

## Scope — create
- `backend/config/model_prices.json`
- `backend/scripts/tier_mix_experiment.py`
- `backend/tests/test_cost_pricing.py`
- `docs/production_readiness/reports/` (dir) + the generated report on first run

## Scope — modify
- `backend/app/application/telemetry.py` — real `estimate_cost` via the price
  table (fail to `None` on unknown tokens/model).
- `backend/app/core/config.py` + `.env.example` — `MODEL_PRICES_PATH`,
  `BUDGET_GUARD_ENABLED` (default `false`), `PER_REQUEST_COST_CEILING_USD`,
  `DAILY_COST_CEILING_USD`.
- `backend/app/application/qa_pipeline.py` — budget guard hook (only active when
  the flag is on) around tier selection; **no change when flag off**.

## Do not touch
- LLM adapters / `infrastructure/llm/` (out of scope; token exposure is a
  separate future task — the experiment labels its estimates instead).
- Answer text, safety, retrieval, verifier.
- The benchmark file contents (`farmer_benchmark_1000.jsonl` is frozen input).

## Invariants
- `estimate_cost` returns a real number **only** when tokens are known and the
  model is in the price table; otherwise `None` — never a fabricated cost
  (AGENTS.md rule 5, extended to cost per plan E.2).
- Every price row carries `fetched_at` + `source_url` verified at build time.
- Budget guard **off by default** → demo/anon path byte-identical (full suite +
  golden replay unchanged).
- The experiment report labels each cost as estimate-based or measured and always
  states its tier mix; a report missing either is invalid.
- The experiment is offline (a script), never in a request path.

## Verification record

**Date:** 2026-08-25
**Implemented by:** Antigravity agent

**Gate results:**
1. `uv run pytest tests/test_cost_pricing.py -v` → **9 passed** in 0.21s ✅
2. `uv run python scripts/tier_mix_experiment.py --limit 50` → Smoke test passed ✅
3. Full experiment over `farmer_benchmark_1000.jsonl` (1,000 queries) → **6.8% Zero-LLM resolution rate, $0.1817 / 1,000 queries** ✅
4. Full `tests/` suite → **522 passed, 7 skipped, 0 failed** ✅
5. `pnpm build` → **✅ green** (22/22 routes prerendered / dynamic clean)

**Outputs generated:**
- `backend/config/model_prices.json` (verified rates with live URLs and fetch dates)
- `docs/production_readiness/reports/tier_mix_20260825.json`
- `docs/production_readiness/reports/tier_mix_20260825.md`
- `backend/scripts/tier_mix_experiment.py`
- `backend/tests/test_cost_pricing.py`
