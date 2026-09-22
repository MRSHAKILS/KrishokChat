# FINAL SUBMISSION FORENSIC AUDIT

## 1. Overall Status

**NOT YET READY — concrete issues remain**

The manuscript’s central narrative is coherent, and its principal counts, percentages, and reported Wilson intervals are internally consistent. The remaining substantive problems concern the architecture figure, the correspondence between evaluated and released artifacts, and the presentation of supporting screenshots. These are specific correction tasks; they do not require reopening novelty, restructuring the argument, or adding experiments. I inspected all 12 PDF pages, extracted the embedded figures, checked the adjacent source files, and tested the important public resources; no manuscript files were changed.

Primary document: :codex-file-citation{path="D:/Web Dev/krishokchat/paper/EACL Final/paper/latex/main.pdf" purpose="source"}. Page references below mean PDF page positions.

## 2. P0 Issues

None found.

Submission-stage anonymity and venue-specific page-limit compliance could not be certified because the exact submission call and review/camera-ready stage were not supplied.

## 3. P1 Issues

### P1-1 — Figure 1 assigns operations to different stages from the text

**[Location]** Page 1, Figure 1; compare §§3.1–3.2 and Appendix A.

**[Original]**

- T0 contains “crop-less treatment check.”
- T1 is “Crop binding,” including “initial crop prediction (image + text).”
- T3 is described as “The only stage calling the language model.”

**[Problem]** The manuscript assigns the missing-crop gate to T1 and explains image-based routing under T2. Appendix D also explicitly reports an LLM query rewriter, making the figure’s general “only stage calling the language model” wording too broad.

**[Why it matters]** The first architecture diagram gives a different allocation of responsibilities from the system description.

**[Minimal fix]** Put the crop-presence check under T1, align the image-routing label with the stage assignment used in the text, and change the T3 statement to **“The only stage calling the answer generator.”** No diagram redesign is necessary.

### P1-2 — The public reproduction package contains stale numbers and overstates what it recomputes

**[Location]** §6’s linked repository, reviewer quick start and `reproduce.py`.

**[Original]** The package announces “ALL PRINCIPAL PAPER METRICS SUCCESSFULLY REPRODUCED!” Its retrieval summary uses **145/400 → 120/400**, whereas the PDF reports **146/400 → 121/400**.

**[Problem]** Inspection shows that the retrieval function assigns fixed counts and compares them with those same constants. The dosage function runs separate unit cases but constructs **114/118** and **0/38** from fixed values. Those operations do not independently reproduce the corresponding paper measurements. [Public reproduction script](https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System/blob/f79d6c3f9650f61b0cc41862f74a33d1509f8066/reproduce.py).

**[Why it matters]** A reviewer following the paper’s repository link encounters both a numerical mismatch and a stronger verification claim than the script supports.

**[Minimal fix]** Reconcile the retrieval summary with the final experiment records. Label the fixed summaries as **reported results**, distinguish them from the checks actually executed, and point readers to the existing experiment runners and logs. This finding does **not** establish that the paper’s underlying results are wrong.

### P1-3 — The evaluated local model and released adapter are not clearly distinguished

**[Location]** §§3.3, 5.3 and 6; linked safety-experiment specification and adapter configuration.

**[Original]** The PDF calls the evaluated deployment `krishokchat-4b` and describes the linked artifact as “The generator’s LoRA adapter.”

**[Problem]** The safety experiment identifies its model as **Gemma3 4.3B Q4_K_M**, while the released adapter specifies **`unsloth/gemma-4-E4B-it-unsloth-bnb-4bit`**. The model nickname alone does not explain their relationship. [Experiment specification](https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System/blob/f79d6c3f9650f61b0cc41862f74a33d1509f8066/paper/EACL%20Final/experiments/N14_local_model_safety/spec.yaml), [adapter configuration](https://huggingface.co/RaiyanKhaan/KrishokChat-Advisory-System/blob/7109a081a6b415f6523974d4668501909d7251ea/gemma_llm/checkpoint-4020/adapter_config.json).

**[Why it matters]** A reviewer cannot confidently identify which released artifact corresponds to the reported attack-success and local-latency measurements.

**[Minimal fix]** Identify the evaluated base model and quantization once in §5.3, then explicitly state whether the Gemma 4 adapter is a separate supported artifact. If a specification is stale, correct that specification from the existing run metadata.

### P1-4 — Some screenshots do not expose the evidence claimed for them

**[Location]** §4 S1–S2; Figures 2a, 3 and 4; Appendix C; Tables 7–8.

**[Original]**

- S1 says the interface displays `sources_retrieved = 0` and non-chemical guidance, citing Figure 2a.
- S2 says the interface displays the predicted crop and resulting evidence scope.
- Appendix C promises “full-size screens.”

**[Problem]** Figures 2a and 3 visibly show the clarification and crop choices, but not the zero-source counter or non-chemical guidance card. Figure 4 shows a selected rice example and the evaluation interface, without a visible retrieved-evidence scope. The appendix screenshots are thumbnails, and Tables 7–8 use approximately **6.2-point body text**.

**[Why it matters]** Readers cannot inspect several interface details that the prose presents as visible evidence. Enlarging the original embedded images confirms that the missing S1 indicators are not merely lost through PDF scaling.

**[Minimal fix]** Use existing captures that expose the claimed indicators, or narrow the descriptions to what the screenshots actually show. Enlarge the appendix screenshots and evidence tables enough to read their substantive content; use additional appendix space if permitted.

### P1-5 — The adjacent LaTeX source is not the source of the final PDF

**[Location]** Adjacent `main.tex`, compared with PDF page 1.

**[Original]** The LaTeX title is “KrishokTech: Deterministic-First, Evidence-Bounded Bengali Agricultural Advisory,” and its author list contains four authors. The PDF has the new authorization-controls title and five authors, including Faiyad Hasan.

**[Problem]** The abstract and an email spelling also differ. The adjacent `figures` directory contains only the architecture image.

**[Why it matters]** Applying corrections or rebuilding from this directory could restore older text, alter the author list, and lose the final screenshots.

**[Minimal fix]** Locate and preserve the exact source bundle that produced this PDF before applying final corrections. This is a source-management issue, not a finding that the PDF’s author list is incorrect.

## 4. P2 Polish Issues

| Location | Original | Problem | Why it matters | Minimal fix |
|---|---|---|---|---|
| Abstract, p. 1 | “built around an explicit authorization boundary around generation” | Accidental repetition of “around.” | Noticeable in the abstract. | “built with an explicit authorization boundary around generation” |
| §3.1, p. 3 | “Six regional synonym presets” | Appendix A lists Standard Bengali plus five regional presets. | The category description is inaccurate. | “Six language presets—Standard Bengali and five regional varieties—…” |
| §6, p. 6 | “depends on an explicit crop mention **or** a confident image prediction” | Detecting the described disagreement requires both crop signals. | “Or” misstates the condition. | Change **“or” to “and.”** |
| §5.3, p. 5 | “The four missed errors and results from the larger passage-derived benchmark are reported in Appendix E.” | Appendix E reports aggregate outcomes, without identifying the four missed errors. | The cross-reference promises detail that is absent. | “Aggregate catch rates for this test and the larger passage-derived benchmark are reported in Appendix E.” |
| Table 8, p. 12 | “70 Bengali-native probes” alongside “Bengali-native 19/100” | The 100-case subset’s composition is unstated. | Readers may suspect inconsistent denominators. | Add: “The Bengali-native subset comprises 30 cases from the seven-family set plus 70 additional probes.” Existing experiment records support this explanation. |
| §B.1, p. 10; Table 8 | “A 160-character Bengali advisory therefore occupies two or three SMS segments” | At the stated 67 characters per concatenated segment, exactly 160 characters require three. | Small but objective arithmetic error. | “A 160-character Bengali advisory occupies three concatenated SMS segments.” |
| Table 8 and dosage screenshot; Table 7 | “ASR,” “PHI,” “PRISM conflicts” | ASR and PHI are not explicitly expanded; PRISM appears without identification. | PHI and PRISM are particularly opaque to an NLP reader. | Define **attack success rate (ASR)** and **pre-harvest interval (PHI)**; replace “PRISM conflicts” with “synthetic conflicts” unless the name is explained. |
| Appendix A, p. 9 | Clickable `backend/app/domain/…` paths | These are relative PDF URI targets, not usable public repository links. | Clicking does not reliably reach the source. | Link the displayed paths to the actual GitHub files, or render them as non-clickable code paths. |
| References, pp. 7–8 | Examples: “Farmer. chat,” “Minicheck,” “llms,” “rag,” “bengali” | Proper names and acronyms have been lowercased or split. | The bibliography looks mechanically uncorrected. | Protect intended capitalization in BibTeX, including **Farmer.Chat, MiniCheck, LLMs, RAG, Bengali**. |
| Linked screencast page | Chapters continue through “2:15–2:30.” | The actual playable video lasts **48.67 seconds**. | The chapter guide cannot describe the current file’s timing. | Correct the chapter timings or link the intended recording. The paper’s “<2.5 min” statement itself remains true. |

## 5. Sentence-Level Grammar & Clarity

| Location | Original | Issue | Minimal Fix | Priority |
|---|---|---|---|---|
| Abstract | “built around an explicit authorization boundary around generation” | Repeated preposition. | “built with an explicit authorization boundary around generation” | P2 |
| Figure 1 | “The only stage calling the language model.” | Too broad given the LLM rewriter. | “The only stage calling the answer generator.” | P1 |
| §3.1 | “Six regional synonym presets extend normalization for supported dialect forms…” | Includes Standard Bengali as regional. | “Six language presets, including Standard Bengali and five regional varieties, extend normalization…” | P2 |
| §4 S1 | “The interface displays sources_retrieved = 0, Bengali crop choices, and non-chemical guidance (Figure 2a).” | The cited screenshot shows only part of this list. | “The interface displays Bengali crop choices (Figure 2a).” Retain the other details only with a supporting capture. | P1 |
| §5.3 | “The four missed errors and results from the larger passage-derived benchmark are reported in Appendix E.” | Overpromises the appendix’s contents. | “Aggregate catch rates for both tests are reported in Appendix E.” | P2 |
| §6 | “depends on an explicit crop mention or a confident image prediction” | Incorrect logical connector. | “…an explicit crop mention and a confident image prediction…” | P2 |
| §B.1 | “A 160-character Bengali advisory therefore occupies two or three SMS segments rather than one.” | Exactly 160 characters require three under the stated encoding assumptions. | “A 160-character Bengali advisory therefore occupies three SMS segments.” | P2 |

No broad grammar cleanup is warranted.

## 6. AI-Like / Formulaic Prose

**No meaningful AI-style problems were found.** Prose alone cannot establish authorship.

| Location | Text/phrase | Why it sounds formulaic | Recommended action |
|---|---|---|---|
| Abstract | “around … around” | Local repetition, classified as an **ACTUAL PROBLEM**, not evidence of AI authorship. | Apply the small correction above. |

The repeated “This step shows…” explanations in §4 serve the demonstration sequence. The recurring admission/evidence/release terminology names the actual architecture. Both are **NORMAL ACADEMIC STYLE — DO NOT CHANGE**.

## 7. Numerical Consistency

| Value/Claim | Location A | Location B | Status | Action |
|---|---|---|---|---|
| Cross-crop retrieval counts | PDF §5.2/Table 7: **146/400 → 121/400** | Public reproduction package: **145/400 → 120/400** | Actual artifact–paper inconsistency. | Reconcile the package with the final recorded run. |
| Bengali-native subset | Table 8: 70 additional probes | Same table: outcomes over 100 | Explainable denominator ambiguity. | State **30 + 70 = 100**. |
| Six regional presets | §3.1 | Appendix A: Standard Bengali plus five regional varieties | Categorical-count wording mismatch. | Describe six presets, five regional. |
| SMS segments | §B.1: 67 characters per concatenated part | Same section: exactly 160 characters in two or three parts | Arithmetic inconsistency. | State three segments. |
| Video chapter timing | Screencast page: through 2:30 | Player metadata: 48.67 seconds | Actual resource-description mismatch. | Synchronize the chapter guide and recording. |

The principal PDF results and reported Wilson intervals checked consistently. Harmless rounding, including **6 × 10⁻⁸ versus 5.96 × 10⁻⁸**, needs no correction.

## 8. Terminology Consistency

- **T0/T1/T2 responsibilities:** reconcile Figure 1 with the prose.
- **`krishokchat-4b`:** identify the evaluated model and distinguish it from the released Gemma 4 adapter.
- **ASR/PHI:** expand once.
- **PRISM conflicts:** identify the set or use the manuscript’s established term, “synthetic conflicts.”
- **Table 7, extractor accuracy:** “miss 1.5%, false positive 3.0%” can be read as crop-presence errors, whereas Appendix A says the errors concern crop identity. Specify that these are **normalized crop-label errors**, with the intended definitions.

The KrishokChat/KrishokTech distinction is explicitly explained in §6 and does not need another naming change.

## 9. Figure ↔ Text Audit

| Figure | Status | Problem | Action |
|---|---|---|---|
| Figure 1 | Fix | Stage assignments differ from the prose; “only” language-model-call claim is too broad. | Correct labels as P1-1. |
| Figure 2a | Fix | Zero-source counter and non-chemical guidance are not visible. | Adjust the capture or the referring sentence. |
| Figure 2b | OK | Bengali text communicates the rice/potato conflict; the warning is visible. | No substantive change. |
| Figure 2c | OK | Referral notice and 16123 button are visible. | No substantive change. |
| Figure 2d | OK | Shows the dropped 20 g/L claim and supporting 2 g/L evidence, consistent with a 10× error. | Define PHI for readers. |
| Figure 3 | Fix | Same missing S1 indicators as Figure 2a; very small displayed size. | Enlarge and align its evidentiary description. |
| Figure 4 | Fix | Shows the selected rice example/evaluation interface, but not an inspectable retrieval scope. | Use a result capture showing the claimed scope, or narrow the caption. |
| Figure 5 | Content OK; size fix | Conflict screen is present but miniature. | Enlarge in Appendix C. |
| Figure 6 | Content OK; size fix | Referral screen is present but miniature. | Enlarge in Appendix C. |
| Figure 7 | Content OK; size fix | DROP evidence is present but miniature. | Enlarge in Appendix C. |

## 10. Table ↔ Text Audit

| Table | Status | Problem | Action |
|---|---|---|---|
| Table 1 | OK | Main counts and sequence agree with the evaluation. | None. |
| Table 2 | OK | Category totals, benign controls and Wilson interval agree. | None. |
| Table 3 | OK | Paired sample sizes and retention values agree with §B.1 and Table 8. | None. |
| Table 4 | OK | Sizes agree with the prose; language-model weights are explicitly excluded. | None. |
| Table 5 | OK | Latencies agree with §B.5; the caption correctly explains component medians. | None. |
| Table 6 | OK | 200 dialogues and 425 turns reconcile; duplicate crop-shift scoring is explained. | None. |
| Table 7 | Minor clarification; size fix | Crop-label error terminology and unexplained PRISM label; very small text. | Clarify terms and enlarge. |
| Table 8 | Minor clarification; size fix | Bengali-native subset composition, undefined acronyms and SMS wording. | Apply the listed corrections and enlarge. |

## 11. References / Cross-References Audit

Figure, table, section and appendix numbering is coherent. No unresolved “??” references or references to nonexistent numbered items were found.

Concrete corrections:

- §5.3’s reference to the **four missed errors** overstates what Appendix E contains.
- Appendix A’s two source-file hyperlinks are relative URI targets.
- Protect bibliography capitalization.

Two potentially suspicious reference details checked out:

- Chen et al.’s **volume 2025, pages 32244–32279** matches the publisher’s BibTeX; leave it alone. [ICLR record](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4ffd05ca3cf3985f4572af015b4cfc1e-Abstract-Conference.html).
- The two-author KrishokChat reference matches **arXiv v1**. The latest version has a different title and an additional author, so this is a version distinction, not proof of an incorrect citation. Cite `v1` explicitly if that is the intended version. [Version 1](https://arxiv.org/abs/2606.29243v1), [current version](https://arxiv.org/abs/2606.29243).

## 12. Link & Availability Audit

Checked on **22 September 2026**.

| URL/resource | Status | What was verified | Issue/action |
|---|---|---|---|
| [Public interface](https://krishoktech.vercel.app) | Accessible without login | Homepage and advisory interface load. | Consistent with the manuscript’s “preview” description. |
| [Advisory page](https://krishoktech.vercel.app/chat) | Interface accessible; request failed | The paper’s Romanized S1 example returned `qa stream failed: 503`. | Interactive execution was unavailable during this check. This does not invalidate the explicitly limited preview claim. |
| [Screencast](https://krishoktech.vercel.app/screencast) | Accessible and playable | Video loaded and played; metadata reports 1920×1080, 48.67 seconds. | Correct the chapter guide, which extends to 2:30. |
| [GitHub implementation](https://github.com/RaiyaanReza/KrishokChat-Agricultural-Advisory-System) | Public | README, source tree, controls, tests and experiment records accessible. | Address P1-2 and P1-3. |
| [Vision models](https://huggingface.co/RaiyanKhaan/KrishokTech-Models) | Public; not gated | ONNX files and model documentation listed. | Identify the exact evaluated model/export configuration where it differs from the broader release. |
| [Adapter and evidence index](https://huggingface.co/RaiyanKhaan/KrishokChat-Advisory-System) | Public; not gated | Adapter configuration, adapter weights and BM25/index artifacts listed. | Clarify evaluated-model correspondence. Large weights were not downloaded or executed. |
| [krishibangla.com](https://krishibangla.com) | **Could not verify externally.** | Retrieval timed out. | Do not infer that it is broken. |
| Appendix A source-file paths | Malformed as public links | PDF annotations use repository-relative URI strings. The named files exist in GitHub. | Replace with absolute repository links or plain code paths. |

Repeated PDF link annotations caused by line wrapping are not accidental duplicate resources.

## 13. Reproducibility Sanity Check

Only three concrete issues require attention:

1. The evaluated local model is not unambiguously mapped to the released adapter.
2. The quick-start runner presents fixed result summaries as reproduced measurements.
3. The adjacent source bundle does not reproduce the final PDF.

The repository, model artifacts and evidence-index files are publicly available. The paper adequately distinguishes browser-side processing, local retrieval and the additional requirements of local generation.

## 14. Silly/Unnecessary Detail Audit

No substantial pruning is warranted.

Remove the accidental repeated “around,” replace unexplained “PRISM” with the established set description, and correct “full-size screens” unless the appendix images are enlarged. The explicit limitations, component timings and distinction between SMS rendering and the complete response serve concrete purposes.

## 15. Reviewer Confusion Points

| Location | Confusing text/detail | Why it may confuse | Minimal clarification |
|---|---|---|---|
| Figure 1 versus §3 | Missing-crop check under T0 in the figure | The text assigns it to T1. | Use one stage assignment consistently. |
| §§5.3/6 and artifacts | `krishokchat-4b` versus released Gemma 4 adapter | The reader cannot identify the evaluated artifact. | Name the model behind the evaluation and distinguish other releases. |
| Table 8 | 70 Bengali-native probes, results over 100 | Subset overlap is unstated. | Explain the 30 + 70 composition. |
| Table 7 versus Appendix A | “miss” and “false positive” alongside perfect crop-presence separation | Error types appear contradictory without specifying identity versus presence. | Label these as crop-identity errors. |
| §4 versus screenshots | Visible zero-source counter/evidence scope claimed but not shown | The reader cannot locate the cited interface evidence. | Adjust the capture or referring text. |

## 16. Claims vs Evidence

- **Figure 1’s “only stage calling the language model”** exceeds the architecture described in Appendix D. Narrow it to the answer generator.
- **The repository’s “all principal paper metrics … reproduced”** exceeds what its summary runner actually computes. Relabel fixed summaries and link the existing measurement procedures.
- **The claimed visibility of specific S1/S2 indicators** exceeds what the supplied screenshots show.

The manuscript’s main result claims are otherwise appropriately bounded. In particular, it acknowledges alias-list dependence, synthetic conflicts, inserted dosage errors, residual attacks and the absence of field-outcome evidence. Those qualifications should remain.

## 17. Final 15-Minute Fix List

**P1 — resolve first**

1. Correct Figure 1’s stage labels and answer-generator wording.
2. Correct the reproduction package’s stale counts and distinguish executed checks from reported summaries.
3. Reconcile the evaluated Gemma 3 deployment with the released Gemma 4 adapter.
4. Align screenshot claims with visible evidence and enlarge the appendix material.
5. Recover the exact source bundle for the final PDF.

**P2 — small edits**

1. Remove the abstract’s repeated “around.”
2. Describe Standard Bengali plus five regional presets accurately.
3. Change “or” to “and” in the conflict-detection limitation.
4. Correct the cross-reference promising descriptions of the four misses.
5. Explain the Bengali-native subset as 30 + 70.
6. Correct exactly 160 Bengali characters to three SMS segments.
7. Define ASR/PHI and clarify PRISM and crop-identity error terminology.
8. Repair the two relative source hyperlinks.
9. Protect bibliography proper names and acronyms.
10. Synchronize the screencast chapter timings with the linked video.

## 18. FINAL VERDICT

**DO NOT SUBMIT YET**

The paper does not need another conceptual revision. Its main numerical results and restrained conclusions are coherent, but the architecture diagram and linked artifacts still create concrete contradictions that a reviewer could encounter immediately. Resolve the model identity and reproduction-package wording, synchronize the source bundle, and make the cited visual evidence inspectable. These corrections address presentation and verification credibility without requiring new experiments or changing the paper’s central narrative.