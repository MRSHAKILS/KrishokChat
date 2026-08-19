# KrishokChat Capstone Presentation Package

This folder contains the judge-facing presentation plan and the compact handout plan. The poster LaTeX source remains in `latex/` and is owned by the poster refinement workflow.

## Use These Files

### 1. Judge script

- `JUDGE_SCRIPT_3_4_MIN_UPDATED.md` — canonical English script with exact laptop-operator actions and timing.
- `JUDGE_SCRIPT_3_4_MIN_BANGLA_UPDATED.md` — natural Bengali delivery version.

The compatibility files in `../presentation/` point to these canonical scripts:

- `../presentation/SCRIPT_3MIN.md`
- `../presentation/SCRIPT_3MIN_BANGLA.md`

### 2. Four-page handout

- `BROCHURE_4PAGE_VISUAL_PLAN.md` — final recommendation: one A3 sheet, printed double-sided, folded into four A4 panels.

### 3. Visual production

- `VISUAL_GENERATION_PROMPTS.md` — exact prompts for text-free image support and specifications for code-generated diagrams.

### 4. Claim and demo control

- `CLAIM_AND_DEMO_CUE_LEDGER.md` — approved wording, source homes, live actions, failure fallbacks, and final print gates.

## Recommended Execution Order

1. Rehearse the English/Bengali script with one presenter and one laptop operator.
2. Confirm the final demo pages and capture the three live screenshots.
3. Generate the safety architecture, field-to-product timeline, vision route, and business flow as SVG/PDF using code or LaTeX.
4. Use real field and product screenshots before considering generated imagery.
5. Layout the four A4 panels on one double-sided A3 sheet.
6. Run the claim ledger’s print gates and test every QR code from the physical proof.

## Core Positioning

> We started with farmers’ questions, turned the observed gaps into research, turned the research into a safety-first architecture, and turned that architecture into a working Bengali agricultural advisory product.

## Important Wording Boundaries

- Current vision artifacts are classification models, not object detectors.
- The current retrieval path is hybrid RRF when dense retrieval is available, with automatic BM25-only fallback.
- The 0.31% figure describes the standalone fine-tuned model’s tested safety behavior, not the full routed application.
- The current runtime checks dosage-bearing claims; the research verifier schema defines fourteen fields.
- The soil contribution is the field dataset and split; the predictor is not presented as deployment-ready.
- The market claim is supervised pilot readiness, not autonomous national deployment.
