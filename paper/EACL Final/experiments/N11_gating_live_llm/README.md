# N11 — Live-vs-Deterministic Gating (LOCKED, critic-audited)

**Status:** REAL_MEASURED · **Result:** `results.json` (+ amendment: crosstab, confidence, provider) + 200 per-query records

- Live endpoint: production container via **OpenRouter**, model `google/gemini-2.5-flash-lite`, temperature 0.2, max 1000 tokens, accessed 2026-09-17, 200 requests. Token usage not recorded by the runner — cost is NOT measured; report latency + qualitative API-cost trade-off only.
- Halt = operational `len(sources)==0` (clarification, guard, refusal, or no-retrieval). Live 20/200 (10%) vs deterministic 76/200 (38%); agreement 136/200 (68%): agree-halt 16, agree-pass 120, live-pass/det-halt 60, live-halt/det-pass 4. Latency p50 4.2s live vs milliseconds deterministic.
- Live confidence: verified 180, flagged-unverified 8, blocked 10, low_confidence 2.
- Framing: two operating points (cheap-conservative vs 4.2s-broader), never a model ranking. The 60 live-pass/det-halt rows await answer-quality review — no coverage or quality superiority claim until then.
