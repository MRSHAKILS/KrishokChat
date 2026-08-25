# R2 — Fact Base v1 (structured, provenance-carrying answer rows)

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part C.1 + Part J item R2
- **Depends on:** R1 (ingestion contract), R3 (tier enum exists so R4 can consume this)
- **Blocks:** R4 (the resolver reads this), R12 (more crops extend it)
- **Amendment:** none — additive offline artifact + loader; nothing runs at request time (rule 2)

## Goal

Widen the existing 71-entry `dose_reference_v1.json` (today only a *verifier
input*) into a **fact base that can answer**: normalized rows keyed by
`crop × problem × stage`, each carrying a registered dose band, timing, IPM
alternatives, and — non-negotiably — the `source_node_id` it was extracted from.

R2 builds and validates the artifact **only**. It does not wire it into the
pipeline; R4 does that. Splitting them keeps each task reversible: R2 can land
and sit inert (like the dose reference did before its verifier hookup).

**Scope is the spine crop only: potato (আলু) late blight + the doses already in
the dose reference.** Breadth is R12. A narrow, correct fact base beats a wide,
shaky one for both the demo and the paper.

## The row schema (fact_base_v1.json)

```
{
  "version": 1,
  "provenance": { builder, source_corpus, built_at, sha256 },   # R1 contract
  "facts": [
    {
      "crop": "potato",
      "crop_bn": "আলু",
      "problem": "late_blight",
      "problem_bn": "নাবি ধ্বসা / লেট ব্লাইট",
      "problem_type": "disease",              # disease|pest|deficiency|abiotic
      "stage": "tuber_bulking",               # must be a stage key from crop_calendars_v1
      "active_ingredient": "mancozeb",
      "dose_min": 2.0, "dose_max": 2.5, "dose_unit": "g/l",
      "application_interval_days": 7,
      "pre_harvest_interval_days": 7,
      "ipm_alternatives_bn": ["আক্রান্ত পাতা অপসারণ", "সুষম সেচ"],
      "banned_flag": false,                   # cross-checked vs chemical_registry
      "severity": "high",
      "source_node_id": "<id from knowledge_nodes_clean.jsonl>",
      "source_doc": "BARC ...",
      "citation": "...",
      "grounding": "corpus-extracted",        # or curated-approximation
      "confidence": 0.9
    }
  ]
}
```

Every numeric field must trace to `source_node_id` — reuse the extraction that
`build_dose_reference.py` already does (it binds an active to a rate within ±120
chars with a citation). R2 is that logic, plus crop/problem/stage keys and IPM,
serialized to the answerable schema.

## Build-time validation (the safety guarantee)

The novelty claim "a bad dose fails the build, not a request" lives here. The
builder must **reject and archive** (not ship) any row where:
- `dose_min`/`dose_max` are absent or non-numeric, or `min > max`;
- the active cross-matches `domain/chemical_registry.BANNED_ACTIVES` but
  `banned_flag` is false (contradiction → reject);
- `stage` is not a known key in `crop_calendars_v1.json` (keeps the two
  artifacts consistent);
- the dose exceeds the F1-02 gross-outlier band (≥3× reference max) — the same
  bound the verifier uses, applied at build time so T1/T2 rows are correct by
  construction (plan doc Part B invariant).

Rejections go to `ml_assets/rag_index/derived/rejected/fact_base_v1.rejected.json`
with the reason (R1 clause 6).

## Scope — create
- `backend/ml_assets/rag_index/derived/fact_base_v1.json` (committed artifact)
- `backend/ml_assets/rag_index/derived/curated_facts_v1.json` (human-editable
  seed for rows the corpus cannot supply, each marked `curated-approximation`)
- `backend/scripts/build_fact_base.py` (offline builder, uses R1 helpers)
- `backend/app/domain/fact_base.py` (`Fact` dataclass + `FactBase` with a pure
  `lookup(crop, problem, stage) -> list[Fact]` — NO I/O, NO LLM)
- `backend/app/infrastructure/knowledge/fact_base_store.py` (fail-open loader)
- `backend/tests/test_fact_base.py`

## Scope — modify
- `backend/app/core/config.py` + `.env.example` — `FACT_BASE_PATH` (empty →
  default derived path, mirroring `dose_reference_path`, `config.py:146`).

## Do not touch
- The pipeline, API, retrieval, verifier — R2 does **not** wire in. The loader
  is constructed nowhere yet (R4 adds it to the container).
- `dose_reference_v1.json` (R2 reads the corpus, not the derived dose file).

## Invariants
- Builder is deterministic (R1 clause 2): re-run → zero diff.
- Every shipped fact has a non-empty `source_node_id` **or**
  `grounding == "curated-approximation"` — never both empty, never a fabricated
  citation.
- `banned_flag` agrees with `chemical_registry` for every row (test-locked).
- Zero rows exceed the F1-02 outlier band (test-locked).
- The artifact loads fail-open; absent file = empty `FactBase`, no error.

## Verification gate (stop/go)
1. `uv run python scripts/build_fact_base.py --print` — reports N potato/late-blight
   rows + rejection count; re-run → `git diff --exit-code` clean.
2. `uv run pytest tests/test_fact_base.py -v` — green (schema, banned agreement,
   outlier bound, fail-open loader, deterministic build).
3. Full `tests/` suite — 410/7/0 baseline held (nothing wired in, so it must be
   exactly unchanged).

## Rollback
`git revert`; delete the new artifacts. Nothing consumes them yet.

## External sources
None for v1 (corpus + curated seed only). R12 later ingests DAE/PPW +
BAMIS disease-weather calendars via R1 — flagged there, not here.

## Notes for the implementing agent
- Reuse `build_dose_reference_entries()` rather than re-writing rate extraction.
- If the corpus yields fewer than ~5 grounded potato/late-blight rows, that is
  fine and honest — fill the rest from `curated_facts_v1.json` marked
  `curated-approximation`, never by inventing corpus citations.
- Do not add crop/problem beyond potato late blight. That is R12.
