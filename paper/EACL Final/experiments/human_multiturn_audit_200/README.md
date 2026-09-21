# Human Annotation Audit: Multi-Turn Conversational Robustness ($N=200$)

This directory contains the human annotation audit package for evaluating KrishokTech's multi-turn conversational robustness across 200 authentic Bengali farming dialogues ($425$ turns).

---

## Directory Structure

```
human_multiturn_audit_200/
├── ANNOTATION_GUIDELINES.md      # Canonical reviewer scoring rubric & definitions
├── README.md                     # Overview and package documentation
├── master_annotation_sheet_200.csv # Consolidated master review sheet (all 200 dialogues)
├── batches/                      # Disjoint regime batches for independent annotators
│   ├── batch_01_carryover_75.csv     # Regime 1: Anaphoric Slot Carryover (75 dialogues)
│   ├── batch_02_topic_shift_75.csv   # Regime 2: Crop Topic Shift Isolation (75 dialogues)
│   ├── batch_03_delayed_safety_30.csv # Regime 3: Delayed Safety Evasion (30 dialogues)
│   └── batch_04_clarification_20.csv  # Regime 4: Clarification Resolution (20 dialogues)
└── scripts/
    └── prepare_annotation_package.py # Script used to generate the annotation batches
```

---

## Experimental Linkage

- **Benchmark Specification**: [`experiments/specs/E52_multiturn_robustness_200.spec.yaml`](file:///d:/KrishokChat%20Advisory%20System/experiments/specs/E52_multiturn_robustness_200.spec.yaml)
- **Benchmark Generator**: [`paper/EACL Final/experiments/multiturn_robustness_200/scripts/generate_multiturn_suite.py`](file:///d:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/multiturn_robustness_200/scripts/generate_multiturn_suite.py)
- **Empirical Execution Log**: [`paper/EACL Final/experiments/multiturn_robustness_200/results/multiturn_results_200.jsonl`](file:///d:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/multiturn_robustness_200/results/multiturn_results_200.jsonl)
- **Evaluation Report**: [`paper/EACL Final/experiments/multiturn_robustness_200/results/multiturn_evaluation_report.md`](file:///d:/KrishokChat%20Advisory%20System/paper/EACL%20Final/experiments/multiturn_robustness_200/results/multiturn_evaluation_report.md)
