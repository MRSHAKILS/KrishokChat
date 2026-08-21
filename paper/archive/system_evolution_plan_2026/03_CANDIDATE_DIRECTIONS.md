# Candidate Research Directions

## Scoring

Each dimension uses 1-10. `Evidence`, `Novelty`, `Safety`, `Bangladesh`, and `Publishability` score upward. `Cost`, `Data burden`, and `Complexity` also score upward, where **10 means cheaper, less data, and simpler**. `Fit` measures compatibility with current seams. Total is an unweighted sum out of 90; scores guide selection and are not empirical results.

| # | Direction | Evidence | Novelty | Safety | Bangladesh | Publish. | Cost | Data | Complexity | Fit | Total |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Structured claim/dosage relation verifier | 9 | 9 | 10 | 9 | 9 | 7 | 5 | 6 | 10 | 74 |
| 2 | Calibrated risk-coverage abstention | 9 | 8 | 10 | 8 | 9 | 7 | 6 | 6 | 9 | 72 |
| 3 | Dialect retrieval raw vs normalized | 9 | 9 | 8 | 10 | 9 | 8 | 6 | 8 | 9 | 76 |
| 4 | Safety-intent preservation under normalization | 8 | 10 | 10 | 10 | 9 | 8 | 5 | 7 | 9 | 76 |
| 5 | Bengali verifier human meta-evaluation | 9 | 8 | 9 | 9 | 9 | 6 | 4 | 6 | 8 | 68 |
| 6 | Lexical vs LLM vs NLI vs hybrid verifier study | 9 | 8 | 9 | 8 | 9 | 6 | 5 | 6 | 9 | 69 |
| 7 | Dosage denominator and interval extraction | 8 | 9 | 10 | 9 | 8 | 7 | 5 | 6 | 9 | 71 |
| 8 | Safety-router dialect oversensitivity study | 9 | 8 | 10 | 10 | 8 | 8 | 6 | 8 | 9 | 76 |
| 9 | Banglish orthography attack surface | 8 | 8 | 9 | 9 | 8 | 8 | 6 | 8 | 9 | 73 |
| 10 | Retrieval fusion activation and ablation | 9 | 5 | 7 | 7 | 6 | 7 | 7 | 7 | 8 | 63 |
| 11 | Query normalization confidence gate | 8 | 7 | 9 | 9 | 8 | 8 | 6 | 8 | 9 | 72 |
| 12 | Vision treatment evidence-chain repair/eval | 9 | 5 | 10 | 8 | 6 | 8 | 8 | 8 | 10 | 72 |
| 13 | Vision class calibration/OOD rejection | 8 | 6 | 8 | 7 | 7 | 5 | 4 | 5 | 7 | 57 |
| 14 | Helpline referral recall/follow-through | 7 | 9 | 9 | 10 | 9 | 3 | 3 | 4 | 6 | 60 |
| 15 | Farmer trace-stepper trust study | 7 | 7 | 6 | 8 | 7 | 4 | 4 | 6 | 7 | 56 |
| 16 | Latency-grounding tradeoff | 8 | 7 | 6 | 6 | 7 | 6 | 7 | 7 | 8 | 62 |
| 17 | Local 4B model benchmark | 8 | 4 | 5 | 7 | 6 | 4 | 7 | 5 | 8 | 54 |
| 18 | Agricultural chemical knowledge graph | 7 | 7 | 10 | 9 | 7 | 2 | 2 | 3 | 5 | 52 |
| 19 | Multi-agent planner/reviewer expansion | 5 | 2 | 4 | 3 | 3 | 2 | 8 | 2 | 3 | 32 |
| 20 | New object detector/localization study | 8 | 3 | 5 | 5 | 5 | 2 | 2 | 2 | 3 | 35 |

## Selection

- **Build core:** 1-9 and 11, consolidated into Modules A and B.
- **Mandatory engineering prerequisite:** 12.
- **Conditional evaluation:** 10, only after an artifact audit proves dense assets and a fixed benchmark exist.
- **Eight-week extension:** 14 or 15, subject to ethics, recruitment, and expert availability.
- **Defer:** 13, 16-18.
- **Reject:** 19-20 for this paper.

The highest scores cluster around dialect retrieval/safety and typed verification. These directions share data and evaluation infrastructure, so the recommendation remains two modules rather than ten features.
