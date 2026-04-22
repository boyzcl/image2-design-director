from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw

from delivery_bundle_lib import (
    get_latest_version_record,
    get_version_record,
    load_bundle,
    register_version,
    resolve_version_asset_path,
)
from delivery_image_ops_lib import (
    contains_cjk,
    ensure_parent,
    fit_multiline_text,
    load_font,
    paste_contained_rgba,
    rounded_panel,
    serialize_box,
)


def zone_box(name: str, width: int, height: int) -> tuple[int, int, int, int]:
    mapping = {
        "top_title": (int(width * 0.07), int(height * 0.07), int(width * 0.74), int(height * 0.30)),
        "top_left_logo": (int(width * 0.07), int(height * 0.03), int(width * 0.25), int(height * 0.12)),
        "bottom_right_qr": (int(width * 0.76), int(height * 0.74), int(width * 0.93), int(height * 0.91)),
        "bottom_cta_band": (int(width * 0.07), int(height * 0.78), int(width * 0.70), int(height * 0.92)),
        "top_right_badge": (int(width * 0.72), int(height * 0.09), int(width * 0.92), int(height * 0.17)),
    }
    return mapping.get(name, mapping["top_title"])


def render_overlay(
    source_path: Path,
    title: str,
    supporting_lines: list[str],
    cta_text: str | None,
    date_text: str | None,
    badge_text: str | None,
    qr_image: Path | None,
    logo_image: Path | None,
    font_path: str | None,
) -> tuple[Image.Image, dict[str, object]]:
    base = Image.open(source_path).convert("RGBA")
    width, height = base.size
    draw = ImageDraw.Draw(base, "RGBA")

    title_box = zone_box("top_title", width, height)
    footer_box = zone_box("bottom_cta_band", width, height)
    qr_box = zone_box("bottom_right_qr", width, height)
    logo_box = zone_box("top_left_logo", width, height)
    badge_box = zone_box("top_right_badge", width, height)

    rounded_panel(base, title_box, (247, 244, 238, 205), radius=max(18, width // 50))
    rounded_panel(base, footer_box, (246, 241, 233, 210), radius=max(18, width // 55))
    rounded_panel(base, qr_box, (255, 255, 255, 230), radius=max(16, width // 60))
    if logo_image:
        rounded_panel(base, logo_box, (248, 245, 239, 218), radius=max(16, width // 70))
    if badge_text:
        rounded_panel(base, badge_box, (37, 60, 83, 218), radius=max(18, width // 70))

    title_font, title_lines = fit_multiline_text(
        draw=draw,
        text=title,
        max_width=(title_box[2] - title_box[0]) - int(width * 0.05),
        max_height=int((title_box[3] - title_box[1]) * 0.62),
        max_font_size=max(36, width // 16),
        min_font_size=max(24, width // 28),
        line_spacing=1.08,
        font_path=font_path,
        bold=True,
        prefer_cjk=contains_cjk(title),
    )
    title_x = title_box[0] + int(width * 0.025)
    title_y = title_box[1] + int(height * 0.03)
    line_height = int(getattr(title_font, "size", width // 18) * 1.1)
    for index, line in enumerate(title_lines):
        draw.text((title_x, title_y + index * line_height), line, fill=(29, 37, 45, 255), font=title_font)

    support_text = "\n".join(item for item in supporting_lines if item)
    support_box = (
        title_x,
        title_y + line_height * len(title_lines) + int(height * 0.015),
        title_box[2] - int(width * 0.025),
        title_box[3] - int(height * 0.025),
    )
    support_font, support_lines = fit_multiline_text(
        draw=draw,
        text=support_text,
        max_width=support_box[2] - support_box[0],
        max_height=max(10, support_box[3] - support_box[1]),
        max_font_size=max(20, width // 34),
        min_font_size=max(14, width // 55),
        line_spacing=1.25,
        font_path=font_path,
        bold=False,
        prefer_cjk=contains_cjk(support_text),
    )
    support_y = support_box[1]
    support_line_height = int(getattr(support_font, "size", width // 40) * 1.28)
    for index, line in enumerate(support_lines):
        draw.text((support_box[0], support_y + index * support_line_height), line, fill=(56, 63, 72, 240), font=support_font)

    footer_font = load_font(
        size=max(18, width // 38),
        bold=False,
        font_path=font_path,
        prefer_cjk=contains_cjk(date_text),
    )
    footer_left_x = footer_box[0] + int(width * 0.02)
    footer_left_y = footer_box[1] + int(height * 0.03)
    if date_text:
        draw.text((footer_left_x, footer_left_y), date_text, fill=(37, 48, 59, 255), font=footer_font)
    if cta_text:
        cta_font = load_font(
            size=max(20, width // 34),
            bold=True,
            font_path=font_path,
            prefer_cjk=contains_cjk(cta_text),
        )
        cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        cta_width = cta_bbox[2] - cta_bbox[0]
        cta_height = cta_bbox[3] - cta_bbox[1]
        cta_box = (
            footer_box[2] - cta_width - int(width * 0.06),
            footer_box[1] + int(height * 0.025),
            footer_box[2] - int(width * 0.025),
            footer_box[1] + int(height * 0.025) + cta_height + int(height * 0.025),
        )
        rounded_panel(base, cta_box, (33, 56, 77, 238), radius=max(16, width // 70))
        draw.text(
            (cta_box[0] + int(width * 0.018), cta_box[1] + int(height * 0.012)),
            cta_text,
            fill=(248, 245, 239, 255),
            font=cta_font,
        )

    badge_payload: dict[str, int] | None = None
    if badge_text:
        badge_font = load_font(
            size=max(18, width // 40),
            bold=True,
            font_path=font_path,
            prefer_cjk=contains_cjk(badge_text),
        )
        bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
        badge_text_width = bbox[2] - bbox[0]
        badge_text_height = bbox[3] - bbox[1]
        badge_x = badge_box[0] + ((badge_box[2] - badge_box[0]) - badge_text_width) // 2
        badge_y = badge_box[1] + ((badge_box[3] - badge_box[1]) - badge_text_height) // 2 - 1
        draw.text((badge_x, badge_y), badge_text, fill=(247, 244, 238, 255), font=badge_font)
        badge_payload = serialize_box(badge_box)

    logo_payload = None
    if logo_image:
        logo = Image.open(logo_image).convert("RGBA")
        inner_logo_box = (
            logo_box[0] + int(width * 0.012),
            logo_box[1] + int(height * 0.012),
            logo_box[2] - int(width * 0.012),
            logo_box[3] - int(height * 0.012),
        )
        placed_logo_box = paste_contained_rgba(base, logo, inner_logo_box)
        logo_payload = serialize_box(placed_logo_box)

    qr_payload = None
    if qr_image:
        qr = Image.open(qr_image).convert("RGBA")
        quiet_box = (
            qr_box[0] + int(width * 0.01),
            qr_box[1] + int(height * 0.01),
            qr_box[2] - int(width * 0.01),
            qr_box[3] - int(height * 0.01),
        )
        placed_qr_box = paste_contained_rgba(base, qr, quiet_box)
        qr_payload = serialize_box(placed_qr_box)

    overlay_summary = {
        "title_box": serialize_box(title_box),
        "footer_box": serialize_box(footer_box),
        "qr_box": qr_payload or serialize_box(qr_box),
        "logo_box": logo_payload,
        "badge_box": badge_payload,
        "text_line_count": len(title_lines) + len(support_lines),
    }
    return base, overlay_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply text and fixed-element overlay to a delivery bundle.")
    parser.add_argument("--bundle", required=True, help="Bundle root or bundle.json path.")
    parser.add_argument("--source-version", default=None, help="Source version id. Defaults to latest text_safe_visual.")
    parser.add_argument("--title", required=True, help="Primary headline to place in the title-safe zone.")
    parser.add_argument("--supporting-line", action="append", default=[], help="Supporting line; repeat for multiple lines.")
    parser.add_argument("--cta-text", default=None, help="CTA text for the footer band.")
    parser.add_argument("--date-text", default=None, help="Date or timing text for the footer band.")
    parser.add_argument("--badge-text", default=None, help="Optional badge text in the top-right zone.")
    parser.add_argument("--qr-image", default=None, help="Path to the QR image asset.")
    parser.add_argument("--logo-image", default=None, help="Path to the logo image asset.")
    parser.add_argument("--font-path", default=None, help="Optional explicit font path.")
    parser.add_argument(
        "--overlay-mode",
        default="title_plus_supporting_text",
        choices=["text_safe_only", "title_plus_supporting_text", "dense_info_layout"],
        help="Overlay mode to record in the new version metadata.",
    )
    parser.add_argument("--target-size", action="append", default=[], help="Target delivery size; repeat for multiple sizes.")
    parser.add_argument("--tag", action="append", default=[], help="Tag for the registered delivery-ready version.")
    parser.add_argument("--note", action="append", default=[], help="Free-form note for the registered version.")
    args = parser.parse_args()

    manifest, manifest_path = load_bundle(args.bundle)
    bundle_root = manifest_path.parent.resolve()
    source_record = (
        get_version_record(manifest, args.source_version)
        if args.source_version
        else get_latest_version_record(manifest, "text_safe_visual")
    )
    if not source_record:
        raise SystemExit("no text_safe_visual source found")

    source_path = resolve_version_asset_path(bundle_root, source_record)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    overlay_dir = bundle_root / "overlay" / "applied" / source_record["version_id"]
    ensure_parent(overlay_dir / "placeholder")
    overlay_image_path = overlay_dir / f"overlay-{timestamp}.png"
    overlay_record_path = overlay_dir / f"overlay-{timestamp}.json"

    composed, overlay_summary = render_overlay(
        source_path=source_path,
        title=args.title,
        supporting_lines=args.supporting_line,
        cta_text=args.cta_text,
        date_text=args.date_text,
        badge_text=args.badge_text,
        qr_image=Path(args.qr_image).expanduser().resolve() if args.qr_image else None,
        logo_image=Path(args.logo_image).expanduser().resolve() if args.logo_image else None,
        font_path=args.font_path,
    )
    composed.save(overlay_image_path)

    overlay_record = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_version_id": source_record["version_id"],
        "source_asset_path": str(source_path),
        "overlay_output_path": str(overlay_image_path),
        "overlay_mode": args.overlay_mode,
        "title": args.title,
        "supporting_lines": args.supporting_line,
        "cta_text": args.cta_text,
        "date_text": args.date_text,
        "badge_text": args.badge_text,
        "qr_image": args.qr_image,
        "logo_image": args.logo_image,
        "summary": overlay_summary,
    }
    overlay_record_path.write_text(json.dumps(overlay_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fixed_elements = []
    if args.qr_image:
        fixed_elements.append("qr_code")
    if args.logo_image:
        fixed_elements.append("primary_logo")
    if args.badge_text:
        fixed_elements.append("badge")

    version = register_version(
        bundle=str(manifest_path),
        state="delivery_ready_visual",
        source_image=str(overlay_image_path),
        transition="fixed_element_overlay_applied",
        parent_version_id=source_record["version_id"],
        overlay_mode=args.overlay_mode,
        reserved_zones=source_record.get("delivery_plan", {}).get("reserved_zones", []),
        fixed_elements=fixed_elements or source_record.get("delivery_plan", {}).get("fixed_elements", []),
        target_sizes=args.target_size or source_record.get("delivery_plan", {}).get("target_sizes", []),
        tags=args.tag,
        notes=args.note,
        extra_metadata={
            "overlay_output_path": str(overlay_image_path),
            "overlay_record_path": str(overlay_record_path),
            "overlay_summary": overlay_summary,
        },
    )

    result = {
        "source_version_id": source_record["version_id"],
        "registered_version_id": version["version_id"],
        "delivery_ready_asset_path": version["asset_path"],
        "overlay_output_path": str(overlay_image_path),
        "overlay_record_path": str(overlay_record_path),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
