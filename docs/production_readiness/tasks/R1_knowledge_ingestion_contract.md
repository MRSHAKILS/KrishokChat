# R1 — Knowledge-Ingestion Contract (data grows without code changes)

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part C.2 + Part J item R1
- **Depends on:** nothing
- **Blocks:** R2 (fact base uses this contract), R12 (more crops)
- **Amendment:** none — formalizes an existing pattern; no runtime behavior change

## Goal

Turn the ad-hoc "build an artifact offline, load it fail-open" pattern (already
used by F1-02 dose reference and P2 crop calendars) into **one documented,
tested contract** every future knowledge asset must follow. The deliverable is
mostly a **contract doc + a reusable builder/loader skeleton + a test that locks
the invariant**, not a new runtime feature.

The invariant to lock, in one sentence: **adding knowledge is editing a data
file and re-running a builder — never a Python change.**

## Why this is the foundation

The whole scaling story for funding ("government data could 10× our corpus")
is only true if ingestion is a data operation. Today that is *true by
convention* (two assets happen to follow it) but *not enforced* — nothing stops
the next agent from hardcoding a crop list or a dose in Python. R1 makes the
convention a checked contract so R2/R12 inherit it for free.

## The contract (what every knowledge asset must satisfy)

Read the two working examples first — they ARE the pattern, do not reinvent:
- `backend/scripts/build_dose_reference.py` + `backend/app/infrastructure/verification/dose_reference.py`
- `backend/scripts/build_crop_calendars.py` + `backend/app/infrastructure/agronomy/calendar_store.py`

Contract clauses:

1. **Curated source is a data file.** Human-editable JSON with per-entry
   `source` (citation) + `grounding` (`corpus-extracted` | `curated-approximation`).
   Example precedent: `ml_assets/agronomy/curated_calendars_v1.json`.
2. **Builder is deterministic + offline.** Same inputs → byte-identical output
   (sorted keys, no timestamps in the payload body — provenance dates live in a
   dedicated `provenance` block). Precedent: `build_dose_reference.py` docstring
   ("same corpus yields a byte-identical JSON").
3. **Artifact is versioned + committed + hash-pinned.** Filename carries `_vN`;
   the builder prints a SHA-256 of the output; the version participates in cache
   keys (extend the existing `corpus_version` mechanism, `config.py:65`).
4. **Loader fails open.** Missing/corrupt/empty artifact → feature inert
   (returns `None`), never a 500. Precedent: `calendar_store.load_crop_calendars`.
5. **No fabricated rows, ever.** An unextractable value is absent, not invented
   (AGENTS.md rule 5; the soil-honesty lesson in PROJECT_HANDOFF).
6. **Rejections are archived, not deleted.** Extraction candidates that fail
   validation are written to a `rejected/` sibling for the paper's error
   analysis, never silently dropped.

## Scope — create
- `docs/production_readiness/KNOWLEDGE_INGESTION_CONTRACT.md` — the 6 clauses
  above, the two reference implementations, and a "new asset checklist".
- `backend/app/infrastructure/ingestion/__init__.py` +
  `backend/app/infrastructure/ingestion/contract.py` — small shared helpers:
  `sha256_of(path)`, `write_deterministic_json(path, payload)` (sorted,
  `ensure_ascii=False`, trailing newline, no in-body timestamp),
  `load_fail_open(path, validate) -> T | None`, and an `ArtifactProvenance`
  dataclass (`source_id`, `endpoint_or_file`, `fetched_at`, `builder`,
  `sha256`). These extract the duplication already present in the two examples.
- `backend/tests/test_ingestion_contract.py`.

## Scope — modify
- `backend/scripts/build_dose_reference.py` + `build_crop_calendars.py` — refit
  to call the shared helpers (proves the contract fits the existing assets; if
  it does not fit, the contract is wrong, not the assets). **Output artifacts
  must stay byte-identical** — this is a refactor, verified by re-running the
  builders and diffing.

## Do not touch
- The artifact *contents* (`dose_reference_v1.json`, `crop_calendars_v1.json`)
  — only the code path that writes them, and only if the diff is empty.
- Runtime pipeline, API, retrieval, verifier logic.

## Invariants
- Re-running both existing builders produces a **zero-diff** artifact
  (locked: build → `git diff --exit-code` on the two JSON files).
- Loaders keep their exact fail-open behavior (existing dose/calendar tests
  stay green unchanged).
- The contract doc names both reference implementations by path.

## Verification gate (stop/go)
1. `uv run pytest tests/test_ingestion_contract.py tests/test_dose_reference.py
   tests/test_crop_calendar.py -v` — green.
2. `uv run python scripts/build_dose_reference.py; uv run python scripts/build_crop_calendars.py`
   then `git diff --exit-code backend/ml_assets/rag_index/derived/dose_reference_v1.json
   backend/ml_assets/agronomy/crop_calendars_v1.json` — **no diff**.
3. Full `tests/` suite — 410/7/0 baseline held.

## Rollback
`git revert`. Pure refactor + new helper module + doc; no schema, no runtime
contract change.

## External sources
None. This task only touches in-repo data and code.

## Notes for the implementing agent
- This is deliberately small and boring. Its value is the *test* that stops
  future data from leaking into Python. Do not add a new data asset here — R2
  does that, using this contract.
