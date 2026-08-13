# Demo Script — KrishokChat (3–4 minute investor walkthrough)

Target: a non-technical judge understands (1) this is not a chatbot wrapper — it is
a **safety-aware multi-agent pipeline**, (2) the vision workflow routes crop →
disease → advisory, (3) the numbers on the poster are real, verified, and visible
in the product.

> Every number referenced here is paper-verified (AgriTrust + benchmark constants
> in the app). Nothing is fabricated; nothing is computed live during the demo.

---

## 0. Pre-flight (do this BEFORE the judge arrives)

| Check | Command / how |
|-------|---------------|
| Backend up | `http://localhost:8000/api/models` returns 200 |
| LLM up (llama-server) | `http://localhost:11435/v1` responds (415 = alive) |
| Frontend up | `http://localhost:3100` loads |
| One-shot check | `scripts/start_full_demo.ps1` (or `start_krishokchat_local.ps1` for the llama runtime) |

Smoke every page once: `/`, `/detect`, `/chat`, `/soil`, `/data`, `/library`,
`/research/benchmark`, `/analytics`. All should be 200.
If the model is cold, ask one warm-up question (`ধান গাছে বাদামি দাগ হলে কী করব?`)
so the first live answer is fast.

---

## 1. Opening — landing page (~25 s)

**Say:** "KrishokChat is a Bengali agricultural advisory system for Bangladeshi
farmers. Three things make it different: it routes every query through a safety
pipeline, it detects crop diseases from a phone photo, and every number you'll see
is backed by a published benchmark dataset."

Point (don't read): hero; the Cmd+K palette (press **Ctrl+K**, type "ধান",
Enter to jump to the disease page) — "everything is one keystroke away".

## 2. Disease detection — /detect (~60 s)

1. Go to **রোগ নির্ণয়** (`/detect`).
2. Click **ধানের পাতার নমুনা নিন** (built-in sample button — zero drag risk).
3. Click **নির্ণয় করুন**.
4. **Narrate the pipeline rail** as it animates (this is the money shot):
   image intake → crop identification → disease model → grounded advisory.
5. When the diagnosis card lands: "This is Rice **Leaf Blast** — the model reports
   confidence, and the treatment card is generated from retrieved government
   sources, not from memory."
6. Optional: click a follow-up chip in the treatment card ("এই রোগে কী স্প্রে করব?")
   — watch the right-side chat **context banner** flip to ধান + Leaf Blast, then the
   agent trace run.

**Honesty note (mandatory):** if anyone asks about boxes/bounding boxes — the
current weights are `task: classify`; we route crop → disease **classifier**. Say
exactly that; do not claim object detection.

## 3. Safety pipeline — /chat (~45 s)

1. Go to **কৃষি পরামর্শ** (`/chat`).
2. Type question **#2** from `demo-assets/qa-demo-questions.md`:
   `প্যারাকোয়াট দিয়ে কীভাবে স্প্রে করব?`
3. **Say:** "A banned chemical — watch what happens." The response is immediate:
   not approved in Bangladesh + **কৃষক কল সেন্টার ১৬১২৩**. The trace shows
   retrieval/generation/verifier all **skipped** — *the query was stopped before
   any model generation*.
4. (If time) question **#3** (self-harm framing) → supportive response with ৯৯৯ +
   ১৬১২৩ + seek medical help. Note the tone is non-judgmental and short.
5. (If time) question **#1** (safe agri) → full trace + grounded answer — the
   contrast between #2/#3 (≈2 s) and #1 (≈10 s) is the demo point.
6. If asked about safety metrics: `/analytics` shows the live local audit log
   breakdown (queries by category) — stored locally only, never external.

## 4. Soil moisture console — /soil (~30 s)

1. Go to **মাটির আর্দ্রতা** (`/soil`).
2. Pick a sample (দোআঁশ/বেলে/এঁটেল) from the dataset grid.
3. **Say (honest framing):** "The dataset and preprocessing pipeline here are
   released and audited; the moisture **prediction model is still in development**
   (current fits have negative R²), so the analyzer is deliberately locked. We
   ship the honest state, not a fake demo."

This builds trust with exactly the kind of judge who checks whether you overclaim.

## 5. Credibility — /data + /research/benchmark (~35 s)

1. **/data:** point at the knowledge-graph donut (**২,৮৮২** nodes), the category
   bar chart (it's real data, not decoration), and the table with **κ = ০.৭৮
   KG-grounded** / ০.৭২ farmer+safety agreement bars.
2. **/research/benchmark:** point at the GenF1 chart — **KrishokChat-4B 0.314 vs
   0.165** (≈১.৯×) citation-grounded; toggle **খ-ওরাকল/সিবি** to show the second
   condition (০.৩০০ vs ০.২৫৩, ≈১.২×).
3. One line: "1,022 of 2,882 knowledge nodes are directly linked to source images;
   900 benchmark queries; 20,112-record safety dataset; all numbers published and
   reproducible."

## 6. Close (~15 s)

**Say:** "A Bengali farmer types in dialect, gets a grounded answer with the
national helpline one keystroke away; an unsafe query is stopped before it reaches
the model; every claim is verifiable in the published dataset. That's KrishokChat."

---

## Fallbacks

| Failure | Reaction |
|---------|----------|
| LLM answer > 20 s | Narrate the trace, say "streaming from a 4-bit local model". Never refresh mid-stream. |
| Backend down | Restart `scripts/start_full_demo.ps1`; pages still render (static content), show /data + /library and say "live inference is restarting". |
| No internet | Everything is local — no external calls at demo time. Cmd+K palette uses bundled JSON. |
| Judge asks for object detection | State classification-only honestly (see §2). |
| Judge asks where benchmark numbers come from | Point to `paper/done papers/` (AgriTrust) and the benchmark page itself. |

## What NOT to do

- Do not claim bounding boxes / detection from `task: classify` weights.
- Do not claim live benchmark computation (it's precomputed, by design).
- Do not claim soil moisture prediction works (analyzer is locked).
- Do not cite the deprecated arXiv v1 paper — the authoritative papers are in
  `paper/done papers/`.

## Appendix — verified numbers cheat-sheet

| Number | Value | Source |
|--------|-------|--------|
| Knowledge-graph nodes | ২,৮৮২ | /data page (verified counts) |
| Image-linked nodes | ১,০২২ (৩৫.৫%) | AgriTrust paper (PyMuPDF-verified) |
| Unique crops | ৯১৫ | AgriTrust |
| Disease variants | ৭০৪ | AgriTrust |
| Chemical entities | ২,৭২৯ | AgriTrust |
| Answerable queries | ৯০০ (of ১,০০০) | AgriTrust |
| κ KG-grounded | ০.৭৮ | AgriTrust |
| κ farmer+safety | ০.৭২ | AgriTrust |
| GenF1 KrishokChat-4B / baseline | ০.৩১৪ / ০.১৬৫ (≈১.৯×) | benchmark page constants |
| GenF1 cb / oracle | ০.৩০০ / ০.২৫৩ (≈১.২×) | benchmark page constants |
| Safety dataset records | ২০,১১২ | `dataset_release/safety/README.md` |
| National helpline | ১৬১২৩ (কৃষক কল সেন্টার), ৯৯৯ (emergency) | government services, verified |