# KrishokChat Handout and Judge-Demo Claim Ledger

This ledger synchronizes the updated judge script, four-page handout, poster language, and live demonstration.

## 1. Chronological Story Claims

| Story point | Approved wording | Evidence/source | Presentation home |
|---|---|---|---|
| Field discovery | `300 face-to-face farmer-interview questions in Rajshahi and Natore` | authoritative benchmark manuscript; local extraction/claim files | script 0:00–0:35; handout panel 2 |
| Real-world extension | `1,000 real farmer questions from field and online farmer sources` | benchmark artifact/paper source | script 0:00–0:35; panel 2 |
| Service pressure | `Krishi Call Center 16123 handled 92,094 calls in the reported FY25–26 context` | `docs/competitive-landscape.md`, `docs/PRODUCTION_ROLLOUT_PLAN.md` | script 0:35–0:58; panel 4 |
| Baseline grounding issue | `chemical hallucination remained 4.05–7.00% under oracle evidence in the evaluated model set` | authoritative paper extraction / claim ledger | script 0:58–1:35; panel 2 |
| Fine-tuned QA result | `KrishokChat-4B scored 0.314 token-F1 versus 0.165 for the best listed zero-shot baseline under the stated comparison` | benchmark constants / local manuscript | script 0:58–1:35; panel 2 |
| Standalone safety issue | `the standalone fine-tuned model followed intended safety behavior on 1/323 tested items, 0.31% compliance` | authoritative manuscript extraction | script 0:58–1:35; panel 2 |
| Dataset creation | `85,979 provenance-traced instances across four tracks, built from 284 official publications` | local benchmark artifact and manuscript | script 1:35–1:58; panel 2 |
| Retrieval result | `hybrid RRF is used when the dense channel is available, with automatic BM25-only fallback` | `backend/app/infrastructure/retrieval/hybrid.py`, container wiring | script 1:35–1:58; panel 3 |
| Soil field asset | `722 RGB soil photographs paired with tensiometer readings from 0.0–21.5 kPa in Pabna` | `dataset_release/soil_moisture/README.md` | script 3:05–3:22; panel 2 or 4 |
| Qualitative failure example | `farmer_q_12` contrasts the pinned reference quantity and seed-treatment guidance with the generated answer's hectare-rate quantity and different treatment | `dataset_release/benchmark/golden_runs_v1.json` | panel 2 |

## 2. Live Demo Cues

| Time | Operator action | Presenter points to | Failure fallback |
|---|---|---|---|
| 0:00 | open landing page | field-first origin | point to cover field image |
| 0:35 | remain on landing/data context | 16123 service gap | point to poster market/problem block |
| 0:58 | open benchmark/data page | baseline and dataset result tiles | use handout panel 2 |
| 1:58 | submit paraquat preset | safety trace; skipped stages; 16123 | use screenshot `03_chat_safety_refusal.png` |
| 2:22 | show prewarmed grounded answer | source chips; trace; verifier | use screenshot `02_chat_grounded.png` |
| 2:42 | start prepared `/detect` sample | crop/disease route; advisory | use screenshot `04_detect_diagnosis.png` |
| 3:05 | show soil page or keep diagnosis | 722-image field asset | use handout soil strip; do not run locked analyzer |
| 3:22 | show business/analytics page | B2G/B2B/Data/API | use handout panel 4 |

## 3. Wording Corrections

| Avoid | Say instead |
|---|---|
| `100% safe` | `safety-first, fail-closed terminal routing for the tested categories` |
| `object detection` | `crop and disease classification` |
| `we use BM25 only` | `hybrid RRF when available, with BM25-only local fallback` |
| `the verifier checks all 14 fields in the current runtime` | `the research schema defines 14 fields; the current runtime checks dosage-bearing claims against retrieved evidence` |
| `all unsupported questions are refused` | `the scoped coverage gate refused 12/12 unanswerable items in the pinned golden probe` |
| `soil moisture prediction is ready` | `the field dataset is released; the predictor remains a development lane` |
| `ready for national deployment` | `ready for a supervised district or extension-office pilot` |
| `farmers will subscribe` | `farmers receive free access; institutions are the primary payer` |
| `the paper proves farmer impact` | `the research and product address a documented access and safety problem; impact needs supervised field evaluation` |

## 4. Evidence Labels

Use one label in small type under each chart, visual, or statistic:

- `FIELD ASSET` — collected field/interview resource;
- `PAPER RESULT` — manuscript evaluation;
- `RUNTIME` — current application behavior;
- `LIVE VERIFICATION` — named live test artifact;
- `MARKET EVIDENCE` — external operating/comparator context;
- `PILOT PLAN` — future operating step.

## 5. Final Print Gates

- [ ] No deprecated paper identifier appears anywhere in the new script, handout, QR label, or reference block.
- [ ] No public paper link is printed unless the researcher has approved it under the project paper policy.
- [ ] Vision language says classification only.
- [ ] Hybrid/BM25 wording matches the current runtime.
- [ ] 0.31% is clearly attributed to the standalone model test, not the full application.
- [ ] Soil prediction is not presented as a deployed capability.
- [ ] Every number has a source and a condition.
- [ ] QR codes are tested from the printed handout.
- [ ] The operator can complete the three live moves without typing long Bengali text manually.
