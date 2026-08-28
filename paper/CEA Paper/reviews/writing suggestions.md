# Comprehensive Editorial Review: Writing, Structure & Presentation
## *Computers and Electronics in Agriculture* — Manuscript Assessment

---

## I. OVERALL VERDICT (Editor's Summary)

The manuscript presents a technically ambitious architecture with a strong empirical backbone. However, **as a writing and presentation artifact, it reads as a technical report or internal lab document rather than a polished journal submission.** The prose is over-dense, self-referential, defensive, and structurally bloated. The formatting has several LaTeX-level issues, figure/table placement is suboptimal, and the rhetorical strategy—while admirably honest—undermines the paper's own authority. In its current state, this would receive a **Major Revision** or **Reject & Resubmit** at CEA on writing/presentation grounds alone, regardless of scientific merit.

Below is a section-by-section, line-by-line dissection.

---

## II. TITLE AND FRONT MATTER

### 2.1 Title
> *"Bounded-Authority Agricultural Advisory: Selective Resolution and Evidence-Bound Verification for Safe Bengali Decision Support"*

**Issues:**
- **22 words / 136 characters.** CEA titles in the last two years average 12–16 words. This is a subtitle-plus-subtitle construction. The reader must parse two compound noun phrases joined by a colon.
- "Bounded-Authority Agricultural Advisory" is an architecture name, not a finding. Top CEA titles name the *contribution* or *finding*: e.g., *"A time-aware retrieval-augmented generation framework for..."* (TARAG, cited in this paper).
- "Safe Bengali Decision Support" buries the domain (crop protection / pesticide advisory) under a vague phrase.

**Suggested rewrite (≤15 words):**
> *"Bounded-Authority Verification for Safety-Critical Pesticide Advisory in Low-Resource Bengali Agriculture"*

### 2.2 Author Block & Affiliations
- Two authors, two affiliations — clean. ✓
- ORCID present. ✓
- **However:** The `\credit{}` for Author 1 includes *seven* CRediT roles including "Project Administration." For a two-author paper this looks like a solo-project with a supervisor attached. Consider whether "Project Administration" adds credibility or raises a question.
- `\cormark[1]` and `\cortext[1]` are correctly used. ✓

### 2.3 Abstract (297 words)
**Target for CEA:** 150–250 words (structured abstract preferred by Elsevier).

**Problems:**

| Issue | Location | Comment |
|---|---|---|
| No structured headings | Entire abstract | CEA now encourages **Background / Methods / Results / Conclusion** sub-headings. This is a single wall of text. |
| Overloaded with numbers | ¶2–3 | The abstract contains **14 distinct numerical results** (10,000; 100.0%; 99.96; 80.0%; 38.65%; 97.0%; 0.0%; 4.82/5; 0.862; 84.56%; 1.26%; 61.5%; 2.28×; 89.7%). A reader cannot retain these. Pick the **3–4 headline numbers**. |
| Jargon before definition | Line 2 | "Bounded-Authority Advisory Architecture (BAA)" is introduced but the *problem* sentence before it is 38 words long. |
| Defensive hedging | "carry no intrinsic bound on factual authority" | Awkward. "Lack factual grounding guarantees" is cleaner. |
| Missing | — | No sentence on *practical impact* or *deployment context*. CEA readers are agricultural engineers; they need the "so what for a farmer?" sentence. |

**Recommendation:** Restructure as:
> **Background** (2 sentences) → **Method** (2 sentences) → **Results** (2–3 sentences, 3–4 key numbers) → **Conclusion** (1–2 sentences with practical framing).

---

## III. SECTION-BY-SECTION WRITING REVIEW

### 3.1 Section 1: Introduction (Pages 1–2)

**Strengths:**
- The opening sentence is strong: *"A wrong agricultural recommendation can remain fluent, grounded-looking, and dangerous."*
- The potato late blight example is concrete and effective.

**Critical Issues:**

1. **§1.1 is 340 words of scene-setting before the first citation.** Top CEA papers anchor the problem in 2–3 sentences and cite within the first two. Move the "Consider a recommendation for potato late blight" example into a boxed example or defer it.

2. **§1.2 "Why Retrieval Alone Is Insufficient"** — This subsection title is an *argument*, not a *topic heading*. CEA style uses noun-phrase headings: *"Limitations of Retrieval-Only Pipelines"* or *"Retrieval Failure Modes in Agricultural RAG."*

3. **§1.3** uses the phrase *"falls into two camps"* — colloquial. Replace with *"can be categorized into two paradigms."*

4. **§1.4 Design Rule** is set as an indented block:
   > *Design Rule. In safety-critical agricultural advisory, the component that generates fluent language must not be the component that holds factual authority.*

   This is the **single most important sentence in the paper**, yet it is visually buried in a paragraph. It should be a **numbered Definition or Axiom environment** (`\begin{definition}...\end{definition}`), or at minimum a `\begin{quote}` with bold. Currently it looks like a throwaway paragraph.

5. **§1.5 Research Questions** — The heading exists but the actual RQ list appears only in **Table 1**, which floats later. The reader hits an empty subsection. Either inline the five RQs as a numbered list *or* remove §1.5 as a heading and let Table 1 carry them.

6. **§1.6 Contributions** — Three contributions is correct, but each bullet is 3–4 lines long and reads like an abstract. Tighten to one sentence each + section pointer.

### 3.2 Section 2: Related Work (Pages 2–3)

**Structural problem:** Five subsections (§2.1–§2.5) but **Table 2 (positioning) appears in §2.5**, which is the *last* subsection. In top CEA papers, the comparison table appears at the **beginning** of Related Work so the reader has the landscape before the prose.

**Writing issues:**
- §2.1: *"engaging over 15,000 farmers across four countries"* — irrelevant detail for positioning. Cut.
- §2.3: *"These works motivate our architecture: they show that..."* — This is a **conclusion sentence inside a literature review**. Move the contrast to the end of §2.5.
- §2.5 title is *"Gap and Positioning"* — "Gap" is overused and reviewers flag it. Use *"Positioning and Differentiation."*
- The final sentence of §2.5: *"The novelty we claim is not any individual component; it is the intersection..."* — The phrase **"we claim"** is weak. State it: *"The contribution is the intersection..."*

### 3.3 Section 3: Problem Formulation (Pages 3–4)

**This is the best-written section in the paper**, but has formatting issues:

- Eq. (1): The action set $\mathcal{A}$ is typeset as a `cases`-style brace. Good. ✓
- Eq. (2): The 11-slot tuple. Good. ✓
- **Eq. (3) and the five conjuncts (i)–(v):** These are explained in a **single dense paragraph** of 120+ words. Break into a **numbered list** or a small table. The reader must parse five logical conditions; a paragraph is the worst format for this.
- **Table 3** (Reliability Requirements): 9 rows × 5 columns. The column "Potential Failure Mode" has entries like *"Missing PHI/ Dosage bounds"* — inconsistent capitalization. "PHI" is all-caps but "Dosage" is title-case. Standardize.
- The table is **very wide** for a two-column CEA layout. It likely overflows or requires `\small`/`\footnotesize`. Check the compiled PDF for column bleed.

### 3.4 Section 4: Architecture (Pages 4–5)

**Major writing issue:** This section describes a five-tier architecture, but the **tiers are introduced in a paragraph, not a list.**

> *"Tier 0 — Risk and context gate. Lightweight deterministic screening..."*
> *"Tier 1 — Capability and perception router..."*

These should be a **numbered list** (`\begin{enumerate}`) or, better, a **description list** with bold tier names. Currently they are buried in running prose and the reader must hunt for each tier.

**§4.2–§4.8** are individually fine, but:
- §4.5 mentions *"a fine-tuned Gemma-4 4-bit model"* — this is an implementation detail that belongs in §6 (Methodology), not the architecture description. Architecture should be model-agnostic.
- §4.8 is titled *"Offline, Edge, and Channel Support"* — three topics in one subsection. Split or rename to *"Offline and Constrained-Channel Operation."*
- The sentence *"a farmer on a char (river island) with no mobile connectivity"* is excellent grounding. Keep it. But it appears mid-paragraph; give it its own sentence for emphasis.

### 3.5 Section 5: Knowledge Governance (Pages 5–6)

- **§5.1** lists three bullet sources (BARI, BRRI, DAE/MoA). Good, concrete. ✓
- **§5.2** introduces the authority hierarchy Eq. (4). The equation is a chain of $\succ$ relations. Fine, but the *example* that follows ("if a 2024 MoA gazette bans...") should be in an `\begin{example}` environment or at least italicized to separate it from the formal definition.
- **§5.3** uses the phrase *"We frame this as a deployment-integrity result, not a cryptography contribution"* — this is **defensive hedging**. A top paper states what it does; it doesn't pre-emptively apologize. Remove the negation and state the positive: *"This ensures offline evidence integrity without requiring a full re-download."*
- **§5.4** is 350 words and mixes ingestion pipeline, authoring cost, and scalability. Split into two subsections: *"Ingestion Pipeline"* and *"Maintenance and Scalability."*

### 3.6 Section 6: Experimental Methodology (Pages 6–7)

**This is where the paper most resembles a lab report rather than a journal article.**

- **§6.1** lists five controls (C1–C5) inline. Use a numbered list.
- **§6.2** lists nine benchmark suites as a numbered paragraph. Convert to a **table** (Suite name | n | Layer tag | Purpose). Currently the reader must parse 250 words of running text to understand the experimental design.
- **§6.4 Baseline Ladder:** Seven baselines (B0–B6) are described in bullet points. This is acceptable, but **Table 6** (which summarizes them) appears *after* the prose description. Move the table first, then use the prose only for nuances not captured in the table.
- **§6.5 Expert Evaluation:** *"Outputs were presented without system labels in a blinded, randomized order"* — good. ✓ But *"raters assigned system IDs only post-hoc"* is unclear. Do you mean raters were unblinded after scoring? Clarify.
- **§6.6 Reproducibility Protocol:** This is 80 words. It either deserves a full subsection with a table of what's recorded, or it should be folded into §14. Currently it's an orphan paragraph.

### 3.7 Sections 7–10: Results (Pages 8–12)

**This is the core of the paper and the most problematic in presentation.**

#### Structural Issue: Four Results Sections
The paper has **four** results sections (§7–§10), mapped to RQ1–RQ5. This is unusual for CEA, which typically has **one Results section** with subsections. The current structure creates a "serial paper" feel — four mini-papers stitched together. Consider:
- Merging §7 and §8 into *"Results: Advisory Quality and Safety Verification"*
- Merging §9 and §10 into *"Results: Selective Reliability and Deployment Efficiency"*

#### Writing Issues in Results:

1. **Every section opens with a bold summary sentence, then immediately undercuts it.** Example (§7):
   > *"BAA achieves 97.0% Certified Advisory Correctness on live farmer queries..."*
   > Two paragraphs later: *"Two framing caveats are noted."*

   The caveats are necessary, but the **placement** destroys the rhetorical momentum. Move caveats to a dedicated "Interpretation" paragraph at the end of the subsection, or to the Discussion.

2. **Over-reliance on parenthetical CIs.** Example:
   > *"BAA certified 65.8% of cases correctly and abstained safely in 34.2%, with 0.0% dangerous acceptance (95% CI [0.0, 0.1]) in all four registers."*

   Four percentages and a CI in one sentence. The reader's eye glazes. Use a **table** for per-register results.

3. **Footnote 1** (Page 8): *"BAA verification latency (3.8 ms) is a modeled in-process value..."* — This is a critical methodological caveat buried in a footnote. It should be in the main text of §7.1 or in a clearly marked "Note" box.

4. **Table 7** (Live benchmark): The "Latency (ms)" column has BAA at **3.8** while baselines are at 1,597–6,011. This 3–4 order-of-magnitude difference is visually misleading because 3.8 is a *modeled* value and the others are *measured*. The table needs a footnote marker on 3.8, or the column should be split into "Latency (ms, measured)" and "Latency (ms, modeled)."

5. **Table 8** (Metamorphic mutation): 7 rows × 5 columns. The "Latency p95 (ms)" column again mixes modeled (B0: 1,450; B4: 1,680; B6: 3.8) and measured values. Same issue. Add a column "Latency type" or footnote.

6. **§8.4 Parametric-vs-Evidence Conflict:** *"Note the effective sample granularity caveat reported in Section 13."* — This forward-reference to Limitations for a basic methodological caveat is poor practice. State the caveat here.

7. **§9.1 Risk-Coverage:** Table 9 is well-structured. ✓ But the paragraph after it says *"At the frozen threshold θ* = 0.2375, it sustains 84.56% test coverage at a selective risk of 1.26%—higher coverage at comparable risk than the conformal baseline (77.62% at 1.06%)."* The em-dash construction is doing too much work. Split into two sentences.

8. **§10 is titled "Deployment Efficiency and Constrained Delivery"** but contains prompt injection results (§10.4). Injection resistance is a **safety/security** result, not a deployment efficiency result. Move §10.4 to §8 or create a standalone subsection.

### 3.8 Sections 11–13: Discussion, Implications, Limitations

- **§11 (Discussion):** Well-structured with clear subsections. §11.4 ("Statistical Uncertainty and Field Safety Mitigation") is the **best-written subsection in the paper** — honest, specific, and practically grounded. Keep it.

- **§12 (Deployment Implications):** §12.6 *"What Is Not Claimed"* — While intellectually honest, this subsection reads as a **legal disclaimer** rather than a scientific discussion. Fold the key points into §13 (Limitations) and remove the standalone heading.

- **§13 (Limitations):** This is **850 words** and reads like a rebuttal to anticipated reviewer comments rather than a structured limitations section. Organize into a **numbered list** of 5–6 limitations with bold labels:
  1. Statistical power
  2. Layer-specific confounds
  3. Scope boundaries
  4. Reproducibility gaps

  Currently it is four dense paragraphs that a reviewer will skim.

### 3.9 Section 14: Reproducibility

- §14.5 *"Result-Provenance Rule"* — *"No acceptance-note prose value was used where it disagreed with the tabulated metrics"* — This is an **internal process note**, not a reproducibility statement. Remove or rephrase.
- §14.6 lists submission package contents. This belongs in a **Data Availability Statement** (already present at the end) or supplementary material, not as a subsection.

### 3.10 Section 15: Conclusion

- **380 words.** Too long for CEA (target: 150–250). The conclusion re-states numbers already in the abstract. A conclusion should: (1) restate the contribution in one sentence, (2) name the 2–3 key findings, (3) state the practical implication, (4) name the next step. Currently it does all four but also re-lists limitations, which belongs in §13.

---

## IV. FIGURE AND TABLE ASSESSMENT

### 4.1 Figures

| Figure | Page | Issue |
|---|---|---|
| Fig. 1 (Authority Model) | p. 17 | **Full-page figure at the very end.** This is the paper's conceptual anchor. It should appear in **§3 or §4** (near Eq. 3), not after the references. In the compiled PDF, it's orphaned on a standalone page. |
| Fig. 2 (BAA Architecture) | p. 18 | Same problem — full-page, after references. Must appear in **§4.1** where the architecture is described. |
| Fig. 3 (Metamorphic Rejection) | p. 18 | Should be in **§8.2** (Page 9). Currently 9 pages away from its discussion. |
| Fig. 4 (Slot Ablation) | p. 18 | Should be in **§8.7 / §7.4** (Page 10). |
| Fig. 5 (Risk-Coverage) | p. 19 | Should be in **§9.1** (Page 10). |
| Fig. 6 (Deployment Trade-offs) | p. 19 | Should be in **§10** (Page 12). |

**All six figures are dumped after the bibliography.** This is a critical formatting failure. In CEA, figures appear **inline within the section that discusses them**, or at most on the next page. The LaTeX preamble adjusts float parameters (`\topfraction`, `\dbltopfraction`, etc.), which suggests the authors tried to fix this but the figures are still placed at the end. This likely means the figures are in a separate file or are `\clearpage`-blocked.

**Fix:** Place each `\begin{figure*}` block within its corresponding section's `.tex` file, immediately after the paragraph that first references it.

### 4.2 Tables

- **Table 2** (Positioning): Appears in §2.5 but discusses systems from §2.1–§2.4. Move to §2.1 or make it the first element of §2.
- **Table 3** (Reliability Requirements): Very wide. In two-column CEA format, this needs `\begin{table*}` (full-width). Verify it doesn't overflow.
- **Table 5** (Layer Taxonomy): 5 rows × 4 columns, but the "Evaluation Layers" column has entries like *"E02, E03, E05, E07, E08, E11, E28–E31, E38, E39"* — 10 layer tags in one cell. This is a **lookup table**, not a results table. Move to an Appendix or Supplementary Material.
- **Table 6** (Baseline Ladder): Good structure. ✓ But "Factual Authority" column has entries of varying length. Standardize.
- **Tables 7–12**: Generally well-formatted. Consistent use of Wilson CIs. ✓

### 4.3 Missing Visual Elements

- **No flowchart for the five-tier resolution ladder.** Fig. 2 shows the architecture, but a simple vertical flowchart (Tier 0 → 1 → 2 → 3 → 4 with branch arrows for CLARIFY/ABSTAIN/ESCALATE) would be far more readable.
- **No example advisory output.** A boxed example showing a certified 11-slot advisory (e.g., the potato late blight case from §1.1) with all slots labeled would make the contract tangible.

---

## V. FORMATTING AND LATEX ISSUES

### 5.1 Document Class and Packages
- `cas-dc` (Elsevier double-column) is correct for CEA. ✓
- `natbib` with `numbers,sort&compress` is correct. ✓
- **Missing:** `\usepackage{booktabs}` is loaded but I don't see consistent use of `\toprule`, `\midrule`, `\bottomrule` vs. `\hline` in the source snippets. Ensure all tables use `booktabs` rules, not `\hline`.

### 5.2 Custom Macros
```latex
\newcommand{\Nmisbind}{10{,}000}
\newcommand{\MisbindDetRate}{100.0\%}
...
```
- Good practice for consistency. ✓
- **But:** `\newcommand{\SMSHazardLLM}{64.4\%}` — the `%` must be escaped as `\%` inside `\newcommand`. Verify this compiles correctly; unescaped `%` will comment out the rest of the line.

### 5.3 Cross-References
- Multiple forward references to "Section 13" for caveats. In the compiled PDF, Section 13 is "Limitations and Threats to Validity." Ensure `\label{sec:limitations}` is correctly placed and all `\ref{sec:limitations}` resolve.
- The abstract references no sections (correct), but §1.6 Contributions references "Section 4," "Section 3," "Section 6 and Table 5" — verify all resolve.

### 5.4 Blank Spaces and Spacing
- In the PDF text extraction, there are numerous instances of **missing spaces**: *"Retrieval-Augmented Generation(RAG)"*, *"Pre-Harvest Interval(PHI)"*, *"Bounded-Authority Advisory Architecture(BAA)"*. This is likely a LaTeX issue where `\textbf{...}` or `\textit{...}` is immediately followed by `(RAG)` without a space. Check all acronym introductions for `~` or explicit space before the parenthesis.
- *"95\%Wilson CI"* → should be *"95\% Wilson CI"*.
- *"Gwet's AC1= 0.862"* → inconsistent spacing around `=`.

### 5.5 Equation Numbering
- Equations (1)–(4) are numbered. ✓
- The certification predicate (Eq. 3) is the central equation but is not highlighted or boxed. Consider `\boxed{}` or a `tcolorbox` to visually mark it.

---

## VI. LANGUAGE, GRAMMAR, AND STYLE

### 6.1 Recurring Issues

| Pattern | Example | Fix |
|---|---|---|
| Em-dash overuse | *"...at 1.26% selective risk level—across 20,112 held-out cases."* | Use a comma or split the sentence. Em-dashes appear **30+ times** in the manuscript. |
| Passive voice overuse | *"The threshold was frozen on the development split"* | *"We froze the threshold on the development split"* (active, first-person plural is standard in CEA). |
| Hedging clusters | *"We report this as a single-cluster case study, not a productivity distribution."* | This appears in §5.4, §8, §10, §13. **Four near-identical disclaimers.** State the scope once in §6 and reference it. |
| Colon + list in running text | *"The decomposition: deterministic advisory coverage (T1+T2) is 51.04%, safety/refusal handling (T0+T4) is 10.48%..."* | Use a bulleted list or a table. |
| Inconsistent terminology | "fact store" / "knowledge base" / "evidence base" / "structured fact authority" | Pick **one** term and use it throughout. I recommend "fact store" since it matches the SQLite implementation. |

### 6.2 Specific Grammatical Errors
- §1.1: *"which spray interval, and which pre-harvest interval (PHI)."* — The list has inconsistent parallel structure. Should be: *"which spray interval, and which pre-harvest interval."*
- §4.3: *"a joint exact match of 78.4%"* → *"an exact-match accuracy of 78.4%"*
- §9.5: *"Detection-gated routing collapses the candidate search space"* — "collapses" is informal. Use "reduces."
- §13: *"the escalation headline is model-confounded"* — "headline" is journalistic. Use "result."

### 6.3 Tone Calibration
The paper oscillates between **highly formal academic** (*"the certification predicate is evaluated against the authority manifest"*) and **conversational/blog-style** (*"Can it survive rural Bangladesh—2G networks, 160-character SMS, $50 phones?"*). The latter appears in §10's transition sentence. CEA is formal. Either commit to formal throughout or use the conversational hook **once** in the Introduction.

---

## VII. CITATION AND REFERENCE ASSESSMENT

- **15 references.** CEA papers in this space typically cite 30–50. The related work covers agricultural AI, RAG, and selective prediction, but is thin on:
  - **Conformal prediction** (only one mention, no citation)
  - **Knowledge graphs in agriculture** (only [8] and [9])
  - **Bengali NLP / low-resource language processing** (zero citations)
  - **Pesticide safety / toxicology informatics** (zero citations)
  - **Human-computer interaction in agricultural extension** (zero citations)

- Reference [2] *"Author, P., Author, S., 2026"* — This is clearly a **placeholder**. Must be resolved before submission.

- Reference [14] is an arXiv preprint. CEA accepts preprints, but if a published version exists, cite the published version.

---

## VIII. COMPARISON WITH RECENT TOP-TIER CEA PAPERS

| Feature | Top CEA Papers | This Manuscript |
|---|---|---|
| Abstract length | 150–220 words, structured | 297 words, unstructured |
| Introduction length | 1.5–2 pages | 2.5 pages (with 6 subsections) |
| Related Work | 1.5–2 pages, table-first | 1.5 pages, table-last |
| Number of Results sections | 1 (with subsections) | 4 separate sections |
| Figures inline | Yes, within discussion | All 6 after references |
| Limitations | 5–8 bullet points | 850 words of prose |
| Conclusion | 150–200 words | 380 words |
| Hedging / disclaimers | Minimal, in Limitations | Distributed across every section |
| Total pages | 14–18 | 19 (with figures displaced) |

---

## IX. PRIORITY RECOMMENDATIONS (Ranked)

### Must-Fix Before Resubmission

1. **Move all 6 figures inline** to their discussion sections. This is a non-negotiable formatting requirement.
2. **Restructure the abstract** to 200–250 words with Background/Methods/Results/Conclusion headings and ≤4 key numbers.
3. **Consolidate Results** from 4 sections into 2, or restructure as one section with 4 subsections.
4. **Convert the five-tier architecture description** (§4) from running prose to a numbered/description list.
5. **Fix Table 7 and Table 8** latency columns to distinguish modeled vs. measured values explicitly.
6. **Resolve Reference [2]** placeholder.
7. **Fix all missing spaces** before parenthetical acronyms throughout.

### Strongly Recommended

8. Shorten the Introduction to 2 pages; merge §1.5 (RQs) into Table 1's caption or a single paragraph.
9. Move Table 2 to the opening of §2.
10. Convert §6.2 benchmark description to a table.
11. Reduce §13 Limitations to a numbered list (≤300 words).
12. Shorten the Conclusion to ≤200 words.
13. Add a boxed worked example of a certified 11-slot advisory.
14. Standardize "fact store" terminology throughout.
15. Reduce em-dash usage by 50%; replace with commas, semicolons, or sentence splits.
16. Add 10–15 references (Bengali NLP, conformal prediction, pesticide informatics).

### Polish

17. Use `\begin{definition}` for the Design Rule in §1.4.
18. Add a flowchart figure for the resolution ladder.
19. Consolidate the four "this is a case study, not a general claim" disclaimers into one statement in §6.
20. Proofread for consistent capitalization in tables (PHI, Dosage, etc.).

---

## X. FINAL EDITORIAL NOTE

The science here is strong. The 100% rejection rate on 10,000 adversarial cases, the clean B5-vs-B6 ablation, the honest treatment of the 33% abstention cost, and the three-layer defense-in-depth framing are all compelling. The experimental design (36 layers, ~60,000 cases) is unusually thorough for this venue.

**But the writing works against the science.** The paper is simultaneously over-detailed (850-word limitations, 380-word conclusion, 297-word abstract) and under-structured (figures after references, tiers in prose, caveats scattered). It reads as though the authors are so aware of every limitation that they pre-emptively defend against every possible reviewer objection *in the body text*, which paradoxically makes the paper seem less confident.

A top CEA paper trusts its evidence, states its scope once, and lets the results speak. This manuscript needs to **trust its own numbers** and get out of their way.

**Recommendation: Major Revision.** The architecture and evidence are publishable. The writing and formatting need a full editorial pass before resubmission.

---

*Reviewed in the capacity of an editorial assessor for Computers and Electronics in Agriculture. All observations pertain to writing, structure, formatting, and presentation. Scientific novelty and experimental validity are acknowledged but not the focus of this review.*