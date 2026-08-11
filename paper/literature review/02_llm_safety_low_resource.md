# Cluster 2 — LLM Safety & Guardrails for Low-Resource Languages: Literature Findings (2025 → Aug 2026)

**Generated:** 2026-08-12 · **Scout:** 2 (safety matrix + formal gaps; safety-benchmark papers cross-verified by Scout 3's sweep) · **Status:** citations verified via fetched arXiv/Anthology pages

> Companion artifacts at root docs: this scout also appended a **Competitive Matrix** to `LITERATURE_REVIEW.md` (root) and produced formal gap objects in `11_RESEARCH_GAPS_competitive_matrix.md` (this folder).

---

## 1. Key papers

### 1.1 Multilingual safety classifiers / guardrails (Bengali coverage status)

| Paper | Venue / ID | Contribution | Bengali status |
|---|---|---|---|
| IndicSafe (2026) | arXiv:2603.17915 | 6,000 culturally grounded prompts across 12 Indic languages, native-speaker translated; cross-language agreement only 12.8%; SAFE-rate variance >17% | Bengali included as 1 of 12, standard script only |
| IndicGuard (2026) | arXiv:2606.22841 | Gemma-3-4B-IT fine-tuned as an Indic safety guard; 10 languages; zero-shot transfer to Dogri/Konkani/Sanskrit with 4–8% macro-F1 drop | Bengali is a training language |
| LinguaSafe (2025) | arXiv:2508.12733 | 45K entries, 12 languages; translated + transcreated + natively sourced; explicitly notes Bengali safety degradation in prior work; oversensitivity measured separately | Bengali included, standard script |
| SGToxicGuard | 2025.emnlp-main.612 | Red-teaming for Singlish, Chinese, Malay, Tamil with three interaction scenarios | Template for reporting safety evaluations per language variety |
| IndicJR (2026) | arXiv:2602.16832 | 45,216 jailbreak prompts over 12 Indic languages incl. Bengali; romanized/mixed orthography drops contract-bound JSR from 0.755 to 0.416 (Δ −0.34); English→Indic attacks transfer strongly (≥0.58 in all languages) | **Orthography changes jailbreak rate** — direct evidence for treating Banglish/romanized input as a distinct attack surface |
| RefusEU | 2026.findings-acl.1537 | DPO experiments: English-only alignment insufficient for cross-lingual safety; multilingual refusal data improves safety without Global MMLU loss | Generic recipe for Bengali refusal tuning |
| PolyRefuse | arXiv:2505.17306 | Refusal directions transfer across 14 languages; compliance rates in low-resource languages rise past 0.87 post-ablation | Refusal is a transferable direction — relevant to Gemma-4B local path |

### 1.2 Multilingual safety benchmarks — the Bengali gap

- **SafetyBench / XSafety lineage:** English + XSafety's 10 languages — **no Bengali row** in the published class sets; no banned-agrochemical or poisoning category exists in MLCommons-style hazard taxonomies (verified class-name inspection per `11_RESEARCH_GAPS_competitive_matrix.md`, Gap 2).
- **RefusalBench** (arXiv:2510.10390, Oct 2025): 176 perturbations, 6 uncertainty categories; best model 73.0% (NQ) / 47.4% (multi-doc); English, generic-domain only.
- **RAGREFUSE:** includes chemical domains but English-only, not agricultural practice.

### 1.3 Epistemic safety / "I don't know" behavior

- **LitmusEvals** (2026, litmusevals.org): the instruction "never say you don't know" causes catastrophic collapse in 8/11 models (**26-point cliff**); omitting the escape hatch produces **−15.6 pp degradation** in correct refusal; with the explicit line: 92% correct behavior vs 76% without.
- **Do RALMs Know When They Don't Know?** (arXiv:2509.01476, AAAI 2026): irrelevant retrieved contexts cause **over-refusal** on answerable queries; two-stage uncertainty + context-utility signal balances refusal vs accuracy — "decide before you retrieve" is a published, validated pattern.
- **Confidence-Based Response Abstinence** (arXiv:2510.13750, UncertaiNLP@EMNLP 2025): production financial RAG; abstains 29.9% of responses at precision 0.95 — abstention as a first-order feature with latency constraints.
- **Energy-Based Abstention for Healthcare RAG** (arXiv:2509.04482): AUROC 0.961 on hard near-distribution abstention; two abstention classes (out-of-domain vs near-domain) — formalizes KrishokChat's `banned_or_restricted_chemical` vs `off_topic` as distinct abstention classes.

### 1.4 Prompt injection defense (2025–2026)

- Field state: detection-vs-mitigation split; safety classifier robustness against injection in RAG/agent pipelines is an open evaluation problem (no Bengali agricultural injection benchmark exists).
- KrishokChat's own design (pre-retrieval terminal category, regex precheck + JSON classification; poisoned-context attacks impossible because context never reaches the generator for terminal classes) is ahead of every competitor reviewed in `11_RESEARCH_GAPS_competitive_matrix.md` Gap 2 (taxonomy containment: all five competitor decision vocabularies have zero intersection with the six KrishokChat classes).

### 1.5 Domain-specific safety (agrochemical, self-harm, helpline patterns)

- **No deployed system** in the 2025–2026 literature implements classification-then-refusal with a live national helpline fallback (KrishokBondhu emits an "expert referral" mention in 100% of responses but has no escalation measurement; Farmer.Chat has no escalation layer; India's KCC AI/ML integration — PIB Dec 2025 — is announced policy, not evaluated).
- Medical abstention papers (ClinicBot numeric string-match, MedRAGChecker KG+NLI, atomic fact-checking catching dosage errors) provide the transferable dosage-interception mechanisms — all English clinical.

## 2. Findings & insights

- **Multilingual guardrails cover Bengali as one row in a matrix, standard script only.** Six 2025–26 resources (IndicSafe, IndicGuard, LinguaSafe, SGToxicGuard, IndicJR, RefusEU) include Bengali; none covers dialectal forms. IndicSafe's 12.8% cross-language agreement is the quantified motivation for per-language (per-dialect) safety evaluation.
- **Orthography changes safety behavior.** IndicJR: romanized/mixed orthography drops jailbreak success rate from 0.755 to 0.416 (Δ −0.34). Bengali farmers type Banglish/romanized — a separate attack surface with no dedicated benchmark.
- **Dialectal safety is entirely unpublished.** Sylheti, Chittagong, Rangpur, Noakhali, Barishal, Mymensingh forms of the *same harmful or benign intent* have no published evaluation anywhere. Not in IndicSafe, not in LinguaSafe, not in any refusal benchmark.
- **Refusal is an engineered, measurable capability** — RefusalBench's <50% multi-doc accuracy for frontier models means "selective refusal must be built and measured, not assumed."
- **The "I don't know" line is load-bearing**: LitmusEvals' 92% vs 76% split is the quantitative case for KrishokChat's explicit system-prompt instruction.

## 3. Research gaps

1. **No multi-dialect safety/refusal dataset for Bangla.** The team's 20,112-record, 6-dialect dataset is a first mover; the field's own data (IndicSafe 12.8% agreement; IndicJR −0.34 orthography shift) provides the quantified problem statement.
2. **No agricultural-domain Bengali safety benchmark.** AgriEval is Chinese; agricultural safety scoring exists only as three-axis rubrics (IPM-AgriGPT: professionalism/safety/effectiveness) in Chinese; Bayer's E.L.Y. benchmark is English crop-protection. The banned-agrochemical + self-harm/poisoning categories KrishokChat classifies do not exist in any published taxonomy.
3. **No helpline-escalation evaluation.** Nobody measures whether AI-system referrals to national helplines (16123) are followed, recalled, or acted on (see Cluster 9).
4. **LLM-as-judge is documented as unreliable for Bengali** (Pariksha: lowest human–judge agreement for Bengali/Odia; multilingual judge κ≈0.3; JuICE best judge F1 0.52) — any safety evaluation must use native human validation with agreement statistics.

## 4. Conventions

- Report automated filter pass rates, LID thresholds, decontamination (13-gram BnMMLU protocol, <0.1% overlap), native-speaker human validation counts, and inter-annotator agreement; LLM-judge-only validation is openly contested for Bengali.
- Parallel standard↔dialect formatting is the community norm; per-dialect annotator counts stated.
- CC-BY-4.0 dominates dataset licensing; HF + GitHub release with a referenced dictionary/map file.
- Safety evaluations must state oversensitivity separately from under-sensitivity (LinguaSafe convention).

## 5. Positioning recommendations for KrishokChat

1. Position the safety dataset as **the first multi-dialect (6 varieties, 110-word genuine map) refusal/safety resource for Bangla**, opening with IndicSafe's 12.8% cross-language agreement and IndicJR's Δ −0.34 orthography result as the quantified problem statement.
2. Present the 6-way taxonomy's enrichment claims with the taxonomy-containment argument (formalized in `11_RESEARCH_GAPS_competitive_matrix.md` Gap 2): no published guardrail or RAG-gating vocabulary contains banned-agrochemical/poisoning terminal classes.
3. Do not rely on LLM-as-judge for refusal classification or dialect-fidelity claims: native per-dialect human validation with agreement statistics (per Pariksha/JuICE evidence).
4. Adopt LinguaSafe's oversensitivity-vs-undersensitivity split reporting for the safety router.
5. Frame the verification output (dosage interception rate) with the medical-literature mechanisms (ClinicBot string-match / MedRAGChecker KG check) as the agrarian analogue — and claim the first such measurement.