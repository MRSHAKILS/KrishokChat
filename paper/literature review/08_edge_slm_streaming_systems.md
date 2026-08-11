# Cluster 8 — Edge/Compact LLMs + Streaming Systems: Literature Findings (2025 → Aug 2026)

**Generated:** 2026-08-12 · **Scout:** 8 · **Status:** citations verified against fetched arXiv/official pages

---

## 1. Key papers

**Gemma 4 Technical Report** — Gemma Team, Google DeepMind, arXiv:2607.02770, Apr 2026. Four sizes: E2B (5.1B total / 2.3B active), E4B, 26B-A4B MoE (~4B active), 31B dense; thinking mode; 140+ languages; 256K context on large, 128K on E2B/E4B; Apache 2.0. E2B roughly matches Gemma 3 27B on MMLU-Pro (60.0 vs 67.6, no-think) with ~10× fewer parameters; E4B scores 57.5 on τ2-bench retail agentic tool use vs 6.6 for Gemma 3 27B. E2B 4-bit weights fit under 3 GB RAM; runs fully offline on phones, Raspberry Pi, Jetson Orin Nano.

**Gemma 3 Technical Report** — arXiv:2503.19786, Mar 2025. 1B–27B; 4B-IT competitive with Gemma 2 27B-IT; 128K context via 5:1 local/global attention; memory table: 4B int4 2.6 GB, 7.3 GB with KV cache at 32K — the hardware-envelope numbers every edge paper cites.

**Qwen3 Technical Report** — arXiv:2505.09388, May 2025. Dense 0.6B–32B plus MoE; 119 languages; unified thinking/non-thinking modes with an explicit thinking-budget mechanism for latency–quality control. The canonical answer to "how do you cap latency at fixed quality."

**Phi-4-Mini Technical Report** — arXiv:2503.01743, Mar 2025. 3.8B, 200K-token vocabulary, 128K context, GQA; matches models twice its size on math/coding.

**SmolLM2 / SmolLM3** — arXiv:2502.02737 (Feb 2025); HuggingFace blog (Jul 2025). 1.7B/3B at 11T tokens; SmolLM3 beats Llama 3.2-3B and Qwen2.5-3B, competitive with Qwen3-4B/Gemma3-4B; **6 languages — Bengali absent**; think/no-think modes.

**The Llama 3 Herd + Llama 3.2** — arXiv:2407.21783; Meta blog (Sep 2024). Llama 3.1 8B is the small-model multilingual/tool-use baseline; 3.2's 1B/3B built by pruning + distillation with 128K context and tool calling — the canonical "edge" lineage.

**BnMMLU** — Joy & Shatabda, arXiv:2505.18951; Findings ACL 2026, DOI 10.18653/v1/2026.findings-acl.593. 41 domains, 134,375 MCQ pairs, 24 model variants. Gemini 2.5 Flash 69.85, Qwen3-32B 65.34, Llama 3.3-70B 61.87, Gemma 3 27B-IT 61.27, TigerLLM-9B 55.70, "small Bengali models cluster near the high-20s"; returns to scale sublinear.

**Evaluating LLMs' Multilingual Capabilities for Bengali** — Bhowmik et al., arXiv:2507.23248, Jul 2025. Llama 3.2-3B drops 0.567→0.280 (English MMLU → Bengali); Qwen2.5-7B 0.690→0.414; inverse tokenization-efficiency/accuracy relation (Bengali costs ~2× tokens per word).

**KrishokChat benchmark (team's own)** — Reza, Nimi & Shahid, EACL 2026 (local copy in `paper/done papers/`). On the 350-query Farmer Benchmark eval split, Gemini-2.5-FL leads (Token F1 0.2196, halluc. 38.29%) followed by Gemma-4-26B-A4B (0.1375, 23.14%) and the fine-tuned KrishokChat-4B (0.1170, 41.14%); LLaMA-3.1-8B scores 0.0078. Fine-tuning closes most of the gap to same-scale open baselines but not to frontier scale, and closed-book generation without retrieval raises the fine-tuned model's hallucination rate — the benchmark's value is as a verifiable RAG knowledge base, not parametric memory.

**KrishokBondhu** — arXiv:2510.18355, Oct 2025. Voice RAG with Gemma 3-4B + LanceDB; 72.7% high-quality answers; 4.53 vs 3.13 (+44.7%) over KisanQRS. Direct precedent that a 4B model with retrieval carries a Bengali agri advisory system.

**KrishiGyan** — Roy & Trafder, IEEE PEEIACON 2026 (to appear; HF dataset). 5,529 Bengali agri QA pairs with CoT; Qwen3-14B 4-bit + LoRA: BERTScore 0.856→0.888, semantic cosine 0.698→0.765, 18.45M trainable params (0.86%), single H100; 7/8 metrics statistically significant. Independent evidence for QLoRA-scale domain adaptation in Bengali agri.

**RouteLLM** — Ong et al., arXiv:2406.18665 (v4 Feb 2025). Learned routers between strong/weak LLMs cut cost >2× with no quality loss. The citation for "classifier → model" routing.

**ServeGen** — arXiv:2505.09999, 2025. Production LLM workload characterization (Alibaba cloud); establishes TTFT and TBT as the SLO metric pair (P99 TTFT 2.25 s, TBT 0.5 s); naïve synthetic workloads under-provision instances by ~50% — report per-stage SLO attainment on trace-like data.

**T-LRU: Tail-Optimized Caching for LLM Inference** — arXiv:2510.15152, NeurIPS 2025. Prompt (KV) caching: OpenAI/Anthropic report 50–90% latency/cost savings from prompt reuse; T-LRU cuts P90 TTFT up to 27.5%, P95 TTFT up to 23.9%, 200ms-TTFT SLO violations down up to 38.9%.

**Latency perception studies (2025–2026)**: Zhou et al., "Thoughtful, Confused, or Untrustworthy" (CHI 2025, DOI 10.1145/3698061.3726907) — five streaming-speed conditions; TTFT and tokens/sec are the industry metrics. "The Impact of Response Latency and Task Type on Human-LLM Interaction" (arXiv:2604.06183, 2026) — controlled TTFT 2/9/20 s at 25 tokens/s: **2 s reads less thoughtful; 9 s optimal for usefulness; users read delay as deliberation**. Maslych et al. (arXiv:2507.22352, 2025): latency above 4 s degrades QoE; natural progress fillers mask delay, artificial spinners do not. Just-in-Time adaptive token pacing (ACM IUI 2026, DOI 10.1145/3772363.3798936): blank-screen waits are the dominant frustration; TTFT is a credibility signal.

## 2. Findings & insights

- **SLM capability deltas are now narrow where ground truth is supplied.** Gemma 4 E2B (2.3B active) reaches 60.0 MMLU-Pro vs 67.6 for Gemma 3 27B no-think. The remaining gap is agentic tool use — E4B (57.5) vs Gemma 3 27B (6.6) on τ2-bench retail; the hierarchy flipped within one generation.
- **Bengali is where small models still bleed.** Llama 3.2-3B loses 51% of MMLU accuracy in Bengali (0.567→0.280); Bengali-centric smalls sit in the high-20s on BnMMLU; per-word tokenization cost rises and correlates with accuracy loss. The team's Farmer Benchmark agrees: LLaMA-3.1-8B earns Token F1 0.0078 and GPT-OSS-120B 0.0002 on authentic farmer queries (EACL 2026).
- **Grounded generation beats parametric memory for dosage-critical content** (team's EACL 2026 benchmark: 4.05–7.00% chemical hallucination floor even with oracle evidence, <44% Treatment QA Correct% zero-shot; KrishokBondhu's 72.7% with 4B+RAG). Both converge on the same architecture: retrieval + 4B-class decoder.
- **Fine-tuning headroom is real and cheap** (KrishiGyan: 0.86% trainable params, single GPU, 7/8 significant metrics; QLoRA remains the budget bound).
- **Caching and routing carry the cost/latency argument** (prompt caching 50–90%; T-LRU −24% P95 TTFT; RouteLLM >2× cost reduction). Neither measured for Bengali, where tokenization inefficiency inflates prefill.
- **Latency perception is non-monotonic**: 2 s = shallow; 9 s = deliberation; >4 s conversational = QoE degradation; blank screens are the worst state. Streaming at fixed 25 tokens/s with staged progress is the documented design envelope.

## 3. Research gaps

**G1 — No Bengali agricultural SLM benchmark.** BnMMLU has no agriculture domain; AgriEval's Bengali split has no peer review and no sub-4B ranking; KrishokBondhu evaluated on self-curated queries; KrishiGyan is training data, not an eval suite; only the team's Farmer Benchmark evaluates Bengali agri at small scale (Gemini-2.5-FL 0.2196, Gemma-4-26B 0.1375, KrishokChat-4B 0.1170, Qwen-2.5-7B 0.0841, LLaMA-3.1-8B 0.0078) — one corpus, one metric family, zero replication.

**G2 — No latency–grounding tradeoff data for low-resource-tokenized domains.** TTFT budgets, caching, routing characterized on English/Chinese; Bengali's token inefficiency changes prefill cost exactly where the seed must quote p95 budgets. The dosage-hallucination rate as a function of TTFT budget is unmeasured for any language — the verifier agent can produce exactly this curve.

**G3 — Stage-trace streaming ("agent stepper") has no controlled evidence.** Perception studies test delay duration and pacing, not structured pre-output progress semantics (safety-check → retrieve → generate). Whether a stage trace beats a blank wait or spinner in a high-stakes advice context is untested; the convention is industry practice, not literature. A between-subjects report on the seed's own trace would be the first such result.

## 4. Conventions

System papers 2025–2026 report latency as **TTFT and TBT** with **p50/p95/p99 and SLO attainment** at explicit thresholds (ServeGen: P99 TTFT 2.25 s / TBT 0.5 s; T-LRU 200 ms SLO; Nexus mean/P50/P95/P99 TTFT-TBT-normalized). Hardware constraints as **quantized weight + KV-cache footprints** at fixed context (Gemma 3: int4 2.6 GB + KV 7.3 GB @32K; Gemma 4 E2B <3 GB RAM 4-bit). Streaming UX as **tokens/s and TTFT** with perception thresholds (25 tokens/s; >4 s conversational degradation). Cost claims cite **per-1M-token pricing and cache hit savings (50–90%)**. Agentic system papers treat multi-stage requests as first-class workloads with stage-level SLOs.

## 5. Positioning recommendations for KrishokChat

- Lead with the architecture the Bengali-agri literature itself converged on — citation-grounded RAG + 4B-class decoder — and present KrishokChat as the full system embodiment, with retrieval as the dosage-safety mechanism rather than parametric memory.
- Justify model choice with the BnMMLU scaling curve (sublinear returns; Qwen3-32B 65.34 ≈ ceiling) and Bengali degradation numbers (Llama 3.2-3B 0.280 vs 0.567); state explicitly which capability losses the local Gemma path accepts and which it routes to flash-lite.
- Report TTFT/TBT per agent stage (Safety → Retrieval → Generation → Verification) with p50/p95 and SLO attainment (ServeGen conventions); anchor SLO at the measured perception envelope (≤4 s conversational threshold; 9 s deliberation-sweet-spot for the advice task).
- Cite T-LRU (50–90% caching savings) and RouteLLM (>2× cost reduction) for semantic caching of repeat farmer queries and classifier-first routing.
- Frame the four-stage agent stepper as the streaming-UX contribution against blank-screen/static baselines (IUI 2026, Maslych et al.) — it converts the pre-first-token window into structured, deliberation-cued progress, and the paper reports the controlled comparison (G3) no prior system provides.