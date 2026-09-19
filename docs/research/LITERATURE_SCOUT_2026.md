# Literature Scout — 2026 Survey for KrishokTech

Scope: 2024–2026 publications on agricultural LLM/RAG, Bengali low-resource NLP,
grounding/safety, voice/multimodal, agentic pipelines, and agri-AI evaluation.
All URLs were surfaced via live search (arXiv, ACL Anthology, Frontiers, MDPI, IEEE,
PubMed, Semantic-Scholar-indexed pages) on 2026-08-14. Claims marked `[unverified]`
where the source was a search snippet rather than a full read.

> **Policy note:** search surfaced the deprecated KrishokTech v1 paper
> (arXiv:2606.29243). Per `AGENTS.md` §2.9 and `docs/PAPER_POLICY.md` it is INVALID
> and excluded here; no number from it is reused.

---

## (a) Per-theme synthesis of state-of-the-art

### Theme 1 — Agricultural LLM / RAG question-answering

The 2024–2026 SOTA has moved from naive chunk-vector RAG toward **hybrid
retrieval + structured knowledge + query-adaptive retrieval**:

- **Hybrid dense+sparse is now the baseline that beats single-channel RAG.** A
  cross-lingual case study on an agricultural machine manual (9 LLMs, 3 RAG
  strategies, unanswerable-question tests) found Hybrid RAG consistently beat
  direct long-context prompting, even on small models (Qwen 2.5 7B >85% accuracy),
  and that long-context "lost-in-the-middle" degrades with context size.
  *Agri-Query*, 2025, arXiv:2508.18093.
- **Graph-augmented RAG suppresses hallucination in crop-disease domains.** Crop
  GraphRAG builds a KG (crops, diseases, pests, symptoms, control measures; 3,100+
  records, 96 crops) with Leiden community summaries, and routes queries into
  entity-centric *local* retrieval or community-summary *global* retrieval; it
  reported accuracy/coverage gains and hallucination suppression over naive RAG
  and BM25+LLM baselines. *Frontiers in Plant Science*, 2026, DOI
  10.3389/fpls.2025.1696872. AgriGPT's Tri-RAG (dense + BM25 + multi-hop KG
  reasoning over ~2M triples) reports similar gains on 13 agri tasks.
  *arXiv:2508.08632*, 2025.
- **Query-complexity-adaptive retrieval works.** AHR-RAG classifies questions
  into single-hop vs multi-hop, uses BM25/Elasticsearch for single-hop and
  vector+graph fusion (RRF) for multi-hop, hitting accuracy 0.921 (single-hop) /
  0.748 (multi-hop) vs Self-RAG and Adaptive-RAG baselines on crop pest QA.
  *Smart Agriculture*, 2026, DOI 10.12133/j.smartag.SA202506026. Sem-RAG (dual
  store: chunk embeddings + community summaries) similarly outperforms NaiveRAG
  and GraphRAG on corn QA. *Applied Sciences* 15(19):10850, 2025.
- **Region/locale matters for agri advice.** AgriRegion adds geospatial metadata
  to retrieval and region-prioritized re-ranking over verified extension
  documents, reporting 10–20% hallucination reduction and better trust scores
  vs generic systems. *arXiv:2512.10114*, 2025.
- **Domain SFT alone is not enough** — every evaluation that measures it finds
  fine-tuning improves formatting/register, while grounding gains come from
  retrieval. Sem-RAG's LoRA addition improved Answer-C by only ~0.5–0.85%.
  *Applied Sciences*, 2025.

### Theme 2 — Low-resource / Bengali NLP for agriculture

- **Translation-sandwich RAG is the current pragmatic pattern for Bengali.**
  Query → English (with domain keyword injection mapping colloquial terms like
  "Magra"→"Stem Borer") → retrieval over English FAO/IRRI corpora → answer →
  translate back to Bengali. Reported reliable grounding, out-of-domain
  rejection, <20s end-to-end latency, fully open-source/4-bit quantized on
  consumer hardware. *arXiv:2601.02065*, 2026. Farmer.Chat independently found
  generating directly in the source language underperforms translate-route-answer.
  *arXiv:2409.08916*, 2024.
- **Bengali resources are maturing fast:** AgriEnBn (first EN↔BN agri MT corpus,
  2,883 train pairs + human-verified gold test with safety subset for dosages and
  negations; huggingface.co/datasets/Sabuktagin/AgriEnBn); KrishiGyan (5,529
  Bengali Q&A with chain-of-thought traces grounded in BARI/BRRI/DAE/SRDI
  publications, Qwen3-14B LoRA baseline, PEEIACON 2026;
  huggingface.co/datasets/AROY76/KrishiGyan).
- **Bengali LLM viability is contested.** COLING 2025 study ("Too Late to Train,
  Too Early To Use?") found modern English-centric LLMs transfer well on
  reasoning but struggle with Bengali script generation, suffer inefficient
  Bengali tokenization, and machine-translated training data carries bias —
  concluding there is a genuine need for Bengali-oriented models but a shortage
  of high-quality pretraining data. *ACL Anthology 2025.coling-main.79*.
- **Dialectal robustness is a hard, unsolved problem in speech.** Ben-10
  (78-hour, 10-dialect Bengali STT corpus) shows foundation ASRs fail badly on
  regional dialects in both zero-shot and fine-tuned settings; dialect-specific
  training is required. *IJCNLP-AACL 2025*, aclanthology.org/2025.ijcnlp-short.17.
  BanglaTalk (dialect-aware IndicWav2Vec ASR + RTP streaming, ~4.9s latency at
  24kbps) is the first real-time dialect-aware Bengali speech system.
  *BanglaLP 2025*, aclanthology.org/2025.banglalp-1.4.
- **Text-side dialect mapping is a cheap, proven lever** (TraSe translative
  prompting for Bangla RAG, LM4UC 2025, aclanthology.org/2025.lm4uc-1.2) — and
  the project's existing 110-word dialect map is the same technique at term level.

### Theme 3 — Safety & faithfulness in domain LLMs

- **Citations are not trustworthy by default.** "Correctness is not Faithfulness
  in RAG Attributions" shows up to **57% of citations lack faithfulness** — models
  post-rationalize citations to fit parametric knowledge rather than genuinely
  relying on documents — even in Command-R+, a model trained for RAG. *SIGIR
  ICTIR 2025*, DOI 10.1145/3731120.3744592. This is the strongest argument for
  independent verification rather than trusting self-citations.
- **NLI-based verification pipelines are the established fix.** VeriCite
  (generate → NLI-verify claims → select supporting evidence → re-attach citations)
  improves citation quality without hurting answer correctness.
  *arXiv:2510.11394*, 2025. MIRAGE instead uses model internals (saliency over
  context-sensitive tokens) for attribution, avoiding external verifiers.
  *EMNLP 2024*, aclanthology.org/2024.emnlp-main.347.
- **Refusal is a first-class, measurable capability.** TRUST-SCORE quantifies
  grounded attribution AND refusal behavior (over-responsiveness, excessive
  refusal), and TRUST-ALIGN (DPO on RAG data) improves both — a LLaMA-3-8B
  aligned this way matched GPT-4 on trust score. *arXiv:2409.11242*, 2024.
  Corollary from Agri-Query: smaller models hallucinate more on unanswerable
  questions (lower specificity), so abstention matters most on small local models.
  *arXiv:2508.18093*.
- **RAGAS metrics** (faithfulness, answer relevancy, context precision/recall)
  remain the standard automated RAG eval suite. *Es et al., EACL 2024 System
  Demonstrations*. "Generate but Verify" formalizes faithfulness prediction as a
  coupled task with dedicated precision/recall, showing post-answer NLI beats
  pre-answer prediction. *IJCNLP 2025*, aclanthology.org/2025.ijcnlp-long.56.

### Theme 4 — Voice / multimodal for agriculture

- **Voice-first is validated, with caveats.** The AIEP Initiative (5 advisory
  MVPs, Kenya + Bihar, ~800-farmer study, NPS≈60) found the working pattern is
  **ASR→MT→TTS around an English-language reasoning core**, that sub-5s latency
  is hard, and that low-resource ASR/MT errors are the top failure mode (e.g.
  "mushroom"→"mosquito" translation drift). They recommend golden Q&A sets for
  evaluation. *arXiv:2601.11537*, 2026.
- **Farmer.Chat** (15,000+ farmers, 300k+ queries, 4 countries, 6 languages)
  confirms multilingual+multimodal (text/voice notes/images) RAG works at scale,
  with >75% of queries successfully answered; women and low-literacy users were
  top beneficiaries. *arXiv:2409.08916*, 2024.
- **KrishokBondhu** is the direct Bangladeshi precedent: OCR-digitized
  handbooks + LanceDB + Gemma 3-4B + Bengali ASR/TTS over a phone interface;
  72.7% high-quality responses on a self-curated test set, +44.7% composite
  score vs KisanQRS baseline. Evaluation caveats: small matched-query set,
  manual scoring. *arXiv:2510.18355*, 2025.
- **Cheap asymmetric stacks exist for Indic languages:** distil-whisper ASR +
  MMS-TTS (Kannada) voice-first crop recommendation, 98.5% suitability accuracy
  — evidence you need NOT pay for cloud speech APIs. *arXiv:2507.08832*, 2025.
  Krishi Sathi adds **intent-slot clarification dialogs** before RAG for
  vague farmer queries (EN+HI, ASR/TTS, 97.5% query completion).
  *arXiv:2508.03719*, 2025. Foundational HCI result: illiterate users prefer
  audio-only; semi-literate prefer audio+text. *FarmChat, IMWUT 2018*.

### Theme 5 — Agentic / tool-using LLM pipelines for agriculture

- **Tool-grounding beats model scale.** On AgriWorld (Python-execution
  environment with geospatial/soil/weather tools), GPT-4o scored only 36.75%
  vs 73.84% for a Qwen3-32B agent with an execute-observe-refine loop — general
  models hallucinate API names. Executable checkers (schema validity, unit
  checks) are core to the design. *arXiv:2602.15325*, 2026. Same pattern in
  weather: Zephyrus agents beat text-only by up to 35 points.
  *arXiv:2510.04017*, 2025.
- **Contract-driven orchestration** (AgriAgent: simple tasks → fast path;
  complex tasks → capability-contract planning + tool hub + dynamic tool
  generation, 96.9% tool-generation success) shows hierarchical
  complexity-routing outperforms unified agent loops. *arXiv:2601.08308*, 2026.
- **Multi-agent critique roles are maturing:** Dynamic Orchestration framework
  (Retriever → Reflector → 2 Answerers → Improver) closes retrieval and answer
  quality loops with explicit evidence-threshold gates for agri VQA.
  *arXiv:2509.24350*, 2025. AgroAskAI (AAAI 2025) adds a reviewer agent +
  full conversation logging for auditability in climate-adaptation advice.
- **Benchmarks now evaluate process, not just answers:** AgroTools provides 539
  QA + 14 executable tools with dual-view scoring (tool-choice/argument validity
  at process level, final-answer at outcome level); current models fail most
  badly at tool planning and argument generation. *arXiv:2605.22366*, 2026.

### Theme 6 — Evaluation / benchmarking of agri AI

- **Human-vs-AI extension evaluation exists and is sobering:** 32 real farmer
  questions, 6 extension agents vs ChatGPT, judged by 4 evaluators — chatbot
  responses preferred in 78% of cases but *poorer on planting time, seed rate,
  and fertilizer rate/timing* (the exact dose/local-appropriateness failure
  mode KrishokTech's verifier targets). *Frontiers in Sustainable Food Systems /
  PubMed 38341517*, 2024.
- **Expert-grounded benchmarks are the 2025 trend:** AgMMU (746 MCQ + 746
  open-ended Qs distilled from 116k real farmer↔USDA-extension dialogues,
  human-verified) and MIRAGE (29k single-turn + 6.3k multi-turn consultations,
  7,600+ biological entities, "clarify-or-respond" decisions) set the bar for
  realistic, non-synthetic evaluation. *arXiv:2504.10568*, *arXiv:2506.20100*,
  2025. AgXQA formalizes extension-domain extractive QA with a custom
  human-eval metric (Computers and Electronics in Agriculture 225:109349, 2024).
- **Consortium infrastructure exists:** AI AgriBench (UIUC Center for Digital
  Agriculture + crop science + extension partners) maintains expert-validated
  agronomy QA pipelines and public leaderboards. *aiagribench.org*.
- **LLM-as-judge has limits:** ACL 2025 Findings work on climate-adaptation QA
  (expert-designed criteria, 15 experts) found LLMs cannot yet reliably identify
  high-quality vs erroneous agri answers compared to domain experts — human
  spot-checking remains mandatory. *aclanthology.org/2025.findings-acl.368*.
- **Farmer-facing eval guidance:** AIEP recommends golden Q&A sets from real
  farmer queries + expert scoring; NPS≈60 across 5 deployments suggests
  satisfaction is achievable. *arXiv:2601.11537*, 2026.

---

## (b) Transferable techniques for KrishokTech (8–12 concrete)

| # | Technique | What it is | Why it matters here | Effort | Source |
|---|-----------|-----------|---------------------|--------|--------|
| 1 | **Hybrid retrieval + reciprocal-rank fusion (RRF)** | Run BM25 and dense in parallel, fuse with RRF instead of picking one | The project already has both channels; fusing is a small change that repeatedly beats single-channel, incl. on small models — and directly strengthens the Retrieval Agent | **Low** | Agri-Query, arXiv:2508.18093; AHR-RAG, Smart Agriculture 2026 |
| 2 | **Query-type routing: single-hop vs multi-hop retrieval** | Classify query complexity first; simple → BM25/keyword; complex → multi-hop + fusion | Extends the existing Router Agent's job with zero new infra; AHR-RAG's adaptive mode beat Self-RAG/Adaptive-RAG on crop pest QA | **Low–Med** | AHR-RAG, DOI 10.12133/j.smartag.SA202506026 |
| 3 | **NLI-verified claims in the Verifier Agent** | Replace/augment prompt-based verification with NLI entailment checks: decompose answer into claims, check each claim is entailed by retrieved passages before release; drop or annotate unsupported claims | Direct upgrade to agent step [4]; addresses dosage-claim grounding. Bengali NLI models are scarce — use a multilingual NLI model (e.g. XLM-R based) + Bengali claim decomposition; start with dosage-only enforcement | **Med** | VeriCite, arXiv:2510.11394; Wallat et al., ICTIR 2025 (57% unfaithful citations warning) |
| 4 | **Explicit refusal metrics + "learn to refuse" alignment** | Track over-responsiveness (answers unanswerable Qs) and excessive refusal; align the 4-bit model (LoRA/DPO on refusal+grounded-attribution pairs) | Maps directly to `low_confidence` / `off_topic` categories and the safety metrics panel; small models are the worst hallucinators on unanswerable questions, so measuring refusal is cheap insurance for the demo | **Low–Med** | TRUST-SCORE/TRUST-ALIGN, arXiv:2409.11242; Agri-Query, arXiv:2508.18093 |
| 5 | **Translation-sandwich + colloquial→scientific keyword injection** | BN query → EN (injecting dialect/colloquial term mappings, e.g. "Magra"→"Stem Borer") → retrieve → EN answer → BN; add safety-verified BN→EN lexicon | The project already has a 110-word dialect map and Bengali corpus; this paper reports reliable grounding, out-of-domain rejection, and <20s latency on consumer hardware with 4-bit models — a proven, deployment-matched pattern | **Med** | arXiv:2601.02065; Farmer.Chat, arXiv:2409.08916; AgriEnBn glossary, HF |
| 6 | **Small entity KG + community summaries beside the FAISS index (local/global query modes)** | Build a crop→disease→pest→treatment KG from the existing knowledge nodes; retrieve adjacency subgraphs for entity queries, community summaries for broad questions | The project's 290 knowledge nodes are already semi-structured; Crop GraphRAG shows this is the strongest published hallucination suppressor in crop-disease QA | **High** | Crop GraphRAG, DOI 10.3389/fpls.2025.1696872; Sem-RAG dual-store, Appl. Sci. 2025 |
| 7 | **Region/season metadata filtering + re-ranking** | Tag nodes with region/season/metadata; filter candidates by farmer location before final re-rank | Advice valid in Rangpur can be wrong in Chattogram; AgriRegion's geospatial re-ranking cut hallucinations 10–20%. The dataset already carries season tags | **Low** | AgriRegion, arXiv:2512.10114 |
| 8 | **Execute-observe-refine for dose math (verifiable computation)** | Let an agent compute dosages via a sandboxed calculator/code tool with unit + dimensional validation instead of free-text arithmetic | Chemical-dose grounding is the project's headline safety risk; executable checkers (schema/unit/numeric-conservation validation) turned 36%→74% accuracy in AgriWorld — strongest known fix for "plausible but wrong" numbers | **Med–High** | AgriWorld/Agro-Reflective, arXiv:2602.15325; Zephyrus, arXiv:2510.04017 |
| 9 | **Audio-in-app via asymmetric ASR/TTS stack** | Add Bengali voice input (Whisper-family fine-tune or Wav2Vec-BERT) + TTS output; keep text path; plan dialect handling explicitly | Farmer.Chat/AIEP/KrishokBondhu all confirm voice is the adoption lever for low-literacy users; open-source stacks avoid cloud costs. Do NOT assume stock Whisper handles Bengali dialects (Ben-10 shows it fails) | **Med–High** | KrishokBondhu, arXiv:2510.18355; arXiv:2507.08832; AIEP, arXiv:2601.11537; Ben-10, IJCNLP 2025 |
| 10 | **Expert-grounded benchmark incl. unanswerable questions** | Build a golden QA set from real farmer queries (project already has 1,001) + extension-officer answers, scored by 2+ evaluators; include unanswerable/out-of-scope items to measure refusal and hallucination | Nigeria study: ChatGPT beat agents 78% but lost exactly on dose/timing — this benchmark shape surfaces precisely what the demo must prove; unanswerable items power the safety metrics panel | **Med** | PubMed 38341517; AIEP golden sets, arXiv:2601.11537; RAGAS metrics, EACL 2024 |
| 11 | **Clarify-or-respond intent slots before retrieval** | When a farmer query is under-specified (crop? stage? region?), ask 1–2 slot questions before generating, instead of guessing | Krishi Sathi reached 97.5% query-completion with this pattern; MIRAGE shows current models fail exactly at clarify-or-respond — a cheap differentiator and demo moment | **Med** | Krishi Sathi, arXiv:2508.03719; MIRAGE, arXiv:2506.20100 |
| 12 | **Dual-view agent metrics (process + outcome)** | For each pipeline step log: safety-category correctness, tool/step choice validity, argument validity, plus final-answer score | Powers the poster's agent-trace visuals with real metrics; AgroTools' finding (models fail at tool planning/argument generation) tells us what to instrument first | **Low** | AgroTools, arXiv:2605.22366 |

---

## (c) Over-hyped / risky approaches to avoid

1. **Direct long-context prompting instead of RAG.** Agri-Query measured it:
   hybrid RAG beat long-context on the same manual even for 128K-window models,
   with a pronounced lost-in-the-middle effect. Keep the BM25+dense pipeline.
2. **Trusting self-generated citations without verification.** Up to 57% of
   RAG citations are post-rationalized, not faithful (ICTIR 2025). Any
   "citation-grounded" claim for the demo must survive an independent
   entailment check, or it will not survive a skeptical judge.
3. **GraphRAG as a magic bullet.** Crop GraphRAG's gains are real but measured
   on self-built test suites; KrishiBot (BRAC thesis, 2025) claims 91.58%
   accuracy on 500 self-made questions — numbers like this are not
   cross-comparable. Use KG augmentation as an incremental channel, not as a
   replacement, and never quote vendor-style accuracy figures.
4. **Fine-tuning alone as a hallucination fix.** Every measured study (Sem-RAG:
   +0.5–0.85% from LoRA; own project's finding; KrishokBondhu) shows retrieval
   carries grounding; SFT mainly improves register/format. Do not let the
   fine-tuned Gemma-4 claim "safety" without the retrieval+verifier stack.
5. **Pure LLM-as-judge evaluation.** ACL 2025 Findings: LLMs are measurably
   worse than agronomy experts at identifying erroneous agri answers. Always
   keep a human (extension officer / researcher) spot-check lane.
6. **Assuming stock ASR handles Bengali dialects.** Ben-10: foundation ASRs
   fail on regional dialects in zero-shot AND fine-tuned settings; AIEP
   documents translation drift ("mushroom"→"mosquito"). Any voice demo must
   either constrain to standard Bengali or budget for dialect-specific
   fine-tuning — otherwise the safety layer operates on garbled text.
7. **Unbounded tool-calling with general models.** GPT-4o scored 36.75% on
   AgriWorld by inventing API names; LLM-written SQL against real data has the
   same failure class. Tool calls need schema grounding and sandboxed,
   read-only, validated execution (see FieldOps pattern: sqlglot validation,
   query_only mode) if ever added.
8. **Huge synthetic-data engines without verification.** AgriGPT's 4-agent
   data engine (342K QA) works but the value is in the human-verified seed +
   filtering, not the volume; synthetic QA inherits systematic errors. Prefer
   the verified 20,112-record corpus already built over mass generation.
9. **Agent traces without real logging.** The audit log is the demo's safety
   evidence; multiple papers (AgroAskAI, Dynamic Orchestration) now treat
   conversation logs + decision checkpoints as first-class. Don't render
   fake-feeling steppers — feed them from the actual log.

---

### Open questions worth resolving before adoption
- Availability/quality of a **Bengali NLI model** for Verifier upgrade (multilingual XLM-R-based candidates need a small Bengali validation set — the AgriEnBn safety test subset is a ready seed).
- Whether to expose **weather/soil tools** at demo time: tool-grounded agents score far higher (Zephyrus/AgriWorld), but tool reliability during a 3-minute demo is a risk — a read-only, mocked-data tool is a safe middle ground.
- **Voice scope**: in-app Bengali ASR/TTS (med effort, strong demo impact) vs full IVR call center (high effort, not needed for the demo).
