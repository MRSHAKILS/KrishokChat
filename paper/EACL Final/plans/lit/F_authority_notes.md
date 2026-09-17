# Beat F Literature Notes — Verification, Faithfulness, Safety Walls

**Research pass:** 1  
**Cutoff:** 2026-09-17  
**Purpose:** evidence ledger for the Beat F story. This is not paper prose.

## A. Companion evidence (ours, reusable as motivation)

| Source | Evidence to use | Boundary |
|---|---|---|
| `arXiv:2606.29243` (KrishokChat benchmark) | 4.05–7.00% chemical hallucination floor under oracle; Treatment QA <44% all zero-shot; SFT → safety compliance 0.31% | Benchmark finding, not a system result; frame as the problem the system answers |
| E03 `results.json` (420 live calls) | BAA 0.95% [0.26, 3.41] vs unconstrained 36.19% [29.99, 42.88]; Bangla native 6.67% vs 76.67% | n=30/family → wide CIs; report intervals, not point claims |
| E01 latency sweep | Verifier p50 ~4.82ms, p95 ~11.2ms | Latency measured; catch-rate is not |

## B. Closest external prior work

| Work | Relevance | How we must position it |
|---|---|---|
| RAGChecker (ACL 2025) | Claim-level diagnostics, Pearson 60.67; faithfulness rises with k | Claim decomposition is precedent; ours binds to a *single* passage and drops sentences instead of scoring |
| RAGAS v2 | Statement extraction + NLI verdicts; 95% WikiEval faithfulness agreement | NLI-verdict pattern is precedent; ours is deterministic entailment + dose band, not an LLM judge |
| CiteEval (ACL 2025) | Principle-grounded citation quality; auto correlates 0.731/0.887 | Citation quality as separate dimension — cite for the "attribution ≠ retrieval" principle |
| GaRAGe (Findings ACL 2025) | RAF ≤60%, attribution F1 ≤58.9%; retrieval alone insufficient | Direct support for the two-wall design: retrieval gains don't imply safe answers |
| SafeRAG | Retrieval-introduced vulnerabilities, poisoned context | Precedent for retrieval-poisoning threat; our E03 poisoning arm (30%→0%) is the measured answer |
| DG-Eval (`arXiv:2603.03294`) | Atomic fact verification + contradiction detection vs Golden Facts; LoRA recall 26.2→50.3% | Downstream-verification precedent in agri; ours is upstream+downstream with live rendering decisions |
| FaithfulRAG | Parametric-vs-retrieved conflict modeling | Cite for the parametric-prior conflict framing; our dose-band check is the domain instance |
| SciTrue (EACL 2026 demo) | Claim-to-source traceability in science | Inspectability precedent; ours adds the drop decision + farmer-visible flags |
| My Climate CoPilot (ACL 2025 demo) | Transparent RAG + expert evaluation | Transparency precedent; ours is farmer-facing with authorship badges |

## C. Follow-up literature to dig (not yet read — marked for next pass)

1. **Selective prediction / abstention with guarantees** (also needed for Beat B) — *not yet verified.*
2. **Numeric-factuality / quantity hallucination studies** — dosage/PHI/unit mutation specifically; strengthens the "poison is in the number" claim. *Not yet verified.*
3. **UI trust in low-literacy AI advisory** — authorship badges, explainability-for-farmers. *Not yet verified.*

## D. Conclusions

1. Post-hoc scoring is established; **render-time sentence dropping with same-passage binding + dose-band check + visible authorship is the candidate distinction**.
2. The two-wall structure (measured gate + measured verifier latency, catch-rate pending) is defensible as a *system* contribution once the catch-rate study lands.
3. Scope discipline wins reviewers: "dosage-claim verifier" (product) vs "11-slot authority" (CEA companion) must never blur.

## E. Citation-use rules

- Cite 2606 oracle floor + SFT collapse as motivation, with exact numbers.
- Cite E03 with CIs; never report 0% without its [0, 11.35] interval context.
- Cite GaRAGe for "retrieval ≠ attribution."
- Do not claim full 11-slot certification for the live path.
- Label arXiv sources as preprints unless venue-verified.
