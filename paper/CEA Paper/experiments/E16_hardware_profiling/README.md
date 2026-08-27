# Layer E16_hardware_profiling: On-Device Hardware & Battery Profiling

**Status:** PLANNED / SPECIFIED (Pending Execution)  
**Research Question:** RQ5  
**Target Venue:** *Computers and Electronics in Agriculture* (Elsevier)  

---

## 1. Scientific Motive & Objective
**Core Question:** Battery drain, memory footprint, and thermal profile of on-device INT8 ONNX + cached Tier 1/2 on sub-$120 Android hardware?  
**Motive:** Validate real physical deployment viability on low-cost devices (Redmi A2 / Walton / Symphony) without cloud dependence.  

## 2. Experimental Protocol
- **Runner Script:** `scripts/run_e16.py`
- **Execution:** `python scripts/run_e16.py`
- **Target Endpoints / Hypotheses:**
  - Cold start latency < 150 ms
  - Warm inference < 35 ms
  - RAM < 75 MB
  - Battery drain < 0.15% per 100 queries

## 3. Results Placeholder
*Results will be populated upon execution and verification following ACCEPTANCE_PROTOCOL.md.*
