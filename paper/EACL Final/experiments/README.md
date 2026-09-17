# EACL Final Experiments — Index

**What this is:** the clean, traceable experiment codebase. Every folder = one validation with `spec.yaml` (machine contract) + `README.md` (human doc); completed folders also carry frozen `results.json` copies. **Root SSOT:** `ground_truth.yaml` — the only place headline numbers live.

## ID scheme

- **E01–E10** — carried from the Demo track (traceability). E02 is SUPERSEDED, E09 is PILOT-demoted; both say so on their doors.
- **N01–N10** — new validations built for Final under the real-data doctrine. No results yet; specs are the work orders.

## Status legend (REAL_DATA_DOCTRINE §6)

REAL_MEASURED · REAL_MEASURED_SMALLN · REAL_MEASURED_PROXY · REAL_MEASURED_MIX_MODELED_COST · REAL_MEASURED_WITH_CROSS_TRACK_BASELINES · REAL_MEASURED_DETERMINISTIC_AND_SIMULATED · PILOT · SUPERSEDED_PENDING_RERUN · PENDING.

## Rules for agents

1. Read the folder's `spec.yaml` before touching anything; obey its gates and bans.
2. Never edit a frozen `results.json`. New runs write to `results/` (root) with a new filename, then the folder spec + `ground_truth.yaml` are updated together.
3. Every number committed here needs: runner path + command + git HEAD + dataset hash + n/seed + status label.
4. Real-data doctrine applies: real queries, real runs, real API where designed, CI-meaningful sizes. Templates are pilots; constants and assumptions are banned from headline numbers.
5. plans/ holds the story; experiments/ holds the evidence. Application code never reads either at runtime.
