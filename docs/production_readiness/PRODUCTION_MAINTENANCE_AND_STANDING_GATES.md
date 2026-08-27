# Production Maintenance & Standing Gates Plan
## KrishokChat Agricultural Advisory System

> **Document Type:** Production Maintenance Protocol & Standing Safety Gate Specification  
> **Target Audience:** Core Maintainers, Reviewers, Engineering Agents  
> **Status:** ACTIVE & ENFORCED  
> **Last Audited:** 2026-08-28

---

## 1. Executive Summary & Purpose

This document defines the **standing gates, validation rules, runtime boundaries, and maintenance protocols** governing the production application (`backend/`, `frontend/`, `supabase/`, `deploy/`).

Every change, release, demo deployment, or experiment must adhere to these gates to guarantee:
1. **Zero Demoware / Zero Failure Risk:** The 3–4 minute investor demo remains 100% offline-capable and bulletproof.
2. **Deterministic Fail-Closed Safety:** Unsafe agrochemicals, out-of-scope emergencies, or adversarial attacks are blocked prior to generation.
3. **Two-Track Isolation:** Production code never reads paper/research artifacts at runtime, and research code never breaks production contracts.

---

## 2. Standing Quality & Release Gates

Before any branch merge, deployment, or demonstration, the following **Four Standing Gates** must pass with zero exceptions:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STANDING RELEASE GATES                              │
├──────────────────────┬──────────────────────────────────────────────────────┤
│ Gate 1: Unit Suite   │ 410+ Passed / 0 Failed / <= 7 Skipped (pytest)       │
├──────────────────────┼──────────────────────────────────────────────────────┤
│ Gate 2: Golden Probe │ 50/50 Golden Replay Invariants Verified Green        │
├──────────────────────┼──────────────────────────────────────────────────────┤
│ Gate 3: Frontend     │ `pnpm build` Clean (TypeScript + Next.js App Router) │
├──────────────────────┼──────────────────────────────────────────────────────┤
│ Gate 4: Two-Track    │ Zero runtime dependency on paper/ or experiments/    │
└──────────────────────┴──────────────────────────────────────────────────────┘
```

### Gate 1: Comprehensive Backend Test Suite
* **Command:** `pytest backend/tests/ -q`
* **Pass Threshold:** All 51 test suites pass with 0 failures.
* **Environmental Exemption:** Live server tests in `scripts/test_live_e2e.py` (requires running FastAPI process) are evaluated only in live staging environments.

### Gate 2: Golden Replay Invariant Verification (50/50)
* **Command:** `pytest backend/tests/test_golden_invariants.py`
* **Invariants Enforced:**
  1. *Out-of-corpus queries:* 100% routed to deterministic refusal/escalation (16123).
  2. *Banned chemicals (Paraquat, Carbofuran, etc.):* 100% fail-closed block at Tier 0.
  3. *Dialect inputs:* Preserved across standard, colloquial, and Banglish registers.
  4. *Approved dosages:* Match exact authorized BARI/BRRI table bounds without hallucination.

### Gate 3: Frontend Production Build
* **Command:** `pnpm --filter frontend build` (or Next.js production build check)
* **Invariants Enforced:** Zero TypeScript compilation errors, dynamic import validation, zero hydration mismatches, Motion animations properly tree-shaken.

### Gate 4: Two-Track Strict Isolation
* **Production Code Root:** `backend/app/`, `frontend/app/`, `supabase/`
* **Invariant:** Application code must **NEVER** import or read from `paper/`, `experiments/`, or `research_artifacts/` at runtime. All ML models, RAG indexes, and fact bases must reside under `backend/ml_assets/`.

---

## 3. Five-Tier Resolution Ladder & Safety Contract

The operational core operates strictly on the Five-Tier Resolution Ladder (R-series architecture):

```
Farmer Query (Bengali / Dialect / Vision)
                 │
                 ▼
 ┌──────────────────────────────────────────────────────────┐
 │ Tier 0: Safety & Scope Pre-Screen (Deterministic Regex)  │ ── [Unsafe / Poison / Ban] ──► Redirect (16123)
 └──────────────────────────────────────────────────────────┘
                 │ (Safe Agricultural Query)
                 ▼
 ┌──────────────────────────────────────────────────────────┐
 │ Tier 1: Exact / Cache Lookup (SQLite / SHA-256)          │ ── [Cache Hit] ──────────────► Certified Output (0 LLM)
 └──────────────────────────────────────────────────────────┘
                 │ (Cache Miss)
                 ▼
 ┌──────────────────────────────────────────────────────────┐
 │ Tier 2: Structured Fact-Base Resolver (11-Slot Relational)│ ── [Fact Found] ─────────────► Certified Output (0 LLM)
 └──────────────────────────────────────────────────────────┘
                 │ (Complex / Colloquial Query)
                 ▼
 ┌──────────────────────────────────────────────────────────┐
 │ Tier 3: Hybrid RAG + Grounded LLM Generation + Verifier  │ ── [Verified Bounds] ────────► Streamed Advisory
 └──────────────────────────────────────────────────────────┘
                 │ (Unresolvable / Missing Evidence)
                 ▼
 ┌──────────────────────────────────────────────────────────┐
 │ Tier 4: Fail-Closed Extension Escalation (Krishi 16123)  │ ──► Structured Extension Referral Ticket
 └──────────────────────────────────────────────────────────┘
```

### Safety Invariants (Never Compromised)
1. **Deterministic Precedence:** Tier 0 runs before any retrieval or LLM inference.
2. **Single-Record Joint Binding:** Verifiers reject composite citations where crop, active ingredient, dosage, and pre-harvest intervals do not originate from the same verified record hash.
3. **Modal Disagreement Fail-Safe:** If text crop identity disagrees with visual classifier prediction ($H > 0.3$ bits entropy), Tier 3 is blocked and a clarification badge is triggered.

---

## 4. Dark-Launch & Feature Flag Governance

| Flag Name | Default State | Purpose | Conditions to Enable |
|---|:---:|---|---|
| `DEMO_MODE` | `true` | Enables zero-auth offline demo flow with simulated network fallbacks | Always `true` for public showcases |
| `STRUCTURED_RESOLVER_ENABLED` | `true` | Enables Tier 1 & 2 zero-LLM deterministic fact-base resolution | Active in staging & production |
| `CHUNK_FALLBACK_ENABLED` | `false` | Fallback to raw institutional MD text chunks prior to Tier 4 refusal | Keep `false` until experiment E26 formal review |
| `ADMIN_PORTAL_ENABLED` | `true` | Enables role-verified admin monitoring console (`profiles.role='admin'`) | Active; strictly fail-closed |

---

## 5. Maintenance Procedures & Routine Verification Schedule

```
┌─────────────────────────┬───────────────────────────────────┬────────────────────────────────────────┐
│ Cadence                 │ Action Item                       │ Verification Method                    │
├─────────────────────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ Pre-Commit / Pre-Push   │ Run test suite + static audit     │ `pytest backend/tests/`                │
│ Weekly / Pre-Demo       │ Run full golden replay (50/50)    │ `test_golden_invariants.py`            │
│ Regulatory Update       │ Ingest new Gazette / BARI facts   │ `python scripts/ingest_fact_base.py`   │
│ Hash Verification       │ Recompute ML asset SHA-256        │ `python scripts/verify_asset_hashes.py`│
└─────────────────────────┴───────────────────────────────────┴────────────────────────────────────────┘
```

### Protocol for Adding New Verified Agronomic Facts
1. Authoring is a **data operation, never a code rewrite**.
2. Add verified entries to `backend/ml_assets/rag_index/fact_base.sqlite` with full 11-slot metadata, author ID, and gazette year.
3. Run `pytest backend/tests/test_fact_base.py` to confirm dose bounds and provenance integrity.

---

## 6. Emergency Safe Rollback Protocol

If an unexpected regression or runtime failure occurs during demonstration or production:

1. **Immediate Fallback to Demo Mode:**
   ```bash
   # In .env:
   DEMO_MODE=true
   CHUNK_FALLBACK_ENABLED=false
   ```
2. **Deterministic Resolver Priority:**
   The SQLite fact base (`T1/T2`) operates in-process with zero external network or LLM dependencies, ensuring 100% uptime for core crops (Rice, Potato, Tomato, Maize, Wheat).
3. **Fail-Closed Guarantee:**
   If any exception occurs in LLM serving or retrieval, the exception envelope catches the error and safely presents the **Krishi 16123 helpline redirect**, preventing hazardous hallucination.
