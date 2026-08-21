# Annotation Toolkit — Stage A support (KrishokChat Expert Systems paper)

Tooling for the human-evaluation critical path (Stage A in
`paper/manuscript/README.md` → Execution order). Goal: when annotators are
recruited, labeling starts same-day and the agreement gate is computed
same-evening with zero engineering lag.

## Files (frozen inputs staged from `paper/archive/system_evolution_plan_2026/...`)

| Path | What |
|---|---|
| `research_artifacts/datasets/frozen/T07_claim_schema_v1.json` | frozen claim schema (verbatim copy) |
| `research_artifacts/annotations/guidelines/T07_{protocol,label_manual,risk_taxonomy}_v1.md` | frozen guidelines (verbatim copies) |
| `research_artifacts/annotations/pilot/T08_pilot_items_v1.jsonl` | 24 dev-only pilot items |
| `research_artifacts/annotations/labels/` | per-annotator task + label files (generated / filled) |
| `tools/annotation/make_labeling_task.py` | generates blind per-annotator tasks |
| `tools/annotation/compute_agreement.py` | percent agreement + Scott's pi (informational) and **the gate alpha** |

## Stage A workflow

```powershell
# A3 — generate blind tasks (independent shuffles; identical item sets)
python tools/annotation/make_labeling_task.py `
  --pilot research_artifacts/annotations/pilot/T08_pilot_items_v1.jsonl `
  --out-dir research_artifacts/annotations/labels `
  --annotators annotator_A,annotator_B --seed 20260813

# ... annotators fill the "label" field in their task file ...

# A4 — compute the gate (Krippendorff alpha >= 0.70, protocol v1)
uv run --with krippendorff python tools/annotation/compute_agreement.py `
  --a research_artifacts/annotations/labels/task_annotator_A.jsonl `
  --b research_artifacts/annotations/labels/task_annotator_B.jsonl
```

Exit codes: `0` PASS, `1` FAIL, `2` reference package unavailable.

## Two hard-won rules baked into the tooling

1. **Authority**: the gate number comes ONLY from the maintained
   `krippendorff` package (v0.8.2 at recording). This repo implements no
   alpha math. Scott's pi is printed for information; it is a DIFFERENT
   coefficient (worked example: alpha = -0.40 vs pi = -0.60) and can never
   pass the gate.
2. **Orientation**: `krippendorff.alpha` expects `(M raters, N units)` — one
   row per annotator. Feeding per-unit pairs silently transposes the matrix:
   perfect agreement scores `-0.5`. The selftest pins both orientations of a
   worked example (`perfect=1.0`, `worked=-0.4`, transposed tripwire) so this
   trap cannot return unnoticed.
