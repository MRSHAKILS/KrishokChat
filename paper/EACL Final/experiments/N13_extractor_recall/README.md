# N13 — T1 Extractor Recall Upgrade (REAL_MEASURED, offline, $0)

**Status:** REAL_MEASURED · **Track:** EACL Final, beat B (missing slots) ·
Reviewer-driven fix for the 47.5% T1 extractor miss rate.

## What this experiment answers

Can the miss rate be driven below 10% without raising false positives —
and *which lever* actually moves it (taxonomy vs fuzzy vs normalization)?

## Key finding up front

The miss audit showed **~99% of misses are crops entirely outside the
9-crop gazetteer** (mango, mustard, coconut, …), not spelling variants of
known crops. A fuzzy-match layer alone would fix ~0 of 95 misses. The fix
is therefore **taxonomy expansion first**, fuzzy second. The ablation below
proves it.

## Folder structure

```
N13_extractor_recall/
  README.md                        this file
  spec.yaml                        frozen design + locked results
  data/
    crop_alias_v2.json             frozen v2.2 alias table (45 crops) + rationale
  scripts/
    run_n13.py                     layered ablation runner (offline, deterministic)
  results/
    n13_records_<stamp>.jsonl      per-row, per-layer (atomic rewrite)
    n13_summary_<stamp>.json       aggregates + ablation + attribution
```

Frozen rule: `backend/app/domain/` is untouched — N13 runs standalone
against `crop_slot_labeling_sheet_200.json` (same 200 queries as N01b).

## Layers

| Layer | Content |
|---|---|
| L0 baseline | Production `QueryExtractor.extract`, frozen backend code |
| L1 taxonomy | v2 table (9 existing + 36 new crops), same exact/token-start rule |
| L2 +norm | L1 + NFKC/lowercase normalization |
| L3 +fuzzy | L2 + rapidfuzz fallback (ratio≥90, token≥4, alias≥4, same first char; করলা-series excluded — collides with common করার at 88.9) |

Safety-critical matching rules (kept from production, extended):

- Single-word aliases match at token start (Bengali vowel signs defeat `\b`);
  multi-word aliases match by substring.
- 2-character aliases (`আম`, `জাম`, `আতা`) are **exact-match only** with
  explicit inflected forms — otherwise pronouns (`আমার/আমি`) and common
  words (`জামা`) flood in as false positives.
- Bare `pat` dropped (collides with `pata`/leaf, `patch`, `Patnitola`);
  jute uses explicit forms instead. Bare `হলুদ*` dropped (it is
  predominantly the color/symptom "yellow", not turmeric).
- Generic collective `শাকসবজি` (vegetables) is a negative token — never a crop.
- `grass` removed: weed-control queries dominate and no grass manual exists
  in the 2,135-node scope (1 grass miss accepted, disclosed).

## How to run

```bash
# Offline, deterministic, $0, no API calls (preflight N/A — no inference)
python3 scripts/run_n13.py
```

## Locked results (2026-09-19, n=200 paired, Wilson 95% CI)

| Layer | Agree | Miss | Mismatch | FP |
|---|---|---|---|---|
| L0 baseline | 104 | 95 (47.5% [40.7, 54.4]) | 0 | 1 |
| L1 taxonomy | 191 | **3 (1.5% [0.5, 4.3])** | 0 | 6 |
| L2 +norm | 191 | 3 (1.5%) | 0 | 6 |
| L3 +fuzzy | 191 | 3 (1.5%) | 0 | 6 |

- **First-fix attribution:** all 92 fixes at L1; L2/L3 add zero fixes and
  (at threshold 90) zero FPs. Fuzzy stays as insurance for unseen spelling
  variants, not as a measured contributor on this set.
- **Regressions vs L0:** 0 — every query the old extractor got right still
  resolves identically.
- **Residual misses (3, all disclosed):** `farmer_q_63` (implicit "Aman
  season" rice — season→crop inference deliberately not attempted);
  `farmer_q_57` (bare-হলুদ turmeric — color/symptom ambiguity rejected by
  design); `farmer_q_79` (grass — dropped by scoping rationale above).
- **FP 1→6, all audited:** every one contains a genuine crop mention —
  multi-crop selection (q_23, q_232, q_678, q_734), sourcing (q_992), or
  business (q_989) queries labeled EMPTY by convention. None is a
  wrong-crop extraction on a treatment query (the safety-relevant FP
  class, which stays at 0 — the old substring-collision class is gone).

## Reading guide for the paper

- Reportable headline: **miss 47.5% → 1.5%** with mismatch 0 and zero
  regressions, fix attributed to taxonomy expansion (ablation-proven).
- Report honestly alongside: closed-set development (alias table built
  against the same 200; independent held-out validation = listed
  follow-up), FP convention analysis above, and the 3 disclosed residual
  misses.
- **Consequence:** adopting v2 changes N01/N01b operating numbers (bad
  halts fall ~48 → ~15). Paper headline numbers must be re-frozen and
  tables updated — do not mix old gate numbers with the new extractor.

## Provenance

- Alias table, per-record JSONL, and summary JSON are hashable audit
  artifacts under `data/` and `results/`. Re-running `run_n13.py`
  reproduces the summary given the same inputs (only the date stamp
  changes). No network, no spend, no production code touched.
