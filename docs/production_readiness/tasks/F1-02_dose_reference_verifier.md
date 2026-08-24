# F1-02 — Corpus-Derived Registered-Dose Reference for the Verifier

- **Status:** DONE (2026-08-25)
- **Spine step:** "Safety" node of the §10 flagship spine (`production/future_plan/00_SCOPE_OUTLINE.md`)
- **Novelty served:** N1 (dosage/chemical safety grounded in official data) — the piece
  F1-01 explicitly deferred ("nuanced HHP handling belongs to a later verifier-side task").
- **Depends on:** F1-01 (done) — same registry-grounding philosophy, verifier side.
- **Blocks:** nothing.
- **Amendment:** none — no hard-rule change; additive verifier capability, offline-built
  artifact loaded from disk (rule 2 respected: nothing built at request time).

## Goal

Today `HardenedDosageVerifier` checks dosage claims only by **passage entailment** (the
amount+unit and chemical must appear in a retrieved passage). If a retrieved passage — or
a poisoned/low-quality source — itself contains an excessive rate, the verifier certifies
it. F1-02 adds a second, independent check: a **dose reference extracted offline from the
cited BARC corpus nodes** (26 nodes pair a pesticide active with a numeric rate, each with
a citation, e.g. "Cypermethrin 1 ml/l of water", "Admire 200 SL @ 0.25 ml/litre"). When an
answer's dosage claim exceeds the referenced band for that active by a gross factor
(default ≥3×), the verifier flags it and the sentence is annotate-and-dropped — exactly the
existing philosophy, now with structured knowledge instead of entailment alone.

## Data honesty rule (AGENTS.md §2.5)

Every reference entry must be **extracted from an in-repo corpus node with its citation**.
No external dose table, no remembered values, no invented ranges. The extractor is
deterministic and its output is committed and reviewable; the task reports the exact node
count. Where the corpus has no rate for an active, there is no entry — the check simply
does not fire (fail-open to today's behavior).

## Scope decision

- **Only spray-rate bands (per-litre) and per-hectare rates** are extracted — the forms
  the corpus actually contains. Fertilizer kg/ha recommendations are EXCLUDED (different
  semantics; the entailment check already covers them; fertilizer overdose is not the N1
  safety story).
- Conservative outlier rule: same-unit comparison only (ml vs ml/l, g vs g/l, kg vs kg/ha),
  denominator context required in the claim sentence (প্রতি লিটার / লিটার পানিতে /
  per litre / ml per / প্রতি হেক্টর / per hectare / a.i/ha …). No context → no flag.
- No new hard blocks. Outlier flags ride the existing `flags` / `unverified_claims` /
  annotate-and-drop path. A missing or unloadable reference file disables the check with
  one warning (demo can never break because of it).

## Scope — create
- `backend/scripts/build_dose_reference.py` (offline extractor; deterministic output)
- `backend/ml_assets/rag_index/derived/dose_reference_v1.json` (committed artifact)
- `backend/app/infrastructure/verification/dose_reference.py` (loader + outlier check)
- `backend/tests/test_dose_reference.py`

## Scope — modify
- `backend/app/application/verifier.py` (optional `dose_reference` constructor param; additive flag path)
- `backend/app/application/container.py` (load reference from settings, wire verifier)
- `backend/app/core/config.py` + `.env.example` (`DOSE_REFERENCE_PATH`, `DOSE_OUTLIER_FACTOR=3.0`)

## Do not touch
- Canned responses, precheck ordering, coverage gate (F1-01 lanes)
- `claim_grounded` / entailment semantics for non-outlier claims
- `dataset_release/`, `paper/`, `frontend/`

## Invariants
- Golden replay stays 50/50 PASS with identical invariants (no new flags on clean items).
- A verifier built without a reference behaves byte-identically to today (tests lock this).
- Every flag names the active, the claimed amount, and the referenced max + citation source.

## Verification gate (stop/go)
1. `uv run pytest tests/test_dose_reference.py tests/test_pipeline.py -v` — green.
2. Full `tests/` suite — no regressions vs the F1-01 baseline (337 passed / 7 skipped /
   2 pre-existing env failures).
3. Golden replay 50/50 invariants PASS, flag counts unchanged.
4. Spot-check: a ≥3× overdose answer sentence is flagged+dropped even when a poisoned
   source "grounds" it; a within-band answer is untouched; an answer with no litre/ha
   context is untouched.

## Rollback
`git revert` — the reference file is additive, the constructor param defaults to None, and
`DOSE_REFERENCE_PATH=` + missing file both disable the check. No schema, no migration.

## Completion log (2026-08-25)

- Delivered `backend/scripts/build_dose_reference.py` (thin CLI) +
  `app/infrastructure/verification/dose_reference.py` (extraction logic,
  `DoseReference` loader, conservative `outlier_details` check) +
  committed artifact `ml_assets/rag_index/derived/dose_reference_v1.json`
  (**71 entries, 15 actives**, every entry with node id + citation + snippet).
  Sources surfaced by the extraction: DAE *List of Registered Agricultural
  Pesticides* pages (real registered-product dosage tables) + BARC Hand Book
  passages. Trade-name aliases restricted to corpus-attested ones (Admire,
  Imitaf, Dursban, Furadan, Tracer, Virtako, Karate; incl. the corpus typo
  "imidachlorpid").
- `HardenedDosageVerifier` gained an optional `dose_reference` param; a
  claim that passes entailment but is a gross outlier (≥ `DOSE_OUTLIER_FACTOR`
  × band max, same unit, explicit per-litre/per-HECTARE context; একর is
  deliberately NOT hectare) is treated as unsupported → flag + annotate-and-drop.
  Default-constructed verifiers are byte-identical to pre-F1-02 (locked by test).
- Container loads the reference from `settings.dose_reference_resolved_path`
  (default `rag_index/derived/dose_reference_v1.json`); missing/broken file ⇒
  warning + check disabled. `DOSE_REFERENCE_PATH` + `DOSE_OUTLIER_FACTOR=3.0`
  in config + `.env.example`.

### Known extraction caveats (audited, fail-safe direction)
- A few proximity misbindings exist in table-style text (e.g. a soap-water
  "5 g/l" bound to imidacloprid where Admire's real 0.25 ml/l stands nearby;
  carbaryl's "2 g/l" bound to dimethoate). Every misbinding found inflates a
  band MAX (⇒ fewer flags, never a false flag on a legitimate rate); no band
  was found suspiciously low. All entries carry snippet + citation so any
  entry can be audited by hand.
- Carbofuran bands (30/60 kg/ha granule rates) are effectively inert: F1-01
  blocks carbofuran/furadan queries before retrieval.

### Verification evidence
1. `tests/test_dose_reference.py` — 20 passed (extraction well-formedness vs
   the real corpus, determinism, committed-artifact freshness, loader
   fail-open, outlier-rule conservativeness incl. acre≠hectare + Bengali
   প্রতি লিটার context, poisoned-source overdose flagged+dropped, default
   verifier equivalence, settings defaults).
2. Full `tests/` suite — **358 passed, 7 skipped, 2 failed** (the two
   documented pre-existing environmental failures: auth JWKS, soil lock;
   identical to the F1-01 baseline otherwise). The SSE-heartbeat test now
   runs un-deselected and passes.
3. Golden replay — **50/50 invariants PASS**, flag counts unchanged
   (6/6 flag-worthy carry flags, zero new flags on clean items).
4. Spot-checks are locked as tests (see 1): ≥3× overdose with per-litre
   context flagged even when a poisoned retrieved source "grounds" it;
   within-band untouched; no-context untouched.
