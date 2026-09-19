# 2. Related Work

> **Status:** DRAFT v1 (D1 lane, 2026-08-22) — written from `paper/literature review/*` + `02_LANDSCAPE_GAPS_COMPETITIVE.md` under the frozen claim ledger (`CLAIM_LEDGER_FREEZE.md`). External numbers cite their sources; `[G0]` marks identifiers requiring URL re-verification at assembly. No empirical claim about THIS system is promoted; our runtime facts are ledger S01/S02/S03/S05/S11/S17-compliant. The arXiv v1 paper banned by `docs/PAPER_POLICY.md` is cited nowhere in this draft.

Work related to this paper falls into five groups: claim verification and selective answering; Bengali language resources and retrieval; agricultural advisory systems; vision-based crop disease identification; and systems-evaluation conventions. Each group supplies a component that an agricultural advisory pipeline needs. None of them combines those components for a low-resource, safety-critical setting such as Bengali agrochemical advice. Two capabilities remain unmeasured in the reviewed literature: relation-aware certification of dosage-bearing advice with calibrated abstention, and dialect normalization evaluated jointly for retrieval benefit and safety preservation. This section reviews each group and locates those gaps.

## 2.1 Five evidence groups

**Claim verification and selective answering.**
Claim-level verification has converged on a common architecture: decompose an answer into atomic claims, verify each against retrieved evidence, and aggregate the labels into an answer-level verdict. RT4CHART applies hierarchical local-to-global verification and reports F1 of 0.776 against a 0.424 baseline on RAGTruth++ (Yu et al., 2026 [G0]). VeriCite places NLI-verified citation selection before final generation rather than after it (Qian et al., 2025). Medical systems instantiate the same pattern with domain structure: MedRAGChecker adds knowledge-graph consistency because text-only entailment misses drug-disease contraindications (MedRAGChecker, 2026 [G0]), ClinicBot validates numeric claims against clinical guidelines by string matching (ClinicBot, 2026 [G0]), and atomic fact-checking recovers incorrect drug dosages in medical answers (Khandekar et al., 2025). Selective answering is measurable and currently unreliable. RefusalBench evaluates 176 perturbations across six uncertainty categories and finds that frontier models fall below 50% refusal accuracy on multi-document tasks (Muhamed et al., 2025). Zhou et al. show that irrelevant retrieved contexts trigger over-refusal on answerable queries, arguing for deciding before retrieval rather than after (Zhou et al., 2026 [G0]). Production deployments confirm that abstention meets latency budgets: one financial RAG system masks 29.9% of responses at precision 0.95 (Huang et al., 2025), and energy-based scoring reaches AUROC 0.961 on near-domain abstention in healthcare (Shankar et al., 2025). Every one of these systems operates in English or another well-resourced domain; none addresses agricultural content, and none addresses Bengali.

**Bengali language resources and retrieval.**
Bengali agricultural NLP has active resources but little safety machinery. KrishokBondhu serves voice queries through retrieval over a vector index with a small open-weight generator and reports 72.7% high-quality responses, while noting the absence of a standard Bengali agricultural QA benchmark (Ameen et al., 2025). A translation-centric alternative retrieves over English FAO and IRRI corpora, rejects out-of-domain inputs, and defers dialectal variants to future work (Hossain et al., 2026 [G0]). Retrieval evaluation for Bengali rests on standard-language Wikipedia: MIRACL-Bengali reports nDCG@10 of 0.508 for BM25 and 0.654 for hybrid retrieval, with no agricultural corpus and no dialectal queries (Bandyopadhyay et al., TACL 2023). Normalization resources exist upstream of any safety evaluation. BUNO canonicalizes farmer-typed Bangla by correcting seven recurring error classes (LREC-COLING 2024), and BhasaBodh contributes parallel dialect corpora with which mBART-50 reaches 87.44 BLEU mapping romanized forms to standard Bangla (BanglaLP at NAACL 2025). What these resources do not establish is whether rewriting preserves semantic slots such as dosage, crop, or polarity when a query crosses registers. The concern is quantified for generation: LLM accuracy on Chittagong-register QA averages 5.44/10 against 7.68/10 for Tangail register across 19 models (Das et al., 2026 [G0]). Safety suites compress Bengali into a single standard-script row; IndicSafe reports 12.8% cross-language agreement, and romanization alone shifts jailbreak rates by -0.34 (IndicJR). No multi-dialect Bengali safety benchmark exists.

**Agricultural advisory systems.**
Deployed advisory systems demonstrate scale without verification. Farmer.Chat serves more than 300,000 queries over government-curated knowledge bases in six languages, reaching 71% retrieval context precision, yet publishes neither a verifier nor refusal logic (Singh et al., 2024). The AIEP initiative's voice-first prototypes operate where extension-worker ratios run 1:750 to 1:1000, which motivates automation but leaves safety handling to the generator (Collis et al., 2026 [G0]). My Climate CoPilot contributes the closest evaluation template, with 50 domain experts assessing an agriculture QA platform (Nguyen et al., 2025). Where dosing is measured, it is the weakest capability: AgriEval averages 41.27% across 51 LLMs against 70.62% for PhD experts (Yan et al., 2026), and IPM-AgriGPT scores correct dosing at 0.392-0.499 after fine-tuning while safety reaches roughly 0.72. A GPT-4-as-evaluator study identifies over-advising, with high false positives, as the dominant failure mode (Yang et al., 2024).

The nearest prior work to our setting is the team's own benchmark. It measures Treatment QA correctness below 44% for every zero-shot model and records a chemical hallucination floor of 4.05-7.00% that persists even when gold evidence is supplied (Reza, Nimi & Shahid, EACL 2026). Answer-only fine-tuning collapses safety compliance to 0.31%, so generation quality and safety behavior dissociate. DG-Eval remains the single published contradiction-detection protocol in agriculture, lifting fact recall from 26.2% to 50.3% when combined with expert-curated tuning data (Singh et al., 2026 [G0]). No published advisory system we are aware of couples automated refusal with escalation to a real national helpline, and none audits generated claims against retrieved sources before display.

**Vision-based crop disease identification.**
Vision components enter this work only as routing context. Supervised classifiers remain the dependable choice for crop and disease identification, outperforming zero-shot vision-language models across reported tasks (Anonymous et al., 2025 [G0]). Calibration and out-of-distribution reporting conventions carry over from medical screening practice. We treat the classifier stack as a front end that routes photographs into the same verified-advice pathway, and we claim no localization capability.

**Systems-evaluation conventions.**
System papers are expected to evaluate components in isolation, account for latency, and release artifacts. Industrial reports pair hallucination reductions with A/B tests and measured latency cost, and the refusal literature has standardized on risk-coverage curves alongside AbstainAccuracy and AbstainF1. We follow these conventions: each experiment in Section 5 fixes its baseline, metric, statistical test, and anticipated failure mode, and each primary number traces to a run manifest.

**Table 1. Taxonomy of related work and the gaps this paper addresses.**

| Group | Representative systems | What they establish | What remains open |
|---|---|---|---|
| Claim verification & selective answering | RT4CHART; VeriCite; MedRAGChecker; ClinicBot; RefusalBench; Zhou et al.; Huang et al.; Shankar et al. | Atomic claim decomposition, NLI/span verification, production-proven abstention with latency budgets | No agricultural relation verifier; nothing for Bengali dosage advice; no calibrated abstention under lexical-only retrieval |
| Bengali language resources & retrieval | KrishokBondhu; cross-lingual bn-en-bn RAG; BUNO; BhasaBodh; MIRACL-Bengali; IndicSafe/IndicJR | Bengali RAG works; dialect normalization is tractable; standard-script retrieval benchmarks exist | No dialect-to-retrieval measurement for Bangla agriculture; slot preservation under rewriting unmeasured; no multi-dialect safety benchmark |
| Agricultural advisory & escalation | Farmer.Chat; DG-Eval; AgriEval; IPM-AgriGPT; AIEP; My Climate CoPilot; KrishokTech benchmark | Deployment scale; expert-grounded fact-checking protocol; dosing identified as weakest axis; chemical hallucination floor | No output-time claim audit in an advisory system; no refusal coupled to a live national helpline |
| Vision & multimodal routing | Supervised crop-disease classifiers; VLM comparisons | Supervised classification beats zero-shot VLMs; calibration/OOD norms transfer | Grounding of treatment advice behind vision routes (secondary scope here) |
| Systems evidence & compute | Faithful Industrial RAG; DecEx-RAG; refusal-metric conventions | Component evaluation, latency accounting, artifact release, risk-coverage reporting | Applied to Bengali agrochemical certification nowhere |

## 2.2 Closest-system comparison

Table 2 compares the nine systems closest to ours along the dimensions that matter for dosage safety. The structural pattern is visible at a glance: systems either verify claims and lack Bengali agricultural grounding, or serve Bengali users and lack verification. The bottom row states the starting point that this paper upgrades with measurement.

**Table 2. Closest-system comparison.**

| System | Retrieval | Safety / abstention | Claim / dosage verification | Bengali / dialect | Difference from this work |
|---|---|---|---|---|---|
| Farmer.Chat (Singh et al., 2024) | RAG over curated KBs | No published domain gate | None | Multilingual; not this Bangla setting | Scale leader; lacks typed dosage verification and calibrated refusal |
| KrishokBondhu (Ameen et al., 2025) | Bengali voice RAG | Referral text; no reported safety layer | None | Bengali; no dialect evaluation reported | Closest language competitor; no verifier or audit trail |
| Cross-lingual Bengali agri RAG (Hossain et al., 2026 [G0]) | Translation-centric FAISS | OOD rejection only | None | Dialects left open | Tests a translation path rather than native dialect handling |
| My Climate CoPilot (Nguyen et al., 2025) | Grounded agricultural QA | Transparency focus | No typed dosage verifier reported | Not Bengali | Expert-evaluation template; different language and verification depth |
| DG-Eval (Singh et al., 2026 [G0]) | Protocol over Farmer.Chat outputs | Stitching safety layer | Expert-grounded fact checking | Not Bengali dialects | Strong evaluation baseline; different schema and domain |
| RAGChecker / RAGAS (2025) | Generic RAG diagnostics | No domain action policy | Claim-level NLI | No validated Bengali agricultural judge | Method baseline, not an advisory system |
| ClinicBot / MedRAGChecker family (2026 [G0]) | Clinical RAG | Medical abstention/validation | Numeric or KG+NLI checks | English clinical | Transferable mechanism; different relations and risks |
| BhasaBodh / BUNO (NAACL 2025; LREC-COLING 2024) | Not agricultural RAG | No safety outcome | None | Dialect/romanized normalization resources | Normalization baselines without downstream safety measurement |
| KrishokTech runtime (this work, before measurement) | BM25 over 2,135-node national-institution corpus | Six-way pre-retrieval terminal gate; keyword-scoped coverage gate; 16123 escalation | Normalized lexical dosage matching | Deterministic Bengali checks; dialect behavior unevaluated | Starting point; this paper adds relation-aware, calibrated certification |

## Positioning

The reviewed literature leaves two adjacent cells empty. No system we are aware of performs relation-aware certification of Bengali agrochemical dosage advice with selective certification (calibrated abstention), and no study pairs dialect normalization for Bangla with a safety-preservation check on the same inputs. This paper fills both cells by measurement. We start from an operational runtime whose safety router precedes retrieval, whose retriever is BM25 over 2,135 knowledge nodes from national institutions, and whose existing verifier matches normalized dosage strings lexically. On that runtime we construct a deterministic relation-aware verifier with fail-closed gating, calibrate a selective-certification threshold on development data, and evaluate raw, Unicode, and dictionary-based dialect normalization under a safety-flip non-inferiority constraint. We claim no architectural novelty in orchestration, trace interfaces, generic RAG, or visual localization; the contribution is the measured protocol.

---

## Provisional references (assembly: G0 re-verification required)

- Yu et al. (2026) [G0]. RT4CHART: claim decomposition and hierarchical verification. arXiv:2603.27752.
- Qian et al. (2025). VeriCite: NLI-verified citation generation. arXiv:2510.11394, SIGIR-AP 2025.
- MedRAGChecker (2026) [G0]. KG+NLI claim verification for biomedical RAG. arXiv:2601.06519.
- ClinicBot (2026) [G0]. Guideline-grounded clinical advisory demo. arXiv:2605.00846.
- Khandekar et al. (2025). Atomic fact-checking for medical QA. arXiv:2505.24830. *(author string to confirm at assembly)*
- Muhamed et al. (2025). RefusalBench. arXiv:2510.10390.
- Zhou et al. (2026) [G0]. Do RALMs know when they don't know? arXiv:2509.01476, AAAI 2026.
- Huang et al. (2025). Confidence-based response abstinence. arXiv:2510.13750, UncertaiNLP @ EMNLP 2025.
- Shankar et al. (2025). Energy-based abstention for healthcare RAG. arXiv:2509.04482.
- Ameen et al. (2025). KrishokBondhu: voice-based agricultural advisory call center. arXiv:2510.18355, IEEE QPAIN 2026.
- Hossain et al. (2026) [G0]. Cost-efficient cross-lingual RAG: Bengali agricultural advisory. arXiv:2601.02065.
- Bandyopadhyay et al. (2023). MIRACL-Bengali. TACL 2023. *(author string to confirm at assembly)*
- Das et al. (2026) [G0]. Dialect degradation in Bengali QA. arXiv:2603.21359. *(author string to confirm at assembly)*
- Singh et al. (2024). Farmer.Chat: scaling AI-powered agricultural services. arXiv:2409.08916.
- Collis et al. (2026) [G0]. AIEP technical learnings. arXiv:2601.11537.
- Nguyen et al. (2025). My Climate CoPilot. ACL 2025 System Demonstrations, 2025.acl-demo.7.
- Yan et al. (2026). AgriEval. AAAI 2026, arXiv:2507.21773.
- Yang et al. (2024). GPT-4 as evaluator: pest management. arXiv:2403.11858.
- Singh et al. (2026) [G0]. Fine-tuning and evaluating conversational AI for agricultural advisory (DG-Eval). arXiv:2603.03294.
- Reza, Nimi & Shahid (2026). KrishokTech: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory. EACL 2026. *(cite by filename per docs/PAPER_POLICY.md; local PDF in `paper/done papers/`)*
- Reza, Maria & Nimi (n.d.). AgRiTrust retrieval benchmark companion. *(local PDF in `paper/done papers/`; public identifier pending)*
- Anonymous et al. (2025) [G0]. Supervised vs zero-shot VLM crop-disease identification. arXiv:2512.15977. *(authorship to resolve at assembly)*
- IPM-AgriGPT (2025). Mathematics 13(4):566, DOI 10.3390/math13040566.
- BUNO / bnunicodenormalizer (2024). LREC-COLING 2024, 2024.lrec-main.1479; arXiv:2306.01743.
- BhasaBodh (2025). BanglaLP @ NAACL 2025, 2025.banglalp-1.9.
- RAGChecker / RAGAS (2025). Diagnostic frameworks for RAG. *(identifiers per cluster 07 at assembly)*
- Singh et al. (2025). DecEx-RAG. EMNLP 2025 Industry, 2025.emnlp-industry.99.
- Li et al. (2026). Faithful industrial RAG. ACL 2026 Industry, 10.18653/v1/2026.acl-industry.42. [G0]

*End of draft v1.*
