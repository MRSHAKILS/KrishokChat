# Gate-0 Freeze — N01 Blind Arm + N02 Metering (2026-09-17)

**Rule:** nothing below changes after the run starts. Any change = new freeze version + re-run.

## Frozen query sets
- **N01 paired:** PRISM B_colloquial (100) + C_dialect (100) + D_banglish (100) + I_ambiguous_disease (100) = **400 rows**, all with `true_crop` (verified 2026-09-17: 7 crops — rice/potato/tomato/brinjal/chilli/wheat/maize).
  Source: `research_artifacts/datasets/prism_benchmark/prism_benchmark_1000.jsonl` (sha256 recorded at run time).
- **F descriptive:** PRISM F_underspecified (100, no true_crop) — blind top-5 distinct-crop spread only, no rate.
- **N02 strings:** real outputs of the N01 run (clarification texts, retrieved contexts, stub answers) + live-generation tokens from provider usage on G5/SMS-live subsets when they run.

## Frozen hazard definition (v2 — amended pre-run after source inspection)
- **Source→crop map** (`crop_map_v1`, committed with runner): system canonical aliases (`QueryExtractor._CROP_ALIASES` + romanized table, longest-first) matched against `title_en/title_bn + section_title + source_document + tags + content_en/bn` of each `RetrievedSource`.
  - Amendment rationale (practical sense): the corpus nodes carry no crop field; title-only mapping (E49's weakness) under-maps. Content-inclusive mapping can only OVER-attribute crops, and the multi-crop rule counts over-attributed sources as safe — i.e., any mapping error favors the BLIND arm. Conservative direction documented.
  - exactly 1 crop → single-crop source; ≥2 → multi-crop (safe for any contained gold); 0 → unknown (excluded, counted + reported as mapping coverage).
- **Hazard (per query):** ≥1 KNOWN single/multi-crop source in blind top-5 whose crop set excludes the gold crop.
- **Decomposition (reported):** halt_rate (no retrieval) · conditional hazard | retrieved · overall hazard = P(retrieved) × P(cross|retrieved). Blind arm always retrieves.
- **Depth:** top-5. **Retriever:** BM25 `candidates(query, depth=10)` truncated to 5, frozen `bm25_index.pkl` (hash recorded).

## Frozen tokenizer
- tiktoken 0.14.0 `cl100k_base` on real strings, both sides. Disclosed: cl100k ≠ Gemini tokenizer; live-API sides additionally report provider-exact usage. Metric: p50/p95 + modeled-vs-metered table.

## Frozen corpus/index (v3 — corrected after source inspection)
- **Live retrieval units = 2,135 knowledge nodes embedded in `bm25_index.pkl`** (dict keys: bm25/BM25Okapi + nodes + corpus + ids; verified 2026-09-17). `corpus_path` args are dead config when the pickle embeds nodes.
- `bm25_index.pkl` sha256: `2ab484aca38b694937a92a4a27bb2779c9e2ffb89f397d3fa168f7ca19e836c5` (matches E01/E06 provenance — same artifact).
- `chunks_corpus.jsonl` = 4,815 rows = R13 fallback-channel material, NOT in the harness path (`chunk_fallback=None`). Excluded from N01.
- Node fields available for mapping: id, category, title_bn/en, content_bn/en, summary, tags, source_document, publisher, section_title, citation.

## Frozen blind-arm recipe (v3 — pipeline-identical minus gate)
Per query (no session), using the same imported functions as `qa_pipeline.py`:
1. `context = QueryContext(crop=None, disease=None, history=(), farmer_context=None)`; `working_memory = AgriculturalWorkingMemory.from_dict(None)`.
2. `info_state = QueryExtractor.extract(query)`; `concept_res = ConceptNormalizer.normalize(query, crop=effective_crop)`; merge into working memory (same fields as pipeline L195-207); promote crop to context if found.
3. `decision = await DeterministicSafety().classify(query, context)` (harness safety: precheck rules + keyword_intent, 0 LLM — offline scope disclosed). Terminal → record terminal, exclude from hazard, count separately.
4. `routing = AdaptiveRetrievalRouter.route(query, working_memory)`; `base = primary_query if route in (C, D) else query`.
5. `retrieval_query = build_retrieval_query(base, context, decision.category.value)` (BNGLISH_TERMS bridge included — this is what makes BM25 hit).
6. `retrieved = BM25Retriever.retrieve(retrieval_query, top_k=5)` (thresholded, same call the pipeline makes).
The ONLY difference vs the gated arm is the skipped halt. Stored per query: retrieval_query string + source ids for audit.

## Outputs
- Raw: `experiments/results/n01_blind_arm_<date>.json`, `experiments/results/n02_metering_<date>.json` (fsync per record).
- Promotion: verified copies → `N01_blind_arm/results.json`, `N02_token_metering/results.json` + `ground_truth.yaml` update + team 50+50 review sample export.

## Method notes (critic fixes, locked 2026-09-17)- Paired arms use thresholded `BM25Retriever.retrieve(top_k=5)`; the F-row descriptive spread uses unthresholded `candidates(depth=10)[:5]` — different functions, F stays descriptive only.
- p=1.0 with zero discordants = no observed difference, NOT equivalence. Report CIs + discordant counts; never "proven equivalent."
- 76 halted rows are UNSCORED for hazard (non-mapped golds); the 56-row table is gate-silent. Never write "gated hazard 0" — halted rows contribute zero sources and are unscored. (v2: 76/38.0%, tie 16.07%.)
- Gate-efficacy reading of N01a is banned: the set cannot test the gate (all rows carry crops). N01a = construction-fidelity check only.

## v6 entry — matcher fix v2 + full re-runs (2026-09-17, critic-ordered)- Code: token-start matching + leading-punct strip + লঙ্কা/লংকা chilli synonyms (`intent.py` modified-tracked, `query_extractor.py` untracked — full copy + diff in `experiments/results/matcher_fix_v2.*`); file hashes recorded in regen log.
- Regression test: `backend/tests/test_crop_matcher_boundary.py` (4 tests); full suite green at fix time.
- Re-runs (deterministic): N01a identical (30.0/30.0); N01b v2 (halt 76, hazard tie 16.07%, 0 discordants); N02 tiers identical. Pre-fix outputs archived as `_PREFIX`, v1 as `_v1`.
- Sheet v2: `extractor_crop_postfix` regenerated (agreement 0.52, FP 0.005, miss 0.475); labels untouched.
- Residuals: dict-order first-pick on multi-crop (734 asterisk); startswith place-name risk; both disclosed, neither asserted fixed.

## v7 entry — critic re-audit fixes (2026-09-17): punct-strip dead line removed, BNGLISH_TERMS bridge fixed, n04a 6-class strings fixed
- `query_extractor.py`: deleted the dead `lowered_tokens = lowered.split()` overwrite — punct-strip now live on the pipeline path (regression test asserts pipeline-path behavior).
- `query_builder.py`: BNGLISH_TERMS single-word keys use token-start matching (ধান-in-সমাধান bridge dead; verified by new test). Multi-word keys unchanged. Other substring keyword lists noted as residual.
- Full suite: 601 passed, 7 skipped at fix time (595 + 6 new boundary tests); independent reproduction showed 600 passed, 8 skipped (one conditionally-skipped env/live test). Zero failures in both. Counts recorded, not claimed as a result.
- Re-runs v3 (deterministic): N01a identical; N01b halt 76 (38.0%), hazard tie 16.07% [8.69,27.81], 0 discordants, extractor 0.52/0.475/0.005; N02 tiers identical. v2 outputs archived as `_v2`; v3 takes base names.
- n04a/n04b re-run (note-only changes): metrics identical, 6-class strings replaced with 10-species truth.
- v3 records: `matcher_fix_v3.diff` (tracked intent.py + query_builder.py hunks), `matcher_fix_v3_query_extractor_FULL.py` + `--no-index` diff vs the v2 FULL copy (all three are untracked working-tree records — "tracked" is never claimed for results/ files).
