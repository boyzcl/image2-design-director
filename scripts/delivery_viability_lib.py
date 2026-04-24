from __future__ import annotations

import json
from pathlib import Path
from typing import Any


Box = tuple[int, int, int, int]
EXPECTED_REGION_ALIGNMENTS = {
    "title_panel": {"title_region"},
}


def _parse_scalar(value: Any, total: int) -> int:
    if isinstance(value, str):
        value = value.strip()
    number = float(value)
    if 0 <= number <= 1:
        number *= total
    return int(round(number))


def normalize_box(x: Any, y: Any, width: Any, height: Any, canvas_width: int, canvas_height: int) -> Box:
    left = max(0, min(canvas_width, _parse_scalar(x, canvas_width)))
    top = max(0, min(canvas_height, _parse_scalar(y, canvas_height)))
    box_width = max(0, _parse_scalar(width, canvas_width))
    box_height = max(0, _parse_scalar(height, canvas_height))
    right = max(left, min(canvas_width, left + box_width))
    bottom = max(top, min(canvas_height, top + box_height))
    return left, top, right, bottom


def box_area(box: Box) -> int:
    return max(0, box[2] - box[0]) * max(0, box[3] - box[1])


def intersection_area(a: Box, b: Box) -> int:
    left = max(a[0], b[0])
    top = max(a[1], b[1])
    right = min(a[2], b[2])
    bottom = min(a[3], b[3])
    if right <= left or bottom <= top:
        return 0
    return (right - left) * (bottom - top)


def serialize_box(box: Box) -> dict[str, int]:
    x0, y0, x1, y1 = box
    return {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}


def _normalize_region(region: dict[str, Any], canvas_width: int, canvas_height: int) -> dict[str, Any]:
    box = normalize_box(
        region.get("x", 0),
        region.get("y", 0),
        region.get("width", 0),
        region.get("height", 0),
        canvas_width,
        canvas_height,
    )
    return {
        "name": region.get("name", "protected_region"),
        "type": str(region.get("type", "hard")).lower(),
        "box": box,
        "notes": region.get("notes"),
    }


def parse_region_spec(spec: str, canvas_width: int, canvas_height: int) -> dict[str, Any]:
    parts = [part.strip() for part in spec.split(":")]
    if len(parts) not in (5, 6):
        raise ValueError(f"invalid protected region spec: {spec}")
    name, x, y, width, height = parts[:5]
    region_type = parts[5] if len(parts) == 6 else "hard"
    return _normalize_region(
        {"name": name, "x": x, "y": y, "width": width, "height": height, "type": region_type},
        canvas_width,
        canvas_height,
    )


def load_protected_regions(
    canvas_width: int,
    canvas_height: int,
    region_specs: list[str] | None = None,
    region_file: str | None = None,
    embedded_regions: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    ordered_regions: list[dict[str, Any]] = []
    by_name: dict[str, int] = {}

    def upsert_region(region_payload: dict[str, Any]) -> None:
        normalized = _normalize_region(region_payload, canvas_width, canvas_height)
        name = str(normalized.get("name", "protected_region")).strip().lower()
        if name in by_name:
            ordered_regions[by_name[name]] = normalized
        else:
            by_name[name] = len(ordered_regions)
            ordered_regions.append(normalized)

    for region in embedded_regions or []:
        upsert_region(region)
    for spec in region_specs or []:
        upsert_region(parse_region_spec(spec, canvas_width, canvas_height))
    if region_file:
        payload = json.loads(Path(region_file).expanduser().resolve().read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload = payload.get("protected_regions", [])
        if not isinstance(payload, list):
            raise ValueError("protected region file must contain a list or {\"protected_regions\": [...]}")
        for region in payload:
            upsert_region(region)
    return ordered_regions


def evaluate_delivery_viability(
    canvas_width: int,
    canvas_height: int,
    candidate_boxes: list[dict[str, Any]],
    protected_regions: list[dict[str, Any]],
    max_overlay_coverage: float = 0.38,
    max_soft_overlap_ratio: float = 0.12,
    required_region_names: list[str] | tuple[str, ...] | None = None,
    publication_review_required: bool = False,
) -> dict[str, Any]:
    canvas_area = max(1, canvas_width * canvas_height)
    overlay_area = sum(box_area(candidate["box"]) for candidate in candidate_boxes)
    hard_hits: list[dict[str, Any]] = []
    soft_hits: list[dict[str, Any]] = []
    declared_region_names = {
        str(region.get("name", "")).strip().lower()
        for region in protected_regions
        if region.get("name")
    }
    required_names = [str(name).strip().lower() for name in (required_region_names or []) if str(name).strip()]
    missing_required_names = [name for name in required_names if name not in declared_region_names]
    protected_regions_declared = bool(protected_regions)
    required_editorial_regions_present = not missing_required_names

    for candidate in candidate_boxes:
        candidate_area = max(1, box_area(candidate["box"]))
        for region in protected_regions:
            overlap = intersection_area(candidate["box"], region["box"])
            if overlap <= 0:
                continue
            candidate_name = str(candidate["name"]).strip().lower()
            region_name = str(region["name"]).strip().lower()
            if region_name in EXPECTED_REGION_ALIGNMENTS.get(candidate_name, set()):
                continue
            hit = {
                "candidate": candidate["name"],
                "region": region["name"],
                "region_type": region["type"],
                "overlap_area": overlap,
                "overlap_ratio_of_candidate": round(overlap / candidate_area, 4),
                "candidate_box": serialize_box(candidate["box"]),
                "region_box": serialize_box(region["box"]),
            }
            if region["type"] == "hard":
                hard_hits.append(hit)
            else:
                soft_hits.append(hit)

    overlay_coverage_ratio = overlay_area / canvas_area
    max_soft_hit_ratio = max((hit["overlap_ratio_of_candidate"] for hit in soft_hits), default=0.0)

    if missing_required_names:
        delivery_viability = "overlay_not_allowed_regenerate"
        collision_risk = "high"
        action = "regenerate"
    elif hard_hits:
        delivery_viability = "overlay_not_allowed_regenerate"
        collision_risk = "high"
        action = "regenerate"
    elif overlay_coverage_ratio > max_overlay_coverage:
        delivery_viability = "overlay_not_allowed_regenerate"
        collision_risk = "high"
        action = "regenerate"
    elif max_soft_hit_ratio > max_soft_overlap_ratio or soft_hits:
        delivery_viability = "overlay_allowed_with_limits"
        collision_risk = "medium"
        action = "continue_with_limits"
    else:
        delivery_viability = "overlay_allowed"
        collision_risk = "low"
        action = "continue_overlay"

    warnings: list[str] = []
    if missing_required_names:
        warnings.append("missing required protected regions for editorial overlay")
    if hard_hits:
        warnings.append("overlay intersects hard protected regions")
    if overlay_coverage_ratio > max_overlay_coverage:
        warnings.append("overlay footprint exceeds default coverage budget")
    if soft_hits and delivery_viability != "overlay_not_allowed_regenerate":
        warnings.append("overlay touches soft protected regions")

    return {
        "delivery_viability": delivery_viability,
        "collision_risk": collision_risk,
        "continue_overlay_or_regenerate": action,
        "overlay_coverage_ratio": round(overlay_coverage_ratio, 4),
        "hard_region_hits": hard_hits,
        "soft_region_hits": soft_hits,
        "candidate_boxes": [
            {"name": candidate["name"], "box": serialize_box(candidate["box"])}
            for candidate in candidate_boxes
        ],
        "protected_regions": [
            {"name": region["name"], "type": region["type"], "box": serialize_box(region["box"])}
            for region in protected_regions
        ],
        "protected_regions_declared": protected_regions_declared,
        "required_editorial_regions_present": required_editorial_regions_present,
        "missing_required_region_names": missing_required_names,
        "viability_handoff_to_publication_review": bool(
            publication_review_required and delivery_viability != "overlay_not_allowed_regenerate"
        ),
        "warnings": warnings,
    }
