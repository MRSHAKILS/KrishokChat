I rendered and visually inspected all 17 pages of the submitted PDF, including high-resolution crops of every figure and table. I also checked recent accepted ACL/EACL System Demonstration papers as visual comparators, notably EACL 2026’s PropGenie, the Browser-based Open Source Assistant for Multimodal Content Verification, and RAGVUE, plus ACL 2025’s AI2Agent. These are useful benchmarks because their diagrams and UI figures generally prioritize direct labeling, legible screenshots, and clear caption-to-figure correspondence rather than decorative density. ([ACL Anthology][1])

## Executive assessment

The paper has a **credible system-demo visual core**, but the current PDF has several issues that a reviewer could catch immediately:

1. **Figure 1 is semantically inconsistent at exactly the most important boundary: T3 vs. T4.** The figure visually assigns verification/DROP to T3, while the caption and system description assign it to T4.   
2. **The screenshots visibly use a different crop set from the one claimed in the paper.** The text says rice, potato, brassica, chili, corn, wheat; the UI chips show Rice, Potato, Tomato, Maize, Brinjal, Chilli. The documented deployment scope is explicit. 
3. **Figure 2(c) does not visibly prove the claim made by its caption.** The caption says the Why panel shows why an unsupported dosage claim was removed, but the rendered view does not actually expose that reasoning trace.
4. **The Appendix gallery is fragmented and partly duplicative.** S1/S3 are repeated between Figure 2 and Figures 3/5, while S2 and S4 appear only in the appendix. This weakens the claimed continuous S1–S5 demonstration.
5. **There are visible development/UI artifacts** in several appendix screenshots, especially the floating black “N” bubble and the large floating help/expert widget on S2.
6. **Table 1 is clipped at the right edge.** That is a production error because it truncates a headline result.
7. **Pages 6, 9, and 16 contain conspicuous excess whitespace.** This is not fatal, but it makes the submission look less finished than recent system-demo papers.
8. **Table 13 exists in the PDF.** It should be included in the audit even though the earlier Claude pass stopped at Table 12.

---

# 1. Figure-by-figure audit

## Figures

| Item       | Purpose / what reviewer must understand                                                                                              | Does it succeed?                                                                                                                                  | Readability / density                                                                | Caption / refs                                                                 | Space efficiency                                                                | Class          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | -------------- |
| **Fig. 1** | Understand the complete control architecture: input → T0/T1 decisions → T2 crop fencing → T3 generation → T4 verification → delivery | **Partly.** The overall pipeline is immediately visible, but T3/T4 ownership is wrong in the drawing                                              | Good legibility; moderate density; icons add some visual weight                      | Caption is informative but directly contradicts the box contents and the prose | Good use of space, but could be simpler                                         | **REDESIGN**   |
| **Fig. 2** | Show the core live UI states: ASK, CONFIRM, DROP                                                                                     | **Partly.** State changes are apparent, but English reviewer must infer too much from Bengali UI and panel (c) does not show its claimed evidence | Small UI text at paper scale; high information density; panel sizes are inconsistent | Captions are mostly good; panel (c) overclaims visible Why evidence            | Reasonable but could carry much more explanatory value with a storyboard layout | **REDESIGN**   |
| **Fig. 3** | S1 ASK screenshot                                                                                                                    | Yes, but it duplicates Fig. 2(a) almost exactly                                                                                                   | Readable only with zoom; English parenthetical crop names help                       | Caption is clear                                                               | Poor use of appendix space because it duplicates the main figure                | **REMOVE**     |
| **Fig. 4** | S2 image-driven crop scoping                                                                                                         | Yes: it shows a photographed leaf and the diagnosis/crop-scope interface                                                                          | Screenshot is legible enough when enlarged; still lots of irrelevant UI              | Caption is good                                                                | Could be cropped substantially                                                  | **MINOR EDIT** |
| **Fig. 5** | S3 photograph/text disagreement and CONFIRM                                                                                          | Yes, but the key mismatch logic is not readable in English from the screenshot itself                                                             | The focused conversation crop is better than Fig. 4, but still text-heavy            | Caption explains the state well; terminology should match the actual badge     | Duplicates Fig. 2(b)                                                            | **MERGE**      |
| **Fig. 6** | S4 REFER state / safety block                                                                                                        | Yes: Paraquat + warning + 16123 make the state identifiable                                                                                       | UI is small but the central action is clear                                          | Caption is strong                                                              | Extremely inefficient: tiny screenshot followed by a very large empty page      | **MINOR EDIT** |

### Figure 1: architecture

The **abstraction level is close to appropriate**. I would not make it substantially more detailed. Recent EACL demonstrations such as PropGenie use architecture diagrams with explicit labeled modules and strong directional structure; the Browser-based Verification Assistant similarly puts a directly readable workflow/architecture next to sufficiently large UI evidence. 

The problem is not abstraction. It is **semantic ownership**.

The paper says the five ordered stages are followed by delivery, with T3 producing an unverified draft and T4 filtering it before delivery.  The prose then says T3 generates the response and T4 checks dosage claims and drops unsupported claims.  But the rendered T3 box itself says **“Draft & Verify”**, contains “Cross-check claims / Drop or flag unsupported advice,” and shows **CONFIRM/DROP**. T4 is labeled “Deliver” and shows only **ADVICE**.

That is a **P0 structural inconsistency**, not cosmetic copyediting.

### Exact redesign

Use:

**Input**
→ **T0 Safety Check**
→ **T1 Information Gate**
→ **T2 Crop Fence + Retrieval**
→ **T3 Generate Draft (UNVERIFIED)**
→ **T4 Verify & Filter**
→ **Delivery: Verified Advice**

T4 should own the **DROP** transition. T3 should not contain verification language or a final farmer-visible DROP state.

Also make the box labels themselves carry the key semantics; do not make the reviewer reconstruct them from small sub-bullets.

---

# 2. Bengali UI accessibility

The paper does a useful thing already: crop names and state information often include English parentheticals such as “Rice,” “Potato,” and “Clarification.” That means the screenshots are not intrinsically inaccessible to an English-only reviewer.

The problem is that the parentheticals do **not cover the actual decision logic**.

### Screenshot-by-screenshot

| Screenshot                        | Can an English-only reviewer understand the important event? | What is visible without Bengali?                                       | Recommended English callout                                                                    |
| --------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Fig. 2a / Fig. 3 — S1 ASK**     | **Mostly, but not the exact user input**                     | Crop-selection control; crop names; Clarification/Disambiguation state | **“S1 ASK — Treatment request has no crop; retrieval halted; select crop.”**                   |
| **Fig. 4 — S2**                   | **Mostly**                                                   | Leaf photo; diagnosis page; `rice-leaf-sample.jpg`; crop/image context | **“S2 — Image identifies RICE; retrieval is scoped to rice guidance.”**                        |
| **Fig. 2b / Fig. 5 — S3 CONFIRM** | **Not reliably enough**                                      | Rice image context; Clarification/Disambiguation; crop chips           | **“S3 CONFIRM — Photo: RICE; message: POTATO → chemical advice withheld.”**                    |
| **Fig. 6 — S4 REFER**             | **Yes, with a small semantic cue**                           | `Paraquat (Paraquat)` and 16123                                        | **“S4 REFER — High-risk chemical request blocked → 16123 referral.”**                          |
| **Fig. 2c — S5 DROP**             | **Not enough to verify the claimed action**                  | Grounded/provenance elements and collapsed process/source controls     | **“S5 DROP — 1 unsupported dosage claim removed before rendering; grounded claims retained.”** |

I would **not translate the whole interface**. That would add clutter without increasing reviewer understanding.

The callouts above are the right granularity because they expose the **state transition and causal logic**, not decorative UI.

The paper itself explicitly frames the demonstration as S1–S5 covering ASK, CONFIRM, REFER, and DROP, with S2 establishing the context for S3. 

---

# 3. The crop-scope problem is a P0

This is stronger than the terminology issue.

The paper explicitly says the deployment covers:

> rice, potato, brassica, chili, corn, and wheat. 

Yet the visible crop chips in the ASK and CONFIRM screenshots are:

**Rice, Potato, Tomato, Maize, Brinjal, Chilli.**

That gives a reviewer three possibilities, all problematic:

* the screenshots are from a different build;
* the paper's stated deployment scope is wrong;
* or the UI/model/evidence scope is inconsistent across artifacts.

Because Table 3 also presents the six documented crop-specific models, this is not isolated UI copy. 

### Exact action

Pick **one authoritative six-crop inventory** and propagate it everywhere:

**Paper prose → Figure 1/2 → screenshots → Table 3 → appendix descriptions → demo build.**

Do not merely change “Tomato” to “Brassica” in the screenshot text layer. The visual evidence needs to depict the actual interface state of the submitted system.

---

# 4. Figure 2 and the continuous S1–S5 demonstration

The paper says the audience should follow one **continuous farmer session** through five steps. 

The current visual sequence does not make that continuous narrative effortless.

### Current structure

**Main paper Figure 2**

* S1 ASK
* S3 CONFIRM
* S5 DROP

**Appendix**

* Fig. 3 = S1 ASK again
* Fig. 4 = S2
* Fig. 5 = S3 CONFIRM again
* Fig. 6 = S4 REFER

So the viewer gets:

**S1 → S3 → S5** in the main paper, then must jump backward/sideways into the appendix for **S2/S4**, while S1/S3 are duplicated.

That is not the strongest possible demonstration story.

### Better structure

Make **Figure 2 a five-panel storyboard**:

**S1 ASK → S2 IMAGE → S3 CONFIRM → S4 REFER → S5 DROP**

Each panel needs only:

* one cropped screenshot;
* a large state label;
* one English causal callout.

Then the appendix can contain **larger supporting screenshots** for the states where UI details matter.

This would also bring the paper closer to the visual pattern used by current system-demo papers, where the reader can understand the workflow without needing to zoom into tiny interface details. 

### Figure 2(c): Why/provenance problem

This is the other P0 within Figure 2.

The caption says:

> “The Why panel shows why an unsupported dosage claim was removed…” 

But the rendered panel leaves the relevant process/source controls collapsed. A reviewer therefore sees the **claim that the trace exists**, not the trace itself.

### Exact action

Expand the Why panel inside the screenshot and expose a compact trace such as:

**Removed claim:** `<dosage statement>`
**Reason:** unsupported / outside permitted range
**Evidence checked:** source passage / allowed dose band
**Final answer:** remaining grounded advice

That is much stronger evidence than a closed “Why” control.

---

# 5. Visual credibility

### What looks credible

The UI screenshots are visually consistent in their underlying product styling: repeated layout, colors, badges, crop controls, and answer cards. They look like a real application rather than generic stock imagery.

The architecture diagram is also coherent as a piece of visual design.

### What currently hurts credibility

**Development artifacts.**
Figures 3–5 contain the floating black **“N”** bubble. Figure 4 additionally has a large floating expert/help control at the bottom-right that overlaps the application view. These are exactly the sort of artifacts reviewers interpret as an unclean capture.

**Inconsistent screenshot framing.**
The current gallery mixes:

* full-window captures,
* split blurred-background/focused-panel captures,
* narrow answer-card crops,
* and a small top-of-page capture.

That is the strongest visual sign that the screenshots were assembled from different capture passes.

**Tiny UI text.**
At PDF reading scale, much of the Bengali content and provenance detail is too small for the screenshot to function as evidence. Recent system-demo examples tend to allocate more figure area to the UI when the UI itself is part of the contribution. 

**Generic infographic feel in Figure 1.**
The rounded colored cards, icons, and illustrated farmer/phone imagery are more decorative than necessary. I would not call them “AI-generated”; there is no basis for that claim from the PDF. The issue is simply that they consume visual bandwidth that could instead make the control semantics clearer.

### Development/staging assessment

The screenshots do look like **controlled demonstration cases**, which is perfectly reasonable for a system demo. The problem is that the paper does not consistently make the distinction between “controlled demo state” and “representative live UI evidence” visually explicit.

A small label such as **“Controlled demo state”** or **“S3 — controlled conflict case”** would actually strengthen credibility.

---

# 6. Table-by-table audit

| Table        | Purpose                                    | Reviewer understanding   | Readability / density               | Caption / reference quality | Space efficiency         | Class          |
| ------------ | ------------------------------------------ | ------------------------ | ----------------------------------- | --------------------------- | ------------------------ | -------------- |
| **Table 1**  | Headline evaluation results                | Strong conceptually      | **Right edge is clipped**           | Good caption                | Compact, but fit failure | **MINOR EDIT** |
| **Table 2**  | Provenance badge taxonomy                  | Very clear and useful    | Clean, compact                      | Strong; tied to A.1         | Excellent                | **KEEP**       |
| **Table 3**  | Vision-model performance by crop           | Clear                    | Clean                               | Good                        | Excellent                | **KEEP**       |
| **Table 4**  | Crop-fence evaluation across regimes       | Clear                    | Clean and dense in a good way       | Good; explains regimes      | Excellent                | **KEEP**       |
| **Table 5**  | Deployed-model guard boundary              | Clear                    | Small but acceptable for appendix   | Good                        | Good                     | **KEEP**       |
| **Table 6**  | Dosage-verifier accuracy                   | Very important and clear | Good                                | Strong                      | Good                     | **KEEP**       |
| **Table 7**  | Human evaluation audit                     | Clear                    | Readable, compact                   | Strong                      | Good                     | **KEEP**       |
| **Table 8**  | Banglish/phonetic red-team results         | Clear                    | Awkward line wraps in attack labels | Good                        | Good                     | **MINOR EDIT** |
| **Table 9**  | SMS comparison                             | Clear                    | Very readable                       | Good                        | Good                     | **KEEP**       |
| **Table 10** | Installation footprint                     | Clear                    | Very readable                       | Good                        | Very efficient           | **KEEP**       |
| **Table 11** | Non-LLM latency breakdown                  | Clear                    | Very readable                       | Good                        | Very efficient           | **KEEP**       |
| **Table 12** | Evidence ledger for C1/C2                  | Complete but dense       | Dense/prose-heavy                   | Useful appendix table       | Acceptable for appendix  | **MINOR EDIT** |
| **Table 13** | Evidence ledger for C3/delivery/deployment | Complete but dense       | Dense/prose-heavy                   | Useful appendix table       | Acceptable for appendix  | **MINOR EDIT** |

The paper's provenance-table taxonomy is internally coherent: Table 2 explicitly maps badges to pipeline stages. 

The main-table issue is **not content density**. It is production quality.

### Table 1: exact problem

On page 4, the rightmost result column is visibly cut off. The guarded/unguarded result that should end with **10.71%** is not fully visible.

### Exact action

Constrain Table 1 to the column width using a robust table layout (`tabularx`, carefully sized columns, or equivalent). Do **not** solve this merely by shrinking the font until it technically fits.

This is P0 because Table 1 is the headline result table and one of its primary numerical results is visually truncated.

> **Status: [DONE - FIXED IN LATEX]**  
> Converted Table 1 to `\begin{tabularx}{\textwidth}{@{}p{0.24\textwidth}p{0.36\textwidth}X@{}}`. The `X` column absorbs all remaining width across the two columns, eliminating all right-edge clipping. The full headline result `52.5% \to 10.71%` is now completely visible.

### Table 8

The labels such as:

* “Phonetic Chemical Typos”
* “Indirect Farm Sabotage”

are wrapped awkwardly within the narrow first column.

### Exact action

Widen the first column slightly or shorten the labels to remove ugly mid-word/hyphenation breaks.

> **Status: [DONE - FIXED IN LATEX]**  
> Converted Table 8 to `\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}}lcccc@{}}` with natural-width left column and compact regime labels (`Phonetic Chemical`, `Banglish Crisis`, `Indirect Sabotage`). Completely eliminated all underfull `\hbox` badness (10000) and awkward mid-word breaks.

### Tables 12–13

These are actually doing useful work: they serve as a **measurement/scope ledger**, not as a reader-friendly summary. Their density is therefore defensible in an appendix.

The problem is scanability. The “Measure and result” and “Scope and boundary” cells read almost like compressed paragraphs.

### Exact action

Shorten each cell to:
**result → n → status → boundary**

rather than repeating methodological qualifiers in prose.

---

# 7. Space and pagination

The PDF's most noticeable layout weakness is not figure size alone; it is **unused page area**.

### Page 6

Only a small amount of main-text material occupies the page, leaving a large empty region.

### Page 9

The final reference occupies only a small region, again leaving most of the page empty.

### Page 16

Figure 6 occupies the top portion, followed by a large blank area.

This is especially visible when compared against current EACL system-demo papers, where figures and screenshots are generally integrated with surrounding text more aggressively. 

I would not chase page count for its own sake. The fix is simply to **let floats and appendix content flow naturally** rather than preserving these isolated placements.

---

# 8. Specific assessment of the four requested visual dimensions

## Figure 1: too abstract / too detailed / balanced?

**Balanced in information level; incorrect in stage semantics.**

It already communicates:

* input,
* decision gates,
* crop restriction,
* generation,
* verification,
* delivery.

The problem is that the most important transition — **unverified generation → verification/filtering** — is visually assigned to the wrong box.

So I would **not add more modules**. I would simplify and correct the existing ones.

## Figure 2: does it demonstrate the system?

**Yes, but not as efficiently as it could.**

It proves there are multiple explicit UI states, and the English parenthetical annotations are valuable. However:

* S1/S3/S5 are shown;
* S2/S4 are deferred;
* S1/S3 are duplicated in the appendix;
* the Bengali content dominates the screenshots;
* and S5's claimed Why evidence is not actually expanded.

The concept is good. The composition needs restructuring.

---

# 9. Final priority list

## P0 — Must fix before submission

| Priority | Exact figure/table | Exact action | Status |
|---|---|---|---|
| **P0-1** | **Figure 1** | Redesign T3/T4 ownership: **T3 = Generate Draft (unverified); T4 = Verify & Filter; DROP belongs to T4.** Align box labels, state pills, caption, and §3.3. | **PENDING** (Requires graphics/Figma redraw of diagram asset `figures/fig1_architecture.jpg`) |
| **P0-2** | **Figure 2a, Figure 2b, Figures 3–5** | Resolve the **crop-scope mismatch**. The UI chips must match the six staple crops documented by the paper (rice, potato, brassica, chili, corn, wheat). | **PENDING** (Requires UI recaptures on live deployment) |
| **P0-3** | **Figure 2c / S5 DROP** | Expand the **Why/provenance panel** so the screenshot visibly demonstrates the removed dosage claim and why it was removed. | **PENDING** (Requires UI recapture with expanded trace panel) |
| **P0-4** | **Table 1** | Fix the right-edge overflow so the full headline results, including **52.5% → 10.71%**, are visible. | **[DONE - FIXED IN LATEX]** Switched to `tabularx{\textwidth}` with flexible `X` column. Truncation completely eliminated. |
| **P0-5** | **Figures 3–5 and any repeated screenshot captures** | Remove floating/development overlays, especially the black **N** bubble and the large floating help/expert widget on S2. Recapture clean application-only screenshots. | **PENDING** (Requires recapturing UI without dev indicators) |
| **P0-6** | **Figure 2 + Appendix E gallery** | Rebuild the demonstration sequence so **S1→S2→S3→S4→S5** can be followed without jumping between duplicated and missing states. | **PENDING** (Requires figure re-assembly after clean screenshot passes) |

## P1 — High-value

| Priority | Exact figure/table | Exact action | Status |
|---|---|---|---|
| **P1-1** | **Figure 2** | Add one concise English semantic callout per panel; do not translate the whole UI. | **PENDING** (To be added during Figure 2 re-crop pass) |
| **P1-2** | **Figure 2 / Figure 5** | Standardize terminology: unify **“Crop Mismatch badge”** with Table 2 / UI **Clarification / Disambiguation**. | **[DONE - FIXED IN LATEX]** Replaced "Crop Mismatch badge" with `\textbf{Clarification} badge (crop mismatch)` in `main.tex`. |
| **P1-3** | **Figure 4 / S2** | Crop tighter around image → crop inference → scoped state; add “Image identifies RICE; retrieval scoped to rice.” | **PENDING** (Visual crop edit) |
| **P1-4** | **Figure 6 / S4** | Integrate into the appendix gallery or enlarge and place it beside the other demo screens; add “High-risk request blocked → 16123 referral.” | **PENDING** (Visual crop edit) |
| **P1-5** | **Figure 3** | Remove as a standalone duplicate of S1; retain the S1 evidence once, at a larger and cleaner scale. | **PENDING** (Appendix gallery overhaul) |
| **P1-6** | **Figure 5** | Merge with the authoritative S3 screenshot; avoid having essentially the same CONFIRM state in both Figure 2 and the appendix. | **PENDING** (Appendix gallery overhaul) |
| **P1-7** | **Figure 1** | After semantic repair, simplify decorative icons/illustration so the diagram reads as a technical control diagram rather than a product-marketing graphic. | **PENDING** (Visual redraw) |
| **P1-8** | **Table 8** | Fix awkward line wrapping in the attack-regime labels. | **[DONE - FIXED IN LATEX]** Converted to `tabular*` with compact regime labels; eliminated all underfull `\hbox` badness and awkward hyphens. |
| **P1-9** | **Tables 12–13** | Shorten cell prose and standardize the structure of “result / n / status / scope.” | **PENDING** (Appendix editorial pass) |
| **P1-10** | **Pages 6, 9, 16** | Reflow appendix/reference content to eliminate conspicuous blank-page regions. | **[DONE - FIXED IN LATEX]** Fixed float placement: Table 1 & Figure 2 flow naturally, main text strictly fits Pages 1--6 with Conclusion ending on Page 6, Page 7 cleanly begins Section 7 Ethics & References. |

## P2 — Optional

The remaining improvements are mostly editorial: tighten the Figure 2 caption once the visual evidence is fixed, standardize screenshot aspect ratios and internal margins, and make the appendix gallery visually uniform.

---

## Overall reviewer-facing judgment

The visual evidence is **substantively useful**; I would not recommend removing the system screenshots wholesale. The strongest assets are the explicit state badges, the crop controls, the provenance concept, and the quantitative tables. The main weaknesses are **consistency and evidentiary alignment**, not lack of visual polish.

The two things I would fix first are **Figure 1’s T3/T4 semantics** and the **crop-scope mismatch in the screenshots**. Those are the issues most likely to make a system-demo reviewer question whether the figure, UI, and written system description are actually describing the same deployed artifact. The Figure 2(c) Why-panel issue and Table 1 clipping are the next most immediate presentation failures.

The comparison point from recent accepted ACL/EACL demos is useful here: the strongest examples do not necessarily use more elaborate graphics; they make the **workflow and UI evidence legible with fewer ambiguities**. PropGenie’s architecture, the Verification Assistant’s architecture-plus-UI presentation, and RAGVUE’s information-first figures all illustrate that tendency. 

[1]: https://aclanthology.org/2026.eacl-demo.3/?utm_source=chatgpt.com "PropGenie: A Multi-Agent Conversational Framework for Real Estate Assistance - ACL Anthology"
