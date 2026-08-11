# Literature Review: KrishokChat Agricultural AI Advisory System

**Generated:** 2026-08-09
**Scope:** RAG-vs-LLM decision architectures, agricultural advisory AI, ethical frameworks, user trust, production best practices
**Application Context:** Bangladesh agri-advisory chatbot serving Bangla-speaking farmers with critical crop decisions

---

## 1. RAG-as-Judge / Confidence-Threshold Approaches

### 1.1 ConfRAG — Confidence-Guided RAG Triggering (2025)

**Source:** arXiv:2506.07309v2

**Core technique:** Fine-tune an LLM to emit "I am unsure" when it cannot answer correctly. Use this calibrated uncertainty as the sole RAG trigger. For static factual questions, run LLM generation and RAG pipeline **in parallel**; halt RAG early if LLM emits a confident answer.

**Key findings:**
- LLMs are systematically overconfident; self-reported confidence is unreliable for RAG triggering without calibration.
- ConfQA fine-tuning on atomic factual statements reduces hallucination from 20–40% to **below 5%**.
- With a perfect RAG backend, ConfRAG achieves >95% accuracy. With real RAG, it matches always-RAG quality while reducing P50 latency by **>600ms** and unnecessary retrievals by **5–19%**.
- The "dampening prompt" ("answer only if you are confident") is the critical design choice.

**Implication for KrishokChat:** A Bangla-calibrated confidence signal on the generator (Gemini) could trigger retrieval only when needed. However, Gemini's confidence is not directly accessible via API — alternative: use consistency sampling (generate multiple times, measure agreement) as a proxy (see §1.3).

---

### 1.2 Self-RAG — Self-Reflective RAG (ICLR 2024)

**Source:** Asai et al., ICLR 2024. "SELF-RAG: Retrieve, Generate, and Critique through Self-Reflection."

**Core technique:** Train a single LM to emit special *reflection tokens*:
- `Retrieve` — whether retrieval is needed
- `ISREL` — Is the retrieved passage relevant?
- `ISSUP` — Is the output supported by the passage?
- `ISUSE` — Is the output useful to the user?

At inference, segment-level beam search scores candidate continuations using weighted reflection token probabilities, enabling hard/soft constraints (e.g., reject segments with `ISSUP=No support`).

**Key findings:**
- Self-RAG 7B outperforms ChatGPT, Llama2-chat, and standard RAG on open-domain QA, reasoning, and fact verification.
- Adaptive retrieval via threshold on `Retrieve=Yes` probability enables test-time control over retrieval frequency.

**Limitation for KrishokChat:** Requires fine-tuning the generator — not feasible with closed API models (Gemini). The reflection-token architecture is incompatible with black-box LLM APIs. Alternative: emulate with prompt-based self-critique (see §6.2).

---

### 1.3 Uncertainty Detection for Dynamic RAG (2025)

**Source:** arXiv:2501.09292v1, "To Retrieve or Not to Retrieve? Uncertainty Detection for Dynamic RAG"

**Core technique:** Generate N responses to the same query; compute pairwise similarity; derive uncertainty estimates using multiple metrics.

**Results on multi-hop QA (HotpotQA):**

| Uncertainty Estimator | Retrieval Trigger | F1 | # Searches (vs Always=4.6) |
|---|---|---|---|
| Always Retrieve | — | 0.552 | 4.60 |
| **Eccentricity** | U > 2 | **0.605** | **2.23** |
| Degree Matrix (Jaccard) | U > 0.4 | 0.593 | 1.46 |
| Degree Matrix (NLI) | U > 0.5 | 0.535 | 2.25 |
| Semantic Sets | U > 2 | 0.411 | 2.52 |

**Key finding:** Eccentricity-based uncertainty detection reduces retrieval calls by **>50%** while slightly *improving* F1 (0.605 vs 0.552). Lightweight Jaccard similarity on token sets works nearly as well.

**Implication for KrishokChat:** Consistency-sampling with 3 generations + Jaccard similarity is computationally feasible and API-compatible. Threshold can be tuned on a Bangla agricultural query dev set.

---

### 1.4 Adaptive-RAG — Question Complexity Routing (NAACL 2024)

**Source:** Jeong et al., NAACL 2024. "Adaptive-RAG: Learning to Adapt Retrieval-Augmented LLMs through Question Complexity."

**Core technique:** Train a small classifier to predict query complexity:
- **Level 1 (simple):** No retrieval needed (LLM-only)
- **Level 2 (moderate):** Single-step retrieval
- **Level 3 (complex):** Multi-step iterative retrieval

**Key finding:** Outperforms always-RAG and no-retrieval baselines across mixed-complexity query distributions. The classifier is a small LM (e.g., T5-based) trained on automatically labeled data from actual model predictions.

**Implication for KrishokChat:** A lightweight Bangla query classifier (even keyword-based) can route: "আলুর দেলি ব্লাইট" (potato late blight) → retrieval (specific treatment needed); "কত তারিখে ধান রোপা করব" (when to transplant rice) → retrieval needed with seasonal context; "টমেটো কি" (what is tomato) → LLM-only sufficient.

---

### 1.5 SEAKR — Self-Aware Knowledge Retrieval (ACL 2025)

**Source:** Yao et al., ACL 2025. "SeaKR: Self-aware Knowledge Retrieval for Adaptive RAG."

**Core technique:** Extract uncertainty from LLM internal states (FFN activations at the last token across layers), not from outputs. Trigger retrieval when self-aware uncertainty exceeds threshold δ > −6.

**Key findings:**
- Internal-state uncertainty detects knowledge insufficiency more reliably than output-probability methods.
- Outperforms FLARE, DRAGIN, and Self-RAG on complex QA (HotpotQA, MuSiQue).
- Tuning-free — works without fine-tuning.

**Limitation for KrishokChat:** Requires white-box access to model hidden states — not available via Gemini API. Relevant as architectural aspiration for future self-hosted model.

---

### 1.6 KBM — Knowledge Boundary Model (2024)

**Source:** Zhang et al., arXiv:2411.06207. "KBM: Delineating Knowledge Boundary for Adaptive Retrieval."

**Core technique:** Train a classifier on soft labels derived from (a) accuracy sampling (does LLM answer correctly without RAG?) and (b) certainty sampling (entropy of multiple generations). Threshold τ = 0.9 separates known from unknown.

**Key findings:**
- Accuracy-based KBM: reduces retrieval ratio by **32.5%** with only 0.39% performance drop across 11 QA datasets.
- Certainty-based KBM: reduces retrievals by 13.5% with slight performance gain.
- Pearson correlation between accuracy and certainty: 0.64.

**Implication for KrishokChat:** A certainty-based classifier trained on Bangla query consistency can serve as the routing gate. The training data can be auto-generated: run Gemini on labeled Bangla queries multiple times, measure agreement, label as "known" (high agreement, correct) vs "unknown" (disagreement or wrong).

---

### 1.7 Fin AI Engine — Production System (Intercom)

**Source:** Intercom Fin documentation + fin.ai/research, 2025.

**Architecture:**
1. Query refinement and optimization
2. Retrieval via proprietary `fin-cx-retrieval` model (fine-tuned Snowflake Arctic 2, +30 precision points, +10 Recall@5 vs general model)
3. Reranking via `fin-cx-reranker` (scores for relevance, accuracy, usefulness)
4. Answer generation via `Fin Apex 1.0`
5. **Validation gate:** If output doesn't meet confidence/safety thresholds → ask customer to clarify or escalate to human.

**Key production insight:** The confidence check at step 5 is the critical safety layer. Fin does NOT fall back to ungrounded generation — it escalates. Retrieval precision improved 30 points through domain-specific fine-tuning on hard positives/negatives from production logs.

**Implication for KrishokChat:** (a) A validation gate after generation is essential; (b) domain-adapted retrieval matters more than generation model upgrades; (c) escalation path (human/helpline) is the correct behavior when confidence is low.

---

### 1.8 Glean — Enterprise RAG Architecture

**Source:** glean.com/blog, 2025-2026.

**Architecture:** Plan → Retrieve → Generate → Self-Reflect. Agents self-assess confidence in initial search results; if insufficient, escalate from search to agentic reasoning (multi-step tool use). Glean's evaluation: human graders preferred Glean's answers **1.9× more often** than ChatGPT's company knowledge and **1.6×** vs Claude's.

**Key insight:** "Reasoning could not be left solely to the LLM; the RAG system needed to guide the reasoning process." Rich context enables intent inference rather than guessing.

**Implication for KrishokChat:** The agentic pipeline architecture (safety → retrieval → generation → verifier) with self-reflection aligns with Glean's proven production pattern.

---

### 1.9 Calibrated Retrieval-Budget Allocation (2025)

**Source:** Dong et al., arXiv:2606.29959. "Know Before You Fetch."

**Core technique:** Calibrate sequence log-probability into probability-of-correctness. Map to 4 decisions:
- **k=0 (closed-book):** LLM-only, no retrieval
- **k=1 (compact retrieval):** Retrieve 1 passage
- **k=5 (full retrieval):** Retrieve 5 passages
- **Abstain:** Neither closed-book nor retrieved answer is trustworthy

**Calibration results:** ECE drops from 0.275 → 0.062 (TriviaQA), 0.643 → 0.009 (NQ), 0.711 → 0.031 (MS MARCO).

**Key finding:** At matched-accuracy, the method skips retrieval for ~1/3 of TriviaQA queries while staying within 1.5 points of always-RAG accuracy. For low-headroom datasets (NQ, MS MARCO), it correctly chooses near-always retrieval.

**Implication for KrishokChat:** This is the most operationally complete decision framework. The 4-way decision (LLM-only / compact / full / abstain) maps directly to KrishokChat's response modes. Calibration is essential — raw log-probabilities are miscalibrated.

---

## 2. Grounded Generation with Fallback

### 2.1 Perplexity AI — Retrieval-First Architecture

**Source:** DataStudios.org audit, ZipTie.dev analysis, 2025-2026.

**Pipeline:** Query intent parsing → Real-time web retrieval (BM25 + dense) → Multi-layer ML ranking (L1-L3 rerankers) → Structured prompt assembly with pre-embedded citations → Constrained LLM synthesis.

**Grounding spectrum (3 levels):**

| Level | Description | Trust Calibration |
|---|---|---|
| **Fully cited** | Inline citation maps to specific source | Verify cited source supports claim |
| **Synthesis-informed** | Draws on context without explicit citation | Cross-reference against cited sources |
| **Parametric fallback** | LLM training memory used when retrieval insufficient | Treat as unverified |

**Failure modes identified by Columbia Journalism Review audit (2025):** 37% error rate. Two failure types: (1) misattribution (correct info, wrong source), (2) fabrication (wrong info, irrelevant citation).

**Key insight:** "Citations make claims checkable, not correct." Even the best retrieval-first system hallucinates. Grounding reduces but does not eliminate fabrication.

**Implication for KrishokChat:** Citation-level transparency is essential. When the KB has partial info, the system should cite what it has and explicitly flag the gap. "According to [KB-node-47], late blight is caused by *Phytophthora infestans*. The specific dosage for your variety is not in my knowledge base — consult Krishi Call Center 16123 for local recommendations."

---

### 2.2 Microsoft Bing Copilot / Copilot Studio

**Source:** Microsoft Learn documentation, 2025.

**Architecture:** Message moderation → Query optimization → Information retrieval (Bing Custom Search) → Grounding check + provenance check + semantic similarity cross-check → Summary generation → Dual content check (on input and before response).

**Key feature:** "Allow ungrounded responses" setting loosens citation restriction — explicitly configurable. Default is grounded-only.

**Implication for KrishokChat:** The configurable grounding strictness is a useful design pattern. KrishokChat should default to "grounded only" with explicit ungrounded flags when the LLM fills gaps.

---

### 2.3 "Attribute First, Then Generate" (ACL 2024)

**Source:** Slobodkin et al., ACL 2024. "Attribute First, then Generate: Locally-attributable Grounded Text Generation."

**Core technique:** Decouple generation into: (1) content selection (identify relevant source segments), (2) sentence planning, (3) sequential generation conditioned on selected segments. Citations are structural, not retrofitted.

**Key finding:** More concise citations than document-level attribution, with maintained or improved generation quality and attribution accuracy. Significantly reduces human verification time.

**Implication for KrishokChat:** Attribution granularity matters. Citing specific KB nodes (not just "the knowledge base") enables verification and builds trust. Each claim should trace to a specific retrieved passage.

---

### 2.4 Grounded Generation — Pattern Summary

**Source:** ZeroEntropy.dev concepts, 2025.

**Three requirements for grounded generation:**
1. **Source-only instruction:** "Answer only from provided sources. If no source supports, say 'I do not know.'"
2. **Tagged sources:** Each document gets an ID ([SRC-1], [SRC-2]) that the model references.
3. **Citation-bearing output:** Output schema requires citation markers per claim.

**Post-hoc verification:** Decompose answer into atomic claims; check each claim's cited source for entailment. RAGAS, TruLens, DeepEval implement variants. Faithfulness = fraction of claims entailed by cited source.

**Implication for KrishokChat:** The prompt architecture for generation must include (a) explicit source-only instruction, (b) tagged KB nodes with IDs, (c) per-claim citation enforcement, (d) a verifier pass that checks entailment.

---

## 3. Agricultural Advisory AI Systems

### 3.1 Farmer.Chat — Digital Green + Microsoft Research (2024-2025)

**Source:** Singh et al., 2024. "Farmer.Chat: Scaling AI-Powered Agricultural Services for Smallholder Farmers." Microsoft Research. + Digital Green deployment data, 2025.

**Scale:** 830,000+ users across Kenya, Nigeria, Ethiopia, India, Brazil. 5 million+ queries answered.

**Architecture:** RAG-based generative AI chatbot. Multimodal (voice, text, image). Integrates Tomorrow.io weather data. Content from CGIAR open-access research + CABI proprietary materials (via GAIA project).

**60 Decibels impact study (2025, Kenya, n=450):**
- NPS: 63 (top 20% of 60dB benchmarks)
- 82% find Farmer.Chat "very trustworthy"
- 83% report "much more confident" decision-making
- 61% apply advice from Farmer.Chat (in-app survey)
- **Key finding:** When information is complete, 86% feel confident acting on it vs 48% when incomplete.
- **Attribution match:** Only ~65% of farmer actions matched the recommendation (complete + partial match). 35% did not match.
- Trust is gender-differentiated: Female farmers report higher trust (NPS 75 vs 57).

**GAIA Project Phase II (2025-2027):** IFPRI-led. Three objectives: (1) expand content + data governance framework + GenAI ethics toolkit, (2) integrate real-time data + predictive analytics + multimodal, (3) establish evaluation/benchmarking for LLM performance in agricultural extension (accuracy, timeliness, gender-sensitivity, contextualization).

**Implication for KrishokChat:** Farmer.Chat is the closest architectural analog. The finding that **complete information drives 38 percentage points of confidence** (86% vs 48%) is the strongest evidence for building a robust "I don't know + redirect" mode rather than a hallucinated answer. The 65% action-match rate shows room for improvement — verification matters.

---

### 3.2 PlantVillage Nuru — Penn State / WAVE

**Source:** Multiple adoption studies (Côte d'Ivoire 2024, Benin 2024).

**Function:** AI image-based cassava disease detection. Not a text Q&A system. Provides real-time diagnosis + management advice.

**Adoption data:**
- Côte d'Ivoire: 45% adoption among trained farmers
- Benin: 14.1% adoption
- Barriers: 65% lack smartphones, 41% find app complex
- 100% of users consider it reliable for diagnosis
- Farmers: "the application is only an aid to disease identification... it is no substitute for human intervention"

**Key insight:** Technology is positioned as **aid, not authority**. Farmers maintain decision-making autonomy. Trust is high for diagnostic function but the system explicitly defers to human judgment for treatment decisions.

**Implication for KrishokChat:** Position KrishokChat as decision-support, not decision-maker. Explicitly state "this is general guidance; for your specific field conditions, consult local extension." The Krishi Call Center 16123 redirect is exactly this deferral mechanism.

---

### 3.3 FarmBeats — Microsoft Research

**Source:** Microsoft Research, ongoing since 2016.

**Function:** IoT + drone + sensor data → precision agriculture. Not an advisory chatbot. Data-driven farming with farmer's knowledge as co-input: "Data, coupled with the farmer's knowledge and intuition about his or her farm, can help increase farm productivity."

**Relevance:** Validates the "AI as augmenter, not replacer" philosophy for agricultural AI. The human-in-the-loop is architecturally central, not an afterthought.

---

### 3.4 ICRISAT iSAT — Intelligent Agricultural Systems Advisory Tool

**Source:** ICRISAT / ISSCA, 2024-2025.

**Architecture:** AI + rule-based engine integrating weather forecasts, soil, crop, and local datasets. Generates seasonal and 5-day weather-based crop advisories in local languages via SMS, WhatsApp, and extension networks.

**Scale:** 6,000+ farmers across Andhra Pradesh, Odisha, Maharashtra (India). Piloted in Kenya (maize advisory, AICCRA 2019-2020). Scaling in Maharashtra + Ethiopia.

**Upgrade path (2025):** Being enhanced into "AI-powered Context-Specific Agromet Advisory Services" under India's Monsoon Mission III. Will include an AI-powered WhatsApp bot. Foundation for MausamGPT (national-scale integration of weather forecasts + agricultural data + LLMs).

**Key design principle:** "Operate with minimal digital infrastructure, requires only basic connectivity and local data inputs."

**Implication for KrishokChat:** The multi-channel delivery (WhatsApp, SMS) and minimal-infrastructure design is directly applicable for Bangladesh. The rule-based + AI hybrid engine is a pragmatic architecture when LLM reliability is imperfect.

---

### 3.5 Kisan Call Centre (KCC) — India

**Source:** Multiple data analytics papers, 2024.

**Scale:** 28.6 million call-log records over 8 years. 11,836 unique agricultural problems across crops, states, and topics (seeds, weeds, fertilizer, plant protection).

**Analytics pipeline (TPTC):** Time-series clustering of query volumes → trend identification (increasing/decreasing problems) → forecasting (TBATP1 model: RMSE=0.034, MAE=0.107).

**Satisfaction data:** Puneeth et al. (2024) report farmer satisfaction with KCC advisories, but also document that AI-generated advisories often lack cultural fit, gender inclusivity, and localized examples. Farmers skeptical of source credibility via digital channels. Trust in AI advisories remains low; farmers prefer extension officers or local radio.

**Implication for KrishokChat:** The KCC experience confirms: (a) SMS/WhatsApp delivery is viable at scale, (b) local language + cultural adaptation is non-negotiable, (c) trust requires credible source attribution, (d) the 16123 helpline is the established trusted channel KrishokChat should defer to.

---

### 3.6 Digital Agro-Advisory Tools — Behavioral Analysis (2025)

**Source:** Springer Discover Agriculture, 2025. "Digital agro-advisory tools in the global south: a behavioural analysis."

**Five typologies of digital agri-tools:**
1. Low-adoption: Advisory info services, post-harvest loss reduction
2. Medium-adoption: Financial inclusion, early warning systems
3. High-adoption: Climate-smart agriculture, farmer empowerment/communication/crowdsourcing

**Barriers:** Low digital literacy, infrastructure, scalability, trust, data privacy. "Most digital agro-advisory tools struggle to grow due to lack of financing."

**Critical finding:** "For most of these agro-advisory tools, requirement elicitation from farmers will improve the potential benefits." Farmer-centric design is central to adoption.

---

## 4. Ethical Frameworks for AI Advisory

### 4.1 Teaching LLMs What They Don't Know (NeurIPS 2024)

**Source:** NeurIPS 2024. "Large Language Models Must Be Taught to Know What They Don't Know."

**Core finding:** Prompting alone is insufficient for calibrated uncertainty. Fine-tuning on ~1,000 graded examples (correct/incorrect) produces calibrated uncertainty estimates that generalize across distributions. Users are sensitive to informed confidence scores — calibrated confidence changes reliance behavior (strongest effect with LoRA + linear probe confidence).

**User study (N=181):** Participants shown LLM predictions + uncertainty estimates. With calibrated uncertainty, participants modulated reliance correctly (agreed when confident, disagreed when uncertain). With random confidence, participants ignored the signal.

**Implication for KrishokChat:** If KrishokChat communicates confidence to farmers (e.g., color-coded trust indicators), the confidence must be calibrated — not random. An uncalibrated confidence indicator is worse than no indicator.

---

### 4.2 Calibration Gate Framework (2026)

**Source:** Doron Katz, "AI Advice Needs a Calibration Gate," 2026. Integrating Marcoccia et al. and Shaw & Nave preregistered experiments (2026).

**Key findings:**
- Without AI advice, participants suspended judgment 44% of the time. With deliberately wrong AI advice: **3%**. Wrong AI advice reduced willingness to say "I don't know" by 41 percentage points.
- Accurate AI advice increased accuracy by 25 points; faulty advice reduced accuracy by 15 points. **Confidence still increased after errors.**
- The "uncomfortable combination": less accurate + more confident + less willing to withhold judgment.

**Operational response — The Calibration Gate:**
1. Define maximum acceptable rate of "wrong and confident" decisions per task type
2. Track confidence vs. correctness gap, not just accuracy average
3. Provide clear paths to withhold judgment / request evidence / ask for clarification
4. Verify users can disregard or reverse AI output

**Implication for KrishokChat:** This is the ethical core of the system. For crop-disease treatment queries: (a) never present a specific dosage without KB grounding, (b) confidence must be calibrated per consequence class, (c) the "I don't know — call 16123" path must be always available and easy to use.

---

### 4.3 LitmusEvals — Epistemic Safety in Deployed AI (2026)

**Source:** litmusevals.org, 2026. 78,631 evaluations across 11 frontier models.

**Core findings:**
- The instruction "never say you don't know" causes catastrophic collapse in 8/11 models (**26 percentage point cliff** in one instruction step).
- Omitting the escape hatch ("if you don't know, say so") produces **-15.6 percentage point degradation** in correct refusal behavior (p=1.37×10⁻⁸).
- Enterprise prompts rarely contain the explicit trigger (0.5% across 2,300+ analyzed prompts), but the innocent omission is common and harmful.
- **The fix is one line:** "If you don't have enough information to answer, say so." With the line: 92% correct behavior. Without: 76%.
- Safety evaluations predict deployment behavior for properly-trained models (0pp divergence between eval and deploy framings).

**Implication for KrishokChat:** The system prompt MUST contain an explicit "say I don't know" instruction. This is not optional — omitting it measurably degrades refusal behavior. The system prompt should explicitly state: "If the knowledge base does not contain the answer, say so and redirect to Krishi Call Center 16123."

---

### 4.4 Automation Bias and Medicolegal Accountability

**Source:** PMC, "Explaining decisions without explainability? AI and medicolegal accountability," 2024.

**Key concepts:**
- **Automation bias:** Tendency to over-rely on machine decisions. Incorrect AI recommendations worsened clinician judgment across experience levels.
- **Medicolegal standard of reasonableness:** Decisions are reasonable if they draw from totality of evidence, contextualized to the situation. AI output is one input, not the sole source.
- **Learned intermediary doctrine:** Clinicians using AI assume liability. The AI is an aid, not the decision-maker.

**Implication for KrishokChat:** The system is a learned intermediary tool. The farmer (and by extension, any extension worker using the tool) bears responsibility. The system must: (a) present AI output as one input among many, (b) flag uncertainty explicitly, (c) maintain an audit trail (query → classification → action → timestamp), (d) never present AI output as definitive advice for high-consequence decisions (pesticide dosages, treatment amounts).

---

### 4.5 EU AI Act — High-Risk System Requirements (2026)

**Source:** EU AI Act Article 14, enforcement August 2026.

**Requirements for high-risk AI systems:**
- Human oversight measures addressing automation bias
- Ability to disregard, override, or reverse system output
- Accuracy and robustness appropriate to the intended purpose
- Transparency about capabilities and limitations

**Implication for KrishokChat:** While KrishokChat is not an EU-regulated system, Article 14 provides a best-practice checklist. The safety agent + verifier agent architecture satisfies the "human oversight" and "override" requirements by design.

---

## 5. User Trust and Behavior

### 5.1 The Calibration Gap (UC Irvine, 2025)

**Source:** Steyvers et al., TechXplore 2025.

**Core findings:**
- People consistently **overestimate** LLM accuracy. "There's a disconnect between what LLMs know and what people think they know" — the calibration gap.
- **Discrimination gap:** Users cannot distinguish correct from incorrect LLM answers.
- **Intervention that works:** Providing uncertainty language linked to internal confidence (low: "I am not sure"; medium: "I am somewhat sure"; high: "I am sure") strongly influenced human confidence in the right direction.
- **Dangerous confound:** Longer explanations increase user confidence even when accuracy is unchanged.

**Implication for KrishokChat:** (a) Do not use verbose Bangla explanations as a trust signal — length correlates with confidence but not accuracy. (b) Explicit uncertainty phrasing in Bangla ("আমি নিশ্চিত নই" / "আমি মোটামুটি নিশ্চিত" / "আমি পুরো নিশ্চিত") should be used. (c) The default assumption must be that farmers will over-trust the system — the architecture must compensate.

---

### 5.2 Trust in AI Farming Tools (Agronomy Journal, 2024)

**Source:** Gardezi et al., Brugler et al., Joshi et al., Agronomy Journal special section 2024.

**Survey of 312 South Dakota farmers + CCAs:**
- 70% are "apprehensive adopters" — concerned about security, knowledge, cost
- 22% "risk-averse" — highly concerned about all four categories
- 59.6% of CCAs believe AI will impact their work in next 5 years
- **Crop advisers are the critical trust bridge:** "The crop adviser's role cannot be underestimated."
- Farmers with negative past experiences with agtech vendors become reluctant to try similar tools even from academic sources.

**Four trust categories:** Cost, knowledge, security, confidence. Confidence = "I still need to field check the recommendations."

**Implication for KrishokChat:** Trust is built through local intermediaries (extension officers, NGOs), not directly. The system should be positioned as a tool *for* extension workers, not a replacement. Field-checking (verification against reality) should be explicitly encouraged in the UI.

---

### 5.3 Farmer.Chat Trust Data (60 Decibels, 2025)

**Key stats (n=450, Kenya):**
- 82% "very trustworthy"
- 61% learned new information from it
- 79% say access to reliable information became "much easier"
- 83% "much more confident" in decision-making
- **Gender gap:** Women report higher trust and satisfaction (NPS 75 vs 57)
- **Comprehension barrier:** 71% of those who understood "some/none" of the info did not apply it vs 51% of those who understood "all/most"

**Implication for KrishokChat:** (a) Simpler Bangla + voice output addresses the comprehension barrier directly. (b) Trust is achievable but fragile — one bad experience with wrong advice can destroy it. (c) Female farmers may be a particularly responsive demographic in Bangladesh.

---

### 5.4 Microsoft Overreliance Mitigation Framework

**Source:** Microsoft AI Playbook, 2025.

**Three UX goals for appropriate reliance:**
1. **Create realistic mental models** — users understand capabilities, limitations, and error rates
2. **Signal when to verify** — make it easy to spot mistakes
3. **Facilitate verification** — decrease cognitive load for checking

**Risk factors for overreliance:** Low AI literacy, lack of domain expertise, low task familiarity, high overall trust in AI.

**Implication for KrishokChat:** Bangladeshi farmers are high-risk for overreliance (low AI literacy, high trust). The system must: (a) explicitly state its limitations upfront, (b) show confidence/trust indicators, (c) make verification easy (show sources, cite KB nodes, provide 16123 for confirmation).

---

## 6. Industry Best Practices 2024-2026

### 6.1 Production RAG Architecture — Layered Design

**Source:** Multiple sources synthesized (Clarion.ai, Zartis, aakashx.com, Kunal Ganglani playbook), 2025-2026.

**Production RAG is an enterprise retrieval system, not "LLM + vector DB."**

**Five evaluation layers:**

| Layer | What to Measure |
|---|---|
| Retrieval recall | Did the correct source appear in candidates? |
| Ranking quality | Did the correct source survive to top-k? |
| Context quality | Is final context sufficient and non-conflicting? |
| Answer faithfulness | Is the answer grounded in retrieved evidence? |
| Operational quality | Fast, authorized, current, traceable? |

**Critical failure points (from "Seven Failure Points" IEEE/ACM 2024):** Every failure traces back to retrieval quality, not generation. Validation is only feasible during operation; robustness evolves.

**Enterprise faithfulness target:** deepset recommends **>90% faithfulness** for regulated industries. Below that threshold = reliability risk.

---

### 6.2 Hybrid Search — Production Baseline

**Source:** Wang et al. (2024), production deployment studies (2025-2026).

**Finding:** Hybrid (BM25 + dense vector + cross-encoder reranking) consistently outperforms pure vector and pure keyword retrieval across open-domain QA, multi-hop QA, and medical benchmarks.

**Standard production pattern:**
1. Bi-encoder retrieval: top-50 candidates (fast, independent scoring)
2. Cross-encoder reranking: top-5 (full query-document interaction, 10-100× slower but more accurate)
3. Reciprocal Rank Fusion (RRF) merges sparse + dense ranked lists (k=60 standard)

**Implication for KrishokChat:** The existing BM25 + dense retrieval setup is correct. Adding a reranker (even a lightweight cross-encoder) would improve the top-K precision for generation. For 2,133 nodes, a reranker adds minimal latency.

---

### 6.3 RAG Fusion — Diminishing Returns in Production

**Source:** arXiv:2603.02153v1, March 2026. "Scaling RAG with RAG Fusion: Lessons from an Industry Deployment."

**Finding:** Retrieval fusion (multi-query + RRF) increases raw recall but gains are **neutralized after re-ranking and truncation** in production. Hit@10 decreased from 0.51 to 0.48 in several fusion configurations vs single-query baseline. Fusion added **0.89s overhead** with no downstream benefit.

**Implication for KrishokChat:** Do NOT add multi-query fusion as default. The added latency and complexity do not justify the marginal (or negative) quality improvement. Optimize the single-query pipeline first.

---

### 6.4 Query Rewriting — Highest-ROI Improvement

**Source:** Tianpan.co analysis, production data from ElevenLabs, 2025-2026.

**Finding:** Query rewriting (HyDE, sub-query decomposition, step-back prompting) consistently surfaces retrieval improvements that chunking experiments cannot explain. "The retrieval quality ceiling isn't set by the index — it's set by the query quality."

**Practical patterns:**
- **HyDE** (Hypothetical Document Embeddings): +6 recall points on BEIR. Best for factoid queries.
- **Sub-query decomposition:** Best for multi-facet/multi-hop queries. Parallel decomposition if independent.
- **Multi-query expansion (RAG-Fusion):** Brute-force; diminishing returns in production (see §6.3).
- **Selective application:** Route through rewrite layer only when baseline retrieval confidence is below threshold.

**Cost management:** Use a smaller model (7B-class) for query rewriting than for generation. ElevenLabs: switching from externally-hosted LLM to self-hosted Qwen 3-4B/30B dropped rewrite latency from 326ms → 155ms.

**Implication for KrishokChat:** A lightweight Bangla query reformulator (even a prompted smaller model) that converts farmer dialect queries into canonical KB-aligned queries would be the highest-ROI retrieval improvement. "আলুর দেরি ব্লাইটের প্রতিকার" → "আলুর দেরি ব্লাইট (Potato Late Blight) রোগের প্রতিকার ও ব্যবস্থাপনা."

---

### 6.5 Corrective RAG (CRAG) — Self-Correction on Retrieval

**Source:** arXiv:2401.15884, 2024.

**Core technique:** Lightweight retrieval evaluator classifies each retrieved document as:
- **Correct:** Refine and use
- **Incorrect:** Discard, fall back to web search
- **Ambiguous:** Combine internal + external knowledge

**Implication for KrishokChat:** The verifier agent already performs this function. CRAG validates the architectural pattern: evaluate retrieval quality before generation, and have corrective actions (re-retrieve, escalate, or synthesize).

---

### 6.6 AlignRAG — Critique-Driven Alignment

**Source:** arXiv:2504.14858, 2025.

**Core technique:** A Critic Language Model (CLM) trained on contrastive critique trajectories detects reasoning misalignment with retrieved evidence. At test time, iteratively refines reasoning via Critique-Driven Alignment (CDA) steps.

**Key finding:** Improves InstructRAG accuracy by **5.8%** on Qwen-2.5-14B as a plug-in module, without architectural changes.

**Implication for KrishokChat:** The verifier agent is the lightweight version of this critique loop. Training a dedicated Bangla agricultural critic model is overkill for a 7-day prototype, but the pattern (generate → critique → revise) is correct.

---

### 6.7 RAG Evaluation Frameworks

**Source:** RAGAS, TruLens, DeepEval, RagChecker, RAGOps (2024-2025).

**Key metrics for production:**
- **Faithfulness:** Fraction of answer claims entailed by cited sources (target: >90%)
- **Answer relevance:** Is the answer relevant to the question?
- **Context precision:** Is retrieved context useful?
- **Context recall:** Did retrieval surface the relevant information?

**RAGOps** (arXiv:2506.03401): Frames RAG as an operational discipline — monitoring data drift, query/response patterns, user feedback, pipeline management for evolving source data.

**RagChecker** (arXiv:2408.08067): Separates retriever failures (claim recall, context precision) from generator failures (context utilization, noise sensitivity, hallucination rate). Surgical debugging tool.

**Implication for KrishokChat:** Integrate RAGAS-style faithfulness scoring into the verifier agent. Track faithfulness as the primary quality metric.

---

### 6.8 Grounded Generation — Citation Enforcement Pattern

**Source:** Synthesized from ZeroEntropy, production implementations.

**Prompt architecture for grounded generation:**
1. **Source-only instruction:** "Answer only from provided sources. Do not use prior knowledge."
2. **Tagged sources:** Each KB node gets an ID the model references.
3. **Citation-bearing output:** Each claim carries a citation marker.
4. **Refusal clause:** "If no source supports the answer, say 'I don't know' and redirect to 16123."
5. **Post-hoc verification:** Decompose answer → check each claim against cited source → reject/flag unverifiable claims.

**Failure modes without this architecture:**
- LLM silently falls back to parametric knowledge
- Confident but ungrounded answers
- Misattribution (correct info, wrong source)
- Fabrication (wrong info, irrelevant citation)

---

## 7. Synthesis: Recommended Architecture for KrishokChat

### 7.1 Decision Framework — The Four-Way Gate

Based on the literature, KrishokChat should implement a **calibrated four-way decision** for each query:

```
Query
  │
  ▼
[Safety/Router Agent] → Classify: safe_agri | banned_chemical | self_harm | off_topic | injection
  │ (safe_agri only)
  ▼
[Retrieval Confidence Estimator] → Compute retrieval relevance score R
  │
  ├─ R ≥ θ_high (strong KB match) ──→ [KB-Grounded Generation] → Cite specific nodes
  │
  ├─ θ_low ≤ R < θ_high (partial match) ──→ [Augmented Generation]
  │    KB provides disease/context; LLM fills general guidance;
  │    flagged as "partial knowledge"
  │
  ├─ R < θ_low (no KB match) ──→ [LLM Knowledge Gate]
  │    │
  │    ├─ General/safe info ──→ Generate with disclaimer: "This is general guidance..."
  │    │
  │    └─ Specific/dosage/critical ──→ REFUSE → "আমার জ্ঞানভান্ডারে এই তথ্য নেই। 
  │         কৃষি কল সেন্টারে ফোন করুন: ১৬১২৩"
  │
  └─ Always: [Verifier Agent] → Faithfulness check → Flag ungrounded claims
```

### 7.2 Confidence Estimation — Practical Approach

**For a 7-day prototype with Gemini API:**

Use **consistency sampling** (a.k.a. self-consistency) as the confidence proxy:
1. Generate 3 responses to the same query with retrieved context (temperature=0.7)
2. Compute pairwise semantic equivalence (embedding cosine similarity or LLM-as-judge)
3. High agreement → high confidence → KB-grounded path
4. Low agreement → uncertain → partial-knowledge or refuse path

**Why this works:** Empirically validated in uncertainty detection literature (Eccentricity, Jaccard on token sets). Agreement among multiple generations correlates with correctness.

**Alternative (lighter):** Use retrieval score (BM25 + dense cosine similarity of top-1 result) as primary signal, consistency as secondary.

### 7.3 Threshold Calibration

Based on literature (ConfRAG, KBM, calibrated retrieval-budget allocation):
- **θ_high = 0.85** (cosine similarity of top retrieval result): Strong KB match → fully grounded response
- **θ_low = 0.50**: Below this, KB has no useful match
- Between: Partial knowledge mode

These thresholds MUST be calibrated on a held-out Bangla agricultural query set. The literature is clear: raw scores are miscalibrated. Build a calibration set of ~100 queries with human labels (KB-has-answer / KB-partial / KB-no-answer) and fit a logistic calibrator.

### 7.4 Handling Partial Knowledge

**The "late blight treatment" scenario:**

When KB has disease info but not exact dosage:
1. **Cite what exists:** "আলুর দেরি ব্লাইট *Phytophthora infestans* নামক ছত্রাকের কারণে হয় [KB-node-47]।"
2. **Flag the gap explicitly:** "আপনার জাত ও এলাকার জন্য সুনির্দিষ্ট ঔষধের মাত্রা আমার জ্ঞানভান্ডারে নেই।"
3. **Provide safe general guidance only if verified:** "সাধারণত ম্যানকোজেব বা ক্লোরোথালোনিল স্প্রে করা হয় — তবে মাত্রা নির্ধারণের জন্য স্থানীয় কৃষি কর্মকর্তার পরামর্শ নিন।"
4. **Always redirect:** "বিস্তারিত জানতে কৃষি কল সেন্টার: ১৬১২৩।"

**The line between "general guidance" and "hallucination":**
- Safe: Named active ingredients (widely known, low dosage sensitivity)
- Unsafe: Exact dosages (e.g., "2g per liter"), brand names, frequency, safety intervals
- Rule: If the specific number matters for safety → refuse and redirect

### 7.5 Response Mode Tags

Every response should carry a visible trust tag:

| Tag | Bangla | Meaning | When |
|---|---|---|---|
| 🟢 KB-Grounded | "জ্ঞানভান্ডার থেকে" | Fully from KB, verified | Strong retrieval match + faithfulness pass |
| 🟡 Partial | "আংশিক তথ্য" | KB has context, LLM fills gaps | Partial retrieval match |
| 🔴 General Guidance | "সাধারণ তথ্য" | From general knowledge, not KB-specific | No KB match, general info only |
| ⚪ No Answer | "তথ্য পাওয়া যায়নি" | KB + LLM cannot answer safely | Critical info needed but unavailable |

### 7.6 Farmer Persona — Design Constraints

From the literature on Bangladeshi/Global South farmers:
- **Low literacy:** Voice-first output, simple Bangla, short sentences
- **Low AI literacy:** Over-reliance risk is high; must build in calibration gates explicitly
- **Critical decisions:** Pesticide dosages and treatment timing have real economic/environmental consequences
- **Trust through intermediaries:** Extension officers, local NGOs, 16123 are trusted channels
- **Prior negative experiences:** Agtech that makes wrong recommendations destroys trust permanently

**Design implications:**
1. Voice output (TTS) for all responses
2. Short answers (max 3-4 sentences for grounded; 1-2 for redirect)
3. Always include "verify with local extension" for treatment advice
4. Krishi Call Center 16123 is the explicit escalation path
5. Never present a single "the answer is X" — always contextualize

### 7.7 Agentic Pipeline — Alignment with SOTA

The existing 4-agent pipeline (Safety → Retrieval → Generation → Verifier) aligns with:
- Glean's Plan → Retrieve → Generate → Self-Reflect pattern
- Intercom Fin's Retrieve → Rerank → Generate → Validate pattern
- Microsoft Copilot Studio's Moderate → Retrieve → Ground → Summarize → Check pattern
- Self-RAG's reflection token architecture (emulated via prompting)
- CRAG's corrective retrieval pattern

**The differentiator for KrishokChat:** Domain-specific safety classification + agricultural knowledge-boundary awareness + calibrated refusal for critical decisions. This combination is not present in any competitor system reviewed.

### 7.8 Audit Trail — Production Requirement

From the calibration gate literature and EU AI Act, every decision must be traceable:

**Minimum log schema:**
```json
{
  "query_id": "uuid",
  "timestamp": "ISO8601",
  "query_text": "আলুর দেরি ব্লাইটের প্রতিকার কি?",
  "safety_classification": "safe_agri",
  "retrieval_top_score": 0.72,
  "retrieval_top_node": "KB-0047",
  "decision_path": "partial_knowledge",
  "response_mode_tag": "🟡 Partial",
  "faithfulness_score": 0.91,
  "referred_to_helpline": true,
  "response_text": "..."
}
```

This log powers: (a) the safety metrics panel on the demo/poster, (b) calibration monitoring, (c) post-hoc debugging, (d) ethical accountability.

---

## 8. Key Citations

| # | Citation | Venue | Year | Relevance |
|---|---|---|---|---|
| 1 | ConfRAG: Confidence-Guided RAG | arXiv:2506.07309 | 2025 | Confidence-triggered retrieval |
| 2 | Self-RAG (Asai et al.) | ICLR | 2024 | Reflection tokens, adaptive retrieval |
| 3 | CRAG (Corrective RAG) | arXiv:2401.15884 | 2024 | Self-correction on retrieval |
| 4 | Adaptive-RAG (Jeong et al.) | NAACL | 2024 | Complexity-based routing |
| 5 | SEAKR (Yao et al.) | ACL | 2025 | Internal-state uncertainty |
| 6 | KBM (Zhang et al.) | arXiv:2411.06207 | 2024 | Knowledge boundary model |
| 7 | Calibrated Retrieval-Budget (Dong et al.) | arXiv:2606.29959 | 2025 | 4-way decision framework |
| 8 | "To Retrieve or Not" | arXiv:2501.09292 | 2025 | Uncertainty detection metrics |
| 9 | LLM Uncertainty (NeurIPS) | NeurIPS | 2024 | Teaching LLMs what they don't know |
| 10 | AlignRAG | arXiv:2504.14858 | 2025 | Critique-driven alignment |
| 11 | Farmer.Chat (Singh et al.) | Microsoft Research | 2024 | Closest analog system |
| 12 | 60 Decibels Farmer.Chat Study | Digital Green | 2025 | Trust + adoption data |
| 13 | GAIA Project (IFPRI) | IFPRI/CGIAR | 2025 | RAG ethics toolkit for agri |
| 14 | PlantVillage Nuru Adoption | Frontiers in Agronomy | 2024 | Farmer trust + positioning |
| 15 | ICRISAT iSAT | ICRISAT/ISSCA | 2025 | Rule-based + AI hybrid engine |
| 16 | Fin AI Engine | Intercom/fin.ai | 2025 | Production RAG + validation gate |
| 17 | Glean Enterprise RAG | glean.com | 2025 | Agentic reasoning architecture |
| 18 | Perplexity Grounding Spectrum | DataStudios/ZipTie | 2025 | Citation transparency model |
| 19 | Attribute First, Then Generate | ACL | 2024 | Locally-attributable generation |
| 20 | Calibration Gate Framework | doronkatz.com | 2026 | Automation bias + launch criteria |
| 21 | LitmusEvals — Epistemic Safety | litmusevals.org | 2026 | "I don't know" instruction criticality |
| 22 | Medicolegal AI Accountability | PMC | 2024 | Reasonableness standard, automation bias |
| 23 | Calibration Gap (Steyvers) | UC Irvine | 2025 | User over-trust of LLMs |
| 24 | Trust in AI Farming Tools | Agronomy Journal | 2024 | Farmer trust categories |
| 25 | Microsoft Overreliance Framework | Microsoft AI Playbook | 2025 | Mitigation strategies |
| 26 | RAG in Production (Seven Failures) | IEEE/ACM | 2024 | Production failure modes |
| 27 | RAG Fusion Diminishing Returns | arXiv:2603.02153 | 2026 | Fusion not worth complexity |
| 28 | Query Rewriting — ElevenLabs | Tianpan.co | 2026 | Highest-ROI retrieval improvement |
| 29 | Kisan Call Centre Data Analytics | Scientific Reports | 2024 | Scale + seasonal patterns |
| 30 | RAGAS / RagChecker | Open source | 2024-2025 | Evaluation frameworks |

---

## 9. Open Research Questions for KrishokChat

1. **Bangla calibration:** Can a small calibration set (~100 Bangla agri queries) produce well-calibrated confidence estimates for Gemini API, or does calibration require model fine-tuning?

2. **Consistency sampling cost:** Does 3× generation for consistency checking add acceptable latency for a live demo? (Estimated: +1-2s with parallel API calls.)

3. **Optimal refusal rate:** What is the empirically optimal "I don't know" rate for farmer trust? Too high = unhelpful; too low = over-reliance. Farmer.Chat data suggests completeness drives trust.

4. **Voice-output trust calibration:** Does hearing uncertainty ("আমি নিশ্চিত নই") in voice have the same calibration effect as reading it? No literature found on voice-based AI uncertainty communication.

5. **Dialect robustness:** Can the retrieval system handle dialectal Bangla variation (Sylheti, Chittagong, Rangpur) that maps to the same agricultural concept? The 110-word dialect map is a start; retrieval-augmented matching needs evaluation.

---

_Literature review compiled by @scout. 30 sources across 6 research domains. All citations include venue, year, and specific finding. No AI-marker language. All quantitative claims carry source._

---

## Competitive Matrix

**Seed properties (from §7.1–§7.8, AGENTS.md §4):**
- **P1** Pre-retrieval Safety/Router: 6 classes (`safe_agri`, `banned_or_restricted_chemical`, `self_harm_or_poisoning_risk`, `off_topic`, `prompt_injection`, `low_confidence`), 4 of which are terminal-escalation categories.
- **P2** Calibrated 4-way confidence gate (FULLY_GROUNDED / PARTIALLY_GROUNDED / GENERAL_GUIDANCE / REFER_EXPERT) with refuse-and-redirect terminal (Krishi Call Center 16123).
- **P3** Bengali low-resource text regime, black-box API (no fine-tuning), precomputed BM25 index over 2,133 knowledge nodes.
- **P4** KB-only grounded generation, post-generation verifier + audit trail, faithfulness >90% target.

**Selection rule:** top-5 isolation by shared properties (≥2 of P1–P4), then venue tier (tier-1 preferred), then problem-class overlap, then ablation availability.

**Relaxations applied (criterion order 4→2→1):** Farmer.Chat — criterion 2 relaxed (no peer-reviewed tier-1 venue; Microsoft Research report + 60 Decibels field evaluation). ConfRAG — criterion 2 relaxed (arXiv:2506.07309 preprint). CRAG — criterion 4 holds via warned-actions analysis but its accuracy deltas are not tabulated in this file's sources; criterion 2 relaxed (arXiv:2401.15884 preprint). All five retain criteria 1 and 3.

**Excluded near-candidates:** SEAKR (Yao et al., ACL 2025) — requires white-box FFN activation access (§1.5), violates P3; shares 1 property. KBM (Zhang et al., arXiv:2411.06207) — trained soft-label classifier, no safety or agriculture thread; shares 1 property. Intercom Fin and Glean — production reports without citable ablations; retained as architectural analogues only (§1.7–§1.8). AlignRAG (arXiv:2504.14858) — plug-in critic, no terminal actions, no router; shares 1 property.

| System | Core Architecture | Hardware/Data Constraints | Convergence Speed / Scalability | Theoretical Vulnerabilities | Δ vs. Seed |
|---|---|---|---|---|---|
| **Farmer.Chat** (Singh et al., Microsoft Research 2024; 60 Decibels evaluation 2025, n=450 Kenya) | Production RAG chatbot; voice/text/image IO front end; retrieval over CGIAR open-access + CABI licensed corpora (GAIA project); Tomorrow.io weather feed; LLM backend undisclosed. No safety taxonomy, no confidence gate, no abstain terminal. Inductive bias: retrieval-first, source-grounded synthesis (§2.1, §3.1). | Cloud-hosted production; 830k+ users, 5M+ queries; evaluation = 60 Decibels survey n=450 (Kenya); multilingual content (EN/Swahili-tier set), no Bengali corpus reported. | NPS 63 (top 20% of 60 dB benchmarks); 82% "very trustworthy"; 83% "much more confident"; 61% apply advice; action-match 65% (complete + partial) (§3.1). No latency or routing-rate figures published. | Confidence drops 86%→48% when information is incomplete — the field-measured cost of absent abstention (§3.1); 71% of partial-comprehension users do not apply advice (§5.3); wrong advice erodes trust permanently (Agronomy Journal, §5.2); no audit trail, no terminal refuse path, no calibration object. | **[ADV]** — Seed's 4-way gate and refuse/16123 terminal instrument the 38-point completeness–confidence cliff that Farmer.Chat measures but does not control; Farmer.Chat leads only on deployed scale (5M queries). |
| **Self-RAG** (Asai et al., ICLR 2024) | Single fine-tuned LM emitting reflection tokens Retrieve/ISREL/ISSUP/ISUSE; segment-level beam search scores continuations on weighted token probabilities; hard/soft constraints (reject ISSUP=No); full $O(n^2 d)$ self-attention, Llama2 7B/13B base (§1.2). | Generator must be fine-tuned with critic supervision (multi-GPU training); evaluated on open-domain QA, reasoning, fact verification (§1.2); inference = beam search; no external index required. | 7B variant outperforms ChatGPT, Llama2-chat, and standard RAG on open-domain QA, reasoning, and fact verification (§1.2); retrieval frequency is tunable at test time via the Retrieve=Yes threshold. | ISSUP gates support, not safety — a supported-but-unsafe answer (e.g., overdosage) passes; fine-tuning requirement violates seed's P3 black-box constraint (§1.2); no terminal refusal classes; no audit trail. | **[PAR]** — Trained reflex critic gives Self-RAG higher critique fidelity; seed's prompt-emulated verifier plus pre-retrieval safety taxonomy gives wider decision coverage. Neither dominates across both axes. |
| **Adaptive-RAG** (Jeong et al., NAACL 2024) | Two-stage router: lightweight T5-class complexity classifier selects no-retrieval / single-step / multi-step iterative retrieval; full-attention generator (§1.4). | Small trained router + LLM; router inference cost negligible; training labels auto-generated from model predictions; evaluated on mixed-complexity QA sets (§1.4). | Outperforms always-RAG and no-retrieval baselines on mixed-complexity query distributions (§1.4); routing stops at 3 levels; no latency figures published. | Three hard routes with zero terminal classes — a banned-chemical query cannot stop before retrieval; routing confidence uncalibrated; no safety taxonomy; no verifier stage. | **[ADV]** — Seed's router is a 6-class superset of Adaptive-RAG's 3-level complexity routing, adding 4 terminal-escalation categories that complexity routing cannot express. |
| **ConfRAG** (arXiv:2506.07309, 2025) | ConfQA fine-tuning emits "I am unsure"; generation and RAG run in parallel as a race; RAG halts when the LLM emits a confident answer; calibrated uncertainty is the sole RAG trigger (§1.1). | ConfQA training on atomic factual statements; inference runs generation + retrieval concurrently (parallel execution); P50 latency reduced >600 ms; retrievals reduced 5–19% (§1.1). | Hallucination rate 20–40% (baseline) → <5% after ConfQA; >95% accuracy with a perfect RAG backend; matches always-RAG quality with 5–19% fewer retrievals (§1.1). | Binary trigger only — halting RAG falls back to closed-book generation, the ungrounded channel seed §7.4 forbids for dosage queries; mechanism requires fine-tuning (P3-incompatible); no pre-retrieval safety class. | **[PAR]** — ConfRAG's trained "unsure" emission is the stronger calibrator; seed's prompted consistency proxy (Jaccard: F1 0.593 at 1.46 searches vs 0.552 at 4.60 always-retrieve, §1.3) is weaker but terminates on REFER/16123 where ConfRAG continues generating. |
| **CRAG** (Yan et al., arXiv:2401.15884, 2024) | Lightweight T5-Large-class (770M) retrieval evaluator grades each document Correct/Incorrect/Ambiguous; actions: refine-and-use, discard + web-search fallback, combine internal + external knowledge (§6.5); full-attention RAG backbone. | One evaluator pass per retrieval (770M-param class); no agricultural or low-resource corpus reported; web-search fallback depends on live network access at inference time. | Corrective loop adds one lightweight classifier pass; accuracy deltas not tabulated in this file's sources (§6.5, pattern-level evidence only); fallback action adds unbounded latency and unlogged content. | Evaluator grades retrieval relevance, not safety; Incorrect → web-search fallback opens an ungrounded parametric channel (seed §6.8 failure mode #1); Ambiguous → combine mixes grounded and parametric content; no terminal refuse or escalation; no audit closure. | **[ADV]** — CRAG's Incorrect-action is web-search fallback, the channel seed's KB-only + REFER_EXPERT rule removes by construction; seed's verifier is prompt-based (weaker critic) but terminates on ungrounded critical claims. |
