#!/usr/bin/env python3
"""
Crop a resume headshot to a fixed portrait size.

Default output size is 540x790 px, matching the PDF photo frame ratio used by
markdown_resume_to_pdf.py. The script fits the source portrait into a fixed
canvas with a small safe padding, so the exported resume can use a stable fixed
photo box without cutting off the portrait, rounded corners, or page-edge pixels.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


DEFAULT_WIDTH = 540
DEFAULT_HEIGHT = 790


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Center-crop a resume headshot to a fixed portrait size."
    )
    parser.add_argument("input", type=Path, help="Source headshot image path.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output image path. Defaults to <input-stem>_cropped.png.",
    )
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Output width in px.")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Output height in px.")
    parser.add_argument(
        "--padding-ratio",
        type=float,
        default=0.06,
        help="White safe padding around the portrait, as a ratio of the shorter side.",
    )
    return parser.parse_args()


def fit_to_canvas(
    image: Image.Image,
    target_width: int,
    target_height: int,
    padding_ratio: float,
) -> Image.Image:
    padding = max(0, round(min(target_width, target_height) * padding_ratio))
    inner_width = max(1, target_width - 2 * padding)
    inner_height = max(1, target_height - 2 * padding)

    fitted = ImageOps.contain(image, (inner_width, inner_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_width, target_height), "white")
    left = (target_width - fitted.width) // 2
    top = (target_height - fitted.height) // 2
    canvas.paste(fitted, (left, top))
    return canvas


def main() -> int:
    args = parse_args()
    if args.width <= 0 or args.height <= 0:
        raise SystemExit("Error: --width and --height must be positive integers.")
    if not args.input.exists():
        raise SystemExit(f"Error: input image not found: {args.input}")

    output = args.output or args.input.with_name(f"{args.input.stem}_cropped.png")
    if args.padding_ratio < 0 or args.padding_ratio >= 0.25:
        raise SystemExit("Error: --padding-ratio must be between 0 and 0.25.")

    image = ImageOps.exif_transpose(Image.open(args.input)).convert("RGB")
    fitted = fit_to_canvas(image, args.width, args.height, args.padding_ratio)
    fitted.save(output)

    print(f"Photo written: {output}")
    print(f"Size check: {args.width}x{args.height}px.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
