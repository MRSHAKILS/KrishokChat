# Beat A Literature Notes — Bengali Register, Dialect, and Agricultural Retrieval

**Research pass:** 1  
**Cutoff:** 2026-09-17  
**Purpose:** evidence ledger for the Beat A story. This is not paper prose.

## A. Primary project sources

| Source | Evidence to use | Boundary |
|---|---|---|
| Reza, Maria & Nimi, *Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory*, `arXiv:2608.14886` | Bengali agricultural retrieval is strongly query-category dependent; dense R@10 is 0.093 for colloquial farmer queries vs 0.970 for formal safety queries; BM25 0.506; hybrid RRF 0.539; configuration and passage choices can move scores by ~7× | Farmer, KG, and safety subsets differ in task/content; this is a register-stratified pattern, not a clean causal estimate of register alone |
| Reza, Nimi & Shahid, *KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory*, `arXiv:2606.29243v2` | 85,979-instance benchmark; 1,000-query farmer benchmark; provenance and chemical traces; oracle evidence still leaves a 4.05–7.00% chemical hallucination floor; farmer transfer remains difficult | Controlled dialect surfaces are not all authentic field language; benchmark evidence does not itself measure a live retrieval-repair policy |
| Local `paper/literature review/07_retrieval_low_resource_rag_eval.md` | Consolidated literature ledger: MIRACL-Bengali hybrid/dense/BM25 anchors, query-expansion risks, BUNO/BhasaBodh, RAG faithfulness and citation-evaluation conventions, gaps in dialect retrieval | Generated 2026-08-12; refresh individual citations before final bibliography |
| Local `paper/literature review/03_low_resource_nlp_bengali.md` | Bengali LLM and dialect resources; native vs translated data; BhasaBodh, BanglaCHQ-Prantik, BUNO; low reliability of multilingual LLM judges for Bengali | Primarily language-resource evidence, not direct agricultural retrieval evidence |

## B. Closest external prior work

| Work | Relevance | How we must position it |
|---|---|---|
| BUNO, `2024.lrec-main.1479` | Unicode and grapheme normalization for Indic languages | Normalization is established; cite as a foundation, not novelty |
| BhasaBodh, `2025.banglalp-1.9` | Chittagong/Sylhet, Standard Bangla, English, and romanized forms | Dialect/romanization resources already exist; ours would need agricultural retrieval and safety preservation |
| Alam & Anastasopoulos, `2025.vardial-1.5` | South Asian dialect/transliteration normalization | Normalization before downstream tasks is not new |
| Sami et al., `2025.banglalp-1.22` | Bengali hybrid/adaptive retrieval or translation | Adaptive sparse/dense handling is prior art; distinguish by safety-critical agricultural integration and auditability |
| IndicIRSuite, `2024.acl-short.46` | Bengali/Indic neural IR baselines | Bengali IR itself is established; avoid “first Bengali retrieval” wording |
| Krishi Sathi, `arXiv:2508.03719` | Intent, slots, clarification, agricultural RAG, ASR/TTS | Missing-slot interaction exists; our claim must be about measured safety and retrieval-scope consequences |
| Hossain et al., `arXiv:2601.02065` | Bengali-to-English retrieval and Bengali answer generation | Translation-centric retrieval exists; compare it rather than presenting language bridging as new |
| Farmer.Chat, `arXiv:2409.08916` | Deployed multilingual agricultural RAG at scale | Strong deployment comparator; no reason to claim agricultural RAG or multilingual access as unique |
| KrishokBondhu, `arXiv:2510.18355` | Bengali voice agricultural RAG with local Gemma | Direct Bengali agricultural comparator; distinguish by visual scope reduction, pre-retrieval gating, and safety trace |
| My Climate CoPilot, `2025.acl-demo.7` | Accepted ACL agricultural system demo with transparency and expert evaluation | Precedent for integration + inspectability; ours must show why Bengali farmer-language handling changes the system path |
| BanSuite, `2026.eacl-demo.44` | Accepted EACL Bangla toolkit | Evidence that integrated open Bangla tooling can be a demo contribution; ours is an advisory workflow, not a toolkit |

## C. Literature conclusions

1. The *problem* is well established: farmer-style Bengali and formal agricultural sources do not align reliably.
2. The *components* are established: normalization, hybrid retrieval, slot filling, clarification, and RAG.
3. The unresolved system question is narrower: can a live advisory system make interpretation and retrieval scope explicit, route conservatively, and demonstrate that language repair does not corrupt safety-bearing fields?
4. The strongest novel result would be a paired, provenance-grounded intervention study — not a new dictionary or another aggregate retrieval score.

## D. Search gaps to verify in the next pass

- Has any published Bengali agricultural system reported retrieval metrics separately for formal, colloquial, dialect, and Banglish queries?
- Has any system measured normalization-induced changes to crop, disease, chemical, dosage, unit, interval, PHI, and polarity?
- Has any accepted ACL/EACL demo shown image-conditioned retrieval-space reduction rather than only image diagnosis?
- Are there human-validated paired dialect forms suitable for strict retrieval qrels?
- Which Bengali/Bangla retrieval models can be run locally and reproduced without external API variability?

## D2. Dataset-reuse precedent — accepted demo papers DO evaluate on existing/released data

Verified from ACL Anthology proceedings (2024–2026). Constructing a brand-new human-validated test set is common in *research* papers but **not** required for system demonstrations; reusing released/external datasets is standard practice.

| Accepted demo | Venue | Evaluation source | Lesson |
|---|---|---|---|
| RAGVUE (`2026.eacl-demo.35`) | EACL 2026 | Constructed 100 synthetic (Q, C, A) triplets **from the released StrategyQA benchmark** | Even a *diagnostic tool* demo reuses an existing benchmark as its substrate |
| GenGO Ultra (`2025.acl-demo.24`) | ACL 2025 | Reuses **SciTLDR, ACLSum, SciRIFF**; on-device encoders evaluated on released scientific datasets; LLM-as-judge for end-to-end | Reusing released datasets + honest judge disclosure is accepted |
| NLP-KG (`2024.acl-demos.13`) | ACL 2024 | **SciERC** dataset for extraction fine-tuning; RAGAS on 50 generated questions | Existing datasets + small sampled evaluations are normal |
| OpenEval (`2024.acl-demos`) | ACL 2024 | 12 existing benchmark datasets for capability; 7 alignment + 6 safety sets | Benchmark reuse is the default, not the exception |
| OLMOtrace (`2025.acl-demo.18`) | ACL 2025 | 98 internal conversations + BM25 relevance rubric + human/LLM-judge | Small, honest, purpose-fit evaluation is acceptable for a tool demo |
| AI for Climate Finance (`2026.eacl-demo`) | EACL 2026 | Manually annotated CREWS corpus + expert WMO co-curated evidence set | A focused domain annotation is used, but it is *narrow*, not a huge new benchmark |

**Verdict for KrishokChat:** using the released `arXiv:2606.29243` benchmark (incl. its 1,000-query Real-World Farmer Benchmark) and the `arXiv:2608.14886` AgRiTrust retrieval set as the primary evaluation backbone is fully within accepted demo-paper practice. A new 8-form × 200-intent paired annotation is **optional** — only if time remains, as an *additional* stress layer, never as the primary evidence.

**Caveats to disclose if we reuse our own released benchmark:**
1. Benchmark-vs-system paper distinction: the benchmark paper *is* ours (2606.29243). We must frame the demo as *operationalizing the failure modes the benchmark quantifies*, not as re-validating the benchmark.
2. Test reuse: use the benchmark's official held-out split (350-query farmer split per 2606.29243; 900-query retrieval set per 2608.14886). Do not re-split.
3. No tuning on test: freeze system config before running; state this explicitly.
4. Companion citation: cite 2606.29243 + 2608.14886 as the dataset sources; do not describe the data construction in the demo paper.

## E. Citation-use rules

- Use `2608.14886` to motivate the failure, not to claim causal register attribution.
- Use `2606.29243` to motivate farmer transfer and safety, not as evidence that the current live router fixes it.
- Label arXiv sources as preprints unless a peer-reviewed venue is verified.
- Separate register, dialect, script/orthography, and language conditions.
- Do not cite local literature-review prose as the primary source in the paper; cite the original paper or official ACL/arXiv record.
