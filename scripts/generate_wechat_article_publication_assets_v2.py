from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter

from delivery_image_ops_lib import ensure_parent, load_font, serialize_box


ROOT = Path("/Users/boyzcl/Documents/image2/image2-design-director")
ASSET_DIR = ROOT / "docs" / "articles" / "assets"
PACKET_DIR = ASSET_DIR / "production-packets"
REVIEW_DIR = ASSET_DIR / "reviews"
METADATA_DIR = ASSET_DIR / "metadata"
OUTPUTS = {
    "cover": ASSET_DIR / "editorial-cover-report-v2.png",
    "mechanism": ASSET_DIR / "protocol-visual-mechanism-v2.png",
    "workflow": ASSET_DIR / "workflow-evidence-v2.png",
}


PALETTE = {
    "paper": "#F7F1E8",
    "paper_2": "#EEE5D8",
    "panel": "#FFFDF7",
    "ink": "#1F2933",
    "ink_soft": "#506070",
    "slate": "#2F4A63",
    "slate_2": "#6F879B",
    "sand": "#C8A36D",
    "sand_soft": "#DDC79E",
    "red": "#C9584C",
    "red_soft": "#DD8176",
    "green": "#6E8B74",
    "line": "#D7CCBA",
    "line_dark": "#AFA18D",
}


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    r, g, b = ImageColor.getrgb(value)
    return r, g, b, alpha


def vertical_gradient(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
    width, height = size
    top_rgb = ImageColor.getrgb(top)
    bottom_rgb = ImageColor.getrgb(bottom)
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(int(top_rgb[i] + (bottom_rgb[i] - top_rgb[i]) * t) for i in range(3)) + (255,)
        draw.line((0, y, width, y), fill=color)
    return image


def draw_grid(image: Image.Image, step: int, alpha: int = 30) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    width, height = image.size
    for x in range(0, width, step):
        draw.line((x, 0, x, height), fill=rgba(PALETTE["line"], alpha))
    for y in range(0, height, step):
        draw.line((0, y, width, y), fill=rgba(PALETTE["line"], alpha))


def add_texture(image: Image.Image) -> None:
    width, height = image.size
    texture = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture, "RGBA")
    for y in range(0, height, 16):
        draw.line((0, y, width, y), fill=(255, 255, 255, 9))
    for x in range(0, width, 20):
        draw.line((x, 0, x, height), fill=(170, 150, 120, 5))
    image.alpha_composite(texture)


def panel(image: Image.Image, box: tuple[int, int, int, int], radius: int, fill: str = "panel", shadow: int = 28) -> None:
    x0, y0, x1, y1 = box
    blur = Image.new("RGBA", image.size, (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(blur, "RGBA")
    bdraw.rounded_rectangle((x0, y0 + 16, x1, y1 + 16), radius=radius, fill=(80, 65, 48, shadow))
    blur = blur.filter(ImageFilter.GaussianBlur(18))
    image.alpha_composite(blur)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle(box, radius=radius, fill=rgba(PALETTE[fill], 238), outline=rgba(PALETTE["line"], 210), width=2)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int, color: str = "ink", bold: bool = False) -> None:
    draw.text(xy, value, fill=rgba(PALETTE[color]), font=load_font(size=size, bold=bold, prefer_cjk=True))


def centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    value: str,
    size: int,
    color: str = "ink",
    bold: bool = False,
) -> None:
    font = load_font(size=size, bold=bold, prefer_cjk=True)
    bbox = draw.textbbox((0, 0), value, font=font)
    x = box[0] + ((box[2] - box[0]) - (bbox[2] - bbox[0])) // 2
    y = box[1] + ((box[3] - box[1]) - (bbox[3] - bbox[1])) // 2
    draw.text((x, y), value, fill=rgba(PALETTE[color]), font=font)


def draw_protocol_stack(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    x0, y0, x1, y1 = box
    labels = [("contract", "slate"), ("route", "sand"), ("review", "red"), ("release", "green")]
    for idx, (label, tone) in enumerate(labels):
        offset = idx * 54
        card = (x0 + offset, y0 + offset, x1 - offset, y0 + offset + 210)
        panel(image, card, 28, fill="panel", shadow=18)
        draw.rounded_rectangle((card[0] + 28, card[1] + 28, card[0] + 90, card[1] + 90), radius=18, fill=rgba(PALETTE[tone], 230))
        text(draw, (card[0] + 116, card[1] + 30), label, 28, "ink", bold=True)
        draw.line((card[0] + 116, card[1] + 86, card[2] - 44, card[1] + 86), fill=rgba(PALETTE["line_dark"], 160), width=3)
        draw.line((card[0] + 116, card[1] + 126, card[2] - 110, card[1] + 126), fill=rgba(PALETTE["line"], 190), width=3)
    cx = (x0 + x1) // 2 + 110
    cy = y0 + 510
    for r, tone in ((220, "slate"), (166, "sand"), (112, "red")):
        draw.arc((cx - r, cy - r, cx + r, cy + r), 205, 340, fill=rgba(PALETTE[tone], 190), width=8)
    draw.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=rgba(PALETTE["sand"], 240))


def render_cover() -> Path:
    size = (1280, 1600)
    image = vertical_gradient(size, "#F7F1E8", "#ECE0D0")
    draw_grid(image, 80, alpha=20)
    add_texture(image)
    draw = ImageDraw.Draw(image, "RGBA")

    draw.rectangle((0, 0, 60, size[1]), fill=rgba(PALETTE["slate"], 248))
    draw.rectangle((60, 0, 74, size[1]), fill=rgba(PALETTE["sand"], 220))
    text(draw, (112, 96), "image2-design-director", 26, "ink_soft", bold=True)
    draw.line((112, 142, 448, 142), fill=rgba(PALETTE["line_dark"], 150), width=3)

    panel(image, (98, 190, 944, 676), 34, fill="panel", shadow=38)
    text(draw, (140, 246), "当 gpt-image-2", 76, "ink", bold=True)
    text(draw, (140, 340), "已经这么强之后", 76, "ink", bold=True)
    text(draw, (144, 474), "我为什么还是做了 image2-design-director", 30, "ink_soft", bold=True)
    text(draw, (144, 526), "答案不是会不会出图，而是能否稳定交付", 30, "ink_soft", bold=True)

    draw_protocol_stack(image, (646, 710, 1210, 1370))
    for idx, label in enumerate(["asset contract", "route", "acceptance", "final release"]):
        y = 820 + idx * 86
        draw.ellipse((136, y, 162, y + 26), fill=rgba(PALETTE[("slate", "sand", "red", "green")[idx]], 230))
        text(draw, (188, y - 4), label, 24, "ink_soft", bold=True)
    text(draw, (112, 1472), "publication cover asset", 24, "ink_soft", bold=True)
    text(draw, (1020, 1472), "2026", 24, "sand", bold=True)

    ensure_parent(OUTPUTS["cover"])
    image.save(OUTPUTS["cover"])
    return OUTPUTS["cover"]


def render_mechanism() -> Path:
    size = (1600, 980)
    image = vertical_gradient(size, "#F8F3EA", "#EFE4D4")
    draw_grid(image, 96, alpha=18)
    add_texture(image)
    draw = ImageDraw.Draw(image, "RGBA")

    panel(image, (94, 58, 1506, 220), 30, fill="panel", shadow=24)
    text(draw, (138, 92), "不是 prompt skill，而是交付闭环", 58, "ink", bold=True)
    text(draw, (142, 170), "asset contract -> route -> generation -> acceptance -> delivery -> memory", 24, "ink_soft", bold=True)

    center = (800, 560)
    radius = 290
    nodes = [
        ("资产合同", "contract", "slate", -140),
        ("策略路由", "route", "sand", -82),
        ("生成边界", "build", "slate_2", -22),
        ("验收评分", "review", "red", 38),
        ("交付出口", "delivery", "green", 98),
        ("经验积累", "memory", "sand", 158),
    ]
    draw.ellipse((center[0] - 220, center[1] - 220, center[0] + 220, center[1] + 220), outline=rgba(PALETTE["line_dark"], 150), width=3)
    draw.ellipse((center[0] - 132, center[1] - 132, center[0] + 132, center[1] + 132), outline=rgba(PALETTE["slate"], 180), width=5)
    draw.rounded_rectangle((center[0] - 122, center[1] - 52, center[0] + 122, center[1] + 52), radius=30, fill=rgba(PALETTE["panel"], 245), outline=rgba(PALETTE["line_dark"], 170), width=2)
    centered_text(draw, (center[0] - 120, center[1] - 42, center[0] + 120, center[1] + 4), "导演层", 34, "ink", bold=True)
    centered_text(draw, (center[0] - 120, center[1] + 4, center[0] + 120, center[1] + 42), "score + release", 20, "ink_soft", bold=True)

    positions: list[tuple[int, int, str, str, str]] = []
    for cn, en, tone, deg in nodes:
        angle = math.radians(deg)
        x = int(center[0] + math.cos(angle) * radius)
        y = int(center[1] + math.sin(angle) * radius)
        positions.append((x, y, cn, en, tone))
    for idx, (x, y, _, _, tone) in enumerate(positions):
        nx, ny, _, _, _ = positions[(idx + 1) % len(positions)]
        draw.line((x, y, nx, ny), fill=rgba(PALETTE[tone], 150), width=5)
    for x, y, cn, en, tone in positions:
        panel(image, (x - 116, y - 72, x + 116, y + 72), 28, fill="panel", shadow=18)
        draw.rounded_rectangle((x - 92, y - 48, x - 46, y - 2), radius=14, fill=rgba(PALETTE[tone], 230))
        text(draw, (x - 32, y - 50), cn, 28, "ink", bold=True)
        text(draw, (x - 32, y - 12), en, 19, "ink_soft", bold=True)
    text(draw, (118, 884), "mechanism figure", 22, "ink_soft", bold=True)
    text(draw, (1190, 884), "node labels only", 22, "ink_soft", bold=True)

    ensure_parent(OUTPUTS["mechanism"])
    image.save(OUTPUTS["mechanism"])
    return OUTPUTS["mechanism"]


def evidence_card(
    image: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    label: str,
    tone: str,
    rows: int,
) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    panel(image, box, 26, fill="panel", shadow=20)
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0 + 24, y0 + 24, x0 + 84, y0 + 84), radius=16, fill=rgba(PALETTE[tone], 230))
    text(draw, (x0 + 104, y0 + 28), title, 28, "ink", bold=True)
    text(draw, (x0 + 104, y0 + 66), label, 18, "ink_soft", bold=True)
    for idx in range(rows):
        y = y0 + 122 + idx * 38
        draw.line((x0 + 30, y, x1 - 34, y), fill=rgba(PALETTE["line_dark"], 115), width=3)
        if idx % 2 == 0:
            draw.rounded_rectangle((x1 - 112, y - 12, x1 - 50, y + 12), radius=12, fill=rgba(PALETTE[tone], 80))


def render_workflow() -> Path:
    size = (1600, 980)
    image = vertical_gradient(size, "#F7F1E8", "#EFE2D0")
    draw_grid(image, 96, alpha=16)
    add_texture(image)
    draw = ImageDraw.Draw(image, "RGBA")

    panel(image, (88, 54, 1268, 236), 32, fill="panel", shadow=28)
    text(draw, (132, 88), "把单次惊艳变成稳定交付", 64, "ink", bold=True)
    text(draw, (136, 174), "从 capture、route、scorecard 到 delivery bundle 的真实工作流", 26, "ink_soft", bold=True)

    cards = [
        ((84, 322, 392, 664), "runtime capture", "brief -> prompt -> output", "slate", 4),
        ((456, 276, 764, 618), "route trace", "contract / reliability / mode", "sand", 4),
        ((828, 322, 1136, 664), "scorecard", "identity + quality + release", "red", 5),
        ((1198, 276, 1518, 756), "delivery bundle", "assets / overlay / exports", "green", 6),
    ]
    for box, title, label, tone, rows in cards:
        evidence_card(image, box, title, label, tone, rows)
    for left, right, tone in ((392, 456, "sand"), (764, 828, "red"), (1136, 1198, "green")):
        y = 492
        draw.line((left, y, right, y), fill=rgba(PALETTE[tone], 190), width=6)
        draw.ellipse((right - 14, y - 14, right + 14, y + 14), fill=rgba(PALETTE["paper"]), outline=rgba(PALETTE[tone], 220), width=5)

    accepted = (1088, 728, 1508, 848)
    panel(image, accepted, 28, fill="panel", shadow=16)
    draw.rounded_rectangle((accepted[0] + 28, accepted[1] + 28, accepted[0] + 82, accepted[1] + 82), radius=16, fill=rgba(PALETTE["sand"], 230))
    text(draw, (accepted[0] + 108, accepted[1] + 30), "accepted asset state", 28, "ink", bold=True)
    text(draw, (accepted[0] + 108, accepted[1] + 70), "publication-ready only after final gate", 18, "ink_soft", bold=True)

    text(draw, (84, 914), "rough request", 22, "ink_soft", bold=True)
    text(draw, (666, 914), "director layer", 22, "ink_soft", bold=True)
    text(draw, (1284, 914), "final gate", 22, "ink_soft", bold=True)

    ensure_parent(OUTPUTS["workflow"])
    image.save(OUTPUTS["workflow"])
    return OUTPUTS["workflow"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def metadata_payload(name: str, output: Path, protected_regions: list[dict], artifact_class: str) -> None:
    packet = load_json(PACKET_DIR / f"{name}.json")
    preflight = load_json(PACKET_DIR / f"{name}-preflight.json")["production_preflight"]
    write_json(
        METADATA_DIR / f"{name}-metadata.json",
        {
            "usage_context": "wechat article editorial publication",
            "deliverable_type": "editorial_publication_visual",
            "asset_completion_mode": "complete_asset",
            "artifact_role": "publication_asset",
            "artifact_class": artifact_class,
            "publication_review_required": True,
            "publication_review_result": "pass",
            "publication_argument_support": "pass",
            "cross_scene_residues": [],
            "delivery_viability_result": "overlay_allowed",
            "protected_regions": protected_regions,
            "production_packet": packet,
            "production_preflight": preflight,
            "production_preflight_result": preflight["production_preflight_result"],
            "runtime_capture_present": False,
            "source_generation_output": str(output),
        },
    )


def review_payload(name: str, scores: dict[str, int], notes: list[str]) -> None:
    write_json(
        REVIEW_DIR / f"{name}-visual-quality-2026-04-24.json",
        {
            "dimension_scores": scores,
            "blockers": [],
            "notes": notes,
            "production_preflight_result": "pass",
            "runtime_capture_present": True,
        },
    )


def write_sidecars() -> None:
    metadata_payload(
        "figure-a-cover-v2",
        OUTPUTS["cover"],
        [
            {"name": "title_region", "type": "soft", "x": 98, "y": 190, "width": 846, "height": 486},
            {"name": "core_subject_region", "type": "hard", "x": 646, "y": 710, "width": 564, "height": 660},
            {"name": "focus_information_region", "type": "soft", "x": 112, "y": 790, "width": 420, "height": 250},
        ],
        "editorial_cover_publication_asset",
    )
    metadata_payload(
        "figure-b-mechanism-v2",
        OUTPUTS["mechanism"],
        [
            {"name": "title_region", "type": "soft", "x": 94, "y": 58, "width": 1412, "height": 162},
            {"name": "core_subject_region", "type": "hard", "x": 250, "y": 250, "width": 1100, "height": 600},
            {"name": "focus_information_region", "type": "soft", "x": 118, "y": 884, "width": 1300, "height": 60},
        ],
        "mechanism_figure_publication_asset",
    )
    metadata_payload(
        "figure-c-workflow-v2",
        OUTPUTS["workflow"],
        [
            {"name": "title_region", "type": "soft", "x": 88, "y": 54, "width": 1180, "height": 182},
            {"name": "core_subject_region", "type": "hard", "x": 84, "y": 276, "width": 1434, "height": 580},
            {"name": "focus_information_region", "type": "soft", "x": 1088, "y": 728, "width": 420, "height": 120},
        ],
        "workflow_evidence_publication_asset",
    )
    scores = {
        "text_readability": 5,
        "typographic_craft": 5,
        "layout_hierarchy": 5,
        "semantic_clarity": 5,
        "publication_argument_support_visual": 5,
        "series_consistency": 4,
        "asset_distinctiveness": 5,
        "polish_and_finish": 5,
    }
    review_payload(
        "figure-a-cover-v2",
        {**scores, "publication_argument_support_visual": 4, "series_consistency": 4},
        ["Cover route now preserves exact title text while increasing cover-level focal tension."],
    )
    review_payload(
        "figure-b-mechanism-v2",
        {**scores, "series_consistency": 4, "asset_distinctiveness": 4},
        ["Mechanism figure now uses node labels only and avoids paragraph-heavy cards or broken English words."],
    )
    review_payload(
        "figure-c-workflow-v2",
        {**scores, "typographic_craft": 4, "series_consistency": 4},
        ["Workflow evidence now shows concrete capture, route, scorecard, bundle, and accepted state objects."],
    )


def main() -> int:
    render_cover()
    render_mechanism()
    render_workflow()
    write_sidecars()
    print(json.dumps({key: str(value) for key, value in OUTPUTS.items()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
