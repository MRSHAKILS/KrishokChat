# Roadmap: Four to Eight Weeks

## Stages 0-10

| Stage | Objective | Dependency | Gate |
|---:|---|---|---|
| 0 | Reconcile PDFs, datasets, indexes, models, and existing eval artifacts | None | Hashed evidence ledger; all unresolved numbers marked TODO |
| 1 | Freeze current behavior and repair vision evidence labeling | 0 | Regression tests; no source-empty `verified` treatment |
| 2 | Freeze hypotheses, claim schema, risk taxonomy, annotation guide, metrics | 0 | Expert-approved pilot guide and preregistered analysis plan |
| 3 | Build and adjudicate pilot annotations | 2 | Agreement and ambiguity review meet prespecified gate |
| 4 | Build reproducible baseline harness | 0,2 | Lexical/BM25 baselines reproduce from one manifest |
| 5 | Implement and evaluate structured verifier candidates offline | 3,4 | Blind test comparison complete; failure taxonomy written |
| 6 | Fit abstention policy on development data | 5 | Threshold frozen before test; risk-coverage report complete |
| 7 | Build dialect/Banglish paired set and normalization conditions | 2,3 | Native authenticity and intent-preservation audit complete |
| 8 | Run retrieval and safety experiments | 4,7 | Paired statistics and subgroup reports complete |
| 9 | Integrate only passing modules; run system/expert study | 1,6,8 | End-to-end negative paths and expert evaluation pass |
| 10 | Freeze artifacts, paper, limitations, release checklist | 9 | Independent reproduction from manifests |

## Four-week version

### Week 1

Complete Stages 0-2. Locate nested dataset artifacts, extract both authoritative PDFs reproducibly, reconcile counts against stable artifacts, record hashes, freeze schema and primary endpoints, and specify the vision evidence fix.

### Week 2

Complete Stages 3-4. Run expert annotation pilot, revise once, freeze guidelines, build manifests and current lexical/BM25 baselines, and add evidence-regression fixtures.

### Week 3

Complete Stages 5-7. Compare verifier candidates, fit calibration on development data, and finish native review of paired dialect/Banglish queries.

### Week 4

Complete Stage 8 and a bounded Stage 10. Run retrieval/safety experiments, paired statistics, ablations, error analysis, and draft the paper around component results. Runtime integration is conditional; expert evaluation may continue into the eight-week plan.

**Four-week deliverable:** reproducible benchmark and component paper evidence for Modules A and B. No farmer outcome claim.

## Eight-week version

### Weeks 5-6

Complete Stage 9 engineering integration through existing ports. Run negative-path, latency, and end-to-end expert evaluation. Serve only precomputed benchmark artifacts through any future endpoint.

### Weeks 7-8

Run the approved farmer-facing study if all ethics and recruitment gates pass. Otherwise expand expert evaluation and reproduction. Complete Stage 10, archive artifacts, reconcile all tables, and prepare a demo video only after the evidence freeze.

**Eight-week deliverable:** system paper with component causality, expert evidence, and optional bounded user study.

## Critical path

`T01/T02 -> T05 -> T07 -> T12 -> T15 -> T20 -> T23 -> T26`

Dataset location, PDF reconciliation, and expert availability can block this path. Model training is not on the critical path.
