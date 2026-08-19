# KrishokChat — Judge Presentation Script (3–4 minutes)

Read this almost word-for-word. It is engineered against the exact rubric:
**Idea 20 · Impact 20 · Business/Economics 20 · Market Readiness 20 · UI 10 · Poster 10.**

Timing: **~3:30 speaking + demo woven in.** Every line is doing rubric work — the tag in
[brackets] tells you which score it targets. Do NOT read the brackets aloud.

Golden rule for delivery: **slow down, say fewer things, land the three numbers** —
`0.02 taka`, `16123 / 92,094 calls`, `95–97% + <30 ms offline`. If you forget everything
else, those three win points.

---

## SECTION 0 — THE ONE-LINE OPENER (0:00–0:15)  [Idea]

Stand, one breath, then:

> "Forty-seven million farming families in Bangladesh, and almost no advisory in their own
> language. The ones online just get a generic chatbot — which will happily tell a farmer
> the wrong pesticide dose. **KrishokChat is a Bengali farming assistant that is built to
> refuse to be dangerous.** May I show you?"

Then open the site. Keep talking while it loads. Don't wait in silence.

---

## SECTION 1 — WHY OURS IS DIFFERENT (0:15–0:50)  [Idea, Market Readiness]

> "Everyone builds an agriculture chatbot. Three things make ours different, and all three
> are things nobody else in Bangladesh has done together.
>
> **One — it's grounded.** Every answer traces back to a real government source — BARC,
> BARI, BRRI, the extension department — through a knowledge graph of **2,882 nodes** built
> from **284 real publications**. It is not guessing from the open internet.
>
> **Two — we trained our own model, and it runs on the phone.** We didn't just wrap
> ChatGPT. We fine-tuned our own 4-billion-parameter Bengali model, and the disease models
> are small enough to run **offline, on a mid-range phone, in under 30 milliseconds.**
>
> **Three — we did the fieldwork nobody does.** We went to Pabna and collected **722 real
> soil photos** with instrument readings, and we collected **1,000 real farmer questions**,
> 300 of them from face-to-face interviews in Rajshahi and Natore. That's real Bangladesh
> data, not scraped text."

*(This is your novelty block. Say it with confidence — this is where you separate from the
20 other agri projects.)*

---

## SECTION 2 — LIVE DEMO (0:50–2:10)  [UI 10, Idea, Impact]

Do these THREE moves only. Do not wander the site. Narrate what the judge sees.

### Move 1 — the safety refusal (the money shot) [Impact]
Type or click a preset unsafe query (a banned/overdose pesticide question).

> "Watch what happens when I ask something dangerous. See the trace at the top —
> **it checks safety *before* it even retrieves anything.** It refuses to give the dose,
> and instead it points the farmer to **16123, the real national Krishi Call Center**. No
> other chatbot here does that. Safety comes first, and it's free for everyone — you never
> pay to be kept safe."

*Let the agent-trace animation play. That stepper is your UI score — point at it.*

### Move 2 — a normal grounded answer [Idea, UI]
Ask a real crop question (rice/potato disease or fertilizer).

> "Now a normal question. Same trace — safety, then it retrieves from the grounded sources,
> the model answers in Bengali, and a **verifier checks the answer against the sources
> before the farmer sees it** — especially any chemical dose. Fourteen fields checked. If
> the evidence isn't there, it refuses rather than guess."

### Move 3 — disease photo [Market Readiness, Idea]
Go to /detect, upload a leaf photo.

> "And a farmer can just take a photo. It identifies the crop, routes to a small
> crop-specific model — **95 to 97% accuracy** — and returns the treatment in Bengali,
> grounded in our library. This whole model is **6 megabytes and runs on the phone offline**
> — which matters, because rural internet reaches under half of farmers."

*(If a demo step fails: don't panic, say "I'll show you the result on the poster" and move
on. Never debug live.)*

---

## SECTION 3 — BUSINESS MODEL & ECONOMICS (2:10–3:00)  [Business 20, Market Readiness 20]

**This is the section most teams fumble. You will not, because you have real numbers.**

> "Now the business — and I'll be practical, not theoretical.
>
> **We run two tiers.** The **free tier answers from our grounded database directly — no AI
> model runs — so it costs us almost nothing.** Every farmer gets that, forever. It's the
> social product.
>
> The **paid tier runs the actual LLM.** And here's the real cost, which I checked this
> week: answering one question with the model costs us about **two paisa — 0.02 taka.**
> If we host our own model on a rented GPU, **one 4090 at about 500 US-dollars a month
> serves over ten million questions.** So the AI cost is genuinely not the problem.
>
> **But we don't make farmers pay — that model has failed before.** ACI's Fosholi has 2.6
> million users and gives farmer advice away free; they earn from businesses. So do we.
>
> **Our money comes from three places.** One: the **government** — the Krishi Call Center
> took **92,000 calls last year** with a handful of operators; we sit in front of it as an
> AI triage-and-safety layer and only escalate the hard cases. Two: **agro-dealers and seed
> companies** buy our analytics dashboard — what are farmers in each district asking, which
> diseases are spiking. Three: we **license our datasets** — the 86,000-instance benchmark
> and the soil dataset — which no one else in Bangladesh has.
>
> So the free tier is a public good that costs us nothing, and we earn from the people who
> can actually pay."

*(That paragraph hits Business AND Market Readiness. The "0.02 taka" and "$500 serves 10
million" lines are your credibility spikes — say them slowly.)*

---

## SECTION 4 — IMPACT & CLOSE (3:00–3:30)  [Impact 20, Market Readiness]

> "The impact is direct. **Health** — we stop farmers getting unsafe pesticide doses and
> point them to real help. **Environment** — grounded, correct doses mean less chemical
> over-spraying into soil and water. **Access** — it's in Bengali, works offline, runs on
> the phones farmers already own.
>
> This isn't a mock-up. The model is trained, the datasets are collected and released, the
> safety pipeline runs, and it's all in front of you. Two papers from this work are under
> review. **KrishokChat is a working, grounded, safety-first advisory system — ready to sit
> in front of Bangladesh's own agricultural helpline.** Thank you."

Stop. Smile. Hands still. Let them ask.

---

## THE THREE NUMBERS (memorize — your anchors)
1. **0.02 taka** per LLM answer; **$500/mo GPU = 10M+ answers**. → Economics.
2. **16123**, and it handled **92,094 calls** last year. → Business (B2G) + Impact.
3. **95–97% disease accuracy, 6 MB, <30 ms, offline.** → Idea + Market Readiness.

## THE ONE SENTENCE (if a judge stops you at 60 seconds)
> "A Bengali farming assistant that's grounded in real government data, runs offline on a
> cheap phone, refuses to give dangerous pesticide advice, and costs two paisa a question —
> free for farmers, paid for by government and agro-business."

---

## DELIVERY CHECKLIST
- [ ] Site open in a tab BEFORE you start; unsafe-query and disease-photo presets ready.
- [ ] Phone/laptop charged; offline demo cached in case wifi dies.
- [ ] Poster within arm's reach to point at if a demo step fails.
- [ ] Practice out loud 5×. Time it. Cut, don't rush.
- [ ] Speak 15% slower than feels natural. Judges are scoring, not chatting.
- [ ] Numbers land only if you PAUSE right after them.
