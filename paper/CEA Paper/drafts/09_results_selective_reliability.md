# Section 09: Results — Selective Resolution & Uncertainty Calibration (Draft Skeleton)

## 9.1 Risk-Coverage Calibration Analysis
- AURC = 0.0153, ECE = 0.0785 on 20,112 test cases (Layer E04).
- 84.56% coverage under strict <= 1.0% risk budget at threshold theta* = 0.2375 (Table 7).

## 9.2 Lightweight Intent Routing
- Supervised intent router achieves 78.4% joint match in 0.3855 ms (3,242x faster than fine-tuned LLM, 1.25 MB footprint) (Layer E25).

## 9.3 100-Case Failure Containment Taxonomy
- Audit of residual failures (Layer E10, Table 10): 28% retrieval omission, 22% relational misbinding, 14% volume ambiguity, 12% linguistic ambiguity.
- All high-risk failures intercepted by fail-closed verifier into safe abstentions.
