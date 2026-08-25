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

## Verification gate (stop/go)
1. `uv run python scripts/build_fact_base.py` + `build_fact_pack.py` — new crops
   present, re-run → `git diff --exit-code` clean on the artifacts.
2. `uv run pytest tests/test_fact_base_maize_rice.py tests/test_fact_base.py
   tests/test_structured_resolver.py -v` — green.
3. R4 resolver answers a maize-FAW dose query at T1/T2, `llm_calls=0`, real
   citation, dose within band — via unchanged resolver code.
4. Full `tests/` suite — 410/7/0 baseline held (plus the new tests).
5. Golden replay PASS including the new maize/rice items.
6. **The diff-audit note**: `git diff --stat main` attached to the verification
   record, demonstrating data-only change.

## Rollback
`git revert`; drop the new rows and regenerate. Potato spine is unaffected.

## External sources
- DAE/BARC/BRRI registered-dose references for maize FAW + rice pests — download
  offline, cite by document, ingest via the R1 contract. If the current corpus
  already contains them, extract with `source_node_id`; otherwise seed as
  `curated-approximation` with the real citation, pending corpus ingestion.
- (Longer lane) BAMIS disease-weather calendars for the new crops, per doc 08
  Route C — corpus ingestion, not blocking R12's fact rows.

## Notes for the implementing agent
- This task is a **test of R4's architecture as much as a feature.** Approach it
  as: "add the data, change nothing else, and prove it." If you find yourself
  editing control flow, pause and write down exactly what forced it — that
  finding is more valuable than the crops.
- Keep maize and rice scoped to a *few* well-cited high-value problems (FAW for
  maize is the obvious one; BPH/stem borer for rice). Breadth for its own sake
  dilutes the provenance quality that makes the fact base defensible.
- Doses must be verbatim from the source. Never round, rephrase, or average a
  registered dose to fit a template.
