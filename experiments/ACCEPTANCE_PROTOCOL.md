# Experiment Acceptance Protocol — run → verify → real-app check → freeze → accept

Every layer in `registry.yaml` is executed under this protocol. A result that skips any step is
not accepted and must not enter the manuscript or the claim ledger.

## 1. Config convention (no duplication)
The spec YAML in `specs/<layer>.spec.yaml` is the single config: runners READ the spec file at
runtime (paths, seeds, thresholds, conditions). No parallel config files. Anything the runner needs
that isn't in the spec gets added to the spec first (dated), then run.

## 2. Run rules
- One layer per branch: `experiment/E<NN>_<name>`.
- Pin the commit: record `git rev-parse HEAD` into the result YAML at run time.
- Seeds: from the spec (default 20260827). Any rerun with a changed seed is a new result file (`_r2`, `_r3`), never an overwrite.
- Environment recorded: python version, key package versions, OS, CPU.
- No temp files: intermediates go to a `work/` dir inside the layer's scripts folder, which is
  gitignored; only the final YAML (+ declared artifacts) lands in `results/<layer>/`.

## 3. Result file contract
Every result is `results/<ELAYER>/e<NN>_results.yaml` following `results/RESULT_SCHEMA_TEMPLATE.yaml`:
meta (script, commit, seed, date, duration), environment, parameters echo, metrics, per-metric
verification, and the acceptance block.

## 4. Verification steps (all mandatory, recorded in the result YAML)
1. **Self-checks:** the runner's internal asserts — schema conformance, metric bounds (e.g.
   probabilities in [0,1], counts sum to n), spec safety gates (e.g. E22 template arm == 0.0).
2. **Determinism check:** rerun a 10% sample with the same seed; metric deltas must be 0 (or
   within declared stochastic tolerance for LLM-bearing arms, with the tolerance stated).
3. **Real-application check (the "checked by real application" gate):** the measured behavior must
   be validated against the live system, not only the offline harness — at minimum:
   - full backend test suite passes (standing baseline: 410 passed / 7 skipped / 0 failed),
   - golden replay 50/50 green,
   - `pnpm build` green,
   - plus one layer-specific integration probe defined in the spec (e.g. E14: reproduce one
     degraded-network delivery against the running FastAPI process; E15: one real tuple rendered
     through the actual pack builder; E17: one detection-gated query through the live API).
   The probe commands + outputs are stored in the result YAML.
4. **Trace check:** every number in the YAML is computable from stored raw outputs (paths listed);
   a reviewer re-running the script from the same commit must reproduce the metrics.

## 5. Freeze and accept
- Freeze = result YAML written, verification block complete, `registry.yaml` status flips to `done`
  with the results path, and a claim-ledger entry (S/F/U ID) is added/updated in the manuscript lane.
- Accepted = the author (human) reviews the verification block and marks
  `acceptance.accepted_by` with date. Until then the layer counts as `done_unverified` in the registry.
- Post-freeze edits are forbidden; corrections happen in a new dated result file.

## 6. Standing regression guard
Any routing-threshold or pipeline change made by an experiment re-runs the golden replay; drift is
reported in the layer's result YAML (`golden_replay_drift` field). Zero drift required for freeze.
