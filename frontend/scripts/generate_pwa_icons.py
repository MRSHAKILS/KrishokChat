"""Generate KrishokChat PWA icons (Field Notebook palette).

Reproducible asset generator — run from the repo root:
    uv run --project backend python frontend/scripts/generate_pwa_icons.py

Outputs to frontend/public/:
    icon-192.png / icon-512.png          (purpose "any": rounded square, transparent padding)
    icon-maskable-192.png / icon-maskable-512.png
                                          (purpose "maskable": full-bleed, glyph in safe zone)

Design: deep leaf-green (#2F5D3A, manifest theme_color) field with the Bengali
monogram "ক" (কৃষক) set in Nirmala UI (Windows system font) in paper
(#FDFBF7) with a small ochre seed dot. If Nirmala UI is unavailable
(non-Windows), falls back to a pointed-oval leaf glyph so the script still runs.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LEAF = (47, 93, 58, 255)       # #2F5D3A — theme_color
PAPER = (253, 251, 247, 255)   # #FDFBF7 — background_color
OCHRE = (200, 137, 60, 255)    # #C8893C — accent

CANVAS = 2048
NIRMALA = Path("C:/Windows/Fonts/Nirmala.ttc")


def draw_icon(maskable: bool) -> Image.Image:
    img = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    inset = 0 if maskable else int(CANVAS * 0.04)
    radius = 0 if maskable else int(CANVAS * 0.22)
    d.rounded_rectangle(
        [inset, inset, CANVAS - inset, CANVAS - inset],
        radius=radius,
        fill=LEAF,
    )

    glyph_scale = 0.66 if maskable else 0.74  # keep maskable content in the ~80% safe zone

    if NIRMALA.exists():
        target = int(CANVAS * glyph_scale)
        font = ImageFont.truetype(str(NIRMALA), 400, index=0)
        # scale font so the glyph box hits the target size
        bbox = d.textbbox((0, 0), "ক", font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        font = ImageFont.truetype(str(NIRMALA), int(400 * target / max(w, h)), index=0)
        bbox = d.textbbox((0, 0), "ক", font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        cx, cy = CANVAS / 2 - w / 2 - bbox[0], CANVAS / 2 - h / 2 - bbox[1] - CANVAS * 0.015
        d.text((cx, cy), "ক", font=font, fill=PAPER)
        # ochre seed dot at the glyph's lower right
        r = CANVAS * 0.030
        dx, dy = cx + bbox[0] + w + CANVAS * 0.035, cy + bbox[1] + h - r * 0.6
        d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=OCHRE)
    else:
        _draw_leaf(d, glyph_scale)
    return img


def _draw_leaf(d: ImageDraw.ImageDraw, glyph_scale: float) -> None:
    size = CANVAS * glyph_scale
    cx, cy = CANVAS / 2, CANVAS / 2
    base = (0.0, -size / 2)
    tip = (0.0, size / 2)
    w = size * 0.38

    def q(p0, c, p1, steps=64):
        return [
            (
                (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t**2 * p1[0],
                (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t**2 * p1[1],
            )
            for t in (i / steps for i in range(steps + 1))
        ]

    right = q(base, (w, 0.0), tip)
    left = q(tip, (-w, 0.0), base)
    a = math.radians(45)
    ca, sa = math.cos(a), math.sin(a)
    poly = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in right + left]
    d.polygon(poly, fill=PAPER)


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "public"
    for maskable, name in ((False, "icon"), (True, "icon-maskable")):
        base = draw_icon(maskable)
        for size in (192, 512):
            base.resize((size, size), Image.LANCZOS).save(out / f"{name}-{size}.png")
            print(f"wrote {out / f'{name}-{size}.png'}")


if __name__ == "__main__":
    main()
