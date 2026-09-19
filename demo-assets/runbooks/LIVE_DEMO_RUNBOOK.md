# Live Demo Runbook (3–4 minutes)

Order matters: open with the strongest, most visual proof, keep the agent
trace visible, and end with the business story.

## 0. Pre-flight (before the reviewer arrives)
1. Backend: `uv run uvicorn app.main:app --port 8000` in `backend/`
   (or `scripts/start_krishoktech_local.ps1` for the local-model lane).
2. Frontend: `pnpm dev` in `frontend/`.
3. Confirm the demo cache loads: `demo-assets/cached_responses.json` must exist
   (21 curated entries, corpus-versioned keys) — it makes the demo resilient to
   LLM outages.
4. Health: `curl http://localhost:8000/health` → `{"status":"ok"}`.
5. Have `demo-assets/images/` and `demo-assets/screenshots/` ready as fallbacks.

## 1. Landing + framing (15 s)
Open `/`. Read the hero: a Bengali agri assistant with a **safety-aware agent
pipeline** — not a chatbot wrapper.

## 2. Grounded Q&A with the agent trace (45 s) — THE core
1. Go to `/chat`, type: `ধান গাছের পাতায় বাদামি দাগ দেখা দিয়েছে, কী করব?`
2. Point at the stepper: Checking safety → Retrieving sources → Generating →
   Verifying. Explain each agent one line.
3. Show the answer's sources and the confidence badge. Note retrieval is
   precomputed BM25 + BGE-M3 (2,135 nodes) — nothing scraped live.

## 3. Safety refusal (30 s)
Type: `প্যারাকোয়াট দিয়ে কীভাবে স্প্রে করব?` — instant refusal, 16123
referral, and the trace shows retrieval/generation/verifier SKIPPED.

## 4. Image diagnosis (45 s)
1. `/detect`, click the built-in rice sample (or drag `images/rice/leaf_blast.jpg`,
   crop hint = ধান).
2. Show the classification result + treatment card with the verifier stamps.
3. Honesty line: *"These are classification models; the crop is declared by the
   farmer and routed to the matching disease model. No bounding boxes are
   claimed."*

## 5. Soil (30 s)
`/soil`: dataset overview (722 images, 0.0–21.5 kPa, Pabna) — then the honest
boundary: *"The dataset is released; the regression predictor stays in
development, so the analyzer is locked. No fabricated readings."*

## 6. Safety metrics + benchmark (30 s)
`/analytics`: category breakdown from the **local audit log only**.
`/research/benchmark`: precomputed stats, never computed live.

## 7. Business (20 s)
`/business`: unit economics (0.02 BDT per answer), farmer-vs-premium tiers.

## Failure fallbacks
- LLM down → cached demo questions still answer (outage replay); everything
  else fails closed with the 16123 referral — say: *"That's the fail-closed
  behavior working as designed."*
- Screenshots in `demo-assets/screenshots/` cover every stage if the live
  stack fails entirely.