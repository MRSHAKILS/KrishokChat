# R5 — Merge Safety + Intent into One Structured Call

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part D.2 + Part J item R5
- **Depends on:** R3 (tier + llm_calls plumbing exists)
- **Blocks:** R6 (capability registry routes on the intent this produces)
- **Amendment:** none — collapses two potential LLM calls into one; safety semantics unchanged

## Goal

Today safety classification is one structured LLM call
(`SafetyClassifier.classify`, `application/safety.py`) and there is a **separate,
legacy** intent path (`services/advisory/intent_classifier.py`) that *re-runs the
whole safety classifier* just to bucket a safe query into
treatment/prevention/fertilizer/general. R5 makes the **single** safety call also
return the intent slots (crop, problem, stage, upazila, intent kind), so a routed
query never pays two LLM calls, and retires the legacy re-run path.

The immediate win is cost/latency (one call, not two, for any query that reaches
the classifier). The structural win is that R6's capability registry gets a
clean `Intent` object to route on, produced by the same call that already runs.

## What must NOT change (the safety contract)

`application/safety.py` has hard-won behavior — do not regress it:
- **Deterministic precheck still runs first** and short-circuits with 0 LLM calls
  (`precheck(query)` at `safety.py:34`). Intent extraction only matters on the
  `safe_agri` branch; a terminal refusal needs no intent.
- **`VALID_CATEGORIES` still excludes `low_confidence`** — the router never
  decides coverage (`safety.py:17`).
- **The confidence-gate lesson stays**: do not reintroduce a confidence threshold
  that refuses normal questions (the 0.65/0.3 incident documented at
  `safety.py:61-70`). Only explicit `requires_escalation` demotes.
- **Fail-closed on classifier outage** → `low_confidence` + `classifier_outage`
  (`safety.py:82-91`). Intent is simply absent on that path.

## Design

### One call returns category **and** intent

Extend the classifier's JSON contract and the `SafetyDecision` (or a sibling
`Intent`) so a single `classify_json` response carries both. Proposed shape:

```json
{"category":"safe_agri","confidence":0.0,"reason":"...",
 "matched_rules":[],"requires_escalation":false,
 "intent":{"kind":"treatment","crop":"potato","problem":"late_blight",
           "stage":null,"upazila":null}}
```

`intent` is **optional and advisory**: a missing/malformed `intent` block never
changes the safety decision and never raises — it degrades to `intent: null`,
exactly like `tokens` degrades in telemetry. Safety is load-bearing; intent is a
routing hint.

### Deterministic-first still holds

The plan (D.2) says a keyword matcher handles common intents and the LLM is only
for ambiguity. R5 keeps the existing keyword logic (the treatment/prevention/
fertilizer keyword scan already in `intent_classifier.py:27-35`) as a
**deterministic pre-fill**: if the keywords resolve the intent kind confidently,
use them and do not depend on the LLM's `intent` block. The LLM block is the
fallback/enricher, not the primary. This keeps intent extraction testable and
cheap.

### Intent cache

Intent for a normalized query string is stable (D.2). Cache the resolved `Intent`
keyed by the normalized query, reusing the existing normalization already applied
for the demo cache. A repeat question resolves intent with 0 additional work.
Scope the cache in-process (dict/LRU) — no new store (AGENTS.md rule 3).

## Scope — create
- `backend/app/domain/intent.py` — frozen `Intent` dataclass (`kind`, `crop`,
  `problem`, `stage`, `upazila`, `source: "keyword"|"llm"|"none"`), plus a pure
  `keyword_intent(query) -> Intent | None` (lifts the existing keyword scan).
- `backend/tests/test_intent_extraction.py`

## Scope — modify
- `backend/app/application/safety.py` — parse the optional `intent` block; attach
  the resolved `Intent` (keyword-first, LLM-fallback) to the returned decision.
  Prompt (`_prompt`, `safety.py:93`) gains the `intent` field in its requested
  JSON shape + a one-line instruction; **the safety guidelines block is
  unchanged**.
- `backend/app/domain/contracts.py` — `SafetyDecision` gains
  `intent: Intent | None = None` (last, defaulted → no constructor breaks).
- `backend/app/application/qa_pipeline.py` — thread the decision's `Intent`
  through to where retrieval query is built (it is available for R6); record
  `intent.kind` in the audit dict (additive key, like R3's tier). **`llm_calls`
  is unchanged** — this was already one call; R5 just stops the *second* one from
  ever being added.
- `backend/app/services/advisory/intent_classifier.py` — reduce to a thin shim
  that reads `decision.intent` instead of re-deriving; mark clearly that it no
  longer issues its own LLM call. (Keep the function signature for old offline
  scripts, per its existing purpose note.)

## Do not touch
- `precheck` / `safety_policy.py` rules, canned responses, `VALID_CATEGORIES`.
- The generation/retrieval/verifier stages.
- Any confidence-threshold behavior (the incident note is a landmine — leave it).

## Invariants
- **Every safety decision is exactly one LLM call or zero** (precheck hit = 0).
  No path issues two. Test: a routed safe query records `llm_calls` no higher
  than today's equivalent.
- Safety category, confidence, matched_rules, canned response, and escalation are
  **byte-identical** to pre-R5 for the full test corpus (intent is additive).
- A malformed/absent `intent` block never changes the category and never raises.
- Precheck still short-circuits with 0 LLM calls and no intent extraction.
- Classifier outage still fails closed to `low_confidence`.

## Verification gate (stop/go)
1. `uv run pytest tests/test_intent_extraction.py -v` — green.
2. `uv run pytest tests/test_pipeline.py tests/test_api.py tests/ -k safety -v` —
   green; safety decisions unchanged.
3. Full `tests/` suite — 410/7/0 baseline held.
4. Golden replay 50/50 PASS (safety-terminal items must be byte-identical).
5. Add a test proving the legacy `classify_intent` no longer triggers a second
   `classify_json` (assert call count on a fake LLM).

## Rollback
`git revert`. `Intent` is additive and defaulted; the shim change is internal.

## External sources
None.

## Notes for the implementing agent
- The prompt edit is delicate: add the `intent` field to the **requested output
  JSON** without touching the safety category guidelines. A safety regression
  here is far more expensive than a missed intent, so bias every ambiguity toward
  preserving the current safety behavior.
- Do not build capability routing here — that is R6. R5 only *produces* the
  `Intent`; nothing consumes it for routing yet beyond the audit field.
