from __future__ import annotations

import argparse
import json

from delivery_bundle_lib import init_bundle, register_version, summarize_bundle
from publication_review_lib import ARTIFACT_ROLES, PUBLICATION_REVIEW_RESULTS


def add_shared_version_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--state", required=True, choices=["raw_visual", "text_safe_visual", "delivery_ready_visual"])
    parser.add_argument("--source-image", required=True, help="Path to the image file for this version.")
    parser.add_argument("--transition", default="promote_state", help="Short transition label for this version.")
    parser.add_argument("--parent-version", default=None, help="Optional explicit parent version id.")
    parser.add_argument(
        "--overlay-mode",
        default="none",
        choices=["none", "text_safe_only", "title_plus_supporting_text", "dense_info_layout"],
        help="Text overlay mode planned or already applied for this version.",
    )
    parser.add_argument("--reserved-zone", action="append", default=[], help="Reserved zone label; repeat for multiple zones.")
    parser.add_argument("--fixed-element", action="append", default=[], help="Fixed element label; repeat for multiple items.")
    parser.add_argument("--target-size", action="append", default=[], help="Target size label; repeat for multiple outputs.")
    parser.add_argument("--tag", action="append", default=[], help="Tag for filtering or grouping.")
    parser.add_argument("--note", action="append", default=[], help="Free-form note; repeat for multiple notes.")
    parser.add_argument("--metadata-file", default=None, help="Optional JSON object to merge as extra metadata.")
    parser.add_argument("--usage-context", default=None, help="Usage context for this version.")
    parser.add_argument("--deliverable-type", default=None, help="Deliverable type for this version.")
    parser.add_argument(
        "--asset-completion-mode",
        default=None,
        choices=["complete_asset", "base_visual", "delivery_refinement", "undecided"],
        help="Asset completion mode for this version.",
    )
    parser.add_argument(
        "--artifact-role",
        default=None,
        choices=sorted(ARTIFACT_ROLES),
        help="Artifact role to record for this version.",
    )
    parser.add_argument("--artifact-class", default=None, help="Artifact class label for this version.")
    parser.add_argument(
        "--publication-review-result",
        default=None,
        choices=sorted(PUBLICATION_REVIEW_RESULTS),
        help="Publication review result to record for this version.",
    )
    parser.add_argument(
        "--publication-blocker",
        action="append",
        default=[],
        help="Publication blocker label; repeat for multiple items.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage raw/text-safe/delivery-ready bundle versioning.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a delivery bundle and seed the first version.")
    init_parser.add_argument("--bundle-root", required=True, help="Directory where the bundle should live.")
    init_parser.add_argument("--bundle-id", required=True, help="Stable bundle identifier.")
    init_parser.add_argument("--asset-name", default=None, help="Human-readable asset name.")
    init_parser.add_argument("--scene", default=None, help="Scene or task description for this bundle.")
    init_parser.add_argument("--domain-direction", default=None, help="Domain direction associated with this asset.")
    init_parser.add_argument("--bundle-usage-context", default=None, help="Usage context associated with this bundle.")
    init_parser.add_argument("--bundle-deliverable-type", default=None, help="Deliverable type associated with this bundle.")
    init_parser.add_argument(
        "--bundle-asset-completion-mode",
        default=None,
        choices=["complete_asset", "base_visual", "delivery_refinement", "undecided"],
        help="Default asset completion mode for this bundle.",
    )
    init_parser.add_argument("--matched-profile", default="none", help="Matched profile if any.")
    init_parser.add_argument(
        "--support-tier",
        default="standard",
        choices=["accelerated", "standard", "exploratory"],
        help="Support tier associated with this asset.",
    )
    add_shared_version_args(init_parser)

    add_parser = subparsers.add_parser("add-version", help="Append one new version to an existing bundle.")
    add_parser.add_argument("--bundle", required=True, help="Bundle root or bundle.json path.")
    add_shared_version_args(add_parser)

    show_parser = subparsers.add_parser("show", help="Print bundle summary as JSON.")
    show_parser.add_argument("--bundle", required=True, help="Bundle root or bundle.json path.")

    args = parser.parse_args()

    if args.command == "init":
        manifest_path = init_bundle(
            bundle_root=args.bundle_root,
            bundle_id=args.bundle_id,
            asset_name=args.asset_name,
            scene=args.scene,
            domain_direction=args.domain_direction,
            usage_context=args.bundle_usage_context,
            deliverable_type=args.bundle_deliverable_type,
            asset_completion_mode=args.bundle_asset_completion_mode,
            matched_profile=args.matched_profile,
            support_tier=args.support_tier,
            tags=args.tag,
            notes=args.note,
        )
        record = register_version(
            bundle=str(manifest_path),
            state=args.state,
            source_image=args.source_image,
            transition=args.transition,
            parent_version_id=args.parent_version,
            overlay_mode=args.overlay_mode,
            reserved_zones=args.reserved_zone,
            fixed_elements=args.fixed_element,
            target_sizes=args.target_size,
            tags=args.tag,
            notes=args.note,
            metadata_file=args.metadata_file,
            usage_context=args.usage_context,
            deliverable_type=args.deliverable_type,
            asset_completion_mode=args.asset_completion_mode,
            artifact_role=args.artifact_role,
            artifact_class=args.artifact_class,
            publication_review_result=args.publication_review_result,
            publication_blockers=args.publication_blocker,
        )
        print(json.dumps({"manifest_path": str(manifest_path), "version_id": record["version_id"]}, ensure_ascii=False))
        return 0

    if args.command == "add-version":
        record = register_version(
            bundle=args.bundle,
            state=args.state,
            source_image=args.source_image,
            transition=args.transition,
            parent_version_id=args.parent_version,
            overlay_mode=args.overlay_mode,
            reserved_zones=args.reserved_zone,
            fixed_elements=args.fixed_element,
            target_sizes=args.target_size,
            tags=args.tag,
            notes=args.note,
            metadata_file=args.metadata_file,
            usage_context=args.usage_context,
            deliverable_type=args.deliverable_type,
            asset_completion_mode=args.asset_completion_mode,
            artifact_role=args.artifact_role,
            artifact_class=args.artifact_class,
            publication_review_result=args.publication_review_result,
            publication_blockers=args.publication_blocker,
        )
        print(json.dumps({"version_id": record["version_id"], "asset_path": record["asset_path"]}, ensure_ascii=False))
        return 0

    summary = summarize_bundle(args.bundle)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
