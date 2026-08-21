# Judge Q&A — Anticipated Questions + Tight Rebuttals

After the 3-minute pitch, judges probe. These are the questions they *will* ask, ranked by
likelihood, with short answers you can actually say. Keep each answer to 2–3 sentences. Land
a number, then stop.

---

## BUSINESS / ECONOMICS (they push hardest here)

**Q: "How do you actually make money if the farmer doesn't pay?"**
> "Same way ACI's Fosholi does with 2.6 million users — free for farmers, paid by
> institutions. Government pays us to sit in front of the 16123 helpline as an AI triage
> layer; agro-dealers and seed companies pay for our district-level analytics dashboard; and
> we license our datasets. The farmer side is a public good that costs us almost nothing to
> run."

**Q: "Will the government / DAE actually buy this?"**
> "The pain is real and quantified — 16123 took 92,000 calls last year on a handful of
> operators. We don't replace them; we auto-answer the routine grounded questions and
> escalate only the hard or unsafe ones, with a full audit log they can inspect. That audit
> trail is exactly what a government buyer needs to trust an AI. It's a capacity multiplier,
> not a black box."

**Q: "What's your GPU / running cost at scale? Isn't AI expensive?"**
> "I checked this week. On Gemini's API an answer costs about 0.02 taka. If we self-host our
> own model, one rented RTX 4090 at roughly $500 a month serves over 10 million questions.
> Ten thousand active paid users is 1.5 million questions a month — that's a fraction of one
> GPU. Cost is genuinely not our constraint."

**Q: "Why free tier with no LLM — isn't that a worse product?"**
> "It's a deliberate cost *and* safety choice. The free tier answers directly from our
> grounded database, so it can't hallucinate a pesticide dose and it needs no GPU. Farmers
> who want open-ended LLM conversation upgrade — but nobody pays to stay safe."

**Q: "What's your market size / who pays first?"**
> "First customer is B2G — DAE and a2i around the 16123 helpline. Then B2B agro-dealers and
> seed companies; ACI's comparable B2B line targeted 3.5 million euro. We're not inventing a
> market — we're entering one that already pays for exactly this, with a better technical
> product."

---

## TECHNICAL / IDEA

**Q: "How is this different from ChatGPT / a generic chatbot?"**
> "Three ways generic chatbots can't match: it's grounded in a knowledge graph of real
> government publications so it doesn't invent facts; it classifies safety *before*
> retrieval so it refuses dangerous chemical queries; and it runs offline on a mid-range
> phone. A generic chatbot fails all three."

**Q: "Did you train the model or just call an API?"**
> "We trained it. We fine-tuned a 4-billion-parameter Bengali model with LoRA, 4-bit
> quantized so it runs on-device. On our Bengali QA benchmark it scores 1.9 times the best
> zero-shot baseline. The disease models are our own too — 6 megabytes, under 30
> milliseconds on a phone."

**Q: "How accurate is the disease detection, really?"**
> "95 to 97% top-1 across five crops — brassica, rice, corn, potato, wheat — on held-out
> test images. And for 436 of 437 library entries it returns a grounded Bengali treatment,
> not just a label. To be precise, it's classification accuracy, not object detection — we
> don't claim bounding boxes."

**Q: "How do you stop it giving wrong chemical doses?"**
> "Two layers. Unsafe categories are refused before the model even runs. And any answer that
> does run goes through a verifier that checks 14 fields — chemical, dose, unit, interval,
> safety interval — against the retrieved sources. If the evidence isn't there, it abstains
> instead of guessing. Fail-closed."

**Q: "Your soil model R² is only 0.39 — isn't that weak?"**
> "It's a 22% error reduction over the baseline, from a single phone photo, on a dataset we
> collected ourselves in the field — 722 labeled images. For a first field dataset that
> didn't exist before, that's a real result and a foundation to improve, not a finished
> product."

---

## IMPACT / SOCIAL

**Q: "What's the real-world impact — who does this help today?"**
> "A smallholder with a cheap Android phone and no reliable internet can photograph a
> diseased leaf and get grounded Bengali treatment offline, and can't be given a dangerous
> pesticide dose. Rural internet reaches under half of farmers, so 'offline' isn't a feature
> — it's the difference between usable and useless."

**Q: "Is this deployed / has anyone used it?"**
> "It's a working prototype — the model is trained, the datasets collected and released
> publicly, the full safety pipeline runs, and two papers from the work are under review.
> The next step is the B2G pilot with the extension office, which is exactly what this
> platform is built to enter."

---

## MARKET READINESS / RISK

**Q: "What's stopping a big player from copying this?"**
> "The datasets. The 86,000-instance grounded benchmark and the 722-image field soil dataset
> took real fieldwork in Pabna, Rajshahi and Natore — that's the moat. Anyone can call an
> API; nobody else has our grounded, provenance-traced Bangladesh data."

**Q: "Language / dialect — does it really handle how farmers talk?"**
> "Yes — that's why we did field interviews. It covers standard Bengali plus five regional
> dialects, and our own retrieval beats dense models that collapse on dialect queries. We
> built for how farmers actually speak, not textbook Bengali."

**Q: "What are the limitations?" (never say the word 'limitation' back)**
> "The roadmap is voice output for low-literacy users, wider dialect coverage, and
> refining the soil model with more field campaigns. The core — grounded advisory, safety,
> disease, offline — is working now."

---

## IF A DEMO BREAKS LIVE
> "The live connection's being slow — let me show you the result on the poster, it's the
> same flow." Point to the relevant diagram. Never debug in front of judges.

## IF YOU GET A QUESTION YOU DON'T KNOW
> "Good question — I don't have that number in front of me, but here's how we'd approach
> it..." Then bridge to something you DO know. Never invent a statistic; judges in this
> field will catch it and you lose more than the point.
