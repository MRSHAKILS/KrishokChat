# 01 — Edge Optimization (on-device, offline, low-bandwidth)

**Parent:** `00_SCOPE_OUTLINE.md` (scopes U1–U6, F2/F3, spine steps 1 & 5)
**Status:** PLANNING — no code changes.
**Constraint from the researcher:** must run on a cheap phone (2–4 GB RAM) on a bad connection.

---

## 1. The honest edge reality (2026)

| Component | On-device viable? | Verdict |
|---|---|---|
| Crop + disease **image classifiers** (INT8 `.tflite`, ≤6 MB each) | **Yes** — <150 ms on a 2–4 GB phone | **BUILD (U1)** — flagship |
| **Safety/router classifier** (tiny text model / rules) | Yes — small footprint | Build later (offline safety) |
| **Generative Bengali LLM** (answer generation) | **No** — Gemma 3 4B needs ~2.8 GB peak RAM, crashes ~15% of 6 GB devices ([MVP Factory 2026](https://mvpfactory.io/blog/running-gemma-3-on-device-in-production-memory-budgets-quant/)) | **KEEP SERVER-SIDE** — do not claim on-device chat |

**Rule:** diagnosis on the phone, generation in the cloud. Never advertise on-device generative Bengali chat on this hardware — it is hype and it will crash the demo.

---

## 2. U1 — On-device INT8 image diagnosis (flagship, build first)

- **Source artifacts:** existing Ultralytics `.pt` crop classifier + per-crop disease classifiers (potato, rice, wheat, corn, brassica). Current task is `classify` — keep it honest, no boxes.
- **Conversion:** `.pt` → LiteRT/TFLite with post-training INT8 quantization. Target ≤6 MB/model.
- **Runtime target:** <150 ms inference on a 2–4 GB Android phone; two-stage (crop → disease) is already edge-friendly (small sequential models).
- **Acceptance gate:** on-device accuracy must stay within ~1.5% of the server model on the held-out set, else fall back to server inference for that crop.
- **Fallback:** if the device is too weak / model missing, silently use the existing server `/detect` route. Additive, never breaks the demo.

## 3. U3 — Confidence-gated upload + client-side compression

- Run the classifier locally first. If top-1 confidence ≥ threshold → resolve **on-device, zero data used**.
- If ambiguous (below threshold, or crop-unknown) → compress (resize → WebP, strip EXIF) and upload only then.
- **Demo/paper metric:** "% of diagnoses resolved without touching the server" and "avg KB uploaded per diagnosis." Quantifiable, defensible bandwidth story. No competitor reports this.

## 4. U2 — Offline-first PWA shell

- Service worker + app-shell caching; IndexedDB for the `.tflite` model cache and last-N advisories.
- Airplane-mode capable: cached advisories, the image-diagnosis queue, and the **16123 redirect** all work with no signal.
- Matches the proven BD pattern (Krishoker Janala offline modules, iFarmer Folon offline audio/video).
- Optional later: **Capacitor** wrapper for Play Store distribution + reliable native camera.

## 5. U5 — Voice (server-side, not edge)

- Bengali ASR in (`bn-BD`) + TTS out. This is a *usability* win (see `05_FRONTEND_REFINEMENT.md`), not an edge win — keep it server-side. Listed here only to mark the boundary: do **not** try to run Bengali ASR/TTS on-device.

## 6. U6 — SMS/USSD fallback

- **Deferred to v2.** Regulated TVAS in Bangladesh — needs a BTRC-enrolled aggregator + short code. Not a prototype build. Frame as a partnership on the roadmap, not something we ship ourselves.

---

## 7. Suggested edge build order (all additive, switch-gated, reversible)

1. INT8 export of **potato + crop** classifiers, accuracy-gated (spine step 1).
2. Confidence-gated upload + WebP compression on `/detect` client (U3).
3. Offline PWA shell + model caching (U2) — pairs with frontend F2/F3.
4. Extend export to maize/rice/wheat/brassica classifiers.
5. (Later) On-device safety classifier for fully-offline refusal + 16123.
6. (v2) Capacitor wrapper; (v2) SMS/USSD partnership.

## 8. Guardrails

- No on-device generative LLM claim.
- On-device model must not diverge >1.5% from server model, or fall back.
- Anonymous / `DEMO_MODE=true` path unchanged; everything additive.
- No new required env var without updating `.env.example`.
