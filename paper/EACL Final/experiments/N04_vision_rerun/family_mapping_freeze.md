# Router Family-Mapping Freeze (preregistered BEFORE scoring — 2026-09-17)

Species prediction → family truth mapping for the 10-class router. Frozen here;
scoring script reads this file (no post-hoc adjustments).

- Cabbage → Brassica; Cauliflower → Brassica
- Chili → Solanacea; Tomato → Solanacea; Eggplant → Solanacea; Potato → Solanacea
- Gourd → GourdGuava; Guava → GourdGuava
- Rice → Rice
- Others → unmapped (excluded, counted)
- Wheat truth rows → out-of-space (no router class; excluded, counted)

Rule: mapped-correct iff mapped prediction == manifest family truth.
Report alongside (never instead of) the exact-match 0.0259.
