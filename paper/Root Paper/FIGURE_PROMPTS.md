# Figure prompts for poster variants

These prompts are for poster/communication artwork only. The manuscript figures should remain data-driven and should use the reconciled YAML values. Do not ask an image model to invent metric labels or draw unverified field scenes.

## Figure 1 — Architecture poster

> Create a clean scientific systems-engineering diagram for a low-resource Bengali agricultural advisory prototype. Show three inputs on the left: crop photograph, Bengali/romanized text, and feature-phone SMS. Route the photograph through an on-device crop/disease **classifier** that emits structured crop and pest metadata. Show this metadata bypassing ordinary text retrieval and entering a deterministic fact-base lookup. Show a separate text-first fallback path for low-confidence or no-image cases. Both paths enter a typed fail-closed certification gate that checks chemical, formulation, dose, unit, volume, interval, pre-harvest interval, crop, pest, stage, and regulatory status against one evidence record. Show an optional LLM fallback outside the primary deterministic path. On the right, show online PWA, offline local cache, and GSM SMS outputs, plus a human escalation arrow to Bangladesh Krishi Call Center 16123. Use restrained teal, dark slate, green, amber, and red; white background; flat vector style; no decorative farm imagery; no invented percentages; label the research-only boundary clearly.

## Figure 2 — DGDR decision flow poster

> Create a publication-quality decision-flow diagram titled “Detection-Gated Deterministic Routing”. Start with “Input image available?” and show the no-image branch going to text-first fallback. On the image branch, show “on-device classification: crop, pest, confidence” followed by the decision “confidence ≥ γ”. Annotate γ = 0.80, mean fact-base search space 2,135 → 516.4 nodes, 13.55% fallback, and 3.15% measured misrouting. The accepted branch goes to “deterministic ≤3-hop fact lookup”; the fallback branch goes to “text-first retrieval / optional generation”. Both converge at “typed fail-closed certification”; failure leads to “abstain / 16123”. Use clear arrows, accessible typography, no claims of dialect immunity, no bounding boxes, and no imagery beyond a small neutral crop-photo icon.

## Figure 3 — Coverage and safety panel

> Create a two-panel scientific chart, not an infographic. Panel A compares text-first coverage with detection-gated coverage for Standard Bengali, Authentic Farmer, Regional Dialects, and Romanized Banglish. Label the endpoint explicitly as “coverage / non-abstention in the tested suite”, not accuracy. Panel B shows the observed dangerous-acceptance count as zero for the four registers, with a note that Wilson upper bounds are nonzero and that the suites are not a full factorial deployment test. Use exact values only from the reconciled E21 YAML; do not synthesize missing confidence intervals.

## Figure 4 — Network stress-test panel

> Create a grouped bar chart for the four named simulated profiles: Perfect 4G (0% loss), Urban 3G (5%), Rural Edge (15%), and Severe 2G (30%). For each profile show cloud-only RAG and offline-first cache delivery. Every bar must display its exact value from the reconciled E14 result artifact. Add a subtitle “controlled network simulation; not a carrier or field trial”. Do not interpolate a curve between profiles and do not mix values from different E14 revisions.

## Figure 5 — GSM slot-survival strip

> Create a compact heatmap with rows “Deterministic template”, “LLM-composed control”, and “Naive truncation”, and columns crop, pest, active ingredient, formulation, dose, unit, volume, interval, PHI, and helpline. Display survival percentages from the reconciled E15 YAML. Highlight the PHI column with a thin outline, but do not use alarmist imagery. Caption the figure as tested field survival inside a GSM-160 composition budget, not live carrier delivery.
