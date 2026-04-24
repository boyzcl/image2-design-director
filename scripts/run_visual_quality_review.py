from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from delivery_bundle_lib import get_version_record, load_bundle, read_json, save_bundle, write_json
from publication_review_lib import run_final_release_gate, run_visual_quality_review


def _latest_version_id(manifest: dict[str, Any], state: str) -> str:
    version_id = manifest.get("latest_versions", {}).get(state)
    if not version_id:
        raise ValueError(f"bundle has no latest version for state: {state}")
    return version_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Attach visual quality review and final release result to a bundle version.")
    parser.add_argument("--bundle", required=True, help="Bundle root or bundle.json path.")
    parser.add_argument("--version-id", default=None, help="Version id to review. Defaults to latest delivery_ready_visual.")
    parser.add_argument("--state", default="delivery_ready_visual", choices=["raw_visual", "text_safe_visual", "delivery_ready_visual"])
    parser.add_argument("--review-file", required=True, help="JSON file with dimension_scores, blockers, notes, and optional release fields.")
    parser.add_argument(
        "--runtime-capture-present",
        action="store_true",
        help="Mark runtime capture as present for final release gate.",
    )
    parser.add_argument(
        "--production-preflight-result",
        default=None,
        choices=["pass", "conditional_pass", "fail"],
        help="Override production preflight result for final release gate.",
    )
    args = parser.parse_args()

    manifest, manifest_path = load_bundle(args.bundle)
    bundle_root = manifest_path.parent.resolve()
    version_id = args.version_id or _latest_version_id(manifest, args.state)
    version = get_version_record(manifest, version_id)
    metadata_path = bundle_root / version["metadata_path"]
    record = read_json(metadata_path)
    review_payload = read_json(Path(args.review_file).expanduser().resolve())

    dimension_scores = review_payload.get("dimension_scores", {})
    if not isinstance(dimension_scores, dict):
        raise ValueError("review-file must contain a dimension_scores object")

    visual_review = run_visual_quality_review(
        dimension_scores=dimension_scores,
        blockers=review_payload.get("blockers", []),
        notes=review_payload.get("notes", []),
    )

    extra = dict(record.get("extra_metadata", {}))
    production_preflight_result = (
        args.production_preflight_result
        or review_payload.get("production_preflight_result")
        or extra.get("production_preflight_result")
    )
    runtime_capture_present = bool(
        args.runtime_capture_present
        or review_payload.get("runtime_capture_present")
        or extra.get("runtime_capture_present")
    )
    publication_review_result = extra.get("publication_review_result")
    delivery_viability_result = extra.get("delivery_viability_result")
    final_release = run_final_release_gate(
        production_preflight_result=production_preflight_result,
        publication_review_result=publication_review_result,
        visual_quality_review_result=visual_review["result"],
        delivery_viability_result=delivery_viability_result,
        runtime_capture_present=runtime_capture_present,
    )

    extra["visual_quality_review"] = visual_review
    extra["visual_quality_review_result"] = visual_review["result"]
    extra["visual_quality_score"] = visual_review["score"]
    extra["production_preflight_result"] = production_preflight_result
    extra["runtime_capture_present"] = runtime_capture_present
    extra["final_release_gate"] = final_release
    extra["final_release_result"] = final_release["result"]
    extra["final_release_blockers"] = final_release["final_release_blockers"]
    record["extra_metadata"] = extra

    write_json(metadata_path, record)
    for index, item in enumerate(manifest.get("versions", [])):
        if item.get("version_id") == version_id:
            manifest["versions"][index] = record
            break
    save_bundle(manifest_path, manifest)

    output = {
        "bundle": str(manifest_path),
        "version_id": version_id,
        "visual_quality_review": visual_review,
        "final_release_gate": final_release,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if final_release["result"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
