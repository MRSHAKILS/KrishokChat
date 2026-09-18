# PRISM Provenance Audit (P0-7, 2026-09-17)

**Method:** read `experiments/scripts/E49_prism_rag_benchmark/generate_prism_benchmark.py` in full.

## Findings

1. **Generation:** deterministic template × slot-filler combinatorics, `random.seed(20260904)`. Curated slot lists: 7 crops (rice/potato/tomato/brinjal/chilli/wheat/maize × BN/roman forms), 8 locations, formal/colloquial/dialect/Banglish/typo template sets, disease pairs, symptom/pest lists.
2. **No LLM involved.** No human review involved. Labels (`true_crop`, `expected_route`, `expected_answerability`, `needs_clarification`, `best_clarification_question`) are ASSIGNED BY THE GENERATOR from the template arm (e.g., formal Bengali → `document_rag` + `A2_strong_evidence`; underspecified → clarification).
3. **Consequence — circularity bound:** scoring the router against `expected_route` tests conformance to the generator's design mapping, NOT independent accuracy. The mapping itself (which template → which route) is a human design decision encoded in the script, so agreement means "the live system behaves as designed across 1,000 varied queries."
4. **Independent evidence still required:** N01b farmer behavior (real queries, team labels) + E09 pilot remain the non-circular legs. N09 is the scale leg.
5. **Dialect arm honesty:** C_dialect rows are template Bengali with dialectal flavor from curated lists — controlled stress, NOT field-collected dialect. Banglish/typo arms are rule-generated romanizations. Label as such wherever cited.

## Decision

USE for N09 route-conformance scoring with the circularity disclosure above. Never present `expected_route` agreement as independently-validated accuracy.
