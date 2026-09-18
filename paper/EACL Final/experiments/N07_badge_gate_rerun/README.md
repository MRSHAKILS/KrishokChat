# N07 — Badge Gate, User Path (LOCKED, critic-audited)

**Status:** REAL_MEASURED · **Result:** `results.json` (54 pairs + amendment with sole-miss record)

Mismatch halt **53/54 (98.15%)**, control false-halt **0/54** on farmer pairs plus **400/400 (100% [99.05, 100.0])** on PRISM pairs (combined 453/454 with 0 false-halts), on the QAInput cross-modal path with real farmer queries. Sole miss (farmer_q_63): implicit-crop query with no text token to contradict — design boundary, counted as miss. Explicit-text contradiction only; not general image-text mismatch; independent of CEA E31.
