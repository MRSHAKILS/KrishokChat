# N05 — SMS Survival (LOCKED, critic-audited)

**Status:** REAL_MEASURED · **Results:** `results_offline.json` (n=300), `results_live.json` (n=100)

- Offline: 299/300 ok (1 correct schema rejection), 0 over-160, 44/44 unsafe→referral.
- Live: 100/100 ok, 0 over-160; taxonomy post-fix is **75 verified advice + 9 flagged referrals + 16 blocked referrals**; safe SMS carry structure but 0/84 dose patterns (truncation drops fields — packer pending); referral purity holds; all texts non-GSM7 (characters, never segments).
- SMS guard fix (flagged→referral) proven on 9/9 flips incl. the brinjal case (157ch advice → 97ch referral). Pre-guard outputs archived as `_v1`.
