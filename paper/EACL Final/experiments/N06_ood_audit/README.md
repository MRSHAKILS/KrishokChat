# N06 — OOD Audit (LOCKED, analysis of frozen records)

**Status:** REAL_MEASURED_ANALYSIS · **Evidence:** E09 stratified file (40 OOD rows)

- Injections blocked **10/10** (prompt_injection, deterministic guard).
- Off-topic refused **0/30** — deterministic path has no firing OFF_TOPIC rule; general-knowledge queries get answered (20) or crop-clarified (10). Real gap, disclosed; production LLM branch may differ (unmeasured here).
- The blended "0.25" is retired. Paper splits both numbers.
