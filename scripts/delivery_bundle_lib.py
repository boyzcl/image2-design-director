from __future__ import annotations

import json
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from publication_review_lib import (
    ARTIFACT_ROLES,
    FINAL_RELEASE_RESULTS,
    INTERNAL_ONLY_ARTIFACT_CLASSES,
    PUBLICATION_REVIEW_RESULTS,
    VISUAL_QUALITY_REVIEW_RESULTS,
    default_artifact_role_for_state,
    is_editorial_publication_context,
)


BUNDLE_SCHEMA_VERSION = 1
DELIVERY_STATES = ["raw_visual", "text_safe_visual", "delivery_ready_visual"]
DEFAULT_SUPPORT_TIERS = {"accelerated", "standard", "exploratory"}
DEFAULT_OVERLAY_MODES = {
    "none",
    "text_safe_only",
    "title_plus_supporting_text",
    "dense_info_layout",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str, fallback: str = "untitled") -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:96] or fallback


def read_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        if default is None:
            raise FileNotFoundError(path)
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative_to_bundle(bundle_root: Path, path: Path) -> str:
    return path.relative_to(bundle_root).as_posix()


def resolve_manifest_path(bundle: str) -> Path:
    bundle_path = Path(bundle).expanduser().resolve()
    if bundle_path.is_dir():
        return bundle_path / "bundle.json"
    return bundle_path


def ensure_bundle_layout(bundle_root: Path) -> None:
    for state in DELIVERY_STATES:
        (bundle_root / "assets" / state).mkdir(parents=True, exist_ok=True)
    (bundle_root / "overlay" / "pending").mkdir(parents=True, exist_ok=True)
    (bundle_root / "overlay" / "applied").mkdir(parents=True, exist_ok=True)
    (bundle_root / "size-adaptation" / "pending").mkdir(parents=True, exist_ok=True)
    (bundle_root / "size-adaptation" / "exports").mkdir(parents=True, exist_ok=True)
    (bundle_root / "notes").mkdir(parents=True, exist_ok=True)


def init_bundle(
    bundle_root: str,
    bundle_id: str,
    asset_name: str | None = None,
    scene: str | None = None,
    domain_direction: str | None = None,
    usage_context: str | None = None,
    deliverable_type: str | None = None,
    asset_completion_mode: str | None = None,
    matched_profile: str = "none",
    support_tier: str = "standard",
    tags: list[str] | None = None,
    notes: list[str] | None = None,
) -> Path:
    if support_tier not in DEFAULT_SUPPORT_TIERS:
        raise ValueError(f"unsupported support_tier: {support_tier}")

    root = Path(bundle_root).expanduser().resolve()
    manifest_path = root / "bundle.json"
    if manifest_path.exists():
        raise FileExistsError(f"bundle already exists: {manifest_path}")

    ensure_bundle_layout(root)
    created_at = now_iso()
    manifest = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "bundle_id": bundle_id,
        "bundle_slug": slugify(bundle_id),
        "asset_name": asset_name or bundle_id,
        "bundle_root": str(root),
        "created_at": created_at,
        "updated_at": created_at,
        "state_order": DELIVERY_STATES,
        "paths": {
            "manifest": "bundle.json",
            "assets": "assets",
            "overlay": "overlay",
            "size_adaptation": "size-adaptation",
            "notes": "notes",
        },
        "context": {
            "scene": scene,
            "domain_direction": domain_direction,
            "usage_context": usage_context,
            "deliverable_type": deliverable_type,
            "asset_completion_mode": asset_completion_mode,
            "matched_profile": matched_profile,
            "support_tier": support_tier,
        },
        "bundle_tags": tags or [],
        "latest_versions": {state: None for state in DELIVERY_STATES},
        "versions": [],
        "export_runs": [],
        "bundle_notes": [
            {"timestamp": created_at, "text": note}
            for note in (notes or [])
        ],
    }
    write_json(manifest_path, manifest)
    return manifest_path


def load_bundle(bundle: str) -> tuple[dict[str, Any], Path]:
    manifest_path = resolve_manifest_path(bundle)
    manifest = read_json(manifest_path)
    return manifest, manifest_path


def save_bundle(manifest_path: Path, manifest: dict[str, Any]) -> None:
    manifest["updated_at"] = now_iso()
    write_json(manifest_path, manifest)


def append_bundle_note(manifest: dict[str, Any], text: str) -> None:
    manifest.setdefault("bundle_notes", []).append({"timestamp": now_iso(), "text": text})


def validate_state(state: str) -> None:
    if state not in DELIVERY_STATES:
        raise ValueError(f"unsupported state: {state}")


def next_state_version(manifest: dict[str, Any], state: str) -> int:
    return sum(1 for item in manifest.get("versions", []) if item["state"] == state) + 1


def infer_parent_version_id(manifest: dict[str, Any], state: str) -> str | None:
    latest_versions = manifest.get("latest_versions", {})
    same_state_latest = latest_versions.get(state)
    if same_state_latest:
        return same_state_latest

    state_index = DELIVERY_STATES.index(state)
    if state_index == 0:
        return None

    previous_state = DELIVERY_STATES[state_index - 1]
    return latest_versions.get(previous_state)


def normalize_extra_metadata(metadata_file: str | None) -> dict[str, Any]:
    if not metadata_file:
        return {}
    metadata_path = Path(metadata_file).expanduser().resolve()
    data = read_json(metadata_path, {})
    if not isinstance(data, dict):
        raise ValueError("metadata_file must contain a JSON object")
    return data


def normalize_version_metadata(
    manifest: dict[str, Any],
    state: str,
    overlay_mode: str,
    tags: list[str] | None,
    extra_payload: dict[str, Any],
) -> dict[str, Any]:
    payload = dict(extra_payload)
    context = manifest.get("context", {})
    usage_context = payload.get("usage_context") or context.get("usage_context")
    deliverable_type = payload.get("deliverable_type") or context.get("deliverable_type")
    asset_completion_mode = payload.get("asset_completion_mode") or context.get("asset_completion_mode")
    artifact_role = payload.get("artifact_role") or default_artifact_role_for_state(state)
    artifact_class = payload.get("artifact_class")
    if not artifact_class:
        if state == "delivery_ready_visual" and overlay_mode != "none":
            artifact_class = "delivery_bundle_artifact"
        elif state == "delivery_ready_visual":
            artifact_class = "delivery_output"
        else:
            artifact_class = "working_visual"
    publication_review_result = payload.get("publication_review_result")
    visual_quality_review_result = payload.get("visual_quality_review_result")
    final_release_result = payload.get("final_release_result")
    publication_blockers = payload.get("publication_blockers", [])

    if artifact_role not in ARTIFACT_ROLES:
        raise ValueError(f"unsupported artifact_role: {artifact_role}")
    if publication_review_result and publication_review_result not in PUBLICATION_REVIEW_RESULTS:
        raise ValueError(f"unsupported publication_review_result: {publication_review_result}")
    if visual_quality_review_result and visual_quality_review_result not in VISUAL_QUALITY_REVIEW_RESULTS:
        raise ValueError(f"unsupported visual_quality_review_result: {visual_quality_review_result}")
    if final_release_result and final_release_result not in FINAL_RELEASE_RESULTS:
        raise ValueError(f"unsupported final_release_result: {final_release_result}")
    if not isinstance(publication_blockers, list):
        raise ValueError("publication_blockers must be a list when provided")

    editorial_context = is_editorial_publication_context(
        usage_context=usage_context,
        deliverable_type=deliverable_type,
        scene=context.get("scene"),
        tags=(tags or []) + list(manifest.get("bundle_tags", [])),
    )
    publication_review_required = bool(payload.get("publication_review_required", editorial_context))

    if artifact_role == "publication_asset" and publication_review_result != "pass":
        raise ValueError("publication_asset requires publication_review_result=pass")
    if publication_review_result == "pass" and artifact_role != "publication_asset":
        raise ValueError("publication_review_result=pass requires artifact_role=publication_asset")
    if final_release_result == "pass" and publication_review_result != "pass":
        raise ValueError("final_release_result=pass requires publication_review_result=pass")
    if final_release_result == "pass" and visual_quality_review_result != "pass":
        raise ValueError("final_release_result=pass requires visual_quality_review_result=pass")
    if final_release_result == "pass" and payload.get("production_preflight_result") != "pass":
        raise ValueError("final_release_result=pass requires production_preflight_result=pass")
    if final_release_result == "pass" and not payload.get("runtime_capture_present"):
        raise ValueError("final_release_result=pass requires runtime_capture_present=true")
    if artifact_class in INTERNAL_ONLY_ARTIFACT_CLASSES and artifact_role == "publication_asset":
        raise ValueError("internal-only artifact_class cannot be promoted to publication_asset")
    if editorial_context and artifact_role == "publication_asset" and asset_completion_mode != "complete_asset":
        raise ValueError("editorial publication_asset requires asset_completion_mode=complete_asset")

    payload["usage_context"] = usage_context
    payload["deliverable_type"] = deliverable_type
    payload["asset_completion_mode"] = asset_completion_mode
    payload["artifact_role"] = artifact_role
    payload["artifact_class"] = artifact_class
    payload["publication_review_required"] = publication_review_required
    if publication_review_result:
        payload["publication_review_result"] = publication_review_result
    if visual_quality_review_result:
        payload["visual_quality_review_result"] = visual_quality_review_result
    if final_release_result:
        payload["final_release_result"] = final_release_result
    if publication_blockers:
        payload["publication_blockers"] = publication_blockers
    return payload


def get_version_record(manifest: dict[str, Any], version_id: str) -> dict[str, Any]:
    for item in manifest.get("versions", []):
        if item.get("version_id") == version_id:
            return item
    raise KeyError(f"unknown version_id: {version_id}")


def get_latest_version_record(manifest: dict[str, Any], state: str) -> dict[str, Any] | None:
    version_id = manifest.get("latest_versions", {}).get(state)
    if not version_id:
        return None
    return get_version_record(manifest, version_id)


def resolve_version_asset_path(bundle_root: Path, version_record: dict[str, Any]) -> Path:
    return bundle_root / version_record["asset_path"]


def register_version(
    bundle: str,
    state: str,
    source_image: str,
    transition: str,
    parent_version_id: str | None = None,
    overlay_mode: str = "none",
    reserved_zones: list[str] | None = None,
    fixed_elements: list[str] | None = None,
    target_sizes: list[str] | None = None,
    tags: list[str] | None = None,
    notes: list[str] | None = None,
    metadata_file: str | None = None,
    extra_metadata: dict[str, Any] | None = None,
    usage_context: str | None = None,
    deliverable_type: str | None = None,
    asset_completion_mode: str | None = None,
    artifact_role: str | None = None,
    artifact_class: str | None = None,
    publication_review_result: str | None = None,
    publication_blockers: list[str] | None = None,
) -> dict[str, Any]:
    validate_state(state)
    if overlay_mode not in DEFAULT_OVERLAY_MODES:
        raise ValueError(f"unsupported overlay_mode: {overlay_mode}")

    manifest, manifest_path = load_bundle(bundle)
    bundle_root = manifest_path.parent.resolve()
    ensure_bundle_layout(bundle_root)

    source_path = Path(source_image).expanduser().resolve()
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if not source_path.is_file():
        raise ValueError(f"source_image must be a file: {source_path}")

    parent_id = parent_version_id
    if parent_id is None:
        parent_id = infer_parent_version_id(manifest, state)

    state_version = next_state_version(manifest, state)
    version_id = f"{state}-v{state_version:03d}"
    suffix = source_path.suffix or ".bin"
    asset_dir = bundle_root / "assets" / state
    asset_path = asset_dir / f"{version_id}{suffix.lower()}"
    metadata_path = asset_dir / f"{version_id}.json"
    if asset_path.exists() or metadata_path.exists():
        raise FileExistsError(f"version already exists: {version_id}")

    shutil.copy2(source_path, asset_path)
    extra_payload = normalize_extra_metadata(metadata_file)
    if extra_metadata:
        extra_payload.update(extra_metadata)
    if usage_context is not None:
        extra_payload["usage_context"] = usage_context
    if deliverable_type is not None:
        extra_payload["deliverable_type"] = deliverable_type
    if asset_completion_mode is not None:
        extra_payload["asset_completion_mode"] = asset_completion_mode
    if artifact_role is not None:
        extra_payload["artifact_role"] = artifact_role
    if artifact_class is not None:
        extra_payload["artifact_class"] = artifact_class
    if publication_review_result is not None:
        extra_payload["publication_review_result"] = publication_review_result
    if publication_blockers is not None:
        extra_payload["publication_blockers"] = publication_blockers
    extra_payload = normalize_version_metadata(
        manifest=manifest,
        state=state,
        overlay_mode=overlay_mode,
        tags=tags,
        extra_payload=extra_payload,
    )
    record = {
        "version_id": version_id,
        "state": state,
        "state_version": state_version,
        "created_at": now_iso(),
        "asset_path": relative_to_bundle(bundle_root, asset_path),
        "metadata_path": relative_to_bundle(bundle_root, metadata_path),
        "source_path": str(source_path),
        "source_file_name": source_path.name,
        "parent_version_id": parent_id,
        "transition": transition,
        "delivery_plan": {
            "overlay_mode": overlay_mode,
            "reserved_zones": reserved_zones or [],
            "fixed_elements": fixed_elements or [],
            "target_sizes": target_sizes or [],
        },
        "tags": tags or [],
        "notes": notes or [],
        "extra_metadata": extra_payload,
    }

    write_json(metadata_path, record)
    manifest.setdefault("versions", []).append(record)
    manifest.setdefault("latest_versions", {})[state] = version_id
    save_bundle(manifest_path, manifest)
    return record


def summarize_bundle(bundle: str) -> dict[str, Any]:
    manifest, manifest_path = load_bundle(bundle)
    latest_versions = manifest.get("latest_versions", {})
    version_counts = {
        state: sum(1 for item in manifest.get("versions", []) if item["state"] == state)
        for state in DELIVERY_STATES
    }
    return {
        "bundle_id": manifest.get("bundle_id"),
        "asset_name": manifest.get("asset_name"),
        "bundle_root": str(manifest_path.parent.resolve()),
        "context": manifest.get("context", {}),
        "bundle_tags": manifest.get("bundle_tags", []),
        "bundle_notes": manifest.get("bundle_notes", []),
        "latest_versions": latest_versions,
        "version_counts": version_counts,
        "export_runs_count": len(manifest.get("export_runs", [])),
        "next_hooks": {
            "overlay_ready_from": latest_versions.get("text_safe_visual"),
            "size_adaptation_ready_from": latest_versions.get("delivery_ready_visual"),
        },
        "versions": manifest.get("versions", []),
        "export_runs": manifest.get("export_runs", []),
    }


def record_export_run(bundle: str, export_run: dict[str, Any], note: str | None = None) -> dict[str, Any]:
    manifest, manifest_path = load_bundle(bundle)
    manifest.setdefault("export_runs", []).append(export_run)
    if note:
        append_bundle_note(manifest, note)
    save_bundle(manifest_path, manifest)
    return export_run
