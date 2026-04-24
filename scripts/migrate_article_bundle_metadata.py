from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image

from delivery_bundle_lib import read_json, write_json
from delivery_viability_lib import evaluate_delivery_viability
from publication_review_lib import (
    REQUIRED_EDITORIAL_PROTECTED_REGIONS,
    default_artifact_role_for_state,
    infer_publication_argument_support,
    is_editorial_publication_context,
    run_publication_readiness_review,
)


DEFAULT_USAGE_CONTEXT = "wechat article editorial publication"
DEFAULT_DELIVERABLE_TYPE = "editorial_publication_visual"
TEXT_SAFE_ARTIFACT_CLASS = "text_safe_intermediate"
REVIEW_CANDIDATE_ARTIFACT_CLASS = "editorial_review_candidate"
MIGRATION_NOTE = "Migrated historical article bundle metadata to publication schema."


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def detect_final_artifact_class(bundle_id: str, asset_name: str) -> str:
    text = f"{bundle_id} {asset_name}".lower()
    if "cover" in text:
        return "editorial_cover_publication_asset"
    if "mechanism" in text or "protocol" in text:
        return "mechanism_figure_publication_asset"
    if "workflow" in text or "evidence" in text:
        return "workflow_evidence_publication_asset"
    return "editorial_publication_asset"


def open_image_size(path: Path) -> tuple[int, int]:
    image = Image.open(path)
    try:
        return image.size
    finally:
        image.close()


def clamp_box(x: int, y: int, width: int, height: int, canvas_width: int, canvas_height: int) -> dict[str, int]:
    left = max(0, min(canvas_width, x))
    top = max(0, min(canvas_height, y))
    box_width = max(1, min(canvas_width - left, width))
    box_height = max(1, min(canvas_height - top, height))
    return {"x": left, "y": top, "width": box_width, "height": box_height}


def box_to_tuple(box: dict[str, int]) -> tuple[int, int, int, int]:
    return (box["x"], box["y"], box["x"] + box["width"], box["y"] + box["height"])


def infer_editorial_protected_regions(
    canvas_width: int,
    canvas_height: int,
    title_box: dict[str, int] | None = None,
    footer_box: dict[str, int] | None = None,
) -> list[dict[str, Any]]:
    if title_box:
        title_region = clamp_box(
            x=title_box["x"] - int(canvas_width * 0.015),
            y=title_box["y"] - int(canvas_height * 0.015),
            width=title_box["width"] + int(canvas_width * 0.03),
            height=title_box["height"] + int(canvas_height * 0.03),
            canvas_width=canvas_width,
            canvas_height=canvas_height,
        )
    else:
        title_region = clamp_box(
            x=int(canvas_width * 0.07),
            y=int(canvas_height * 0.07),
            width=int(canvas_width * 0.60),
            height=int(canvas_height * 0.18),
            canvas_width=canvas_width,
            canvas_height=canvas_height,
        )

    if footer_box:
        focus_region = clamp_box(
            x=footer_box["x"],
            y=footer_box["y"],
            width=footer_box["width"],
            height=footer_box["height"],
            canvas_width=canvas_width,
            canvas_height=canvas_height,
        )
    else:
        focus_region = clamp_box(
            x=int(canvas_width * 0.10),
            y=int(canvas_height * 0.76),
            width=int(canvas_width * 0.46),
            height=int(canvas_height * 0.14),
            canvas_width=canvas_width,
            canvas_height=canvas_height,
        )

    core_top = max(int(canvas_height * 0.22), title_region["y"] + title_region["height"] + int(canvas_height * 0.05))
    core_bottom_target = min(
        int(canvas_height * 0.78),
        focus_region["y"] - int(canvas_height * 0.05),
    )
    core_height = core_bottom_target - core_top
    if core_height < int(canvas_height * 0.22):
        core_height = int(canvas_height * 0.30)
    core_region = clamp_box(
        x=int(canvas_width * 0.18),
        y=core_top,
        width=int(canvas_width * 0.64),
        height=core_height,
        canvas_width=canvas_width,
        canvas_height=canvas_height,
    )

    return [
        {"name": "title_region", "type": "soft", **title_region},
        {"name": "core_subject_region", "type": "hard", **core_region},
        {"name": "focus_information_region", "type": "soft", **focus_region},
    ]


def protected_regions_for_viability(protected_regions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "name": region["name"],
            "type": region["type"],
            "box": box_to_tuple(region),
        }
        for region in protected_regions
    ]


def build_candidate_boxes_from_overlay_record(overlay_record: dict[str, Any]) -> list[dict[str, Any]]:
    summary = overlay_record.get("summary", {})
    candidates: list[dict[str, Any]] = []
    title_box = summary.get("title_box")
    if title_box:
        candidates.append({"name": "title_panel", "box": box_to_tuple(title_box)})
    if overlay_record.get("cta_text") or overlay_record.get("date_text"):
        footer_box = summary.get("footer_box")
        if footer_box:
            candidates.append({"name": "footer_band", "box": box_to_tuple(footer_box)})
    if overlay_record.get("qr_image") and summary.get("qr_box"):
        candidates.append({"name": "qr_zone", "box": box_to_tuple(summary["qr_box"])})
    if overlay_record.get("logo_image") and summary.get("logo_box"):
        candidates.append({"name": "logo_zone", "box": box_to_tuple(summary["logo_box"])})
    if overlay_record.get("badge_text") and summary.get("badge_box"):
        candidates.append({"name": "badge_zone", "box": box_to_tuple(summary["badge_box"])})
    return candidates


def load_overlay_record(version_record: dict[str, Any]) -> tuple[dict[str, Any] | None, Path | None]:
    record_path = version_record.get("extra_metadata", {}).get("overlay_record_path")
    if not record_path:
        return None, None
    path = Path(record_path).expanduser().resolve()
    if not path.exists():
        return None, path
    return read_json(path), path


def set_bundle_context(manifest: dict[str, Any]) -> tuple[str, str]:
    context = manifest.setdefault("context", {})
    bundle_id = manifest.get("bundle_id", "")
    asset_name = manifest.get("asset_name", "")
    final_artifact_class = detect_final_artifact_class(bundle_id, asset_name)
    context["usage_context"] = DEFAULT_USAGE_CONTEXT
    context["deliverable_type"] = DEFAULT_DELIVERABLE_TYPE
    context["asset_completion_mode"] = "complete_asset"
    return DEFAULT_DELIVERABLE_TYPE, final_artifact_class


def migrate_bundle(bundle_root: Path) -> dict[str, Any]:
    manifest_path = bundle_root / "bundle.json"
    manifest = read_json(manifest_path)
    deliverable_type, final_artifact_class = set_bundle_context(manifest)
    latest_delivery_ready = manifest.get("latest_versions", {}).get("delivery_ready_visual")

    migrated_versions = []
    publication_assets = []
    review_candidates = []

    for version in manifest.get("versions", []):
        state = version["state"]
        version_file = bundle_root / version["metadata_path"]
        record = read_json(version_file)
        tags = list(dict.fromkeys(list(record.get("tags", [])) + list(manifest.get("bundle_tags", [])) + ["article", "publication"]))
        record["tags"] = tags

        asset_path = bundle_root / record["asset_path"]
        width, height = open_image_size(asset_path)

        extra = dict(record.get("extra_metadata", {}))
        extra["usage_context"] = DEFAULT_USAGE_CONTEXT
        extra["deliverable_type"] = deliverable_type

        overlay_record, overlay_record_path = load_overlay_record(record)
        title_box = None
        footer_box = None
        if overlay_record:
            summary = overlay_record.get("summary", {})
            title_box = summary.get("title_box")
            footer_box = summary.get("footer_box")
        protected_regions = infer_editorial_protected_regions(width, height, title_box=title_box, footer_box=footer_box)
        extra["protected_regions"] = protected_regions

        if state == "text_safe_visual":
            extra["asset_completion_mode"] = "delivery_refinement"
            extra["artifact_role"] = default_artifact_role_for_state(state)
            extra["artifact_class"] = TEXT_SAFE_ARTIFACT_CLASS
            extra["publication_review_required"] = False
        else:
            is_latest = record["version_id"] == latest_delivery_ready
            overlay_title = overlay_record.get("title") if overlay_record else None
            overlay_supporting = overlay_record.get("supporting_lines", []) if overlay_record else []
            candidate_boxes = build_candidate_boxes_from_overlay_record(overlay_record or {})
            viability_report = evaluate_delivery_viability(
                canvas_width=width,
                canvas_height=height,
                candidate_boxes=candidate_boxes,
                protected_regions=protected_regions_for_viability(protected_regions),
                required_region_names=REQUIRED_EDITORIAL_PROTECTED_REGIONS,
                publication_review_required=True,
            )
            artifact_role = "publication_asset" if is_latest else "review_candidate"
            artifact_class = final_artifact_class if is_latest else REVIEW_CANDIDATE_ARTIFACT_CLASS
            publication_argument_support = infer_publication_argument_support(
                usage_context=DEFAULT_USAGE_CONTEXT,
                deliverable_type=deliverable_type,
                artifact_class=artifact_class,
                title=overlay_title,
                supporting_lines=overlay_supporting,
                scene=manifest.get("context", {}).get("scene"),
                tags=tags,
                cross_scene_residues=[],
            )
            review = run_publication_readiness_review(
                artifact_role=artifact_role,
                artifact_class=artifact_class,
                asset_completion_mode="complete_asset",
                publication_argument_support=publication_argument_support,
                cross_scene_residues=[],
                protected_regions=protected_regions,
                delivery_viability_result=viability_report["delivery_viability"],
            )
            if is_latest and review["result"] != "pass":
                artifact_role = "review_candidate"
                artifact_class = REVIEW_CANDIDATE_ARTIFACT_CLASS
                review = run_publication_readiness_review(
                    artifact_role=artifact_role,
                    artifact_class=artifact_class,
                    asset_completion_mode="complete_asset",
                    publication_argument_support=publication_argument_support,
                    cross_scene_residues=[],
                    protected_regions=protected_regions,
                    delivery_viability_result=viability_report["delivery_viability"],
                )

            extra["asset_completion_mode"] = "complete_asset"
            extra["artifact_role"] = artifact_role
            extra["artifact_class"] = artifact_class
            extra["publication_review_required"] = True
            extra["publication_argument_support"] = publication_argument_support
            extra["cross_scene_residues"] = []
            extra["delivery_viability_result"] = viability_report["delivery_viability"]
            extra["collision_risk"] = viability_report["collision_risk"]
            extra["viability_report"] = viability_report
            extra["publication_review_result"] = review["result"]
            extra["publication_blockers"] = review["publication_blockers"]
            extra["publication_review"] = review

            if overlay_record:
                overlay_record["usage_context"] = DEFAULT_USAGE_CONTEXT
                overlay_record["deliverable_type"] = deliverable_type
                overlay_record["asset_completion_mode"] = "complete_asset"
                overlay_record["artifact_role_requested"] = artifact_role
                overlay_record["artifact_class"] = artifact_class
                overlay_record["cross_scene_residues"] = []
                overlay_record["publication_argument_support"] = publication_argument_support
                overlay_record["viability_report"] = viability_report
                overlay_record["publication_review"] = review
                write_json(overlay_record_path, overlay_record)

            if artifact_role == "publication_asset":
                publication_assets.append(record["version_id"])
            else:
                review_candidates.append(record["version_id"])

        record["extra_metadata"] = extra
        write_json(version_file, record)
        migrated_versions.append(record)

    manifest["versions"] = migrated_versions
    manifest["updated_at"] = now_iso()
    bundle_notes = manifest.setdefault("bundle_notes", [])
    bundle_notes.append(
        {
            "timestamp": now_iso(),
            "text": MIGRATION_NOTE,
        }
    )
    write_json(manifest_path, manifest)
    return {
        "bundle_id": manifest.get("bundle_id"),
        "manifest_path": str(manifest_path),
        "publication_assets": publication_assets,
        "review_candidates": review_candidates,
        "version_count": len(migrated_versions),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate historical article bundle metadata to the publication schema.")
    parser.add_argument(
        "--bundles-root",
        default="/Users/boyzcl/Documents/image2/image2-design-director/docs/articles/assets/bundles",
        help="Root directory containing historical article bundles.",
    )
    args = parser.parse_args()

    bundles_root = Path(args.bundles_root).expanduser().resolve()
    results = []
    for bundle_dir in sorted(path for path in bundles_root.iterdir() if (path / "bundle.json").exists()):
        results.append(migrate_bundle(bundle_dir))

    print(json.dumps({"migrated_bundles": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
