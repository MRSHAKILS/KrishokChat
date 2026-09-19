# N05 — SMS Survival (LOCKED, critic-audited) + N05c LLM Baseline

**Status:** REAL_MEASURED · **Track:** EACL Final, beats C+G (constrained delivery)

## What this experiment answers

Can safety-critical dosage content survive the 160-character SMS channel, and
is the deterministic 11-slot compressor *necessary* — not just better than
naive truncation, but better than (or equal to) an actual LLM summarizer?

## Folder structure

```
N05_sms_survival/
  README.md                        this file
  spec.yaml                        frozen design + locked results (N05a/b + N05c)
  results_live.json / .jsonl       N05 live arm, frozen 2026-09-17 (DO NOT EDIT)
  results_offline.json             N05 offline arm, frozen (DO NOT EDIT)
  scripts/
    run_n05_sms.py                 N05a/b runner (offline + live endpoint). Frozen.
    evaluate_sms_survival_84.py    N05 vs compressor on 84 live cases. Frozen.
    run_n05c_llm_summarizer.py     N05c runner: samples 100, calls the LLM once
                                   per advisory, fsyncs every record. Spends ~$0.01.
    score_n05c.py                  N05c scorer: recomputes naive + LLM +
                                   compressor arms deterministically. Free ($0).
  results/
    n05c_sample_100.json           frozen sample manifest (row_ids + texts)
    n05c_records_<stamp>.jsonl     per-record LLM outputs (fsync'd at write)
    n05c_summary_<stamp>.json      aggregate rates + Wilson 95% CIs
```

Frozen files are never edited in place. New work adds new dated files.

## Arms

| Arm | Method | n |
|---|---|---|
| N05a offline | stub endpoint, 300 queries | 300 |
| N05b live | production endpoint via OpenRouter (`gemini-2.5-flash-lite`), 100 queries | 100 |
| N05c naive | hard truncation `gold[:avail]` + DAE prefix + helpline suffix | 100 |
| N05c llm | Gemini Flash Lite summary, reviewer prompt + "no preamble" clause | 100 |
| N05c compressor | deterministic 11-slot `SMSCompressor` from the gold answer | 100 |

N05c uses the **same 100 advisories for all three arms** (paired by `row_id`)
and the **same frozen detectors** (`DOSE_RE`, chemical lexicon mirrored from
`run_n05_sms.py`), so cross-arm differences are method effects, not
measurement artifacts.

## N05c sample

Pool = advisories in `backend/ml_assets/rag_index/eval/farmer_benchmark_1000.jsonl`
with `len(gold_answer) > 160` **and** a dose pattern → **652 eligible**.
Sample = `random.Random(42).sample(pool, 100)`, frozen in
`results/n05c_sample_100.json`.

## Metrics (all deterministic — no LLM judge)

- **Length:** `len(text) <= 160` characters (Bengali is non-GSM7; characters,
  never segments — same convention as N05).
- **Dose survival:** frozen `DOSE_RE` matches the summary.
- **Chemical survival:** frozen lexicon substring match.
- **Hallucination** (LLM arm only): a dose `(number, unit)` pair or chemical
  token in the summary that is **absent from the source advisory**.
  Bengali digits are normalized to ASCII and bn↔en unit synonyms are unified
  first (`মিলি`↔`ml`, etc.), so genuine translations are not flagged.
  Spelling variants are unified too (urea `ইউরিয়া`/`ইউরিয়া`).

## How to run

```bash
# 0. Smoke test — prints the exact prompts for the first 2 rows, spends $0
python3 scripts/run_n05c_llm_summarizer.py --smoke

# 1. (optional) Freeze the sample manifest without spending
python3 scripts/run_n05c_llm_summarizer.py --sample-only

# 2. Live run — 100 OpenRouter calls (~$0.01). Preflight auth is enforced
#    in-runner; aborts after >20 consecutive API errors; every record fsync'd.
python3 scripts/run_n05c_llm_summarizer.py --n 100 --seed 42

# 3. Score all three arms — deterministic, free, re-runnable
python3 scripts/score_n05c.py
```

Money rules (AGENTS.md §0.1): preflight 1-token auth check before any live
call; per-record `flush()` + `os.fsync()`; FREE_ONLY with error-pause;
`max_output_tokens=500` cloud cap; model fixed to the paper's frozen
benchmark (`google/gemini-2.5-flash-lite`).

## Locked results (2026-09-19, n=100 paired, Wilson 95% CI)

| Metric | Naive truncation | LLM summarizer | Deterministic compressor |
|---|---|---|---|
| Dose survival | 23/100 [15.8, 32.2] | 89/100 [81.4, 93.8] | **92/100 [85.0, 95.9]** |
| Chemical survival | 20/100 | 56/100 | 34/100 |
| Length ≤160 | 100/100 | 98/100 (2 violations) | **100/100** |
| Hallucinated dose | n/a (copies text) | **2 records** (1 genuine + 1 borderline) | 0 by construction |

Autopsy of the 2 flagged LLM records:

- `farmer_q_608` — **genuine invention.** Source discusses urea only
  qualitatively (splits, guti urea; no numeric amount anywhere in 2,061
  chars). Summary states "৮০০-১০০০ গ্রাম" (800–1000 g) per shotangsho.
  A fabricated dosage on a safety-critical channel.
- `farmer_q_304` — **borderline paraphrase, disclosed not claimed.**
  Source "প্রতি লিটার পানিতে ১ গ্রাম" (1 g per litre) rendered as
  "১ লিটার জলে ১ গ্রাম" (1 g in 1 litre). Semantically identical;
  flagged only because the source lacks an explicit numeral.

Chemical retention favors the LLM (56 vs 34) and is reported honestly:
the 11-slot template prioritizes dose / interval / PHI / referral slots,
so chemical names can be displaced. The certified compressor claim stays
**dose/interval/PHI slot survival** (100% on 1,000 tuples, 65/66 live
gold) — never chemical-name retention.

## Reading guide for the paper

- The LLM is a *strong* baseline (89% dose) — the result is not "LLM fails."
  The claim it supports is the **guarantee** story: the compressor matches
  the LLM on dose (92 vs 89), never violates length (100 vs 98), never
  invents numbers (0 vs ≥1 genuine invention), and runs offline at zero
  marginal cost.
- Appendix E home: Delivery appendix → SMS Enforcement subsection; add the
  3-arm table + 2 sentences in §5.3. Body cost ≈ 30 words.

## Provenance

- Sample manifest, per-record JSONL, and summary JSON are hashable audit
  artifacts under `results/`. Scoring script is deterministic — re-running
  `score_n05c.py` reproduces `n05c_summary_*.json` byte-for-byte given the
  same inputs (only the date stamp in the filename changes).
- Live spend 2026-09-19: 100/100 calls ok, 0 failures.
