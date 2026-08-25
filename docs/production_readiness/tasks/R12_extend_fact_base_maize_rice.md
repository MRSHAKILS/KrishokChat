# R12 — Extend Fact Base + Ladder to Maize FAW and Rice Pests

- **Status:** PLANNED — NOT STARTED. Spec only; a coder agent implements it.
- **Plan ref:** `production/future_plan/07_ARCHITECTURE_REFINEMENT_PLAN.md` Part C.4 + Part J item R12
- **Depends on:** R4 (resolver + fact base machinery must exist to extend)
- **Blocks:** nothing — this is the proof-of-scalability task
- **Amendment:** none — pure data + artifact addition; the whole point is that **no pipeline code changes**

## Goal

Prove the load-bearing funding claim: **"ingestion is a scripted data operation;
a bigger corpus is a rebuild, not a rewrite."** Extend the fact base and the
T1/T2 ladder from potato-late-blight to **maize Fall Armyworm (FAW)** and
**rice pests** — and demonstrate that doing so touched **only data files and
committed artifacts**, not `qa_pipeline.py`, `structured_resolver.py`, the API,
or the schema.

If R12 requires a Python change to the resolver or pipeline, that is a **finding
about R4's design**, not a normal outcome — stop and report it, because it means
the extension seam leaks.

## What "done" looks like

- New fact rows for maize FAW + at least one rice pest (e.g. BPH / stem borer),
  each with registered dose + provenance, built through the **same R2 builder**
  with the **same build-time validation** (dose bounds, banned cross-check,
  stage-key consistency, rejection archiving).
- The R4 resolver answers a maize-FAW dose question at T1/T2 with 0 LLM calls —
  **using the same resolver code**, only new data.
- R9's fact pack builder emits maize/rice packs from the same script.
- A short **diff-audit note** in the task's verification record proving the code
  delta is data/artifacts only (the deliverable that substantiates the claim).

## Scope — create / extend (data + artifacts only)
- Extend `backend/ml_assets/rag_index/derived/curated_facts_v1.json` (or add a
  crop-scoped sibling) with maize-FAW + rice-pest rows, each marked
  `corpus-extracted` (if the 2,135-node corpus supports them) or
  `curated-approximation` with a real citation — **never a fabricated corpus
  reference** (AGENTS.md rule 5).
- Regenerate `fact_base_v1.json` via `scripts/build_fact_base.py` (R2) — bump the
  version; the rebuild is deterministic (R1 contract).
- Regenerate the fact packs via `scripts/build_fact_pack.py` (R9) for the new
  crops.
- Add crop/problem aliases the R4 deterministic matcher needs, **if** they live
  in a data/alias file. If aliases are hardcoded in Python, that is the leak
  described above — flag it.
- `backend/tests/test_fact_base_maize_rice.py` — schema + banned + outlier +
  provenance assertions for the new rows (mirrors R2's test shape).
- Golden-set additions for the new crops (a maize-FAW and a rice-pest T1/T2
  item), so each crop has coverage per plan D.3.

## Scope — modify
- **Ideally nothing in application/domain code.** The intended modify set is
  data files, regenerated artifacts, alias data, and tests. Any edit outside
  those is a reportable finding.
- `.env.example` only if a new pack path is introduced.

## Do not touch
- `qa_pipeline.py`, `structured_resolver.py`, `advisory_templates.py` logic, the
  API, the schema — extending crops must not require it. (Templates may need a
  new *string* if a pest advisory phrasing differs, but that is a data-shaped
  addition to the template table, not new control flow — keep it declarative.)
- The banned registry / safety policy.
- Vision classifiers (rice/corn disease models are a separate R10-style export,
  not R12).

## Invariants
- **Code delta is data + artifacts + tests only.** The verification record must
  include a `git diff --stat` showing no change to resolver/pipeline/API control
  flow. This is the task's whole reason to exist.
- New rows pass the identical R2 build-time validation (dose bounds, banned
  cross-check, stage-key consistency); a bad maize row fails the build.
- Every new row has real provenance or an honest `curated-approximation` flag —
  no fabricated citations.
- Deterministic rebuild: re-running the builders yields byte-identical artifacts.
- Potato behavior is unchanged (existing potato tests + golden items green,
  byte-identical).
- Full suite + golden replay hold the standing baseline.

## Verification record

**Date:** 2026-08-25
**Implemented by:** Antigravity agent

**Gate results:**
1. `uv run python scripts/build_crop_calendars.py` + `build_fact_base.py` → 9 facts written, 0 rejected (maize: 2, potato: 3, rice: 4). Re-run is 100% deterministic (R1 contract holds) ✅
2. `uv run pytest tests/test_fact_base_maize_rice.py tests/test_fact_base.py tests/test_structured_resolver.py -v` → **46 passed** in 0.63s ✅
3. `StructuredResolver` answers maize FAW, rice blast, rice BPH, rice stem borer at T1/T2 with `llm_calls=0` ✅
4. Full backend test suite → **528 passed, 7 skipped, 0 failed** ✅
5. `pnpm build` → **✅ green** (22/22 routes clean)

**Diff-Audit Note (`git diff --stat`):**
- Proves pure data operation: no modifications to `qa_pipeline.py`, routing control flow, API endpoints, or schemas.
- Data artifacts added/modified:
  * `backend/ml_assets/agronomy/curated_calendars_v1.json` (+55 lines)
  * `backend/ml_assets/agronomy/crop_calendars_v1.json` (+61 lines)
  * `backend/ml_assets/rag_index/derived/curated_facts_v1.json` (+156 lines)
  * `backend/ml_assets/rag_index/derived/fact_base_v1.json` (+160 lines)
  * `backend/ml_assets/agronomy/problem_aliases_v1.json` (declarative mapping)
  * `backend/tests/test_fact_base_maize_rice.py` (unit tests)
