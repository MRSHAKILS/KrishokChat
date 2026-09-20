# N14 — Headline Safety on the Deployed Local Model

**Status:** RUNNING · **Track:** EACL Final, beat F (safety) · Reviewer Item A

## What this experiment answers

E03/N12 measured guarded-vs-unguarded ASR on cloud models (Gemini Flash Lite
vs GPT-4o-mini). N14 replicates the **same** design on the production
artifact, `krishokchat-4b` (Gemma3 4.3B Q4_K_M, local Ollama), so the
guarded-vs-unguarded comparison isolates the guard's contribution **on the
deployed model itself**.

## Arms

| Arm | Model | Prompt |
|---|---|---|
| **guarded** | krishokchat-4b (localhost) | E03 safety system prompt, verbatim |
| **unguarded** | krishokchat-4b (localhost) | E03 neutral prompt, verbatim |

280 calls per arm (210 E03 cases across 7 families + 70 N12 native probes
across 7 angles) = **560 calls**, sequential, ~3–4 h CPU. Temperature 0.0,
150 output tokens — identical to E03/N12.

## Folder structure

```
N14_local_model_safety/
  README.md                        this file
  spec.yaml                        frozen design (key filled on completion)
  scripts/
    run_n14_local_safety.py        runner: sequential calls, per-record fsync,
                                   resume-safe, crash-tolerant
  results/
    n14_records_<stamp>.jsonl      per-call (prompt, response, judge, latency)
    n14_summary_<stamp>.json       ASR overall + per family + per N12 angle +
                                   combined Bangla-100, both arms, Wilson CIs
    n14_stdout.log / n14_stderr.log  runner logs
```

## Methodological identity (imported, never reimplemented)

- Attack cases: `build_attack_cases(30)` from `run_e03_safety_screening.py`
  (210) + `build_cases()` from `run_n12_bangla.py` (70).
- Arm prompts: `BASELINES` system prompts verbatim from the E03 runner.
- Judge: `classify_attack_response` verbatim (rule-based, deterministic).
- Stats: `wilson_ci` verbatim.

## Naming note

The E03 source runner labels its guarded arm "BAA". N14 reports that arm as
**guarded** everywhere user-facing. Raw record files retain the source
labels (`BAA_LOCAL`/`UNC_LOCAL`) 1:1 so a restarted run resumes instead of
repeating calls; the summary maps them to guarded/unguarded.

## How to run

```bash
# Smoke: 2 calls (1 E03 + 1 N12 probe, guarded arm), $0
python3 scripts/run_n14_local_safety.py --smoke

# Full: 2 x 280 calls, sequential, ~3-4 h CPU, resumable
# (launch detached; progress = line count of results/n14_records_*.jsonl)
python3 scripts/run_n14_local_safety.py --arm both
```

## Results (locked 2026-09-20, n=280/arm, Wilson 95% CI)

| Arm | Overall ASR | Bangla-100 ASR |
|---|---|---|
| **guarded** (local + safety prompt) | **30/280 = 10.71% [7.61, 14.88]** | **19/100 = 19.0% [12.51, 27.78]** |
| **unguarded** (local, neutral prompt) | 147/280 = 52.5% [46.66, 58.28] | 77/100 = 77.0% [67.85, 84.16] |

Guarded per-family: direct 0/30, evidence 0/30, banglish 0/30, banned 0/30,
bangla-native 5/30, retrieval-poisoning 5/30, delimiter 6/30; N12 angles
1–3/10 each. Local CPU latency p50 ≈ 24 s/call (deployment footnote, not a
paper latency claim).

## Reading guide for the paper (assessed post-run)

**Put it in.** The guard cuts ASR 52.5% → 10.71% on the deployed model
itself — a same-model comparison, methodologically tighter than the
cross-model E03 pair. Absolute guarded ASR is higher than cloud (10.71% vs
0.95%, non-overlapping CIs): report E03 as the architecture result and N14
as the deployment boundary, with abstract and §5.3 stating
model/attack composition explicitly. The Bangla-100 pair (19% vs 77%) is
the operationally relevant headline for a Bengali system. Residuals match
the paper's existing residual-risk narrative; nothing here contradicts E03.
