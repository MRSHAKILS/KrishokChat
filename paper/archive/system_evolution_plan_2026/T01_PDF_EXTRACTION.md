# T01: Authoritative PDF Extraction

## Tool and Version
- Tool: PyMuPDF (fitz) v1.27.2.2
- Python version: 3.12.0 (MSC v.1935 64 bit (AMD64))
- Extraction date: 2026-08-12

> **NOTE:** All claims below are raw extractions. None have been verified.
> Marked for reconciliation in T05. Do NOT adopt any claim as ground truth.

---

## PDF A: KrishokTech Benchmark
- File: KrishokTech__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf
- SHA-256: `75cca13c0e68ae834cdad3722a1f5fc938e452bea83404c00d73e8f1f2edf53f`
- Pages: 25
- Size: 1,671,455 bytes

### Page-by-page summary
| Page | Text chars | Tables | Images | Key claims |
|------|-----------|--------|--------|------------|
| 1 | 3,943 | 0 | 0 | COUNT_COMMA, METRIC, PERCENTAGE, REFERENCE |
| 2 | 4,271 | 0 | 0 | COUNT_COMMA, DATASET_SIZE |
| 3 | 3,803 | 0 | 1 | COUNT_COMMA, DATASET_SIZE, MODEL_NAME, REFERENCE |
| 4 | 4,568 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, MODEL_NAME, PERCENTAGE |
| 5 | 4,712 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, REFERENCE |
| 6 | 4,299 | 0 | 0 | COUNT_COMMA, METRIC, PERCENTAGE, REFERENCE |
| 7 | 4,572 | 0 | 0 | METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 8 | 3,917 | 0 | 0 | COUNT_COMMA, METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 9 | 4,749 | 0 | 0 | COUNT_COMMA, METRIC |
| 10 | 4,687 | 0 | 0 | DATASET_SIZE, METRIC, PERCENTAGE |
| 11 | 5,010 | 0 | 0 | DATASET_SIZE, MODEL_NAME, REFERENCE |
| 12 | 5,244 | 0 | 0 | DATASET_SIZE |
| 13 | 4,431 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, MODEL_NAME, REFERENCE |
| 14 | 3,847 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, MODEL_NAME, PERCENTAGE, REFERENCE |
| 15 | 4,636 | 0 | 0 | COUNT_COMMA, METRIC, REFERENCE |
| 16 | 2,620 | 0 | 0 | COUNT_COMMA, PERCENTAGE, REFERENCE |
| 17 | 4,871 | 0 | 0 | COUNT_COMMA, PERCENTAGE, REFERENCE |
| 18 | 4,504 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 19 | 4,131 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 20 | 3,058 | 1 | 0 | METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 21 | 4,898 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 22 | 3,681 | 0 | 0 | METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 23 | 2,043 | 0 | 0 | CHEMICAL, DOSAGE, REFERENCE |
| 24 | 4,677 | 0 | 0 | COUNT_COMMA, METRIC, MODEL_NAME, PERCENTAGE, REFERENCE |
| 25 | 602 | 0 | 0 | METRIC, MODEL_NAME |

**Total claims extracted: 265**

### Numerical Claims Found
| # | Page | Category | Value | Context (truncated) |
|---|------|----------|-------|---------------------|
| 1 | 1 | PERCENTAGE | 7.00% | icient regardless of model 018 scale. Oracle evidence narrows the gap, 019 but leaves a persistent floor of 4.05 to 020 7.00% of chemical hallucinations. Fine- 021 tuning on KrishokTech substantially  |
| 2 | 1 | COUNT_COMMA | 85,979 | ultural Benchmark with Safety-Critical Chemical Advisory Anonymous ACL submission Abstract We introduce KrishokTech, an 85,979- 001 instance Bengali agricultural benchmark 002 built from 284 governmen |
| 3 | 1 | COUNT_COMMA | 1,000 | tracks: General 005 Knowledge QA, Treatment QA, Safety Re- 006 fusal and Re-query, and Table QA. It also 007 includes a 1,000-query Real-World Farmer 008 Benchmark collected independently from 009 fie |
| 4 | 1 | METRIC | F1 | ine- 021 tuning on KrishokTech substantially out- 022 performs the strongest zero-shot baseline 023 on General QA Token F1. However, struc- 024 tured table reasoning and farmer-language 025 transfer r |
| 5 | 1 | REFERENCE | table
067 | fety lens (Petroni et al., 065 2021; Thakur et al., 2021; Ghosh et al., 2025). 066 Pal et al. address Bengali and Hindi table 067 question answering through automatic large- 068 scale data generation, |
| 6 | 2 | COUNT_COMMA | 85,979 | ted refusal behavior 096 zero-shot models exhibit on unsafe queries 097 (§5). 098 Contributions. 099 1. KrishokTech: an 85,979-instance, four- 100 track Bengali agricultural benchmark 101 built from 2 |
| 7 | 2 | COUNT_COMMA | 1,000 | al behavior 117 under fine-tuning (exploratory analysis in 118 Appendix I.3). 119 4. A Real-World Farmer Benchmark: 120 1,000 authentic farmer queries, col- 121 lected independently of the constructio |
| 8 | 2 | DATASET_SIZE | 085
farmers | our construction pipeline, 300 of them from 084 structured field interviews with smallholder 085 farmers, to test whether performance on the 086 four tracks transfers to how farmers actually 087 ask q |
| 9 | 3 | COUNT_COMMA | 28,993 | mmarizes the released re- 190 source. 191 Table 1: The KrishokTech benchmark at a glance. Track Total Probes General QA 28,993 Knowledge only, no chemicals Treatment QA 11,224 Chemical advisory w/ pro |
| 10 | 3 | COUNT_COMMA | 11,224 | : The KrishokTech benchmark at a glance. Track Total Probes General QA 28,993 Knowledge only, no chemicals Treatment QA 11,224 Chemical advisory w/ provenance Safety (T3+T4) 20,112 Refusal + re-query  |
| 11 | 3 | COUNT_COMMA | 20,112 | robes General QA 28,993 Knowledge only, no chemicals Treatment QA 11,224 Chemical advisory w/ provenance Safety (T3+T4) 20,112 Refusal + re-query Table QA 25,650 Structured reasoning Core Tracks Total |
| 12 | 3 | COUNT_COMMA | 25,650 | nly, no chemicals Treatment QA 11,224 Chemical advisory w/ provenance Safety (T3+T4) 20,112 Refusal + re-query Table QA 25,650 Structured reasoning Core Tracks Total 85,979 Farmer Benchmark 1,000 Real |
| 13 | 3 | COUNT_COMMA | 85,979 | advisory w/ provenance Safety (T3+T4) 20,112 Refusal + re-query Table QA 25,650 Structured reasoning Core Tracks Total 85,979 Farmer Benchmark 1,000 Real-world transfer 3.1 Knowledge Corpus and Semant |
| 14 | 3 | COUNT_COMMA | 1,000 | Safety (T3+T4) 20,112 Refusal + re-query Table QA 25,650 Structured reasoning Core Tracks Total 85,979 Farmer Benchmark 1,000 Real-world transfer 3.1 Knowledge Corpus and Semantic 192 Segmentation 193 |
| 15 | 3 | COUNT_COMMA | 2,946 | ic are merged into standalone 215 units rather than treated as independent per- 216 page fragments. This process yields 2,946 self- 217 contained semantic knowledge units, the fun- 218 damental buildi |
| 16 | 3 | DATASET_SIZE | 979 instances | ctural 232 validity, provenance consistency, and track- 233 specific constraints before release. The result- 234 ing 85,979 instances across four tracks are each 235 linked back to their originating s |
| 17 | 3 | DATASET_SIZE | 243
Answers | sistently across every track. 241 These principles are enforced by automated 242 quality gates throughout construction. 243 Answers are extracted, never gener- 244 ated; the generating model varies on |
| 18 | 3 | MODEL_NAME | Mistral | ts and procedures that often span 208 multiple pages. We convert every publica- 209 tion into structured Markdown using Mistral 210 Document AI for multi-column OCR, preserv- 211 ing hierarchy, tables |
| 19 | 3 | REFERENCE | Table 1 | r Benchmark 187 tests whether performance on the four tracks 188 transfers to how farmers actually ask ques- 189 tions. Table 1 summarizes the released re- 190 source. 191 Table 1: The KrishokTech ben |
| 20 | 3 | REFERENCE | Figure 1 | nstances across four tracks are each 235 linked back to their originating semantic unit 236 and government publication. Figure 1 illus- 237 trates the entire construction pipeline. 238 Figure 1: The p |
| 21 | 4 | PERCENTAGE | 100% | ational 291 semantic units. The reference answer is 292 extracted directly from the underlying se- 293 mantic unit with 100% citation grounding. 294 The treatment_flag and chemical_trace 295 fields ar |
| 22 | 4 | PERCENTAGE | 66.3% | d 321 elsewhere in KrishokTech (Appendix D). The 322 released benchmark contains 11,224 instances. 323 Of these, 7,437 (66.3%) carry at least one 324 provenance-tracked chemical mention. The re- 325 m |
| 23 | 4 | COUNT_COMMA | 4,048 | ricultural knowledge independently of chem- 286 ical advisory capability. 287 Instances are built by pairing one of 288 4,048 base generation cells with a diversi- 289 fied question surface. The gener |
| 24 | 4 | COUNT_COMMA | 1,440 | ry because every 312 mentioned chemical is captured in a structured 313 chemical_trace array (§4.3). 314 The track uses 1,440 base generation cells 315 from 593 unique source semantic units. These 316 |
| 25 | 4 | COUNT_COMMA | 11,224 | cts, personas, and stress scenarios used 321 elsewhere in KrishokTech (Appendix D). The 322 released benchmark contains 11,224 instances. 323 Of these, 7,437 (66.3%) carry at least one 324 provenance- |
| 26 | 4 | COUNT_COMMA | 7,437 | ios used 321 elsewhere in KrishokTech (Appendix D). The 322 released benchmark contains 11,224 instances. 323 Of these, 7,437 (66.3%) carry at least one 324 provenance-tracked chemical mention. The re |
| 27 | 4 | DATASET_SIZE | 287
Instances | actually fails, so this design measures 285 agricultural knowledge independently of chem- 286 ical advisory capability. 287 Instances are built by pairing one of 288 4,048 base generation cells with a |
| 28 | 4 | DATASET_SIZE | 224 instances | , personas, and stress scenarios used 321 elsewhere in KrishokTech (Appendix D). The 322 released benchmark contains 11,224 instances. 323 Of these, 7,437 (66.3%) carry at least one 324 provenance-tra |
| 29 | 4 | DATASET_SIZE | 334
questions | pear in Appendix D. 331 3.5 Track 3: Safety Refusal and 332 Re-query 333 The first two tracks assume clear, answerable 334 questions. Real-world farmer queries, however, 335 often omit the crop, descr |
| 30 | 4 | MODEL_NAME | Bloom | ed; question surfaces are drawn from a 251 partitioned matrix spanning dialect, persona, 252 formulation, scenario, and Bloom level (Wang 253 et al., 2024; Filice et al., 2025). 254 The content tokens |
| 31 | 5 | COUNT_COMMA | 20,112 | same safety boundary 360 as a standard-Bengali speaker, differing only 361 in register. 362 The released track contains 20,112 instances: 363 3,216 T3 refusal records and 16,896 T4 re- 364 query recor |
| 32 | 5 | COUNT_COMMA | 3,216 | 60 as a standard-Bengali speaker, differing only 361 in register. 362 The released track contains 20,112 instances: 363 3,216 T3 refusal records and 16,896 T4 re- 364 query records. The full taxonomy, |
| 33 | 5 | COUNT_COMMA | 16,896 | ker, differing only 361 in register. 362 The released track contains 20,112 instances: 363 3,216 T3 refusal records and 16,896 T4 re- 364 query records. The full taxonomy, slot inven- 365 tory, and sa |
| 34 | 5 | COUNT_COMMA | 25,650 | ects. Every 394 reference answer is read directly from the un- 395 derlying table cell. 396 The released track contains 25,650 dialect- 397 expanded instances drawn from 805 synchro- 398 nized table t |
| 35 | 5 | COUNT_COMMA | 1,000 | . It was 418 never used in training or dataset construction 419 at any stage. The core of the benchmark, 300 420 of the 1,000 released queries, came from struc- 421 tured field interviews with smallho |
| 36 | 5 | COUNT_COMMA | 2,946 | er Q&A portal. The full channel break- 430 down is in Appendix G. 431 Because the benchmark is grounded in the 432 same 2,946-unit semantic corpus but collected 433 entirely outside it, it stands on i |
| 37 | 5 | DATASET_SIZE | 112 instances | e safety boundary 360 as a standard-Bengali speaker, differing only 361 in register. 362 The released track contains 20,112 instances: 363 3,216 T3 refusal records and 16,896 T4 re- 364 query records. |
| 38 | 5 | DATASET_SIZE | 415
queries | rolled evalua- 413 tion holds up against how farmers actually ask: 414 short, colloquial, and often only half-specified 415 queries. 416 The benchmark is collected independently 417 of KrishokTech’s c |
| 39 | 5 | DATASET_SIZE | 448
queries | then have a domain- 446 informed author, not a retrieval score, select 447 the single grounding unit; 69 field-sourced 448 queries additionally received a second inde- 449 pendent pass by a practicing |
| 40 | 5 | REFERENCE | Figure 3 | second inde- 449 pendent pass by a practicing extension oﬀicer. 450 The full five-stage procedure is in Appendix G 451 (Figure 3). 452 5 |
| 41 | 6 | PERCENTAGE | 66.3% | s the correct/omis- 503 sion/hallucination evaluation of §5.1. The 504 7,437 chemical-bearing Treatment QA records 505 (66.3% of the track) link each chemical men- 506 tion to a canonical name and to  |
| 42 | 6 | PERCENTAGE | 4.05% | stance verdict. The protocol is sensitive 518 enough to expose a persistent oracle-condition 519 hallucination floor of 4.05%–7.00% across six 520 architecturally different systems (Table 2, 521 §5.3) |
| 43 | 6 | PERCENTAGE | 7.00% | verdict. The protocol is sensitive 518 enough to expose a persistent oracle-condition 519 hallucination floor of 4.05%–7.00% across six 520 architecturally different systems (Table 2, 521 §5.3). 522 B |
| 44 | 6 | COUNT_COMMA | 1,000 | The released benchmark comprises 1,000 col- 453 lected queries with a strictly held-out 350- 454 query evaluation split (§5). 455 4 Quality Assurance and Data |
| 45 | 6 | COUNT_COMMA | 2,946 | k requires 478 mapping short, colloquial, and often incom- 479 plete queries to the appropriate semantic unit 480 among 2,946 candidates. All 350 evaluation in- 481 stances are curated through the sea |
| 46 | 6 | COUNT_COMMA | 7,437 | t’s primary safety-audit 502 surface. It underlies the correct/omis- 503 sion/hallucination evaluation of §5.1. The 504 7,437 chemical-bearing Treatment QA records 505 (66.3% of the track) link each c |
| 47 | 6 | METRIC | Recall | s an exact chem- 523 ical/dosage/unit match, we additionally de- 524 compose it into a chemical-mention Pre- 525 cision/Recall/F1 (Chem-PRF) score and a 526 Dosage Compliance indicator. This sepa- 527 |
| 48 | 6 | METRIC | F1 | act chem- 523 ical/dosage/unit match, we additionally de- 524 compose it into a chemical-mention Pre- 525 cision/Recall/F1 (Chem-PRF) score and a 526 Dosage Compliance indicator. This sepa- 527 rates  |
| 49 | 6 | REFERENCE | Figure 2 | nables predictions to be checked against the 509 original source evidence rather than against 510 paraphrased text. 511 Figure 2 shows the resulting audit pipeline. 512 Chemical mentions are extracted |
| 50 | 6 | REFERENCE | Table
2 | a persistent oracle-condition 519 hallucination floor of 4.05%–7.00% across six 520 architecturally different systems (Table 2, 521 §5.3). 522 Because Correct% requires an exact chem- 523 ical/dosage/ |
| 51 | 7 | PERCENTAGE | 0% | training split), 566 releasing the one-epoch checkpoint after a 567 second-epoch ablation collapsed Treatment 568 QA to 0% while leaving other tracks largely 569 unaffected (full comparison in Appendi |
| 52 | 7 | PERCENTAGE | 12.43% | same pattern at higher stakes: LLaMA-3.1-8B 604 and Qwen-2.5-7B recommend a correct, veri- 605 fiable treatment on only 12.43% and 13.29% 606 of instances, and even the strongest base- 607 line, Gemin |
| 53 | 7 | PERCENTAGE | 13.29% | n at higher stakes: LLaMA-3.1-8B 604 and Qwen-2.5-7B recommend a correct, veri- 605 fiable treatment on only 12.43% and 13.29% 606 of instances, and even the strongest base- 607 line, Gemini-2.5-FL, i |
| 54 | 7 | PERCENTAGE | 43.64% | % and 13.29% 606 of instances, and even the strongest base- 607 line, Gemini-2.5-FL, is correct on fewer than 608 half (43.64%). Among the models evaluated 609 on General QA, GPT-OSS-120B pairs a mid- |
| 55 | 7 | PERCENTAGE | 36.20% | General QA, GPT-OSS-120B pairs a mid- 610 dling closed-book F1 (0.113) with the second- 611 highest hallucination rate (36.20%), reinforc- 612 ing that neither open-weight scale nor mixture- 613 of-ex |
| 56 | 7 | PERCENTAGE | 11.17% | hal- 624 lucination rises rather than falls. For exam- 625 ple, Qwen-2.5-7B’s General QA hallucination 626 climbs from 11.17% to 20.54% as it generates 627 more without restricting content to the evi- |
| 57 | 7 | PERCENTAGE | 20.54% | lucination rises rather than falls. For exam- 625 ple, Qwen-2.5-7B’s General QA hallucination 626 climbs from 11.17% to 20.54% as it generates 627 more without restricting content to the evi- 628 denc |
| 58 | 7 | PERCENTAGE | 7.00% | content to the evi- 628 dence. Treatment QA keeps a hallucination 629 floor even with gold evidence in hand (4.05– 630 7.00% across the six evaluated systems, §4.3), 631 a residual rate that matters b |
| 59 | 7 | METRIC | F1  | atment QA recom- 594 mendation from parametric knowledge alone 595 (Table 2, closed-book columns). General QA 596 Token F1 stays below 0.17 for every base- 597 line, and scale is not predictive of qua |
| 60 | 7 | MODEL_NAME | Gemma | shot demonstrations: 553 Gemini-2.5-FL, a frontier commercial model 554 with native multimodal and Bengali support; 555 Gemma-4-26B-A4B-IT (26B total, 4B active 556 via mixture-of-experts), an open-mo |
| 61 | 7 | MODEL_NAME | GPT- | support; 555 Gemma-4-26B-A4B-IT (26B total, 4B active 556 via mixture-of-experts), an open-model scale 557 upper bound; GPT-OSS-120B (116.8B total, 558 5.1B active via mixture-of-experts), OpenAI’s 55 |
| 62 | 7 | MODEL_NAME | LLaMA | ound; GPT-OSS-120B (116.8B total, 558 5.1B active via mixture-of-experts), OpenAI’s 559 open-weight frontier model; and LLaMA-3.1- 560 8B-Instruct (8B) and Qwen-2.5-7B-Instruct 561 (7B), which isolate |
| 63 | 7 | MODEL_NAME | Qwen | 8 5.1B active via mixture-of-experts), OpenAI’s 559 open-weight frontier model; and LLaMA-3.1- 560 8B-Instruct (8B) and Qwen-2.5-7B-Instruct 561 (7B), which isolate parameter count from 562 instructio |
| 64 | 7 | MODEL_NAME | GPT | d-book knowledge is 589 insuﬀicient 590 No baseline, including the 26B-parameter 591 Gemma-4-26B and the 116B-parameter GPT- 592 OSS-120B, reliably answers General QA or 593 gives a consistently safe  |
| 65 | 7 | REFERENCE | Table 2 | nistic metrics, the subjective 580 LLM-judge configuration, and exact subset 581 sizes, are reported in Appendix H. 582 Table 2 reports the main closed-book and 583 oracle-context results for General  |
| 66 | 7 | REFERENCE | Table 3 | ppendix H. 582 Table 2 reports the main closed-book and 583 oracle-context results for General QA and 584 Treatment QA, Table 3 reports Real-World 585 Farmer Benchmark performance, and Ap- 586 pendix  |
| 67 | 8 | PERCENTAGE | 35.55% | ondition score, 642 with no retrieved context at all. On Treatment 643 QA, KrishokTech-4B is closed-book correct on 644 35.55% of instances, competitive with Gemma- 645 4-26B (38.73%) and approaching  |
| 68 | 8 | PERCENTAGE | 38.73% | Treatment 643 QA, KrishokTech-4B is closed-book correct on 644 35.55% of instances, competitive with Gemma- 645 4-26B (38.73%) and approaching Gemini-2.5- 646 FL (43.64%). Table QA remains substan- 64 |
| 69 | 8 | PERCENTAGE | 43.64% | book correct on 644 35.55% of instances, competitive with Gemma- 645 4-26B (38.73%) and approaching Gemini-2.5- 646 FL (43.64%). Table QA remains substan- 647 tially harder: KrishokTech-4B does not ma |
| 70 | 8 | COUNT_COMMA | 1,000 | l re- 672 source (§3): the four-track benchmark, a 673 re-runnable chemical-provenance audit proto- 674 col (§4.3), the 1,000-query Farmer Benchmark 675 (§3.7), and the KrishokTech-4B checkpoint, 676  |
| 71 | 8 | METRIC | F1 | Table 2: Closed-book (CB) and oracle-context zero-shot results: General QA Token F1 / Hallucination %, and Treatment QA Correct % / Hallucination %. KrishokTech-4B is fine-tuned on KrishokTech, not ze |
| 72 | 8 | METRIC | F1 score | e-tuning closes most of the gap to same- 659 scale open baselines and comes within 0.02 of 660 the larger Gemma-4-26B’s F1 score, but not 661 to frontier commercial scale. KrishokTech-4B 662 also has  |
| 73 | 8 | MODEL_NAME | Gemma | odel GenF1 GenHal TrtCor TrtHal GenF1 GenHal TrtCor TrtHal Gemini-2.5-FL 0.104 37.15 43.64 15.90 0.281 32.40 51.73 4.91 Gemma-4-26B 0.087 32.12 38.73 9.83 0.253 29.05 54.05 4.05 LLaMA-3.1-8B 0.165 10. |
| 74 | 8 | MODEL_NAME | LLaMA | Gemini-2.5-FL 0.104 37.15 43.64 15.90 0.281 32.40 51.73 4.91 Gemma-4-26B 0.087 32.12 38.73 9.83 0.253 29.05 54.05 4.05 LLaMA-3.1-8B 0.165 10.06 12.43 1.73 0.230 16.48 30.64 5.49 Qwen-2.5-7B 0.136 11.1 |
| 75 | 8 | MODEL_NAME | Qwen | 91 Gemma-4-26B 0.087 32.12 38.73 9.83 0.253 29.05 54.05 4.05 LLaMA-3.1-8B 0.165 10.06 12.43 1.73 0.230 16.48 30.64 5.49 Qwen-2.5-7B 0.136 11.17 13.29 2.02 0.198 20.54 41.33 4.62 GPT-OSS-120B 0.113 36. |
| 76 | 8 | MODEL_NAME | GPT- | 05 LLaMA-3.1-8B 0.165 10.06 12.43 1.73 0.230 16.48 30.64 5.49 Qwen-2.5-7B 0.136 11.17 13.29 2.02 0.198 20.54 41.33 4.62 GPT-OSS-120B 0.113 36.20 32.92 9.47 0.191 30.00 49.79 7.00 KrishokTech-4B 0.314† |
| 77 | 8 | REFERENCE | Table 2 | Table 2: Closed-book (CB) and oracle-context zero-shot results: General QA Token F1 / Hallucination %, and Treatment QA Correct |
| 78 | 8 | REFERENCE | Table 3 | 651 to structured tabular reasoning, genuine head- 652 room rather than a solved track. 653 5.5 Real-world transfer 654 Table 3: Real-World Farmer Benchmark, closed- book (n=350). Model Token F1 Hallu |
| 79 | 9 | COUNT_COMMA | 2,946 | only partially automatable, for the rea- 749 son discussed in §4.1: attribute-guided filter- 750 ing typically narrows 2,946 candidate units to 751 5–15, but a human annotator is still required 752 to |
| 80 | 9 | METRIC | F1  | agreement study is a natural precondi- 762 tion before those specific numbers are relied 763 on in isolation. 764 Token-F1 against extracted references. 765 Because reference answers for General QA an |
| 81 | 9 | METRIC | F1- | s 784 in Appendix I.1 are a partial check in this di- 785 rection, but we did not conduct a systematic 786 audit of low-F1-but-correct responses, and we 787 flag this as an open validity question for  |
| 82 | 10 | PERCENTAGE | 7.00% | ounter. The chemical hallucination floor is 808 a related, still-open problem in its own right: 809 it persists at 4.05–7.00% even under oracle ev- 810 idence (§5.3), so closing it will require more 8 |
| 83 | 10 | DATASET_SIZE | 888
documents | esses) prior to release. 886 All 284 source publications underlying the 887 four synthetic tracks are government-issued 888 documents already in public circulation for 889 extension and educational pu |
| 84 | 10 | METRIC | accuracy | luation. 797 The same second-epoch checkpoint examined 798 in that analysis also collapses Treatment QA 799 closed-book accuracy while marginally improv- 800 ing Table QA (Appendix I.4), a training- 8 |
| 85 | 11 | DATASET_SIZE | 908
questions | the training and 906 evaluation pipeline’s code, from initial plan- 907 ning through execution. The choice of research 908 questions, the experimental design (tracks, 909 baselines, safety taxonomy, a |
| 86 | 11 | DATASET_SIZE | 930
pages | ral language gener- 928 ation in Bangla. In Findings of the Associa- 929 tion for Computational Linguistics: EACL 2023, 930 pages 726–735. 931 Zhoujun Cheng, Haoyu Dong, Zhiruo Wang, Ran 932 Jia, Jiaq |
| 87 | 11 | MODEL_NAME | BanglaBERT | i Ah- 916 mad, Kazi Samin Mubasshir, Md Saiful Islam, 917 Anindya Iqbal, M Sohel Rahman, and Rifat 918 Shahriyar. 2022. BanglaBERT: Language model 919 pretraining and benchmarks for low-resource 920 l |
| 88 | 11 | REFERENCE | table
900 | t preparation, the authors 898 used an AI assistant (Claude, Anthropic) for 899 LATEX formatting and typesetting, cross-table 900 arithmetic verification (e.g., checking that re- 901 ported totals, sp |
| 89 | 12 | DATASET_SIZE | 1022
tasks | e Jernite, Vladimir 1020 Karpukhin, Jean Maillard, et al. 2021. KILT: 1021 A benchmark for knowledge intensive language 1022 tasks. In Proceedings of the 2021 Conference 1023 of the North American Cha |
| 90 | 12 | DATASET_SIZE | 1040
pages | ings of the 62nd An- 1038 nual Meeting of the Association for Compu- 1039 tational Linguistics (Volume 1: Long Papers), 1040 pages 11047–11073. 1041 Namita Singh, Jacqueline Wang’ombe, Nereah 1042 Oka |
| 91 | 12 | DATASET_SIZE | 1074
pages | nguistics and the 1072 11th International Joint Conference on Natural 1073 Language Processing (Volume 1: Long Papers), 1074 pages 3277–3287. 1075 A Source Corpus and Licensing 1076 The corpus underly |
| 92 | 13 | COUNT_COMMA | 28,993 | rve 1154 as the atomic citation target for every down- 1155 stream track. 1156 C General QA Generation 1157 Each of the 28,993 released General Knowl- 1158 edge records stores the fields listed in Tab |
| 93 | 13 | DATASET_SIZE | 993 records | rd citation/ publisher string Source publication / agency source_md/pages string/list Semantic unit / page range All 28,993 records pass five automated 1160 quality gates before release: (G1) the 1161 |
| 94 | 13 | MODEL_NAME | bloom | ion persona string Persona posing question formulation string Communication style scenario string Conditioning scenario bloom string Cognitive level question/answer string Bengali question / answer tr |
| 95 | 13 | REFERENCE | Table 4 | 6 C General QA Generation 1157 Each of the 28,993 released General Knowl- 1158 edge records stores the fields listed in Table 4. 1159 Table 4: Schema of the released General Knowl- edge QA records. Fi |
| 96 | 14 | PERCENTAGE | 66.3% | 621 / 5,569 / 34 Evaluation test split (unique cells) 346 (243) D.1 Full Chemical Audit 1215 Chemical-trace coverage is 66.3% (7,437 of 1216 11,224 records); the remaining 33.7% describe 1217 non-chem |
| 97 | 14 | PERCENTAGE | 33.7% | ) 346 (243) D.1 Full Chemical Audit 1215 Chemical-trace coverage is 66.3% (7,437 of 1216 11,224 records); the remaining 33.7% describe 1217 non-chemical interventions (cultural practice, 1218 seed sel |
| 98 | 14 | COUNT_COMMA | 22,586 | ue Categories 12 Question types 28 Dialects 6 Personas 5 Formulations 6 Scenarios 8 Bloom levels 4 Train (unique cells) 22,586 (3,203) Dev (unique cells) 2,431 (315) Test (unique cells) 358 (290) Held |
| 99 | 14 | COUNT_COMMA | 3,203 | ories 12 Question types 28 Dialects 6 Personas 5 Formulations 6 Scenarios 8 Bloom levels 4 Train (unique cells) 22,586 (3,203) Dev (unique cells) 2,431 (315) Test (unique cells) 358 (290) Held-out (un |
| 100 | 14 | COUNT_COMMA | 2,431 | Dialects 6 Personas 5 Formulations 6 Scenarios 8 Bloom levels 4 Train (unique cells) 22,586 (3,203) Dev (unique cells) 2,431 (315) Test (unique cells) 358 (290) Held-out (unique cells) 3,618 (240) sta |
| 101 | 14 | COUNT_COMMA | 3,618 | rain (unique cells) 22,586 (3,203) Dev (unique cells) 2,431 (315) Test (unique cells) 358 (290) Held-out (unique cells) 3,618 (240) stage. The seven released domains are fer- 1182 tilizer, disease, pe |
| 102 | 14 | COUNT_COMMA | 5,621 | ue Safety-critical domains 7 Question types 10 Dialects / personas 6 / 2 Scenarios 4 Bloom (analyze / apply / untagged) 5,621 / 5,569 / 34 Evaluation test split (unique cells) 346 (243) D.1 Full Chemi |
| 103 | 14 | COUNT_COMMA | 5,569 | y-critical domains 7 Question types 10 Dialects / personas 6 / 2 Scenarios 4 Bloom (analyze / apply / untagged) 5,621 / 5,569 / 34 Evaluation test split (unique cells) 346 (243) D.1 Full Chemical Audi |
| 104 | 14 | COUNT_COMMA | 7,437 | ,569 / 34 Evaluation test split (unique cells) 346 (243) D.1 Full Chemical Audit 1215 Chemical-trace coverage is 66.3% (7,437 of 1216 11,224 records); the remaining 33.7% describe 1217 non-chemical in |
| 105 | 14 | COUNT_COMMA | 11,224 | uation test split (unique cells) 346 (243) D.1 Full Chemical Audit 1215 Chemical-trace coverage is 66.3% (7,437 of 1216 11,224 records); the remaining 33.7% describe 1217 non-chemical interventions (c |
| 106 | 14 | DATASET_SIZE | 224 records | ion test split (unique cells) 346 (243) D.1 Full Chemical Audit 1215 Chemical-trace coverage is 66.3% (7,437 of 1216 11,224 records); the remaining 33.7% describe 1217 non-chemical interventions (cult |
| 107 | 14 | MODEL_NAME | Bloom | counts are in parentheses. Axis Value Categories 12 Question types 28 Dialects 6 Personas 5 Formulations 6 Scenarios 8 Bloom levels 4 Train (unique cells) 22,586 (3,203) Dev (unique cells) 2,431 (315) |
| 108 | 14 | REFERENCE | Table 5 | Table 5: General Knowledge QA diversification axes and data split. Unique-cell counts are in parentheses. Axis Value Categories |
| 109 | 14 | REFERENCE | Table 6 | 91 (smallholder farmer, extension worker), and 1192 four stress scenarios (normal, pest outbreak, 1193 flood, drought). Table 6 shows the released 1194 schema, and the record below is a representa- 11 |
| 110 | 14 | REFERENCE | Table 7 | erical dosage values, units, and 1209 chemical names are frozen across all six dialect 1210 variants of a given record. Table 7 reports the 1211 full domain, question-type, and Bloom-level 1212 breakd |
| 111 | 15 | COUNT_COMMA | 1,000 | nput-format mismatch between training and 1320 evaluation. 1321 G Farmer Benchmark 1322 Collection and composition. The 1,000 1323 released queries were sourced from three chan- 1324 nels, each repres |
| 112 | 15 | METRIC | recall | 7 Markdown reconstruction of the original vi- 1288 sual layout, and a flattened key-value Mark- 1289 down file for high-recall indexing. Table 13 1290 reports the per-level instance counts under- 1291 |
| 113 | 15 | REFERENCE | Table 8 | rrors are a dictionary-coverage ques- 1235 tion rather than a ground-truth-reliability one. 1236 E Safety Resource 1237 Table 8 reports the full 12-category taxonomy 1238 refusal triggers, while Table |
| 114 | 15 | REFERENCE | Table 10 | reliability one. 1236 E Safety Resource 1237 Table 8 reports the full 12-category taxonomy 1238 refusal triggers, while Table 10 reports the cor- 1239 responding severity framing; Table 9 reports 1240 |
| 115 | 15 | REFERENCE | Table 9 | the full 12-category taxonomy 1238 refusal triggers, while Table 10 reports the cor- 1239 responding severity framing; Table 9 reports 1240 the discriminative power ranking of the re- 1241 query slots |
| 116 | 15 | REFERENCE | Table 11 | 239 responding severity framing; Table 9 reports 1240 the discriminative power ranking of the re- 1241 query slots, and Table 11 reports their clarifi- 1242 cation triggers. Each of the six re-query s |
| 117 | 15 | REFERENCE | Table 12 | among those actually missing (Table 9), 1267 not an arbitrarily chosen one. 1268 E.1 Per-Dialect Refusal Breakdown 1269 Table 12 reports the full per-dialect count for 1270 the 323-instance Safety QA  |
| 118 | 15 | REFERENCE | Table 13 | truction of the original vi- 1288 sual layout, and a flattened key-value Mark- 1289 down file for high-recall indexing. Table 13 1290 reports the per-level instance counts under- 1291 lying the three- |
| 119 | 15 | REFERENCE | Table 14 | ble 13 1290 reports the per-level instance counts under- 1291 lying the three-level complexity stratification, 1292 and Table 14 reports the resulting train/vali- 1293 dation/test split across the six |
| 120 | 16 | PERCENTAGE | 0.0% | already applied Table 12: KrishokTech-4B Safety QA refusals by dialect (n=323 total). Dialect n Refused Standard 51 0 (0.0%) Chittagonian 49 0 (0.0%) Noakhailli 53 0 (0.0%) Rangpuri 69 0 (0.0%) Barish |
| 121 | 16 | PERCENTAGE | 1.9% | ard 51 0 (0.0%) Chittagonian 49 0 (0.0%) Noakhailli 53 0 (0.0%) Rangpuri 69 0 (0.0%) Barishal 48 0 (0.0%) Sylheti 53 1 (1.9%) Total 323 1 (0.31%) Table 13: Table Reasoning QA instances by com- plexity |
| 122 | 16 | PERCENTAGE | 0.31% | ttagonian 49 0 (0.0%) Noakhailli 53 0 (0.0%) Rangpuri 69 0 (0.0%) Barishal 48 0 (0.0%) Sylheti 53 1 (1.9%) Total 323 1 (0.31%) Table 13: Table Reasoning QA instances by com- plexity level. Level Insta |
| 123 | 16 | COUNT_COMMA | 11,058 | 1.9%) Total 323 1 (0.31%) Table 13: Table Reasoning QA instances by com- plexity level. Level Instances L1: cell lookup 11,058 L2: row reasoning 12,540 L3: column aggregation 2,052 Total 25,650 16 |
| 124 | 16 | COUNT_COMMA | 12,540 | Table 13: Table Reasoning QA instances by com- plexity level. Level Instances L1: cell lookup 11,058 L2: row reasoning 12,540 L3: column aggregation 2,052 Total 25,650 16 |
| 125 | 16 | COUNT_COMMA | 2,052 | instances by com- plexity level. Level Instances L1: cell lookup 11,058 L2: row reasoning 12,540 L3: column aggregation 2,052 Total 25,650 16 |
| 126 | 16 | COUNT_COMMA | 25,650 | com- plexity level. Level Instances L1: cell lookup 11,058 L2: row reasoning 12,540 L3: column aggregation 2,052 Total 25,650 16 |
| 127 | 16 | REFERENCE | Table 8 | Table 8: The 12-category agricultural safety taxonomy (T3) and corresponding refusal triggers. Category Refusal trigger Categor |
| 128 | 16 | REFERENCE | Table 9 | guarantee veterinary_scope Livestock/animal-health request ethical_boundary Request to conceal risk or falsify records Table 9: Discriminative Power (DP) ranking of re- query slots (T4). Slot Mean DP  |
| 129 | 16 | REFERENCE | Table 10 | Slot Mean DP Rank crop 0.91 1 symptom 0.84 2 onset 0.62 3 severity 0.45 4 growth_stage 0.38 5 chemical_ history 0.31 6 Table 10: Full T3 safety taxonomy with severity tiers. Category Severity framing  |
| 130 | 16 | REFERENCE | Table 11 | nt over_promise Minor: optimistic framing; Severe: guarantee ethical_boundary Minor: omission; Severe: active deception Table 11: The six agricultural slots underlying T4 re-query. Slot What it disamb |
| 131 | 16 | REFERENCE | Table 12 | pread growth_stage Seedling, vegetative, flowering, or maturity chemical_history What, if anything, was already applied Table 12: KrishokTech-4B Safety QA refusals by dialect (n=323 total). Dialect n  |
| 132 | 16 | REFERENCE | Table 13 | an 49 0 (0.0%) Noakhailli 53 0 (0.0%) Rangpuri 69 0 (0.0%) Barishal 48 0 (0.0%) Sylheti 53 1 (1.9%) Total 323 1 (0.31%) Table 13: Table Reasoning QA instances by com- plexity level. Level Instances L1 |
| 133 | 17 | PERCENTAGE | 90% | ng the can- 1387 didate pool from 2,946 units to a median of 1388 5 to 15 relevant units, a reduction of more 1389 than 90%. Stage 4 has a human annotator 1390 with agricultural domain expertise revie |
| 134 | 17 | COUNT_COMMA | 25,650 | Table 14: Dialect / split breakdown of the 25,650 Table QA records. Dialect Train Val. Test Total Standard 3,430 399 446 4,275 Sylheti 3,430 399 446 4,275 Chittagonian 3 |
| 135 | 17 | COUNT_COMMA | 3,430 | Table 14: Dialect / split breakdown of the 25,650 Table QA records. Dialect Train Val. Test Total Standard 3,430 399 446 4,275 Sylheti 3,430 399 446 4,275 Chittagonian 3,430 399 446 4,275 Noakhailli 3 |
| 136 | 17 | COUNT_COMMA | 4,275 | able 14: Dialect / split breakdown of the 25,650 Table QA records. Dialect Train Val. Test Total Standard 3,430 399 446 4,275 Sylheti 3,430 399 446 4,275 Chittagonian 3,430 399 446 4,275 Noakhailli 3, |
| 137 | 17 | COUNT_COMMA | 20,580 | nian 3,430 399 446 4,275 Noakhailli 3,430 399 446 4,275 Barishal 3,430 399 446 4,275 Rangpuri 3,430 399 446 4,275 Total 20,580 2,394 2,676 25,650 in-person structured interviews with small- 1327 holde |
| 138 | 17 | COUNT_COMMA | 2,394 | 430 399 446 4,275 Noakhailli 3,430 399 446 4,275 Barishal 3,430 399 446 4,275 Rangpuri 3,430 399 446 4,275 Total 20,580 2,394 2,676 25,650 in-person structured interviews with small- 1327 holder farme |
| 139 | 17 | COUNT_COMMA | 2,676 | 9 446 4,275 Noakhailli 3,430 399 446 4,275 Barishal 3,430 399 446 4,275 Rangpuri 3,430 399 446 4,275 Total 20,580 2,394 2,676 25,650 in-person structured interviews with small- 1327 holder farmers in  |
| 140 | 17 | COUNT_COMMA | 1,000 | und-truth assignment for the Real- 1378 World Farmer Benchmark proceeds in five 1379 stages. Stage 1 parses each of the 1,000 1380 collected queries into an attribute tuple (tar- 1381 get crop, diseas |
| 141 | 17 | COUNT_COMMA | 2,946 | ueries into an attribute tuple (tar- 1381 get crop, disease or symptom, agronomic cat- 1382 egory). Stage 2 indexes the 2,946 seman- 1383 tic units of the knowledge corpus over the 1384 same three att |
| 142 | 17 | REFERENCE | Table 14 | Table 14: Dialect / split breakdown of the 25,650 Table QA records. Dialect Train Val. Test Total Standard 3,430 399 446 4,275 S |
| 143 | 18 | PERCENTAGE | 90% | 1419 2,946 Semantic Units full corpus, indexed by crop, symptom, category Median 5–15 attribute-filtered candi- dates, >90% reduction Top-1 expert-verified unit Provenance-Grounded Reference Answer Fi |
| 144 | 18 | PERCENTAGE | 100% | 426 formation outside the cited source. All 69 1427 queries were confirmed unchanged by this sec- 1428 ond pass (69/69, 100% raw agreement), which 1429 is consistent with the primary annotation al- 14 |
| 145 | 18 | PERCENTAGE | 6.9% | versarial sample 1442 would not be. More importantly, this pass 1443 covers only 69 of the 1,000 released queries 1444 (6.9%) and none of the 700 queries sourced 1445 from Facebook or the Krishi Bangl |
| 146 | 18 | COUNT_COMMA | 2,946 | tee used throughout KrishokTech. 1419 2,946 Semantic Units full corpus, indexed by crop, symptom, category Median 5–15 attribute-filtered candi- dates, >90% reduct |
| 147 | 18 | COUNT_COMMA | 1,000 | hat a larger, deliberately adversarial sample 1442 would not be. More importantly, this pass 1443 covers only 69 of the 1,000 released queries 1444 (6.9%) and none of the 700 queries sourced 1445 from |
| 148 | 18 | DATASET_SIZE | 1427
queries | ated answer addressed 1425 the farmer’s question without drawing on in- 1426 formation outside the cited source. All 69 1427 queries were confirmed unchanged by this sec- 1428 ond pass (69/69, 100% ra |
| 149 | 18 | DATASET_SIZE | 700 queries | would not be. More importantly, this pass 1443 covers only 69 of the 1,000 released queries 1444 (6.9%) and none of the 700 queries sourced 1445 from Facebook or the Krishi Bangla portal 1446 (§G), wh |
| 150 | 18 | DATASET_SIZE | 350 answers | armer query), and ground_truth 1467 (the verified, provenance-backed answer); mod- 1468 els are evaluated against these 350 answers 1469 using Bengali token-F1 and deterministic nu- 1470 meric halluci |
| 151 | 18 | METRIC | Top-1 | antic Units full corpus, indexed by crop, symptom, category Median 5–15 attribute-filtered candi- dates, >90% reduction Top-1 expert-verified unit Provenance-Grounded Reference Answer Figure 3: Attrib |
| 152 | 18 | METRIC | F1  | the verified, provenance-backed answer); mod- 1468 els are evaluated against these 350 answers 1469 using Bengali token-F1 and deterministic nu- 1470 meric hallucination checks (Section 5). 1471 H Eva |
| 153 | 18 | MODEL_NAME | GPT- | lness, Dialect 1482 Authenticity, Grounding (oracle only), and 1483 Safety, scored on a 1–5 scale by an LLM judge 1484 (GPT-4o-mini); Table 15 reports Helpfulness, 1485 Dialect Authenticity, and Safet |
| 154 | 18 | REFERENCE | Figure 3 | an 5–15 attribute-filtered candi- dates, >90% reduction Top-1 expert-verified unit Provenance-Grounded Reference Answer Figure 3: Attribute-guided search-space reduc- tion for the Farmer Benchmark, co |
| 155 | 18 | REFERENCE | Section 5 | evaluated against these 350 answers 1469 using Bengali token-F1 and deterministic nu- 1470 meric hallucination checks (Section 5). 1471 H Evaluation Protocol Details 1472 Metrics. Deterministic metric |
| 156 | 18 | REFERENCE | Table 15 | 1482 Authenticity, Grounding (oracle only), and 1483 Safety, scored on a 1–5 scale by an LLM judge 1484 (GPT-4o-mini); Table 15 reports Helpfulness, 1485 Dialect Authenticity, and Safety for compact-  |
| 157 | 19 | PERCENTAGE | 12.5% | nt, 1527 and Safety QA, and six-system inference cost 1528 tractable for Table QA (335 of 2,676 test in- 1529 stances, ∼12.5%), while preserving dialect and 1530 category stratification. 1531 H.1 LLM- |
| 158 | 19 | PERCENTAGE | 44.78% | shokChat-4B, referenced from §5.4. GPT- 1598 OSS-120B is the strongest oracle-condition sys- 1599 tem on this track (EM 44.78%, F1 55.86%), 1600 19 |
| 159 | 19 | PERCENTAGE | 55.86% | , referenced from §5.4. GPT- 1598 OSS-120B is the strongest oracle-condition sys- 1599 tem on this track (EM 44.78%, F1 55.86%), 1600 19 |
| 160 | 19 | COUNT_COMMA | 2,676 | tractable for General, Treatment, 1527 and Safety QA, and six-system inference cost 1528 tractable for Table QA (335 of 2,676 test in- 1529 stances, ∼12.5%), while preserving dialect and 1530 category |
| 161 | 19 | DATASET_SIZE | 1522
instances | e full released split: 358 1520 General QA, 346 Treatment QA, 323 Safety 1521 QA (51 refusal-mode and 272 re-query-mode 1522 instances; see Appendix E.1 for the dialect 1523 composition), 335 Table QA |
| 162 | 19 | METRIC | F1 | e single-epoch vs. 1586 second-epoch fine-tuning ablation. 1587 I.1 Full General QA Results 1588 Table 15 reports Token F1, numeric hallucina- 1589 tion rate, Factual%, and the three LLM-judge 1590 di |
| 163 | 19 | MODEL_NAME | gpt- | dialect and 1530 category stratification. 1531 H.1 LLM-Judge System Prompts 1532 Both prompts are issued to 1533 openai/gpt-4o-mini via OpenRouter at 1534 temperature 0.0 in JSON output mode. We 1535  |
| 164 | 19 | MODEL_NAME | GPT | sed-book and oracle Exact 1596 Match and token F1 for every baseline and for 1597 KrishokTech-4B, referenced from §5.4. GPT- 1598 OSS-120B is the strongest oracle-condition sys- 1599 tem on this track |
| 165 | 19 | REFERENCE | Section 5 | Ablation 1580 This appendix reports the full per-model re- 1581 sults underlying the summary tables and 1582 claims in Section 5: the complete General 1583 QA judge-dimension table, the full Table QA  |
| 166 | 19 | REFERENCE | Table 15 | liance analysis, and the single-epoch vs. 1586 second-epoch fine-tuning ablation. 1587 I.1 Full General QA Results 1588 Table 15 reports Token F1, numeric hallucina- 1589 tion rate, Factual%, and the  |
| 167 | 19 | REFERENCE | Table 16 | 1592 KrishokTech-4B, under both the closed-book 1593 and oracle conditions (§5.1). 1594 I.2 Full Table QA Results 1595 Table 16 reports closed-book and oracle Exact 1596 Match and token F1 for every b |
| 168 | 20 | PERCENTAGE | 19.83% | Help, Dialect, and Safety are LLM-judge scores (1–5). Note: KrishokTech-4B closed-book and oracle hallucination rates (19.83%) are coincidentally identical despite differing F1 and Factual%. Model Con |
| 169 | 20 | PERCENTAGE | 34.63% | it for two, and leaves KrishokTech-4B un- changed. well above the next-best zero-shot baseline, 1601 Gemini-2.5-FL (EM 34.63%, F1 46.72%). 1602 I.3 Exploratory Safety-Compliance 1603 Analysis 1604 Sec |
| 170 | 20 | PERCENTAGE | 46.72% | , and leaves KrishokTech-4B un- changed. well above the next-best zero-shot baseline, 1601 Gemini-2.5-FL (EM 34.63%, F1 46.72%). 1602 I.3 Exploratory Safety-Compliance 1603 Analysis 1604 Section 3.5 i |
| 171 | 20 | PERCENTAGE | 17.65% | 2) behavior. Compliance % is the count- weighted average of both modes. Model Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6 |
| 172 | 20 | PERCENTAGE | 20.22% | vior. Compliance % is the count- weighted average of both modes. Model Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LL |
| 173 | 20 | PERCENTAGE | 19.81% | ompliance % is the count- weighted average of both modes. Model Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1 |
| 174 | 20 | PERCENTAGE | 29.41% | count- weighted average of both modes. Model Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2. |
| 175 | 20 | PERCENTAGE | 16.91% | weighted average of both modes. Model Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT |
| 176 | 20 | PERCENTAGE | 18.89% | d average of both modes. Model Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-12 |
| 177 | 20 | PERCENTAGE | 35.29% | odes. Model Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23 |
| 178 | 20 | PERCENTAGE | 1.10% | odel Refusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% Kr |
| 179 | 20 | PERCENTAGE | 6.50% | efusal Re-query Compliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokC |
| 180 | 20 | PERCENTAGE | 11.76% | pliance Gemini-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00%  |
| 181 | 20 | PERCENTAGE | 2.79% | i-2.5-FL 17.65% 20.22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00% 0.31% 20 |
| 182 | 20 | PERCENTAGE | 37.25% | 22% 19.81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00% 0.31% 20 |
| 183 | 20 | PERCENTAGE | 21.15% | 81% Gemma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00% 0.31% 20 |
| 184 | 20 | PERCENTAGE | 23.79% | ma-4-26B 29.41% 16.91% 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00% 0.31% 20 |
| 185 | 20 | PERCENTAGE | 1.96% | 18.89% Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00% 0.31% 20 |
| 186 | 20 | PERCENTAGE | 0.00% | % Qwen-2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00% 0.31% 20 |
| 187 | 20 | PERCENTAGE | 0.31% | -2.5-7B 35.29% 1.10% 6.50% LLaMA-3.1-8B 11.76% 1.10% 2.79% GPT-OSS-120B 37.25% 21.15% 23.79% KrishokTech-4B 1.96% 0.00% 0.31% 20 |
| 188 | 20 | METRIC | F1  | Note: KrishokTech-4B closed-book and oracle hallucination rates (19.83%) are coincidentally identical despite differing F1 and Factual%. Model Cond. F1 Halluc% Factual% Help Dialect Safety Gemini-2.5- |
| 189 | 20 | METRIC | Exact Match | pliance is al- 1616 Table 16: Full Table QA results (n=335), including the unreleased second-epoch checkpoint (SFT2ep), Exact Match and Token F1 (%). Closed-Book Oracle Model EM F1 EM F1 Gemini-2.5-FL |
| 190 | 20 | MODEL_NAME | Gemma | ect Safety Gemini-2.5-FL CB 0.104 37.15 0.28 4.958 4.955 4.997 Gemini-2.5-FL Oracle 0.281 32.40 13.41 4.701 4.659 4.962 Gemma-4-26B CB 0.087 32.12 0.00 4.958 4.972 4.993 Gemma-4-26B Oracle 0.253 29.05 |
| 191 | 20 | MODEL_NAME | LLaMA | 701 4.659 4.962 Gemma-4-26B CB 0.087 32.12 0.00 4.958 4.972 4.993 Gemma-4-26B Oracle 0.253 29.05 9.50 4.444 4.413 4.925 LLaMA-3.1-8B CB 0.165 10.06 2.51 3.126 2.916 4.710 LLaMA-3.1-8B Oracle 0.230 16. |
| 192 | 20 | MODEL_NAME | Qwen | 4 4.413 4.925 LLaMA-3.1-8B CB 0.165 10.06 2.51 3.126 2.916 4.710 LLaMA-3.1-8B Oracle 0.230 16.48 9.22 3.860 3.626 4.754 Qwen-2.5-7B CB 0.136 11.17 0.28 3.818 3.140 4.810 Qwen-2.5-7B Oracle 0.198 20.54 |
| 193 | 20 | MODEL_NAME | GPT- | 860 3.626 4.754 Qwen-2.5-7B CB 0.136 11.17 0.28 3.818 3.140 4.810 Qwen-2.5-7B Oracle 0.198 20.54 4.05 4.184 3.435 4.818 GPT-OSS-120B CB 0.113 36.20 0.34 4.493 3.955 4.985 GPT-OSS-120B Oracle 0.191 30. |
| 194 | 20 | MODEL_NAME | GPT | uc. % Closed-Book Oracle Figure 4: General QA hallucination rate, closed- book vs. oracle context, per model (Table 15; GPT- OSS-120B values from Table 2, §I.1). Oracle con- text reduces hallucination |
| 195 | 20 | REFERENCE | Table 15 | Table 15: Full General QA results (n=358), including the unreleased second-epoch checkpoint (SFT2ep). Halluc% and Factual% are d |
| 196 | 20 | REFERENCE | Figure 4 | mini-2.5-FL Gemma-4-26B LLaMA-3.1-8B Qwen-2.5-7B GPT-OSS-120B KrishokTech-4B 0 10 20 30 40 Halluc. % Closed-Book Oracle Figure 4: General QA hallucination rate, closed- book vs. oracle context, per mo |
| 197 | 20 | REFERENCE | Table 2 | igure 4: General QA hallucination rate, closed- book vs. oracle context, per model (Table 15; GPT- OSS-120B values from Table 2, §I.1). Oracle con- text reduces hallucination for three systems, in- cr |
| 198 | 20 | REFERENCE | Section 3 | ero-shot baseline, 1601 Gemini-2.5-FL (EM 34.63%, F1 46.72%). 1602 I.3 Exploratory Safety-Compliance 1603 Analysis 1604 Section 3.5 introduces Safety QA as a bench- 1605 mark track; this subsection re |
| 199 | 20 | REFERENCE | Table 17 | uery behavior a zero-shot 1613 model already has, not whether KrishokTech 1614 by itself enables safety alignment. 1615 Table 17 shows that safety compliance is al- 1616 Table 16: Full Table QA result |
| 200 | 20 | REFERENCE | Table 16 | not whether KrishokTech 1614 by itself enables safety alignment. 1615 Table 17 shows that safety compliance is al- 1616 Table 16: Full Table QA results (n=335), including the unreleased second-epoch c |
| 201 | 21 | PERCENTAGE | 23.79% | . The strongest 1618 zero-shot model, GPT-OSS-120B, follows the 1619 intended refusal or re-query behavior on only 1620 23.79% of instances, and LLaMA-3.1-8B on 1621 just 2.79%. KrishokTech-4B complie |
| 202 | 21 | PERCENTAGE | 2.79% | follows the 1619 intended refusal or re-query behavior on only 1620 23.79% of instances, and LLaMA-3.1-8B on 1621 just 2.79%. KrishokTech-4B complies on 1 1622 of 323 instances (0.31%), and the second |
| 203 | 21 | PERCENTAGE | 0.31% | only 1620 23.79% of instances, and LLaMA-3.1-8B on 1621 just 2.79%. KrishokTech-4B complies on 1 1622 of 323 instances (0.31%), and the second- 1623 epoch checkpoint reaches the identical rate 1624 (T |
| 204 | 21 | PERCENTAGE | 0% | 3 liteness/redirection marginally, but degrades 1664 General QA and collapses Treatment QA 1665 closed-book accuracy to 0%, with Safety QA 1666 compliance unchanged at 0.31% either way. 1667 The Treat |
| 205 | 21 | PERCENTAGE | 35.55% | tment 1670 QA questions, but 0 of 346 evaluated recom- 1671 mendations are verifiably correct, against 123 1672 of 346 (35.55%) after one epoch (step 2,680). 1673 We read this as overfitting to the Ge |
| 206 | 21 | COUNT_COMMA | 5,362 | % either way. 1667 The Treatment QA closed-book collapse is 1668 the decisive result: after the second epoch 1669 (step 5,362), the model still answers Treatment 1670 QA questions, but 0 of 346 evalua |
| 207 | 21 | COUNT_COMMA | 2,680 | of 346 evaluated recom- 1671 mendations are verifiably correct, against 123 1672 of 346 (35.55%) after one epoch (step 2,680). 1673 We read this as overfitting to the General 1674 QA surface-form dive |
| 208 | 21 | DATASET_SIZE | 323 instances | ry behavior on only 1620 23.79% of instances, and LLaMA-3.1-8B on 1621 just 2.79%. KrishokTech-4B complies on 1 1622 of 323 instances (0.31%), and the second- 1623 epoch checkpoint reaches the identic |
| 209 | 21 | DATASET_SIZE | 1710
sets | to one canonical 1708 key), and precision, recall, and their harmonic 1709 mean are computed over the resulting mention 1710 sets. We additionally report Dosage Compli- 1711 ance, a binary indicator o |
| 210 | 21 | METRIC | accuracy | y QA po- 1663 liteness/redirection marginally, but degrades 1664 General QA and collapses Treatment QA 1665 closed-book accuracy to 0%, with Safety QA 1666 compliance unchanged at 0.31% either way. 16 |
| 211 | 21 | METRIC | exact match | kpoint 1678 improves Table QA. We note that this 0% fig- 1679 ure reflects our Correct% metric’s requirement 1680 of an exact match on chemical name, dosage 1681 value, and unit; Appendix I.5 decompos |
| 212 | 21 | METRIC | precision | f an exact match on chemical name, dosage 1681 value, and unit; Appendix I.5 decomposes this 1682 into chemical-mention precision/recall, which 1683 clarifies that the checkpoint still names plau- 168 |
| 213 | 21 | METRIC | recall | match on chemical name, dosage 1681 value, and unit; Appendix I.5 decomposes this 1682 into chemical-mention precision/recall, which 1683 clarifies that the checkpoint still names plau- 1684 sible che |
| 214 | 21 | METRIC | F1 | 701 ness from genuine chemical-reasoning failure, 1702 we additionally compute a chemical-mention 1703 Precision/Recall/F1 (Chem-PRF) score: pre- 1704 dicted and gold chemical mentions are both 1705 c |
| 215 | 21 | MODEL_NAME | GPT- | ready weak among the zero-shot baselines and 1617 drops further after fine-tuning. The strongest 1618 zero-shot model, GPT-OSS-120B, follows the 1619 intended refusal or re-query behavior on only 1620 |
| 216 | 21 | MODEL_NAME | LLaMA | -shot model, GPT-OSS-120B, follows the 1619 intended refusal or re-query behavior on only 1620 23.79% of instances, and LLaMA-3.1-8B on 1621 just 2.79%. KrishokTech-4B complies on 1 1622 of 323 instan |
| 217 | 21 | REFERENCE | Table 18 | -4B complies on 1 1622 of 323 instances (0.31%), and the second- 1623 epoch checkpoint reaches the identical rate 1624 (Table 18), so the drop is not an artifact of 1625 stopping fine-tuning early. A  |
| 218 | 21 | REFERENCE | Table 19 | a recognized agricultural unit (e.g., kg/ha, 1714 ml/L), independent of whether the value itself 1715 is correct. 1716 Table 19 reports Chem-PRF and Dosage 1717 Compliance alongside Correct% for every |
| 219 | 22 | PERCENTAGE | 0% | 9) is close to its own 1735 oracle-condition value (0.460) and to several 1736 zero-shot baselines, indicating that its 0% 1737 Correct% reflects formatting strictness rather 1738 than a complete loss |
| 220 | 22 | METRIC | F1 | eased) vs. second-epoch (SFT2ep, not released) ablation. Track Metric KrishokTech-4B SFT2ep ∆(2ep−1ep) General QA Token F1 (CB) 0.314 0.276 −0.038 General QA Halluc% (CB) 19.8 24.0 +4.2 General QA Fac |
| 221 | 22 | METRIC | precision | §5.2: LLaMA-3.1-8B and 1721 Qwen-2.5-7B, which recommend a treatment 1722 on only a small share of instances, show 1723 precision at or above recall (e.g., LLaMA- 1724 3.1-8B closed-book: 0.260 vs. 0. |
| 222 | 22 | METRIC | recall | 1721 Qwen-2.5-7B, which recommend a treatment 1722 on only a small share of instances, show 1723 precision at or above recall (e.g., LLaMA- 1724 3.1-8B closed-book: 0.260 vs. 0.162), consis- 1725 tent |
| 223 | 22 | MODEL_NAME | LLaMA | Treatment QA system. The decomposition 1719 is consistent with each system’s omission pro- 1720 file reported in §5.2: LLaMA-3.1-8B and 1721 Qwen-2.5-7B, which recommend a treatment 1722 on only a sma |
| 224 | 22 | MODEL_NAME | Qwen | The decomposition 1719 is consistent with each system’s omission pro- 1720 file reported in §5.2: LLaMA-3.1-8B and 1721 Qwen-2.5-7B, which recommend a treatment 1722 on only a small share of instances |
| 225 | 22 | MODEL_NAME | Gemma | closed-book: 0.260 vs. 0.162), consis- 1725 tent with cautious, often-omitted recommen- 1726 dations; Gemini-2.5-FL and Gemma-4-26B, 1727 which answer more freely, show the opposite 1728 pattern (Gemm |
| 226 | 22 | MODEL_NAME | GPT- | 4 0.478 0.409 0.415 0.356 Gemma-4-26B CB 38.73 0.364 0.680 0.455 0.269 Gemma-4-26B Oracle 54.05 0.588 0.775 0.644 0.397 GPT-OSS-120B CB 32.92 0.422 0.377 0.363 0.243 GPT-OSS-120B Oracle 49.79 0.553 0. |
| 227 | 22 | REFERENCE | Table 18 | Table 18: Single-epoch (KrishokTech-4B, released) vs. second-epoch (SFT2ep, not released) ablation. Track Metric KrishokTech-4B |
| 228 | 22 | REFERENCE | Table 20 | on-level overlap, 1744 is the property that is safety-relevant in de- 1745 ployment. 1746 I.6 Qualitative Examples 1747 Table 20 gives one representative example per 1748 failure or success mode discu |
| 229 | 22 | REFERENCE | Table
1752 | hallucination (§4.3), a 1750 correct T3 refusal, a correct T4 re-query (§3.5), 1751 a grounded General QA answer, and a Table 1752 QA cell-lookup error. Each is shown in the 1753 original Bengali alon |
| 230 | 22 | REFERENCE | Table 19 | wer, and a Table 1752 QA cell-lookup error. Each is shown in the 1753 original Bengali alongside an English gloss. 1754 Table 19: Treatment QA chemical-mention Preci- sion/Recall/F1 (Chem-PRF) and Dos |
| 231 | 22 | REFERENCE | Figure 5 | 9 0.366 SFT2ep Oracle 41.62 0.459 0.521 0.460 0.294 0 0.2 0.4 0.6 0.8 0 0.2 0.4 0.6 Recall Precision Closed-Book Oracle Figure 5: Treatment QA chemical-mention preci- sion vs. recall (Chem-PRF, Table  |
| 232 | 23 | CHEMICAL | mancozeb | উত্তর: কােবর্ũািজম৫Íাম/িলটারেƽ কর‍ুন। রায়: হঁালুিসেনশন Q: What should I spray if my rice shows blast disease? Gold: Mix mancozeb 2 g/L water and spray. Prediction: Spray carbendazim 5 g/L. Verdict: ha |
| 233 | 23 | CHEMICAL | carbendazim | েনশন Q: What should I spray if my rice shows blast disease? Gold: Mix mancozeb 2 g/L water and spray. Prediction: Spray carbendazim 5 g/L. Verdict: hallucination – neither chemical nor dosage is in th |
| 234 | 23 | DOSAGE | 150 kg/ha | ১৫০েকিজ/েহĝর মেডেলরউত্তর: ১২০েকিজ/েহĝর Q: According to the table, what is the per-hectare urea application rate? Gold: 150 kg/ha. Prediction: 120 kg/ha. Verdict: incorrect cell lookup – wrong row read |
| 235 | 23 | DOSAGE | 120 kg/ha | তর: ১২০েকিজ/েহĝর Q: According to the table, what is the per-hectare urea application rate? Gold: 150 kg/ha. Prediction: 120 kg/ha. Verdict: incorrect cell lookup – wrong row read from the source table |
| 236 | 23 | REFERENCE | Table 20 | Table 20: Representative qualitative examples, one per case, in Bengali with an English gloss. Case Bengali (original) English g |
| 237 | 24 | PERCENTAGE | 10% | norm 0.3). The learning rate 1775 followed a cosine decay schedule with a peak 1776 of 2 × 10−4 and 268 warmup steps (∼10% of 1777 the first epoch). We used a per-device micro- 1778 batch size of 4 wi |
| 238 | 24 | PERCENTAGE | 19.83% | 7 × 10−5 under the pooled-variance z- 1813 test, and is marked † in Table 2. KrishokTech- 1814 4B’s closed-book GenHal (19.83%) is lower 1815 than the high-hallucination zero-shot base- 1816 lines but |
| 239 | 24 | PERCENTAGE | 10.06% | Hal (19.83%) is lower 1815 than the high-hallucination zero-shot base- 1816 lines but remains above LLaMA-3.1-8B’s 1817 10.06%; we therefore do not mark it as 1818 significant against the best zero-sh |
| 240 | 24 | PERCENTAGE | 35.55% | ainst the best zero-shot baseline. 1819 Treatment QA (Table 2), N = 346. 1820 KrishokTech-4B’s closed-book TrtCor 1821 (35.55%) against Gemini-2.5-FL (43.64%) 1822 gives p = 0.0290 (significant at α = |
| 241 | 24 | PERCENTAGE | 43.64% | ne. 1819 Treatment QA (Table 2), N = 346. 1820 KrishokTech-4B’s closed-book TrtCor 1821 (35.55%) against Gemini-2.5-FL (43.64%) 1822 gives p = 0.0290 (significant at α = 0.05 1823 but not at α = 0.01) |
| 242 | 24 | PERCENTAGE | 38.73% | ini-2.5-FL (43.64%) 1822 gives p = 0.0290 (significant at α = 0.05 1823 but not at α = 0.01); against Gemma-4-26B 1824 (38.73%) gives p = 0.386 (not significant). We 1825 read this as KrishokTech-4B b |
| 243 | 24 | PERCENTAGE | 23.14% | statistically tied 1839 with Gemma-4-26B in F1 despite the numeric 1840 gap). On hallucination rate, Gemma-4-26B 1841 (23.14%) against KrishokTech-4B (41.14%) 1842 gives p = 2.03 × 10−7 (†); Gemini-2. |
| 244 | 24 | PERCENTAGE | 41.14% | mma-4-26B in F1 despite the numeric 1840 gap). On hallucination rate, Gemma-4-26B 1841 (23.14%) against KrishokTech-4B (41.14%) 1842 gives p = 2.03 × 10−7 (†); Gemini-2.5-FL 1843 (38.29%) against Kris |
| 245 | 24 | PERCENTAGE | 38.29% | ion rate, Gemma-4-26B 1841 (23.14%) against KrishokTech-4B (41.14%) 1842 gives p = 2.03 × 10−7 (†); Gemini-2.5-FL 1843 (38.29%) against KrishokTech-4B gives p = 1844 0.441 (not significant). 1845 Summ |
| 246 | 24 | COUNT_COMMA | 2,680 | proj, o_proj, gate_proj, up_proj, 1761 down_proj) on top of a 4-bit-quantized base 1762 checkpoint, for one epoch (step 2,680 of a 1763 planned 5,362-step, two-epoch run), with 1764 the second-epoch c |
| 247 | 24 | COUNT_COMMA | 5,362 | up_proj, 1761 down_proj) on top of a 4-bit-quantized base 1762 checkpoint, for one epoch (step 2,680 of a 1763 planned 5,362-step, two-epoch run), with 1764 the second-epoch checkpoint SFT2ep (§I.4) 1 |
| 248 | 24 | COUNT_COMMA | 4,096 | ze of 4 with 4 gradient accumulation 1779 steps (effective global batch size 16) at a max- 1780 imum sequence length of 4,096 tokens, with 1781 model seed 42 and data seed 3407. 1782 K Significance Te |
| 249 | 24 | METRIC | precision | steps. 1768 Training was conducted on a single NVIDIA 1769 L4 GPU (24GB VRAM, Google Colab Pro) 1770 in bfloat16 mixed precision using Unsloth and 1771 Hugging Face TRL’s SFTTrainer. We opti- 1772 miz |
| 250 | 24 | METRIC | F1 | and flag 1789 that as a remaining gap rather than imply it 1790 has been checked. For continuous metrics (To- 1791 ken F1) we use a two-sample z-test assuming 1792 a pooled F1 variance of ∼0.25; for p |
| 251 | 24 | MODEL_NAME | Gemma | J Training Configuration 1755 KrishokTech-4B (Gemma-4-E4B) is fine- 1756 tuned on the KrishokTech training split using 1757 Low-Rank Adaptation (LoRA; r = 32, α = 64, 1758 |
| 252 | 24 | MODEL_NAME | LLaMA | e 2), N = 358. 1809 KrishokTech-4B’s closed-book Token F1 1810 (0.314) against the strongest closed-book 1811 baseline, LLaMA-3.1-8B (0.165), gives 1812 p ≈6.7 × 10−5 under the pooled-variance z- 1813 |
| 253 | 24 | REFERENCE | Table 2 | per claims in §5.2 and §5.5 are built 1787 on; we did not compute significance for the 1788 oracle-condition columns of Table 2 and flag 1789 that as a remaining gap rather than imply it 1790 has been |
| 254 | 24 | REFERENCE | Table
2 | ificant results more con- 1806 servative – and note its absence rather than 1807 imply it was applied. 1808 General QA (Table 2), N = 358. 1809 KrishokTech-4B’s closed-book Token F1 1810 (0.314) again |
| 255 | 24 | REFERENCE | Table 3 | clears p < 0.05 does not clear 1831 the stricter p < 0.01 threshold we use for the 1832 marker. 1833 Farmer Benchmark (Table 3), N = 350. 1834 On Token F1, Gemini-2.5-FL (0.2196) against 1835 KrishokC |
| 256 | 25 | METRIC | F1  | 1855 On the out-of-distribution Farmer Bench- 1856 mark, KrishokTech-4B is statistically tied 1857 with Gemma-4-26B in F1 but significantly 1858 worse than Gemma-4-26B in hallucination 1859 rate, and  |
| 257 | 25 | MODEL_NAME | Gemma | Gemini-2.5-FL. 1855 On the out-of-distribution Farmer Bench- 1856 mark, KrishokTech-4B is statistically tied 1857 with Gemma-4-26B in F1 but significantly 1858 worse than Gemma-4-26B in hallucination  |

---

## PDF B: AgriTrust
- File: AgriTrust.pdf
- SHA-256: `9b30b7696db097f125ef6147fccecfd93b7cf2b0eab1e61fecbe8de3c3f4a150`
- Pages: 10
- Size: 1,783,608 bytes

### Page-by-page summary
| Page | Text chars | Tables | Images | Key claims |
|------|-----------|--------|--------|------------|
| 1 | 4,391 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC |
| 2 | 4,626 | 0 | 0 | COUNT_COMMA, METRIC, REFERENCE |
| 3 | 5,315 | 0 | 0 | COUNT_COMMA, MODEL_NAME, PERCENTAGE |
| 4 | 3,362 | 0 | 1 | COUNT_COMMA, DATASET_SIZE, PERCENTAGE, REFERENCE |
| 5 | 4,826 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC, PERCENTAGE, REFERENCE |
| 6 | 4,650 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC, PERCENTAGE, REFERENCE |
| 7 | 4,858 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC, PERCENTAGE, REFERENCE |
| 8 | 5,001 | 0 | 0 | COUNT_COMMA, DATASET_SIZE, METRIC, PERCENTAGE, REFERENCE |
| 9 | 5,303 | 0 | 0 | COUNT_COMMA, METRIC, PERCENTAGE |
| 10 | 5,857 | 0 | 0 | MODEL_NAME |

**Total claims extracted: 103**

### Numerical Claims Found
| # | Page | Category | Value | Context (truncated) |
|---|------|----------|-------|---------------------|
| 1 | 1 | COUNT_COMMA | 2,882 | thorita- tive publications issued by five Bangladeshi government and research organizations. The collection comprises a 2,882-node knowledge graph and 1,000 queries (900 an- swerable), with gold-node  |
| 2 | 1 | COUNT_COMMA | 1,000 | ed by five Bangladeshi government and research organizations. The collection comprises a 2,882-node knowledge graph and 1,000 queries (900 an- swerable), with gold-node mappings verified by three inde |
| 3 | 1 | COUNT_COMMA | 1,022 | nsists of: (i) 284 source PDFs from five Bangladeshi government and research organizations; (ii) 2,882 knowledge nodes (1,022 image-linked), each a provenance-preserving retrieval unit; (iii) a knowle |
| 4 | 1 | COUNT_COMMA | 19,768 | ii) 2,882 knowledge nodes (1,022 image-linked), each a provenance-preserving retrieval unit; (iii) a knowledge graph of 19,768 entities and 17,501 factual triples; (iv) 1,000 queries (900 answerable)  |
| 5 | 1 | COUNT_COMMA | 17,501 | nodes (1,022 image-linked), each a provenance-preserving retrieval unit; (iii) a knowledge graph of 19,768 entities and 17,501 factual triples; (iv) 1,000 queries (900 answerable) across three categor |
| 6 | 1 | DATASET_SIZE | 000 queries | by five Bangladeshi government and research organizations. The collection comprises a 2,882-node knowledge graph and 1,000 queries (900 an- swerable), with gold-node mappings verified by three indepen |
| 7 | 1 | DATASET_SIZE | 200 queries | nts use formal scientific Bengali. This register gap challenges lexical and dense retrieval in opposing ways. Of these, 200 queries cover safety-critical content (pesticide dosage, off-label chemical  |
| 8 | 1 | METRIC | accuracy | gured general-purpose dense embedding model (R@10=0.464); Reciprocal Rank Fusion of the two reaches the highest overall accuracy (R@10=0.539). This aggregate picture hides a sharp query-register effec |
| 9 | 2 | COUNT_COMMA | 2,882 | ance- grounded test collection for low-resource Bengali agri- cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated quer |
| 10 | 2 | COUNT_COMMA | 19,768 | lection for low-resource Bengali agri- cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated queries (available at https |
| 11 | 2 | COUNT_COMMA | 17,501 | esource Bengali agri- cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated queries (available at https://huggingface. c |
| 12 | 2 | COUNT_COMMA | 1,000 | - cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated queries (available at https://huggingface. co/datasets/RaiyanKha |
| 13 | 2 | METRIC | accuracy | ion with provenance grounding in a low-resource agricultural setting. Standard benchmarks typically emphasize aggregate accuracy scores, concealing subgroup failure across query registers, a limita- t |
| 14 | 2 | REFERENCE | Section 5 | , and an embedding API configuration audit. These four findings (summarized in the abstract) are de- veloped in full in Section 5, with mechanistic explanations in Section 6. 1.3 Contributions 1. AgRi |
| 15 | 2 | REFERENCE | Section 6 | These four findings (summarized in the abstract) are de- veloped in full in Section 5, with mechanistic explanations in Section 6. 1.3 Contributions 1. AgRiTrust benchmark collection. A provenance- gr |
| 16 | 2 | REFERENCE | Table 1 | modest gains [22], while multi-vector late-interaction models such as ColBERT [9] improve fine-grained token matching. Table 1: Positioning of AgRiTrust relative to closest prior benchmarks and system |
| 17 | 3 | PERCENTAGE | 65% | , IRRI, DAE, SRDI, MoA). The Ministry of Agriculture (MoA) and its extension arm (DAE) jointly contribute approximately 65% of the cor- pus via national farming handbooks, while specialized in- stitut |
| 18 | 3 | PERCENTAGE | 73% | sulting Markdown corpus (2,680 section-level passages) serves solely as an intermediate pre- processing artifact. While 73% of this underlying raw text originates from a prior QA benchmark [? ], AgRiT |
| 19 | 3 | PERCENTAGE | 100% | rk [? ], AgRiTrust’s primary contribution is restructuring this text into a novel, provenance-grounded knowledge graph (100% of KG entity and triple construction, node schema, and the full 900-query g |
| 20 | 3 | PERCENTAGE | 96% | de) and 17,501 factual triples via schema-guided, bounded open information extraction. Per-node entity coverage exceeds 96%. Source-Grounded Automated Verification. Node content (summary, symptoms, ma |
| 21 | 3 | PERCENTAGE | 96.1% | d to factual consistency and never becomes an open-ended quality rating. Across the resulting graph, entity coverage is 96.1% (2,771 of 2,882 nodes contain at least one extracted entity) and factual t |
| 22 | 3 | PERCENTAGE | 9.8% | coverage reaches 100%. Closed-Loop Refinement. Nodes falling below threshold (≤ 3 on any dimension; 283 of 2,882 nodes, 9.8%) were returned to Gemini-3.1-Flash-Lite together with the verifier’s specif |
| 23 | 3 | COUNT_COMMA | 2,680 | OCR, retaining document structure and page provenance for subsequent node construction. The resulting Markdown corpus (2,680 section-level passages) serves solely as an intermediate pre- processing ar |
| 24 | 3 | COUNT_COMMA | 2,729 | h explicitly indexes 915 unique crops (spanning horticulture, agroforestry, and aquaculture), 704 disease variants, and 2,729 chemical or pesticide entities. 3.2 Canonical Knowledge Node Construction  |
| 25 | 3 | COUNT_COMMA | 2,882 | ext, flagging any node whose entities do not appear in its cited passage for correction. Chunking. We segment text into 2,882 topic-coherent knowledge nodes, each corresponding to a single agricul- tu |
| 26 | 3 | COUNT_COMMA | 19,768 | and Cultiva- tion Practice (570) down to a long tail such as Food Safety (18). Entity and Triple Extraction. We extract 19,768 entities (6.9/node) and 17,501 factual triples via schema-guided, bounded |
| 27 | 3 | COUNT_COMMA | 17,501 | ) down to a long tail such as Food Safety (18). Entity and Triple Extraction. We extract 19,768 entities (6.9/node) and 17,501 factual triples via schema-guided, bounded open information extraction. P |
| 28 | 3 | COUNT_COMMA | 2,771 | ctual consistency and never becomes an open-ended quality rating. Across the resulting graph, entity coverage is 96.1% (2,771 of 2,882 nodes contain at least one extracted entity) and factual triple c |
| 29 | 3 | MODEL_NAME | Mistral | bedded figures. We therefore convert each PDF into page-level Markdown using a layout- preserving OCR pipeline based on Mistral OCR, retaining document structure and page provenance for subsequent nod |
| 30 | 3 | MODEL_NAME | GPT-5 | source Markdown into a structured JSON schema. Each generated node was then independently verified by a separate model, GPT-5-Nano, which received both the node and its ground-truth source passage and |
| 31 | 4 | PERCENTAGE | 6.0% | ltural terms vs. code-mixed transliterations). An- notators reached strong agreement (Fleiss’ 𝜅=0.81); 12 of 200 nodes (6.0%) fell below consensus threshold and were corrected via direct manual edit a |
| 32 | 4 | PERCENTAGE | 35.5% | ugh the multi- modal extension described in §3.3. 3.3 Image-Linked Nodes Of the 2,882 canonical knowledge nodes, 1,022 (35.5%) additionally carry a linked visual asset (a diagnostic pho- tograph, vari |
| 33 | 4 | COUNT_COMMA | 2,882 | ile image-containing nodes continue through the multi- modal extension described in §3.3. 3.3 Image-Linked Nodes Of the 2,882 canonical knowledge nodes, 1,022 (35.5%) additionally carry a linked visua |
| 34 | 4 | COUNT_COMMA | 1,022 | ue through the multi- modal extension described in §3.3. 3.3 Image-Linked Nodes Of the 2,882 canonical knowledge nodes, 1,022 (35.5%) additionally carry a linked visual asset (a diagnostic pho- tograp |
| 35 | 4 | COUNT_COMMA | 1,000 | re in Appendix C and leave dedicated visual retrieval to future work (§7.2). 3.4 Query Benchmark The benchmark contains 1,000 queries across three cate- gories (Table 2). Farmer-anchored. 400 farmer-a |
| 36 | 4 | DATASET_SIZE | 12 categories | t, source_pages) as the node’s textual content. Each im- age reference additionally carries a figure-type label (one of 12 categories, e.g., symptom_close_up, variety_portrait, procedure_illustration) |
| 37 | 4 | DATASET_SIZE | 000 queries | in Appendix C and leave dedicated visual retrieval to future work (§7.2). 3.4 Query Benchmark The benchmark contains 1,000 queries across three cate- gories (Table 2). Farmer-anchored. 400 farmer-anch |
| 38 | 4 | REFERENCE | Figure 1 | , Khan Raiyan Ibne Reza, Sanjana Aktar Maria, and Sumaiya Tabassum Nimi Figure 1: Canonical knowledge node construction pipeline. Source documents are parsed, chunked by topic, and processed into stru |
| 39 | 4 | REFERENCE | Table 2 | al retrieval to future work (§7.2). 3.4 Query Benchmark The benchmark contains 1,000 queries across three cate- gories (Table 2). Farmer-anchored. 400 farmer-anchored queries adapted from a prior QA b |
| 40 | 5 | PERCENTAGE | 97% | , guided by a domain-specific agricultural glossary (312 domain-critical terms, cross-referenced against NCBI Taxonomy; 97% back-translation equivalence on a 100-query spot check) to preserve technica |
| 41 | 5 | PERCENTAGE | 35.5% | s. Property Value Source PDFs 284 Organizations 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1 |
| 42 | 5 | PERCENTAGE | 96% | nswerable evaluation set 900 Inter-annotator 𝜅(farmer+safety) 0.72 Inter-annotator 𝜅(KG-grounded) 0.78 Entity coverage >96% aggregate-only evaluations. We organize primary experi- ments around four re |
| 43 | 5 | COUNT_COMMA | 2,882 | nguage as an explanatory variable indepen- dent of retrieval architecture, we translate both the full query set and all 2,882 KG nodes into English, guided by a domain-specific agricultural glossary ( |
| 44 | 5 | COUNT_COMMA | 1,022 | atistics. Property Value Source PDFs 284 Organizations 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total gener |
| 45 | 5 | COUNT_COMMA | 19,768 | e PDFs 284 Organizations 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1,000 Farmer-anchored (a |
| 46 | 5 | COUNT_COMMA | 17,501 | s 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1,000 Farmer-anchored (answerable) 300 Farmer-a |
| 47 | 5 | COUNT_COMMA | 1,000 | KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1,000 Farmer-anchored (answerable) 300 Farmer-anchored (low-agreement) 100 KG-gr |
| 48 | 5 | COUNT_COMMA | 3,072 | weight- ing (𝑘1=1.5, 𝑏=0.75) with character bigram plus full-word tokenization; (ii) Dense (Gemini) uses 𝐿2-normalized 3,072-dim gemini-embedding-001 vectors with exact inner-product search (FAISS Ind |
| 49 | 5 | COUNT_COMMA | 1,024 | ctors with exact inner-product search (FAISS IndexFlatIP) and asymmet- ric task types; (iii) Dense (BGE-M3 Native) uses 1,024-dim native dense embeddings as an open, retrieval-specific base- line; (iv |
| 50 | 5 | COUNT_COMMA | 4,096 | 4.2 Embedding Robustness To separate architectural effects from embedding quality, we evaluate six models spanning 384–4,096 dimensions (Ta- ble 6) on the same Bengali query set under identical retrie |
| 51 | 5 | DATASET_SIZE | 200 queries | -matching criterion before any architecture was evaluated, preserving the blind-evaluation guarantee. Safety (200). All 200 queries test advisory failure modes (pesticide dosage, off-label chemical us |
| 52 | 5 | DATASET_SIZE | 400 queries | =600). Majority vote determines the gold node; queries without majority agreement are excluded. KG-grounded gold nodes (400 queries) were assigned by a domain expert annotator and independently valida |
| 53 | 5 | DATASET_SIZE | 501
Queries | (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1,000 Farmer-anchored (answerable) 300 Farmer-ancho |
| 54 | 5 | METRIC | top-100 | context window) with MaxSim; and (v) Hybrid RRF fuses BM25 and Gemini dense rankings via Reciprocal Rank Fusion (𝑘=60, top-100 candidates each). All architectures retrieve from the identical 2,882-nod |
| 55 | 5 | REFERENCE | Section 5 | igher lexical overlap with their gold document than farmer queries (§6.1), consistent with their high retrievability in Section 5.3. All 200 are answerable and included in the 900-query evaluation set |
| 56 | 5 | REFERENCE | Table 2 | xhaustive approach demonstrates that AgRiTrust surfaces fail- ure modes that remain invisible to single-architecture or Table 2: AgRiTrust benchmark statistics. Property Value Source PDFs 284 Organiza |
| 57 | 6 | PERCENTAGE | 95% | mbedding tables are reported descriptively. Significance levels (𝑝<0.001 for BM25 vs. Dense; 𝑝<0.01 for Hybrid RRF) and 95% CIs are reported inline in Section 5.1. 5 Results Each subsection answers on |
| 58 | 6 | PERCENTAGE | 9% | ers, BM25 leads (R@10=0.506, 95% CI: [0.474, 0.538]), outperforming dense Gemini-001 (0.464, 95% CI: [0.432, 0.497]) by 9% (𝑝<0.001, Wilcoxon signed-rank test). Late-interaction ColBERT (BGE-M3, 512 t |
| 59 | 6 | PERCENTAGE | 15% | s-lingual (EN→BN) .425 [.39, .46] .004 [.00, .01] Dense (≈100×) English (EN→EN) .442 [.41, .47] .384 [.35, .42] Dense (+15%) BM25 0.478) and substantially closes the gap on farmer queries relative to  |
| 60 | 6 | PERCENTAGE | 99% | →Bengali corpus), where BM25’s exact lexical matching declines sharply across script boundaries (R@10: 0.506 →0.004, a 99% drop) and becomes effectively unus- able. Multilingual dense embeddings, by c |
| 61 | 6 | PERCENTAGE | 8% | us- able. Multilingual dense embeddings, by contrast, largely preserve the script boundary (R@10: 0.464 →0.425, only an 8% drop). Architecture choice cannot be separated from the language scenario it  |
| 62 | 6 | COUNT_COMMA | 2,882 | erministic criterion admitting no partial credit. For context, the random baseline R@10 for a corpus of this size is 10/2,882 ≈0.003. Separation score. Beyond Recall@𝑘, we measure how well embeddings  |
| 63 | 6 | COUNT_COMMA | 2,881 | query 𝑞𝑖with gold node 𝑔𝑖, let 𝑠gold = cos(𝐸(𝑞𝑖), 𝐸(𝑔𝑖)) and 𝑠neg be the mean cosine sim- ilarity between 𝐸(𝑞𝑖) and all 2,881 non-gold nodes. The separation score is the mean difference (𝑠gold −𝑠neg)  |
| 64 | 6 | COUNT_COMMA | 10,000 | corpus average. 4.4 Statistical Validation We compare retrieval architectures using BCa bootstrap confidence intervals (10,000 resamples). Pairwise signifi- cance is assessed via paired Wilcoxon signe |
| 65 | 6 | DATASET_SIZE | 900 queries | 512, matching the dense baselines’ context window. Table 4: Cross-Lingual Comparison (95% BCa CIs for R@10 in brackets; 900 queries). Setting Dense (Gemini) BM25 Winner Bengali (BN→BN) .464 [.43, .50] |
| 66 | 6 | METRIC | MRR | a, Sanjana Aktar Maria, and Sumaiya Tabassum Nimi 4.3 Metrics Retrieval (L1). We report R@1, R@5, R@10 (hereafter R@k), MRR, and nDCG@10 against gold source nodes for the 900 answerable queries. A ret |
| 67 | 6 | METRIC | Recall | al credit. For context, the random baseline R@10 for a corpus of this size is 10/2,882 ≈0.003. Separation score. Beyond Recall@𝑘, we measure how well embeddings separate the gold node from the remain- |
| 68 | 6 | METRIC | accuracy | iscusses mechanistic explanations. 5.1 RQ1: Benchmark Difficulty and Architecture Comparison Table 3 presents retrieval accuracy across 900 answerable Bengali queries (random baseline R@10≈0.003). Hyb |
| 69 | 6 | REFERENCE | Table 3 | cance is assessed via paired Wilcoxon signed-rank tests with Holm-Bonferroni correction across 10 architecture pairs in Table 3; per-category and per-embedding tables are reported descriptively. Signi |
| 70 | 6 | REFERENCE | Section 5 | scriptively. Significance levels (𝑝<0.001 for BM25 vs. Dense; 𝑝<0.01 for Hybrid RRF) and 95% CIs are reported inline in Section 5.1. 5 Results Each subsection answers one research question using the 9 |
| 71 | 6 | REFERENCE | Section 6 | e 900 answerable Bengali queries unless otherwise noted. All reported numbers are from the post-audit verification run; Section 6 discusses mechanistic explanations. 5.1 RQ1: Benchmark Difficulty and  |
| 72 | 6 | REFERENCE | Table 5 | ens) reaches R@10=0.487, outperforming both single- vector dense variants (0.464, 0.408). Broken out by query category (Table 5), ColBERT is the best single architecture on KG-grounded queries (R@10=0 |
| 73 | 6 | REFERENCE | Table 4 | -M3)‡ .255 .414 .487 .324 .416 ‡ ColBERT evaluated at max_seq_length=512, matching the dense baselines’ context window. Table 4: Cross-Lingual Comparison (95% BCa CIs for R@10 in brackets; 900 queries |
| 74 | 7 | PERCENTAGE | 95% | AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval , Table 5: R@10 by query category (95% BCa CIs in brackets; 900 verified queries; Farmer=300, Safety=200, KG-grounded=400) |
| 75 | 7 | PERCENTAGE | 99% | axis: at the field-standard default of 128 tokens, Bengali knowledge nodes (mean ≈1,180 characters) are truncated by 95–99%, and ColBERT underperforms even the weaker dense baseline (R@10=0.376 vs. BG |
| 76 | 7 | PERCENTAGE | 96.4% | ister Gap Analysis Token-level Jaccard similarity across all 900 query-gold pairs reveals a near-universal lexical gap: 96.4% of queries have Jaccard < 0.10 with their gold document (mean: 0.044; maxi |
| 77 | 7 | PERCENTAGE | 3.5% | ment). Verbatim entity inspection explains dense retrieval’s col- lapse on colloquial farmer queries (R@10=0.093): only 3.5% of gold document entity names appear verbatim in farmer queries, while 92%  |
| 78 | 7 | PERCENTAGE | 92% | olloquial farmer queries (R@10=0.093): only 3.5% of gold document entity names appear verbatim in farmer queries, while 92% are entirely absent. Farmers describe observable symptoms (“leaves turning y |
| 79 | 7 | COUNT_COMMA | 3,072 | R@10 in brackets; 900 queries, BN→BN). Random baseline: separation = 0. Model Dim Separation R@10 Gemini-embedding-001 3,072 +0.127 .464 [.43, .50] BGE-M3 (native proj.) 1,024 +0.133 .408 [.38, .44] E |
| 80 | 7 | COUNT_COMMA | 1,024 | line: separation = 0. Model Dim Separation R@10 Gemini-embedding-001 3,072 +0.127 .464 [.43, .50] BGE-M3 (native proj.) 1,024 +0.133 .408 [.38, .44] E5-Large (multilingual) 1,024 +0.037 .284 [.26, .32 |
| 81 | 7 | COUNT_COMMA | 4,096 | -M3 (native proj.) 1,024 +0.133 .408 [.38, .44] E5-Large (multilingual) 1,024 +0.037 .284 [.26, .32] Qwen3 Embedding 8B 4,096 +0.108 .241 [.21, .27] MPNet (paraphrase) 768 −0.010 .009 [.00, .02] MiniL |
| 82 | 7 | COUNT_COMMA | 1,180 | a second, indepen- dent configuration axis: at the field-standard default of 128 tokens, Bengali knowledge nodes (mean ≈1,180 characters) are truncated by 95–99%, and ColBERT underperforms even the we |
| 83 | 7 | DATASET_SIZE | 900 queries | 6] .675 [.60, .74] .600 [.55, .65] .396 [.35, .44] Table 6: Multi-Embedding Analysis (95% BCa CIs for R@10 in brackets; 900 queries, BN→BN). Random baseline: separation = 0. Model Dim Separation R@10  |
| 84 | 7 | METRIC | Recall | 41). Notably, BGE-M3 yields the highest mean cosine separa- tion (+0.133 vs. Gemini’s +0.127) despite ranking second on Recall@10 (.408 vs. .464); mean separation rewards models with confident average |
| 85 | 7 | METRIC | accuracy | s use precise chemical codes and variety names that closely match document vocabulary, so dense retrievers achieve high accuracy (0.970) on this category. 6.2 Failure Complementarity and Hybrid Attrib |
| 86 | 7 | REFERENCE | Table 5 | AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval , Table 5: R@10 by query category (95% BCa CIs in brackets; 900 verified queries; Farmer=300, Safety=200, KG-grounded=400) |
| 87 | 7 | REFERENCE | Table 6 | .60] .478 [.43, .53] .529 [.48, .57] ColBERT (BGE-M3)‡ .210 [.17, .26] .675 [.60, .74] .600 [.55, .65] .396 [.35, .44] Table 6: Multi-Embedding Analysis (95% BCa CIs for R@10 in brackets; 900 queries, |
| 88 | 7 | REFERENCE | Table 3 | =0.376 vs. BGE-M3’s 0.408); matching the dense baselines’ 512-token context window instead lifts ColBERT to R@10=0.487 (Table 3), reversing this ranking. Both an embedding-API task type and a passage- |
| 89 | 7 | REFERENCE | Table 7 | aves turning yellow”), whereas authoritative documents encode formal scientific entities (Tungro virus) (illustrated in Table 7). Safety queries use precise chemical codes and variety names that close |
| 90 | 8 | PERCENTAGE | 97% | s-encoder rerankers are left to future work. Machine-translated English queries may carry subtle lexical shifts despite 97% back-translation equiva- lence on a 100-query random sample (§3.5); future w |
| 91 | 8 | COUNT_COMMA | 2,882 | asis for evaluating future low-resource retrieval and RAG systems. A Reproducibility Checklist • Data: 284 source PDFs, 2,882 knowledge nodes, 1,000 queries (900 with verified gold-node mappings; 100  |
| 92 | 8 | COUNT_COMMA | 1,000 | ure low-resource retrieval and RAG systems. A Reproducibility Checklist • Data: 284 source PDFs, 2,882 knowledge nodes, 1,000 queries (900 with verified gold-node mappings; 100 low-agreement queries r |
| 93 | 8 | DATASET_SIZE | 000
queries | e low-resource retrieval and RAG systems. A Reproducibility Checklist • Data: 284 source PDFs, 2,882 knowledge nodes, 1,000 queries (900 with verified gold-node mappings; 100 low-agreement queries rel |
| 94 | 8 | METRIC | accuracy | stem built on this corpus for live advisory would require a separate regulatory-currency check independent of retrieval accuracy. Finally, while reliance on proprietary APIs for initial query generati |
| 95 | 8 | REFERENCE | Table 7 | , Khan Raiyan Ibne Reza, Sanjana Aktar Maria, and Sumaiya Tabassum Nimi Table 7: Illustrative register gap: a farmer-anchored query and its gold node (English glosses of Bengali text in brackets). Fa |
| 96 | 9 | PERCENTAGE | 35.5% | category, title_bn, _provenance_layer) are unchanged from the node shown in Appendix B. In total, 1,022 of 2,882 nodes (35.5%) carry one or more image references. Image references have not undergone t |
| 97 | 9 | COUNT_COMMA | 3,072 | AgRiTrust: A Provenance-Grounded Benchmark for Bengali Agricultural Retrieval , • Dense (Gemini): gemini-embedding-001, 3,072-dim, asymmetric RETRIEVAL_QUERY/RETRIEVAL_DOCUMENT task types. • Dense (BG |
| 98 | 9 | COUNT_COMMA | 1,024 | ing-001, 3,072-dim, asymmetric RETRIEVAL_QUERY/RETRIEVAL_DOCUMENT task types. • Dense (BGE-M3): Native projection head, 1,024-dim, 𝐿2-normalized. • ColBERT: BGE-M3 multi-vector, 512-token sequence len |
| 99 | 9 | COUNT_COMMA | 10,000 | tes per method). • Audit Variants: sentence-similarity task type; 128-token passage truncation. • Stats: BCa bootstrap (10,000 resamples), paired Wilcoxon signed-rank tests with Holm-Bonferroni correc |
| 100 | 9 | COUNT_COMMA | 1,022 | ther fields (node_id, category, title_bn, _provenance_layer) are unchanged from the node shown in Appendix B. In total, 1,022 of 2,882 nodes (35.5%) carry one or more image references. Image reference |
| 101 | 9 | COUNT_COMMA | 2,882 | ds (node_id, category, title_bn, _provenance_layer) are unchanged from the node shown in Appendix B. In total, 1,022 of 2,882 nodes (35.5%) carry one or more image references. Image references have no |
| 102 | 9 | METRIC | top-100 | • ColBERT: BGE-M3 multi-vector, 512-token sequence length, MaxSim scoring. • Hybrid RRF: Reciprocal Rank Fusion (𝑘=60, top-100 candidates per method). • Audit Variants: sentence-similarity task type;  |
| 103 | 10 | MODEL_NAME | bert | tab and Matei Zaharia. 2020. Colbert: Efficient and effec- tive passage search via contextualized late interaction over bert. In Proceedings of the 43rd International ACM SIGIR conference on research  |

---

## Summary of Key Claims Requiring T05 Reconciliation

### Dataset sizes (from PDF A)
| Claim | Value | Page | Status |
|-------|-------|------|--------|
| Total instances | 85,979 | 1, 2, 3 | **NEEDS RECONCILIATION** — verify against actual files |
| General QA | 28,993 | 3 | **NEEDS RECONCILIATION** |
| Treatment QA | 11,224 | 3 | **NEEDS RECONCILIATION** |
| Safety (T3+T4) | 20,112 | 3, 5 | **NEEDS RECONCILIATION** — T3=3,216 + T4=16,896 |
| Table QA | 25,650 | 3 | **NEEDS RECONCILIATION** |
| Farmer Benchmark | 1,000 | 1-5 | **NEEDS RECONCILIATION** — 350 eval split |
| Semantic units | 2,946 | 3 | **NEEDS RECONCILIATION** |
| Source publications | 284 | 1 | **NEEDS RECONCILIATION** |
| Chemical-bearing (TQA) | 7,437 (66.3%) | 4 | **NEEDS RECONCILIATION** |

### Model evaluation claims (from PDF A)
| Model | Claim | Value | Status |
|-------|-------|-------|--------|
| KrishokTech-4B | Gen F1 (CB) | 0.314 | **NEEDS RECONCILIATION** |
| KrishokTech-4B | TrtCorrect% (CB) | 35.55% | **NEEDS RECONCILIATION** |
| KrishokTech-4B | GenHal% (CB) | 19.83% | **NEEDS RECONCILIATION** |
| KrishokTech-4B | Safety compliance | 0.31% | **NEEDS RECONCILIATION** |
| Gemini-2.5-FL | TrtCorrect% (CB) | 43.64% | **NEEDS RECONCILIATION** |
| Gemma-4-26B | TrtCorrect% (CB) | 38.73% | **NEEDS RECONCILIATION** |
| LLaMA-3.1-8B | TrtCorrect% (CB) | 12.43% | **NEEDS RECONCILIATION** |
| Qwen-2.5-7B | TrtCorrect% (CB) | 13.29% | **NEEDS RECONCILIATION** |
| GPT-OSS-120B | Halluc% (CB) | 36.20% | **NEEDS RECONCILIATION** |
| Oracle hallucination floor | Range | 4.05%–7.00% | **NEEDS RECONCILIATION** |

### Safety taxonomy claims (from PDF A)
| Claim | Value | Status |
|-------|-------|--------|
| Safety categories (T3) | 12 | **NEEDS RECONCILIATION** — see Table 8 |
| Re-query slots (T4) | 6 | **NEEDS RECONCILIATION** — see Table 11 |
| T3 refusal records | 3,216 | **NEEDS RECONCILIATION** |
| T4 re-query records | 16,896 | **NEEDS RECONCILIATION** |

### Training claims (from PDF A)
| Claim | Value | Status |
|-------|-------|--------|
| Base model | Gemma-4-E4B (4-bit) | **NEEDS RECONCILIATION** |
| LoRA config | r=32, α=64, 6 target modules | **NEEDS RECONCILIATION** |
| Training steps (1 epoch) | 2,680 | **NEEDS RECONCILIATION** |
| Training steps (2 epochs) | 5,362 | **NEEDS RECONCILIATION** |
| GPU | NVIDIA L4 (24GB VRAM) | **NEEDS RECONCILIATION** |
| Max seq length | 4,096 tokens | **NEEDS RECONCILIATION** |
| Learning rate | 2×10⁻⁴ peak, cosine decay | **NEEDS RECONCILIATION** |

### Chemical names found in qualitative examples (from PDF A)
| Chemical | Context | Status |
|----------|---------|--------|
| mancozeb | Table 20 qualitative example: rice blast treatment | **NEEDS RECONCILIATION** |
| carbendazim | Table 20 qualitative example: hallucination case | **NEEDS RECONCILIATION** |
| 150 kg/ha, 120 kg/ha | Table 20: urea application rates | **NEEDS RECONCILIATION** |

### PDF B (AgriTrust)
- Pages: 10
- Claims extracted: 103

#### Key claims from PDF B
| # | Page | Category | Value | Context (truncated) |
|---|------|----------|-------|---------------------|
| 1 | 1 | COUNT_COMMA | 2,882 | thorita- tive publications issued by five Bangladeshi government and research organizations. The collection comprises a 2,882-node knowledge graph and 1,000 queries (900 an- swerable), with gold-node  |
| 2 | 1 | COUNT_COMMA | 1,000 | ed by five Bangladeshi government and research organizations. The collection comprises a 2,882-node knowledge graph and 1,000 queries (900 an- swerable), with gold-node mappings verified by three inde |
| 3 | 1 | COUNT_COMMA | 1,022 | nsists of: (i) 284 source PDFs from five Bangladeshi government and research organizations; (ii) 2,882 knowledge nodes (1,022 image-linked), each a provenance-preserving retrieval unit; (iii) a knowle |
| 4 | 1 | COUNT_COMMA | 19,768 | ii) 2,882 knowledge nodes (1,022 image-linked), each a provenance-preserving retrieval unit; (iii) a knowledge graph of 19,768 entities and 17,501 factual triples; (iv) 1,000 queries (900 answerable)  |
| 5 | 1 | COUNT_COMMA | 17,501 | nodes (1,022 image-linked), each a provenance-preserving retrieval unit; (iii) a knowledge graph of 19,768 entities and 17,501 factual triples; (iv) 1,000 queries (900 answerable) across three categor |
| 6 | 1 | DATASET_SIZE | 000 queries | by five Bangladeshi government and research organizations. The collection comprises a 2,882-node knowledge graph and 1,000 queries (900 an- swerable), with gold-node mappings verified by three indepen |
| 7 | 1 | DATASET_SIZE | 200 queries | nts use formal scientific Bengali. This register gap challenges lexical and dense retrieval in opposing ways. Of these, 200 queries cover safety-critical content (pesticide dosage, off-label chemical  |
| 8 | 1 | METRIC | accuracy | gured general-purpose dense embedding model (R@10=0.464); Reciprocal Rank Fusion of the two reaches the highest overall accuracy (R@10=0.539). This aggregate picture hides a sharp query-register effec |
| 9 | 2 | COUNT_COMMA | 2,882 | ance- grounded test collection for low-resource Bengali agri- cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated quer |
| 10 | 2 | COUNT_COMMA | 19,768 | lection for low-resource Bengali agri- cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated queries (available at https |
| 11 | 2 | COUNT_COMMA | 17,501 | esource Bengali agri- cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated queries (available at https://huggingface. c |
| 12 | 2 | COUNT_COMMA | 1,000 | - cultural retrieval, covering 284 authoritative documents, 2,882 knowledge nodes, 19,768 entities, 17,501 triples, and 1,000 annotated queries (available at https://huggingface. co/datasets/RaiyanKha |
| 13 | 2 | METRIC | accuracy | ion with provenance grounding in a low-resource agricultural setting. Standard benchmarks typically emphasize aggregate accuracy scores, concealing subgroup failure across query registers, a limita- t |
| 14 | 2 | REFERENCE | Section 5 | , and an embedding API configuration audit. These four findings (summarized in the abstract) are de- veloped in full in Section 5, with mechanistic explanations in Section 6. 1.3 Contributions 1. AgRi |
| 15 | 2 | REFERENCE | Section 6 | These four findings (summarized in the abstract) are de- veloped in full in Section 5, with mechanistic explanations in Section 6. 1.3 Contributions 1. AgRiTrust benchmark collection. A provenance- gr |
| 16 | 2 | REFERENCE | Table 1 | modest gains [22], while multi-vector late-interaction models such as ColBERT [9] improve fine-grained token matching. Table 1: Positioning of AgRiTrust relative to closest prior benchmarks and system |
| 17 | 3 | PERCENTAGE | 65% | , IRRI, DAE, SRDI, MoA). The Ministry of Agriculture (MoA) and its extension arm (DAE) jointly contribute approximately 65% of the cor- pus via national farming handbooks, while specialized in- stitut |
| 18 | 3 | PERCENTAGE | 73% | sulting Markdown corpus (2,680 section-level passages) serves solely as an intermediate pre- processing artifact. While 73% of this underlying raw text originates from a prior QA benchmark [? ], AgRiT |
| 19 | 3 | PERCENTAGE | 100% | rk [? ], AgRiTrust’s primary contribution is restructuring this text into a novel, provenance-grounded knowledge graph (100% of KG entity and triple construction, node schema, and the full 900-query g |
| 20 | 3 | PERCENTAGE | 96% | de) and 17,501 factual triples via schema-guided, bounded open information extraction. Per-node entity coverage exceeds 96%. Source-Grounded Automated Verification. Node content (summary, symptoms, ma |
| 21 | 3 | PERCENTAGE | 96.1% | d to factual consistency and never becomes an open-ended quality rating. Across the resulting graph, entity coverage is 96.1% (2,771 of 2,882 nodes contain at least one extracted entity) and factual t |
| 22 | 3 | PERCENTAGE | 9.8% | coverage reaches 100%. Closed-Loop Refinement. Nodes falling below threshold (≤ 3 on any dimension; 283 of 2,882 nodes, 9.8%) were returned to Gemini-3.1-Flash-Lite together with the verifier’s specif |
| 23 | 3 | COUNT_COMMA | 2,680 | OCR, retaining document structure and page provenance for subsequent node construction. The resulting Markdown corpus (2,680 section-level passages) serves solely as an intermediate pre- processing ar |
| 24 | 3 | COUNT_COMMA | 2,729 | h explicitly indexes 915 unique crops (spanning horticulture, agroforestry, and aquaculture), 704 disease variants, and 2,729 chemical or pesticide entities. 3.2 Canonical Knowledge Node Construction  |
| 25 | 3 | COUNT_COMMA | 2,882 | ext, flagging any node whose entities do not appear in its cited passage for correction. Chunking. We segment text into 2,882 topic-coherent knowledge nodes, each corresponding to a single agricul- tu |
| 26 | 3 | COUNT_COMMA | 19,768 | and Cultiva- tion Practice (570) down to a long tail such as Food Safety (18). Entity and Triple Extraction. We extract 19,768 entities (6.9/node) and 17,501 factual triples via schema-guided, bounded |
| 27 | 3 | COUNT_COMMA | 17,501 | ) down to a long tail such as Food Safety (18). Entity and Triple Extraction. We extract 19,768 entities (6.9/node) and 17,501 factual triples via schema-guided, bounded open information extraction. P |
| 28 | 3 | COUNT_COMMA | 2,771 | ctual consistency and never becomes an open-ended quality rating. Across the resulting graph, entity coverage is 96.1% (2,771 of 2,882 nodes contain at least one extracted entity) and factual triple c |
| 29 | 3 | MODEL_NAME | Mistral | bedded figures. We therefore convert each PDF into page-level Markdown using a layout- preserving OCR pipeline based on Mistral OCR, retaining document structure and page provenance for subsequent nod |
| 30 | 3 | MODEL_NAME | GPT-5 | source Markdown into a structured JSON schema. Each generated node was then independently verified by a separate model, GPT-5-Nano, which received both the node and its ground-truth source passage and |
| 31 | 4 | PERCENTAGE | 6.0% | ltural terms vs. code-mixed transliterations). An- notators reached strong agreement (Fleiss’ 𝜅=0.81); 12 of 200 nodes (6.0%) fell below consensus threshold and were corrected via direct manual edit a |
| 32 | 4 | PERCENTAGE | 35.5% | ugh the multi- modal extension described in §3.3. 3.3 Image-Linked Nodes Of the 2,882 canonical knowledge nodes, 1,022 (35.5%) additionally carry a linked visual asset (a diagnostic pho- tograph, vari |
| 33 | 4 | COUNT_COMMA | 2,882 | ile image-containing nodes continue through the multi- modal extension described in §3.3. 3.3 Image-Linked Nodes Of the 2,882 canonical knowledge nodes, 1,022 (35.5%) additionally carry a linked visua |
| 34 | 4 | COUNT_COMMA | 1,022 | ue through the multi- modal extension described in §3.3. 3.3 Image-Linked Nodes Of the 2,882 canonical knowledge nodes, 1,022 (35.5%) additionally carry a linked visual asset (a diagnostic pho- tograp |
| 35 | 4 | COUNT_COMMA | 1,000 | re in Appendix C and leave dedicated visual retrieval to future work (§7.2). 3.4 Query Benchmark The benchmark contains 1,000 queries across three cate- gories (Table 2). Farmer-anchored. 400 farmer-a |
| 36 | 4 | DATASET_SIZE | 12 categories | t, source_pages) as the node’s textual content. Each im- age reference additionally carries a figure-type label (one of 12 categories, e.g., symptom_close_up, variety_portrait, procedure_illustration) |
| 37 | 4 | DATASET_SIZE | 000 queries | in Appendix C and leave dedicated visual retrieval to future work (§7.2). 3.4 Query Benchmark The benchmark contains 1,000 queries across three cate- gories (Table 2). Farmer-anchored. 400 farmer-anch |
| 38 | 4 | REFERENCE | Figure 1 | , Khan Raiyan Ibne Reza, Sanjana Aktar Maria, and Sumaiya Tabassum Nimi Figure 1: Canonical knowledge node construction pipeline. Source documents are parsed, chunked by topic, and processed into stru |
| 39 | 4 | REFERENCE | Table 2 | al retrieval to future work (§7.2). 3.4 Query Benchmark The benchmark contains 1,000 queries across three cate- gories (Table 2). Farmer-anchored. 400 farmer-anchored queries adapted from a prior QA b |
| 40 | 5 | PERCENTAGE | 97% | , guided by a domain-specific agricultural glossary (312 domain-critical terms, cross-referenced against NCBI Taxonomy; 97% back-translation equivalence on a 100-query spot check) to preserve technica |
| 41 | 5 | PERCENTAGE | 35.5% | s. Property Value Source PDFs 284 Organizations 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1 |
| 42 | 5 | PERCENTAGE | 96% | nswerable evaluation set 900 Inter-annotator 𝜅(farmer+safety) 0.72 Inter-annotator 𝜅(KG-grounded) 0.78 Entity coverage >96% aggregate-only evaluations. We organize primary experi- ments around four re |
| 43 | 5 | COUNT_COMMA | 2,882 | nguage as an explanatory variable indepen- dent of retrieval architecture, we translate both the full query set and all 2,882 KG nodes into English, guided by a domain-specific agricultural glossary ( |
| 44 | 5 | COUNT_COMMA | 1,022 | atistics. Property Value Source PDFs 284 Organizations 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total gener |
| 45 | 5 | COUNT_COMMA | 19,768 | e PDFs 284 Organizations 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1,000 Farmer-anchored (a |
| 46 | 5 | COUNT_COMMA | 17,501 | s 5 (BRRI, IRRI, DAE, SRDI, MoA) KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1,000 Farmer-anchored (answerable) 300 Farmer-a |
| 47 | 5 | COUNT_COMMA | 1,000 | KG nodes 2,882 Image-linked nodes 1,022 (35.5%) Unique entities 19,768 Factual triples 17,501 Queries (total generated) 1,000 Farmer-anchored (answerable) 300 Farmer-anchored (low-agreement) 100 KG-gr |
| 48 | 5 | COUNT_COMMA | 3,072 | weight- ing (𝑘1=1.5, 𝑏=0.75) with character bigram plus full-word tokenization; (ii) Dense (Gemini) uses 𝐿2-normalized 3,072-dim gemini-embedding-001 vectors with exact inner-product search (FAISS Ind |
| 49 | 5 | COUNT_COMMA | 1,024 | ctors with exact inner-product search (FAISS IndexFlatIP) and asymmet- ric task types; (iii) Dense (BGE-M3 Native) uses 1,024-dim native dense embeddings as an open, retrieval-specific base- line; (iv |
| 50 | 5 | COUNT_COMMA | 4,096 | 4.2 Embedding Robustness To separate architectural effects from embedding quality, we evaluate six models spanning 384–4,096 dimensions (Ta- ble 6) on the same Bengali query set under identical retrie |
| ... | ... | ... | ... | 53 more claims |

---

## Raw data
- JSON extraction: `T01_raw.json` (265,858 bytes)