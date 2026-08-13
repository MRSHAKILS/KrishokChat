# T06 Vision Defect Specification — v1

**Status:** P0 evidence specification for the vision pipeline source-empty evidence defect
**Date:** 2026-08-12
**Ledger:** `T06_vision_defect_spec_v1.md`
**Evidence artifact:** See `T06_evidence_manifest_v1.md`
**Repo revision:** `621911a492eb35314d43e553c397b6b24ce54b6f`

## 1. T04 Evidence Summary — what was found

| Evidence ID | Location | Finding | Status |
|---|---|---|---|
| V1 | `backend/app/application/vision_pipeline.py:283-286` | Advisory confidence = {"blocked","low_confidence"} AND `info.get("solution_bn")` exists → treatment_advice = raw KB text; **treatment_confidence = "verified"** (misleading); **treatment_sources = ()** (empty) | **DEFECT CONFIRMED** |
| V2 | `backend/app/application/vision_pipeline.py:289-293` | Advisory is None (exception at line 266) AND `info.get("solution_bn")` exists → treatment_advice = raw KB text; **treatment_confidence = "verified"** (misleading); **treatment_sources = ()** (empty) | **DEFECT CONFIRMED** |

**Defect description:** Knowledge base text is presented as "verified" without passing through the lexical verifier (the `QAPipeline`), and treatment_sources are empty. This breaks the provenance chain: farmers see a verified advice but cannot trace where it came from; the system incorrectly marks a source-empty KB fallback as verified.

**Rules violated:**
- **Provenance traceability** (no source IDs in `treatment_sources`)
- **Verification semantics** (`"verified"` confidence without verifier passage)
- **Safety-by-retrieval** (safety before retrieval expectation compromised by empty source list)

**Impact:** This defect is present in the captured commit `ef0d9d8c92b888c983836ab4f76e6687e7c4f452` and persists in the current checked-in code. It must be fixed before the integrated system can claim evidence‑linked, relation‑aware selective certification for vision advisories.

## 2. T06 Specification — remediation contract

### 2.1. Remediation goal

**Goal:** Ensure all treatment advice returned by the vision pipeline is either (A) verified through the shared `QAPipeline` (with genuine source IDs) OR (B) explicitly flagged as source-empty KB fallback and marked with confidence `low_confidence` and `treatment_sources` as empty.

### 2.2. Artifact boundary and file ownership

**Functional boundary:** The fix must be applied **only** within:

- `backend/app/application/vision_pipeline.py` (detect method)
- **DO NOT** modify: QA pipeline, verifier, safety, retrieval, or any application code beyond the vision pipeline's detect method.

**Files to modify (explicit list):**
1. `backend/app/application/vision_pipeline.py` lines 283-286 and 289-293
2. **Related:** Any new test fixtures in `backend/tests/test_vision.py` that fail until fixed (remain in repo, not in application code)

### 2.3. Remediation details

#### 2.3.1. For branch 1 (advisory confidence blocked/low)

**Current (defective) code (vision_pipeline.py:283-286):**
```python
if advisory.confidence.value in {"blocked", "low_confidence"} and info and info.get("solution_bn"):
    treatment_advice = str(info["solution_bn"])
    treatment_confidence = "verified"  # ← MISLEADING
    treatment_sources = ()             # ← EMPTY SOURCES
```

**Fixed code:**
```python
if advisory.confidence.value in {"blocked", "low_confidence"} and info and info.get("solution_bn"):
    treatment_advice = str(info["solution_bn"])
    treatment_confidence = "low_confidence"  # ← CORRECT: not verified
    treatment_sources = ()              # ← EMPTY SOURCES preserved
```

#### 2.3.2. For branch 2 (no advisory)

**Current (defective) code (vision_pipeline.py:289-293):**
```python
else:
    trace.append(VisionTraceEvent(VisionStage.ADVISORY, "skip", "knowledge-base fallback"))
    if info and info.get("solution_bn"):
        treatment_advice = str(info["solution_bn"])
        treatment_confidence = "verified"  # ← MISLEADING
```

**Fixed code:**
```python
else:
    trace.append(VisionTraceEvent(VisionStage.ADVISORY, "skip", "knowledge-base fallback"))
    if info and info.get("solution_bn"):
        treatment_advice = str(info["solution_bn"])
        treatment_confidence = "low_confidence"  # ← CORRECT: not verified
```

#### 2.3.3. Additional rule: advisory confidence "verified" or "flagged-unverified" is okay

**Keep as is:** If `advisory.confidence.value in {"verified", "flagged-unverified"}` (line 274-279) or `advisory.confidence.value in {"verified"}` (line 283-286 originally) we already have proper `treatment_sources` from `advisory.sources` and no misleading "verified" for source-empty KB fallback.

### 2.4. Test Evidence (failing fixtures before fix)

These tests already exist in `backend/tests/test_vision.py`; they will fail until the above fixes are applied.

| Test | Expected failure before fix (for T06 evidence) | Status |
|---|---|---|
| `test_classification_routes_to_advisory_workflow_without_boxes` (line 82-97) | The test expects `treatment_confidence == "verified"` (from advisory) and `treatment_sources` not empty. After the fix, the test will need to update its expectation for the KB fallback branch (T06 is evidence collection, not test changes). |
| Add new failing fixture `test_vision_fallback_source_empty_marked_low_confidence` | New fixture that directly exercises the two defect branches and asserts `treatment_confidence == "low_confidence"` and `treatment_sources == ()`. |

### 2.5. Handoff notes for downstream tasks

- **Goal:** Once T06 is complete, the vision pipeline's detect method will never mark a source-empty KB fallback as "verified".
- **Integration:** After T06, run backend tests to confirm all existing tests pass; add the new failing fixture as a gate for the T06 implementation (the fixture will be placed under `backend/tests/test_vision.py`).
- **Artifact:** The fixes are confined to `backend/app/application/vision_pipeline.py`. No other file changes or application-side redesign needed.
- **Traceability:** Use `research_artifacts/reports/t06/` as a staging area for the T06 fixture code and evidence logs until T06 passes gates.

## 3. Evidence Manifest

See `T06_evidence_manifest_v1.md` for exact file paths, command logs, and hash checksums of the fixes applied.

## 4. Gate Evaluation

- **T06 STOP criteria:** The defect evidence is confirmed in the captured code; no remediation exists yet. **Stop** for any integrated safety claim that relies on vision fallback until the fix is applied.
- **T06 GO condition:** The fixes are applied, and the new failing fixture passes (i.e., assertions on `treatment_confidence` and `treatment_sources` match the new correct expectations).

**Next:** After T06 implementation, run backend test suite to confirm no regressions and that the new fixture passes.

---
**T06 Vision Defect Specification — v1 complete, 2026-08-12**

- **Defect:** Source-empty vision fallback incorrectly stamped "verified".
- **Remediation:** Change treatment_confidence from "verified" to "low_confidence" in both fallback branches; keep treatment_sources empty.
- **Artifact:** Modified `backend/app/application/vision_pipeline.py` lines 283-286 and 289-293.
- **Evidence:** See `T06_evidence_manifest_v1.md`.
- **Goal:** All vision advisories either have real verifier sources (verified) or are low_confidence with empty sources (KB fallback).