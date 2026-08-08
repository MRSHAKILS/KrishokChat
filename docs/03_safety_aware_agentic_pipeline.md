# TASK 03 — Safety-Aware Agentic Pipeline (Real Implementation)

**Read `AGENTS.md` Section 4 first — this task builds exactly what's specified there.**
**Requires Task 01 (working retrieval + generation) complete. Can run in parallel with Task 02's frontend work, since Task 02 already built a visual placeholder for the "flagged" state that this task will wire up for real in Step 9.**

---

## 0. Scope

**In scope:** the four-stage pipeline (Safety/Router Agent → Retrieval Agent → Generation Agent → Verifier Agent), the audit-trail log, wiring it into `/api/qa` in place of Task 01's direct path, and streaming real agent-stage events to the frontend's `AgentTraceStepper`.

**Out of scope:** anything about the crop classifier/YOLO pipeline (a separate agent-safety pass for that is a later task, not this one). Voice/TTS. Multi-turn conversation memory.

**Why this matters beyond the poster:** this is the one piece of the project that visibly demonstrates responsible-AI engineering to reviewers, not just model capability. Build it so it's genuinely correct, not just genuinely present — a safety layer that's decorative (always says "safe," never actually triggers) is worse for your credibility than not having one, if a reviewer probes it.

---

## Step 1 — Decide how the Safety/Router Agent classifies queries

You already have a warm, loaded Gemma model behind llama.cpp (from Task 01). Reuse it — do not load a second model just for classification, that doubles your memory footprint and demo-day risk for marginal benefit.

1. **Rule-based Prefilters:** Before the LLM, implement deterministic checks:
   - **Banned/Restricted Chemicals:** A curated list of banned active ingredients/brands in Bangladesh (handling Bengali/Banglish spelling variants).
   - **Self-Harm/Poisoning Risk:** Keyword/pattern filters for high-risk phrases in Bangla/Banglish.
   - **Prompt Injection:** Simple pattern matching for jailbreak attempts in Bangla/English.
   If a rule triggers, bypass the LLM and return the corresponding unsafe classification immediately.
2. Design a short, structured classification prompt: system instruction describing the six categories from `AGENTS.md` Section 4 (`safe_agri`, `banned_or_restricted_chemical`, `self_harm_or_poisoning_risk`, `off_topic`, `prompt_injection`, `low_confidence`), instructing the model to output **only** a JSON object. Ensure the schema includes `category`, `confidence`, `reason`, `matched_rules` (array), and `requires_escalation` (boolean).
3. 🔎 Check whether your installed llama.cpp server supports **grammar-constrained decoding** (GBNF grammars) or a JSON-mode/structured-output flag on its completion endpoint. If it does, use it to force valid JSON output for this call — this is meaningfully more reliable than hoping a free-text completion happens to parse as JSON, and it's exactly the kind of thing that silently breaks a demo if you skip it.
3. Keep this call cheap: low `max_tokens` (you only need a few words of JSON back), and no retrieved context needed at this stage — it only needs the raw user query.
4. Write `backend/app/agents/safety_agent.py`: takes a query string, calls the classification prompt against the same llama.cpp server, parses the JSON response, and returns a structured result (category + reason). If parsing fails for any reason, **fail closed**: treat it as `low_confidence` rather than `safe_agri` — a classification error should never accidentally skip the safety check.

**Verify:** Develop a comprehensive safety benchmark dataset (100–200 examples per category, plus Banglish and adversarial rephrasings). Write a test script and confirm the classifier (rules + LLM) returns the expected category.

---

## Step 2 — Canned responses for unsafe/out-of-scope categories

1. Draft short, calm canned responses for `banned_or_restricted_chemical` and `self_harm_or_poisoning_risk` per `AGENTS.md` Section 4: one or two sentences, non-judgmental tone, includes the Krishi Call Center number (**16123**) as the escalation contact, no long safety essay. Draft these in English first for review, then have a fluent Bengali speaker (you) write/review the final Bengali wording directly rather than trusting a raw translation — these are safety-relevant strings and deserve a human pass, not an agent's best guess at phrasing.
2. Draft a short, matter-of-fact response for `off_topic` (politely states this assistant is agriculture-focused) and `prompt_injection` (declines and restates purpose, doesn't explain the detection).
3. Draft a `low_confidence` response acknowledging the knowledge base doesn't clearly cover this, suggesting 16123 as an alternative rather than guessing.
4. Store these as a small structured file (`backend/app/agents/canned_responses.py` or a JSON file next to it) keyed by category — not hardcoded inline in the agent logic, so they're easy to review/edit without touching code.

**Verify:** every non-`safe_agri` category has a reviewed, final-wording response ready, in Bengali, with 16123 included where specified.

---

## Step 3 — Audit trail logging

1. Write `backend/app/services/audit_log.py`: appends one record per query to a local store under `backend/app/logs/` — JSON Lines is simplest (one JSON object per line: timestamp, query text, category, action taken, and later the verifier's flag from Step 6). SQLite is a reasonable alternative if you'd rather query it with SQL for the Step 10 metrics panel — pick whichever you'll actually query later with less friction.
2. Make sure this directory is gitignored (already set up in Task 00) but exists at runtime (create it on startup if missing).
3. This must be a **local file only** — no external logging service, no analytics SDK. This is a prototype safety measure, not a production telemetry pipeline.

**Verify:** running a few test queries through the classifier produces corresponding log lines with correct fields.

---

## Step 4 — Confirm Retrieval and Generation agents are orchestration-ready

These already exist from Task 01 (`rag_index.py` retrieval function, `generation_agent.py`). This step is just making sure they're callable as clean, independent functions the orchestrator can call in sequence, not tangled into the old direct `/api/qa` route logic.

1. If Task 01's retrieval/generation logic is currently inline inside the old route handler, extract it into standalone, testable functions if it isn't already (`retrieval_agent.py` wrapping the Step-3-from-Task-01 retrieval function, `generation_agent.py` already exists).
2. No behavior change here — just confirm clean separation so Step 7's orchestrator can call each stage independently.

**Verify:** retrieval and generation each still work correctly when called directly, exactly as they did at the end of Task 01.

---

## Step 5 — Verifier Agent

This runs **after** generation, before the answer reaches the user — its job is catching ungrounded specific claims (especially chemical dosages, treatment amounts) that the model stated but that don't clearly appear in the retrieved source passages.

1. Start with a **fast heuristic pass**, not another full LLM call, to keep latency down in the common case: a regex/pattern check for dosage-like patterns in the generated answer. This must handle **Bengali numerals (০-৯)**, **English numerals (0-9)**, **unit synonyms** (মিলি, মিলিলিটার, গ্রাম, লিটার, mg/ml/L equivalents, etc.), and **dosage phrasing normalizations** (e.g., "প্রতি লিটার পানিতে ২ মিলি", "আধা চামচ"). For each match, check whether that same normalized number+unit combination appears in the retrieved source passages.
2. If the heuristic finds an ungrounded dosage claim, mark the answer as `flagged-unverified` rather than blocking it outright — attach a visible note ("this specific amount could not be verified against our database — please confirm with 16123 before applying") rather than silently failing. This maps directly to the `ConfidenceBadge` component already built in Task 02.
3. If the heuristic finds nothing suspicious, mark the answer `verified` (grounded) with no extra LLM call needed — keeps the common-case latency low.
4. (Optional, only if time allows after everything else works): a true LLM-based grounding check as a second pass for borderline cases, instead of the heuristic being the only check. Do not build this until Steps 1–9 are solid — it's a nice-to-have, not core.

**Verify:** run 3–4 test answers you construct to contain an obviously ungrounded dosage number and confirm they get flagged; run 3–4 clean, grounded answers and confirm they pass through as `verified`.

---

## Step 6 — Orchestrator

1. Write `backend/app/agents/orchestrator.py`: a single async function taking a user query, running the four stages in order (Safety → [stop here if unsafe/off-topic/injection, return canned response] → Retrieval → Generation → Verifier), and yielding stage-change events plus the final streamed answer.
2. Design the event stream so the frontend can update `AgentTraceStepper` in real time as stages progress — 🔎 confirm how to interleave stage-marker events with the token-streaming response in whatever protocol Task 02 already wired the frontend to expect (Server-Sent Events custom event types, or a simple prefixed-line convention within the existing stream — match whatever's already working rather than redesigning the transport).
3. Every path through the orchestrator (safe, flagged, unsafe/canned) must call `audit_log.py` exactly once with the correct final outcome.

**Verify:** a full run through each of the 8–10 test queries from Step 1 produces the correct end-to-end behavior: canned response + log entry for unsafe categories, real grounded/flagged answer + log entry for safe ones, and correct stage events emitted throughout.

---

## Step 7 — Replace the `/api/qa` route

1. Update `backend/app/api/qa.py` to call `orchestrator.py` instead of Task 01's direct retrieval→generation path.
2. Keep the response format backward-compatible with what Task 02's frontend already expects, extended with the new stage events — this should be additive, not a breaking change to the frontend contract, so Task 02's chat page mostly just starts reflecting real stages instead of a placeholder.

**Verify:** the chat page from Task 02 now shows the `AgentTraceStepper` progressing through real stages (not a canned animation), and a genuinely unsafe test query now visibly produces the flagged/redirected card style Task 02 built as a placeholder — this is the moment the two tasks converge.

---

## Step 8 — Wire the frontend "flagged" card to real output

1. In the chat page, replace Task 02's manual test-flag trigger for the flagged `AdvisoryCard` variant with the real category/action data now coming from the orchestrator.
2. Confirm the flagged card's "consult 16123 / go to Find Help page" link still works correctly against real backend output.

**Verify:** triggering each unsafe category from your Step 1 test set produces the correct visible card variant end to end, live, through the actual UI — not just in backend logs.

---

## Step 9 — Safety metrics on the Research & Benchmarks page

1. Add a small section to the Research page (built in Task 02) reading from the audit log: a simple breakdown (count per category) from your test-run history. This turns your safety layer into a visible, credibility-building artifact rather than an invisible backend feature — genuinely useful for the poster.
2. This can be a static read at page-load from the log file — no need for live polling.

**Verify:** the Research page shows real counts reflecting your actual test queries so far, not placeholder numbers.

---

## Step 10 — Full regression test

Before calling this task done, re-run:
1. All 8–10 classification test queries from Step 1 — confirm still correct end to end through the full pipeline, not just the isolated classifier.
2. The Task 01 Step 6 sanity test set — confirm normal safe queries still work correctly and haven't regressed in quality or latency now that a classification call precedes them.
3. Note the added latency from the classification step specifically (compare against the Task 01 baseline) — if it's meaningfully hurting your 3–4 minute demo window, that's the moment to revisit Step 1's "keep it cheap" choices (shorter prompt, lower max_tokens) before demo day, not after.

---

## Step 11 — Report back

Write `TASK_03_REPORT.md`:
- Confirm grammar-constrained/JSON-mode decoding worked, or note the fallback parsing approach used instead.
- The final reviewed Bengali canned-response wording (or a link to where it's stored).
- **Safety Metrics Tracking:** Report safety classification precision/recall, false negative rates for unsafe categories, refusal correctness, prompt injection resistance, and ungrounded dosage interception rates over the benchmark dataset. Note any human expert review of flagged cases.
- Step 10's latency comparison numbers.

**Stop here.** A true LLM-based verifier second pass, multi-turn safety context (e.g. a user rephrasing to get around a flag), and the equivalent safety wrapper for the image-detection pipeline are all reasonable next steps but are separate future tasks, not required for this one.