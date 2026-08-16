# Anti-AI-Flag & Strengths-Framing Checklist for the Poster

This file gives (1) the competition framing principle, (2) the banned vocabulary, (3) the writing rules, (4) the pre-print checklist, and (5) a peer-reviewer simulation. The goal: the poster reads like a researcher wrote it, not like a language model — and it frames everything as a strength.

---

## 1. Competition framing principle (faculty guidance)

> **This is a competition, not a peer review.** The poster shows what we built and what we achieved. Unfinished work is framed as an **ongoing roadmap**, never as a weakness, limitation, or "not yet" confession.

Three rules follow from this:

1. **No weakness displays.** Do not write sections titled "Limitations," "Known Issues," "What Doesn't Work," or similar. If something is unfinished, it goes in the "Roadmap & Ongoing Work" block as a forward-looking next step.
2. **Frame every fact as a strength.** The soil model achieves R²=0.39 — that is a result, not "the model is still weak." The verifier is deterministic-first — that is a deliberate SOTA design choice, not "no LLM-based verifier yet."
3. **Specificity, not hedging.** A competition poster with vague claims loses to one with concrete numbers. Every claim carries a number, a named method, or a named source. This is also the primary anti-AI-flag defence — AI-generated posters are vague; real research is specific.

> **Why keep the anti-AI-flag discipline in a competition?** Judges see dozens of posters. The ones that read like AI marketing copy (buzzwords, empty adjectives, symmetric bullet triples) score lower on Poster 10 and Idea 20 regardless of the underlying work. The ones that read like a researcher wrote them — specific, numbered, named — score higher. The anti-AI-flag rules below are about *voice*, not about *honesty*. Keep the voice discipline; drop the weakness display.

---

## 2. Banned vocabulary (do not use anywhere on the poster)

| Banned | Why | Replace with |
|---|---|---|
| groundbreaking, revolutionary, game-changing, cutting-edge, state-of-the-art | empty intensifiers | the specific number or method |
| comprehensive, robust, seamless, scalable (alone) | filler adjectives | the concrete scope (e.g. "6 dialects, 12 categories") |
| leverage, utilise, empower, enable (as filler verbs) | corporate-speak | "uses", "runs on", "returns" |
| delve, realm, tapestry, navigate the landscape | AI floridness | delete the clause |
| in today's rapidly evolving world, in the modern era | filler openers | delete |
| it is worth noting, it is important to mention, notably, importantly | hollow hedges | delete |
| plays a crucial/vital/pivotal role | hollow claim | the specific role, named |
| in conclusion, to summarise, in summary | essay transitions | delete (posters do not need them) |
| a wide range of, various, numerous, several (without a count) | vague quantifiers | the exact count |
| harness, unlock, transform, redefine, supercharge | marketing verbs | the concrete action |
| "AI-powered", "cloud-native", "next-generation", "intelligent" (as adjectives) | buzzword stacks | delete the adjective |
| 🚀 🌾 ✨ 🤖 and any other emoji | decoration | none — posters use no emoji |
| **limitation, not yet, doesn't work, fails, weak, underperform** | weakness display | reframe as "ongoing," "roadmap," "next step," or cite the positive number |

---

## 3. Writing rules (apply to every block of copy)

1. **One idea per sentence.** If a sentence has two clauses joined by "and" and they are different ideas, split it.
2. **Active voice.** "The verifier drops ungrounded claims" not "ungrounded claims are dropped by the verifier."
3. **Numbers in numerals, not words.** "85,979" not "eighty-five thousand." Tabular numerics so digits align.
4. **Name the method, not the category.** "EfficientNet-B0, 5-fold CV, Optuna-tuned" not "a deep learning model." "YOLO26s-cls, 97.23% top-1" not "a high-accuracy classifier."
5. **Bengali first, English second.** Bengali terms (কৃষি পরামর্শ, নিরাপত্তা যাচাই, ১৬১২৩) are evidence the work is for the stated users. Pair each with a short English gloss.
6. **No sentence longer than ~25 words.** Long sentences are where AI padding hides.
7. **No paragraph longer than 4 lines** at 24 pt. A0 is read standing up.
8. **Frame as strength, not as confession.** "R²=0.39, a 22% improvement over baseline" not "R²=0.39, still below lab-dataset results." The first is a result; the second is a weakness display.
9. **Cite the source for any number a judge might challenge.** A small superscript or footnote pointing to the paper / dataset / file. This reads as rigorous.
10. **Read every block aloud.** If it sounds like a LinkedIn post or a product launch tweet, rewrite it.

---

## 4. Pre-print checklist (run against the final draft)

### Content
- [ ] Every number on the poster appears in `01_FIGURES_AND_ASSETS_LIST.md` §2. No exceptions.
- [ ] No number from `01_…` §3 (the "never use" list) appears anywhere.
- [ ] The deprecated arXiv ID 2606.29243 does not appear. Only the two papers + the AgriVision report are cited.
- [ ] Node count is **2,882** everywhere (not 2,120).
- [ ] Soil section shows **R²=0.39, RMSE=4.09 kPa** (the EffNet-B0 5-fold results), not the old negative-R² numbers.
- [ ] Disease detection section shows the **AgriVision 95–97% accuracy table**.
- [ ] The four pillars are all present and each has a dedicated block: KrishokChat (A), Safety architecture (B), Disease detection (C1), Soil (C2).
- [ ] The 16123 Krishi Call Center appears in the hero diagram AND in the impact section.
- [ ] The 85,979 benchmark appears in the stat ribbon AND in the benchmark section.
- [ ] No section is titled "Limitations," "Known Issues," or "Weaknesses." Unfinished work is in "Roadmap & Ongoing Work."
- [ ] No fabricated market size or revenue projection. Business section uses qualitative lanes with comparator evidence.

### Language (AI-flag scan)
- [ ] No word from the §2 banned-vocabulary table appears anywhere. (Search the final text for each.)
- [ ] No emoji.
- [ ] No "in conclusion / to summarise / in summary."
- [ ] No sentence over ~25 words (spot-check the longest 10).
- [ ] No paragraph over 4 lines at 24 pt.
- [ ] Every strong claim is paired with a number or a named method.
- [ ] At least one Bengali term appears with an English gloss.

### Visual / hierarchy
- [ ] Title, hook, and the 6 stat chips are legible from 2 m (print an A3 proof and stand back).
- [ ] The hero pipeline diagram is the largest graphic and sits at eye level (centre column).
- [ ] Every graph and photo is ≥ 12 × 18 cm.
- [ ] Headings 48–60 pt; body 24–32 pt; nothing smaller than 20 pt except footnotes/QR labels.
- [ ] Colour follows the field-notebook palette (paper #faf6ef, ink #1a1611, leaf #2f5d3a, ochre #c8893c, clay #a8542b). No dark-mode chrome, no purple/blue gradients.
- [ ] Body text meets WCAG AA contrast.
- [ ] No pale grey text on white.
- [ ] Tabular numerics for all stats and tables.

### Judging-criteria coverage (cross-check with `03_JUDGING_CRITERIA_MAPPING.md`)
- [ ] Idea 20: 4 contributions + hero diagram + structured verifier schema.
- [ ] Impact 20: health/safety + environment + access, each with a concrete anchor.
- [ ] Business 20: three lanes with comparator evidence; "framework in development" tag.
- [ ] Market 20: product screenshots + published datasets + real model accuracies (vision 95–97%, soil R²=0.39) + roadmap.
- [ ] UI 10: product screenshots show the field-notebook design system + agent trace.
- [ ] Poster 10: hierarchy, legibility, palette, no AI-flags, no weakness displays.

---

## 5. Peer-reviewer simulation (competition judge mode)

Read the poster as a competition judge would — looking for strengths, not weaknesses. For each question, the poster must have a strong answer:

1. **"What is actually new here?"** → The 4 contributions (A5) + the structured verifier schema (B3) + the hero diagram (B1). The gap table vs Farmer.Chat/KrishokBondhu makes it concrete.
2. **"Is the safety pipeline real or a slide?"** → Hero diagram shows the 16123 stop-branch + audit log; /chat screenshot shows the trace skipping stages; the 14-field claim schema shows the SOTA approach.
3. **"Where do your numbers come from?"** → Every number cites the paper, the dataset, or the AgriVision report. QR codes link to the dataset and the papers.
4. **"Does the disease detection actually work?"** → The AgriVision table: 97.29% / 96.49% / 97.23% / 95.04% / 88% across five crops, with F1 scores, edge-deployment sizes, and inference speeds. Not a claim — a measured result.
5. **"Does the soil model actually work?"** → The scatter plot + the table: R²=0.39, RMSE=4.09 kPa, 22% improvement over baseline, 5-fold CV, EffNet-B0. A real field-collected dataset with a working model.
6. **"What happens when the model is wrong about a dose?"** → The structured verifier does 14-field claim matching with 6 relation types and drops unsupported claims; the audit log records it; /analytics surfaces it.
7. **"Is this deployed or a demo?"** → Working end-to-end prototype: chat + vision + soil + audit + research panel. Edge-deployable disease models (<30 ms on Android). Datasets published. Two papers under review. Roadmap for the next phase.
8. **"How is this different from Farmer.Chat?"** → The comparison table: safety before retrieval, structured dosage verifier, audit log, Bengali + 6 dialects, 85,979 benchmark, photo → grounded treatment at 95–97%, field soil dataset + model.
9. **"What is the business model?"** → Three lanes (freemium + B2B audit; 16123 B2G partnership; dataset/API licensing) with comparator evidence; "framework in development."
10. **"What is the environmental impact?"** → Source-grounded dosage reduces over-application of pesticide/fertilizer → less soil and water contamination. Edge models reduce cloud compute.

---

## 6. Final 60-second self-test

Stand 2 metres from the A0 print (or A3 proof at 1 m). In 60 seconds, point to:
1. the title and hook,
2. the 6 hero numbers,
3. the four-stage pipeline diagram with the 16123 branch,
4. the AgriVision 95–97% accuracy table,
5. the soil scatter plot (R²=0.39),
6. one product screenshot,
7. the 4 contributions / gap table,
8. the roadmap block (no "limitations" block),
9. the QR codes.

If you cannot point to all nine in 60 seconds, the hierarchy is wrong — fix it before printing.

---

## 7. The one-sentence voice test

Read this aloud: *"KrishokChat is a safety-first Bengali agricultural advisory system where a farmer types a question in dialect or uploads a diseased leaf photo, and receives source-cited treatment advice that has passed a four-stage verified agent pipeline — backed by an 85,979-instance benchmark, a 722-image field soil dataset with a working EfficientNet regression model, and crop-disease classifiers at 95–97% accuracy — escalating unsafe queries to 16123."*

If the poster's voice matches that sentence — specific, numbered, named, no buzzwords — it passes. If any block sounds vaguer or more marketing-y than that sentence, rewrite it.