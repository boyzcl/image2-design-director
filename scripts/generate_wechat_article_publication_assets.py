from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFilter

from delivery_image_ops_lib import fit_multiline_text, load_font


ROOT = Path("/Users/boyzcl/Documents/image2/image2-design-director")
ASSET_DIR = ROOT / "docs" / "articles" / "assets"
OUTPUTS = {
    "cover": ASSET_DIR / "editorial-cover-report-final.png",
    "mechanism": ASSET_DIR / "protocol-visual-mechanism-final.png",
    "workflow": ASSET_DIR / "workflow-evidence-final.png",
}


PALETTE = {
    "paper": "#F5F0E8",
    "paper_dark": "#ECE2D3",
    "panel": "#FBF8F2",
    "ink": "#1F2933",
    "ink_soft": "#53606F",
    "slate": "#334A60",
    "slate_light": "#6E859A",
    "sand": "#D7BE97",
    "sand_dark": "#B89264",
    "red": "#C05043",
    "red_soft": "#D98175",
    "line": "#D9D0C1",
    "line_dark": "#B8AB96",
    "shadow": "#C9BDAA",
}


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    r, g, b = ImageColor.getrgb(value)
    return (r, g, b, alpha)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def vertical_gradient(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
    width, height = size
    top_rgb = ImageColor.getrgb(top)
    bottom_rgb = ImageColor.getrgb(bottom)
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(int(lerp(top_rgb[i], bottom_rgb[i], t)) for i in range(3)) + (255,)
        draw.line((0, y, width, y), fill=color)
    return image


def add_paper_texture(image: Image.Image, intensity: int = 14) -> None:
    width, height = image.size
    texture = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture, "RGBA")
    step = max(12, width // 96)
    for y in range(0, height, step):
        alpha = intensity + ((y // step) % 3) * 3
        draw.line((0, y, width, y), fill=(255, 255, 255, alpha))
    for x in range(0, width, step):
        alpha = intensity // 2
        draw.line((x, 0, x, height), fill=(210, 200, 185, alpha))
    image.alpha_composite(texture)


def draw_shadow_panel(
    image: Image.Image,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int, int],
    shadow_alpha: int = 52,
    offset: tuple[int, int] = (0, 16),
) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow, "RGBA")
    sx, sy = offset
    shadow_box = (box[0] + sx, box[1] + sy, box[2] + sx, box[3] + sy)
    shadow_draw.rounded_rectangle(shadow_box, radius=radius, fill=(120, 108, 92, shadow_alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(8, radius // 2)))
    image.alpha_composite(shadow)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=rgba(PALETTE["line"], 200), width=2)


def draw_grid(image: Image.Image, step: int, alpha: int = 48) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    width, height = image.size
    for x in range(0, width, step):
        draw.line((x, 0, x, height), fill=rgba(PALETTE["line"], alpha))
    for y in range(0, height, step):
        draw.line((0, y, width, y), fill=rgba(PALETTE["line"], alpha))


def draw_label(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, color: str = "ink_soft") -> None:
    font = load_font(size=24, bold=False, prefer_cjk=True)
    draw.text((x, y), text, fill=rgba(PALETTE[color]), font=font)


def draw_small_chip(image: Image.Image, box: tuple[int, int, int, int], text: str, tone: str = "slate") -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=rgba(PALETTE[tone], 235))
    font = load_font(size=max(16, (box[3] - box[1]) // 2), bold=True, prefer_cjk=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tx = box[0] + ((box[2] - box[0]) - (bbox[2] - bbox[0])) // 2
    ty = box[1] + ((box[3] - box[1]) - (bbox[3] - bbox[1])) // 2 - 1
    draw.text((tx, ty), text, fill=rgba(PALETTE["panel"]), font=font)


def draw_module_card(
    image: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    subtitle: str,
    accent: str,
    icon_mode: str,
) -> None:
    draw_shadow_panel(image, box, radius=28, fill=rgba(PALETTE["panel"], 244), shadow_alpha=30, offset=(0, 10))
    draw = ImageDraw.Draw(image, "RGBA")
    x0, y0, x1, y1 = box
    accent_box = (x0 + 26, y0 + 26, x0 + 96, y0 + 96)
    draw.rounded_rectangle(accent_box, radius=18, fill=rgba(PALETTE[accent], 28), outline=rgba(PALETTE[accent], 140), width=2)
    cx = (accent_box[0] + accent_box[2]) // 2
    cy = (accent_box[1] + accent_box[3]) // 2
    if icon_mode == "packet":
        draw.rounded_rectangle((cx - 18, cy - 22, cx + 18, cy + 22), radius=8, outline=rgba(PALETTE[accent]), width=3)
        draw.line((cx - 10, cy - 6, cx + 10, cy - 6), fill=rgba(PALETTE[accent]), width=3)
        draw.line((cx - 10, cy + 6, cx + 10, cy + 6), fill=rgba(PALETTE[accent]), width=3)
    elif icon_mode == "route":
        points = [(cx - 16, cy + 12), (cx - 2, cy - 12), (cx + 18, cy + 2)]
        draw.line(points, fill=rgba(PALETTE[accent]), width=4)
        for px, py in points:
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=rgba(PALETTE[accent]))
    elif icon_mode == "generation":
        draw.rounded_rectangle((cx - 20, cy - 18, cx + 20, cy + 18), radius=8, outline=rgba(PALETTE[accent]), width=3)
        draw.rectangle((cx - 10, cy - 6, cx + 10, cy + 6), fill=rgba(PALETTE[accent], 90))
    elif icon_mode == "score":
        for idx, px in enumerate((cx - 14, cx, cx + 14)):
            h = (12, 20, 28)[idx]
            draw.rounded_rectangle((px - 4, cy + 16 - h, px + 4, cy + 16), radius=4, fill=rgba(PALETTE[accent]))
    elif icon_mode == "delivery":
        draw.rounded_rectangle((cx - 22, cy - 18, cx + 22, cy + 18), radius=10, outline=rgba(PALETTE[accent]), width=3)
        draw.line((cx - 12, cy, cx + 12, cy), fill=rgba(PALETTE[accent]), width=3)
        draw.line((cx - 12, cy + 10, cx + 12, cy + 10), fill=rgba(PALETTE[accent], 120), width=3)
    elif icon_mode == "memory":
        draw.arc((cx - 22, cy - 22, cx + 22, cy + 22), start=35, end=335, fill=rgba(PALETTE[accent]), width=4)
        draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=rgba(PALETTE[accent]))

    title_font = load_font(size=30, bold=True, prefer_cjk=True)
    subtitle_font = load_font(size=20, bold=False, prefer_cjk=True)
    draw.text((x0 + 124, y0 + 28), title, fill=rgba(PALETTE["ink"]), font=title_font)
    support_text = subtitle
    support_draw = ImageDraw.Draw(image)
    support_font_fitted, support_lines = fit_multiline_text(
        draw=support_draw,
        text=support_text,
        max_width=(x1 - x0) - 150,
        max_height=(y1 - y0) - 90,
        max_font_size=20,
        min_font_size=16,
        line_spacing=1.28,
        bold=False,
        prefer_cjk=True,
    )
    line_height = int(getattr(support_font_fitted, "size", 18) * 1.28)
    base_y = y0 + 74
    for i, line in enumerate(support_lines):
        draw.text((x0 + 124, base_y + i * line_height), line, fill=rgba(PALETTE["ink_soft"]), font=support_font_fitted)


def draw_connection(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], accent: str) -> None:
    sx, sy = start
    ex, ey = end
    mid_x = int((sx + ex) / 2)
    draw.line((sx, sy, mid_x, sy), fill=rgba(PALETTE[accent], 180), width=4)
    draw.line((mid_x, sy, mid_x, ey), fill=rgba(PALETTE[accent], 180), width=4)
    draw.line((mid_x, ey, ex, ey), fill=rgba(PALETTE[accent], 180), width=4)
    draw.ellipse((ex - 6, ey - 6, ex + 6, ey + 6), fill=rgba(PALETTE[accent]))


def draw_book_cover(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw_shadow_panel(image, box, radius=30, fill=rgba(PALETTE["panel"], 232), shadow_alpha=44, offset=(0, 18))
    draw = ImageDraw.Draw(image, "RGBA")
    spine = (x0, y0, x0 + int((x1 - x0) * 0.12), y1)
    draw.rounded_rectangle(spine, radius=30, fill=rgba(PALETTE["slate"], 248))
    draw.rounded_rectangle((x0 + 22, y0 + 22, x1 - 22, y1 - 22), radius=24, outline=rgba(PALETTE["line_dark"], 160), width=2)
    cx = x0 + int((x1 - x0) * 0.62)
    cy = y0 + int((y1 - y0) * 0.70)
    for radius, alpha in ((230, 48), (170, 54), (110, 60)):
        draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), start=200, end=346, fill=rgba(PALETTE["slate"], alpha), width=3)
    for radius, alpha in ((190, 42), (128, 56), (84, 74)):
        draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), start=220, end=326, fill=rgba(PALETTE["sand_dark"], alpha), width=5)
    draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=rgba(PALETTE["sand_dark"], 160))
    draw.line((x0 + 120, y0 + 140, x1 - 90, y0 + 140), fill=rgba(PALETTE["line_dark"], 130), width=3)
    draw.line((x0 + 120, y0 + 190, x1 - 140, y0 + 190), fill=rgba(PALETTE["line_dark"], 110), width=3)
    draw.line((x0 + 120, y0 + 240, x1 - 200, y0 + 240), fill=rgba(PALETTE["line_dark"], 90), width=3)


def draw_title_block(
    image: Image.Image,
    box: tuple[int, int, int, int],
    title: str,
    supporting: list[str],
    project_label: str | None = None,
) -> None:
    draw_shadow_panel(image, box, radius=34, fill=rgba(PALETTE["panel"], 244), shadow_alpha=38, offset=(0, 14))
    draw = ImageDraw.Draw(image, "RGBA")
    x0, y0, x1, y1 = box
    if project_label:
        label_font = load_font(size=24, bold=False, prefer_cjk=True)
        draw.text((x0 + 42, y0 + 28), project_label, fill=rgba(PALETTE["ink_soft"]), font=label_font)
        title_top = y0 + 76
    else:
        title_top = y0 + 42
    title_font, title_lines = fit_multiline_text(
        draw=draw,
        text=title,
        max_width=(x1 - x0) - 84,
        max_height=int((y1 - y0) * 0.52),
        max_font_size=76,
        min_font_size=42,
        line_spacing=1.06,
        bold=True,
        prefer_cjk=True,
    )
    line_height = int(getattr(title_font, "size", 60) * 1.08)
    for i, line in enumerate(title_lines):
        draw.text((x0 + 42, title_top + i * line_height), line, fill=rgba(PALETTE["ink"]), font=title_font)
    support_text = "\n".join(supporting)
    support_font, support_lines = fit_multiline_text(
        draw=draw,
        text=support_text,
        max_width=(x1 - x0) - 84,
        max_height=(y1 - y0) - int((title_top - y0) + line_height * len(title_lines) + 38),
        max_font_size=28,
        min_font_size=20,
        line_spacing=1.3,
        bold=False,
        prefer_cjk=True,
    )
    support_y = title_top + line_height * len(title_lines) + 28
    support_line_height = int(getattr(support_font, "size", 24) * 1.3)
    for i, line in enumerate(support_lines):
        draw.text((x0 + 42, support_y + i * support_line_height), line, fill=rgba(PALETTE["ink_soft"]), font=support_font)


def draw_monogram(image: Image.Image, origin: tuple[int, int], size: int) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    x, y = origin
    stroke = max(8, size // 18)
    draw.arc((x, y, x + size, y + size), start=270, end=90, fill=rgba(PALETTE["sand_dark"]), width=stroke)
    draw.line((x + size // 2, y, x + size // 2, y + size), fill=rgba(PALETTE["sand_dark"]), width=stroke)
    draw.line((x + size // 2 - stroke * 2, y, x + size // 2 - stroke * 2, y + size), fill=rgba(PALETTE["ink"]), width=stroke)


def abstract_asset_frame(image: Image.Image, box: tuple[int, int, int, int], accent: str = "red") -> None:
    x0, y0, x1, y1 = box
    draw_shadow_panel(image, box, radius=20, fill=rgba(PALETTE["panel"], 236), shadow_alpha=24, offset=(0, 8))
    draw = ImageDraw.Draw(image, "RGBA")
    inner = (x0 + 18, y0 + 18, x1 - 18, y1 - 18)
    draw.rounded_rectangle(inner, radius=18, outline=rgba(PALETTE["line_dark"], 140), width=2)
    bands = [
        rgba(PALETTE["slate_light"], 135),
        rgba(PALETTE["sand_dark"], 112),
        rgba(PALETTE["red_soft"], 112 if accent == "red" else 76),
    ]
    cx = x0 + int((x1 - x0) * 0.64)
    cy = y0 + int((y1 - y0) * 0.72)
    for idx, color in enumerate(bands):
        radius = int((x1 - x0) * (0.48 - idx * 0.1))
        draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), start=198, end=344, fill=color, width=5)
    draw.line((x0 + 32, y0 + 44, x1 - 54, y0 + 44), fill=rgba(PALETTE["line_dark"], 120), width=3)
    draw.line((x0 + 32, y0 + 72, x1 - 96, y0 + 72), fill=rgba(PALETTE["line_dark"], 96), width=3)
    chip_box = (x0 + 32, y0 + 112, x0 + 84, y0 + 164)
    draw.rounded_rectangle(chip_box, radius=12, fill=rgba(PALETTE["sand"], 180))
    draw.line((x0 + 32, y0 + 190, x0 + 188, y0 + 190), fill=rgba(PALETTE["line_dark"], 100), width=3)


def render_cover() -> Path:
    size = (1280, 1600)
    image = vertical_gradient(size, PALETTE["paper"], "#F0E8DB")
    add_paper_texture(image)
    draw_grid(image, 80, alpha=24)
    draw = ImageDraw.Draw(image, "RGBA")

    draw.rectangle((0, 0, 44, size[1]), fill=rgba(PALETTE["slate"], 245))
    draw.rounded_rectangle((90, 64, 1210, 430), radius=42, outline=rgba(PALETTE["line"], 180), width=2)
    draw_monogram(image, (72, 74), 68)
    label_font = load_font(size=24, bold=False, prefer_cjk=True)
    draw.text((160, 86), "image2-design-director", fill=rgba(PALETTE["ink_soft"]), font=label_font)

    title_box = (82, 140, 946, 560)
    draw_title_block(
        image,
        title_box,
        "当 gpt-image-2 已经这么强之后",
        [
            "我为什么还是做了 image2-design-director",
            "问题已经不是会不会出图，而是能否稳定交付",
        ],
    )

    card_boxes = [
        (116, 618, 488, 812),
        (116, 862, 488, 1056),
        (116, 1106, 488, 1300),
    ]
    titles = ["资产合同", "策略路由", "验收与交付"]
    subtitles = [
        "先对齐交付物、成品度与允许文本。",
        "按事实负载和任务类型决定该走哪条路。",
        "评分、发表审核和交付可行性要一起成立。",
    ]
    accents = ["slate", "sand_dark", "red"]
    icons = ["packet", "route", "delivery"]
    for box, title, subtitle, accent, icon in zip(card_boxes, titles, subtitles, accents, icons):
        draw_module_card(image, box, title, subtitle, accent, icon)

    for upper, lower, accent in zip(card_boxes, card_boxes[1:], ("slate", "sand_dark")):
        draw_connection(draw, (upper[2], upper[1] + (upper[3] - upper[1]) // 2), (lower[0], lower[1] + 44), accent)

    report_box = (706, 786, 1188, 1380)
    draw_book_cover(image, report_box)
    draw.line((492, 956, 686, 956), fill=rgba(PALETTE["slate"], 184), width=5)
    draw.line((492, 1200, 686, 1080), fill=rgba(PALETTE["sand_dark"], 170), width=5)
    draw.ellipse((666, 938, 704, 976), fill=rgba(PALETTE["paper"]))
    draw.ellipse((666, 938, 704, 976), outline=rgba(PALETTE["slate"]), width=5)

    footer_font = load_font(size=22, bold=False, prefer_cjk=True)
    draw.text((112, 1468), "editorial publication asset", fill=rgba(PALETTE["ink_soft"], 210), font=footer_font)
    draw.text((932, 1468), "2026", fill=rgba(PALETTE["sand_dark"], 220), font=footer_font)

    ensure_parent(OUTPUTS["cover"])
    image.save(OUTPUTS["cover"])
    return OUTPUTS["cover"]


def render_mechanism() -> Path:
    size = (1600, 980)
    image = vertical_gradient(size, "#F8F4ED", "#F2EBDE")
    add_paper_texture(image)
    draw_grid(image, 96, alpha=18)
    draw = ImageDraw.Draw(image, "RGBA")

    title_box = (96, 56, 1500, 210)
    draw_title_block(
        image,
        title_box,
        "这不是一个 prompt skill，而是一条交付闭环",
        ["asset contract → route → generation → acceptance → delivery → accumulation"],
        project_label="mechanism figure",
    )

    module_width = 216
    gap = 26
    start_x = 88
    top = 286
    height = 282
    modules = [
        ("资产合同", "交付物、成品度、文本范围。", "slate", "packet"),
        ("路由", "按事实负载与任务类型分流。", "sand_dark", "route"),
        ("生成", "只让模型承担该承担的图像层。", "slate_light", "generation"),
        ("验收", "用 scorecard 判断是不是对的资产。", "red_soft", "score"),
        ("交付", "overlay、导出与继续交付仍然稳定。", "slate", "delivery"),
        ("积累", "capture 把有效经验留下来。", "sand_dark", "memory"),
    ]
    centers: list[tuple[int, int]] = []
    for idx, (title, subtitle, accent, icon) in enumerate(modules):
        x0 = start_x + idx * (module_width + gap)
        box = (x0, top, x0 + module_width, top + height)
        draw_module_card(image, box, title, subtitle, accent, icon)
        centers.append((box[2], box[1] + 124))
        if idx < len(modules) - 1:
            next_x = x0 + module_width + gap
            draw_connection(draw, (box[2], box[1] + 124), (next_x, box[1] + 124), accent)

    base_y = 678
    labels = ["contract", "routing", "visual build", "review", "delivery", "memory"]
    for idx, label in enumerate(labels):
        cx = start_x + idx * (module_width + gap) + module_width // 2
        draw.ellipse((cx - 20, base_y - 20, cx + 20, base_y + 20), fill=rgba(PALETTE["panel"]), outline=rgba(PALETTE["line_dark"], 160), width=2)
        dot_color = ("slate", "sand_dark", "slate_light", "red_soft", "slate", "sand_dark")[idx]
        draw.ellipse((cx - 10, base_y - 10, cx + 10, base_y + 10), fill=rgba(PALETTE[dot_color], 230))
        chip_box = (cx - 78, base_y + 34, cx + 78, base_y + 74)
        draw.rounded_rectangle(chip_box, radius=18, fill=rgba(PALETTE["panel"], 230), outline=rgba(PALETTE["line"], 200), width=2)
        font = load_font(size=18, bold=False, prefer_cjk=True)
        bbox = draw.textbbox((0, 0), label, font=font)
        draw.text((cx - (bbox[2] - bbox[0]) // 2, base_y + 42), label, fill=rgba(PALETTE["ink_soft"]), font=font)

    draw.line((166, 658, 1434, 658), fill=rgba(PALETTE["line_dark"], 145), width=3)
    ensure_parent(OUTPUTS["mechanism"])
    image.save(OUTPUTS["mechanism"])
    return OUTPUTS["mechanism"]


def draw_pinboard_block(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    draw_shadow_panel(image, box, radius=28, fill=rgba(PALETTE["panel"], 238), shadow_alpha=26, offset=(0, 10))
    draw = ImageDraw.Draw(image, "RGBA")
    x0, y0, x1, y1 = box
    cols = 3
    rows = 3
    card_w = int((x1 - x0 - 56) / cols)
    card_h = int((y1 - y0 - 56) / rows)
    accents = ["slate", "sand_dark", "red_soft"]
    for r in range(rows):
        for c in range(cols):
            px0 = x0 + 18 + c * card_w
            py0 = y0 + 18 + r * card_h
            px1 = px0 + card_w - 14
            py1 = py0 + card_h - 14
            draw.rounded_rectangle((px0, py0, px1, py1), radius=16, fill=rgba(PALETTE["paper"], 230), outline=rgba(PALETTE["line"], 170), width=2)
            tone = accents[(r + c) % len(accents)]
            draw.line((px0 + 18, py0 + 22, px1 - 18, py0 + 22), fill=rgba(PALETTE[tone], 150), width=3)
            draw.line((px0 + 18, py0 + 48, px1 - 40, py0 + 48), fill=rgba(PALETTE["line_dark"], 100), width=3)
            if (r + c) % 2 == 0:
                draw.line((px0 + 22, py1 - 30, px1 - 22, py0 + 72), fill=rgba(PALETTE[tone], 120), width=3)
            else:
                draw.arc((px0 + 22, py0 + 64, px1 - 24, py1 - 20), start=200, end=330, fill=rgba(PALETTE[tone], 140), width=4)


def draw_engine_block(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    draw_shadow_panel(image, box, radius=34, fill=rgba(PALETTE["panel"], 242), shadow_alpha=34, offset=(0, 12))
    draw = ImageDraw.Draw(image, "RGBA")
    x0, y0, x1, y1 = box
    core = (x0 + 88, y0 + 54, x1 - 88, y1 - 78)
    draw.rounded_rectangle(core, radius=26, fill=rgba(PALETTE["paper"], 214), outline=rgba(PALETTE["line_dark"], 180), width=2)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2 + 8
    for radius, color in ((128, "red_soft"), (92, "slate"), (56, "sand_dark")):
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=rgba(PALETTE[color], 180), width=4)
    draw.regular_polygon((cx, cy, 34), 6, rotation=30, fill=rgba(PALETTE["red"], 210))
    nodes = [
        (cx, y0 + 86, "packet"),
        (x0 + 120, cy, "route"),
        (x1 - 120, cy, "generation"),
        (cx, y1 - 100, "score"),
    ]
    for px, py, _ in nodes:
        draw.ellipse((px - 20, py - 20, px + 20, py + 20), fill=rgba(PALETTE["panel"]), outline=rgba(PALETTE["line_dark"], 150), width=2)
        draw.line((cx, cy, px, py), fill=rgba(PALETTE["line_dark"], 130), width=3)
    chip_y = y1 - 52
    chips = ["route", "score", "delivery"]
    for idx, chip in enumerate(chips):
        left = x0 + 72 + idx * 126
        draw_small_chip(image, (left, chip_y, left + 104, chip_y + 38), chip, tone=("slate", "sand_dark", "red_soft")[idx])


def draw_device_cluster(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    desktop = (x0 + 20, y0 + 18, x1 - 110, y0 + 228)
    tablet = (x0 + 70, y0 + 250, x0 + 310, y1 - 18)
    phone = (x1 - 176, y0 + 132, x1 - 30, y1 - 24)
    for frame in (desktop, tablet, phone):
        draw_shadow_panel(image, frame, radius=24, fill=rgba(PALETTE["panel"], 242), shadow_alpha=28, offset=(0, 10))
        draw = ImageDraw.Draw(image, "RGBA")
        inset = (frame[0] + 14, frame[1] + 14, frame[2] - 14, frame[3] - 14)
        draw.rounded_rectangle(inset, radius=18, fill=rgba(PALETTE["paper"], 214), outline=rgba(PALETTE["line_dark"], 140), width=2)
        abstract_asset_frame(image, (inset[0] + 18, inset[1] + 18, inset[2] - 18, inset[3] - 18), accent="red")


def render_workflow() -> Path:
    size = (1600, 980)
    image = vertical_gradient(size, "#F7F3EC", "#F0E8DB")
    add_paper_texture(image)
    draw_grid(image, 96, alpha=16)
    draw = ImageDraw.Draw(image, "RGBA")

    title_box = (90, 52, 1178, 246)
    draw_title_block(
        image,
        title_box,
        "把单次惊艳 变成稳定交付",
        ["让 gpt-image-2 真正进入可控、可验收、可复利的工作流"],
        project_label="workflow evidence",
    )

    left_box = (66, 314, 434, 846)
    center_box = (514, 280, 1012, 800)
    right_box = (1088, 276, 1530, 854)

    draw_pinboard_block(image, left_box)
    draw_engine_block(image, center_box)
    draw_device_cluster(image, right_box)

    draw.line((434, 542, 514, 542), fill=rgba(PALETTE["line_dark"], 160), width=5)
    draw.line((1012, 542, 1088, 542), fill=rgba(PALETTE["line_dark"], 160), width=5)
    draw.ellipse((496, 524, 532, 560), fill=rgba(PALETTE["paper"]), outline=rgba(PALETTE["slate"], 180), width=4)
    draw.ellipse((1070, 524, 1106, 560), fill=rgba(PALETTE["paper"]), outline=rgba(PALETTE["red_soft"], 180), width=4)

    footer_font = load_font(size=20, bold=False, prefer_cjk=True)
    draw.text((84, 914), "rough request", fill=rgba(PALETTE["ink_soft"]), font=footer_font)
    draw.text((698, 914), "director layer", fill=rgba(PALETTE["ink_soft"]), font=footer_font)
    draw.text((1328, 914), "publication assets", fill=rgba(PALETTE["ink_soft"]), font=footer_font)

    ensure_parent(OUTPUTS["workflow"])
    image.save(OUTPUTS["workflow"])
    return OUTPUTS["workflow"]


def main() -> int:
    render_cover()
    render_mechanism()
    render_workflow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
