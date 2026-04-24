from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from PIL import Image

from delivery_bundle_lib import get_latest_version_record, get_version_record, load_bundle, record_export_run, resolve_version_asset_path
from delivery_image_ops_lib import cover_crop_resize, ensure_parent, parse_size, safe_pad_resize
from publication_review_lib import is_editorial_publication_context


def main() -> int:
    parser = argparse.ArgumentParser(description="Export delivery bundle size variants from a delivery-ready source.")
    parser.add_argument("--bundle", required=True, help="Bundle root or bundle.json path.")
    parser.add_argument("--source-version", default=None, help="Source version id. Defaults to latest delivery_ready_visual.")
    parser.add_argument("--target-size", action="append", required=True, help="Target size in WIDTHxHEIGHT format.")
    parser.add_argument(
        "--mode",
        default="safe_pad",
        choices=["safe_pad", "cover_crop"],
        help="Adaptation mode. safe_pad preserves the full source; cover_crop fills the frame by cropping.",
    )
    parser.add_argument("--format", default="png", choices=["png", "jpg"], help="Output image format.")
    parser.add_argument(
        "--allow-non-publication-source",
        action="store_true",
        help="Allow export even when an editorial source has not passed publication review.",
    )
    args = parser.parse_args()

    manifest, manifest_path = load_bundle(args.bundle)
    bundle_root = manifest_path.parent.resolve()
    source_record = (
        get_version_record(manifest, args.source_version)
        if args.source_version
        else get_latest_version_record(manifest, "delivery_ready_visual")
    )
    if not source_record:
        raise SystemExit("no delivery_ready_visual source found")

    source_metadata = source_record.get("extra_metadata", {})
    bundle_context = manifest.get("context", {})
    editorial_context = is_editorial_publication_context(
        usage_context=source_metadata.get("usage_context") or bundle_context.get("usage_context"),
        deliverable_type=source_metadata.get("deliverable_type") or bundle_context.get("deliverable_type"),
        scene=bundle_context.get("scene"),
        tags=list(manifest.get("bundle_tags", [])) + list(source_record.get("tags", [])),
    )
    if editorial_context and not args.allow_non_publication_source:
        artifact_role = source_metadata.get("artifact_role")
        publication_review_result = source_metadata.get("publication_review_result")
        if artifact_role != "publication_asset" or publication_review_result != "pass":
            print(
                json.dumps(
                    {
                        "error": "editorial_source_not_publication_ready",
                        "source_version_id": source_record["version_id"],
                        "artifact_role": artifact_role,
                        "publication_review_result": publication_review_result,
                    },
                    ensure_ascii=False,
                )
            )
            return 2

    source_path = resolve_version_asset_path(bundle_root, source_record)
    source_image = Image.open(source_path).convert("RGBA")
    export_dir = bundle_root / "size-adaptation" / "exports" / source_record["version_id"]
    ensure_parent(export_dir / "placeholder")

    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    outputs = []
    for size_text in args.target_size:
        width, height = parse_size(size_text)
        if args.mode == "safe_pad":
            output_image = safe_pad_resize(source_image, width, height)
        else:
            output_image = cover_crop_resize(source_image, width, height)
        suffix = ".jpg" if args.format == "jpg" else ".png"
        output_path = export_dir / f"{source_record['version_id']}-{width}x{height}{suffix}"
        if args.format == "jpg":
            output_image.convert("RGB").save(output_path, quality=95)
        else:
            output_image.save(output_path)
        outputs.append({"target_size": f"{width}x{height}", "path": str(output_path)})

    run_id = f"size-export-{timestamp}"
    plan_path = export_dir / f"{run_id}.json"
    export_run = {
        "run_id": run_id,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_version_id": source_record["version_id"],
        "source_asset_path": str(source_path),
        "mode": args.mode,
        "format": args.format,
        "outputs": outputs,
        "plan_path": str(plan_path),
    }
    plan_path.write_text(json.dumps(export_run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    record_export_run(
        bundle=str(manifest_path),
        export_run=export_run,
        note=f"Exported {len(outputs)} size variants from {source_record['version_id']} using {args.mode}.",
    )
    print(json.dumps(export_run, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
