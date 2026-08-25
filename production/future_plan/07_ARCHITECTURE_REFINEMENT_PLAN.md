# 07 — Architecture Refinement Plan (Senior-Engineer Pass)

**Status:** PLANNING DOCUMENT — nothing here changes code until a task executes it.
**Date:** 2026-08-25
**Author role:** senior engineer + market pass, requested by the researcher.
**Reads before this:** `00_SCOPE_OUTLINE.md` (capability menu + spine),
`docs/refactor/ARCHITECTURE.md` (current contracts),
`docs/refactor/PROJECT_HANDOFF.md` (what is built).
**Companion written with this:** `08_WEATHER_DATA_SOURCING.md` (BMD/BAMIS routes).

> **Purpose.** `00_SCOPE_OUTLINE.md` answered *what to build*. This document
> answers *how the system must be shaped* so that (a) it stays cheap and safe at
> farmer scale, (b) new knowledge/crops/modules drop in without a rewrite, and
> (c) the architecture itself is the paper's contribution rather than the model
> choice. Every later agent should be able to read Part A and Part J alone and
> know where the project stands and what to pick up.

---

## Part A — Current state, measured (2026-08-25)

Facts below were read off the repo, not remembered. Numbers are the baseline any
future claim must be compared against.

### A.1 Knowledge and deterministic assets

| Asset | Size / count | Path | Read by |
|---|---|---|---|
| Clean knowledge nodes | **2,135 nodes** (12.0 MB JSONL) | `backend/ml_assets/rag_index/processed/knowledge_nodes_clean.jsonl` | retrieval loader |
| Refined nodes | 9.95 MB JSONL | same dir | corpus lineage |
| Source sections (provenance) | **2,946 markdown files** (11.8 MB) | `rag_index/source_md/**` | provenance chain |
| BM25 index | 16.2 MB pickle (+4.5 MB tokens) | `rag_index/indexes/bm25_index.pkl` | `infrastructure/retrieval/bm25.py` |
| Dense index | `nodes.faiss` 8.34 MB + `embeddings.npy` 8.34 MB | `rag_index/indexes/` | `infrastructure/retrieval/dense.py` |
| Dose reference | 71 cited entries / 15 actives | `rag_index/derived/dose_reference_v1.json` | dosage verifier (F1-02) |
| Banned-chemical registry | 15 BD records | `domain/chemical_registry.py` | safety precheck (F1-01) |
| Crop calendars | committed artifact + curated source | `ml_assets/agronomy/crop_calendars_v1.json` | `domain/crop_calendar.py` (P2) |
| Dialect map | 110 words | retrieval expansion | `infrastructure/retrieval/expansion.py` |
| Vision classifiers | crop classifier + 5 crop-specific (`task: classify`) | `ml_assets/vision/**` | `infrastructure/vision/` |
| Soil | 5-fold EfficientNet-B0 + frozen sample manifest | `ml_assets/soil/` | replay-only analyzer |
| Weather | **1 sample snapshot, flagged `is_sample`** | `ml_assets/weather/` | `infrastructure/weather/snapshot.py` |

**The honest headline: 2,135 nodes is small.** It is enough for a defensible
demo and paper, not enough for open-domain Bangladeshi agriculture. The
architecture must therefore be explicitly *coverage-honest* (refuse outside
coverage) and *ingestion-ready* (adding 20k nodes must be a data operation, not
a code change). Both are design requirements below, not aspirations.

### A.2 LLM call sites and cost surface

| Stage | Deterministic part | LLM part | Fallback |
|---|---|---|---|
| Safety | `domain/safety_policy.precheck` rules + 15-item banned registry → terminal decision with **zero** LLM calls | `SafetyClassifier.classify_json` when no rule matched | fail-closed to `low_confidence` (+ demo-cache replay on outage) |
| Rewrite (A1) | — | `ConversationalQueryRewriter.maybe_rewrite` (follow-ups only) | raw query used |
| Retrieval | BM25 + FAISS hybrid + dialect expansion — **no LLM** | — | — |
| Generation | prompt assembly, source truncation, structural citation injection | 1 call (stream or block) | `REFERRAL` text |
| Verifier | `HardenedDosageVerifier` + dose reference + claim parser — **fully deterministic** | — | annotate-and-drop |

**Worst case today: 3 LLM calls per farmer question** (safety + rewrite +
generation). Best case on a deterministic refusal: **0**. Provider config:
`llm_provider=openrouter`, `openrouter_model=google/gemini-2.5-flash-lite`,
`gemini_model=gemini-2.5-flash-lite`, local lane `krishokchat-4b` via
llama-server, ASR `groq/whisper-large-v3-turbo`. Failover chain + circuit
breaker exist (T0-06). `cost_estimate` is recorded but **null** — there is no
price table yet.

### A.3 Surfaces and gates

- **API:** ~27 routes across `qa`, `vision`, `soil`, `speech`, `extras`,
  `history`, `notifications`, `admin`, `auth`, `benchmark`.
- **Frontend:** 21 pages (marketing / app / admin groups), 49 components.
- **PWA:** `frontend/public/sw.js` is a **shell-only** worker — precaches pages
  and library JSON, explicitly never caches `/api/*`. Offline chat is *not*
  supported; `offline-indicator.tsx` exists.
- **Tests:** 37 test files, **410 passed / 7 skipped / 0 failed**; golden replay
  **50 items**, invariants PASS; per-stage telemetry + audit v2 live.

### A.4 The four structural gaps this plan closes

1. **Every safe question costs an LLM call.** There is no deterministic answer
   path. A farmer asking "potato late blight dose?" — a question we have a
   *table* for — still pays generation latency, cost, and hallucination risk.
2. **Knowledge is text-only.** 2,135 prose nodes, but no structured
   `crop × problem × stage → action` table. Retrieval can find a passage; it
   cannot *compute* an answer, so the LLM is forced to be the reasoner.
3. **No extension seams.** Adding irrigation or drone modules today means
   editing the pipeline. There is no capability registry.
4. **No cost/latency budget as a first-class contract.** Telemetry measures;
   nothing enforces, and no price table exists.

---

## Part B — The one architectural idea (this is the contribution)

Everything below follows from a single principle the researcher already named:

> **Answer deterministically when we can prove the answer. Use the LLM only to
> phrase, disambiguate, or when nothing deterministic applies — and say so.**

Concretely, replace "safety → retrieve → generate → verify" with a **five-tier
resolution ladder**. Every query descends the ladder and stops at the first tier
that can answer. The tier that answered is recorded, shown to the farmer, and
counted in the audit trail.

```
Q ──▶ T0  DETERMINISTIC GUARD        rules + banned registry     0 LLM   ~1ms
      │   (already built: precheck, 15-item registry)
      ├──▶ T1  STRUCTURED RESOLVER   fact/decision tables        0 LLM   <10ms
      │   crop × problem × stage → dose, timing, IPM, PHI
      │   → answer is *composed from cited table rows*, not generated
      ├──▶ T2  TEMPLATED ADVISORY    table row + Bengali template 0 LLM  <20ms
      │   (deterministic phrasing; farmer sees a real sentence)
      ├──▶ T3  GROUNDED GENERATION   retrieval + LLM + verifier   1-2 LLM  ~2-8s
      │   (today's path — now the *fallback*, not the default)
      └──▶ T4  HONEST REFUSAL        coverage gate → 16123        0 LLM
```

**Why this is genuinely novel and not just caching.** T1/T2 answers are
*computed from a structured knowledge base with row-level provenance*, so
citation is structural (N2), dosage is correct by construction (N1), and the
answer is byte-identical for the same question forever — which is exactly what a
safety-critical agricultural advisory needs and what an LLM cannot promise. The
literature confirms the direction: CGIAR's Ugani 2.0 puts a rule engine first
and uses AI only to *narrate* rule output; Pezego-HITL (Ghana) reports 55% p95
latency reduction via validated-memory routing; the Bihar Golden-Facts work
reports 85% cost reduction by decoupling facts from phrasing. Nobody has done
this for Bengali with a BD-registered-dose safety verifier underneath.

**What it buys us, in the language funders and reviewers care about:**

| Dimension | Today | With the ladder |
|---|---|---|
| LLM calls per query | 1–3 always | 0 for the common, high-value, high-risk questions |
| Dose-answer correctness | verifier catches errors *after* generation | correct *by construction*; verifier becomes a regression net |
| Latency for a table-answerable question | seconds | milliseconds, works offline |
| Marginal cost per farmer | scales linearly with queries | scales with *novelty* of queries only |
| Paper claim | "we verify LLM output" | "we bound the LLM's authority; it never invents a dose" |

**Non-negotiable invariants (regression-lock these):**
- T0 always runs first; no tier may bypass safety.
- The verifier runs on **T3 only** for sanitization, but T1/T2 rows must pass the
  same dose bounds at *build* time — a bad table row must fail the build, not a
  request.
- Every response carries `resolution_tier` + `provenance` in the API payload and
  in the audit record.
- An empty structured hit is never a silent fall-through to a guess: it is
  either T3 (with sources) or T4 (honest refusal).

---

## Part C — Knowledge architecture: from prose to a real knowledge base

This is the highest-leverage change and the direct answer to "we only have 2k
nodes, but government support could give us far more."

### C.1 Two-layer knowledge model

**Layer 1 — Facts (structured, machine-checkable).** A normalized table set,
built offline from the corpus, each row carrying `source_node_id` + document +
page/section so provenance survives:

```
crop, problem(disease|pest|deficiency|abiotic), stage,
  active_ingredient, registered_dose(min,max,unit), application_interval,
  pre_harvest_interval, ipm_alternatives[], banned_flag, severity,
  source_node_id, source_doc, confidence, verified_by, verified_at
```

`dose_reference_v1.json` (71 entries) is the seed — it proves the extraction
works. The task is to widen it into a real fact base and make it the *primary*
answer source rather than only a verifier input.

**Layer 2 — Passages (prose, for T3).** The existing 2,135 nodes + BM25/FAISS,
unchanged.

### C.2 Ingestion as a data operation, not a code change

The crop-calendar pattern already proves the shape and must become the standard
for **all** knowledge: `curated source → offline builder script → committed,
versioned artifact → fail-open loader → test that locks "adding data needs no
code change."`

```
sources/            official PDFs/HTML + license + retrieval date
  ↓ extract (offline, scripted, logged)
staging/            candidate rows w/ provenance + extraction confidence
  ↓ validate        schema + dose bounds + banned cross-check + unit sanity
  ↓ human review    agronomist approves; rejections are recorded, not deleted
artifacts/          facts_vN.json + nodes_vN.jsonl + indexes (SHA-256 pinned)
  ↓ load            fail-open; missing artifact = honest "unavailable"
```

**Non-negotiables:** every artifact versioned + hash-pinned; `corpus_version`
already flows into cache keys (P0-7) and must extend to fact-base version;
rejected extractions are archived for the paper's error analysis; **no fabricated
row ever ships** — an unextractable dose stays absent (the soil-honesty lesson,
AGENTS.md rule 5).

### C.3 Designed-for-growth, not just "more data"

The same loader shape must accept future node types without touching the
pipeline: `text` (now), `fact` (C.1), `image` (disease reference photos),
`geo` (upazila/AEZ attributes), `timeseries` (weather, prices), `sensor`
(irrigation/IoT), `media` (audio advisories). A node is a typed record with
provenance; retrievers are registered per type. That is the whole extension
mechanism — no new pipeline per data kind.

### C.4 If government funding arrives (scale plan, stated honestly)

| Scale | Nodes | What changes | What does *not* |
|---|---|---|---|
| Today | 2,135 | — | — |
| +DAE/BAMIS bulletins + Hatboi | ~10–20k | rebuild indexes offline; fact base grows | pipeline code, API, UI |
| +full NARS corpus | ~50–100k | FAISS→IVF/HNSW; sharded BM25; may need a real vector store | contracts stay identical |
| +farmer interaction data | millions of rows | separate analytics store, privacy review | advisory path |

The claim to make to a funder is precise: **"ingestion is a scripted data
operation; a 10× corpus is a rebuild, not a rewrite."** That is only true if C.2
is enforced, which is why it is task 1 in Part J.

---

## Part D — Separation of use cases (the "top-tier company" structure)

The researcher's instinct is right: use cases must be genuinely separated, not
one chat endpoint doing everything. The clean-architecture layers already exist
(`domain / application / ports / infrastructure`); what is missing is an explicit
**capability contract** so features become plug-ins.

### D.1 Capability registry

Every farmer-facing capability declares itself as a module implementing one port:

```python
class Capability(Protocol):
    id: str                      # "disease_advisory", "irrigation", "market_price"
    def can_handle(intent) -> float          # 0..1 claim strength
    async def resolve(ctx) -> CapabilityResult  # tier, answer, provenance, cost
    requires: frozenset[str]     # "vision", "weather", "farm_profile", "facts"
    available: bool              # honest false when its assets are missing
```

The orchestrator asks: *which capability claims this intent, and can it be served
at which tier?* Adding drone imagery, agentic irrigation, market prices, credit,
or livestock later = register a new capability + its data artifacts. **No
pipeline edits.** This is the seam the researcher asked for.

Capabilities to declare now (even if some are stubs marked `available: false` —
honesty over vapor): `disease_advisory` (vision + facts), `qa_advisory` (T3),
`soil_advisory` (replay-only today), `weather_risk` (PR1), `stage_advice` (P2),
`safety_escalation` (16123). Reserved, explicitly not built: `irrigation`,
`market_price`, `drone_survey`, `livestock`, `credit`.

### D.2 Intent classification — the cheap-model sweet spot

This is exactly where `gemini-2.5-flash-lite` earns its keep: one small
structured call that routes to a capability and extracts slots
(crop, problem, stage, upazila). Rules:

- **Deterministic first:** a keyword/embedding matcher handles the common cases
  (the safety precheck already proves the pattern). The LLM is called only on
  ambiguity.
- **Cache aggressively:** intent for a normalized query string is stable →
  cache it. Repeat questions cost nothing.
- **Fail-closed:** unknown intent → T4 refusal + 16123, never a guess.
- **Merge with safety:** safety classification and intent extraction are one
  structured call, not two. That removes one LLM call from every query
  immediately.

### D.3 Per-capability quality gates

Each capability owns its own golden set and its own refusal policy, so a
regression in irrigation cannot silently degrade disease advisory. The existing
50-item golden replay becomes the *first* such set, not the only one.

---

## Part E — Cost, latency, and the market-efficiency case

### E.1 Make cost a real contract

`cost_estimate` is currently null. Fix in three steps:

1. **Price table artifact** (`config/model_prices.json`): per-model input/output
   token price + fetch date + source URL. Versioned like any other artifact,
   because prices change.
2. **Per-request budget**: a soft ceiling per query and a hard daily ceiling per
   API key/user. Exceeding the soft ceiling forces a cheaper tier (T3 with fewer
   sources, or T4 refusal) rather than silently spending.
3. **Cost dashboards from the audit trail** — the data is already recorded
   per-stage; only the price join is missing.

### E.2 The tier-mix argument (measure it, don't assert it)

The economics of the whole system reduce to one number: **what fraction of real
farmer queries resolve at T0–T2 (zero LLM)?** That single metric is the paper
result, the funder slide, and the ops KPI simultaneously.

Design a **dedicated cost experiment**, not a hand-wave:
- Input: the existing `farmer_benchmark_1000.jsonl` + the 20,112-record safety
  set already built.
- Measure per tier: resolution %, p50/p95 latency, LLM calls, measured token
  cost, and answer quality vs the T3 baseline.
- Report cost per 1,000 queries at three mixes (pessimistic / measured /
  with-fact-base-expanded) so the projection is bounded by evidence.
- **Rule:** never publish a projected cost without stating the measured tier mix
  it came from (AGENTS.md rule 5 applies to cost numbers too).

### E.3 Latency budget

| Tier | Target p95 | Why it matters |
|---|---|---|
| T0/T1/T2 | < 100 ms | feels instant on a cheap phone; works offline |
| T3 stream first token | < 2.5 s | farmer sees motion before giving up on 3G |
| T3 full answer | < 8 s | current stage telemetry already measures this |
| Vision (on-device) | < 150 ms | the U1 claim from doc 00 |

### E.4 Safety of the API surface (market-efficient ≠ careless)

Keys server-side only; per-user and per-key rate limits (T0-07 exists); prompt-
injection guard before any tool/capability dispatch — **critical** once
capabilities can take actions like irrigation; no farmer PII in provider
payloads (redaction exists for audit, extend the rule to prompts); provider
failover already circuit-broken (T0-06). Any future capability that *acts* (not
just advises) requires an explicit human confirmation step — an agentic
irrigation module must never open a valve on an LLM's say-so.

---

## Part F — Mobile-first reality (the farmer's actual phone)

Doc 00 established the constraint: on-device generative LLM on 2–4 GB phones is
not deployable; on-device *classification* is. This plan adds the systems view.

- **The ladder is what makes offline real.** T1/T2 are table lookups —
  shippable to the device as a compact JSON pack (crop-scoped, tens of KB).
  A farmer with no signal still gets a correct, cited dose for their crop. That
  is impossible in a generation-only architecture, and it is the strongest
  practical-feasibility claim we can make.
- **Service worker must grow from shell-only to data-aware**: cache the fact
  pack + the farmer's own profile/stage + last N advisories in IndexedDB.
  Current `sw.js` deliberately never caches `/api/*`; the new rule is "cache
  *deterministic* responses (tier ≤ 2) keyed by fact-base version, never cache
  T3 generations."
- **Bandwidth discipline**: client-side resize → WebP → EXIF strip before
  upload; upload only when the on-device classifier is unsure (U1/U3). Show the
  farmer *why* ("এই ছবিটি স্পষ্ট নয়, তাই পাঠানো হচ্ছে") — transparency is a
  trust feature, not a nicety.
- **Install + update UX**: PWA install prompt, explicit "advice pack updated"
  state, and a visible last-synced timestamp so nobody acts on stale guidance.

---

## Part G — UI/UX architecture (structure, not decoration)

The design system (কৃষি পত্রক) and 21 pages exist. What is missing is
**information architecture that mirrors the ladder** so the interface teaches
trust.

1. **Every answer shows its provenance level.** A farmer should see, at a
   glance: *measured / official table / official document / AI-drafted*. The
   soil card's "ডেটাসেট নমুনা · পরিমাপিত" badge is the correct pattern — make it
   a system-wide component driven by `resolution_tier`.
2. **Task-first home, not feature-first.** Replace a feature grid with the
   farmer's actual decisions: "আমার ফসলের এখন কী করা দরকার" (stage tasks),
   "সমস্যা চিহ্নিত করুন" (photo), "প্রশ্ন করুন" (chat), "সতর্কতা" (alerts). P1/P2
   already supply the data for a personalized home (F5).
3. **The agent trace stays, but earns its place.** Show tier resolution, not
   just stage names — "টেবিল থেকে উত্তর (এআই ব্যবহার হয়নি)" is a stronger trust
   signal to both farmers and reviewers than a spinner sequence.
4. **Every screen states its limits.** Coverage refusals, sample data, forecast-
   derived alerts, and approximations must be visually distinct from measured
   facts. This is already the house style; make it a checklist item per page.
5. **Accessibility as a hard gate** (F1 in doc 00): 44–48 px touch targets, the
   12 px legibility floor already adopted, `aria-live` on streams, and Bengali
   plain-language review of every farmer-facing string.
6. **Voice is the accessibility multiplier**, but scope it: TTS on advisories
   first (already partly built), ASR second, and never make voice the only path
   to a feature.

---

## Part H — What the paper claims after this refinement

Doc 00 §8 lists five claims (N1–N5). The ladder adds the one that ties them
together and is the strongest of the set:

> **N6 — A tiered resolution architecture that bounds an LLM's authority in a
> safety-critical advisory domain**: dosage and treatment answers are composed
> from a provenance-carrying structured fact base and never generated, with the
> LLM confined to phrasing, disambiguation, and out-of-table questions —
> evaluated by measured tier mix, cost per 1,000 queries, p95 latency, and
> dose-error rate against a held-out set.

Evaluation to run (all with assets we already have):
- **Tier mix + cost/latency** on `farmer_benchmark_1000.jsonl` (Part E.2).
- **Dose-error rate**: T1/T2 vs T3 vs an ungrounded baseline.
- **Citation integrity**: structural provenance → hallucinated-citation rate 0
  by construction at T1/T2 (N2 becomes provable, not argued).
- **Safety**: existing 20,112-record set; refusal and over-refusal (144 tests).
- **Dialect**: 110-word map, dialect vs standard Bengali retrieval accuracy.
- **Offline feasibility**: fact-pack size, on-device classifier latency/accuracy.

Positioning honesty: rule-engine-first advisory is not new (Ugani 2.0 CGIAR),
routing/caching for latency is not new (Pezego-HITL), fact/phrasing decoupling is
not new (Bihar Golden Facts). **The combination for Bengali, with BD-registered
dose bounds, structural provenance, dialect input, and an offline-capable
deterministic tier, is.** Claim the combination and cite the priors — exactly the
framing doc 00 §8 already mandates.

---

## Part I — Risks and where this plan could go wrong

| Risk | Mitigation |
|---|---|
| Fact-base extraction produces wrong rows | build-time validation + agronomist review gate + archived rejections; a bad row fails the build |
| The ladder becomes two systems that disagree | T1/T2 rows and T3 answers both trace to the same corpus nodes; disagreement is a test failure |
| Over-refusal rises as coverage honesty tightens | the 144 over-refusal tests already guard this; track refusal rate per release |
| Scope explosion via capabilities | registry requires assets + golden set + `available` flag before a capability ships; stubs stay `false` |
| Offline packs go stale | version + last-synced timestamp surfaced in UI; refuse to answer from a pack older than a configured window |
| Cost projections outrun evidence | E.2 rule: no published cost without its measured tier mix |
| Non-commercial data licensing (BMD) leaks into a paid tier | licensing recorded per artifact; see doc 08 §Route B |

---

## Part J — Execution roadmap (dependency-ordered, for later agents)

Each item is bounded, additive, reversible, and independently verifiable — the
same discipline as the T0/P0/F1/PR1/P1-P2 tasks already completed. **Nothing
here is started.** An agent picking this up should write a task doc under
`docs/production_readiness/tasks/` first, exactly like `P1_P2_farm_profile_stage_advice.md`.

| # | Task | Depends on | Deliverable | Why first/later |
|---|---|---|---|---|
| **R1** | **Knowledge-ingestion contract**: formalize `sources → staging → validate → artifact → loader` with schema, hash pinning, and a test that locks "new data needs no code change" | — | `docs/` contract + builder skeleton + test | everything else assumes data can grow safely |
| **R2** | **Fact base v1** for the potato/late-blight spine: widen `dose_reference_v1.json` into the Part C.1 schema with row provenance + build-time dose validation | R1 | `facts_v1.json` + validator + tests | turns the verifier's data into an *answer source* |
| **R3** | **Resolution-tier plumbing**: add `resolution_tier` + provenance to contracts, API payloads, audit records, and the UI badge — with T3 as the only implemented tier | — | schema + audit + UI component | makes the ladder observable before it exists; zero behavior change |
| **R4** | **T1/T2 structured resolver** behind a flag, for potato late blight only | R2, R3 | resolver + Bengali templates + golden set | the actual novelty; scoped to one disease first |
| **R5** | **Merge safety + intent into one structured call**, deterministic matcher first, cached | R3 | one call instead of two; capability routing | immediate cost/latency win |
| **R6** | **Capability registry** + declare existing features as capabilities (stubs `available: false`) | R5 | `Capability` port + registration | the extension seam for drone/irrigation later |
| **R7** | **Cost + latency contract**: price-table artifact, per-request budget, tier-mix experiment on the 1,000-query benchmark | R4 | measured cost/latency report | the funder + paper number |
| **R8** | **Real weather snapshot** (drop `is_sample`) via the RIMES upazila route | — | dated artifact + provenance | see doc 08; unblocks PR1 honestly; can run in parallel |
| **R9** | **Offline fact pack + data-aware service worker** (cache tier ≤ 2 only) | R4 | crop-scoped pack + IndexedDB + UI sync state | the practical-feasibility claim |
| **R10** | **On-device classifier export** (U1) + confidence-gated upload (U3) | R9 | `.tflite` + client gating + accuracy report | completes the mobile story |
| **R11** | **Task-first personalized home + provenance badges everywhere** (F5, G.1–G.4) | R3, R9 | UI restructure | makes the architecture legible to farmers and judges |
| **R12** | **Extend the fact base + ladder to maize FAW and rice pests** | R4 | more crops, same code | proves the "data operation, not rewrite" claim |

**Suggested first sprint (highest value per unit risk): R3 → R1 → R2 → R4**, with
R8 running in parallel since it has no dependencies. R3 first because it is pure
instrumentation with zero behavior change, so it can land immediately and makes
every later step measurable.

---

## Part K — For a future agent reading this cold

- **What this project is:** a Bengali agricultural advisory system with a
  safety-aware pipeline (safety → retrieval → generation → verification), 2,135
  knowledge nodes with full provenance, 6 vision classifiers, a soil replay
  lane, admin/broadcast console, Supabase auth, PWA shell, 410 passing tests.
- **What is built:** see `docs/refactor/PROJECT_HANDOFF.md` — it is the
  authoritative log (T0 hardening, P0 rollout, G0–G9 govt lane, F1 safety data,
  PR1 weather alert, P1+P2 farm profile, soil honesty fix).
- **What is planned but NOT built:** everything in Part J of this document, plus
  the doc 00 menu items not yet marked done.
- **The two documents that define direction:** `00_SCOPE_OUTLINE.md` (what to
  build and why, with the potato spine) and this file (how it must be shaped).
- **The rules you cannot break:** `AGENTS.md` — especially no fabricated data
  (rule 5), no live scraping/index building (rule 2), auth never gates the demo
  (rule 1), locked tech stack (§3), and the deprecated-arXiv policy (rule 9).
- **The discipline that has kept this project clean:** one bounded task, one task
  doc, additive and reversible changes, full test suite + golden replay before
  calling anything done, and honesty over polish when data is missing.


