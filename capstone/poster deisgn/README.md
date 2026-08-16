# KrishokChat A0 Poster — Design Package

A complete, research-grounded content organization and creation plan for the Innovation Challenge / capstone poster. Built by auditing the repo's actual research, product, datasets, and the AgriVision crop-detection report — every number cites a source file.

## Framing principle (faculty guidance)

> **This is a competition, not a peer review.** The poster shows what we built and what we achieved. Unfinished work is framed as an **ongoing roadmap**, never as a weakness. Four main pillars carry the poster.

## The four pillars

| # | Pillar | Hero evidence |
|---|---|---|
| 1 | **KrishokChat — Bengali Agri QA** (benchmark + model + retrieval) | 85,979 instances, R@10 chart, GenF1 0.314 vs 0.165 |
| 2 | **Crop Disease Detection + Agentic Pipeline** | AgriVision 95–97% top-1 accuracy, edge-deployable |
| 3 | **Soil Moisture — Field Dataset + Model** | 722 Pabna images, EffNet-B0 R²=0.39 (22% over baseline) |
| 4 | **Safety-First Verification Architecture** | 4-stage pipeline, 14-field claim schema, 16123 escalation |

## Read these in order

1. **`00_POSTER_DESIGN_MASTER.md`** — the master outline. 3-column A0 layout, four-pillar section map, exact copy (Bengali + English), figure specs, sizes, reading-order rationale, what NOT to include, colour/type rules, build sequence.
2. **`01_FIGURES_AND_ASSETS_LIST.md`** — every figure with its source file, every defensible number with its citation, the soil scatter plot, the AgriVision accuracy table, and the list of numbers to never use.
3. **`02_ANTI_AI_FLAG_AND_PROOF_CHECKLIST.md`** — competition framing principle, banned vocabulary, writing rules, pre-print checklist, peer-reviewer simulation, 60-second self-test, one-sentence voice test.
4. **`03_JUDGING_CRITERIA_MAPPING.md`** — how each IC criterion (Idea 20, Impact 20, Business 20, Market 20, UI 10, Poster 10) is won on the poster, with the four-pillar → criteria coverage map.

## The one-line thesis the poster must land

> KrishokChat is a safety-first Bengali agricultural advisory system where a farmer types a question in dialect or uploads a diseased leaf photo, and receives source-cited treatment advice that has passed a four-stage verified agent pipeline — backed by an 85,979-instance benchmark, a 722-image field soil-moisture dataset with a working EfficientNet regression model (R²=0.39), and crop-disease classifiers at 95–97% top-1 accuracy — escalating unsafe queries to the national Krishi Call Center (16123).

## Quick build order

1. Confirm numbers against `01_…` §2 (node count = 2,882; soil = R²=0.39; vision = 95–97%).
2. Redraw the hero pipeline diagram (reuse `capstone/figure.png`, add 16123 branch + audit log + structured-verifier label).
3. Use `backend/ml_assets/soil/pred_vs_actual.png` for the soil scatter plot.
4. Build the AgriVision accuracy table from `docs/disease detection/AgriVision_1.pdf`.
5. Make the R@10 bar chart from the AgriTrust numbers.
6. Capture three product screenshots (`/detect`, `/chat` banned query, `/analytics`).
7. Write final copy from `00_…` §3 blocks; frame everything as a strength.
8. Run `02_…` checklist (no weakness displays, no banned vocabulary).
9. Lay out in Figma / Illustrator / Inkscape on the 3-column A0 grid.
10. Print A3 proof, read from 2 m. Fix hierarchy. Print A0 on matte paper.

## Hard rules inherited from the repo (AGENTS.md + paper policy)

- Do not fabricate any number. If it is not in `01_…` §2, it does not go on the poster.
- Do not cite the deprecated arXiv v1 (2606.29243). Use the two papers in `paper/done papers/` + the AgriVision report only.
- Vision is classification-only when discussing boxes — but the AgriVision top-1 classification accuracies ARE measured and ARE fine to cite.
- No invented market size or revenue projection — qualitative business lanes with comparator evidence only.
- Soil: show the EffNet-B0 R²=0.39 results, not the old negative-R² numbers.

## Folder location

`D:\KrishokChat Advisory System\capstone\poster deisgn\` (note: the folder name carries a pre-existing typo "deisgn").