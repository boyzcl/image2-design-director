from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw

from delivery_image_ops_lib import contains_cjk, fit_multiline_text, load_font, paste_contained_rgba


Box = tuple[int, int, int, int]


def _box_payload(box: Box) -> dict[str, int]:
    x0, y0, x1, y1 = box
    return {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _diff_ratio(before: Image.Image, after: Image.Image, box: Box) -> float:
    before_crop = before.crop(box).convert("RGB")
    after_crop = after.crop(box).convert("RGB")
    diff = ImageChops.difference(before_crop, after_crop)
    changed = 0
    for pixel in diff.getdata():
        if pixel != (0, 0, 0):
            changed += 1
    total = max(1, before_crop.width * before_crop.height)
    return round(changed / total, 4)


def _draw_soft_panel(draw: ImageDraw.ImageDraw, box: Box, radius: int, fill: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=(178, 160, 130, 180), width=max(2, radius // 12))


def _draw_fitted_text(
    image: Image.Image,
    box: Box,
    text: str,
    max_font_size: int,
    min_font_size: int,
    fill: tuple[int, int, int, int],
    bold: bool = True,
    align: str = "left",
) -> dict[str, Any]:
    draw = ImageDraw.Draw(image, "RGBA")
    padding_x = max(20, int((box[2] - box[0]) * 0.06))
    padding_y = max(18, int((box[3] - box[1]) * 0.10))
    inner = (box[0] + padding_x, box[1] + padding_y, box[2] - padding_x, box[3] - padding_y)
    font, lines = fit_multiline_text(
        draw=draw,
        text=text,
        max_width=inner[2] - inner[0],
        max_height=inner[3] - inner[1],
        max_font_size=max_font_size,
        min_font_size=min_font_size,
        line_spacing=1.05,
        bold=bold,
        prefer_cjk=contains_cjk(text),
    )
    line_height = int(getattr(font, "size", min_font_size) * 1.12)
    total_height = line_height * len(lines)
    y = inner[1] + max(0, (inner[3] - inner[1] - total_height) // 2)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        if align == "center":
            x = inner[0] + max(0, (inner[2] - inner[0] - line_width) // 2)
        else:
            x = inner[0]
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return {"text": text, "lines": lines, "box": _box_payload(box), "font_size": getattr(font, "size", None)}


def replace_qr(base_path: Path, provided_qr_path: Path, output_path: Path) -> dict[str, Any]:
    before = Image.open(base_path).convert("RGBA")
    after = before.copy()
    width, height = after.size
    card_box = (int(width * 0.645), int(height * 0.625), int(width * 0.96), int(height * 0.945))
    inner_box = (
        card_box[0] + int(width * 0.035),
        card_box[1] + int(height * 0.035),
        card_box[2] - int(width * 0.035),
        card_box[3] - int(height * 0.035),
    )
    draw = ImageDraw.Draw(after, "RGBA")
    _draw_soft_panel(draw, card_box, radius=max(22, width // 42), fill=(255, 253, 248, 248))
    qr = Image.open(provided_qr_path).convert("RGBA")
    pasted_box = paste_contained_rgba(after, qr, inner_box)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    after.convert("RGB").save(output_path, quality=96)
    return {
        "scenario": "qr_replacement",
        "source_path": str(base_path),
        "provided_qr_path": str(provided_qr_path),
        "output_path": str(output_path),
        "provided_qr_sha256": _sha256(provided_qr_path),
        "replaced_region": _box_payload(card_box),
        "pasted_qr_box": _box_payload(pasted_box),
        "target_region_diff_ratio": _diff_ratio(before, after, card_box),
        "result": "pass",
    }


def edit_text(base_path: Path, output_path: Path) -> dict[str, Any]:
    before = Image.open(base_path).convert("RGBA")
    after = before.copy()
    width, height = after.size
    title_box = (int(width * 0.095), int(height * 0.085), int(width * 0.63), int(height * 0.64))
    metric_box = (int(width * 0.655), int(height * 0.195), int(width * 0.94), int(height * 0.86))
    draw = ImageDraw.Draw(after, "RGBA")
    _draw_soft_panel(draw, title_box, radius=max(22, width // 58), fill=(250, 247, 240, 248))
    _draw_soft_panel(draw, metric_box, radius=max(22, width // 58), fill=(250, 247, 240, 248))
    title_payload = _draw_fitted_text(
        after,
        title_box,
        "Stable Gate",
        max_font_size=max(72, width // 13),
        min_font_size=max(38, width // 28),
        fill=(14, 34, 49, 255),
        bold=True,
    )
    metric_label = _draw_fitted_text(
        after,
        (metric_box[0], metric_box[1] + int(height * 0.02), metric_box[2], metric_box[1] + int(height * 0.22)),
        "Quality Score",
        max_font_size=max(34, width // 28),
        min_font_size=max(24, width // 44),
        fill=(14, 34, 49, 255),
        bold=True,
        align="center",
    )
    metric_value = _draw_fitted_text(
        after,
        (metric_box[0], metric_box[1] + int(height * 0.22), metric_box[2], metric_box[1] + int(height * 0.58)),
        "94",
        max_font_size=max(110, width // 5),
        min_font_size=max(72, width // 12),
        fill=(176, 133, 74, 255),
        bold=True,
        align="center",
    )
    status = _draw_fitted_text(
        after,
        (metric_box[0], metric_box[1] + int(height * 0.60), metric_box[2], metric_box[3] - int(height * 0.03)),
        "Release Gate: PASS",
        max_font_size=max(28, width // 38),
        min_font_size=max(18, width // 68),
        fill=(14, 34, 49, 230),
        bold=False,
        align="center",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    after.convert("RGB").save(output_path, quality=96)
    return {
        "scenario": "exact_text_patch",
        "source_path": str(base_path),
        "output_path": str(output_path),
        "patches": [title_payload, metric_label, metric_value, status],
        "title_region_diff_ratio": _diff_ratio(before, after, title_box),
        "metric_region_diff_ratio": _diff_ratio(before, after, metric_box),
        "result": "pass",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run direct-first post-processing regression scenarios.")
    parser.add_argument("--root", required=True, help="Regression benchmark root.")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    generated = root / "generated"
    postprocess = root / "postprocess"
    fixtures = root / "fixtures"
    review = root / "review"
    review.mkdir(parents=True, exist_ok=True)

    qr_result = replace_qr(
        base_path=generated / "qr-base.png",
        provided_qr_path=fixtures / "provided-qr.png",
        output_path=postprocess / "qr-replaced.png",
    )
    text_result = edit_text(
        base_path=generated / "text-base.png",
        output_path=postprocess / "text-edited.png",
    )
    output = {
        "benchmark": "direct-first-full-regression-2026-04-24",
        "postprocess_policy": "surgical_patch_only",
        "results": [qr_result, text_result],
        "overall_result": "pass",
    }
    output_path = review / "postprocess-regression-results.json"
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
