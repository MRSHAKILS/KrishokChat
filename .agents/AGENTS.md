# AGENTS.md — Canonical Agent Directives & Multi-Agent Pipeline Standards

> **CANONICAL PROJECT DIRECTIVES — KRISHOKCHAT ADVISORY SYSTEM**  
> Last Audited: 2026-09-01 | Architecture Version: 2.0  
> Applies to: All sub-agents, dispatchers, inference workers, dataset builders, and interactive coding assistants.

---

## 0. AUTHORIZED MODEL REGISTRY & SELECTION RULES (NON-NEGOTIABLE)

| Role / Pipeline Stage | Exact Authorized Model Identifier | Gateway / Provider | Quota / Concurrency Policy |
|---|---|---|---|
| **Production NLU & Cloud Benchmark** | `google/gemini-2.5-flash-lite` | OpenRouter (`OPENROUTER_API_KEY`) | Single consolidated JSON slot extraction ($\le 180$ tok) |
| **Local Advisory Generation (LoRA)** | `krishoktech-4b` | `llama-server` / Ollama (`127.0.0.1:11434/v1`) | Fine-tuned Gemma-4 4-bit base + LoRA adapter |
| **Free Gemini Key Pool (Worker A & B)** | `gemini-3.1-flash-lite` | Google Generative Language API | 14 Keys (Pool A: 7 keys, Pool B: 7 keys in `.env`) |
| **Free Gemini Key Pool (Worker C)** | `gemini-3.5-flash-lite` | Google Generative Language API | 7 Keys (Pool C: 7 keys in `.env`) |
| **On-Device Edge Perception** | YOLOv8 / YOLO26n (INT8/FP32) | ONNX Runtime / WASM ($26\text{--}265\,$ms) | 6 per-crop classifiers (Wheat, Rice, Potato, etc.) |

### Mandatory Model Selection Directives
1. **Free Gemini Key Pool (Absolute & Non-Negotiable):**
   - ✅ **ONLY `gemini-3.1-flash-lite` and `gemini-3.5-flash-lite`** are authorized for free Gemini key generation.
   - ❌ **NEVER use any other models** for free key batch tasks (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`, or preview `-preview` variants).
2. **Never switch models during retries** or error handling to bypass rate limits.
3. **Methods Section Standard:** In academic papers, cite model access dates and parameterizations in the appendix, referencing the frozen model strings.

---

## 0.1 ZERO MONEY LOSS & TOKEN PROTECTION DIRECTIVES

> **STRICT MONEY & TOKEN PROTECTION RULES** (from `OPENROUTER_SAFE_EXECUTION_POLICY.md`)

1. **Pre-Flight Key Authorization Check:**
   - Every inference script MUST perform a 1-token authorization test for all active keys BEFORE launching batches.
   - If any key returns HTTP `401 Unauthorized` or `403 Forbidden`, **ABORT IMMEDIATELY (`sys.exit(1)`)**. Never spam failed requests.
2. **Immediate Durable Disk Sync (Zero Memory Buffering):**
   - Every completed API return MUST be appended to disk (`.jsonl`), flushed (`f.flush()`), and synced (`os.fsync()`) immediately under `threading.Lock()`.
   - In-memory result accumulation (`results.append()`) is strictly prohibited.
3. **Paid Escalation Human Approval Gate:**
   - Default execution mode is strictly `FREE_ONLY`.
   - If a batch accumulates $>20$ consecutive errors, the pipeline must **PAUSE** and request human approval. Auto-escalating to paid models is strictly forbidden.
4. **Per-Request Token Caps:**
   - Structured NLU / Classification: `max_output_tokens=180`
   - Grounded Advisory Generation: `max_output_tokens=250` (local) or `500` (cloud)

---

## 0.2 3-WORKER PARALLEL DISPATCHER PIPELINE (FOR FREE GEMINI KEYS)

When running high-throughput generation using the pool of 21 verified free Gemini API keys, use the 3-worker parallel dispatcher pipeline:

```
                          [ Input Dataset / Base Generation Cells ]
                                             │
                       ┌─────────────────────┼─────────────────────┐
                       │                     │                     │
                 [ Partition A ]       [ Partition B ]       [ Partition C ]
                       │                     │                     │
                       ▼                     ▼                     ▼
                 ┌───────────┐         ┌───────────┐         ┌───────────┐
                 │ Worker A  │         │ Worker B  │         │ Worker C  │
                 │  7 Keys   │         │  7 Keys   │         │  7 Keys   │
                 │3.1-flash-l│         │3.1-flash-l│         │3.5-flash-l│
                 └─────┬─────┘         └─────┬─────┘         └─────┬─────┘
                       │                     │                     │
                  agent_a.log           agent_b.log           agent_c.log
                 checkpoints_a/        checkpoints_b/        checkpoints_c/
                       │                     │                     │
                       └─────────────────────┼─────────────────────┘
                                             ▼
                                  [ Auto-Merge & Quality Gate ]
                                  [ G1-G8 Schema Verification ]
```

1. **Key Pool Partitioning & Model Assignment (21 Active Verified Keys in `.env`):**
   - **Worker A (7 keys $\to$ `gemini-3.1-flash-lite`):** `GEMINI_API_KEY_2`, `3`, `5`, `29`, `30`, `6`, `7`
   - **Worker B (7 keys $\to$ `gemini-3.1-flash-lite`):** `GEMINI_API_KEY_8`, `9`, `10`, `11`, `12`, `13`, `14`
   - **Worker C (7 keys $\to$ `gemini-3.5-flash-lite`):** `GEMINI_API_KEY_15`, `16`, `24`, `25`, `26`, `27`, `28`
2. **Subprocess Dispatcher Semantics:**
   - Launch 3 parallel worker subprocesses (`subprocess.Popen` or `threading.Thread`) with disjoint, non-overlapping cell partitions.
   - Workers log progress to dedicated logs and write atomic checkpoints.
   - Upon completion, auto-merge outputs and run Quality Gate validation.

---

## 0.3 MANDATORY PRE-FLIGHT VERIFICATION PROTOCOL

Before launching any batch inference or evaluation script ($>50$ calls):

* **Step A (Field Name Audit):**
  Inspect the first 3 rows of the actual dataset file on disk using `python -c "import json; [print(list(json.loads(l).keys())) for l in open('FILE').readlines()[:3]]"`. Verify exact key names. Never guess fields with fallback chains (`row.get("a") or row.get("b")`).
* **Step B (Smoke Test):**
  Render and print the full system + user prompt for the first 2 rows to the terminal. Verify that any referenced image files exist and exceed $10\,\text{KB}$.
* **Step C (Lock & Checkpoint Verification):**
  Confirm thread locks and atomic temporary files (`.tmp` $\rightarrow$ replace) are configured.

---

## 1. TWO-TRACK ARCHITECTURE SEPARATION

The repository strictly enforces a two-track boundary:

```
d:\KrishokTech Advisory System\
├── backend/                   # Production Track (FastAPI, Domain, Ports, Adapters)
├── frontend/                  # Production Track (Next.js 14, TypeScript, Tailwind, UI)
├── paper/
│   ├── CEA Paper/             # Research Paper Track (Scientific Theory, Why BAA is Safer)
│   └── EACL Demo/             # Demo Paper Track (System Features, UX, Latency, Flowcharts)
└── experiments/               # Master Experiment Trace & Registry
```

1. **Production Track (`backend/`, `frontend/`, `supabase/`):**
   - Single FastAPI backend process, single Next.js frontend process.
   - Fail-closed security: prechecks run in $0.32\,\text{ms}$, 16123 escalation on banned chemicals, 11-slot relational verification.
   - Code in `backend/` must never read `paper/` or `experiments/` at runtime.
2. **Paper Track (`paper/CEA Paper/`, `paper/EACL Demo/`, `experiments/`):**
   - **EACL Demo Paper:** Focuses on **WHAT** features exist (3 TikZ flowcharts, interactive quick-reply chips, latency, streaming provenance traces).
   - **CEA Research Paper:** Focuses on **WHY** BAA is architecturally safer (eliminating $38.5\%$ cross-crop hazard, fail-closed prechecks, $0.0\%$ toxic leak rate).
3. **External Research Data Root (`E:\CSE498R\Agri-LLM\KrishokTech`):**
   - Read-only source for base datasets, raw chunk libraries, and reference archives.
   - The production app depends solely on mirrored assets under `backend/ml_assets/`.

---

## 2. COST-GATED DECISION LADDER & DISAMBIGUATION PROTOCOL

All query processing strictly follows the multi-tier decision ladder:

```
[ User Bangla Query ]
        │
        ▼
[ Tier 0 Deterministic Precheck ] (0.32 ms, 0 LLM Cost)
   ├── Banned Chemical / Poisoning / Crisis matched ──► Instant 16123 Escalation (0 LLM Tokens)
   │
   ▼ (Pass)
[ Level 0 Fast Keyword Matcher ] (0.05 ms, 0 LLM Cost)
   ├── High Confidence Crop + Problem ──► Check Fact Base (T1/T2 0-LLM Cost) or Grounded RAG
   │
   ▼ (Missing Slots / Dialectal Phrasing)
[ Level 1 Structured NLU: google/gemini-2.5-flash-lite ] (Single JSON call, <= 180 Tokens)
   ├── Crop Identified ──► Normalized Grounded Retrieval + Generation (T3)
   │
   ▼ (Crop == NULL on Symptom / Treatment Query)
[ Interactive Clarification Intercept ]
   ├── Bangla Prompt with Quick-Reply Chips: [ ধান ] [ আলু ] [ টমেটো ]
   └── Record Partial Slot in Session & SKIP Retrieval/Generation (Saves 88% Tokens, 0% Hazard)
```

---

## 3. DEFINITION OF DONE

A task is considered complete ONLY when:
1. It runs without errors locally (`pytest` backend green, `pnpm build` frontend green).
2. It complies with the authorized model registry (Section 0) and zero-token-waste directives (Section 0.1).
3. Both paper tracks (`paper/CEA Paper/` and `paper/EACL Demo/`) and master manifests (`paper/manifest.yaml`, `experiments/results.yaml`) are updated and compiling with 0 LaTeX errors.
