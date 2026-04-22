from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont


FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def contains_cjk(text: str | None) -> bool:
    if not text:
        return False
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def load_font(
    size: int,
    bold: bool = False,
    font_path: str | None = None,
    prefer_cjk: bool = False,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if font_path:
        candidates.append(font_path)
    if prefer_cjk:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Songti.ttc",
                "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            ]
        )
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf",
            ]
        )
    candidates.extend(FONT_CANDIDATES)
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    if not text:
        return []
    lines: list[str] = []
    current = ""
    for char in text:
        probe = current + char
        bbox = draw.textbbox((0, 0), probe, font=font)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = probe
            continue
        lines.append(current)
        current = char
    if current:
        lines.append(current)
    return lines


def fit_multiline_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_height: int,
    max_font_size: int,
    min_font_size: int,
    line_spacing: float = 1.15,
    font_path: str | None = None,
    bold: bool = False,
    prefer_cjk: bool = False,
) -> tuple[ImageFont.ImageFont, list[str]]:
    for size in range(max_font_size, min_font_size - 1, -2):
        font = load_font(size=size, bold=bold, font_path=font_path, prefer_cjk=prefer_cjk)
        lines = wrap_text(draw, text, font, max_width)
        line_height = max(1, int(size * line_spacing))
        total_height = line_height * max(1, len(lines))
        widest = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            widest = max(widest, bbox[2] - bbox[0])
        if widest <= max_width and total_height <= max_height:
            return font, lines
    font = load_font(size=min_font_size, bold=bold, font_path=font_path, prefer_cjk=prefer_cjk)
    return font, wrap_text(draw, text, font, max_width)


def rounded_panel(image: Image.Image, box: tuple[int, int, int, int], fill: tuple[int, int, int, int], radius: int) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def paste_contained_rgba(base: Image.Image, overlay: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    width = max(1, x1 - x0)
    height = max(1, y1 - y0)
    copy = overlay.convert("RGBA")
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)
    paste_x = x0 + (width - copy.width) // 2
    paste_y = y0 + (height - copy.height) // 2
    base.alpha_composite(copy, dest=(paste_x, paste_y))
    return paste_x, paste_y, paste_x + copy.width, paste_y + copy.height


def safe_pad_resize(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    source = image.convert("RGBA")
    background = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(radius=max(8, target_width // 120)))
    dimmer = Image.new("RGBA", (target_width, target_height), (245, 242, 236, 76))
    background.alpha_composite(dimmer)

    contained = source.copy()
    contained.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 0))
    offset = ((target_width - contained.width) // 2, (target_height - contained.height) // 2)
    canvas.alpha_composite(background, dest=(0, 0))
    canvas.alpha_composite(contained, dest=offset)
    return canvas


def cover_crop_resize(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    source = image.convert("RGBA")
    ratio = max(target_width / source.width, target_height / source.height)
    resized = source.resize(
        (max(1, int(math.ceil(source.width * ratio))), max(1, int(math.ceil(source.height * ratio)))),
        Image.Resampling.LANCZOS,
    )
    left = max(0, (resized.width - target_width) // 2)
    top = max(0, (resized.height - target_height) // 2)
    return resized.crop((left, top, left + target_width, top + target_height))


def parse_size(size: str) -> tuple[int, int]:
    normalized = size.lower().replace(" ", "")
    if "x" not in normalized:
        raise ValueError(f"invalid size: {size}")
    width_text, height_text = normalized.split("x", 1)
    width = int(width_text)
    height = int(height_text)
    if width <= 0 or height <= 0:
        raise ValueError(f"invalid size: {size}")
    return width, height


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def serialize_box(box: tuple[int, int, int, int]) -> dict[str, int]:
    x0, y0, x1, y1 = box
    return {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}


def source_from_version(bundle_root: Path, version_record: dict[str, Any]) -> Path:
    return bundle_root / version_record["asset_path"]
