# Cluster 7 — Retrieval for Low-Resource Languages + RAG Evaluation: Literature Findings (2025 → Aug 2026)

**Generated:** 2026-08-12 · **Scout:** 7 · **Status:** every arXiv ID and ACL Anthology ID fetched and checked 12 Aug 2026; two requested items excluded as unverifiable (ColBERTv3 — no resolvable arXiv record; a VarDial-2025 Bangla-LM-normalizer paper — candidate ID resolved to an unrelated paper)

---

## 1. Key papers

**Retrieval architectures: hybrid, learned sparse, late interaction**

1. **MILCO: Learned Sparse Retrieval Across Languages via a Multilingual Connector** — Thong Nguyen, Yibin Lei, Jia-Huei Ju, Eugene Yang, Andrew Yates (arXiv:2510.00671v2, **ICLR 2026**). Maps queries/docs from 39 languages into a shared English lexical space; LexEcho head preserves source-language entity views. On MIRACL: 72.3 avg nDCG@10 (SOTA: +34.1% over BGE-M3 sparse, +4.5% over BGE-M3 dense, +3.6% over Qwen3-Embed-8B); mass-pruning to 30 active dims stays above Qwen3-Embed-0.6B at 3× lower latency and 10× smaller index. Bilingual Bangla↔English lexical projection now exists at SOTA with one-machine serving numbers.
2. **CSPLADE: Learned Sparse Retrieval with Causal Language Models** — Zhichao Xu et al. (arXiv:2504.10816v3, IJCNLP-AACL 2025). First 8B-scale LSR; 55.3 avg nDCG@10 over 16 BEIR datasets, statistically tied with dense baseline, Lucene index <8 GB vs ~135 GB dense. CPU-servable, inspectable sparse indexing.
3. **ColBERTv2 / SPLATE** — Santhanam et al. (arXiv:2112.01488, NAACL 2022); Formal et al. (arXiv:2404.13950, EMNLP 2024). Reference late-interaction engine + SPLATE training without three-stage distillation. Still English-centric.
4. **Jina-ColBERT-v2** — Jha et al. (arXiv:2408.16672). Multilingual late interaction on Jina-XLM-RoBERTa, matryoshka token heads 64–768 dims; no Bengali-specific numbers.
5. **PyLate** — Chaffin & Sourty (arXiv:2508.03555). Modular training/retrieval for late-interaction models; produced GTE-ModernColBERT and Reason-ModernColBERT (SOTA on reasoning/long-context retrieval). Tooling to fine-tune late interaction on Bengali domain pairs now exists.
6. **BGE-M3** — Chen et al. (arXiv:2402.03216, 2024, rev. 2025). Dense + sparse + multi-vector in one model, 100+ languages; natural cross-lingual dense baseline and MILCO's main comparison target.

**Multilingual benchmarks and ranking evidence**

7. **MIRACL** — Zhang, Thakur et al. (arXiv:2210.09984; TACL 2023). 18 languages incl. Bengali (bn: 297,265 passages, 1,631 training queries). Pyserini 2CR reproductions: bn BM25 0.508 vs mDPR-pFT 0.443 vs **hybrid 0.654** vs in-language fine-tuned dense 0.684 (18-lang means 0.388/0.421/0.581). **Dense-alone underperforms BM25 for bn; the hybrid gain (+14.6 pts bn) is the load-bearing result.**
8. **Multilingual E5 Text Embeddings** — Wang et al. (arXiv:2402.05672). MIRACL dev 60.8/62.3/66.5 nDCG@10 (small/base/large); **bn: 68.2/70.2/75.9**, bn R@100 98.2 (large). This is the exact embedding family KrishokChat serves; 75.9 is the standard-language ceiling to report against.
9. **Boosting Data Utilization for Multilingual Dense Retrieval** — Huang et al. (arXiv:2509.09459, EMNLP 2025). LLM-filtered hard negatives (19.5% false negatives eliminated; LLM-vs-human agreement 90% on bn) + language-uniform, topic-diverse mini-batches: mE5-large to 67.4 avg, BGE to 70.6 avg (bn 80.8). The concrete recipe for domain fine-tuning.
10. **Evaluating LLMs for Cross-Lingual Retrieval** — Zuo et al. (Findings EMNLP 2025, 2025.findings-emnlp.612). Embedding choice dominates architecture: E5-family weak (0.181 MAP) vs NV-Embed-v2 (0.323) on CLEF/CIRAL; BM25 over translated queries stays competitive; LLM rerankers transfer to low-resource languages.

**Query rewriting, normalization, dialects**

11. **ExpandR** — Yao et al. (arXiv:2502.17057). Jointly trains LLM (DPO with retrieval-aware reward) and retriever on expansions as pseudo-relevant documents; +8.6% nDCG@10 over Contriever.
12. **SAGE: Strategy-Adaptive Generation Engine** — Wang et al. (arXiv:2506.19783). Strategy-guided RL query rewriting; SOTA NDCG@10 on HotpotQA, FEVER, NFCorpus, SciFact; the agent learns to shorten rewrites, cutting inference cost.
13. **DeepRetrieval** — Jiang et al. (arXiv:2503.00223). RL query generation with retrieval-metric rewards, zero hand-labeled queries: 65.07% vs 24.68% prior recall on publication search; 3B model beats GPT-4o/Claude-3.5 on 11/13 datasets.
14. **Generative Query Reformulation Using Ensemble Prompting** — Dhole et al. (arXiv:2405.17658). Up to +18% nDCG@10 pre-retrieval, +9% post-retrieval; robust to weak base models.
15. **LLM-based Query Expansion Fails for Unfamiliar and Ambiguous Queries** — Abe et al. (arXiv:2505.12694, SIGIR 2025 short). When the LLM lacks topical knowledge or the query is ambiguous, LLM-QE *significantly degrades* retrieval for sparse and dense models. **Agronomic jargon + dialectal spellings are exactly the "unfamiliar" regime — blind QE is a risk; this is the citable negative result.**
16. **BUNO (Unicode Normalization and Grapheme Parsing of Indic Languages)** — Ansary, Adib, Reasat et al. (arXiv:2306.01743, LREC-COLING 2024). The canonical preprocessing fix for farmer-typed Bangla; outperforms IndicNLP normalizer; noise-robustness gains in Bengali NLP.
17. **BhasaBodh** — Bhuiyan et al. (BanglaLP @ NAACL 2025, 2025.banglalp-1.9). Chittagong/Sylhet ↔ Standard Bangla/English plus romanized variants; mBART-50 **87.44 BLEU romanized→standard** (NLLB-200: 79.13); 74.36 Chittagong→Sylhet. Dialect→standard normalization is tractable with a small model.
18. **Sylheti-CAP** — Prama (BanglaLP 2025, 2025.banglalp-1.24). Prompt-only Bangla↔Sylheti translation across five LLMs with three-step prompting (linguistic rulebook + dictionary + authenticity check): improves quality, reduces hallucinations vs zero-shot.
19. **BanglaCHQ-Prantik** — Mohona et al. (BanglaLP 2025, 2025.banglalp-1.19). 1,285 QA questions spanning 6 regional Bangla variants across 27 districts; closed-book LLaMA-3.1-8B degrades sharply on regional variants. Closest existing resource to a dialectal-query eval set.

**RAG faithfulness, citation, and evaluator evidence**

20. **RAGAS** — Es et al. (arXiv:2309.15217). WikiEval meta-evaluation: 95% human agreement on faithfulness, 83% on relevance (4,704 QA pairs). The 2025 rewrite decomposes metrics into statement extraction + NLI verdicts.
21. **ARES** — Saad-Falcon et al. (arXiv:2311.09476, NAACL 2024). Lightweight fine-tuned judges; PPI 0.93 with human preference; beats RAGAS by +59.3% (context relevance), +14.4% (answer relevance), +32.6% (faithfulness).
22. **RAGChecker** — Ru, Qiu et al. (arXiv:2408.08067, ACL 2025). Claim-level diagnostics; Pearson 60.67 vs 41.07 best baseline; faithfulness rises 88.1→92.2 as k goes 5→20. Quantifies the k-dependence reviewers will ask about.
23. **RAG Evaluation Comprehensive Survey** — Gan et al. (arXiv:2504.14891). Taxonomy: retrieval-stage, generation-stage, system-internal evaluation; 45+ datasets. One-stop map of what an industry-track RAG paper must report.
24. **MEMERAG** — Cruz Blandón et al. (ACL 2025, 2025.acl-long.1101). Native-language (not translated) meta-evaluation on MIRACL for EN/DE/ES/FR/HI; native data > translated data. **The template for a Bengali RAG meta-eval, and proof that Bengali is absent from every multilingual RAG meta-benchmark to date.**
25. **MIRAGE-Bench** — (NAACL 2025, 2025.naacl-long.14). 18-language Wikipedia answer arena; surrogate judge Kendall τ 0.909 with GPT-4o teacher over 19 LLMs; **Bengali is an explicit low-resource focus language (surrogate fit R² 0.937 on bn)**.
26. **CiteEval** — Xu et al. (ACL 2025, 2025.acl-long.1574). Principle-grounded citation-quality evaluation; CiteEval-Auto correlates Pearson 0.731/0.887 with human judgments, beating NLI-based metrics. First citation-specific evaluation suite.
27. **GaRAGe** — (Findings ACL 2025, 2025.findings-acl.875). With retrieval, average RAF ≤ 60%, attribution F1 ≤ 58.9%, deflection ≤ 31% TPR; **retrieval alone is never sufficient — attribution must be evaluated separately from retrieval.**
28. **XRAG** — (Findings EMNLP 2025, 2025.findings-emnlp.849). Cross-lingual RAG, 2-hop, five language pairs: best 42.9% F1; English-only systems lose −12% F1 when queries go cross-lingual; response-language correctness fails even when retrieved content is correct.
29. **On the Consistency of Multilingual Context Utilization in RAG** — Qi, Fernández, Bisazza (arXiv:2504.00597; **Best Paper, MRL Workshop @ EMNLP 2025**). 4 LLMs, 48 languages: models extract facts from foreign-language passages but fail to produce full answers in the correct language; distractors hurt answers regardless of language.

**Bengali agriculture RAG (2026)**

30. **AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval** — Reza, Maria & Nimi (companion to the KrishokChat EACL 2026 benchmark; local copy in `paper/done papers/`). 2,882 provenance-preserving KG nodes from 284 PDFs of five institutions (BRRI, IRRI, DAE, SRDI, MoA; 1999–2024); 19,768 entities, 17,501 triples; 900 answerable queries (300 farmer-anchored + 400 KG-grounded + 200 safety-critical; κ=0.72/0.78); five architectures × six embeddings × three language conditions. BN→BN R@10: Hybrid RRF 0.539 > BM25 0.506 > ColBERT 0.487 > Gemini dense 0.464 > BGE-M3 0.408. Sharp register effect (Dense: farmer 0.093 vs safety 0.970); cross-lingual collapse (BM25 0.506→0.004 vs Dense 0.464→0.425); configuration audit shows a 7× R@10 swing from an embedding-API default. Dataset: HF RaiyanKhaan/AgriTrust-RAG.
31. **KrishokChat (benchmark paper)** — Reza, Nimi & Shahid, EACL 2026 (`paper/done papers/`). 85,979 instances, four tracks, 2,946 semantic units, citation-level provenance, chemical-trace audit protocol; 1,000-query Real-World Farmer Benchmark. Closed-book General QA Token F1 <0.17 for all zero-shot baselines; Treatment QA Correct% <44% for all; 4.05–7.00% chemical hallucination floor under oracle evidence; fine-tuned KrishokChat-4B: General F1 0.314, Treatment 35.55%, Safety compliance 0.31%.
32. **Translation-centric Bengali agricultural RAG** — Hossain et al. (arXiv:2601.02065, Jan 2026). bn→en retrieval + en→bn generation with keyword injection; 15.6 s/query on a T4; leaves dialectal variants to future work; reports no retrieval-stage metrics.
33. **KrishokBondhu** — Ameen et al. (IEEE QPAIN 2026, DOI 10.1109/qpain69676.2026.11546653). Voice-LLM RAG (local Gemma 3-4B, LanceDB): 72.7% high-quality responses, composite 4.53 vs 3.13; no claim-level or retrieval-stage metrics.

## 2. Findings & insights

- **Hybrid fusion is the consistent, quantified win; dense-alone is weak for Bengali.** MIRACL 18-lang means: BM25 0.388 → mDPR 0.421 → **hybrid 0.581** nDCG@10; bn: BM25 0.508 > mDPR 0.443, hybrid 0.654, in-language fine-tuned dense 0.684. AgRiTrust measures the same ordering in-domain: BM25 0.506 → Hybrid RRF 0.539, with dense Gemini-001 0.464 behind both and a 0.093 farmer-query collapse; supervised bn fine-tuning on domain pairs remains the next step.
- **Bengali ceilings are known and standard-language-only.** mE5-large bn 75.9 nDCG@10, R@100 98.2; BGE-M3-finetuned bn 80.0–80.8. **No published number exists for dialectal or Banglish queries; that delta is unmeasured.**
- **Learned sparse matured 2025–26:** MILCO (ICLR 2026) 72.3 MIRACL avg with 30-active-dimension docs, 3× latency, 10× index reduction; CSPLADE 8B (<8 GB Lucene index vs ~135 GB dense). For a ~2,100-node KB, absolute index size is moot — but latency and index-size reporting is what industry-track reviewers expect (and 15.6 s/query is the current agri baseline to beat).
- **QE is double-edged.** RL-based rewriting delivers (SAGE SOTA; DeepRetrieval 65.07% vs 24.68%; ensemble +18%), but Abe et al. show LLM-QE *degrades* retrieval in low-knowledge/ambiguous regimes — exactly the dialectal-agronomy regime. Dialect→standard normalization (BUNO; BhasaBodh 87.44 BLEU; Sylheti-CAP prompting) is the safer, empirically grounded alternative for Bangla.
- **Evaluator norms are settled:** claim decomposition + NLI verdicts (RAGAS v2, RAGChecker); LLM judges reported with human-agreement figures (95% WikiEval; ARES PPI 0.93; RAGChecker Pearson 60.67; MIRAGE τ 0.909; CiteEval 0.731/0.887). Citation quality is a distinct dimension (CiteEval); attribution must be evaluated separately from retrieval (GaRAGe).
- **Multilingual RAG fails in the language channel, not the content channel** (Qi et al. 48 languages; XRAG response-language errors): a metric KrishokChat should report for mixed Bangla/Banglish inputs.
- **The Bengali agri-RAG evaluation space was empty until AgRiTrust:** MEMERAG excludes bn; MIRAGE-bn is Wikipedia-only; KrishokBondhu and the cross-lingual system report no retrieval-stage or citation-level metrics. AgRiTrust (2,882-node, 900-query, provenance-level gold) is the first retrieval-only benchmark in this space — and its register effect (dense R@10 0.093 farmer vs 0.970 safety) is the gap KrishokChat's hybrid pipeline is built to answer.

## 3. Research gaps (evidence-based)

1. **Dialect→retrieval degradation for Bangla is completely unmeasured.** MIRACL bn is standard-language Wikipedia; BanglaCHQ-Prantik provides regional QA but no retrieval judgments; the 2026 agri pipeline explicitly leaves dialectal variants to future work (2601.02065). No paper reports nDCG@10/Recall@100 for Sylheti-, Chittagong-, or Rangpur-variant queries against any Bengali corpus. **First measurement — with and without normalization — is publishable on its own.**
2. **No validated Bengali faithfulness/citation evaluator exists.** All judge-correlation numbers come from English or Wikipedia-based multilingual meta-evals; MEMERAG's native-language methodology excludes bn. A human-judged Bengali judge calibration is an explicit benchmark gap and is required to make the verifier's verdicts defensible.
3. **The hybrid-vs-dense-vs-sparse ablation is unpublished for any Bengali domain corpus, and the QE-failure regime is unstudied for Bangla agronomy.** The ablation ladder (BM25Op / mE5-small / hybrid-RRF / hybrid+normalizer) on Farmer-Benchmark-style queries + claim-level faithfulness is the missing evidence cell.

## 4. Conventions (how hybrid-RAG ablations and faithfulness evals are presented)

1. **Retrieval ablations report a fixed ladder** — BM25 → dense → hybrid (RRF or score-summation) → hybrid + reranker — with nDCG@10 and R@100, per-language/per-domain breakdowns, and k-sensitivity (MIRACL Table 4; EMNLP'25 Table 1; mE5 Tables 4–6; RAGChecker k=5→20).
2. **Faithfulness evals decompose claims** — atomic statements verified against context via NLI verdicts (RAGAS v2, RAGChecker), with judge identity, temperature, prompt, few-shot exemplars disclosed (ARES) and human meta-evaluation as agreement/correlation.
3. **Citations are evaluated separately from correctness** — per-claim citation precision/recall, principle-based citation quality (CiteEval), attribution-vs-retrieval independence (GaRAGe-style RAF/deflection), ungrounded-claim rate per answer.
4. **Multilingual papers report native-language data, response-language correctness, translation baselines, and cost** — MEMERAG's native > translated finding, Qi et al.'s language-channel analysis, BM25-DT baselines, and latency/index-size numbers (MILCO 3×/10×; 15.6 s/T4).

## 5. Positioning recommendations for KrishokChat

1. **Claim the dialectal-query retrieval evaluation** — Sylheti/Chittagong/Rangpur paraphrases of Farmer Benchmark queries + BUNO-style normalization ablation; report nDCG@10/R@100 against the MIRACL-bn reference points (BM25 0.508, hybrid 0.654, mE5-large 75.9) as the first published cells for dialectal Bengali retrieval.
2. **Frame the verifier as a Bengali CiteEval/RAGChecker instantiation** — per-claim citation scoring + claim-level faithfulness with human-judge Pearson on a Bengali subset; cite MEMERAG (bn absent) and MIRAGE (Wikipedia-only bn) as justification.
3. **Use the QE-failure result as the negative motivation** — cite arXiv:2505.12694 to explain why KrishokChat normalizes dialect (BUNO/BhasaBodh evidence) instead of prompt-expanding; contrast with SAGE/DeepRetrieval in related work.
4. **Differentiate from the three 2026 siblings on omitted evidence** — retrieval-stage metrics (absent in 2601.02065), claim-level groundedness (KrishokBondhu composite scores only), and RAG-layer construction on the 2,120-node KB (the dataset paper covers generation/formatting; the dosage-safety failure is the hook for hybrid retrieval + verifier).
5. **Follow industry-track reporting conventions** — k-ladder ablations, faithfulness + citation metrics with human meta-eval correlation, response-language correctness for Banglish inputs, latency/index-size figures.