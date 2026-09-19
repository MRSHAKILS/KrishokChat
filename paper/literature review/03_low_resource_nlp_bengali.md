# Cluster 3 — Low-Resource NLP, Bengali & Dialects: Literature Findings (2025 → Aug 2026)

**Generated:** 2026-08-12 · **Scout:** 3 · **Status:** all citations verified against arXiv abs/HTML pages, ACL Anthology records, or publisher pages during review; unverifiable references omitted

---

## 1. Key papers

**Bengali LLMs & instruction data**

1. **TituLLMs: A Family of Bangla LLMs with Comprehensive Benchmarking** — Nahin et al., Findings of ACL 2025 (2025.findings-acl.1279; arXiv:2502.11187). First pretrained Bangla LLMs (1B/3B) on ~37B tokens; extended Llama-3.2 tokenizer; released five benchmark datasets (~137K samples incl. 87,869-item Bangla MMLU). Bangla MMLU accuracy is 0.25 (0-shot) and does not improve with 5-shot — world-knowledge gaps are parametric, not prompting-limited.
2. **TigerLLM - A Family of Bangla LLMs** — Raihan & Zampieri, ACL 2025 short (2025.acl-short.69; arXiv:2503.10995). Bangla-TextBook corpus (9.9M tokens from 163 NCTB textbooks) + Bangla-Instruct, 100K instruction pairs via self-instruct with GPT-4o/Claude-3.5-Sonnet and ~63% four-criteria filtering; 30–55% benchmark gains; 1B variant beats larger baselines. Native pairs outperform 224K translated pairs by 30–55%.
3. **BnMMLU: Understanding in Bengali** — Joy & Shatabda (arXiv:2505.18951; Findings ACL 2026, DOI 10.18653/v1/2026.findings-acl.593). 41 domains, 134,375 MCQ pairs, MathML preservation, BnMMLU-HARD subset; 24 models under Direct/CoT × 0/5-shot. 13-gram decontamination: <0.1% overlap with published Bangla corpora. Bengali-centric families plateau earlier than global families.
4. **B-REASO: A Multi-Level Multi-Faceted Bengali Evaluation Suite** — Hosain & Morol, Findings of EMNLP 2025 (2025.findings-emnlp.492). 13,497 MCQs, 50 fields, four difficulty tiers; only Claude-3.5-Sonnet exceeds 65%.
5. **Evaluating LLMs' Multilingual Capabilities for Bengali** — Bhowmik et al. (arXiv:2507.23248). 8 translated benchmarks, 10 open LLMs; Bengali tokenization inefficiency correlates with degraded accuracy; Bengali prompts incur ~2× token counts vs English.
6. **Reveal-Bangla** (arXiv:2508.08933) — manually translated multi-step reasoning; CoT gains in Bangla (+3.9%) far below English (+19.2%); reasoning techniques do not transfer mechanically.

**Dialect handling**

7. **DialectalArabicMMLU** — LREC 2026 (lrec2026-main-251; arXiv:2510.27543). 3K MMLU-Redux items human-translated into 5 dialects (15K pairs), double-checked; 19 open-weight models; explicit dialect conditioning does not improve performance; dialect-identification skill correlates only moderately with dialect reasoning.
8. **AraDiCE** — Mousi et al., COLING 2025 (2025.coling-main.283; arXiv:2409.11404). ~45K post-edited samples: MT from MSA into Egyptian/Levantine + human post-editing; dialect generation lags dialect understanding.
9. **AL-QASIDA** (2025.findings-acl.1137) — 9 LLMs × 8 dialect varieties; models understand dialectal Arabic better than they produce it; post-training creates refusal-to-generate-dialect bias, recoverable via few-shot examples.
10. **BhasaBodh** (2025.banglalp-1.9, BanglaLP @ NAACL 2025) — Chittagong/Sylhet parallel corpus aligned with Standard Bangla and English plus Gemini-2.5-Pro romanized variants; mBART-50 hits BLEU 87.44 on Romanized→Standard normalization; cross-script tasks remain hard.
11. **BanglaCHQ-Prantik** (2025.banglalp-1.18) — first medical-domain Sylheti/Chittagonian benchmark on public-health content; 17 native translators; errors persist on terminology, numerals, idioms — the same failure classes an agri-advisory system faces.
12. **Vashantor** (arXiv:2311.11142, background) — 32,500 sentences across Chittagong, Noakhali, Sylhet, Barishal, Mymensingh; DialectBanglaT5 BLEU 71.93 (Mymensingh); region classification 89.02%.
13. **ANCHOLIK-NER** (PLOS ONE, 2026; doi:10.1371/journal.pone.0342786) — 17,405 sentences across 5 dialect regions; best F1 82.61% (Mymensingh), Chittagong weakest (76.38%); dialect spread changes named-entity boundaries.
14. **IndicJR** (arXiv:2602.16832) — 45,216 jailbreak prompts over 12 Indic languages incl. Bengali; romanized/mixed orthography drops contract-bound JSR from 0.755 to 0.416 (Δ −0.34); English→Indic attacks transfer strongly (≥0.58 in all languages).

**Synthetic data for low-resource languages**

15. **A Rigorous Evaluation of LLM Data Generation Strategies for Low-Resource Languages** — Anikina et al., EMNLP 2025 (2025.emnlp-main.418; arXiv:2506.12158). 11 languages × 3 tasks × 4 models; target-language demonstrations + LLM-based revision closes the gap with gold data to ~5% absolute; English demonstrations hurt low-resource languages; no human annotation in the pipeline (stated limitation).
16. **Updesh** (arXiv:2509.21294) — 9.5M grounded instruction pairs for 13 Indic languages from language-specific Wikipedia (bottom-up, not translation); 10K native-speaker ratings, 0.27% zero-rated; LLM-judge agreement declines on culturally nuanced criteria; IndicLID confidence 0.75 filtering, repetition caps.
17. **BhashaKritika** (arXiv:2511.10338) — 540B synthetic tokens, 10 Indic languages; quality pipeline = LID ensemble + heuristics + FastText classifier + KenLM perplexity; quality-classifier flag rate 3.40%; synthetic annealing matches web-data convergence on 1B models.
18. **SynOPUS** (arXiv:2505.14423) — GPT-4o forward-translation of Europarl into 7 low-resource languages (2–2.3M sentences); +20.63 ChrF for LLaMA-3B; HeLI-OTS filtered only 0.45%; documents teacher-model artifacts and contamination risk.
19. **Does Synthetic Data Help NER for Low-Resource Languages?** (arXiv:2505.16814) — 100 manually annotated datapoints beat large synthetic sets; zero-shot transfer from related languages beats synthetic fine-tuning in most cases.

**Multilingual safety (Bengali included)** — see Cluster 2 file for detail; short list: IndicSafe (arXiv:2603.17915, 12.8% cross-language agreement), IndicGuard (arXiv:2606.22841, Gemma-3-4B guard, 10 languages), LinguaSafe (arXiv:2508.12733), SGToxicGuard (2025.emnlp-main.612), RefusEU (2026.findings-acl.1537), PolyRefuse (arXiv:2505.17306).

**LLM-as-judge & cultural evaluation**

26. **Pariksha** (arXiv:2406.15053) — 90K human evaluations, 10 Indic languages; human–LLM judge agreement is lowest for Bengali and Odia in direct assessment; GPT evaluator exhibits self-bias.
27. **How Reliable is Multilingual LLM-as-a-Judge?** — Fu & Liu (arXiv:2505.12201). Fleiss' κ ≈ 0.3 across 25 languages; Telugu κ = 0.002 on MGSM; neither scale nor multilingual pretraining fixes consistency.
28. **JuICE** (arXiv:2605.26955) — 7,470 span-level cultural-error annotations incl. Bangladesh/Bengali (44 native annotators, 14 for Bangla); best judge F1 0.52; LLM judges miss "thick" cultural errors.
29. **CulturalNB** (arXiv:2605.30481) — 717 Bengali cultural instances with parallel Bangla/English; English prompts increase global substitution and institutional framing; evidence grounding reduces but does not remove the shift.

**Agricultural domain**

30. **Leveraging Synthetic Data for QA in Agriculture (EN/HI/PA)** (arXiv:2507.16974) — 60,130 synthetic QA pairs from Indian agri documents; human evaluation each step; fine-tuning +22.1% relevancy, +14% factuality; translate-test beats native-language fine-tuning for Hindi/Punjabi.
31. **Fine-Tuning and Evaluating Conversational AI for Agricultural Advisory** — DigiGreen (arXiv:2603.03294) — 11,966 expert-validated QA pairs, 110,723 golden facts; F1 37.2→51.8% (GPT-4o Mini FT, p<0.001); safety handled via a stitching layer.
32. **KrishokTech: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory** — Reza, Nimi & Shahid, EACL 2026 (with companion AgRiTrust retrieval benchmark; local copies in `paper/done papers/`). 85,979 instances across four tracks: General Knowledge QA (28,993), Treatment QA (11,224; 7,437 with chemical-trace arrays), Safety Refusal & Re-query (20,112: 3,216 T3 refusal + 16,896 T4 re-query over a 12-category taxonomy), and Table QA (25,650 over 584 government tables). Built from 284 government publications and 13 institutions; question surfaces diversified across six Bengali dialects with content tokens frozen; reference answers extracted verbatim, never generated; citation-level provenance on every instance. Released CC-BY-4.0; dataset on Hugging Face (RaiyanKhaan/krishokChat).

**Normalization**

33. **Unicode Normalization and Grapheme Parsing of Indic Languages** — Ansary et al., LREC-COLING 2024 (2024.lrec-main.1479) — the published reference for bnunicodenormalizer (BUNO), the exact library KrishokTech uses; fixes 7 error classes + 4 Bangla-specific operations; MIT licensed.

## 2. Findings & insights

- Bengali instruction data quality is the gating factor: TigerLLM's 100K native pairs outperform 224K translated pairs by 30–55%; most prior Bangla LLMs are non-reproducible (TigerLLM Table 1) — any new Bengali dataset paper is read against this reproducibility bar.
- Bangla MMLU saturation (0.25 for ~3B models, flat with shots) contrasts with gains Bengali-centric models show with 5-shot CoT in BnMMLU (TigerLLM-9B-IT 11.01→23.32). Prompting protocol decisions move numbers more than model size.
- Dialect evaluation is translation-dominant: DialectalArabicMMLU, AraDiCE, BhasaBodh, ONUBAD, Vashantor, BD-Dialect all construct parallel standard↔dialect resources; **none evaluates refusal/safety behavior in dialect**. AL-QASIDA shows models refuse to *generate* dialect; IndicJR shows romanized input changes jailbreak rates by 0.34 — orthography and dialect alter both safety and capability, measured nowhere for Bangla.
- Dialect identification does not co-vary with dialect reasoning quality (DialectalArabicMMLU oracle + DID experiments). A dialect map alone cannot certify dialect competence; per-dialect task evaluation is required.
- Synthetic-data QC conventions are standardized: LID with confidence thresholds (IndicLID 0.75 in Updesh), perplexity filters (KenLM in BhashaKritika), teacher-artifact scrubbing (SynOPUS), pass-rate reporting (~63% TigerLLM; 3.4% BhashaKritika).
- Human validation is mandatory evidence for tier-1 dataset papers: Updesh (10K native ratings), JuICE (dual annotation), DialectalArabicMMLU (double native checking), BanglaCHQ-Prantik (17 translators), AraDiCE (post-editing). MT-only datasets openly admit under-validation.
- LLM-as-judge is documented as unreliable for Bengali: Pariksha's low human–judge agreement for Bengali, κ≈0.3 multilingual consistency, JuICE F1 0.52. A Bengali agri-safety paper relying on LLM judges alone will be attacked on this evidence.
- Agricultural advisory work for South Asia uses human-expert-verified gold answers (DigiGreen: 9.23 facts/answer); domain-specific fine-tuning beats zero-shot frontier models (+22.1/+14 points).

## 3. Research gaps

- **No multi-dialect safety/refusal dataset exists for Bangla.** IndicSafe, IndicGuard, IndicJR, LinguaSafe, SGToxicGuard cover Bengali as one row in a language matrix, always in standard script; the only orthography-axis results are romanization-vs-native (IndicJR ΔJSR −0.34). Sylheti, Chittagong, Rangpur, Noakhali, Barishal, Mymensingh forms of *the same harmful or benign intent* have no published evaluation anywhere. This is the team's 20,112-record, 6-dialect dataset's exact claim — first mover, with the quantified motivation (IndicSafe 12.8% agreement).
- **No agricultural-domain Bengali evaluation suite.** BnMMLU, B-REASO, TituLLM-MMLU are general-knowledge; agri QA benchmarks exist only for English/Hindi/Punjabi (2507.16974) and English (DigiGreen). The only Bengali agri evaluation resource is the team's own 4-track KrishokTech benchmark plus its 1,000-query Real-World Farmer Benchmark (EACL 2026), whose held-out 350-query split shows frontier models still failing farmer-language transfer (Gemini-2.5-FL Token F1 0.220; LLaMA-3.1-8B 0.008). Chemical-dosage exactness is the benchmark's measured failure axis (Treatment QA Correct% <44% for every zero-shot baseline) — a dosage-focused Bengali agri evaluation set beyond the team's own still has no competitor.
- **Dialect-rewrite fidelity lacks a published QC protocol.** Existing dialect resources measure word-level divergence (ChatgaiyyaAlap 1,500-word dictionary; BD-Dialect 950 aligned entries) but no paper measures whether an LLM dialect rewrite preserves slot semantics (dosage, crop, action) under normalization. A measurable protocol — per-dialect word-map agreement against a published dictionary plus semantic-slot preservation — is unclaimed.

## 4. Conventions

- **Quality control**: report automated filter pass rates, LID thresholds, decontamination explicitly (BnMMLU 13-gram <0.1%; Updesh pass rates; SynOPUS filtering). Tier-1 dataset papers pair this with native-speaker human validation counts and inter-annotator agreement; LLM-judge-only validation is now contested (JuICE, Pariksha, 2505.12201).
- **Dialect coverage**: state dialects, speaker populations, annotator counts per dialect, multiple native speakers per dialect (BD-Dialect names 3 per dialect). Parallel standard↔dialect formatting is the community norm (Vashantor, ONUBAD, BhasaBodh).
- **Licensing**: CC-BY-4.0 dominates (KrishokTech, BD-Dialect); MIT for code/tools (BUNO, Ajrasakha); HF + GitHub release with a referenced dictionary or map file. Reproducibility tables (TigerLLM Table 1) are becoming an expected artifact.

## 5. Positioning recommendations for KrishokTech

1. Position the safety dataset as the first multi-dialect (6 varieties, 110-word genuine map) refusal/safety resource for Bangla; open with IndicSafe's 12.8% cross-language agreement and IndicJR's −0.34 orthography result as the quantified problem statement.
2. Cite BUNO by its paper (Ansary et al., 2024.lrec-main.1479), not only as a library; present the normalization layer as the reproducibility anchor for retrieval.
3. Follow BnMMLU's contamination protocol (13-gram analysis against Pralekha, Bangla-Instruct, Bangla-TextBook, TituLM) before submission.
4. Do not rely on LLM-as-judge for refusal classification or dialect-fidelity claims: native per-dialect human validation with agreement statistics; report filter pass rates like TigerLLM (~63%) and BhashaKritika (3.4%).
5. Position the safety dataset as a named extension of the KrishokTech resource family ("second release"): the EACL 2026 benchmark's Safety QA (20,112 records, 12-category taxonomy) is template-grounded policy content, while the 20,112-record multi-dialect safety/refusal dataset here adds genuine dialect maps and stress scenarios. Benchmark refusal-compliance against the EACL 2026 finding that answer-only SFT collapses compliance to 0.31% — no competitor covers agri-domain Bengali let alone its dialects.