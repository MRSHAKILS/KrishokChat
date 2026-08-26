# experiments/ — experiment organization root

```
experiments/
├── README.md                             # this file
├── registry.yaml                         # canonical trace of ALL layers E02–E26 (done + planned),
│                                         #   resolves every conflicting E-numbering from older docs
├── ACCEPTANCE_PROTOCOL.md                # run → verify → real-app check → freeze → accept (mandatory)
├── IMPLEMENTATION_AND_AGGREGATION_PLAN.md# execution order, feasibility, manuscript aggregation map
├── .gitignore                            # keeps temp/intermediate files out of git
├── specs/                                # ONE YAML spec per planned layer — design AND runtime config
│   └── E14…E26 *.spec.yaml
├── scripts/<ELAYER>/                     # dedicated runner folder per layer (run_eNN.py + helpers;
│                                         #   scratch lives in gitignored scripts/<layer>/work/)
└── results/
    ├── RESULT_SCHEMA_TEMPLATE.yaml       # frozen-result contract (meta/verification/acceptance blocks)
    └── <ELAYER>/e<NN>_results.yaml       # frozen results; acceptance.accepted_by=PENDING until signed
```

## How done vs planned layers are organized
- **Planned layers (E14–E26):** spec in `specs/`, runner folder in `scripts/`, frozen result in
  `results/` — one folder per layer, created up front so nothing is ever improvised at run time.
- **Completed battery (E02–E13 + R7):** runners live in `research_artifacts/scripts/runners/`,
  frozen YAMLs in `research_artifacts/evaluations/` — mapped and traced in `registry.yaml`
  (`completed_layers`). They are not copied here; the registry is the single index.

## Config policy
The spec file is the config. Runners read `specs/<layer>.spec.yaml` at runtime — no duplicate
config files, no untracked parameters.

## Lifecycle (per layer)
spec → branch `experiment/E<NN>_<name>` → runner → self-checks + determinism check +
real-application check (backend suite, golden replay, pnpm build, layer probe) → frozen YAML per
template → registry status `done_unverified` → author signs `acceptance.accepted_by` → `done`.
Targets in specs are hypotheses; only values in frozen result YAMLs are results.
