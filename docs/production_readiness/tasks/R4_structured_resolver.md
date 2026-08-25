# R4 — T1/T2 Structured Resolver (the actual novelty: 0-LLM answers)

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part B + Part J item R4
- **Depends on:** R2 (fact base), R3 (tier plumbing)
- **Blocks:** R7 (tier-mix experiment measures this), R9 (offline pack ships these rows)
- **Amendment:** none — additive resolver behind a flag; T3 remains the default when the flag is off

## Goal

Insert tiers **T1 (structured_fact)** and **T2 (templated_advisory)** into the
pipeline **before** retrieval/generation. When a query resolves to a fact-base
row for potato late blight, compose the answer **from the row** (with a Bengali
template) and return it with **zero LLM calls** — citation structural, dose
correct by construction. On any miss, fall through to T3 exactly as today.

This is the claim N6 in the plan. It is scoped to **potato late blight only**;
everything else still goes T3. Behind a config flag (`structured_resolver_enabled`,
default **off**) so it lands dark and is proven on golden replay before flipping.

## Where it sits in the pipeline

```
safety (T0 guard runs first — UNCHANGED)
   │ safe_agri
   ▼
[NEW] structured resolve  ──hit──▶ compose from fact row → T1/T2 → return, 0 LLM
   │ miss
   ▼
retrieval → generation → verifier  (T3, today's path, UNCHANGED)
```

Safety is never bypassed (plan invariant). The resolver runs only on a
`safe_agri` decision, after the terminal-refusal branch, before retrieval — i.e.
inserted at `qa_pipeline.py` around line 262 (after the cache-replay check,
before `emit(RETRIEVAL, START)`).

## T1 vs T2

- **T1 structured_fact** — a single confident row answers directly (dose +
  interval + PHI rendered from fields).
- **T2 templated_advisory** — the row plus stage/IPM context rendered through a
  fuller Bengali advisory template (e.g. includes the calendar stage note and
  IPM alternatives). Same 0-LLM guarantee; T2 is just a richer surface.

Both carry the row's `source_node_id`/`citation` as the single source in the
`QAResult.sources`, so the UI and audit see real provenance, not a generated
citation.

## Intent → fact lookup (deterministic, no LLM in R4)

R4 uses a **deterministic matcher only** — keyword/alias against the fact base's
crop/problem aliases + the farmer's stage (from `farmer_context` / crop calendar
if present, else the row's default stage). The *LLM* intent classifier is R5,
explicitly out of scope here. Rationale: prove the resolver + templates are
correct with a matcher we can unit-test exhaustively, before adding a model.

Matcher rule: a query resolves to T1/T2 only when crop **and** problem match a
fact row with `confidence >= threshold`. Anything ambiguous → miss → T3. Bias
toward missing to T3 (safe, just costs an LLM call) over a wrong structured
answer.

## Scope — create
- `backend/app/application/structured_resolver.py` — `StructuredResolver`
  (holds a `FactBase`, `CropCalendarLibrary`, and the Bengali templates); pure
  `resolve(query, context) -> ResolvedAnswer | None`. No I/O, no LLM.
- `backend/app/domain/advisory_templates.py` — Bengali T1/T2 template functions
  (pure string composition from a `Fact`; unit-testable).
- `backend/tests/test_structured_resolver.py`
- `backend/tests/test_advisory_templates.py`

## Scope — modify
- `backend/app/application/qa_pipeline.py` — construct-time optional
  `resolver: StructuredResolver | None = None`; the insertion point above.
  When it returns a hit, build a `QAResult` with `resolution_tier` T1/T2,
  the fact row as the single source, `llm_calls=0`, emit RETRIEVAL/GENERATION/
  VERIFIER as `SKIP` with detail "structured fact answer", and audit normally.
- `backend/app/application/container.py` — build the resolver from the R2 fact
  base + P2 calendars when `settings.structured_resolver_enabled`; else `None`.
- `backend/app/core/config.py` + `.env.example` — `STRUCTURED_RESOLVER_ENABLED`
  (default `false`), `STRUCTURED_RESOLVER_MIN_CONFIDENCE` (default 0.85).

## Do not touch
- Safety/precheck (T0), verifier internals, retrieval, the T3 generation path.
- The fact-base artifact/schema (R2 owns it).
- Any crop other than potato — the fact base only has potato late blight; the
  matcher must not pretend otherwise.

## Invariants
- **Flag off → byte-identical to today** (locked: full suite + golden replay
  with flag off must match the 410/7/0 + 50/50 baseline exactly).
- Safety always runs first; a terminal decision never reaches the resolver.
- A T1/T2 answer records `llm_calls == 0` and carries a real `source_node_id`.
- A T1/T2 dose never exceeds the F1-02 band (guaranteed upstream by R2's
  build-time validation; re-assert with a resolver test as a regression net).
- Resolver miss → the request proceeds to T3 with no observable difference from
  today (same retrieval query, same generation).
- The resolver performs **no network and no LLM call** (test with a fake that
  raises if any LLM method is touched).

## Verification gate (stop/go)
1. `uv run pytest tests/test_structured_resolver.py tests/test_advisory_templates.py -v` — green.
2. `uv run pytest tests/test_pipeline.py tests/test_api.py -v` — green with flag
   on and off.
3. Flag **off**: full `tests/` suite 410/7/0 + golden replay 50/50 — exact match.
4. Flag **on**: a curated potato-late-blight dose question returns T1/T2 with
   `llm_calls=0`, a real citation, and a dose within band; an unrelated question
   (e.g. rice pest) still returns T3.
5. `pnpm build` green; the R3 badge shows the stronger "0-LLM / table" state.

## Rollback
`git revert`, or simply leave `STRUCTURED_RESOLVER_ENABLED=false` — the feature
is dark by default and additive.

## External sources
None. Consumes R2's in-repo artifact.

## Notes for the implementing agent
- The hard part is the **templates reading naturally in Bengali**, not the
  plumbing. Follow the tone of the canned safety responses and the P2 stage
  advisory strings (`curated_calendars_v1.json` `advisory_bn`). Keep dose
  numbers verbatim from the fact row; never round or rephrase a number.
- Do NOT add the LLM intent classifier here — that is R5. Deterministic matcher
  only.
- Measure honestly: this task makes the tier-mix number real, so resist the urge
  to widen matching to inflate the T1/T2 hit rate. Missing to T3 is correct.
