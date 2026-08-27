# Section 13: Results — Systems Efficiency & Economics (Draft Skeleton)

## 13.1 Zero-LLM Traffic Share
- 5-tier resolution ladder resolves 61.52% of queries without LLM invocation (Layer E18).
- Resolves 51.04% via Tier 1/2 deterministic facts and 10.48% via Tier 0/4 safety handling.

## 13.2 Latency Decomposition
- Weighted average latency reduced from 1,247.9 ms to 546.2 ms (2.28x speedup) (Layer E09).
- Deterministic path executes in <1 ms p95.

## 13.3 Local Serving Economics
- Cost per certified safe advisory (C_safe): $0.0768/1k queries on local VPS vs $2.30/1k on commercial cloud LLM APIs (Layer E20).
- Localized Bangladesh SMS integration: 0.0308 BDT online vs 0.2808 BDT SMS fallback.

## 13.4 Pareto Frontier Analysis
- Multi-objective Pareto optimization across Safety (CUAR), Advisory Coverage, End-to-End Latency, and Cost.
