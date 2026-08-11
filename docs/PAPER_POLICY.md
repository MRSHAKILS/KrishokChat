# PAPER POLICY — Deprecated arXiv v1; Authoritative Papers Only

**Strict rule — read before citing anything about the KrishokChat paper.**

## THE RULE (non-negotiable)

1. **The arXiv paper `arXiv:2606.29243` (v1, "KrishokChat: A Citation-Grounded Dataset
   and Benchmark for Bengali Agricultural Advisory") is DEPRECATED and its content is
   considered INVALID.** Do not cite it, quote it, link it, summarize it, or reuse any
   number, claim, or stat from it — in docs, README, frontend copy, literature reviews,
   paper drafts, poster text, demo narration, or commit messages.
2. **The authoritative papers for the KrishokChat line of work are the local files in
   `paper/done papers/`:**
   - `KrishokChat__A_Provenance_Traceable_Multi_Task_Bengali_Agricultural_Benchmark_with_Safety_Critical_Chemical_Advisory.pdf`
   - `AgriTrust.pdf`
3. If a citation is required, reference the authoritative papers **by filename/path**
   (`paper/done papers/…`). Do NOT invent a new arXiv ID, DOI, or URL for them. If a
   public identifier is needed, use a clearly marked `TODO` placeholder until the
   researcher provides one.
4. If any existing file still contains `2606.29243` or content traceable to the v1
   paper, fix it immediately: replace with the authoritative-paper reference or remove
   the claim entirely. **Do not silently reintroduce v1 information in future work.**
5. When in doubt whether a number came from v1: **do not use it.** Prefer the verified
   stats in docs/vision-pipeline/VERIFIED_STATS.md, backend/ml_assets/rag_index/eval/,
   and the research claims listed in frontend/src/lib/constants.ts (RESEARCH_STATS).

## Why this rule exists

The v1 arXiv release does not reflect the current benchmark/system. Continuing to
reference it contaminates the literature review, confuses reviewers, and undermines the
paper's acceptance. The updated papers in `paper/done papers/` are the single source of
truth for KrishokChat research claims.

## Enforcement checklist (run before any submission/commit that mentions research claims)

- [ ] `grep -ri "2606.29243" .` returns nothing
- [ ] No file references "Citation-Grounded Dataset and Benchmark" as KrishokChat's paper
- [ ] Any paper link in UI/docs points to `paper/done papers/` or a real public ID (TODO if none)
- [ ] All research stats trace to the updated papers or verified local artifacts