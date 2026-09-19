KrishokChat — Stage 3 Structural Blueprint (YAML-Locked)
EACL 2027 System Demonstrations — response to the "rebuild the paper conceptually" brief
0. Method, and six things this version corrects
I read all six files you uploaded, not just the ones that render inline: paper_results.yaml, main.pdf, and — separately, on disk — main.tex, krishokchat_eacl.bib, step_1.md, and step_2.md. The last two turned out to be earlier stages of this same pipeline: step_1.md is a forensic audit done without the YAML (it says so explicitly), and step_2.md is a feature-selection pass done afterward, in the same voice, evidently by whichever model produced the "ChatGPT" blueprint you attached. So there are really four prior passes on this paper, not two, and they already agree on most of the big calls (cut to a control-flow story, kill the fourth contribution, fix the bibliography, replace all twelve placeholder figures). I don't re-argue that agreement below — I flag it and move on.

I treated paper_results.yaml as binding, per its own header ("every number here traces to a frozen results.json"), and checked every structural recommendation against it, against the actual \citep/\cite graph in main.tex, and against both attached blueprints. That surfaced six corrections that neither attached blueprint made — the "ChatGPT" one because it doesn't cite the YAML's paper_map/contributions block explicitly even though its numbers match it, and the "Qwen" one because it says outright that it never received the YAML:

Three contributions, with the exact taglines, not an invented "modest three-part statement." The YAML names them C1_halt_before_retrieval, C2_fence_and_badge, C3_two_walls_mouthpiece_four_renderings, gives each a verbatim tagline, and maps each to specific demo scenarios. These map almost one-to-one onto the current manuscript's contributions 1, 3, and 4 — contribution 2 (PRISM-RAG) is exactly the one the ground truth drops. Section A uses these directly.
Table 1 is a claim-honesty table, not a competitor feature matrix. paper_map.figures lists exactly [Fig1 five-stage pipeline, Fig2 workspace-plus-Why screenshots, Tab1 honesty table, Tab2 results]. Both attached blueprints assumed Table 1 = the Farmer.Chat/KrishokBondhu/Krishi Sathi/CoPilot comparison currently in §5. The ground truth wants something else there, and it's a better fit for a paper whose whole personality is "here is exactly what we can and cannot claim" (see Section D).
An exact page budget, not an invented one. paper_map gives abstract_intro 0.8 / system 1.0 / demo_scenarios 1.2 / evaluation 1.6 / related_work 0.6 / limitations 0.4 — that's 5.6 pages, leaving 0.4 for availability + conclusion. Limitations is its own budget line, separate from availability/conclusion; both attached blueprints folded the three together (see Section C).
Exactly five demo scenarios (S1–S5), not six. demo_scenarios lists S1: halt-chips-resume, S2: photo-fence-to-card, S3: mismatch-badge, S4: refuse-plus-16123, S5: sms-offline. The current manuscript's §3.6 lists six, and the sixth — "evidence-conflict request," driven by the ConceptNormalizer and Evidence Agreement Gate — has no counterpart anywhere in the YAML. That is also, I think, why Screenshot numbering in the current draft jumps from Screenshot 5 straight to Screenshot 7 (main.tex lines 243–247): a "Screenshot 6" for that sixth scenario was never going to get made, because that scenario isn't in scope. The fix isn't to draw the missing screenshot; it's to cut the scenario.
PRISM-RAG, the ConceptNormalizer, the Evidence Agreement Gate, DialectSelector, "typed session working memory," and "5-level answerability-aware routing" appear nowhere in the ground-truth YAML — not as low-status entries, but by name, at all. N09_conformance (clarification 0.86 / overall 0.458 — the number currently used to defend PRISM) is filed as evidence for C1_halt_before_retrieval, i.e., for the gate/clarify contribution, not for a routing contribution. Both attached blueprints treat these five names as under-evidenced components to demote to the appendix. I'd go one step further: the ground truth doesn't recognize them as named things at all, which means the rewrite should describe the mechanisms (a routing step, a diagnosis-disagreement check) without necessarily keeping the branded names, rather than demoting the names while keeping them.
Two fixes that need no new evidence, only wiring, which I confirmed directly against main.tex and the .bib:
bari_handbook2023 and brri_handbook2024 are already defined in krishokchat_eacl.bib but are never \cited anywhere in main.tex (grep count: 0 each), even though the text repeatedly invokes "BARI/BRRI fact lookup" and "BRRI manual" as the knowledge source (e.g. the provenance-badge sentence in §2.3, Screenshot 2's caption). This is a same-afternoon fix: add the two \citeps where the knowledge base is first named.
sus1996 (Brooke's SUS scale) is also in the .bib with zero citations. That's consistent with — and probably why — the kill list bans "SUS scores": some earlier draft cited it to dress up a proxy usability number, the number was retired, and the citation was never removed. Delete it, or keep it only if you explicitly want a sentence contrasting your proxy score with a real SUS instrument you didn't run.
Everything else below is either consistent with, or an explicit refinement of, what step_1.md, step_2.md, and the two attached blueprints already established.

A. Final recommended paper storyline
Anchor sentence (built by generalizing C3's own tagline, which is the most quotable of the three, across the whole system):

KrishokChat is a Bengali agricultural advisory system built on one rule: at every point where a wrong answer would be dangerous, the system either has evidence for what it's about to say, or it says nothing — and the farmer can see which one just happened.

The three contributions are the spine. Use the YAML's own taglines as section-opening thesis sentences (they're already good prose; don't paraphrase them into something blander):

Tagline (verbatim)	Mechanism	Demo	Headline evidence
C1 Halt before retrieval	"The cheapest and safest retrieval is the one the system refuses to run."	Deterministic extractor finds crop empty on treatment intent → clarify (zero retrieval) / non-chemical guidance card / refuse+16123	S1: halt→chips→resume, sources_retrieved=0	76/200 halted, 0.38 [N01b_farmer_200]; pilot 100/100 + 140/140 [E09_pilot, PILOT]; conformance 0.86/0.458 [N09_conformance]
C2 Fence and badge	"The photo is a fence around the evidence — when words jump the fence, the system says so."	Tri-state gated crop router → per-crop disease models → crop pre-binds the advisory query; text-vs-image mismatch → badge + confirm before chemical advice	S2 photo-fence-to-card, S3 mismatch-badge	0.3625→0.30, 25/0 discordant, p=5.96×10⁻⁸ [N08_fence, gold-routing]; badge 453/454 [N07_badge]
C3 Two walls, one mouthpiece, four renderings	"The LLM is the mouthpiece; the evidence is the witness; the verifier is the judge — and the farmer sees all three."	Upstream gate → untrusted generator → dosage-claim verifier (same-passage binding, annotate-and-drop, ~5 ms) → authorship badges → rendered as answer / SMS / offline / 16123	S4 refuse-plus-16123, S5 sms-offline, + Why/trace panel	guarded 0.95% vs unguarded 36.19% ASR [E03_N12_safety]; verifier 114/118 detected, 0/38 FP [N03_verifier]
This table is essentially the paper's outline. Introduction states it in prose; System explains the three mechanisms; Demonstration shows S1→S5 in that order; Evaluation proves each with Tab2; Related Work explains why FC/KB/KS/MC don't already do this combination. Nothing else needs an independent narrative thread.

What this story is not — the YAML's kill_list, operationalized against what I actually found in main.tex:

Kill-list item	Current status in main.tex
First-Bengali-RAG / first-multimodal / first-voice	Already absent. Keep it that way.
11-slot live certification	Not present here (belongs to the companion CEA benchmark paper). Do not import it.
SUS scores, guaranteed SMS dose survival, measured network retention	SUS absent from the manuscript (only the dead sus1996 citation remains, see §0.6); SMS dose loss is already reported honestly as 0/84; network loss is already labeled simulated. Compliant already — just delete the orphan citation.
INT8-for-all, INT8 speedup, voice/ASR claims	INT8 is already correctly hedged as size-only, never speed. The voice-transcription toggle, however, still appears in Figure 2's caption with zero supporting evidence anywhere — remove it, don't just hedge it.
$2.30/92pct, 38.5pct baseline, 88pct tokens, E08 100pct, pooled purity 0.6924	Already absent from main.tex (I grepped for all of these; zero hits). These are retired numbers from an earlier draft — good, nothing to undo.
"Proven-equivalent" for p=1.0	Appendix A.2 already gets this right ("no observed difference... rather than mathematical equivalence"). Just don't let a compressed main-text sentence lose that nuance.
So the kill list is largely already enforced in the LaTeX — the remaining work is citation hygiene (sus1996), one caption (voice toggle), and not re-introducing any of this when compressing.

B. Final section/subsection structure
Title + Abstract                              (hook numbers only, ends with access line)

§1  Introduction                              (no subsections; ends with the C1/C2/C3 statement)

§2  Related Work and Positioning              (no subsections; one compact 4-row comparison,
                                               not a numbered floating table — see Section D)

§3  System Design                             §3.1 Pipeline overview (→ Fig. 1)
                                               §3.2 C1 — halting before retrieval
                                               §3.3 C2 — crop fence and the mismatch badge
                                               §3.4 C3 — untrusted generation, verification, delivery

§4  Demonstration                             one continuous farmer session, S1→S2→S3→S4→S5,
                                               anchored by Fig. 2 (→ Tab1 introduced here or at
                                               the head of §5, see Section D)

§5  Evaluation                                three short paragraphs (C1, C2, C3) + Table 2
                                               + one closing "what this does not show" paragraph

§6  Availability, Limitations, Conclusion     Availability (2–3 lines) / Limitations (curated
                                               subset of the 18-row ledger) / Conclusion (2–3
                                               sentences)

Ethics and Broader Impact Statement           (after p.6, unlimited — CFP-confirmed)
References                                    (unlimited)

Appendix A  Extended architecture (PRISM/router internals, mechanism names, conformance detail)
Appendix B  Vision models, INT8, browser/WASM latency
Appendix C  Gate/extractor detail, equivalence arm, live-vs-deterministic comparison
Appendix D  Verifier per-mutation detail, safety envelope, off-topic audit
Appendix E  Delivery, offline, footprint, cost, trace-ordering detail
Appendix F  Additional UI-state screenshots (ask/confirm/refer states not in Fig. 2), failure ledger
Appendix G  Full 18-row limitations ledger (verbatim from LIMITATIONS.md) + claim-status table
This keeps the same six main sections both attached blueprints proposed — I'm not disputing the shape, only the contents of §2's table, §3's internal split (now explicitly C1/C2/C3-keyed), §4's scenario count (five, not six), and §5's organization (by contribution, so it echoes §1 and §3 instead of re-deriving its own categories).

C. Approximate six-page allocation
This is the YAML's own budget, not an estimate:

Section	Budget (paper_map)	Contains
Abstract + Introduction	0.8 pp	C1/C2/C3, hook numbers: 38% halt, 0.95% vs 36.19%, 25/0 fence
System	1.0 pp	T0–T4 pipeline, badges, verifier, router, vision pipeline
Demonstration	1.2 pp	S1, S2, S3, S4, S5
Evaluation	1.6 pp	Table 2, "ground-truth key rows"
Related Work	0.6 pp	4-row comparison vs Farmer.Chat / KrishokBondhu / Krishi Sathi / My Climate CoPilot
Limitations	0.4 pp	Curated subset of the 18-row LIMITATIONS.md ledger
Subtotal	5.6 pp	
Availability + Conclusion	0.4 pp (remainder)	Everything else has to fit here
The 0.4 pp tail is the tight part, tighter than either attached blueprint assumed (ChatGPT gave Availability/Limitations/Conclusion 0.45 pp combined; Qwen gave it 0.65 pp combined — neither anticipated Limitations getting its own separate 0.4 pp line, which leaves less than either estimate for what's left over). Two things make this workable:

Do not save all access information for §6. Put the demo URL, video URL, and license in the last sentence of the Introduction (inside the 0.8 pp block, which has room), the same way both attached blueprints already recommended — this is now a budget necessity, not just good practice, given how little room §6 has.
LIMITATIONS.md's 18 rows almost certainly can't run verbatim in 0.4 main-text pages (≈180–200 words) unless they're extremely short. Read limitations_0_4pp: LIMITATIONS.md 18 rows verbatim as: the appendix reproduces all 18 rows verbatim (unlimited space, Appendix G), and the main text prints a curated 6–8 row subset in the same compact two-column format (Limitation | Scope), with a one-line pointer to the full ledger. You'll need to supply LIMITATIONS.md before drafting — it isn't among the six files I have, and I don't want to invent its 18 rows.
D. Figure/screenshot plan
Two figures, two tables — matching paper_map.figures exactly, and noticeably leaner than either attached blueprint's plan.

Figure 1 — Five-stage pipeline (paper_map: "five-stage pipeline")
T0 → T1 → T2 → T3 → T4, with four colored exits (ASK at T1, CONFIRM at T2, DROP at T4, REFER at T0), the crop fence marked at T2, the provenance badge marked at output, and the four delivery channels at the far right. Replaces the current §2.1–§2.4 walkthrough prose. Must be a real vector diagram — the current \placeholderbox is a text table in a box, not a figure.

Figure 2 — "Workspace + Why" (paper_map: "workspace-plus-Why screenshots")
This is a narrower brief than either attached blueprint's four-panel ASK/CONFIRM/DROP/REFER storyboard. The plural "screenshots" plus the explicit callout of a Why panel in C3's demo line ("Why/trace panel") points to one flagship interaction, shown as two linked views:

(a) Workspace view: a grounded Bengali answer with sentence-level citations and the provenance badge visible.
(b) Why-panel view (expanded): the same answer with its decision trace open, showing one dosage claim visibly dropped with the audit line — this is the DROP outcome and the one place the paper actually shows its own honesty mechanism working live.
The ASK (halt/chips), CONFIRM (mismatch badge), and REFER (16123) states are described in §4's prose against small inline thumbnails, or moved to Appendix F's fuller screenshot set — they do not need their own main-text figure once Figure 2 is doing this specific job. This is a deliberate narrowing from both attached blueprints, which each spent the whole of Figure 2 on a 2×2 grid of all four outcomes.

Table 1 — Claim-honesty table (paper_map: "Tab1 honesty table")
This is the correction that most changes the paper's personality. Instead of a feature-comparison grid, Table 1 is a compact (6–8 row) version of the current Appendix Table 7 ("Scope of Claims and Evaluation Status"), one row per headline claim, using the YAML's own status vocabulary directly:

Claim	Status	What it shows	What it doesn't
Gate halts 38% of treatment queries	REAL_MEASURED	Operating point on 200 farmer queries	Not an ambiguity-prevalence estimate; single-reviewer labels
Fence: 36.25%→30.0% wrong-crop advice	REAL_MEASURED (simulation)	Fence reduces wrong-crop advice	Gold-routing upper bound, not end-to-end
Mismatch badge: 453/454	REAL_MEASURED	Explicit contradictions caught	Implicit conflicts untested
Guarded ASR 0.95% vs 36.19%	REAL_MEASURED	Guard sharply cuts attack success	Bangla-native residual 10/100 remains
Dosage verifier 114/118, 0/38 FP	REAL_MEASURED_SMALLN	Mutations detected reliably	Small-n, not a general factuality score
Pilot 100/100 + 140/140	PILOT	Conformance check only	Constructed set, not the headline estimate
Placing this early — I'd put it at the very end of the Introduction or as the opening artifact of §5 — tells the reviewer up front how to read every number that follows, which is a stronger and more distinctive move for a paper whose actual argument is "we made failure visible" than a 13-row competitor grid that mostly checks boxes only KrishokChat has. Recommendation: open §5 Evaluation with it, so it functions as a legend for Table 2 immediately below.

Table 2 — Evidence summary (paper_map: "Tab2 results")
One row per contribution's headline evidence (this is largely what both attached blueprints already designed, and I don't materially change it): gate, fence, badge, safety guard, verifier, SMS/offline, each with Measure / Result / n / Condition, using the exact paper_results.yaml numbers.

The Related-Work comparison is not a third floating table
paper_map.figures lists exactly two tables. The related_work_0_6pp: 4-row matrix (Farmer.Chat / KrishokBondhu / Krishi Sathi / CoPilot) entry is separate from that list, which reads to me as: render it as a compact, unlabeled 4-row inline comparison (or even four contrastive sentences) rather than a numbered Table 3. Four rows, matching the four control outcomes: pre-answer stopping / crop-multimodal evidence constraint / pre-render dosage verification / terminal human referral, columns Ours/FC/KB/KS/MC. This also solves the current Table 1's worst problem — a 13-row grid where nearly every row is checked for KrishokChat alone reads as "novelty by exhaustive checklist," which is exactly the pattern step_1.md's audit flagged ("Novelty argued by measurement gaps").

E. Main-paper content inventory
The problem (crop loss / wasted spend / chemical misuse from a wrong recommendation), stated through the extension-agent ratio, one verified statistic only.
The specific unmet need: existing systems retrieve-and-generate fluently but don't expose what they don't know.
The three contributions (C1/C2/C3), each with its tagline, its one-line mechanism, and its demo mapping.
Figure 1 (architecture) and Figure 2 (workspace+Why).
One continuous S1→S5 demonstration.
Table 1 (honesty) and Table 2 (results), plus the 4-row related-work comparison.
Availability line (URL/video/license) inside the Introduction's last sentence, repeated compactly in §6.
A curated 6–8 row Limitations subset, pointing to the full 18-row ledger.
A 2–3 sentence conclusion that does not restate the results.
F. Appendix content inventory
Appendix	Content	Why the main paper stands without it
A. Extended architecture	Router/routing internals, whatever internal names you keep for the diagnosis-disagreement check and the concept-normalization step, per-route conformance (0.458 overall, 16/168 document-RAG, etc.)	These names are absent from the ground-truth YAML entirely (§0.5); the main paper only needs to say a routing step exists
B. Vision models & efficiency	Per-crop top-1 (0.90/0.9625/0.9413/0.9118), ONNX parity, family router 433/437, INT8 (wheat reportable, rice rejected at 2.5pp), browser WASM latencies	Implementation detail behind the one claim the main text needs: crop identity from vision is reliable enough to fence retrieval
C. Gate/extractor detail	Extractor agreement 0.52 / miss 0.475 / FP 0.005, hazard 0.1607 [8.69,27.81], firewall case farmer_q_593, equivalence arm (0.30 vs 0.30, p=1.0, no-observed-difference), live-vs-deterministic (0.10 vs 0.38, 4218.6 ms)	Supports gate honesty; the main text needs only the headline 76/200 and the single-reviewer caveat
D. Verifier & safety detail	Per-mutation table (33/33, 30/31, 22/25, 29/29), 4 autopsied misses, Bangla-native breakdown (embedded 4/10, roleplay 2/10), routing probe (n=3000, certify recall 0.7165), off-topic audit (10/10 / 0/30)	Main text needs the aggregate 114/118 and the 0.95%-vs-36.19% headline only
E. Delivery & deployment	SMS detail (299/300, 100/100, 16/16, dose 0/84), offline (BM25 0.94, simulated loss), footprint (95.64/284.0/339.6 MB), latency table, tier mix (7.8% zero-LLM), modeled cost	One sentence each suffices in §3.4
F. Additional screenshots	Ask-state, mismatch-badge-state, referral-state, delivery-state screens not covered by Fig. 2; the implicit-crop miss (farmer_q_63) and firewall case as a failure gallery	Fig. 2 covers the one interaction the paper stakes its identity on; this is the rest of the tour
G. Full limitations ledger + claim-status table	All 18 LIMITATIONS.md rows verbatim; the full version of Table 1 (all statuses, not just the 6–8 headline rows)	Reviewers who want to audit every claim's boundary get the complete ledger without it displacing the main narrative
G. Removed-content inventory
Beyond the kill-list items already tracked in Section A, cut structurally:

Item	Why
Contribution 2 ("We introduce PRISM-RAG...")	Has no counterpart in C1/C2/C3; its evidence (N09_conformance) already belongs to C1
"5-level answerability-aware routing," "typed session working memory" as novelty language (main.tex line 370, Related Work)	Absent from the SSOT by name (§0.5); undescribed; no independent evaluation
§3.6's six-scenario restatement list	Restates §3.1–§3.5; also the source of the phantom sixth scenario (§0.4)
Token comparison (89 vs. 2,146) framed as a saving	Different execution paths, not comparable; retired per kill list
Modeled cost ($0.1798/1k, 7.79% saving) as a headline benefit	Modeled, not measured; belongs in Appendix E as one honest line, not the main text
"LLM is not the default path"	92.2% of turns reach T3; contradicted by the system's own tier mix
Farmer/GDP statistics beyond the one extension-agent-ratio figure; dense-retrieval-vs-BM25 numbers; FrugalGPT/RouteLLM discussion; IndicGLUE/BhasaBodh citations	Background padding not needed to establish the demo's contribution
Voice-input toggle (Figure 2 caption only)	Zero evidence anywhere in the YAML or the manuscript body; not a hedge candidate, a removal candidate
sus1996 bib entry	Orphaned (0 citations); consistent with the SUS ban on the kill list
The current 13-row Table 1	Replaced by the honesty table (Table 1, new) + a 4-row comparison (Section D)
H. Introduction argument flow
Four moves, ending with the C1/C2/C3 statement and the access line, inside the 0.8 pp budget:

The problem (~2–3 sentences): a farmer needs a treatment decision before the next day; the extension-agent ratio makes that hard at scale; a wrong crop/chemical/dose recommendation is not a minor error.
Why fluent retrieve-and-generate isn't enough (~2–3 sentences): the failure is often before generation — an unspecified crop, a contradicting photo, an unsupported dosage claim — and a fluent system can turn any of these into a confident wrong answer rather than a visible boundary. One sentence on the colloquial-Bengali retrieval gap, citing the authors' own prior study, is enough; the actual 0.093/0.970/0.539 numbers belong in that other paper, not repeated here.
What we built, stated through the three taglines and their one-line mechanisms (the table in Section A, compressed to prose).
Access, in the final sentence: demo URL, video URL, license.
Must not appear: a generic "AI has revolutionized..." opener; four contributions; "We introduce PRISM-RAG"; more than one or two headline evaluation numbers (save the rest for the honesty table and Table 2); a standalone deployment-constraints paragraph.

I. Related-work argument flow
Two short paragraphs plus the 4-row comparison, inside 0.6 pp:

Conversational agricultural advisory (Farmer.Chat, KrishokBondhu, Krishi Sathi): what they establish (localized digital advisory works), what none of them measures (a pre-retrieval halt rate, a crop-fencing effect, an explicit text–image contradiction state).
Safety and evidence-grounding (My Climate CoPilot's post-hoc self-evaluation vs. KrishokChat's pre-render verifier; the authors' own prior safety paper's residual-hallucination finding as the motivating gap; one sentence on multimodal text-bias, citing Deng et al., CVPR 2025, "Words or Vision: Do Vision-Language Models Have Blind Faith in Text?" — I verified this exists and is the correct replacement for the current unverifiable "Agrawal et al., 2024" entry, which I could not locate anywhere).
Positioning sentence + 4-row comparison: the contribution is the combination (pre-answer stopping + crop-conditioned evidence + pre-render verification + terminal referral), not any one mechanism in isolation.
Citation fixes needed before drafting (step_1.md's audit already did most of this verification in detail; I independently confirmed the two most load-bearing ones — Farmer.Chat's real author list, and the Deng et al. replacement — via direct search; the rest below is step_1.md's finding, which I'd trust but re-check once during drafting):

Manuscript currently says	Correction
Farmer.Chat: Mishra, Verma, Gupta, Seth, CSCW 2024	Confirmed: Namita Singh, Jacqueline Wang'ombe, et al. (Digital Green + Microsoft Research), arXiv:2409.08916
"Agrawal, Batra, Parikh, CVPR 2024"	Confirmed real replacement: Ailin Deng, Tri Cao, Zhirui Chen, Bryan Hooi, "Words or Vision...", CVPR 2025, pp. 3867–3876
KrishokBondhu: Ahmed, Kabir, Rahman, EMNLP 2025	Per step_1.md: real authors are Ameen, Islam, Aktar, Rafat — venue is IEEE WIECON-ECE 2025 or QPAIN 2026; your own arXiv paper already cites the corrected version. Re-verify venue before drafting.
Krishi Sathi: Sharma, Patel, Kumar, arXiv:2508.03719	Per step_1.md: that arXiv ID belongs to Vijayvargia et al., "Intent Aware Context Retrieval..."; find the actual Krishi Sathi paper or drop the citation
My Climate CoPilot: Wadhwa et al., pp. 112–122	Per step_1.md: Nguyen, Hallgren, Harkin, Prakash, Karimi, ACL 2025 System Demonstrations, pp. 62–70
Reza et al. 2026b, third author "Arshad Shahid"	Per step_1.md: your own arXiv 2608.14886 lists "Omar-Ibne Shahid." Reconcile which is correct.
—	New: wire in \citep{bari_handbook2023,brri_handbook2024} wherever "BARI/BRRI" is first named (§0.6)
—	New: drop the unused sus1996 entry, or keep it only for an explicit "not a validated SUS instrument" contrast
J. System-description argument flow
Structured explicitly around C1/C2/C3 rather than a generic T0–T4 walkthrough, inside 1.0 pp:

3.1 Pipeline overview (~1 paragraph): the five stages, one sentence each, the "each stage narrows what the next may do" principle, pointer to Fig. 1. Name the generator LLM and its hosting here — this is currently missing from the entire manuscript and is a CFP-relevant gap (step_1.md, step_2.md both flag it; the YAML doesn't resolve it either, so it needs to come from you before drafting).
3.2 C1: T0/T1, the three bounded outcomes, one sentence of evidence (76/200).
3.3 C2: crop identity from text or vision, the fence, the mismatch badge, one sentence of evidence (0.3625→0.30, gold-routing labeled explicitly).
3.4 C3: the verifier's mechanism (same-passage binding, dose-band check, annotate-and-drop), the provenance badge, one sentence per delivery channel, and the one honest sentence both prior audits insist on: 92.2% of turns still reach generation; the control outcomes cover the rest plus the safety-critical filtering inside T3/T4 — this pre-empts the "LLM not default" objection instead of asserting something the tier mix contradicts.
Must not appear: router/mechanism internal names beyond at most one, kept for orientation, not evaluated; INT8/WASM/footprint/latency/cost numbers; token medians.

K. Demonstration argument flow
One continuous session, S1→S5 in order, inside 1.2 pp (~500 words, ~90–100 words per beat):

S1: colloquial Bengali treatment query, no crop → halt, zero retrieval, chips → farmer picks a crop, retrieval resumes.
S2: a leaf photo is uploaded; on-device ONNX predicts the crop; evidence is bounded to that crop's manual.
S3: the photo's crop and the text's crop disagree → mismatch badge, chemical advice held until confirmed.
S4 (can be reordered to come after S5, or interleaved as the "meanwhile, a different kind of request" beat): a banned-chemical or crisis query → deterministic guard, terminal 16123 referral.
S5: the confirmed, grounded answer is exported as SMS (dose does not survive — say so) or an offline card.
Figure 2's Why-panel view belongs at the natural point in this narration where a dosage claim gets dropped — likely folded into the S2→S3 resolution once the crop is confirmed and an answer is generated, rather than as a separate sixth beat.

One sentence, no more, for the cut sixth scenario if you want to keep any trace of it: "When retrieved evidence disagrees on the diagnosis, the system asks a discriminative clarification question rather than blending competing treatments" — mechanism-level, not a numbered demo beat, no screenshot.

L. Evaluation argument flow
Organized by contribution (echoing §1 and §3), inside 1.6 pp, opening with Table 1 as the legend:

C1 paragraph: 76/200 halted (0.38); pilot 100/100+140/140 as a conformance check, not the headline; single-reviewer-label caveat stated once, plainly.
C2 paragraph: 0.3625→0.30 under gold routing, 25/0 discordant, p=5.96×10⁻⁸ — labeled an upper-bound simulation in the same sentence as the number, not two sentences later; badge 453/454 explicit contradictions, one miss (implicit reference); bring in the cross-track baselines (E08_divergence: 68/80 at 0.85) with the caveat that this is a prompted-judge divergence measure, not the badge-detection rate itself.
C3 paragraph: guarded 0.95% vs unguarded 36.19% ASR, with the Bangla-native residual (10/100) stated in the same breath, not omitted; verifier 114/118, 0/38 FP, small-n flagged; one line each on SMS (399/400 within limit, dose 0/84) and offline (BM25 hit 0.94, loss simulated).
Closing paragraph — what this does not establish: no farmer user study; no end-to-end (non-gold-routed) fence measurement; no general factuality claim beyond dosage-claim sentences; no field-measured network behavior.
M. Final checklist before rewriting
Blocking / desk-reject (per the current, confirmed EACL 2027 CFP)
 Deadline is 22 Sept 2026, 23:59 AoE — three days out from today. If a live demo and a ≤2.5-minute screencast cannot exist by Sunday, that's the real constraint on everything else in this document.
 Live demo URL or installable package, in the PDF and the OpenReview form.
 Screencast ≤2.5 minutes, narrated, linked in both places.
 License stated (code, knowledge base, model).
 Reciprocal reviewer nominated in the form.
 Page count ≤6 for the main body (current draft is ≈11.5).
 All 12 \placeholderbox figures replaced with real diagrams/screenshots; the Screenshot-6 gap resolved by cutting the sixth scenario (§0.4), not by drawing a sixth screenshot.
Missing inputs (need from you before drafting)
 LIMITATIONS.md — referenced by the YAML (limitations_0_4pp: LIMITATIONS.md 18 rows verbatim) but not among the six files supplied. Section C's plan (curated subset in-text, full 18 rows in Appendix G) depends on having it.
 Generator LLM identity, hosting, and data-handling terms — absent from the manuscript entirely.
 Knowledge-base description beyond "BARI/BRRI" (size, license, whether it's the benchmark-paper release) — the citations exist unused (§0.6); the descriptive text around them doesn't yet.
 Dose-band source and coverage (which crops, which chemicals).
 Confirmation that 16123 is the current national helpline and that routing farmers to it is authorized.
 Farmer-query provenance and consent basis for the 200 queries (needed for the Ethics statement).
Number reconciliation (already diagnosed in detail by step_1.md; apply, don't re-derive)
 420 total live calls = 210 guarded + 210 unguarded per arm — say so explicitly wherever "420" appears.
 Bangla-native 10/100 vs. the ≈2/210 implied by the overall guarded CI — report both, reconciled.
 Fence baseline (0.3625→0.30) vs. the equivalence arm (0.30 vs 0.30, p=1.0) — these are different experiments; say which is which every time either is mentioned.
 "8–33 cases per mutation type" (Limitations) vs. "25–33" (Appendix D) — use one number.
 Consistent CI formatting; never pair a fraction with a percent-style interval in the same clause.
 One tier vocabulary throughout: T0–T4 pipeline stages. Retire "Tier-0..3 execution tiers," "5-tier provenance," and "5-level routing" as separate, colliding terms.
Claims to soften (already identified by both attached blueprints; confirmed against main.tex line numbers here)
 Abstract, line 42: "76/200 ambiguous farmer queries" → "76/200 halted"; add "gold-routing simulation" to the fence sentence; "dangerous advice" → "attack success rate"; mention the Bangla-native residual.
 Line 67: "Our contributions are fourfold" → threefold, using C1/C2/C3.
 Line 70: delete the PRISM-RAG contribution bullet; fold N09_conformance into the C1 evidence discussion instead.
 Line 370 (Related Work): delete "typed session working memory... 5-level answerability-aware routing" as novelty language.
Presentation
 No \placeholderbox remains anywhere.
 Table 1 rebuilt as the honesty table; the old 13-row comparison becomes a 4-row inline comparison in Related Work (Section D).
 Figure 2 rebuilt as the workspace+Why pairing, not a 4-panel outcome grid.
 No "novel" / "first" / "We introduce" language for components absent from the SSOT (§0.5).
 Ethics statement present after page 6, covering farmer-query consent, image-data handling (on-device, no transmission), LLM provider data handling, pesticide dual-use, and the single-reviewer-label limitation.
Bottom line. The paper the ground truth actually wants is narrower than either attached blueprint drew it, in a specific, checkable way: three contributions with their own taglines, five demo scenarios, two figures, two tables (one of them a first-of-its-kind honesty table rather than a competitor grid), and a page budget that has already been decided down to the tenth of a page. The remaining work before drafting is not more editorial judgment — it's LIMITATIONS.md, the generator-LLM facts, the final citation-verification pass, and the demo/video, all of which are yours to supply, not mine to infer.