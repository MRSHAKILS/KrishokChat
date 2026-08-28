# Figure & Image Generation Prompts — KrishokChat Innovation Dossier

Every visual referenced by `main.tex` is listed here. The LaTeX compiles today with
**blank placeholder boxes** (via `\IfFileExists`). When you generate/drop the real
asset at the exact path below, the box is automatically replaced — no LaTeX edit needed.

- Place **conceptual illustrations** in `figures/`
- Place **real product screenshots** in `screenshots/`
- Charts (`slot_ablation`, `network`, `efficiency`, etc.) are drawn natively in LaTeX
  with `pgfplots` from `data/canonical_numbers.yaml`, so they need **no** image file.

Consistent prompt prefix for all generated conceptual illustrations:

> Premium editorial illustration for a Bangladesh national innovation dossier,
> A4-oriented composition with a clear widescreen-safe center area, authentic
> Bangladeshi agricultural environment, restrained deep agricultural green
> (#1E5E3A) and warm earth (#B87333) palette, realistic human proportions,
> documentary rather than futuristic, clean negative space, no logos, no
> watermark, no fake statistics, no decorative text.

---

## Conceptual illustrations (`figures/`)

### `figures/cover_field.png`  — Cover hero
`<prefix>` + "A smallholder farmer standing in a green Bangladeshi crop field at
soft morning light, holding a basic smartphone, mid-shot, hopeful and grounded,
space at the top for a title overlay."

### `figures/field_origin.png` — Page 3 origin
`<prefix>` + "Researcher in the field talking with two farmers beside a diseased
crop plant, notebook in hand, genuine field-interview moment, documentary tone."

### `figures/ecosystem_bg.png` — Page 33 commercial model (optional background)
`<prefix>` + "Abstract, very subtle background suggesting a network connecting a
farmer, an extension office, an NGO and a government building, faint line work,
mostly negative space, suitable to place text on top."

### `figures/closing_system.png` — Closing page
`<prefix>` + "Wide serene view of Bangladeshi farmland at dusk with a faint
overlaid impression of a phone screen, quiet and confident, room for one line of text."

---

## Real product screenshots (`screenshots/`)

Capture from the live KrishokChat UI. Do **not** fabricate.

| File | What to capture |
|------|-----------------|
| `screenshots/farmer_home.png` | Landing / home page of the PWA |
| `screenshots/bengali_chat.png` | A Bengali conversation turn |
| `screenshots/agent_trace.png` | The animated agent-trace stepper (Safety → Retrieve → Generate → Verify) |
| `screenshots/evidence.png` | Evidence / source-citation panel with page provenance |
| `screenshots/vision.png` | Crop-image diagnosis result view |
| `screenshots/conflict.png` | Cross-modal conflict clarification prompt |
| `screenshots/safety_block.png` | A blocked unsafe query with the 16123 redirect |
| `screenshots/offline.png` | Offline / cached-state indicator |
| `screenshots/admin.png` | Analytics / safety-metrics / health panel |
| `screenshots/sms.png` | SMS export / compressed template preview |

---

## Charts drawn natively in LaTeX (no image needed)

These are rendered by `pgfplots`/`tikz` directly in `main.tex` from verified numbers:

- Slot-ablation hazard hierarchy (horizontal bar)
- Counterfactual certification comparison (bar)
- Retrieval degradation hazard (grouped bar)
- Generator-independent safety boundary (grouped bar)
- Dialect coverage lift (paired bar)
- Network resilience (grouped bar)
- Efficiency workload distribution (stacked/segmented bar)
- All system/flow diagrams (TikZ)
