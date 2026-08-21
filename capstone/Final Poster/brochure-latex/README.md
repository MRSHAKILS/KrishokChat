# KrishokChat A3 Bi-fold Brochure

This directory contains the editable A3 bi-fold LaTeX source for the four-panel judge handout.

## Physical format

- Compile to **two A3 landscape PDF pages**.
- Print page 1 and page 2 double-sided.
- Fold once vertically at the centre.
- Page 1 is the outside: left = back cover, right = front cover.
- Page 2 is the inside: left = field-to-research story, right = product/safety flow.

This follows the established CTAN `latex-brochure` A3 bi-fold pattern, but uses a local article/geometry implementation so all content remains easy to edit.

## Compile

```powershell
lualatex -interaction=nonstopmode krishokchat-brochure.tex
lualatex -interaction=nonstopmode krishokchat-brochure.tex
```

LuaLaTeX is the currently practical local compiler because the installed MiKTeX
XeLaTeX executable exits with an internal error before processing the source.
The content and layout are engine-neutral; re-run with XeLaTeX in a clean TeX
installation if the print vendor requires it.

The source uses fonts already present in `capstone/poster-design/latex/fonts/` when available. If a local font is unavailable, XeLaTeX will fall back to a system font.

## Asset workflow

1. Existing screenshots are loaded from `demo-assets/screenshots/` and can be replaced by final captures.
2. Existing field/interview assets are loaded from `capstone/poster-design/latex/img/`.
3. Generated diagrams belong in `assets/generated/`.
4. The source intentionally provides a labelled placeholder when a generated diagram is not yet present.
5. Exact prompts and diagram specifications are in `../VISUAL_GENERATION_PROMPTS.md`.

## Important content rule

The brochure is positive and product-facing, but it distinguishes:

- **measured research evidence**;
- **working application behavior**;
- **field dataset contribution**;
- **pilot/deployment pathway**.

It does not present unmeasured or unimplemented capabilities as completed facts. This keeps the brochure promotional and defensible when an industry judge asks a follow-up question.
