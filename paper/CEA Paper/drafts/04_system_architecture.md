# Section 04: Bounded-Authority Advisory Architecture (Draft Skeleton)

## 4.1 Architectural Overview
- Five functional tiers: Tier 0 (Risk Gate), Tier 1 (Router), Tier 2 (Fact Store), Tier 3 (Generator), Tier 4 (Verifier).
- End-to-end dataflow diagram (Figure 1).

## 4.2 Multimodal Perception & Search-Space Reduction
- INT8 ONNX crop and disease classification.
- Collapse of candidate knowledge nodes from 2,135 to 516.4 (-75.64% reduction at threshold tau = 0.80).

## 4.3 Five-Tier Selective Resolution Ladder
- Tier 0: Static safety redirects (0 ms LLM latency).
- Tier 1: Deterministic structured entity resolution.
- Tier 2: Pre-verified localized template rendering.
- Tier 3: Grounded fine-tuned Gemma-4 4-bit generation under single-record constraints.
- Tier 4: Fail-closed abstention and Krishi Call Center (16123) escalation.

## 4.4 Relational Verifier Implementation
- Candidate tuple extraction from Bengali output.
- Field-by-field joint matching against retrieved evidence hash.
- Fail-closed suppression on any slot discrepancy.
