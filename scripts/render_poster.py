#!/usr/bin/env python3
"""CLI entrypoint for hiccai-commercial-poster: render single posters or multi-family contact sheets."""

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from poster_engine import (  # noqa: E402
    ALL_ARCHITECTURES,
    COLOR_BLOCK_ARCHITECTURES,
    CURATED_CN_ARCHITECTURES,
    FULL_BLEED_ARCHITECTURES,
    PROTECTED_ARCHITECTURES,
    Typesetter,
    compose_editorial_poster,
)

RATIO_SIZES = {
    "3:4": (1080, 1440),
    "4:5": (1080, 1350),
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
    "16:9": (1920, 1080),
    "4:3": (1440, 1080),
}

PRESET_GROUPS = {
    "curated_cn": list(CURATED_CN_ARCHITECTURES),
    "fullbleed": [
        "fresh_retail_promo",
        "social_sticker_zine",
        "neon_highlighter_poster",
        "oriental_vertical_frame",
        "full_bleed_clean",
        "full_bleed_poster_type",
    ],
    "colorblock": list(COLOR_BLOCK_ARCHITECTURES),
    "editorial": ["ledger", "offset", "monument", "ribbon", "edge", "window", "diagonal_bleed", "diptych_focus"],
    "protected": list(PROTECTED_ARCHITECTURES),
    "all": list(ALL_ARCHITECTURES),
}


def render_one(size, photo, ts, brand, copy, *, seed, family, protect_subject, accent_color):
    kit = {"color": accent_color} if accent_color else None
    scene, layer, box, recipe = compose_editorial_poster(
        size,
        photo,
        ts,
        brand,
        copy,
        seed_text=seed,
        protected_subject=protect_subject,
        kit=kit,
        architecture=family if family and family != "auto" else None,
    )
    out = Image.alpha_composite(scene.convert("RGBA"), layer).convert("RGB")
    return out, recipe


def build_contact_sheet(images, dest_path, cols=4, tile_max=540, pad=24):
    if not images:
        return
    w0, h0 = images[0].size
    scale = tile_max / max(w0, h0)
    tw, th = max(1, round(w0 * scale)), max(1, round(h0 * scale))
    cols = min(cols, len(images))
    rows = math.ceil(len(images) / cols)
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, rows * th + (rows + 1) * pad), (18, 19, 21))
    for i, img in enumerate(images):
        r, c = divmod(i, cols)
        sheet.paste(img.resize((tw, th), Image.Resampling.LANCZOS), (pad + c * (tw + pad), pad + r * (th + pad)))
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest_path, quality=93)


def main():
    parser = argparse.ArgumentParser(description="hiccai-commercial-poster 24-family commercial poster renderer")
    parser.add_argument("--list-families", action="store_true", help="List all 24 layout families and presets")
    parser.add_argument("--photo", help="Path to hero product/scene image (omit for pure typographic poster)")
    parser.add_argument("--brand", default="", help="Brand or store name")
    parser.add_argument("--title", default="", help="Primary headline (8-18 chars social currency hook)")
    parser.add_argument("--subtitle", default="", help="Secondary subtitle (<=20 chars product/offer proof)")
    parser.add_argument("--cta", default="", help="Commercial closing call-to-action")
    parser.add_argument("--offer", default="", help="Confirmed price/offer (e.g. 29.9元/盒)")
    parser.add_argument("--terms", default="", help="Confirmed terms/expiry (optional)")
    parser.add_argument("--ratio", default="3:4", choices=sorted(RATIO_SIZES), help="Poster aspect ratio")
    parser.add_argument("--family", default="auto", help="Specific family ID or 'auto'")
    parser.add_argument("--preset", choices=sorted(PRESET_GROUPS), help="Render a curated group of families")
    parser.add_argument("--seed", default="poster-v1", help="Deterministic parametric seed")
    parser.add_argument("--accent-color", default="", help="Optional hex brand color override (e.g. #B8292F)")
    parser.add_argument("--custom-font", default="", help="Optional path to custom TTF/OTF font")
    parser.add_argument("--protect-subject", action="store_true", help="Never crop merchant real product photo")
    parser.add_argument("--output", help="Output PNG/JPG path (single render mode)")
    parser.add_argument("--output-dir", help="Output directory for batch/preset individual renders")
    parser.add_argument("--sheet", help="Optional contact sheet JPG path when rendering a preset group")
    args = parser.parse_args()

    if args.list_families:
        print(
            json.dumps(
                {
                    "total": len(ALL_ARCHITECTURES),
                    "full_bleed_families": list(FULL_BLEED_ARCHITECTURES),
                    "color_block_families": list(COLOR_BLOCK_ARCHITECTURES),
                    "curated_cn_families": list(CURATED_CN_ARCHITECTURES),
                    "protected_safe_families": list(PROTECTED_ARCHITECTURES),
                    "all_families": list(ALL_ARCHITECTURES),
                    "presets": PRESET_GROUPS,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if not args.title:
        parser.error("--title is required unless --list-families is specified")

    photo = Image.open(args.photo).convert("RGB") if args.photo else None
    size = RATIO_SIZES[args.ratio]
    ts = Typesetter(custom=args.custom_font or None)
    copy = {
        "title": args.title,
        "body": args.subtitle,
        "cta": args.cta,
        "offer": args.offer,
        "terms": args.terms,
    }

    if args.preset:
        fams = PRESET_GROUPS[args.preset]
        if args.protect_subject:
            fams = [f for f in fams if f in PROTECTED_ARCHITECTURES] or list(PROTECTED_ARCHITECTURES)
        out_dir = Path(args.output_dir) if args.output_dir else None
        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
        images = []
        summary = []
        for idx, fam in enumerate(fams):
            img, rec = render_one(
                size,
                photo,
                ts,
                args.brand,
                copy,
                seed=f"{args.seed}-{fam}-{idx}",
                family=fam,
                protect_subject=args.protect_subject,
                accent_color=args.accent_color,
            )
            images.append(img)
            saved = ""
            if out_dir:
                fp = out_dir / f"{idx + 1:02d}_{fam}_{args.ratio.replace(':', 'x')}.png"
                img.save(fp)
                saved = str(fp)
            summary.append(
                {
                    "family": rec["architecture"],
                    "taste": rec["taste"],
                    "titleContrast": rec["titleContrast"],
                    "file": saved,
                }
            )
        if args.sheet:
            cols = 3 if len(images) in (3, 6) else 4 if len(images) >= 4 else len(images)
            build_contact_sheet(images, Path(args.sheet), cols=cols)
        print(json.dumps({"count": len(summary), "sheet": args.sheet or "", "items": summary}, ensure_ascii=False, indent=2))
        return

    if not args.output:
        parser.error("--output is required for single-poster mode (or use --preset)")

    img, rec = render_one(
        size,
        photo,
        ts,
        args.brand,
        copy,
        seed=args.seed,
        family=args.family,
        protect_subject=args.protect_subject,
        accent_color=args.accent_color,
    )
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(
        json.dumps(
            {
                "output": str(out_path),
                "ratio": args.ratio,
                "size": list(size),
                "family": rec["architecture"],
                "taste": rec["taste"],
                "titleContrast": rec["titleContrast"],
                "bodyContrast": rec["bodyContrast"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
