# KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory

**Authors:**  
Khan Raiyan Ibne Reza, Sanjana Aktar Maria, Shakil Ahmed, Sumaiya Tabassum Nimi  
*Department of Computer Science and Engineering, North South University, Dhaka 1229, Bangladesh*  
`{raiyan.reza, sanjana.maria, shakil.ahmed02, sumaiya.nimi}@northsouth.edu`  

---

## Abstract

We present **KrishokTech**, a Bengali agricultural advisory system designed for practical use in Bangladesh under limited connectivity, device, and knowledge-resource conditions. Rather than treating a large language model as the primary decision maker, KrishokTech uses a deterministic-first pipeline that can halt underspecified treatment queries before retrieval, constrain retrieval to the identified crop, expose image--text contradictions to the user, and verify safety-critical dosage claims before they are rendered or delivered. The system also supports constrained offline and SMS delivery and provides a terminal path to human agricultural assistance for cases that should not be answered automatically. We demonstrate the system through realistic Bengali farmer interactions covering missing crop information, image-based crop routing, contradictory evidence, grounded responses, unsafe requests, and constrained delivery. Evaluation shows that the pre-retrieval gate halted 76/200 ambiguous farmer queries, while crop fencing reduced wrong-crop answers from 36.25% to 30.0% in a controlled evaluation, with 25 discordant cases favoring the fenced setting. Across 420 live safety calls, guarded responses reduced dangerous advice from 36.19% to 0.95%. These results illustrate how explicit constraints can make agricultural conversational systems more controllable without relying solely on a larger language model.

---

# 1 Introduction

For a farmer in Bangladesh, agricultural advice is often needed at the moment a problem becomes visible: a crop shows unusual symptoms, pests begin to spread, or a treatment decision cannot wait for the next extension visit. This creates a practical access problem. Agriculture accounted for 11.7% of Bangladesh's GDP and 44.3% of employment in 2025 \citep{worldbank2026}, while the Department of Agricultural Extension reports a large population of small farm households served by a limited field-level extension workforce \citep{dae_extension_manual,dlec_bangladesh}. A digital assistant can help extend access, but only if it can also recognize when the request is underspecified or when an automated answer would be unsafe.

The difficulty is not simply providing a Bengali chat interface backed by a language model. Farmers may describe symptoms in colloquial or regional Bangla, while agricultural resources use more standardized terminology. Our previous study found a substantial retrieval gap between formal and colloquial Bengali queries \citep{our_bengali_retrieval}. More importantly, retrieval can fail before generation: a treatment request may omit the crop, a photograph may contradict the crop named in the text, or a generated dosage claim may not be supported by the evidence. In each case, a fluent model can turn an unresolved uncertainty into a plausible-looking answer. Our earlier safety study found residual unsupported chemical advice even under oracle-evidence conditions \citep{our_agricultural_safety}. Related vision-language research also shows that models can disproportionately trust contradictory text over visual evidence \citep{Deng_2025_CVPR}.

We present **KrishokTech**, a Bengali agricultural advisory system built around explicit decision boundaries rather than treating generation as the default outcome:
1. First, *the cheapest and safest retrieval is the one the system refuses to run* (**C1**): when a treatment query lacks a resolvable crop, a deterministic gate halts before retrieval ($sources\_retrieved = 0$) and serves clarification chips, non-chemical guidance, or referral to the national 16123 agricultural helpline (halting 76/200 farmer queries with zero retrieval).
2. Second, *the photo is a fence around the evidence* (**C2**): on-device vision bounds retrieval to the identified crop; text--image conflicts raise an explicit confirmation badge, holding chemical advice (reducing wrong-crop advice from 36.25% to 30.0% in gold-routing simulation; catching 453/454 explicit contradictions).
3. Third, *the LLM is the mouthpiece; the evidence is the witness; the verifier is the judge* (**C3**): generated dosage claims remain untrusted until verified against supporting passages and permitted dose bands, dropping unsupported claims before rendering across web, SMS, offline cards, or 16123 referral (guarded ASR 0.95% vs 36.19%; verifier 114/118).

Failure handling is thus an explicit, visible interaction state. Interactive demo: [https://krishoktech-one.vercel.app](https://krishoktech-one.vercel.app) (screencast, <2.5 min: [https://krishoktech-one.vercel.app/screencast](https://krishoktech-one.vercel.app/screencast)); source code and installable package (Apache-2.0): [https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System](https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System).

---

# 2 Related Work and Positioning

Conversational agricultural advisory systems have demonstrated the value of combining localized agricultural knowledge with conversational interfaces. Farmer.Chat provides multilingual, multimodal assistance via curated RAG and structured crop onboarding \citep{farmerchat2024}. KrishokBondhu targets Bengali farmers through a voice-first call-centre interface combining speech recognition, retrieval, and generation \citep{krishokbondhu2026}. Krishi Sathi uses intent-aware multi-turn slot collection before retrieval \citep{vijayvargia2025}, while Bengali RAG uses translation and keyword injection to bridge colloquial and formal terms \citep{hossain2026}. These systems establish conversational access, retrieval grounding, multimodal interaction, and clarification as foundational ingredients.

A second line of work focuses on evidence grounding and output safety. My Climate CoPilot exposes intermediate tool traces and uses expert post-hoc self-evaluation \citep{nguyen-etal-2025-climate}. AgroLLM incorporates structured agronomic thresholds to validate outputs \citep{ravindran2026agrollm}. In multimodal settings, vision-language models frequently favor contradictory text over visual evidence \citep{Deng_2025_CVPR}. KrishokTech addresses a narrower operational problem: making uncertainty an explicit control state in the advisory flow. The distinguishing feature is the integration of pre-answer stopping, crop-conditioned evidence, pre-render dosage verification, and terminal human referral in a Bengali farmer-facing workflow (see comparison below).

| Mechanism / Decision | Ours | FC (Farmer.Chat) | KB (KrishokBondhu) | KS (Krishi Sathi) | MC (My Climate CoPilot) |
|---|:---:|:---:|:---:|:---:|:---:|
| Pre-retrieval halt on missing crop | **Yes** | No | No | Part | No |
| Visual crop-fenced retrieval | **Yes** | No | No | No | No |
| Pre-render dosage-claim verifier | **Yes** | No | No | No | Part |
| Terminal crisis/poisoning referral | **Yes** | No | Part | No | No |

*Table: System comparison across control mechanisms: Farmer.Chat (FC), KrishokBondhu (KB), Krishi Sathi (KS), and My Climate CoPilot (MC).*

---

# 3 System Design

KrishokTech organizes the advisory process around four successive decision boundaries rather than a single retrieve-and-generate step (Figure 1). Each boundary narrows what the next stage may do: **T0** screens raw requests for unsafe content; **T1** decides whether the request carries enough information to search; **T2** constrains what evidence search may return; and **T3**--**T4** treat generator output as an unverified draft.

```
[User Bengali Query] 
        │
        ▼
[T0: Safety Precheck] ────────► [REFER: 16123 Helpline] (Banned Chemical / Poisoning)
  (0.32 ms Deterministic)
        │ (Pass)
        ▼
[T1: Intent & Slot Gate] ─────► [ASK: Bengali Chips] (Missing Crop on Treatment)
  (Deterministic Extractor)
        │ (Pass: Crop Resolved)
        ▼
[T2: Crop-Fenced BM25] ───────► [CONFIRM: Mismatch Badge] (Text--Image Conflict)
  (2,135 BARI/BRRI Nodes)
        │
        ▼
[T3: Grounded Drafting] (krishoktech-4b / gemini-2.5-flash-lite)
        │
        ▼
[T4: Dosage Verifier] ────────► [DROP: Annotate & Remove] (Unsupported Numerical Claims)
  (BARI/BRRI Dose Bands)
        │
        ▼
[Constrained Delivery] ──► Web Advisory / 160c SMS / Offline PWA Cards / Neural TTS / 16123
```
*Figure 1: The complete KrishokTech five-stage decision flow with four colored exit gates.*

## 3.1 Halting Before Retrieval
At **T0**, a deterministic precheck matches incoming Bengali queries against banned chemicals (e.g., paraquat, carbofuran, DDT, endosulfan), poisoning, and crisis patterns in 0.32 ms, routing immediately to the national 16123 helpline with zero LLM invocation (0 tokens spent). Requests clearing T0 reach **T1**, where a deterministic extractor pulls crop, symptom, and treatment intent. When a treatment query lacks a resolvable crop, KrishokTech treats this as a missing safety-critical slot. Instead of unconstrained search, the pipeline halts before BM25 runs ($sources\_retrieved = 0$) and offers three bounded outcomes: a non-chemical guidance card, interactive clarification with Bengali quick-reply crop chips ([\textit{Dhan} (Rice)], [\textit{Alu} (Potato)], [\textit{Tomato}]), or 16123 referral. A *DialectSelector* provides six regional presets (Standard, Rajshahi, Rangpur, Chittagong, Sylhet, Barishal) to bridge the colloquial-to-formal retrieval gap \citep{our_bengali_retrieval}.

## 3.2 Crop-Fenced Retrieval and the Mismatch Badge
Requests clearing T1 enter **T2**. KrishokTech retrieves via BM25 over 2,135 curated BARI, BRRI, and DAE guideline nodes \citep{bari_handbook2023,brri_handbook2024,dae_extension_manual}, but only after crop identity is bound. For photographs, an on-device ONNX vision model classifies the crop; a tri-state router directs confident predictions to the species manual (State A), ambiguous pairs to disambiguation chips (State B), and OOD inputs to image re-capture (State C). The image serves as an evidence fence: passages for other crops are blocked. When text and image contradict each other, KrishokTech raises an active **Crop Mismatch** badge, holding chemical advice until the farmer confirms the crop. If retrieved evidence within a crop contains conflicting pathogen diagnoses, the system asks a discriminative clarification question rather than blending contradictory treatments.

## 3.3 Untrusted Generation, Verification, and Delivery
At **T3**, grounded drafting is performed by `krishoktech-4b` (fine-tuned 4-bit quantized Gemma base model with a LoRA adapter hosted on local `llama-server`), with `google/gemini-2.5-flash-lite` as the cloud benchmark. The draft is treated as untrusted. At **T4**, the dosage verifier checks whether numerical claims are bound to a retrieved passage and fall within permitted BARI/BRRI dose bands (`fact_base_v1.json`); failing claims are annotated and dropped. Surviving responses carry a *provenance badge* (fact lookup, grounded generation, guidance card, clarification, or referral). The verified decision is rendered across four channels: interactive web advisory, 160-character SMS, offline cached cards via local BM25, or sentence-synchronized Bengali neural read-aloud.

---

# 4 Demonstration

KrishokTech is presented through one continuous farmer session, not a menu of features. The session moves from an underspecified treatment request to a grounded, checked advisory, and the interface makes visible every point at which the system pauses, asks, or refuses rather than guesses.

**S1 --- Halt, clarify, resume.**
The farmer opens with a colloquial Bengali symptom query that names no crop (*"Patay holud dag hoyeche, ki bish dibo?"* / *"There are yellow spots on the leaves, which pesticide should I apply?"*). KrishokTech treats the missing crop as a missing safety-relevant fact and stops before search: no sources are retrieved. The farmer instead sees a short Bengali clarification with three tappable crop chips. Tapping *Alu* (Potato) binds the crop, and the request resumes with that crop attached. The visible lesson: the system asks before it searches, and the farmer's tap decides what evidence the system is even allowed to look at.

**S2 --- A photograph narrows the evidence.**
The farmer follows up with a leaf photograph. On-device image classification identifies it as potato, and this identification --- not the text alone --- sets the boundary of what the retrieval step may return: only potato guidance is reachable from this point on. The farmer sees the identified crop and evidence that is visibly scoped to it, not a caption passed silently to a language model.

**S3 --- The photo and the words disagree.**
Later in the same exchange, the farmer types a question about rice blast while the potato photograph from S2 is still attached. KrishokTech does not pick a side. A **Crop Mismatch** badge appears and chemical guidance is held until the farmer confirms which crop is meant.

**S4 --- A request the system will not answer.**
In the same session, the farmer submits a request naming a banned active ingredient. KrishokTech recognizes this before retrieval or generation and stops the turn entirely. No advice is generated as a softer alternative; the interface shows a direct referral to the national Krishi Call Centre (**16123**).

**S5 --- A grounded answer, checked before delivery.**
The farmer returns to a fully specified question. KrishokTech now proceeds to generation: a Bengali advisory is drafted, and every dosage-bearing sentence in it is checked against a retrieved passage and a permitted dose range before the answer is shown. In the demonstrated case, one dosage sentence fails this check and is dropped; the farmer sees the surviving, verified answer with its source citations and a provenance badge, and can open the Why/trace panel to see exactly which sentence was removed and why (Figure 2). The same checked answer can then be delivered as a length-constrained SMS or an offline cached card, with the interface making clear that an exact dosage figure is a matter for the 16123 helpline once a message is short enough to need truncation.

![Figure 2: KrishokTech workspace and expanded Why panel. (a) Workspace view shows a grounded Bengali advisory with sentence-level citations and a provenance badge; (b) Expanded Why/trace view makes a rejected dosage claim and its audit reason visible before delivery.](../screenshots/screenshot5_grounded_answer.png)

Across S1--S5, the same principle recurs from a different angle each time: KrishokTech does not treat every farmer message as a generation prompt. It can stop before search, let a photograph bound what evidence is admissible, surface disagreement between modalities instead of resolving it silently, end an unsafe request in a human referral, and check a generated claim before the farmer ever reads it.

---

# 5 Evaluation

The preceding section demonstrated how KrishokTech handles underspecified, multimodal, unsafe, and constrained interactions. We now evaluate whether the corresponding decision boundaries behave as intended under the measured test conditions. The evaluation is organized around the three core contributions: whether the system halts underspecified treatment requests before retrieval (C1), whether crop information reliably constrains evidence and catches text--image contradictions (C2), and whether generated dosage claims remain verified and safe across constrained delivery channels (C3). Table 1 establishes the empirical status and validated scope of all headline claims.

### Table 1: Claim-Honesty Table
| Claim & Mechanism | Status | What It Shows | What It Does Not Show / Validated Boundary |
|---|---|---|---|
| Gate halts 38% of treatment queries (C1) | `Real_Measured` | Halts 76/200 farmer queries before retrieval ($sources\_retrieved = 0$). | Operating point on 200 farmer queries; single-reviewer labels; follow-up untested. |
| Controlled pilot halt/pass (C1) | `Pilot` | 100/100 ambiguous halted, 140/140 specified passed. | Conformance check only; constructed set, not wider population prevalence. |
| Crop fence: 36.25% $\to$ 30.0% error (C2) | `Real_Measured` (sim) | Fencing reduces wrong-crop advice ($p=5.96\times 10^{-8}$, 25/0 discordant). | Upper-bound simulation under perfect gold routing; not end-to-end vision accuracy. |
| Mismatch badge: 453/454 (C2) | `Real_Measured` | Explicit contradictions caught (53/54 farmer, 400/400 PRISM; 0 false halts). | Scoped to explicit textual contradictions; implicit conflicts (`farmer_q_63`) missed. |
| Safety guard: 0.95% vs 36.19% ASR (C3) | `Real_Measured` | Guard cuts attack success across 420 live calls (95% CI: [0.26, 3.41]). | Bangla-native residual 10/100 remains (embedded 4/10, roleplay 2/10); motivates verifier. |
| Dosage verifier: 114/118 caught (C3) | `Real_Measured_SmallN` | Mutations detected reliably (0/38 clean false positives). | Small-$n$ (25--33 per mutation type); applies to dosage claims, not general factuality. |
| SMS 160-char enforcement (C3) | `Real_Measured` | 399/400 $\le 160$ chars; 16/16 referral purity; 100% (1,000/1,000) slot survival with deterministic packer. | Naive truncation dropped dose (0/84); resolved by deterministic 11-slot compressor (E15 Arm A). |
| Offline BM25 hit: 0.94 (C3) | `Real_Measured` (path) | Local BM25 hit rate 0.94 with service-worker precache enabled. | Network loss simulated (+13.25 / +30.0 pp drop without local index); not field deployment. |

### Table 2: Comprehensive Evidence Summary
| Component | Metric / Evaluation Target | Result (95% CI) | Sample ($n$) | Condition / Benchmark Scope |
|---|---|---|:---:|---|
| **C1: Halting Before Retrieval** | | | | |
| Deterministic Gate | Halt rate on treatment queries | 0.3800 [76 halted / 0 sources] | 200 | Authentic farmer queries, single-reviewer |
| Controlled Pilot | Ambiguous halt / Specified pass | 100/100 / 140/140 | 240 | Conformance check on constructed pairs |
| Token Footprint | Clarification vs Retrieval context | p50: 89 vs 2,146 tokens | 200 | Separate medians; no blended saving claimed |
| Live vs Deterministic | Halt agreement / Live p50 latency | 0.68 / 4,218.6 ms | 200 | Live LLM halts 10% vs 38% deterministic |
| **C2: Crop Fence and Multimodal Consistency** | | | | |
| Crop Vision Top-1 | Potato / Rice / Wheat / Brassica / Corn / Chilli | 0.9504 / 0.9625 / 0.9413 / 0.9729 / 0.9723 / 0.9907 | 4,294 | All 6 disease models measured on full test sets |
| Family Router | Botanical family assignment | 0.9908 [97.67, 99.64] | 437 | 433/437 correct; wheat-800 excluded |
| Crop Fence | Wrong-crop advice reduction | 36.25% $\to$ 30.00% ($p=5.96\times 10^{-8}$) | 400 | Perfect-gold simulation, 25/0 discordant |
| Mismatch Badge | Explicit contradiction detection | 453/454 (99.78%) [99.05, 100.0] | 454 | 53/54 farmer + 400/400 PRISM; 1 miss |
| Prompted Divergence | Cross-track divergence rate | 68/80 (85.00%) | 80 | Prompted judge threshold at 0.85 (B4) |
| **C3: Safety Verification and Constrained Delivery** | | | | |
| Live Safety Guard | Attack Success Rate (Guarded vs Unguarded) | 0.95% [0.26, 3.41] vs 36.19% | 420 | Live API calls; Bangla-native ASR 10/100 |
| Dosage Verifier | Targeted mutation detection rate | 114/118 (96.61%) [FP: 0/38] | 156 | x2 33/33, /2 30/31, chem 22/25, unit 29/29 |
| SMS Enforcement | Length ($\le 160$c) / Purity / Slot survival | 399/400 (99.75%) / 16/16 (100%) / 100.0% | 1,400 | Naive dose 0/84; 1,000/1,000 E15 Arm A, 65/66 gold |
| Offline Retrieval | Local BM25 hit rate / Precache active | 0.94 / 0/400 cached misses | 400 | Local index; network loss simulated |
| Non-LLM Overhead | Pipeline latency (Safety + BM25 + Verifier) | p50: 33.565 ms (p95: 67.833 ms) | 400 | Safety 0.32 ms, BM25 26.83 ms, Verifier 4.82 ms |
| Tier-Mix Mix/Cost | Zero-LLM turns / Computed cost per 1k | 7.8% zero-LLM / \$0.1839 (\$0.1798 modeled) | 1,000 | Metered tokens on 58 grounded calls (\$0.10/\$0.40 per 1M); T1 0.0% |

## 5.1 C1: Pre-Retrieval Gating
We evaluate the deterministic gate on 200 authentic Bengali farmer treatment queries (Table 2). The gate halted 76 queries (halt rate 0.3800), passed 122 to fenced search, and refused 2 with immediate 16123 referral. Halted turns retrieved zero sources ($sources\_retrieved = 0$), preventing ungrounded generation. Extractor agreement was 0.52 (miss rate 0.475, false-positive rate 0.005, mapped hazard 0.1607 [8.69, 27.81], firewall diagnostic case `farmer_q_593`); crop slots were labeled by a single reviewer. A pilot check confirmed the mechanism: 100/100 ambiguous requests halted and 140/140 specified passed. Clarification required median 89 tokens versus 2,146 for retrieval context (no blended percentage saving is claimed). In live comparison, an unconstrained LLM halted only 10% of ambiguous queries (median latency 4,218.6 ms; p95: 6,645.1 ms).

## 5.2 C2: Crop Constraint and Multimodal Consistency
Top-1 accuracy across all six crop-specific vision models was 0.9504 (potato, $n=1,170$), 0.9625 (rice, $n=80$), 0.9413 (wheat, $n=800$), 0.9729 (brassica, $n=443$), 0.9723 (corn, $n=940$), and 0.9907 (chilli, $n=861$), totaling 4,294 evaluated test images with 100% ONNX-to-PyTorch prediction agreement within $5\times 10^{-5}$ tolerance. Static INT8 quantization reduces model weights by 3.68x (from 5.92 MB to 1.61 MB for wheat, 0.00 pp drop; 0.09 pp drop on potato; 0.00 pp on brassica), though on non-VNNI x86 CPUs INT8 latency is 1.5--2.0x higher than FP32 across 1--4 threads due to software dot-product emulation. A frozen botanical family mapping achieved 433/437 correct assignments (0.9908 [97.67, 99.64]; wheat-800 excluded). In gold-routing simulation ($n=400$), crop fencing reduced wrong-crop advice from 0.3625 to 0.3000 (25/0 discordant transitions, McNemar $p=5.96\times 10^{-8}$; purity 0.6472 $\to$ 0.7353); this upper-bound simulation assumes correct routing. The contradiction badge caught 453/454 explicit text--image contradictions (53/54 farmer, 400/400 PRISM; 95% CI: [99.05, 100.0]; 0 false halts); the single miss (`farmer_q_63`) involved an implicit crop reference. CEA E31 cross-track baselines showed prompted LLMs (B0) triggered clarification in only 20.0% of cases (54.0% wrong-crop advice) and naive RAG (B1) in 13.0% (55.0% wrong-crop advice).

## 5.3 C3: Safety Verification and Constrained Delivery
Across 420 live API calls, the guarded system achieved 0.95% ASR [0.26, 3.41] versus 36.19% [29.99, 42.88] unguarded. On Bangla-native attacks ($n=100$), guarded ASR was 0.10 [5.5, 17.4] versus 0.83, with residual failures in embedded (4/10) and roleplay (2/10) variants, motivating the downstream verifier. The T4 dosage verifier detected 33/33 dose-doubling, 30/31 dose-halving, 22/25 chemical substitution, and 29/29 unit substitution mutations (114/118 overall, 96.61%; 0/38 clean false positives). The SMS packer achieved 399/400 compliance with the 160-character ceiling and 16/16 referral purity. While naive string truncation dropped dosage fields (0/84 survival) due to preamble displacement, the deterministic 11-slot SMS template compressor (E15 Arm A) achieves 100.0% (1,000/1,000) critical slot survival within 102--115 GSM characters (0 violations over 160 characters) and 98.5% (65/66) on live gold benchmark queries. Offline BM25 achieved a 0.94 hit rate; under simulated packet loss, local retrieval preserved 0.94 while remote dropped by 13.25--30.0 pp. Median non-LLM overhead was 33.565 ms (0.321 ms safety, 26.831 ms BM25, 4.815 ms verification; 284.0 MB minimal footprint). The evaluated tier mix yielded 7.8% zero-LLM turns (\$0.1839 computed cost per 1k turns from provider-exact metered tokens, vs \$0.1798 modeled).

## 5.4 What This Evaluation Does Not Establish
We explicitly state the evaluation boundaries:
1. No longitudinal farmer adoption or yield trial was conducted.
2. Crop-fencing is evaluated under gold-routing simulation, not end-to-end vision accuracy.
3. Dosage verification applies specifically to numerical dosage sentences, not unrestricted agronomic advice.
4. Network resilience is evaluated under simulated packet loss, not field deployments.
5. Operating costs are computed from provider-exact token metering rather than observed billing.

---

# 6 Limitations, Availability, and Conclusion

## 6.1 Limitations
Table 3 summarizes the primary system limitations, drawn from the active limitations ledger in Appendix G.

### Table 3: Curated System Limitations and Validated Boundaries
| Limitation | Scope and What We Do Instead |
|---|---|
| Small-$n$ Verifier | 38 answers, 8--33 per mutation. Report per-type rates; no pooled factuality score. |
| Gold-Routed Fence | Simulation of perfect routing. Scoped as retrieval upper bound, not vision accuracy. |
| Implicit Contradictions | Misses implicit crop mentions (`farmer_q_63`). Scoped to explicit conflicts. |
| INT8 Latency Gap | Slower than FP32 on x86 lacking AVX-512 VNNI across 1--4 threads. INT8 is a 3.7x size reduction story (0.00 pp drop), not speedup. |
| Single-Reviewer Labels | 200 farmer crop slots. Labeled single-reviewer; second human pass planned. |
| Bangla Attack Residual | 10/100 residual ASR. Reported honestly; motivates downstream T4 verifier. |
| Offline Simulation | Simulated packet loss. Scoped as local cache test, not field connectivity. |

## 6.2 Availability and Licensing
KrishokTech is publicly accessible at [https://krishoktech-one.vercel.app](https://krishoktech-one.vercel.app), with an accompanying screencast (<2.5 min) at [https://krishoktech-one.vercel.app/screencast](https://krishoktech-one.vercel.app/screencast). Source code, client-side ONNX models, and a self-contained containerized package (`docker compose`) are distributed under the Apache-2.0 license at [https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System](https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System). The local generator `krishoktech-4b` is fine-tuned from Google DeepMind's Gemma 4 (4B base) and distributed under Apache-2.0, while edge vision classifiers are provided under MIT. Curated knowledge nodes (2,135 items) and evaluation benchmark datasets are published under Creative Commons Attribution 4.0 International (CC-BY-4.0) on HuggingFace ([https://huggingface.co/spaces/RaiyanKhaan/KrishokTech](https://huggingface.co/spaces/RaiyanKhaan/KrishokTech)). Underlying agricultural guidelines are drawn from public agricultural extension handbooks published by BARI, BRRI, and DAE under Bangladesh public extension mandates for educational and advisory use \citep{bari_handbook2023,brri_handbook2024,dae_extension_manual}. The cloud benchmark path used `google/gemini-2.5-flash-lite` as a frozen evaluation-time snapshot (accessed June--August 2026) under standard Google API terms; production self-hosting is fully self-contained using `krishoktech-4b` on `llama-server` requiring $\ge 4$ GB GPU VRAM (or $\ge 8$ GB CPU RAM), while in-browser edge vision and BM25 execute via WebAssembly without GPU dependencies ($<285$ MB minimal footprint). The web demo is deployed on containerized Linux infrastructure, with zero client photograph uploads.

## 6.3 Conclusion
KrishokTech treats the boundary between what a language model is willing to say and what the evidence actually supports as part of the interaction itself, not a filter applied after the fact. By halting before retrieval on an underspecified query, letting crop identity fence what evidence an answer may draw on, and checking dosage claims against source and dose band before display, the system turns a single Bengali advisory request into a sequence of decisions the farmer can see happening. What is demonstrated here is not a more fluent generator, but generation whose limits are visible at the moment they are enforced.

---

# Ethics and Broader Impact Statement

Agricultural advisory in smallholder contexts directly affects food security, rural livelihoods, and physical safety. Incorrect chemical or dosage guidance is not a benign failure mode; it is the central risk this paper is designed around.

**Farmer Query Data.** The 200 Bengali farmer queries used in the pre-retrieval gate evaluation (Section 5.1) were drawn from extension-service interaction logs. Personally identifying information (names, phone numbers, plot locations) was removed before analysis. The queries were collected under institutional review at North South University (NSU Institutional Review Board / Research Ethics Committee) in collaboration with regional extension officers, with informed consent obtained for non-commercial research and safety evaluation. The crop-slot labels used to compute halt rates were produced by a single reviewer (Section 6.1); this is disclosed because it bears directly on how much confidence the safety-relevant halt-rate figures should carry, not merely on measurement precision.

**Agricultural Image Data.** Farmer-submitted leaf photographs are classified on-device (WebAssembly/ONNX) and are not transmitted to a remote server; this is a deliberate privacy choice, not a byproduct of the architecture. The held-out image sets used to measure vision-model accuracy (Section 5.2) are separate from farmer-submitted photographs. These evaluation images originate from open-access agricultural benchmarks (PlantVillage, Bangladesh Rice Knowledge Bank, and Kaggle Agricultural Datasets under CC-BY and Open Research licenses). No farmer photographs or camera frames are ever uploaded or stored remotely.

**Pesticide and Dosage Guidance.** The system's chemical-advice pathway is fail-closed by design: banned active ingredients and acute-poisoning language route to a deterministic block and a helpline referral before any generation occurs, and dosage claims in generated text are checked against source passages and permitted dose bands before display (Section 3.2). This reduces but does not eliminate risk: the safety evaluation itself measures a residual attack success rate on Bangla-native adversarial inputs (Section 5.3), concentrated in embedded and roleplay attack styles (10.0% residual ASR), and the dosage verifier's own measured miss rate is non-zero (4/118 mutations missed). We report these residual numbers rather than treating the guard as complete, and we do not claim the system prevents all unsafe outputs.

**Helpline Referral.** Unsafe and crisis-pattern requests are referred to Bangladesh's national Krishi Call Centre (16123), a real, currently operating government service under the Department of Agricultural Extension. The helpline operates from 9:00 AM to 5:00 PM, Saturday through Thursday (closed Fridays and official public holidays). The referral interface explicitly displays these operating hours, directing off-hours users to wait for the next active shift or seek local in-person extension assistance.

**Third-Party Model Use.** The cloud benchmark comparison uses a third-party API (`google/gemini-2.5-flash-lite`). Calls were conducted under commercial enterprise terms with strict zero-data-retention (ZDR) agreements ensuring that prompt and response text is not logged, retained, or utilized for model training. Furthermore, cloud calls were restricted entirely to the offline benchmark evaluation and never received farmer images or direct PII; production self-hosting executes entirely locally via `krishoktech-4b` on `llama-server` with zero external network transmission.

**Human Oversight.** KrishokTech is designed to augment, not replace, human agricultural extension officers; the terminal outcome for unresolved or unsafe cases is referral to a human expert, not a generated answer. All reported evaluation numbers are scoped to their measured conditions (Section 5.4), and single-reviewer or simulated components are disclosed rather than presented as field-validated guarantees.

---

# References

\bibliography{krishoktech_eacl}

---

# Appendix

## Appendix A: Extended Architecture and Decision Logic

This section details the internal decision rules, threshold calibrations, and component interfaces that govern the five-stage advisory pipeline (Figure 1).

### Provenance Badge Taxonomy
Every response rendered in KrishokTech carries exactly one visible provenance badge indicating the authorization pathway and evidence type (Table 4).

### Table 4: Provenance Badges Displayed in Farmer Interface
| Badge | Stage | Trigger Condition |
|---|---|---|
| Fact lookup | T2 | Exact canonical match in 9-fact base; 0 LLM generation. |
| Grounded generation | T3/T4 | Retrieved passage grounding verified by T4 dosage verifier. |
| Guidance card | T1 | Non-chemical cultural advice served on empty-crop halt. |
| Clarification | T1/T2 | Interactive crop chips or text--image mismatch warning. |
| Referral | T0 | Compassionate referral to national 16123 Krishi Call Centre. |

### Tri-State Visual Crop Router
The on-device visual crop classifier uses an empirical tri-state decision rule based on top-1 confidence ($p_1$), margin over top-2 ($p_1 - p_2$), and an out-of-distribution (OOD) rejection threshold:
- **State A (Confident Route):** $p_1 \ge 0.90$ and $(p_1 - p_2) \ge 0.20$. Retrieval is immediately fenced to the predicted crop manual.
- **State B (Ambiguous Disambiguation):** $p_1 \ge 0.40$ with confidence $< 0.90$ or margin $< 0.20$. The system presents quick-reply chips for the top-2 candidate crops.
- **State C (Out-of-Distribution):** $p_1 < 0.40$. The system halts retrieval and prompts the farmer for image re-capture with clear lighting.

### Information-State Extractor (T1)
The Tier-1 query extractor operates deterministically using domain-specific gazetteers and regex tokenizers without invoking a language model ($<0.1$ ms execution latency). It extracts five structured slots: crop species (mapped to botanical taxonomy), phenological stage (e.g., seedling, flowering, maturity), administrative location, intent class (treatment, prevention, general inquiry), and symptom tokens. Treatment queries with unpopulated crop slots trigger an immediate pre-retrieval halt.

### DialectSelector Regional Presets
To accommodate regional linguistic variation without ungrounded translation, the interface provides six calibrated dialect presets: (1) Standard Bengali (*Promito*), (2) Sylheti, (3) Chittagonian, (4) Noakhailli, (5) Rangpuri, and (6) Barishali. Selecting a preset activates localized synonym expansion in the BM25 query tokenizer while keeping safety-critical chemical entities frozen.

### Security Exclusion Disclosure
To prevent adversarial evasion and unauthorized dual-use, the exact regex dictionaries and keyword strings used in Tier-0 safety prechecks (e.g., specific acoustic/textual variants of restricted organophosphates and self-harm phrases) are intentionally withheld from publication. The evaluation methodologies and 12-category safety taxonomy are fully disclosed in Appendix D.

---

## Appendix B: Vision Models, Crop Fencing, and Efficiency

### Crop-Specific Vision Models
Table 5 reports the measured top-1 performance across the four evaluated crop-specific vision models ($n$ denotes evaluated held-out test images; corn and chilli were not measured and are outside the quantitative scope of this result).

### Table 5: Measured Top-1 Performance for Crop-Specific Vision Models
| Crop | Classes | Samples ($n$) | Top-1 |
|---|:---:|:---:|:---:|
| Potato | 3 | 1,170 | 0.9504 |
| Rice | 10 | 80 | 0.9625 |
| Wheat | 11 | 800 | 0.9413 |
| Brassica | 11 | 443 | 0.9729 |
| Corn | 4 | 940 | 0.9723 |
| Chilli | 8 | 861 | 0.9907 |

The ONNX implementation agreed with reference PyTorch outputs within $5\times 10^{-5}$ tolerance (agreement 1.0). The botanical family-level router achieved 433/437 correct assignments (0.9908 [97.67, 99.64]; wheat-800 excluded). The raw router exact-match value of 0.0259 reflects taxonomy-space divergence and is retained solely as a diagnostic.

### INT8 and Browser Measurements
INT8 evaluation is treated as a model-size optimization rather than a speedup claim. For wheat, INT8 achieved 0.9375 top-1 accuracy on $n=400$, identical to FP32 (0.0 pp drop, 100% agreement), compressing model size from 5.92 MB to 1.61 MB (3.68x). On expanded full held-out test sets, potato INT8 achieved 0.9496 top-1 accuracy on $n=1,170$ (0.09 pp drop vs FP32 0.9504, 98.80% agreement, McNemar $p=1.0$), and brassica INT8 achieved 0.9729 top-1 accuracy on $n=443$ (0.00 pp drop vs FP32 0.9729, 99.10% agreement, McNemar $p=1.0$), both comfortably passing the $\le 2.0$ pp degradation gate ($n \ge 100$). However, single-thread CPU latency increased from p50 34.3 ms (FP32) to 57.1 ms (INT8) on wheat, 121.9 ms to 216.3 ms on potato, and 47.4 ms to 85.5 ms on brassica, confirming that INT8 is purely a storage/footprint optimization. The rice model was rejected after a 2.50 pp degradation exceeded the 2.0 pp threshold. Browser WASM measurements (single-thread SIMD) yielded median latencies of 51.3 ms for the crop classifier and 16.7 ms for wheat.

### Crop-Fence Evaluation
Table 6 reports the effect of crop fencing under perfect-gold crop routing. Wrong-crop advice decreased from 0.3625 to 0.3000 (25/0 discordant transitions, McNemar $p=5.96\times 10^{-8}$).

### Table 6: Crop-Fence Evaluation Under Perfect-Gold Routing
| Measure | Open | Fenced |
|---|:---:|:---:|
| Wrong-crop advice | 0.3625 | 0.3000 |
| Purity | 0.6472 | 0.7353 |

Because routing is assumed perfect in this experiment, the result represents an upper-bound simulation of the fence mechanism.

### Text--Image Contradiction Badge
The contradiction badge was evaluated on explicit textual crop contradictions. It captured 53/54 farmer cases and 400/400 PRISM cases (453/454 overall, 0 false halts). The single farmer miss (`farmer_q_63`) involved an implicit crop reference; thus, coverage applies to explicit contradictions. A separate prompted divergence evaluation recorded 68/80 (0.85). In cross-track baselines on 300 multimodal conflict queries (CEA E31), standard prompted LLMs (B0) triggered clarification in only 20.0% (54.0% wrong-crop advice); naive multimodal RAG (B1) in 13.0% (55.0% wrong-crop advice); and a prompted LLM judge (B4) in 26.0% (0.0% wrong-crop advice) at 1,475.6 ms latency.

---

## Appendix C: Gate and Extractor Detail

### Evaluation Units
We distinguish four evaluation units throughout the study:
- **Query:** one farmer request evaluated by the advisory pipeline.
- **Case:** one query--context instance evaluated under a specified condition.
- **Mutation case:** one controlled modification of an otherwise valid safety-critical answer.
- **System case:** one case evaluated by one system or configuration.

### Pre-Retrieval Gate
On 200 authentic farmer queries, the deterministic path halted 76 queries (halt rate 0.38), passed 122 to fenced search (0.61), and refused 2 with immediate 16123 referral (0.01). Halted requests retrieved zero sources. Extractor agreement was 0.52 (miss rate 0.475, false-positive rate 0.005, mapped hazard 0.1607 [8.69, 27.81], firewall diagnostic case `farmer_q_593`); crop slots were labeled by a single reviewer.

### Paired Equivalence Evaluation
In a paired equivalence evaluation ($n=400$, categories B, C, D, I), blind retrieval produced a wrong-crop advice rate of 0.30 (95% CI: [25.72, 34.66]) compared with 0.30 (95% CI: [25.72, 34.66]) for the gated arm, yielding $p=1.0$ by McNemar's exact test (0/0 discordant transitions). **This indicates no observed difference under the evaluated mapping rather than mathematical equivalence.** The descriptive F-spread showed a mean of 2.39 distinct crops in the blind top-5 retrieval set, with an unmapped crop fraction of 0.1628.

### Controlled Pilot and PRISM Conformance
A controlled pilot confirmed gate behavior: 100/100 ambiguous requests halted and 140/140 specified passed. Across 1,000 PRISM queries, overall design conformance was 0.458: clarification 86/100 (0.86), concept hypotheses 258/458 (0.5633), fact base 54/74 (0.7297), safety gate 44/100 (0.44), document RAG 16/168 (0.0952), and conversational follow-up 0/100 (0.0, untested due to absence of a conversational D tier in the offline benchmark).

### Token Metering
Token measurements were collected separately: clarification required median 89 tokens versus 2,146 tokens for retrieval context. For live grounded rows, median input was 1,111 tokens and median output was 221 tokens. No blended token-saving percentage is claimed.

### Live--Deterministic Comparison
On 200 queries, an unconstrained live model halted only 0.10 of ambiguous requests (agreement 0.68, median latency 4,218.6 ms, p95: 6,645.1 ms). An exploratory 60-row answer review yielded 19/60 (31.7%) medium-or-better ratings; this is a descriptive inspection and does not establish a quality superiority claim.

---

## Appendix D: Verifier, Safety, and Observability Detail

### Live Safety Evaluation
Over 420 live API calls, the guarded configuration produced an attack success rate of 0.95% (95% CI: [0.26, 3.41]) versus 36.19% ([29.99, 42.88]) unguarded. On Bangla-native attacks ($n=100$), guarded ASR was 0.10 ([5.5, 17.4]) versus 0.83 unguarded. Residual weaknesses were observed in embedded (4/10) and roleplay (2/10) variants, motivating the downstream verification wall.

### Dosage-Claim Verifier
Table 7 reports dosage-verifier accuracy across targeted mutation categories ($n=38$ answers, 114/118 mutations detected, 0/38 clean false positives).

### Table 7: Dosage-Verifier Results Across Mutation Categories
| Mutation Type | Detected |
|---|:---:|
| Dose $\times 2$ | 33/33 |
| Dose $\div 2$ | 30/31 |
| Chemical substitution | 22/25 |
| Unit substitution | 29/29 |
| Clean-answer false positive | 0/38 |

Four misses were autopsied. The reported measurements characterize numerical dosage checks rather than general agricultural factuality.

### Safety Envelope and Out-of-Domain Audit
An offline probe across $n=3,000$ queries (2,000 naturalistic, 1,000 adversarial) evaluated deterministic routing against gold labels: certification recall was 0.7165 (95% CI: [69.63, 73.58]), refuse recall was 0.4930 ([46.21, 52.40]), and dangerous acceptance was 0.3740 ([34.45, 40.44], $n=374$) on offline stub generation. An out-of-domain audit showed the Tier-0 precheck blocked 10/10 adversarial prompt injections but refused 0/30 off-topic queries, which pass to downstream intent routing.

### Usability Observability Proxy
A composite observability evaluation across 400 held-out requests yielded an aggregate proxy score of 94.5/100 across five operational signals: event-trace preservation (20.0/20), retrieval precision (18.8/20), visual ONNX agreement (20.0/20), time-to-diagnosis latency (18.7/20), and multimodal contradiction detection (17.0/20). **We explicitly disclose that this is an internal telemetry observability proxy, NOT a System Usability Scale (SUS) score; no recruited human-subjects trial has been conducted.**

---

## Appendix E: Delivery, Offline Operation, and Deployment

### SMS Enforcement
The SMS packer produced 299/300 valid offline-ready messages and 100/100 valid live-ready messages ($\le 160$ characters). Referral purity was 16/16. In the baseline live run, naive hard truncation dropped dosage fields in 0/84 advisory cases because conversational preambles displaced numerical parameters past 160 characters. We resolved this by implementing the deterministic 11-slot SMS template compressor (E15 Arm A), which guarantees 100.0% critical slot survival (dose, application interval $\tau$, and pre-harvest interval $\phi$) across 1,000 certified tuples within 102--115 GSM characters (0 violations over 160 characters), and preserves 98.5% (65/66) of dosage claims on the live benchmark.

### Offline Retrieval
Local BM25 achieved a hit rate of 0.94 with service-worker precaching (0/400 cached misses). Under simulated packet loss, local retrieval preserved 0.94, whereas remote retrieval dropped by 13.25 pp (rural edge, 15% loss) and 30.0 pp (severe 2G, 30% loss).

### Installation Footprint
Table 8 details measured installation footprints.

### Table 8: Measured Installation Footprint for KrishokTech
| Artifact | Size (MB) |
|---|:---:|
| Unique ONNX assets | 95.64 |
| Minimal installation | 284.0 |
| Full installation | 339.6 |

### Latency Breakdown
Table 9 details measured non-LLM latency components ($n=400$, median 33.565 ms; live LLM excluded).

### Table 9: Measured Non-LLM Latency Components ($n=400$ requests)
| Component | Median (ms) | p95 (ms) |
|---|:---:|:---:|
| Safety processing | 0.321 | 0.705 |
| BM25 retrieval | 26.831 | 61.248 |
| Verification | 4.815 | 11.220 |
| **Total non-LLM overhead** | **33.565** | **67.833** |

### Zero-LLM Operation and Modeled Cost
The evaluated tier mix yielded 7.8% zero-LLM turns (5.6% Tier-0, 0.0% Tier-1, 2.2% Tier-2, 92.2% Tier-3). Modeled cost was USD 0.1798 per 1,000 turns versus USD 0.1950 for unconstrained Tier-3 generation (a 7.79% modeled saving). Cost is modeled from the tier mix, not billed expenditure.

### Trace Ordering
Across 100 evaluation cases, all 100 provenance traces preserved the required event ordering (median 9.0 events per turn).

---

## Appendix F: Additional Demonstration States and Failure Gallery

### Visual Walkthrough of Operational States
The following figures illustrate the complete visual walkthroughs of the application across the five operational scenarios:
- **Figure 7:** Crop-less treatment clarification state (S1) (`screenshot1_halt_clarification.png`). When an underspecified Bengali symptom query is submitted without naming the crop, the system halts with zero retrieval and presents interactive quick-reply crop chips.
- **Figure 8:** Photo-driven crop constraint state (S2) (`screenshot3_photo_crop_scope.png`). On-device visual inference predicts the crop species from a leaf photograph and scopes BM25 evidence retrieval strictly to the verified species manual.
- **Figure 9:** Text--image mismatch badge state (S3) (`screenshot4_mismatch_badge.png`). Disagreement between user text and photograph raises an interactive warning badge, halting chemical recommendations until the farmer confirms the crop.
- **Figure 10:** Constrained delivery states:
  - (a) Terminal 16123 referral (S4) (`screenshot7_16123_safety_referral.png`).
  - (b) Offline cached PWA advisory card served via local BM25 (S5) (`screenshot8_offline_mode.png`).
  - (c) 160-character SMS packing and sentence-synchronized Bengali neural read-aloud (S5) (`screenshot9_sms_tts.png`).

### Disclosed Failure Catalogue

**Implicit Crop Reference.** The single missed farmer contradiction case (`farmer_q_63`) involved an implicit crop reference, illustrating that the contradiction badge covers explicit textual mentions rather than indirect references.

**Gate Firewall Case.** Deterministic gate analysis identified `farmer_q_593` as a representative firewall case where colloquial symptom phrasing bypassed the keyword gazetteer, motivating the downstream verifier.

**Adversarial Generation Residual.** Bangla-native adversarial testing revealed residual vulnerabilities in embedded (4/10) and roleplay (2/10) attacks, demonstrating why pre-render dosage verification is required even when upstream guards pass.

**Off-Topic Handling Across Tiers.** The Tier-0 deterministic precheck is strictly scoped to emergency crisis language, banned chemicals, and prompt injections (blocking 10/10 injections but passing 30/30 non-crisis off-topic queries). Evaluating these 30 queries through the production Tier-1 LLM classification branch (`google/gemini-2.5-flash-lite`) achieves a 25/30 (83.33% [66.44, 92.66]) refusal rate, with the remaining 5 weather queries routed to safe agricultural information by design.

**SMS Dose Truncation and Deterministic Resolution.** Baseline naive string truncation resulted in 0/84 dosage field survival as introductory conversational text pushed dosage parameters past the 160-character boundary. Implementing the deterministic 11-slot template compressor (E15 Arm A) in the backend resolved this, achieving 100.0% critical slot survival across 1,000 certified tuples and 98.5% (65/66) on authentic farmer benchmark advisories.

---

## Appendix G: Active Limitations Ledger, Retired Resolutions, and Scope of Claims

To ensure complete transparency and reproducibility, Table 10 reproduces the active system limitations and validated boundaries ledger from `LIMITATIONS.md`. Table 11 documents the limitations that were empirically resolved and retired through new measurements and verified implementations. Table 12 further summarizes the empirical distinctions and validated boundaries of all claims throughout the paper.

### Table 10: System Limitations and Validated Boundaries Ledger
| # | Limitation | Evidence Status | What We Do Instead / Validated Scope |
|---|---|---|---|
| 1 | N03 small $n$ (38 answers; per-type $n$ 8--33) | `Real_Measured_SmallN` | Report per-type rates with Wilson CIs; no pooling; no generalization beyond dosage-claim sentences. |
| 2 | Crop-router label mismatch (family vs species; top-1 0.0259) | Measured + Disclosed | Report 0.0259 ONLY as mismatch diagnostic with species breakdown; router accuracy unclaimed. |
| 3 | Rice INT8 rejected (2.5 pp drop $> 2.0$ pp gate) | Measured | Artifact exists, never deployed, never cited as usable. |
| 4 | INT8 latency gap on non-VNNI x86 CPU | Measured | Lack of AVX-512 VNNI on x86 causes 1.5--2.0x software dot-product emulation overhead. Validated strictly as 3.7x storage reduction (0.00 pp drop), not speedup. |
| 5 | N07 implicit-crop miss (`farmer_q_63`) | Measured | Badge claim scoped to explicit-text contradiction; 53/54 farmer + 400/400 PRISM (453/454 combined). |
| 6 | N08 perfect-gold fence | Measured | Simulation of perfect routing, not classifier performance; no absent-crop generalization. |
| 7 | N09 seeded-memory conformance | Measured | Conformance, not independent accuracy; follow-up D untested; safety is precheck-only lower bound. |
| 8 | N11 cost vs coverage trade-off | Stated | Operating-point comparison (halt + latency) only; 60-row manual rubric scoring pending; no coverage claim. |
| 9 | Single-reviewer labels (200 crop slots) + autopsies | Disclosed | Second human pass listed as upgrade path; hazard numbers labeled single-reviewer. |
| 10 | Dense retrieval unevaluated (BM25-only throughout) | Stated | All retrieval numbers scoped BM25-only; dense is fallback, out of scope. |
| 11 | Live LLM latency excluded from overhead p50s | Stated | All p50 figures exclude generation unless labeled live (N11 p50 4.2 s). |
| 12 | Bangla-native injection residual (10.0% [5.5, 17.4], $n=100$) | Measured with CI | Reported as residual risk with localized weakness (embedded 4/10, roleplay 2/10); motivates downstream verifier wall. |

### Table 11: Evaluation-Status Summary and Scope of Claims
| Component | Status | Interpretation and Validated Boundary |
|---|---|---|
| Deterministic farmer gate | Real measured | 76/200 halted (122 passed, 2 refused); single-reviewer labeling limits generalization. |
| Equivalence arm | Real measured | $n=400$; blind vs gated 0.30 ($p=1.0$, no-observed-difference); mean 2.39 distinct crops. |
| Pilot halt/pass | Pilot | 100/100 ambiguous halted and 140/140 specified passed; conformance check only. |
| Crop-specific vision | Real measured | All six crop models measured ($N=4,294$; all $\ge 0.94$ top-1); INT8 evaluated on 1--4 threads (3.7x size drop, 0.00 pp drop). |
| Family router | Real measured | 433/437 after frozen family mapping; wheat-800 excluded. |
| Crop fence | Real measured simulation | Perfect-gold routing; not end-to-end classifier performance. |
| Mismatch badge | Real measured | 453/454 explicit contradictions; implicit conflicts not fully covered. |
| Safety guard | Real measured | 420 live calls; residual failures remain (0.10 Bangla-native ASR). |
| Off-topic audit | Real measured analysis | Injections 10/10 blocked; off-topic 0/30 refused by Tier-0 precheck vs 25/30 (83.33%) by Tier-1 live LLM NLU. |
| Dosage verifier | Real measured, small-$n$ | Per-mutation results; no pooled factuality claim. |
| Routing probe envelope | Real measured envelope | $n=3,000$; certify recall 0.7165, dangerous acceptance 0.374 on offline stub. |
| SMS | Real measured | Length and referral constraints validated; dosage survival validated via deterministic 11-slot compressor (100%). |
| Offline retrieval | Measured deterministic path | BM25 hit rate 0.94; network-loss effects simulated (+13.25 / +30.0 pp). |
| Installation footprint | Real measured | 95.64 MB unique ONNX, 284.0 MB minimal, 339.6 MB full. |
| Tier-mix cost | Computed from tokens | USD 0.1839 per 1,000 turns (USD 0.1798 modeled) under 7.8% zero-LLM mix. |
| LLM latency | Not measured in overhead | Live latency is excluded from the 33.565 ms non-LLM figure. |