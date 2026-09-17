# EACL Final — Story-Building Plan (High-Level, Before Any Drafting)

**Goal:** build the *feel* first — why a Bengali farmer's query breaks normal LLM/RAG, and why each of our stages exists out of necessity, not as a feature list.
**Rule:** no drafting, no new features. We dig problem → fix → story-feel per beat, with literature + our evidence side by side.
**Anchors:** our own `2606.29243` (benchmark: oracle still leaves 4.05–7.00% chemical hallucinations; farmer transfer unsolved; SFT reduces refusal) and `2608.14886` (retrieval: dense R@10 0.093 colloquial vs 0.970 formal; BM25 0.506→0.004 across language; Hybrid 0.539 best; passage/task config swings 7×). Plus CEA story (fluency ≠ authority, fail-closed contract).

---

## 1. Story spine (one journey, not a catalog)

> A tired farmer types half a sentence in mixed dialect, forgets the crop name, attaches a blurry leaf photo on 2G. A normal chatbot guesses — wrong crop, wrong dose, fluent Bengali. Ours narrows, asks, verifies, and if unsure, refuses + hands to 16123 + leaves an SMS that still fits in 160 chars.

Every beat below is one failure point on that journey. Paper will compress to 3 contributions; story work needs 7 beats so we can *choose* the strongest 3–5 later.

---

## 2. Seven beats (candidate — we finalize after digging)

| # | Beat (pipeline stage) | Normal failure in Bengali | Why Bengali specifically | Our necessity-fix | Our measured effect (today) | Novel angle to test |
|---|---|---|---|---|---|---|
| A | **Language gap** (colloquial query vs formal manuals) | Dense collapses, BM25 brittle | Morphology, 6 dialects, Banglish, formal docs vs spoken queries | Normalization + expansion + hybrid BM25-first with graceful dense fallback | 2608: dense 0.093 colloquial; BM25 0.506 native; Hybrid 0.539 | "Aggregate R@10 lies in low-resource" — report by register, not single score |
| B | **Missing slots** (no crop / vague symptom) | Blind RAG hallucinates cross-crop pesticide | Illiterate/short queries: "patay dag, ki dimu?" often omits crop | Cost-gated NLU halts *before* retrieval; chips resume | E09: 100/100 halted, 140/140 passed, 38.5%→0% misbinding, 88% token save | Halt-before-retrieval as *safety* primitive, not UX polish |
| C | **Cost / availability trap** (LLM for everything) | $$$, latency, offline dead | Rural 2G, no GPU, API keys die | Tiered ladder T0–T4: precheck + lightweight intent/NER first, LLM only for realization | Overhead p50 ~33.6ms BM25-only; T1+T2 deterministic; T3 stub-scoped | Each skipped LLM call = money + battery + offline survivability |
| D | **Vision as scope reducer** (photo → crop → disease) | Text-only retrieval searches whole KB | Farmer can't name disease; text alone under-specifies | Hierarchical classification-only ONNX narrows retrieval space before text search | 100% ONNX-vs-pt n=1,237; WASM 26–265ms; per-model top-1 0.90–0.94 | Photo is *retrieval filter*, not just diagnosis — prevents chemical mismatch |
| E | **Cross-modal conflict** (text says begun, photo shows potato) | Silent merge → wrong chemical | Code-switch + misnamed crops common | Explicit mismatch badge, confirm-crop before advice | E08: 68/80 = 85.0% flagged | Conflict UI as trust device for low-literacy users |
| F | **Fluency ≠ authority** (generate-then-trust) | Even oracle hallucinates dose/PHI | Numbers in Bengali digits/words mutate silently | Relational verifier on 11-slot contract; abstain/escalate on incomplete | 2606: 4–7% floor even with oracle; E03: 0.95% ASR, 6.67% Bangla-native leak vs 36.2% baseline | Verifier as *authority boundary*, LLM as *mouthpiece* — CEA thesis, demo shows it |
| G | **Last-mile + trust** (offline / SMS / 16123 / Why?) | Good advice that can't load = useless; opaque advice = distrusted | 2G, shared phones, low trust in AI, need human handoff | Deterministic 160-char GSM from certified object + SW precache + 16123 + Why/trace | BM25 0.94; SW precache true; cached 0/400 (honest); minimal 284MB | SMS as *safety-preserving compression*, not shortening; Why-panel as literacy bridge |

If beats merge later: A+B = "understanding under Bengali ambiguity", C+D = "cheap narrowing before expensive reasoning", E+F = "refuse rather than invent", G = "reach + trust". But dig as 7 first.

---

## 3. Literature angles per beat (where to dig, not what to conclude)

- **A language/retrieval:** Bengali morphology + dialect ASR/NLP; low-resource RAG eval (report-by-register); BM25 vs dense vs hybrid RRF; BGE-M3 task-config + chunk-length sensitivity; Banglish/code-switch retrieval. Start: 2608 full §3–5 + AgriTrust-RAG HF + BanSuite (EACL 2026) + low-resource RAG eval papers.
- **B ambiguity/slots:** Task-oriented dialogue slot-filling (Krishi Sathi intent+slots); clarification policy / MNC; query rewriting; cross-crop misbinding as relational error (CEA E02/E05). Start: Krishi Sathi pipeline + selective-answering under ambiguity + Farmer.Chat follow-up behaviour.
- **C cost/tiers:** Cascaded inference, FrugalGPT-style routing, edge/cloud hybrid, offline-first ICT4D; telemetry-gated ladders. Start: cost-aware LLM routing + ICT4D low-connectivity + CEA E18 ladder numbers (re-scoped, not copied).
- **D vision-scope:** Crop→disease hierarchical classification; YOLO-cls on-device; INT8 parity methodology; retrieval-space reduction via vision filter. Start: on-device INT8 reports (ours) + plant-disease vision benchmarks + multimodal RAG where image filters text search.
- **E conflict:** Cross-modal consistency / contradiction detection; human-AI deferral UI for low-literacy. Start: vision-language mismatch + clarification-UX for low-literacy (Farmer.Chat gender/literacy findings).
- **F authority/verify:** FaithfulRAG / SafeRAG / SciTrue claim-verification; dosage/PHI numeric mutation; refusal calibration; SFT-harms-refusal (2606 finding). Start: 2606 §safety + SafeRAG + FaithfulRAG + CEA verifier design (read, don't duplicate numbers).
- **G delivery/trust:** SMS compression with slot survival; PWA offline; helpline escalation; explainability-for-farmers (Why-panel, Safe Action Card); expert dual-view. Start: ICT4D SMS + PWA offline + My Climate CoPilot transparency + Farmer.Chat trust study.

Each beat gets: 4–8 must-reads, 1 table (prior claim vs gap vs our hook), verbatim failure example in Bengali + transliteration + English gloss.

---

## 4. Problem → Fix → Feel template (every beat file uses this)

```md
## Beat X — <name>
### 1. The human moment (2–3 lines, sensory, Bengali quote)
### 2. Why normal systems fail HERE (mechanism, not slogan + lit + our 2606/2608 number)
### 3. Why Bengali makes it worse (dialect/morphology/literacy/connectivity — specific)
### 4. What we built out of necessity (stage, threshold, halt/resume rule)
### 5. Why it's uniquely ours (one-line contrast vs Farmer.Chat / KrishokBondhu / Krishi Sathi / CoPilot)
### 6. Feel-line for paper (one sentence a reviewer remembers)
### 7. Evidence status (implemented / measured artifact+hash / planned — no invented numbers)
### 8. Open dig (what multi-agent research must still find)
```

Writing-feel rule: problem and fix share the same vocabulary (e.g., "scope" appears in failure *and* fix for Beat D). No essay; each beat contributes ≤3 sentences to final paper, but we write 1 page of feel now to choose from.

---

## 5. Documentation plan in `plans/` (flat, numbered, append-only)

```
plans/
  roadmap.md              — index (done, update only on scope change)
  story_plan.md           — this file (high-level digging plan)
  paper_outline.md        — 6-page budget (after beats chosen)
  problems_we_solved.md   — final 3–5 compressed rows (after beats chosen)
  beats/
    A_language_gap.md
    B_missing_slots.md
    C_cost_trap.md
    D_vision_scope.md
    E_conflict.md
    F_authority.md
    G_lastmile_trust.md
  lit/
    <beat>_notes.md       — per-beat lit table + quotes (agents write here)
```

Workflow: one beat at a time, 2–3 research agents max per beat (one lit-search, one evidence-check vs our artifacts, one story-distill). Agent output lands in `beats/` + `lit/`, never straight into paper. `problems_we_solved.md` is filled only after all 7 beats drafted — then we kill the weakest 2–4.

---

## 6. Multi-agent digging order (slow, no hurry)

1. **A + 2608 deep-read** (retrieval failure is the hook; our own paper = credibility).
2. **F + 2606 deep-read** (hallucination floor justifies verifier; CEA thesis link).
3. **B** (ambiguity — our strongest measured differentiator, E09).
4. **D + E** (vision scope + conflict — visual story for video).
5. **C + G** (cost + last-mile — deployment soul, ICT4D lit).
6. **Synthesize** → choose 3–5 beats → `problems_we_solved.md` → `paper_outline.md`.

Stop rule per beat: stop when we can state failure-mechanism + Bengali-reason + our-rule + one feel-line + evidence hash. More papers after that = diminishing returns.

---

## 7. Definition of done for story phase

- 7 beat files exist, each with Bengali example + mechanism + lit gap + our rule + feel-line + evidence status.
- `lit/` tables cite 2606 + 2608 + Farmer.Chat + KrishokBondhu + Krishi Sathi + CoPilot + BanSuite minimum.
- Explicit kill-list: which 2–4 beats/angles did NOT survive and why.
- No numbers without artifact; no new features proposed; code stays frozen.
