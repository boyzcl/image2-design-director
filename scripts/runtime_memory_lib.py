from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SKILL_NAME = "image2-design-director"
CAPTURE_SCHEMA_VERSION = 2
RUNTIME_MANIFEST_VERSION = 2
LOCAL_SKILL_MANIFEST_VERSION = 1
KNOWN_PROFILES = {"product-mockup", "social-creative", "ui-mockup", "app-asset"}
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]+")

HOST_DEFAULTS = {
    "codex": {
        "support_tier": "portable",
        "home_env": "CODEX_HOME",
        "fallback_home_dir": ".codex",
    },
    "claude-code": {
        "support_tier": "portable",
        "home_env": "CLAUDE_HOME",
        "fallback_home_dir": ".claude",
    },
    "openclaw": {
        "support_tier": "portable",
        "home_env": "OPENCLAW_HOME",
        "fallback_home_dir": ".openclaw",
    },
}

RUNTIME_ROOT_ENV = "IMAGE2_DESIGN_DIRECTOR_RUNTIME_ROOT"
SKILLS_HOME_ENV = "AGENT_SKILLS_HOME"
AGENT_HOME_ENVS = ["AI_AGENT_HOME", "AGENT_HOME"]
HOST_HINT_ENV = "IMAGE2_DESIGN_DIRECTOR_HOST"
GENERIC_FALLBACK_ROOT = "~/.ai-agents"

DEFAULT_POLICY = {
    "version": 2,
    "backlog_threshold": 10,
    "default_batch_size": 5,
    "max_reviewed_history": 200,
    "max_raw_reads": 5,
    "max_promoted_reads": 3,
    "max_local_skill_reads": 3,
    "promote_min_score": 3,
    "local_skill_min_score": 4,
    "promoted_working_set_ceiling": 20,
    "local_skill_working_set_ceiling": 4,
    "merge_similarity_threshold": 0.36,
    "dedup_similarity_threshold": 0.52,
    "scene_family_merge_threshold": 0.74,
    "scene_family_variant_tokens": [
        "alpha",
        "beta",
        "gamma",
        "delta",
        "retry",
        "retake",
        "variant",
        "version",
        "pass",
        "round",
        "attempt",
        "revision",
        "rev",
        "draft",
        "take",
    ],
    "scene_role_markers": [
        "baseline",
        "candidate",
        "repair",
        "preflight",
        "spot check",
        "scored result",
        "asset linkage",
        "validation",
    ],
    "hard_scene_role_separation": True,
    "archive_keywords": ["smoke test", "bootstrap"],
    "manual_repo_candidate_only": True,
    "scoring": {
        "repeat_signal": 1,
        "transfer_signal": 1,
        "specificity_signal": 1,
        "future_judgment_signal": 1,
    },
    "notes": (
        "Runtime to local skill can be auto-promoted. "
        "Runtime to repo/GitHub stays manual."
    ),
}


@dataclass
class RuntimeResolution:
    host_id: str
    runtime_root: Path
    source: str
    support_tier: str


@dataclass
class PendingItem:
    capture_file: Path
    session_id: str
    scene: str
    promotion_hint: str
    timestamp: str
    schema_version: int
    domain_direction: str
    matched_profile: str
    support_tier: str
    deliverable_type: str
    asset_completion_mode: str
    content_language: str
    allowed_text_scope: str
    layout_owner: str
    acceptance_bar: str
    contract_alignment_result: str | None
    completion_readiness_result: str | None
    repair_class: str | None
    legacy_use_case: str | None


@dataclass
class NoteDoc:
    path: Path
    slug: str
    title: str
    text: str
    tokens: set[str]
    scene: str
    scene_family: str
    domain_direction: str
    matched_profile: str
    support_tier: str
    deliverable_type: str
    asset_completion_mode: str
    content_language: str
    allowed_text_scope: str
    layout_owner: str
    acceptance_bar: str


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(value: str, fallback: str = "untitled") -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:96] or fallback


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_json_if_missing(path: Path, data: Any) -> None:
    if not path.exists():
        write_json(path, data)


def merge_nested_defaults(current: dict[str, Any], default: dict[str, Any]) -> dict[str, Any]:
    merged = dict(default)
    for key, value in current.items():
        if isinstance(value, dict) and isinstance(default.get(key), dict):
            merged[key] = merge_nested_defaults(value, default[key])
        else:
            merged[key] = value
    return merged


def normalize_promotion_policy(policy: dict[str, Any]) -> dict[str, Any]:
    merged = merge_nested_defaults(policy, DEFAULT_POLICY)
    safe_archive_keywords = {keyword.lower() for keyword in DEFAULT_POLICY.get("archive_keywords", [])}
    archive_keywords = []
    for keyword in merged.get("archive_keywords", []):
        normalized = str(keyword).strip().lower()
        if not normalized:
            continue
        if normalized in {"sample", "one-off", "one off", "cli sample"} and normalized not in safe_archive_keywords:
            continue
        archive_keywords.append(normalized)
    merged["archive_keywords"] = archive_keywords or list(DEFAULT_POLICY.get("archive_keywords", []))
    return merged


def load_promotion_policy(runtime_root: Path) -> dict[str, Any]:
    raw = read_json(runtime_root / "state" / "promotion-policy.json", DEFAULT_POLICY)
    policy = normalize_promotion_policy(raw)
    if raw != policy:
        write_json(runtime_root / "state" / "promotion-policy.json", policy)
    return policy


def resolve_runtime_resolution(host: str | None = None, root: str | None = None) -> RuntimeResolution:
    if root:
        runtime_root = Path(root).expanduser()
        chosen_host = host or os.environ.get(HOST_HINT_ENV) or "generic"
        source = "explicit-root"
        support_tier = HOST_DEFAULTS.get(chosen_host, {}).get("support_tier", "custom")
        return RuntimeResolution(chosen_host, runtime_root, source, support_tier)

    chosen_host = host or os.environ.get(HOST_HINT_ENV) or "generic"
    explicit_runtime_root = os.environ.get(RUNTIME_ROOT_ENV)
    if explicit_runtime_root:
        return RuntimeResolution(
            chosen_host,
            Path(explicit_runtime_root).expanduser(),
            f"env:{RUNTIME_ROOT_ENV}",
            HOST_DEFAULTS.get(chosen_host, {}).get("support_tier", "portable"),
        )

    skills_home = os.environ.get(SKILLS_HOME_ENV)
    if skills_home:
        return RuntimeResolution(
            chosen_host,
            Path(skills_home).expanduser() / SKILL_NAME / "runtime",
            f"env:{SKILLS_HOME_ENV}",
            HOST_DEFAULTS.get(chosen_host, {}).get("support_tier", "portable"),
        )

    host_info = HOST_DEFAULTS.get(chosen_host, {})
    env_root = None
    if host_info.get("home_env"):
        env_root = os.environ.get(host_info["home_env"])

    if env_root:
        base = Path(env_root).expanduser()
        source = f"env:{host_info['home_env']}"
    else:
        generic_agent_home = None
        generic_source = None
        for env_name in AGENT_HOME_ENVS:
            value = os.environ.get(env_name)
            if value:
                generic_agent_home = Path(value).expanduser()
                generic_source = f"env:{env_name}"
                break

        if generic_agent_home is not None:
            base = generic_agent_home
            source = generic_source or "agent-home"
        elif host_info.get("fallback_home_dir"):
            base = Path.home() / host_info["fallback_home_dir"]
            source = "host-default"
        else:
            base = Path(GENERIC_FALLBACK_ROOT).expanduser()
            source = "generic-default"

    runtime_root = base / "skills" / SKILL_NAME / "runtime"
    return RuntimeResolution(
        host_id=chosen_host,
        runtime_root=runtime_root,
        source=source,
        support_tier=host_info.get("support_tier", "portable"),
    )


def ensure_runtime_root(runtime_root: Path, resolution: RuntimeResolution) -> dict[str, str]:
    dirs = [
        runtime_root / "captures",
        runtime_root / "index",
        runtime_root / "inbox",
        runtime_root / "promoted" / "field-notes",
        runtime_root / "promoted" / "repo-candidates",
        runtime_root / "promoted" / "archive",
        runtime_root / "promoted" / "local-skill" / "active",
        runtime_root / "promoted" / "local-skill" / "disabled",
        runtime_root / "promoted" / "local-skill" / "archive",
        runtime_root / "promoted" / "local-skill" / "history",
        runtime_root / "state",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    readme = runtime_root / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Runtime Memory\n\n"
            "This directory stores runtime captures, review queue, promoted field notes, and local skill references.\n",
            encoding="utf-8",
        )

    write_json_if_missing(runtime_root / "inbox" / "review-queue.json", {"pending": [], "reviewed": []})
    write_json_if_missing(runtime_root / "index" / "by-scene.json", {})
    write_json_if_missing(runtime_root / "index" / "by-failure-mode.json", {})
    write_json_if_missing(runtime_root / "index" / "by-generation-id.json", {})
    write_json_if_missing(runtime_root / "index" / "by-domain-direction.json", {})
    write_json_if_missing(runtime_root / "index" / "by-matched-profile.json", {})
    write_json_if_missing(runtime_root / "index" / "by-support-tier.json", {})
    write_json_if_missing(runtime_root / "index" / "by-deliverable-type.json", {})
    write_json_if_missing(runtime_root / "index" / "by-asset-completion-mode.json", {})
    write_json_if_missing(runtime_root / "index" / "by-content-language.json", {})
    write_json_if_missing(runtime_root / "index" / "by-layout-owner.json", {})
    write_json_if_missing(runtime_root / "index" / "by-contract-alignment-result.json", {})
    write_json_if_missing(runtime_root / "index" / "by-completion-readiness-result.json", {})
    write_json_if_missing(runtime_root / "index" / "by-repair-class.json", {})
    write_json_if_missing(runtime_root / "state" / "promotion-policy.json", DEFAULT_POLICY)
    write_json_if_missing(
        runtime_root / "state" / "promotion-ledger.json",
        {"version": 2, "created_at": now_iso(), "updated_at": now_iso(), "runs": [], "note_stats": {}},
    )
    write_json_if_missing(
        runtime_root / "state" / "local-skill-manifest.json",
        {"version": LOCAL_SKILL_MANIFEST_VERSION, "updated_at": now_iso(), "entries": {}},
    )
    write_json_if_missing(
        runtime_root / "state" / "runtime-memory-manifest.json",
        {
            "version": RUNTIME_MANIFEST_VERSION,
            "skill_name": SKILL_NAME,
            "host_id": resolution.host_id,
            "support_tier": resolution.support_tier,
            "source": resolution.source,
            "runtime_root": str(runtime_root),
            "capture_schema_version": CAPTURE_SCHEMA_VERSION,
            "created_at": now_iso(),
            "last_local_skill_refresh_at": None,
        },
    )
    return {"runtime_root": str(runtime_root)}


def enrich_capture_record(record: dict[str, Any], resolution: RuntimeResolution) -> dict[str, Any]:
    enriched = dict(record)
    enriched.setdefault("schema_version", CAPTURE_SCHEMA_VERSION)
    if "legacy_use_case" not in enriched and enriched.get("use_case"):
        enriched["legacy_use_case"] = enriched["use_case"]
    if "layout_owner" not in enriched and enriched.get("final_layout_owner"):
        enriched["layout_owner"] = enriched["final_layout_owner"]

    legacy_use_case = enriched.get("legacy_use_case")
    if "matched_profile" not in enriched:
        if legacy_use_case in KNOWN_PROFILES:
            enriched["matched_profile"] = legacy_use_case
        else:
            enriched["matched_profile"] = "none"

    if "support_tier" not in enriched:
        enriched["support_tier"] = "standard" if legacy_use_case in KNOWN_PROFILES else "exploratory"

    enriched.setdefault("domain_direction", enriched.get("scene", "unspecified"))
    enriched.setdefault("deliverable_type", enriched.get("scene", enriched.get("domain_direction", "unspecified")))
    enriched.setdefault("asset_completion_mode", "complete_asset")
    enriched.setdefault("content_language", "unspecified")
    enriched.setdefault("allowed_text_scope", "unspecified")
    enriched.setdefault("layout_owner", "model")
    enriched.setdefault("acceptance_bar", "usable asset aligned with the user request")
    enriched.setdefault("timestamp", now_iso())
    enriched.setdefault("host_id", resolution.host_id)
    enriched.setdefault("skill_name", SKILL_NAME)
    enriched.setdefault("session_id", f"{SKILL_NAME}-{slugify(enriched.get('scene', 'session'))}")
    return enriched


def extract_generation_id(record: dict[str, Any]) -> str | None:
    generation_id = record.get("image_generation_id")
    if generation_id:
        return str(generation_id)
    image_generation = record.get("image_generation")
    if isinstance(image_generation, dict):
        nested = image_generation.get("generation_id")
        if nested:
            return str(nested)
    return None


def append_capture(runtime_root: Path, record: dict[str, Any]) -> Path:
    ensure_runtime_root(
        runtime_root,
        RuntimeResolution(record.get("host_id", "generic"), runtime_root, "append", "portable"),
    )
    date_key = record["timestamp"][:10]
    capture_path = runtime_root / "captures" / f"{date_key}.jsonl"
    with capture_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    update_indices(runtime_root, record, capture_path)
    queue_review(runtime_root, record, capture_path)
    return capture_path


def update_indices(runtime_root: Path, record: dict[str, Any], capture_path: Path) -> None:
    scene_index_path = runtime_root / "index" / "by-scene.json"
    failure_index_path = runtime_root / "index" / "by-failure-mode.json"
    generation_index_path = runtime_root / "index" / "by-generation-id.json"
    domain_index_path = runtime_root / "index" / "by-domain-direction.json"
    profile_index_path = runtime_root / "index" / "by-matched-profile.json"
    tier_index_path = runtime_root / "index" / "by-support-tier.json"
    deliverable_index_path = runtime_root / "index" / "by-deliverable-type.json"
    completion_index_path = runtime_root / "index" / "by-asset-completion-mode.json"
    language_index_path = runtime_root / "index" / "by-content-language.json"
    layout_owner_index_path = runtime_root / "index" / "by-layout-owner.json"
    contract_result_index_path = runtime_root / "index" / "by-contract-alignment-result.json"
    readiness_result_index_path = runtime_root / "index" / "by-completion-readiness-result.json"
    repair_class_index_path = runtime_root / "index" / "by-repair-class.json"

    scene_index = read_json(scene_index_path, {})
    failure_index = read_json(failure_index_path, {})
    generation_index = read_json(generation_index_path, {})
    domain_index = read_json(domain_index_path, {})
    profile_index = read_json(profile_index_path, {})
    tier_index = read_json(tier_index_path, {})
    deliverable_index = read_json(deliverable_index_path, {})
    completion_index = read_json(completion_index_path, {})
    language_index = read_json(language_index_path, {})
    layout_owner_index = read_json(layout_owner_index_path, {})
    contract_result_index = read_json(contract_result_index_path, {})
    readiness_result_index = read_json(readiness_result_index_path, {})
    repair_class_index = read_json(repair_class_index_path, {})

    scene = record.get("scene", "unknown")
    failure_mode = record.get("failure_class", "unspecified")
    generation_id = extract_generation_id(record)
    domain_direction = record.get("domain_direction", "unspecified")
    matched_profile = record.get("matched_profile", "none")
    support_tier = record.get("support_tier", "unspecified")
    deliverable_type = record.get("deliverable_type", "unspecified")
    asset_completion_mode = record.get("asset_completion_mode", "unspecified")
    content_language = record.get("content_language", "unspecified")
    layout_owner = record.get("layout_owner", "unspecified")
    contract_alignment_result = record.get("contract_alignment_result", "unspecified")
    completion_readiness_result = record.get("completion_readiness_result", "unspecified")
    repair_class = record.get("repair_class", "unspecified")
    item = {
        "session_id": record.get("session_id"),
        "timestamp": record.get("timestamp"),
        "capture_file": str(capture_path),
        "domain_direction": domain_direction,
        "matched_profile": matched_profile,
        "support_tier": support_tier,
        "deliverable_type": deliverable_type,
        "asset_completion_mode": asset_completion_mode,
        "content_language": content_language,
        "layout_owner": layout_owner,
        "contract_alignment_result": contract_alignment_result,
        "completion_readiness_result": completion_readiness_result,
        "repair_class": repair_class,
    }

    scene_index.setdefault(scene, []).append(item)
    failure_index.setdefault(failure_mode, []).append(item)
    if generation_id:
        generation_index.setdefault(generation_id, []).append(item)
    domain_index.setdefault(domain_direction, []).append(item)
    profile_index.setdefault(matched_profile, []).append(item)
    tier_index.setdefault(support_tier, []).append(item)
    deliverable_index.setdefault(deliverable_type, []).append(item)
    completion_index.setdefault(asset_completion_mode, []).append(item)
    language_index.setdefault(content_language, []).append(item)
    layout_owner_index.setdefault(layout_owner, []).append(item)
    contract_result_index.setdefault(contract_alignment_result, []).append(item)
    readiness_result_index.setdefault(completion_readiness_result, []).append(item)
    repair_class_index.setdefault(repair_class, []).append(item)

    write_json(scene_index_path, scene_index)
    write_json(failure_index_path, failure_index)
    write_json(generation_index_path, generation_index)
    write_json(domain_index_path, domain_index)
    write_json(profile_index_path, profile_index)
    write_json(tier_index_path, tier_index)
    write_json(deliverable_index_path, deliverable_index)
    write_json(completion_index_path, completion_index)
    write_json(language_index_path, language_index)
    write_json(layout_owner_index_path, layout_owner_index)
    write_json(contract_result_index_path, contract_result_index)
    write_json(readiness_result_index_path, readiness_result_index)
    write_json(repair_class_index_path, repair_class_index)


def queue_review(runtime_root: Path, record: dict[str, Any], capture_path: Path) -> None:
    hint = record.get("promotion_hint")
    if hint not in {"review", "review_for_field_note"}:
        return

    queue_path = runtime_root / "inbox" / "review-queue.json"
    queue = read_json(queue_path, {"pending": [], "reviewed": []})
    queue["pending"].append(
        {
            "capture_file": str(capture_path),
            "session_id": record.get("session_id"),
            "scene": record.get("scene"),
            "schema_version": record.get("schema_version", CAPTURE_SCHEMA_VERSION),
            "domain_direction": record.get("domain_direction", "unspecified"),
            "matched_profile": record.get("matched_profile", "none"),
            "support_tier": record.get("support_tier", "unspecified"),
            "deliverable_type": record.get("deliverable_type", "unspecified"),
            "asset_completion_mode": record.get("asset_completion_mode", "unspecified"),
            "content_language": record.get("content_language", "unspecified"),
            "allowed_text_scope": record.get("allowed_text_scope", "unspecified"),
            "layout_owner": record.get("layout_owner", "unspecified"),
            "acceptance_bar": record.get("acceptance_bar", "unspecified"),
            "contract_alignment_result": record.get("contract_alignment_result"),
            "completion_readiness_result": record.get("completion_readiness_result"),
            "repair_class": record.get("repair_class"),
            "legacy_use_case": record.get("legacy_use_case", record.get("use_case")),
            "promotion_hint": hint,
            "timestamp": record.get("timestamp"),
        }
    )
    write_json(queue_path, queue)


def iter_capture_records(runtime_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted((runtime_root / "captures").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    return records


def find_record_by_session(runtime_root: Path, session_id: str) -> dict[str, Any] | None:
    for record in iter_capture_records(runtime_root):
        if record.get("session_id") == session_id:
            return record
    return None


def normalize_tokens(*parts: str) -> set[str]:
    tokens: set[str] = set()
    for part in parts:
        for token in TOKEN_RE.findall(part.lower()):
            if len(token) < 3:
                continue
            tokens.add(token)
            for subtoken in token.replace("_", "-").split("-"):
                if len(subtoken) >= 3:
                    tokens.add(subtoken)
    return tokens


def stringify_runtime_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return " ".join(stringify_runtime_value(item) for item in value if stringify_runtime_value(item))
    if isinstance(value, dict):
        pieces: list[str] = []
        for key in sorted(value):
            rendered = stringify_runtime_value(value[key])
            if rendered:
                pieces.append(f"{key} {rendered}")
        return " ".join(pieces)
    return str(value)


def scene_family_tokens(scene: str, policy: dict[str, Any] | None = None) -> list[str]:
    variant_tokens = {
        token.lower() for token in (policy or DEFAULT_POLICY).get("scene_family_variant_tokens", [])
    }
    tokens = [token.lower() for token in TOKEN_RE.findall(scene.lower())]
    filtered: list[str] = []
    for token in tokens:
        if len(token) < 3:
            continue
        if token in variant_tokens:
            continue
        if re.fullmatch(r"v\d+", token):
            continue
        if re.fullmatch(r"\d+", token):
            continue
        if re.fullmatch(r"(take|pass|round|attempt|rev|revision|variant|retry)\d+", token):
            continue
        filtered.append(token)
    return filtered


def derive_scene_family(scene: str, policy: dict[str, Any] | None = None) -> str:
    tokens = scene_family_tokens(scene, policy=policy)
    if not tokens:
        return slugify(scene or "unspecified-scene")
    return "-".join(tokens[:8])


def detect_scene_roles(scene: str, policy: dict[str, Any] | None = None) -> set[str]:
    lowered = scene.lower()
    markers = (policy or DEFAULT_POLICY).get("scene_role_markers", [])
    detected: set[str] = set()
    for marker in markers:
        normalized = str(marker).strip().lower()
        if normalized and normalized in lowered:
            detected.add(normalized)
    return detected


def combined_record_text(record: dict[str, Any]) -> str:
    return "\n".join(
        [
            stringify_runtime_value(record.get("scene", "")),
            stringify_runtime_value(record.get("domain_direction", "")),
            stringify_runtime_value(record.get("matched_profile", "")),
            stringify_runtime_value(record.get("support_tier", "")),
            stringify_runtime_value(record.get("deliverable_type", "")),
            stringify_runtime_value(record.get("asset_completion_mode", "")),
            stringify_runtime_value(record.get("content_language", "")),
            stringify_runtime_value(record.get("allowed_text_scope", "")),
            stringify_runtime_value(record.get("layout_owner", "")),
            stringify_runtime_value(record.get("acceptance_bar", "")),
            stringify_runtime_value(record.get("evaluation_summary", "")),
            stringify_runtime_value(record.get("contract_alignment_result", "")),
            stringify_runtime_value(record.get("completion_readiness_result", "")),
            stringify_runtime_value(record.get("repair_class", "")),
            stringify_runtime_value(record.get("what_worked", "")),
            stringify_runtime_value(record.get("what_failed", "")),
            stringify_runtime_value(record.get("correction_rule", "")),
            stringify_runtime_value(record.get("next_input", "")),
        ]
    )


def parse_pending(queue: dict[str, Any]) -> list[PendingItem]:
    items: list[PendingItem] = []
    for raw in queue.get("pending", []):
        items.append(
            PendingItem(
                capture_file=Path(raw["capture_file"]).expanduser(),
                session_id=raw["session_id"],
                scene=raw.get("scene", ""),
                promotion_hint=raw.get("promotion_hint", "review"),
                timestamp=raw.get("timestamp", ""),
                schema_version=int(raw.get("schema_version", CAPTURE_SCHEMA_VERSION)),
                domain_direction=raw.get("domain_direction", "unspecified"),
                matched_profile=raw.get("matched_profile", "none"),
                support_tier=raw.get("support_tier", "unspecified"),
                deliverable_type=raw.get("deliverable_type", "unspecified"),
                asset_completion_mode=raw.get("asset_completion_mode", "unspecified"),
                content_language=raw.get("content_language", "unspecified"),
                allowed_text_scope=raw.get("allowed_text_scope", "unspecified"),
                layout_owner=raw.get("layout_owner", "unspecified"),
                acceptance_bar=raw.get("acceptance_bar", "unspecified"),
                contract_alignment_result=raw.get("contract_alignment_result"),
                completion_readiness_result=raw.get("completion_readiness_result"),
                repair_class=raw.get("repair_class"),
                legacy_use_case=raw.get("legacy_use_case"),
            )
        )
    return items


def token_overlap(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / max(1, min(len(left), len(right)))


def extract_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def load_field_notes(runtime_root: Path, ledger: dict[str, Any]) -> list[NoteDoc]:
    note_stats = ledger.get("note_stats", {})
    policy = load_promotion_policy(runtime_root)
    notes: list[NoteDoc] = []
    for path in sorted((runtime_root / "promoted" / "field-notes").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        entry = note_stats.get(path.stem, {})
        if entry.get("archived"):
            continue
        notes.append(
            NoteDoc(
                path=path,
                slug=path.stem,
                title=extract_heading(text) or path.stem,
                text=text,
                tokens=normalize_tokens(path.stem, text),
                scene=entry.get("scene", path.stem),
                scene_family=entry.get("scene_family", derive_scene_family(entry.get("scene", path.stem), policy=policy)),
                domain_direction=entry.get("domain_direction", "unspecified"),
                matched_profile=entry.get("matched_profile", "none"),
                support_tier=entry.get("support_tier", "unspecified"),
                deliverable_type=entry.get("deliverable_type", "unspecified"),
                asset_completion_mode=entry.get("asset_completion_mode", "unspecified"),
                content_language=entry.get("content_language", "unspecified"),
                allowed_text_scope=entry.get("allowed_text_scope", "unspecified"),
                layout_owner=entry.get("layout_owner", "unspecified"),
                acceptance_bar=entry.get("acceptance_bar", "unspecified"),
            )
        )
    return notes


def metadata_alignment_score(record: dict[str, Any], note: NoteDoc) -> float:
    score = 0.0
    if record.get("domain_direction", "").lower() == note.domain_direction.lower():
        score += 0.2
    elif record.get("domain_direction") and note.domain_direction != "unspecified":
        score += 0.1 * token_overlap(
            normalize_tokens(record.get("domain_direction", "")),
            normalize_tokens(note.domain_direction),
        )
    if record.get("matched_profile", "none").lower() == note.matched_profile.lower():
        score += 0.12
    if record.get("support_tier", "unspecified").lower() == note.support_tier.lower():
        score += 0.08
    if record.get("deliverable_type", "").lower() == note.deliverable_type.lower():
        score += 0.2
    elif record.get("deliverable_type") and note.deliverable_type != "unspecified":
        score += 0.08 * token_overlap(
            normalize_tokens(record.get("deliverable_type", "")),
            normalize_tokens(note.deliverable_type),
        )
    if record.get("asset_completion_mode", "unspecified").lower() == note.asset_completion_mode.lower():
        score += 0.1
    if record.get("content_language", "unspecified").lower() == note.content_language.lower():
        score += 0.1
    if record.get("layout_owner", "unspecified").lower() == note.layout_owner.lower():
        score += 0.05
    if record.get("contract_alignment_result") and record.get("contract_alignment_result", "").lower() in note.text.lower():
        score += 0.05
    if record.get("failure_class", "").lower() in note.text.lower() and record.get("failure_class"):
        score += 0.1
    return min(score, 1.0)


def note_similarity(record: dict[str, Any], note: NoteDoc, policy: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    record_tokens = normalize_tokens(combined_record_text(record))
    text_overlap = token_overlap(record_tokens, note.tokens)
    record_scene_family = derive_scene_family(record.get("scene", ""), policy=policy)
    metadata_score = metadata_alignment_score(record, note)
    record_roles = detect_scene_roles(record.get("scene", ""), policy=policy)
    note_roles = detect_scene_roles(note.scene, policy=policy)
    role_conflict = bool(
        policy.get("hard_scene_role_separation", True)
        and record_roles
        and note_roles
        and record_roles != note_roles
    )
    scene_family_exact = record_scene_family == note.scene_family
    scene_family_overlap = token_overlap(
        set(record_scene_family.split("-")) if record_scene_family else set(),
        set(note.scene_family.split("-")) if note.scene_family else set(),
    )
    weighted = (
        (0.55 if scene_family_exact else 0.25 * scene_family_overlap)
        + (0.25 * text_overlap)
        + (0.20 * metadata_score)
    )
    if scene_family_exact and metadata_score >= 0.55:
        weighted = max(weighted, float(policy.get("scene_family_merge_threshold", 0.74)))
    if role_conflict:
        weighted = min(weighted, float(policy.get("merge_similarity_threshold", 0.36)) - 0.01)
    evidence = {
        "scene_family_exact": scene_family_exact,
        "scene_family_overlap": round(scene_family_overlap, 4),
        "text_overlap": round(text_overlap, 4),
        "metadata_score": round(metadata_score, 4),
        "record_scene_family": record_scene_family,
        "note_scene_family": note.scene_family,
        "record_roles": sorted(record_roles),
        "note_roles": sorted(note_roles),
        "role_conflict": role_conflict,
    }
    return min(weighted, 1.0), evidence


def find_best_field_note_match(
    record: dict[str, Any],
    notes: list[NoteDoc],
    policy: dict[str, Any],
) -> tuple[NoteDoc | None, float, dict[str, Any] | None]:
    best_note = None
    best_score = 0.0
    best_evidence = None
    for note in notes:
        score, evidence = note_similarity(record, note, policy)
        if score > best_score:
            best_score = score
            best_note = note
            best_evidence = evidence
    return best_note, best_score, best_evidence


def score_runtime_record(runtime_root: Path, record: dict[str, Any]) -> tuple[int, dict[str, bool]]:
    policy = load_promotion_policy(runtime_root)
    scene_index = read_json(runtime_root / "index" / "by-scene.json", {})
    failure_index = read_json(runtime_root / "index" / "by-failure-mode.json", {})
    worked_text = stringify_runtime_value(record.get("what_worked", ""))
    next_input_text = stringify_runtime_value(record.get("next_input", ""))
    evaluation_text = stringify_runtime_value(record.get("evaluation_summary", ""))
    signals = {
        "repeat_signal": len(scene_index.get(record.get("scene", ""), [])) >= 2
        or len(failure_index.get(record.get("failure_class", ""), [])) >= 2,
        "transfer_signal": bool(record.get("what_worked")) and bool(record.get("correction_rule")),
        "specificity_signal": len(worked_text) >= 24 and len(next_input_text) >= 24,
        "future_judgment_signal": bool(next_input_text) and bool(evaluation_text),
    }
    score = 0
    for key, enabled in signals.items():
        if enabled:
            score += int(policy["scoring"].get(key, 1))
    return score, signals


def should_archive_low_value(record: dict[str, Any], policy: dict[str, Any]) -> tuple[bool, str | None]:
    combined = combined_record_text(record).lower()
    for keyword in policy.get("archive_keywords", []):
        if keyword in combined:
            return True, f"matched archive keyword: {keyword}"
    if record.get("promotion_hint") == "raw_only":
        return True, "promotion_hint requested raw_only"
    return False, None


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}-{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def render_field_note(record: dict[str, Any], score: int, signals: dict[str, bool], source_capture: Path) -> str:
    signal_lines = [f"- `{name}`: {'yes' if enabled else 'no'}" for name, enabled in signals.items()]
    return (
        f"# Field Note: {record.get('scene', 'Untitled')}\n\n"
        "## Scene Profile\n\n"
        f"- `scene`: {record.get('scene', 'n/a')}\n"
        f"- `domain_direction`: {record.get('domain_direction', 'unspecified')}\n"
        f"- `matched_profile`: {record.get('matched_profile', 'none')}\n"
        f"- `support_tier`: {record.get('support_tier', 'unspecified')}\n"
        f"- `route`: {record.get('route', 'unspecified')}\n\n"
        "## Asset Contract\n\n"
        f"- `deliverable_type`: {record.get('deliverable_type', 'unspecified')}\n"
        f"- `asset_completion_mode`: {record.get('asset_completion_mode', 'unspecified')}\n"
        f"- `content_language`: {record.get('content_language', 'unspecified')}\n"
        f"- `allowed_text_scope`: {record.get('allowed_text_scope', 'unspecified')}\n"
        f"- `layout_owner`: {record.get('layout_owner', 'unspecified')}\n"
        f"- `acceptance_bar`: {record.get('acceptance_bar', 'unspecified')}\n\n"
        "## Trigger\n\n"
        f"- {record.get('evaluation_summary', 'n/a')}\n\n"
        "## Intervention\n\n"
        f"- {record.get('what_worked', record.get('correction_rule', 'n/a'))}\n\n"
        "## Failure Or Risk\n\n"
        f"- {record.get('what_failed', record.get('failure_class', 'n/a'))}\n\n"
        "## Evaluation Outcome\n\n"
        f"- `contract_alignment_result`: {record.get('contract_alignment_result', 'unspecified')}\n"
        f"- `completion_readiness_result`: {record.get('completion_readiness_result', 'unspecified')}\n"
        f"- `repair_class`: {record.get('repair_class', 'n/a')}\n\n"
        "## Next Move\n\n"
        f"- {record.get('next_input', 'n/a')}\n\n"
        "## Promotion Signals\n\n"
        f"- `score`: {score}\n"
        + "\n".join(signal_lines)
        + "\n\n## Source Runtime Capture\n\n"
        f"- `{source_capture}#{record.get('session_id', '')}`\n"
    )


def update_note_stats(ledger: dict[str, Any], note: NoteDoc, record: dict[str, Any], action: str) -> None:
    note_stats = ledger.setdefault("note_stats", {})
    entry = note_stats.setdefault(
        note.slug,
        {
            "note_path": str(note.path),
            "title": note.title,
            "created_at": now_iso(),
            "last_updated_at": now_iso(),
            "source_session_ids": [],
            "merge_count": 0,
            "archived": False,
            "archive_reason": None,
            "last_action": None,
            "scene": note.scene,
            "scene_family": note.scene_family,
            "domain_direction": note.domain_direction,
            "matched_profile": note.matched_profile,
            "support_tier": note.support_tier,
            "deliverable_type": note.deliverable_type,
            "asset_completion_mode": note.asset_completion_mode,
            "content_language": note.content_language,
            "allowed_text_scope": note.allowed_text_scope,
            "layout_owner": note.layout_owner,
            "acceptance_bar": note.acceptance_bar,
        },
    )
    entry["note_path"] = str(note.path)
    entry["title"] = note.title
    entry["last_updated_at"] = now_iso()
    entry["scene"] = note.scene
    entry["scene_family"] = note.scene_family
    entry["domain_direction"] = note.domain_direction
    entry["matched_profile"] = note.matched_profile
    entry["support_tier"] = note.support_tier
    entry["deliverable_type"] = note.deliverable_type
    entry["asset_completion_mode"] = note.asset_completion_mode
    entry["content_language"] = note.content_language
    entry["allowed_text_scope"] = note.allowed_text_scope
    entry["layout_owner"] = note.layout_owner
    entry["acceptance_bar"] = note.acceptance_bar
    entry["last_action"] = action
    session_id = record.get("session_id")
    if session_id and session_id not in entry["source_session_ids"]:
        entry["source_session_ids"].append(session_id)
    if action == "merge_into_existing_note":
        entry["merge_count"] = int(entry.get("merge_count", 0)) + 1
    if action == "archive":
        entry["archived"] = True
        entry["archive_reason"] = record.get("archive_reason")


def create_field_note(
    runtime_root: Path,
    record: dict[str, Any],
    score: int,
    signals: dict[str, bool],
    ledger: dict[str, Any],
) -> NoteDoc:
    note_dir = runtime_root / "promoted" / "field-notes"
    policy = load_promotion_policy(runtime_root)
    slug = slugify(record.get("scene", "field-note"))
    path = ensure_unique_path(note_dir / f"{slug}.md")
    slug = path.stem
    text = render_field_note(record, score, signals, Path(record["capture_file"]))
    path.write_text(text, encoding="utf-8")
    note = NoteDoc(
        path=path,
        slug=slug,
        title=extract_heading(text) or slug,
        text=text,
        tokens=normalize_tokens(slug, text),
        scene=record.get("scene", slug),
        scene_family=derive_scene_family(record.get("scene", slug), policy=policy),
        domain_direction=record.get("domain_direction", "unspecified"),
        matched_profile=record.get("matched_profile", "none"),
        support_tier=record.get("support_tier", "unspecified"),
        deliverable_type=record.get("deliverable_type", "unspecified"),
        asset_completion_mode=record.get("asset_completion_mode", "unspecified"),
        content_language=record.get("content_language", "unspecified"),
        allowed_text_scope=record.get("allowed_text_scope", "unspecified"),
        layout_owner=record.get("layout_owner", "unspecified"),
        acceptance_bar=record.get("acceptance_bar", "unspecified"),
    )
    update_note_stats(ledger, note, record, "promote_to_field_note")
    return note


def merge_field_note(existing: NoteDoc, record: dict[str, Any], ledger: dict[str, Any]) -> NoteDoc:
    addition = (
        "\n## Merge Update\n\n"
        f"- `session_id`: {record.get('session_id', '')}\n"
        f"- `evaluation`: {record.get('evaluation_summary', 'n/a')}\n"
        f"- `deliverable_type`: {record.get('deliverable_type', existing.deliverable_type)}\n"
        f"- `asset_completion_mode`: {record.get('asset_completion_mode', existing.asset_completion_mode)}\n"
        f"- `content_language`: {record.get('content_language', existing.content_language)}\n"
        f"- `contract_alignment_result`: {record.get('contract_alignment_result', 'unspecified')}\n"
        f"- `completion_readiness_result`: {record.get('completion_readiness_result', 'unspecified')}\n"
        f"- `repair_class`: {record.get('repair_class', 'n/a')}\n"
        f"- `what_worked`: {record.get('what_worked', 'n/a')}\n"
        f"- `correction_rule`: {record.get('correction_rule', 'n/a')}\n"
        f"- `next_input`: {record.get('next_input', 'n/a')}\n"
    )
    existing.path.write_text(existing.text.rstrip() + addition + "\n", encoding="utf-8")
    updated_text = existing.path.read_text(encoding="utf-8")
    note = NoteDoc(
        path=existing.path,
        slug=existing.slug,
        title=extract_heading(updated_text) or existing.title,
        text=updated_text,
        tokens=normalize_tokens(existing.slug, updated_text),
        scene=existing.scene,
        scene_family=existing.scene_family,
        domain_direction=record.get("domain_direction", existing.domain_direction),
        matched_profile=record.get("matched_profile", existing.matched_profile),
        support_tier=record.get("support_tier", existing.support_tier),
        deliverable_type=record.get("deliverable_type", existing.deliverable_type),
        asset_completion_mode=record.get("asset_completion_mode", existing.asset_completion_mode),
        content_language=record.get("content_language", existing.content_language),
        allowed_text_scope=record.get("allowed_text_scope", existing.allowed_text_scope),
        layout_owner=record.get("layout_owner", existing.layout_owner),
        acceptance_bar=record.get("acceptance_bar", existing.acceptance_bar),
    )
    update_note_stats(ledger, note, record, "merge_into_existing_note")
    return note


def write_archive_record(runtime_root: Path, record: dict[str, Any], reason: str) -> Path:
    archive_dir = runtime_root / "promoted" / "archive"
    slug = slugify(record.get("scene", "archive"))
    path = ensure_unique_path(archive_dir / f"{slug}.md")
    body = "\n".join(
        [
            f"# Archived Runtime Note: {record.get('scene', 'Untitled')}",
            "",
            "## Decision",
            "",
            "- `archive`",
            "",
            "## Reason",
            "",
            f"- {reason}",
            "",
            "## Source Runtime Capture",
            "",
            f"- `{record.get('capture_file', '')}#{record.get('session_id', '')}`",
            "",
        ]
    )
    path.write_text(body + "\n", encoding="utf-8")
    return path


def load_local_skill_manifest(runtime_root: Path) -> dict[str, Any]:
    return read_json(
        runtime_root / "state" / "local-skill-manifest.json",
        {"version": LOCAL_SKILL_MANIFEST_VERSION, "updated_at": now_iso(), "entries": {}},
    )


def write_local_skill_manifest(runtime_root: Path, manifest: dict[str, Any]) -> None:
    manifest["updated_at"] = now_iso()
    write_json(runtime_root / "state" / "local-skill-manifest.json", manifest)


def history_snapshot_path(runtime_root: Path, slug: str, version: int) -> Path:
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S")
    return runtime_root / "promoted" / "local-skill" / "history" / f"{slug}--v{version}--{timestamp}.md"


def resolve_local_skill_path(runtime_root: Path, slug: str, recorded_path: str | None) -> Path | None:
    if recorded_path:
        candidate = Path(recorded_path).expanduser()
        if candidate.exists():
            return candidate
    search_roots = [
        runtime_root / "promoted" / "local-skill" / "active",
        runtime_root / "promoted" / "local-skill" / "disabled",
        runtime_root / "promoted" / "local-skill" / "archive",
    ]
    for root in search_roots:
        candidate = root / f"{slug}.md"
        if candidate.exists():
            return candidate
    return None


def render_local_skill_reference(note: NoteDoc, record: dict[str, Any], score: int, signals: dict[str, bool]) -> str:
    signal_lines = [f"- `{name}`: {'yes' if enabled else 'no'}" for name, enabled in signals.items()]
    return (
        f"# Local Skill Reference: {record.get('scene', note.scene)}\n\n"
        "## Boundary\n\n"
        "- `runtime_to_local_skill`: auto\n"
        "- `runtime_to_repo_or_github`: manual_only\n\n"
        "## Scope\n\n"
        f"- `scene`: {record.get('scene', note.scene)}\n"
        f"- `domain_direction`: {record.get('domain_direction', note.domain_direction)}\n"
        f"- `matched_profile`: {record.get('matched_profile', note.matched_profile)}\n"
        f"- `support_tier`: {record.get('support_tier', note.support_tier)}\n\n"
        "## Asset Contract\n\n"
        f"- `deliverable_type`: {record.get('deliverable_type', note.deliverable_type)}\n"
        f"- `asset_completion_mode`: {record.get('asset_completion_mode', note.asset_completion_mode)}\n"
        f"- `content_language`: {record.get('content_language', note.content_language)}\n"
        f"- `allowed_text_scope`: {record.get('allowed_text_scope', note.allowed_text_scope)}\n"
        f"- `layout_owner`: {record.get('layout_owner', note.layout_owner)}\n"
        f"- `acceptance_bar`: {record.get('acceptance_bar', note.acceptance_bar)}\n\n"
        "## Trigger\n\n"
        f"- {record.get('evaluation_summary', 'n/a')}\n\n"
        "## Default Carry Forward\n\n"
        f"- {record.get('what_worked', record.get('correction_rule', 'n/a'))}\n\n"
        "## Avoid\n\n"
        f"- {record.get('what_failed', record.get('failure_class', 'n/a'))}\n\n"
        "## Evaluation Outcome\n\n"
        f"- `contract_alignment_result`: {record.get('contract_alignment_result', 'unspecified')}\n"
        f"- `completion_readiness_result`: {record.get('completion_readiness_result', 'unspecified')}\n"
        f"- `repair_class`: {record.get('repair_class', 'n/a')}\n\n"
        "## Next Move\n\n"
        f"- {record.get('next_input', 'n/a')}\n\n"
        "## Evidence\n\n"
        f"- `field_note`: `{note.path}`\n"
        f"- `session_id`: `{record.get('session_id', '')}`\n"
        f"- `promotion_score`: {score}\n"
        + "\n".join(signal_lines)
        + "\n"
    )


def local_skill_gate(record: dict[str, Any], score: int, signals: dict[str, bool], policy: dict[str, Any]) -> tuple[bool, dict[str, bool]]:
    gate_checks = {
        "score_ready": score >= int(policy.get("local_skill_min_score", 4)),
        "trigger_ready": bool(record.get("evaluation_summary")) or bool(record.get("scene")),
        "intervention_ready": bool(record.get("what_worked")) or bool(record.get("correction_rule")),
        "result_ready": bool(record.get("next_input")) or bool(record.get("what_failed")),
    }
    return all(gate_checks.values()), gate_checks


def upsert_local_skill_reference(
    runtime_root: Path,
    manifest: dict[str, Any],
    note: NoteDoc,
    record: dict[str, Any],
    score: int,
    signals: dict[str, bool],
) -> dict[str, Any]:
    slug = note.slug
    entries = manifest.setdefault("entries", {})
    entry = entries.setdefault(
        slug,
        {
            "slug": slug,
            "status": "active",
            "path": None,
            "created_at": now_iso(),
            "last_updated_at": now_iso(),
            "version": 0,
            "source_note_slug": slug,
            "source_note_path": str(note.path),
            "source_session_ids": [],
            "scene": note.scene,
            "domain_direction": note.domain_direction,
            "matched_profile": note.matched_profile,
            "support_tier": note.support_tier,
            "deliverable_type": note.deliverable_type,
            "asset_completion_mode": note.asset_completion_mode,
            "content_language": note.content_language,
            "allowed_text_scope": note.allowed_text_scope,
            "layout_owner": note.layout_owner,
            "acceptance_bar": note.acceptance_bar,
            "last_action": None,
            "disable_reason": None,
            "archive_reason": None,
            "last_restored_from": None,
        },
    )

    if entry.get("status") in {"disabled", "archived"}:
        return {
            "action": "skip_local_skill",
            "status": entry["status"],
            "reason": f"local skill reference is {entry['status']}",
            "path": entry.get("path"),
            "slug": slug,
        }

    active_dir = runtime_root / "promoted" / "local-skill" / "active"
    path = active_dir / f"{slug}.md"
    previous_version = int(entry.get("version", 0))
    if path.exists():
        snapshot = history_snapshot_path(runtime_root, slug, max(previous_version, 1))
        shutil.copy2(path, snapshot)
        action = "update_local_skill_reference"
    else:
        action = "promote_to_local_skill_reference"

    text = render_local_skill_reference(note, record, score, signals)
    path.write_text(text, encoding="utf-8")

    entry["status"] = "active"
    entry["path"] = str(path)
    entry["version"] = previous_version + 1
    entry["source_note_slug"] = slug
    entry["source_note_path"] = str(note.path)
    entry["scene"] = record.get("scene", note.scene)
    entry["domain_direction"] = record.get("domain_direction", note.domain_direction)
    entry["matched_profile"] = record.get("matched_profile", note.matched_profile)
    entry["support_tier"] = record.get("support_tier", note.support_tier)
    entry["deliverable_type"] = record.get("deliverable_type", note.deliverable_type)
    entry["asset_completion_mode"] = record.get("asset_completion_mode", note.asset_completion_mode)
    entry["content_language"] = record.get("content_language", note.content_language)
    entry["allowed_text_scope"] = record.get("allowed_text_scope", note.allowed_text_scope)
    entry["layout_owner"] = record.get("layout_owner", note.layout_owner)
    entry["acceptance_bar"] = record.get("acceptance_bar", note.acceptance_bar)
    entry["last_updated_at"] = now_iso()
    entry["last_action"] = action
    entry["disable_reason"] = None
    entry["archive_reason"] = None
    session_id = record.get("session_id")
    if session_id and session_id not in entry["source_session_ids"]:
        entry["source_session_ids"].append(session_id)
    return {"action": action, "status": "active", "path": str(path), "slug": slug}


def set_local_skill_reference_status(runtime_root: Path, slug: str, status: str, reason: str | None = None) -> dict[str, Any]:
    if status not in {"active", "disabled", "archived"}:
        raise ValueError(f"unsupported local skill status: {status}")

    manifest = load_local_skill_manifest(runtime_root)
    entry = manifest.setdefault("entries", {}).get(slug)
    if not entry:
        raise ValueError(f"local skill reference `{slug}` not found")

    current_status = entry.get("status", "active")
    current_path = resolve_local_skill_path(runtime_root, slug, entry.get("path"))
    active_dir = runtime_root / "promoted" / "local-skill" / "active"
    disabled_dir = runtime_root / "promoted" / "local-skill" / "disabled"
    archive_dir = runtime_root / "promoted" / "local-skill" / "archive"

    if status == "active":
        target_path = active_dir / f"{slug}.md"
    elif status == "disabled":
        target_path = disabled_dir / f"{slug}.md"
    else:
        target_path = archive_dir / f"{slug}.md"

    if current_path and current_path.exists() and current_path != target_path:
        target_path = ensure_unique_path(target_path)
        current_path.rename(target_path)
    elif current_path is None:
        raise ValueError(f"local skill reference `{slug}` has no recorded path")
    else:
        target_path = current_path

    entry["path"] = str(target_path)
    entry["status"] = status
    entry["last_updated_at"] = now_iso()
    entry["last_action"] = f"set_status:{status}"
    if status == "disabled":
        entry["disable_reason"] = reason or entry.get("disable_reason")
    if status == "archived":
        entry["archive_reason"] = reason or entry.get("archive_reason")
    if current_status == "archived" and status == "active":
        entry["archive_reason"] = None
    if current_status == "disabled" and status == "active":
        entry["disable_reason"] = None
    write_local_skill_manifest(runtime_root, manifest)
    return {"slug": slug, "status": status, "path": str(target_path), "reason": reason}


def rollback_local_skill_reference(runtime_root: Path, slug: str) -> dict[str, Any]:
    manifest = load_local_skill_manifest(runtime_root)
    entry = manifest.setdefault("entries", {}).get(slug)
    if not entry:
        raise ValueError(f"local skill reference `{slug}` not found")

    history_dir = runtime_root / "promoted" / "local-skill" / "history"
    snapshots = sorted(history_dir.glob(f"{slug}--v*.md"))
    if not snapshots:
        raise ValueError(f"local skill reference `{slug}` has no history snapshot")

    latest_snapshot = snapshots[-1]
    target_path = runtime_root / "promoted" / "local-skill" / "active" / f"{slug}.md"
    if target_path.exists():
        current_version = int(entry.get("version", 0))
        snapshot = history_snapshot_path(runtime_root, slug, max(current_version, 1))
        shutil.copy2(target_path, snapshot)
    shutil.copy2(latest_snapshot, target_path)

    entry["status"] = "active"
    entry["path"] = str(target_path)
    entry["version"] = int(entry.get("version", 0)) + 1
    entry["last_updated_at"] = now_iso()
    entry["last_action"] = "rollback"
    entry["last_restored_from"] = str(latest_snapshot)
    entry["disable_reason"] = None
    write_local_skill_manifest(runtime_root, manifest)
    return {"slug": slug, "status": "active", "path": str(target_path), "restored_from": str(latest_snapshot)}


def apply_local_skill_working_set_ceiling(
    runtime_root: Path,
    manifest: dict[str, Any],
    ceiling: int,
    touched_slugs: set[str],
) -> list[dict[str, Any]]:
    active_entries = [
        entry
        for entry in manifest.get("entries", {}).values()
        if entry.get("status") == "active" and entry.get("path")
    ]
    if len(active_entries) <= ceiling:
        return []

    active_entries.sort(
        key=lambda entry: (
            entry.get("slug") in touched_slugs,
            len(entry.get("source_session_ids", [])),
            int(entry.get("version", 0)),
            entry.get("last_updated_at", ""),
        )
    )
    overflow = len(active_entries) - ceiling
    archived: list[dict[str, Any]] = []
    for entry in active_entries[:overflow]:
        result = set_local_skill_reference_status(
            runtime_root,
            entry["slug"],
            "archived",
            reason="working_set_ceiling",
        )
        archived.append(result)

    refreshed = load_local_skill_manifest(runtime_root)
    manifest.clear()
    manifest.update(refreshed)
    return archived


def trim_reviewed_history(queue: dict[str, Any], max_items: int) -> None:
    reviewed = queue.setdefault("reviewed", [])
    if len(reviewed) > max_items:
        queue["reviewed"] = reviewed[-max_items:]


def update_runtime_manifest(runtime_root: Path) -> None:
    manifest_path = runtime_root / "state" / "runtime-memory-manifest.json"
    manifest = read_json(manifest_path, {})
    manifest["last_review_at"] = now_iso()
    manifest["last_local_skill_refresh_at"] = now_iso()
    write_json(manifest_path, manifest)


def review_pending(runtime_root: Path) -> dict[str, Any]:
    ensure_runtime_root(runtime_root, RuntimeResolution("generic", runtime_root, "review", "portable"))
    queue_path = runtime_root / "inbox" / "review-queue.json"
    queue = read_json(queue_path, {"pending": [], "reviewed": []})
    policy = load_promotion_policy(runtime_root)
    ledger_path = runtime_root / "state" / "promotion-ledger.json"
    ledger = read_json(
        ledger_path,
        {"version": 2, "created_at": now_iso(), "updated_at": now_iso(), "runs": [], "note_stats": {}},
    )
    local_manifest = load_local_skill_manifest(runtime_root)

    pending = parse_pending(queue)
    pending_before = len(pending)
    backlog_threshold = int(policy.get("backlog_threshold", 10))
    default_batch_size = int(policy.get("default_batch_size", 5))
    backlog_triggered = pending_before >= backlog_threshold
    batch_size = pending_before if backlog_triggered else min(default_batch_size, pending_before)

    to_review = pending[:batch_size]
    queue["pending"] = [
        {
            "capture_file": str(item.capture_file),
            "session_id": item.session_id,
            "scene": item.scene,
            "schema_version": item.schema_version,
            "domain_direction": item.domain_direction,
            "matched_profile": item.matched_profile,
            "support_tier": item.support_tier,
            "deliverable_type": item.deliverable_type,
            "asset_completion_mode": item.asset_completion_mode,
            "content_language": item.content_language,
            "allowed_text_scope": item.allowed_text_scope,
            "layout_owner": item.layout_owner,
            "acceptance_bar": item.acceptance_bar,
            "contract_alignment_result": item.contract_alignment_result,
            "completion_readiness_result": item.completion_readiness_result,
            "repair_class": item.repair_class,
            "legacy_use_case": item.legacy_use_case,
            "promotion_hint": item.promotion_hint,
            "timestamp": item.timestamp,
        }
        for item in pending[batch_size:]
    ]

    notes = load_field_notes(runtime_root, ledger)
    note_by_slug = {note.slug: note for note in notes}
    touched_local_skill_slugs: set[str] = set()
    reviewed_items: list[dict[str, Any]] = []
    actions = {
        "archive": 0,
        "keep_raw": 0,
        "promote_to_field_note": 0,
        "merge_into_existing_note": 0,
        "promote_to_local_skill_reference": 0,
        "update_local_skill_reference": 0,
        "skip_local_skill": 0,
    }

    for item in to_review:
        record = find_record_by_session(runtime_root, item.session_id)
        if not record:
            queue["pending"].append(
                {
                    "capture_file": str(item.capture_file),
                    "session_id": item.session_id,
                    "scene": item.scene,
                    "schema_version": item.schema_version,
                    "domain_direction": item.domain_direction,
                    "matched_profile": item.matched_profile,
                    "support_tier": item.support_tier,
                    "deliverable_type": item.deliverable_type,
                    "asset_completion_mode": item.asset_completion_mode,
                    "content_language": item.content_language,
                    "allowed_text_scope": item.allowed_text_scope,
                    "layout_owner": item.layout_owner,
                    "acceptance_bar": item.acceptance_bar,
                    "contract_alignment_result": item.contract_alignment_result,
                    "completion_readiness_result": item.completion_readiness_result,
                    "repair_class": item.repair_class,
                    "legacy_use_case": item.legacy_use_case,
                    "promotion_hint": item.promotion_hint,
                    "timestamp": item.timestamp,
                }
            )
            continue

        record["capture_file"] = str(item.capture_file)
        score, signals = score_runtime_record(runtime_root, record)
        low_value, low_value_reason = should_archive_low_value(record, policy)
        best_note, best_similarity, match_evidence = find_best_field_note_match(
            record,
            list(note_by_slug.values()),
            policy,
        )

        action = "keep_raw"
        reason = None
        target_path = None
        local_skill_result = None

        if low_value:
            action = "archive"
            reason = low_value_reason
            record["archive_reason"] = low_value_reason
            target_path = str(write_archive_record(runtime_root, record, low_value_reason or "policy archive"))
        elif score < int(policy.get("promote_min_score", 3)):
            action = "keep_raw"
            reason = f"score {score} stayed below promote threshold"
        else:
            merged = False
            if best_note and best_similarity >= float(policy.get("merge_similarity_threshold", 0.36)):
                merged_note = merge_field_note(best_note, record, ledger)
                note_by_slug[merged_note.slug] = merged_note
                target_path = str(merged_note.path)
                evidence_suffix = ""
                if match_evidence:
                    evidence_suffix = (
                        f" [scene_family_exact={match_evidence['scene_family_exact']},"
                        f" metadata_score={match_evidence['metadata_score']},"
                        f" text_overlap={match_evidence['text_overlap']}]"
                    )
                if best_similarity >= float(policy.get("dedup_similarity_threshold", 0.52)):
                    reason = (
                        f"merged into existing note `{best_note.slug}` by strong similarity "
                        f"{best_similarity:.2f}{evidence_suffix}"
                    )
                else:
                    reason = (
                        f"merged into existing note `{best_note.slug}` by soft similarity "
                        f"{best_similarity:.2f}{evidence_suffix}"
                    )
                action = "merge_into_existing_note"
                merged = True
                source_note = merged_note
            else:
                source_note = create_field_note(runtime_root, record, score, signals, ledger)
                note_by_slug[source_note.slug] = source_note
                target_path = str(source_note.path)
                action = "promote_to_field_note"
                reason = "record met field-note gate"

            local_skill_allowed, gate_checks = local_skill_gate(record, score, signals, policy)
            if local_skill_allowed:
                local_skill_result = upsert_local_skill_reference(
                    runtime_root,
                    local_manifest,
                    source_note,
                    record,
                    score,
                    signals,
                )
                actions[local_skill_result["action"]] = actions.get(local_skill_result["action"], 0) + 1
                if local_skill_result["action"] != "skip_local_skill":
                    touched_local_skill_slugs.add(source_note.slug)
            else:
                local_skill_result = {
                    "action": "skip_local_skill",
                    "status": "gated",
                    "reason": "did not meet local skill gate",
                    "gate_checks": gate_checks,
                }
                actions["skip_local_skill"] += 1

            if merged:
                note_by_slug[source_note.slug] = source_note

        actions[action] = actions.get(action, 0) + 1
        reviewed = {
            "timestamp": now_iso(),
            "session_id": record.get("session_id"),
            "scene": record.get("scene"),
            "schema_version": record.get("schema_version", CAPTURE_SCHEMA_VERSION),
            "domain_direction": record.get("domain_direction", "unspecified"),
            "matched_profile": record.get("matched_profile", "none"),
            "support_tier": record.get("support_tier", "unspecified"),
            "deliverable_type": record.get("deliverable_type", "unspecified"),
            "asset_completion_mode": record.get("asset_completion_mode", "unspecified"),
            "content_language": record.get("content_language", "unspecified"),
            "allowed_text_scope": record.get("allowed_text_scope", "unspecified"),
            "layout_owner": record.get("layout_owner", "unspecified"),
            "acceptance_bar": record.get("acceptance_bar", "unspecified"),
            "contract_alignment_result": record.get("contract_alignment_result"),
            "completion_readiness_result": record.get("completion_readiness_result"),
            "repair_class": record.get("repair_class"),
            "legacy_use_case": record.get("legacy_use_case", record.get("use_case")),
            "promotion_hint": record.get("promotion_hint"),
            "score": score,
            "signals": signals,
            "action": action,
            "reason": reason,
            "target_path": target_path,
            "match_evidence": match_evidence,
            "local_skill": local_skill_result,
            "repo_candidate_auto_write": False,
        }
        reviewed_items.append(reviewed)
        queue.setdefault("reviewed", []).append(reviewed)

    write_local_skill_manifest(runtime_root, local_manifest)

    overflow_archives = apply_local_skill_working_set_ceiling(
        runtime_root,
        local_manifest,
        int(policy.get("local_skill_working_set_ceiling", 4)),
        touched_local_skill_slugs,
    )
    if overflow_archives:
        actions["archive_local_skill_overflow"] = len(overflow_archives)

    trim_reviewed_history(queue, int(policy.get("max_reviewed_history", 200)))
    write_json(queue_path, queue)
    write_json(ledger_path, ledger)
    write_local_skill_manifest(runtime_root, local_manifest)
    update_runtime_manifest(runtime_root)

    run_summary = {
        "run_id": f"promotion-run-{datetime.now().astimezone().strftime('%Y%m%dT%H%M%S')}",
        "timestamp": now_iso(),
        "pending_before": pending_before,
        "pending_after": len(queue.get("pending", [])),
        "backlog_triggered": backlog_triggered,
        "batch_size": batch_size,
        "actions": actions,
        "overflow_archives": overflow_archives,
        "reviewed_items": reviewed_items,
        "repo_candidate_auto_write": False,
    }
    ledger["updated_at"] = now_iso()
    ledger["last_run_id"] = run_summary["run_id"]
    ledger.setdefault("runs", []).append(run_summary)
    write_json(ledger_path, ledger)
    return run_summary


def metadata_matches(
    scene_value: str,
    failure_value: str,
    domain_value: str,
    profile_value: str,
    tier_value: str,
    deliverable_value: str,
    completion_value: str,
    language_value: str,
    layout_owner_value: str,
    text_scope_value: str,
    contract_result_value: str,
    readiness_result_value: str,
    repair_class_value: str,
    *,
    scene: str | None,
    failure_mode: str | None,
    domain_direction: str | None,
    matched_profile: str | None,
    support_tier: str | None,
    deliverable_type: str | None,
    asset_completion_mode: str | None,
    content_language: str | None,
    layout_owner: str | None,
    allowed_text_scope: str | None,
    contract_alignment_result: str | None,
    completion_readiness_result: str | None,
    repair_class: str | None,
    text: str = "",
) -> bool:
    scene_hit = scene is None or scene.lower() in scene_value.lower() or scene.lower() in text.lower()
    failure_hit = failure_mode is None or failure_mode.lower() in failure_value.lower() or failure_mode.lower() in text.lower()
    domain_hit = domain_direction is None or domain_direction.lower() in domain_value.lower() or domain_direction.lower() in text.lower()
    profile_hit = matched_profile is None or profile_value.lower() == matched_profile.lower()
    tier_hit = support_tier is None or tier_value.lower() == support_tier.lower()
    deliverable_hit = (
        deliverable_type is None
        or deliverable_type.lower() in deliverable_value.lower()
        or deliverable_type.lower() in text.lower()
    )
    completion_hit = asset_completion_mode is None or completion_value.lower() == asset_completion_mode.lower()
    language_hit = content_language is None or language_value.lower() == content_language.lower()
    layout_hit = layout_owner is None or layout_owner_value.lower() == layout_owner.lower()
    text_scope_hit = (
        allowed_text_scope is None
        or allowed_text_scope.lower() in text_scope_value.lower()
        or allowed_text_scope.lower() in text.lower()
    )
    contract_result_hit = (
        contract_alignment_result is None
        or contract_result_value.lower() == contract_alignment_result.lower()
        or contract_alignment_result.lower() in text.lower()
    )
    readiness_result_hit = (
        completion_readiness_result is None
        or readiness_result_value.lower() == completion_readiness_result.lower()
        or completion_readiness_result.lower() in text.lower()
    )
    repair_class_hit = (
        repair_class is None
        or repair_class_value.lower() == repair_class.lower()
        or repair_class.lower() in text.lower()
    )
    return (
        scene_hit
        and failure_hit
        and domain_hit
        and profile_hit
        and tier_hit
        and deliverable_hit
        and completion_hit
        and language_hit
        and layout_hit
        and text_scope_hit
        and contract_result_hit
        and readiness_result_hit
        and repair_class_hit
    )


def collect_local_skill_references(
    runtime_root: Path,
    *,
    scene: str | None,
    failure_mode: str | None,
    domain_direction: str | None,
    matched_profile: str | None,
    support_tier: str | None,
    deliverable_type: str | None,
    asset_completion_mode: str | None,
    content_language: str | None,
    layout_owner: str | None,
    allowed_text_scope: str | None,
    contract_alignment_result: str | None,
    completion_readiness_result: str | None,
    repair_class: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    manifest = load_local_skill_manifest(runtime_root)
    items: list[dict[str, Any]] = []
    for entry in manifest.get("entries", {}).values():
        if entry.get("status") != "active" or not entry.get("path"):
            continue
        path = resolve_local_skill_path(runtime_root, entry["slug"], entry.get("path"))
        if path is None:
            continue
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if not metadata_matches(
            entry.get("scene", ""),
            "",
            entry.get("domain_direction", ""),
            entry.get("matched_profile", "none"),
            entry.get("support_tier", "unspecified"),
            entry.get("deliverable_type", "unspecified"),
            entry.get("asset_completion_mode", "unspecified"),
            entry.get("content_language", "unspecified"),
            entry.get("layout_owner", "unspecified"),
            entry.get("allowed_text_scope", "unspecified"),
            "",
            "",
            "",
            scene=scene,
            failure_mode=failure_mode,
            domain_direction=domain_direction,
            matched_profile=matched_profile,
            support_tier=support_tier,
            deliverable_type=deliverable_type,
            asset_completion_mode=asset_completion_mode,
            content_language=content_language,
            layout_owner=layout_owner,
            allowed_text_scope=allowed_text_scope,
            contract_alignment_result=contract_alignment_result,
            completion_readiness_result=completion_readiness_result,
            repair_class=repair_class,
            text=text,
        ):
            continue
        items.append(
            {
                "source_layer": "local_skill_reference",
                "slug": entry["slug"],
                "path": str(path),
                "status": entry["status"],
                "scene": entry.get("scene"),
                "domain_direction": entry.get("domain_direction"),
                "matched_profile": entry.get("matched_profile"),
                "support_tier": entry.get("support_tier"),
                "deliverable_type": entry.get("deliverable_type"),
                "asset_completion_mode": entry.get("asset_completion_mode"),
                "content_language": entry.get("content_language"),
                "allowed_text_scope": entry.get("allowed_text_scope"),
                "layout_owner": entry.get("layout_owner"),
                "acceptance_bar": entry.get("acceptance_bar"),
                "version": entry.get("version"),
                "summary": text.splitlines()[:18],
            }
        )
        if len(items) >= limit:
            break
    return items


def collect_field_notes(
    runtime_root: Path,
    ledger: dict[str, Any],
    *,
    scene: str | None,
    failure_mode: str | None,
    domain_direction: str | None,
    matched_profile: str | None,
    support_tier: str | None,
    deliverable_type: str | None,
    asset_completion_mode: str | None,
    content_language: str | None,
    layout_owner: str | None,
    allowed_text_scope: str | None,
    contract_alignment_result: str | None,
    completion_readiness_result: str | None,
    repair_class: str | None,
    limit: int,
    excluded_slugs: set[str],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for note in load_field_notes(runtime_root, ledger):
        if note.slug in excluded_slugs:
            continue
        if not metadata_matches(
            note.scene,
            "",
            note.domain_direction,
            note.matched_profile,
            note.support_tier,
            note.deliverable_type,
            note.asset_completion_mode,
            note.content_language,
            note.layout_owner,
            note.allowed_text_scope,
            "",
            "",
            "",
            scene=scene,
            failure_mode=failure_mode,
            domain_direction=domain_direction,
            matched_profile=matched_profile,
            support_tier=support_tier,
            deliverable_type=deliverable_type,
            asset_completion_mode=asset_completion_mode,
            content_language=content_language,
            layout_owner=layout_owner,
            allowed_text_scope=allowed_text_scope,
            contract_alignment_result=contract_alignment_result,
            completion_readiness_result=completion_readiness_result,
            repair_class=repair_class,
            text=note.text,
        ):
            continue
        items.append(
            {
                "source_layer": "field_note",
                "slug": note.slug,
                "path": str(note.path),
                "scene": note.scene,
                "domain_direction": note.domain_direction,
                "matched_profile": note.matched_profile,
                "support_tier": note.support_tier,
                "deliverable_type": note.deliverable_type,
                "asset_completion_mode": note.asset_completion_mode,
                "content_language": note.content_language,
                "allowed_text_scope": note.allowed_text_scope,
                "layout_owner": note.layout_owner,
                "acceptance_bar": note.acceptance_bar,
                "summary": note.text.splitlines()[:18],
            }
        )
        if len(items) >= limit:
            break
    return items


def collect_captures(
    runtime_root: Path,
    *,
    scene: str | None,
    failure_mode: str | None,
    domain_direction: str | None,
    matched_profile: str | None,
    support_tier: str | None,
    deliverable_type: str | None,
    asset_completion_mode: str | None,
    content_language: str | None,
    layout_owner: str | None,
    allowed_text_scope: str | None,
    contract_alignment_result: str | None,
    completion_readiness_result: str | None,
    repair_class: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for record in reversed(iter_capture_records(runtime_root)):
        if not metadata_matches(
            record.get("scene", ""),
            record.get("failure_class", ""),
            record.get("domain_direction", ""),
            record.get("matched_profile", "none"),
            record.get("support_tier", "unspecified"),
            record.get("deliverable_type", "unspecified"),
            record.get("asset_completion_mode", "unspecified"),
            record.get("content_language", "unspecified"),
            record.get("layout_owner", "unspecified"),
            record.get("allowed_text_scope", "unspecified"),
            record.get("contract_alignment_result", ""),
            record.get("completion_readiness_result", ""),
            record.get("repair_class", ""),
            scene=scene,
            failure_mode=failure_mode,
            domain_direction=domain_direction,
            matched_profile=matched_profile,
            support_tier=support_tier,
            deliverable_type=deliverable_type,
            asset_completion_mode=asset_completion_mode,
            content_language=content_language,
            layout_owner=layout_owner,
            allowed_text_scope=allowed_text_scope,
            contract_alignment_result=contract_alignment_result,
            completion_readiness_result=completion_readiness_result,
            repair_class=repair_class,
            text=combined_record_text(record),
        ):
            continue
        copy = dict(record)
        copy["source_layer"] = "capture"
        items.append(copy)
        if len(items) >= limit:
            break
    return items


def search_runtime_context(
    runtime_root: Path,
    scene: str | None = None,
    failure_mode: str | None = None,
    domain_direction: str | None = None,
    matched_profile: str | None = None,
    support_tier: str | None = None,
    deliverable_type: str | None = None,
    asset_completion_mode: str | None = None,
    content_language: str | None = None,
    layout_owner: str | None = None,
    allowed_text_scope: str | None = None,
    contract_alignment_result: str | None = None,
    completion_readiness_result: str | None = None,
    repair_class: str | None = None,
    limit: int = 5,
    include_local_skill: bool = True,
) -> dict[str, Any]:
    policy = load_promotion_policy(runtime_root)
    ledger = read_json(runtime_root / "state" / "promotion-ledger.json", {"note_stats": {}})
    local_skill_limit = min(limit, int(policy.get("max_local_skill_reads", 3)))
    field_note_limit = min(limit, int(policy.get("max_promoted_reads", 3)))
    capture_limit = min(limit, int(policy.get("max_raw_reads", 5)))

    local_skill_items = []
    if include_local_skill:
        local_skill_items = collect_local_skill_references(
            runtime_root,
            scene=scene,
            failure_mode=failure_mode,
            domain_direction=domain_direction,
            matched_profile=matched_profile,
            support_tier=support_tier,
            deliverable_type=deliverable_type,
            asset_completion_mode=asset_completion_mode,
            content_language=content_language,
            layout_owner=layout_owner,
            allowed_text_scope=allowed_text_scope,
            contract_alignment_result=contract_alignment_result,
            completion_readiness_result=completion_readiness_result,
            repair_class=repair_class,
            limit=local_skill_limit,
        )

    excluded_slugs = {item["slug"] for item in local_skill_items if item.get("slug")}
    field_note_items = collect_field_notes(
        runtime_root,
        ledger,
        scene=scene,
        failure_mode=failure_mode,
        domain_direction=domain_direction,
        matched_profile=matched_profile,
        support_tier=support_tier,
        deliverable_type=deliverable_type,
        asset_completion_mode=asset_completion_mode,
        content_language=content_language,
        layout_owner=layout_owner,
        allowed_text_scope=allowed_text_scope,
        contract_alignment_result=contract_alignment_result,
        completion_readiness_result=completion_readiness_result,
        repair_class=repair_class,
        limit=field_note_limit,
        excluded_slugs=excluded_slugs,
    )
    capture_items = collect_captures(
        runtime_root,
        scene=scene,
        failure_mode=failure_mode,
        domain_direction=domain_direction,
        matched_profile=matched_profile,
        support_tier=support_tier,
        deliverable_type=deliverable_type,
        asset_completion_mode=asset_completion_mode,
        content_language=content_language,
        layout_owner=layout_owner,
        allowed_text_scope=allowed_text_scope,
        contract_alignment_result=contract_alignment_result,
        completion_readiness_result=completion_readiness_result,
        repair_class=repair_class,
        limit=capture_limit,
    )
    ordered = (local_skill_items + field_note_items + capture_items)[:limit]
    return {
        "count": len(ordered),
        "items": ordered,
        "read_chain": ["local_skill_reference", "field_note", "capture"] if include_local_skill else ["field_note", "capture"],
        "local_skill_references": local_skill_items,
        "field_notes": field_note_items,
        "captures": capture_items,
        "repo_candidate_auto_write": False,
    }
