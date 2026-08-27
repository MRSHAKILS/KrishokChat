# Section 07: Results — End-to-End Advisory Quality (Draft Skeleton)

## 7.1 Overall Correctness & Certified Advisory Precision
- BAA achieves 97.2% Certified Advisory Correctness (CAC) vs 54.2% LLM-Only and 68.6% Vanilla RAG (Table 5).
- B4 deterministic baseline achieves 98.4% CAC but suffers from low coverage (51.4%).
- BAA bridges this gap with 65.8% advisory coverage.

## 7.2 Critical Unsafe Acceptance Rate (CUAR)
- BAA achieves 0.0% CUAR (0/4,000 unsafe events certified, 95% Wilson CI: [0.00%, 0.09%]).
- LLM-only accepts 28.4% dangerous errors; Vanilla RAG accepts 18.2%; RAG + LLM Judge accepts 6.8%.

## 7.3 Safe Abstention & Escalation Performance
- 34.2% safe abstention on ambiguous/out-of-domain queries.
- 98.6% appropriate abstention rate under expert agronomist consensus.
