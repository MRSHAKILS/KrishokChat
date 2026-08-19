# KrishokChat — Updated 3–4 Minute Judge Showcase

**Narrative:** field discovery → service gap → baseline failure → research assets → product → market path.

**Target duration:** 3:35–3:55 at a calm pace.

**Roles:**

- **Presenter:** speaks continuously and faces the judges.
- **Laptop operator:** changes only the prepared tabs/actions listed below. The operator does not explain or debug.
- **Second teammate:** stands near the poster and points only when the presenter references research evidence or business readiness.

---

## Pre-demo setup

Open these tabs in this exact order:

1. `/` — landing page.
2. `/data` or `/research/benchmark` — research/data evidence.
3. `/chat` — unsafe-query preset ready: `প্যারাকোয়াট দিয়ে কীভাবে স্প্রে করব?`
4. `/chat` — a preloaded or prewarmed grounded answer to: `ধান গাছের পাতায় বাদামি দাগ দেখা দিয়েছে, কী করব?`
5. `/detect` — rice or potato sample already selected; analysis not yet started.
6. `/analytics` or `/business` — use whichever is most visually stable on the final demo machine.

Before judges arrive:

- warm the local model;
- verify the unsafe query still returns a terminal refusal;
- verify the safe answer has sources and a completed trace;
- verify the chosen image reaches the expected crop-specific classifier;
- keep the four-page brochure beside the poster, not in the presenter’s hands.

---

## Timed script with live cues

### 0:00–0:35 — We started in the field

**Laptop:** show the landing page. If the page includes the fieldwork/data story, keep it visible. Otherwise, the second teammate points to the field photograph on the poster.

**Presenter:**

> “We did not begin this project by deciding to build a chatbot. We began by speaking with farmers.
>
> We collected 300 questions through face-to-face interviews in Rajshahi and Natore, then added questions farmers had already asked in Facebook groups and the Krishi Bangla portal. Together, that gave us 1,000 real farmer questions.
>
> The same problems kept appearing: crop disease, chemical use, incomplete or confusing advice, irrigation decisions, and difficulty reaching an expert when the farmer actually needed one.”

### 0:35–0:58 — Why an application was necessary

**Laptop:** remain on the landing page. Second teammate points to the 16123/problem section of the poster.

**Presenter:**

> “Bangladesh already has agricultural officers and the 16123 Krishi Call Center, but human capacity is limited. The call center handled 92,094 calls in the last reported financial year. Our question became: can AI answer routine questions safely, and pass uncertain or dangerous cases to people?”

### 0:58–1:35 — Why a normal LLM was not enough

**Laptop:** switch to `/data` or `/research/benchmark`. Show the benchmark/model evidence, not a dense table of all results.

**Presenter:**

> “Before building the application, we tested that assumption. The best listed zero-shot baseline reached only 0.165 token-F1 on our Bengali general-QA evaluation. More importantly, even when models were given the correct evidence, chemical hallucination remained between 4.05 and 7 percent.
>
> Fine-tuning improved our 4-billion-parameter model to 0.314 token-F1, but the standalone model followed the intended safety behavior on only 0.31 percent of the tested safety items. That result changed our design: the language model could write an answer, but it could not be the safety system.”

### 1:35–1:58 — Research became the product foundation

**Laptop:** keep the data/benchmark page visible. Second teammate points to the research-foundation section of the poster.

**Presenter:**

> “We also could not find a Bangladesh-focused resource matching what we needed: farmer-language questions linked back to authoritative agricultural evidence. So we built one—85,979 benchmark instances across four tracks, grounded in 284 publications, plus the independent 1,000-query farmer benchmark.
>
> Then we studied retrieval itself. Dense retrieval was strong on formal safety language but fell sharply on colloquial farmer questions. Hybrid RRF performed best overall, while BM25 remained a strong, lightweight local path. The product now uses hybrid retrieval when the dense channel is available and automatically falls back to BM25 when it is not.”

### 1:58–2:22 — Live moment 1: dangerous query stops immediately

**Laptop:** switch to the unsafe-query `/chat` tab and submit the prepared paraquat question. Do not type it live if a preset is available.

**Presenter:**

> “Now watch what happens when a farmer asks how to spray paraquat. Safety runs first. The query is blocked before retrieval, generation, or verification, and the farmer is redirected to the real Krishi Call Center at 16123. The skipped stages are visible in the trace, and the decision is written to the local audit log.”

Pause for one second so the judges can see the skipped stages.

### 2:22–2:42 — Live moment 2: a normal question follows the full path

**Laptop:** switch to the preloaded grounded-answer tab. Point the cursor at the trace and then the source chips. Do not scroll repeatedly.

**Presenter:**

> “A normal crop question follows a different path: safety, retrieval from Bangladesh-focused sources, Bengali answer generation, and a dosage verifier. The runtime checks dosage-bearing claims against the retrieved passages, while our research schema represents fourteen fields such as chemical, formulation, amount, unit, interval, safety period, and source. Unsupported dosage claims are removed or flagged instead of being presented as confident advice.”

### 2:42–3:05 — Live moment 3: photo to crop-specific model

**Laptop:** switch to `/detect` and start the prepared sample. Let the pipeline rail animate. Stop scrolling when the diagnosis and advisory card are both visible.

**Presenter:**

> “For a farmer who cannot describe the disease, we use the photo route. The system checks image quality, identifies or confirms the crop, and routes the image to a crop-specific disease classifier. This is classification—not bounding-box detection. Smaller, specialized models reduce size and computation, and the deployment design can download only the crop model a farmer needs. The diagnosis then enters the same grounded advisory path instead of producing treatment from the image model alone.”

If the result is visible quickly, add:

> “Four crop-specific held-out evaluations are in the 95-to-97 percent top-1 range; the current wheat live sweep is 88 percent.”

### 3:05–3:22 — Irrigation and field sensing

**Laptop:** keep the diagnosis visible, or switch briefly to `/soil` only if that page is already open and stable. Do not run the analyzer.

**Presenter:**

> “We followed the same field-first process for irrigation. In Pabna, we collected 722 soil photographs paired with tensiometer readings from 0 to 21.5 kilopascals. Today, the released contribution is the field dataset and its leakage-checked split; the prediction model remains a development lane rather than a claim we hide behind the demo.”

### 3:22–3:47 — Business, market readiness, and close

**Laptop:** switch to `/business` or `/analytics`. Show the three institutional lanes or the audit dashboard. Second teammate points to the market section of the poster.

**Presenter:**

> “Our farmer service remains free, because smallholders are not the right primary payer. The business has three institutional paths.
>
> First, B2G: routine-question triage and auditable escalation around 16123. Second, B2B: advisory and district-level analytics for extension teams, NGOs, agro-dealers, and seed companies. Third, licensed datasets and an advisory API for research and agricultural services.
>
> Under the stated API-token assumption, one model answer costs about two paisa. The working system already has the web application, safety boundary, local audit, precomputed retrieval assets, model fallback, health checks, rate-limit controls, and a production start path. The next step is not an unsupervised national launch; it is a supervised district-level pilot with agricultural experts.
>
> We started with farmers’ questions, turned the gaps into research, turned the research into architecture, and turned that architecture into a working product. That is KrishokChat.”

Stop. Do not add another summary.

---

## The five points the judges must retain

1. **Field-first:** 300 face-to-face interviews within a 1,000-query farmer benchmark.
2. **Research-backed:** baseline failure led to an 85,979-instance provenance-traced resource and retrieval study.
3. **Safety boundary:** unsafe queries stop before retrieval; the model is not trusted as the safety mechanism.
4. **Practical product:** Bengali Q&A, crop/disease classification, grounded advisory, local audit, and lightweight fallback paths.
5. **Credible market path:** free for farmers; paid institutional triage, analytics, and data/API services; supervised pilot next.

---

## Delivery rules

- Say “classification,” never “object detection.”
- Say “hybrid when available, BM25 fallback,” never “BM25 only” as a description of the current configured architecture.
- Attribute 0.31% to the **standalone fine-tuned model’s tested safety behavior**, not to the full safety-routed application.
- Do not say the current runtime checks all fourteen schema fields. The runtime checks dosage-bearing claims; the research schema defines fourteen structured fields.
- Say the soil **dataset** is released; do not present soil prediction as deployment-ready.
- Say “ready for a supervised pilot,” not “ready for autonomous national deployment.”
- If a page fails, point to the matching brochure panel and continue. Never troubleshoot in front of judges.
