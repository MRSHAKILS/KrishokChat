# Bangladesh Agri-AI Capstone — Evidence-Grade Industry System Plan
*High-level architecture + evaluation-driven execution for industry-track publication*

---

## 0. The real brief (read this before touching code)

You are not just building a product in 7 days. You are building an **evidence-grade, responsible AI system**. Every technical decision below is filtered through one question: *does this provide measurable, reproducible evidence of safety and utility in low-resource settings?* For a top-tier industry track publication, rigorous evaluation, safety red-teaming, and farmer-centered design beat a simple demo. Auth, admin panels, multi-tenant DB design — actively cut those, but evaluation metrics, safety logs, and deterministic fallbacks are non-negotiable.

Your actual assets, translated into "features":
1. **RAG / retrieval benchmark work** → an "Ask your farm anything" Bengali agri-QA experience (BM25 + dense retrieval + your fine-tuned Gemma-4 4-bit).
2. **Crop classifier + specialized YOLO models** → an "upload a leaf photo → auto-detect crop → route to the right disease model → show diagnosis + confidence + treatment" flow.
3. **Evidence-backed framing** → "To the best of our knowledge, this is among the first safety-aware, grounded, multimodal Bangla agricultural advisory systems targeting smallholder farmers."
4. **Reproducible evaluation dashboard** → a panel containing dataset stats, metrics, baselines, ablations, and expert reviews to substantiate the safety claims.
5. **Real-world constraints modeling** → explicit handling of Bangla/Banglish variations, low-end devices, low bandwidth, farmer digital literacy, and pesticide safety risks.

Everything else is *proof-of-depth material* — dataset scale, model comparisons, and paper references that substantiate your claims for reviewers.

---

## 1. Tech stack (researched, current as of Aug 2026)

### Frontend — the thing investors actually judge
- **Next.js 16 (App Router) + TypeScript + Tailwind CSS v4 + shadcn/ui v3.** This is the default 2026 stack for AI-product demos for good reason: server components for instant loads, huge component ecosystem, trivial Vercel deploy.
- **Vercel AI SDK v6 + AI Elements** for the chat/QA surface — gives you streaming tokens, tool-call rendering, and message state out of the box, so your Gemma answers *type themselves out* instead of appearing after a dead pause. Perceived speed > actual speed.
- **Motion (formerly Framer Motion)** for transitions between the three demo modules — this is what separates "vibe-coded generic AI app" from something that feels designed. Page/section transitions, number count-ups for your benchmark stats, a satisfying "scanning" animation while YOLO runs.
- **To avoid the "generic AI app" look specifically:** don't use the default shadcn zinc/purple-gradient/glassmorphism combo everyone's agent tools output by default. Pick one distinctive move and commit: e.g. a warm earthy palette (soil/rice-green tones) + a real Bengali display type (Tiro Bangla / Noto Sans Bengali for UI text, not just body copy) + actual field/crop photography instead of stock icons. One strong, specific design decision reads as "designed"; five generic ones read as "template."
- **Component libraries worth pulling from** (copy-paste into shadcn, don't add as dependencies to avoid theme conflicts): **Cult UI** and **assistant-ui** — both are 2026 shadcn-based libraries built specifically for AI-product surfaces (streaming text, "agent thinking" states, tool-call cards) — exactly the vocabulary your demo needs for the QA and detection flows.

### Design workflow — this is your force multiplier given your agent setup
- **Google Stitch** (free, Gemini-powered, stitch.withgoogle.com) is genuinely the right tool for you specifically, for one reason: it now exports a **`DESIGN.md`** — an agent-readable design-system file (colors, type, spacing rules, component conventions). That's the exact bridge you need: you iterate on look-and-feel conversationally in Stitch (or with Qwen/DeepSeek for concept breakdowns), get `DESIGN.md` + exported React/Tailwind code, and hand *that* to your coding agents as ground truth so every screen your agents build afterward stays visually consistent — solving the single biggest failure mode of multi-agent vibe-coded UIs (each screen looking like a different app). Also supports multi-screen generation (up to 5 connected screens per prompt) with a shared design language, which maps directly onto your 3 demo modules + landing + results screen.
- Use Stitch → get direction + `DESIGN.md` + starter code → refine structure/logic yourself or with agents → do NOT expect Stitch output to be your final UI; treat it as a very good first draft + design contract.

### Backend — keep it boring and monolithic
- **One FastAPI service.** Not microservices, not separate deployments per model — one Python process, a few routes:
  - `POST /api/qa` — RAG + Gemma-4 answer generation (streamed)
  - `POST /api/classify` — crop classifier inference
  - `POST /api/detect` — routes to the crop-specific YOLO model, returns boxes + labels + confidence
  - `GET /api/benchmark` — serves precomputed retrieval-benchmark numbers/charts (do not compute live)
- FastAPI is the right call because it natively does async + streaming responses (needed for the token-by-token QA feel) and both your YOLO (Ultralytics/PyTorch) and Gemma inference stacks are Python-native — no need for a translation layer.

### Model serving
- **Gemma 4 (4-bit) →  llama.cpp server.** Use llama.cpp server as the primary local inference engine (rather than Ollama) to support advanced structured decoding (JSON-mode/GBNF grammars). This is critical for reliable safety classification and verifiable structured outputs. Load the model once, keep the process warm the whole session.
- **YOLO models → export `.pt` → ONNX (or TensorRT if you'll demo on an NVIDIA GPU laptop).** Ultralytics' current models report up to ~43% faster inference after ONNX export and up to 5x with TensorRT on GPU — this is the single highest-leverage performance change you can make this week for the "3-4 minutes to impress" constraint. Warm-load every crop-specific model into memory at server startup (`lifespan` hook in FastAPI) so the *first* detection isn't slow — cold model-load latency on first inference is the #1 way live ML demos die.
- **RAG index:** precompute embeddings for your demo corpus subset (don't index live) using FAISS or Chroma running in-process. No external vector DB service for a 7-day prototype — that's infra risk with zero demo value.

### Hosting for demo day — the decision that actually protects you
Given you only get 3–4 minutes and it's live in front of investors, **do not rely on a cold cloud endpoint.** Serverless GPU platforms (Modal, RunPod Serverless) are excellent for real products but carry cold-start risk (seconds to tens of seconds on first request) — unacceptable when a judge is staring at a spinner. Two safe patterns, pick one:
1. **Run fully local** on a laptop/desktop with a GPU (even a decent RTX card handles a 4-bit Gemma-4 + a couple of YOLO nano/small models fine). Zero network dependency, zero cold start, you control every variable.
2. **Rent a persistent (not serverless) GPU box** (RunPod on-demand pod) hours before your slot, load and warm everything, keep it running through your demo window, tunnel your frontend to it. Never use scale-to-zero serving live.
Either way: **have a recorded backup video/GIF of the full flow** ready to cut to instantly if wifi or hardware fails. Investors forgive a "here's the live version, and here's a recording as backup" far more than a dead demo.

---

## 2. Latency engineering checklist (do these — they matter more than any framework choice)
- Warm-load all models (Gemma, classifier, every crop YOLO) at server startup, not on first request.
- Pre-run and cache the exact demo queries/images you plan to show live, as a safety net — if live inference lags, the UI can fall back to a cached response indistinguishably.
- Stream every LLM response token-by-token — this alone makes the QA module *feel* instant even at normal token speeds.
- Keep images small (resize on upload) before hitting YOLO — most of your latency budget on detection will be image I/O, not the model.
- Build a literal **"Demo Mode"**: a short curated script of 2–3 pre-validated inputs (one QA question, one leaf photo per crop you're showcasing) that you *know* work end-to-end, rehearsed until muscle memory. Judges don't need to see you improvise — they need to see it work.

---

## 3. Using your agent stack (opencode, Antigravity, Stitch, Qwen/DeepSeek) well

You already have the right instinct — you're the architect/PM, the agents are the execution layer. Structure it like this:

1. **Ideation & breakdown (you + Qwen/DeepSeek chats):** turn this masterplan into a concrete screen list, a data-flow diagram per module, and a component inventory. This is "what" and "why" — keep it in a doc your agents can read.
2. **Visual design contract (Google Stitch):** generate your 4–5 core screens (landing, QA/chat, upload-and-detect, results/diagnosis, benchmark/research panel) as one connected multi-screen flow so they share a design language automatically. Export `DESIGN.md` + code. This file becomes the single source of visual truth for every agent from here on.
3. **Execution (Antigravity / opencode, running in parallel):** Antigravity's **Manager surface** is built exactly for this — you can spawn multiple agents in parallel (e.g., one on the FastAPI `/qa` route + Ollama integration, one on the YOLO `/detect` route, one on frontend component wiring against `DESIGN.md`), and it has a built-in browser it uses to visually verify UI work against your design reference — useful for catching the "agent drifted from the design system" problem automatically. Feed every agent the same `DESIGN.md` + a short spec of its one task; don't hand a single agent "build the whole app."
4. **Review loop (you):** your highest-value 20% of the week is reviewing agent output for visual consistency and demo-flow coherence — not writing code yourself. Budget real time for this; it's where "looks like 10 different vibe-coded apps stapled together" gets caught and fixed.

---

## 4. 7-day roadmap (direction, not tickets)

**Day 1 — Narrative + data prep, no UI yet.** Lock the exact 3-minute story arc and the exact inputs you'll demo. Pull your best pre-validated QA question(s) and 3–5 leaf images per crop (clean, high-confidence cases) into a `demo-assets/` folder. Confirm your Gemma-4 4-bit model runs in Ollama locally and responds correctly to your planned demo questions. Confirm every crop YOLO `.pt` loads and detects correctly on your chosen images.

**Day 2 — Design system.** Build your screen flow in Stitch (or v0 as a second opinion), get `DESIGN.md` + starter code. Set up the Next.js + shadcn/ui project skeleton, drop in your palette/type/tokens. This is the day everything downstream depends on — don't rush it.

**Day 3–4 — Backend + model wiring, in parallel with frontend scaffolding.** Stand up the FastAPI service with the four routes above; get real inference working end-to-end from a basic frontend (ugly is fine at this stage — function before polish). Export YOLO models to ONNX and re-benchmark speed. Get token streaming working for `/qa`.

**Day 5 — Real UI, wired to real backend.** Replace scaffolding with the actual designed screens. Add Motion transitions between modules. Add the "research/benchmark" dashboard with your precomputed stats, baselines, ablations, dataset metrics, and expert evaluation results as a rigorous evidence layer.

**Day 6 — Latency hardening + rehearsal.** Implement warm-loading, caching, Demo Mode. Run the full 3–4 minute script start to finish, timed, at least 5 times. Record the backup video. Test on the actual machine/network you'll use on demo day if at all possible.

**Day 7 — Buffer.** Something on days 1–6 will slip; this day exists to absorb it. If everything's on track, spend it purely on polish (micro-animations, copy, one more rehearsal) — not new features. New features 24 hours before a demo are how demos break.

---

## 5. Demo-day tactical notes
- Script your exact click path and time it — 3–4 minutes disappears fast once you factor in an intro sentence and transitions.
- One laptop, one browser tab, everything warm and pre-loaded before the judge sits down.
- Lead with the crop detection flow (visual, immediately legible) or the QA flow (shows language + reasoning depth) depending on which lands better with a non-technical audience in your rehearsals — test both orders on a friend and see which gets a stronger reaction.
- Close on the "first in Bangladesh" research credibility slide/panel — that's your differentiation vs. anyone can wrap an API in a chat UI.

---

## 6. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Live model inference lags on stage | Warm-loading + Demo Mode cached fallback + rehearsed curated inputs |
| Wifi/venue network fails | Run fully local, or tunnel to a pre-warmed persistent GPU box, plus a recorded backup video |
| UI looks "AI-generated generic" | One committed design decision (palette/type/imagery) via Stitch's `DESIGN.md`, enforced across all agent output |
| Multi-agent output is visually inconsistent | Single shared `DESIGN.md` fed to every agent; you review for drift, not code correctness |
| Scope creep (auth, admin panel, etc.) | Explicitly out of scope — say so out loud if a judge asks; frame as "deliberately deferred for a working prototype" |
| Agents get stuck on a subtask | Keep tasks small and single-purpose per agent; don't hand off ambiguous multi-step work |

---

*This is direction, not implementation. Next step: turn Section 4 into day-by-day sub-tasks with your Qwen/DeepSeek breakdown sessions, then hand those to your agents with `DESIGN.md` as their shared reference.*