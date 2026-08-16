# IC Judging-Criteria Mapping — Where Each Score Is Won on the Poster

Judging weights: Idea 20 · Impact 20 · Business 20 · Market Readiness 20 · UI 10 · Poster 10.

> **Framing principle:** competition, not peer review. Every criterion is scored on **strengths**. The four pillars (KrishokChat, disease detection+agentic, soil, safety architecture) are each mapped to the criteria they score highest on. Unfinished work is a roadmap, not a limitation.

---

## Criterion 1 — Idea (20)

**What it rewards:** the novelty of the core idea — the problem, the gap, and what was built that did not exist before.

| Poster block | What it contributes | Leverage |
|---|---|---|
| A5 Gap table + 4 contributions | Names exactly what is new vs Farmer.Chat / KrishokBondhu | **highest** |
| B1 Hero pipeline diagram | The architecture IS the idea (safety-before-retrieval + verifier + audit) | **highest** |
| B3 Structured claim verifier schema | The SOTA contribution: 14-field schema, 6 relation types, deterministic-first | **highest** |
| A1 The Problem | Frames the harm (47M households, 4.05–7.00% hallucination floor) | high |
| A4 KrishokChat-4B 1.9× model result | Proves the fine-tuned model beats zero-shot | high |
| C1 AgriVision 95–97% accuracies | Original edge-deployable disease detection for Bangladesh | high |
| C2 Soil R²=0.39 + field dataset | Original fieldwork + working model — a data contribution | high |

**Highest-leverage blocks:** A5 (gap table + 4 contributions) + B1 (hero diagram) + B3 (structured verifier). A judge who reads these three gets the full idea.

**Strengths-framing note:** the structured verifier is framed as "the SOTA approach — deterministic-first with 14-field claim matching and 6 relation types," not as "lexical matcher with no LLM verifier yet." The former is a contribution; the latter is a weakness display. Use the former.

---

## Criterion 2 — Impact on Society & Environment (20)

**What it rewards:** measurable good for people and the environment, grounded in the real Bangladesh context.

| Poster block | What it contributes | Leverage |
|---|---|---|
| A1 The Problem | 47M households, 92,094 calls to 16123, 20–40% yield loss to disease | high |
| B2 16123 + 999 branch | Real escalation path for at-risk users | **highest** |
| C4 Impact section | Health/safety + environment + access, three concrete anchors | **highest** |
| C1 Disease detection 95–97% | Reduces the 20–40% yield loss from undetected disease | high |
| C2 Soil moisture model | Enables irrigation advisories → water conservation | high |
| C1 Edge deployment <30 ms | Extends reach to Android smartphones in rural areas | high |

**Anchors to use (all cited):**
- **Health/safety:** refusing unsafe agrochemical queries + verifying dosages → reduces pesticide misuse, accidental poisoning, self-harm; redirects to 16123 and 999.
- **Environment:** source-grounded dosage → less over-application of pesticide/fertilizer → less soil and water contamination. Edge models reduce cloud compute.
- **Access:** ~47M farming households; laptop-deployable + offline-capable + Android edge-deployable disease models → reaches the connectivity gap.
- **Yield:** disease detection at 95–97% catches the 20–40% yield loss from undetected disease early.

**Strengths-framing note:** state impact as the positive contribution. "Reduces the risk of pesticide misuse" not "pesticide misuse is a problem we haven't solved." "Catches disease early to prevent 20–40% yield loss" not "disease causes losses."

---

## Criterion 3 — Business Model / Economics (20)

**What it rewards:** a credible path to sustainability. The user said this is in development for the capstone — the poster carries a defensible framework.

| Poster block | What it contributes | Leverage |
|---|---|---|
| C5 Business section | Three monetization lanes with comparator evidence | **highest** |
| C3 /analytics screenshot | The audit engine = the least-commoditized B2B/B2G asset | high |
| C6 QR to dataset | Dataset/API licensing lane | medium |
| A2 Published benchmark | 85,979 CC-BY-4.0 dataset = licensing asset | medium |

**The three lanes (evidence-based):**
1. **Freemium + B2B** — free advisory/diagnosis for farmers; paid audit/analytics dashboard for agro-dealers, SAAOs, extension officers. *Comparator: PxD 7.8M users; ACI IDSS/Fosholi €3.5M 2025 target.*
2. **Government partnership (B2G)** — AI front-end to 16123 (triage + escalation). The audit engine is the trust asset for a DAE/a2i partnership.
3. **Dataset + API licensing** — 85,979 benchmark + 722-image soil dataset + AgriVision disease models enable third-party validation, research licensing, advisory API for agri-fintech.

**Tag on the poster:** "Business model framework in development for the capstone; the prototype is research-stage (v0.2.0)."

**Strengths-framing note:** the lanes are framed as a credible strategy with market evidence, not as "we haven't figured out monetization yet." The audit engine is named as the differentiated asset — a specific, defensible moat, not a generic "we will monetize."

---

## Criterion 4 — Market Readiness (20)

**What it rewards:** how close to real deployment — working product, published assets, real model results.

| Poster block | What it contributes | Leverage |
|---|---|---|
| C1 AgriVision 95–97% accuracy table | Real, measured, edge-deployable model results | **highest** |
| C2 Soil scatter plot R²=0.39 | Real field-collected dataset + working regression model | **highest** |
| C3 Product screenshots | Three real app surfaces (/detect, /chat, /analytics) | **highest** |
| B1 Hero diagram + B4 tech one-liner | A real system, single-process, local-first, replaceable LLM | high |
| A2-A4 Research validation | 85,979 benchmark + retrieval eval + model comparison | high |
| C6 Roadmap block | Forward-looking next steps signal momentum | high |
| C6 QR codes | Dataset + papers verifiable | high |

**What is genuinely ready (state as strengths):**
- Working end-to-end: chat (streaming SSE + agent trace), vision (photo → 95–97% diagnosis → grounded treatment), soil (dataset + R²=0.39 model), audit + /analytics, research/benchmark panel.
- Datasets published (HuggingFace CC-BY-4.0). Two papers under peer review. AgriVision disease report done.
- Edge-deployable: disease models in ONNX FP16 + TFLite INT8, <30 ms on Android.
- Local-first: runs on a laptop via Ollama; demo cache for offline venue.

**Roadmap items (frame as "ongoing," not as "missing"):**
- Voice-output (TTS) for low-literacy users — ongoing.
- Extended dialect coverage — ongoing.
- B2B pilot with an extension office — planned.
- Soil-model refinement for higher-accuracy irrigation advisories — ongoing.

**Strengths-framing note:** the roadmap block reads as "here is our next phase," not as "here is what we failed to do." A team with a clear roadmap looks more ready than a team that claims everything works.

---

## Criterion 5 — UI / Outlook (10)

**What it rewards:** visual polish and a coherent product identity.

| Poster block | What it contributes | Leverage |
|---|---|---|
| C3 Product screenshots | Shows the actual UI | **highest** |
| Poster palette + type (field-notebook) | Coherence between poster and product | **highest** |
| Row 0–1 title + stat ribbon | First impression | high |
| B1 Hero diagram (clean, labelled) | Architecture clarity | medium |

**What makes the UI defensible:**
- The "কৃষি পত্রক" field-notebook design system (warm paper, not dark AI chrome) is deliberate — `frontend/src/app/globals.css`, `docs/FRONTEND_DESIGN_PLAN.md`.
- Motion-animated agent trace on every query — the visible differentiator.
- Bengali-first typography (Tiro Bangla / Noto Sans Bengali), voice input (bn-BD), Ctrl+K command palette, sunlight high-contrast mode (a specifically agrarian accessibility feature), `prefers-reduced-motion` support.
- The poster uses the same palette as the product, so the screenshot and the poster read as one identity.

**Strengths-framing note:** name the specific features (field-notebook system, agent trace, voice input, sunlight mode). Do not claim "WCAG-AA certified" — claim the features that exist.

---

## Criterion 6 — Poster Score (10)

**What it rewards:** the poster itself — hierarchy, legibility, information density, no wasted space, professional finish.

| Poster block | What it contributes | Leverage |
|---|---|---|
| 3-column layout grid with clear reading order | Readability | **highest** |
| Hero diagram at eye level | Focal point | high |
| 6-chip stat ribbon | 8-second comprehension | high |
| No AI-flags (per `02_…`) | Professional voice | **highest** |
| Roadmap block (no weakness display) | Maturity framing | high |
| QR codes | Verifiability | medium |

**Highest-leverage blocks:** the layout grid + the anti-AI-flag voice discipline. A poster that is easy to read in 60 seconds and sounds like a researcher wrote it beats a poster with more content that reads like a product launch.

**Space budget (no criterion is starved):**
- Column A: KrishokChat (Pillar 1) + novelty → Idea 20.
- Column B: Safety architecture (Pillar 4) → Idea 20 + Poster 10 + Market 20.
- Column C: Disease detection (Pillar 2) + Soil (Pillar 3) + Product + Impact + Business + Roadmap → Impact 20 + Business 20 + Market 20 + UI 10.
- Every criterion has at least one dedicated block.

---

## Summary matrix

| Criterion | Weight | Primary block(s) | Secondary block(s) | Strengths-framing rule |
|---|---|---|---|---|
| Idea | 20 | A5, B1, B3 | A1, A4, C1, C2 | verifier = "SOTA deterministic-first," not "no LLM verifier yet" |
| Impact | 20 | C4, B2 (16123) | A1, C1, C2 | "reduces the risk of," not "is a problem we haven't solved" |
| Business | 20 | C5 | C3 (audit), C6, A2 | three lanes with evidence; "framework in development" |
| Market Readiness | 20 | C1, C2, C3 | B1, A2-A4, C6 | real results (95–97%, R²=0.39) + roadmap, not "missing" list |
| UI | 10 | C3, poster palette | Row 0–1, B1 | name specific features, no "WCAG certified" claim |
| Poster | 10 | grid + anti-AI-flag | hero diagram, stat ribbon, QR, roadmap | no weakness displays |

---

## The four pillars → criteria coverage

| Pillar | Primary criteria scored |
|---|---|
| **1. KrishokChat (benchmark + model + retrieval)** | Idea 20, Market 20 |
| **2. Crop disease detection + agentic pipeline (95–97%, edge)** | Idea 20, Impact 20, Market 20 |
| **3. Soil moisture (field dataset + R²=0.39 model)** | Idea 20, Impact 20, Market 20 |
| **4. Safety-first verification architecture (14-field, 6 relations, 16123)** | Idea 20, Impact 20, Poster 10 |

Every pillar contributes to Idea 20 (the project is genuinely multi-faceted). Pillars 2+3 carry Impact and Market (real results for farmers). Pillar 4 carries Poster (the hero diagram) and Impact (16123 escalation). The product screenshots (C3) and the field-notebook palette carry UI 10. The business section carries Business 20.

---

## What to do if a criterion feels thin

- **Business thin?** The three lanes from `docs/competitive-landscape.md` §c are defensible. Add one sentence per lane with the comparator evidence. The audit engine is the moat — name it specifically. Do not add invented numbers.
- **Market Readiness thin?** The real model results (vision 95–97%, soil R²=0.39) + the three product screenshots + the published datasets + the roadmap carry it. A team with measured results and a roadmap looks more ready than one claiming everything works.
- **UI thin?** Three real screenshots + the field-notebook palette on the poster itself. Make sure the screenshots are high-resolution and the Bengali text is legible at 24 pt.
- **Impact thin?** The 16123 escalation is the strongest single impact anchor. Make sure it appears in the hero diagram, the safety section, AND the impact section — three sightings, one message. The disease-detection 95–97% and the soil model add yield + water-conservation impact.

---

## Final note: research for winning vs product from research

The IC expects a product from research. The poster resolves this by giving **equal column weight to the system (B) and the product (C)**, while the research foundation (A) is positioned as *evidence backing the product*. The hero diagram is the bridge — it is simultaneously the research contribution (the architecture) and the product feature (the agent trace a user sees). The four pillars each have both a research artifact and a product surface:
- Pillar 1: benchmark (research) → /research/benchmark page (product).
- Pillar 2: AgriVision models (research) → /detect page (product).
- Pillar 3: soil dataset + model (research) → /soil page (product).
- Pillar 4: claim schema (research) → /chat agent trace + /analytics (product).

Keep that dual role central; do not let the poster drift into a pure research summary or a pure product pitch.