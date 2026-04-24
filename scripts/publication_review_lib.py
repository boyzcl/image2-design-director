from __future__ import annotations

from typing import Any


ARTIFACT_ROLES = {"internal_candidate", "review_candidate", "publication_asset"}
PUBLICATION_REVIEW_RESULTS = {"pass", "conditional_pass", "fail"}
VISUAL_QUALITY_REVIEW_RESULTS = {"pass", "conditional_pass", "fail"}
FINAL_RELEASE_RESULTS = {"pass", "conditional_pass", "fail"}
INTERNAL_ONLY_ARTIFACT_CLASSES = {
    "benchmark_candidate",
    "delivery_bundle_artifact",
    "overlay_demo",
    "exploratory_repair_output",
}
EDITORIAL_DELIVERABLE_TYPES = {
    "wechat_article_editorial_visual_set",
    "editorial_publication_visual",
}
EDITORIAL_USAGE_KEYWORDS = (
    "wechat article",
    "editorial publication",
    "article publication",
    "publication figure",
    "editorial cover",
    "editorial",
    "article",
)
REQUIRED_EDITORIAL_PROTECTED_REGIONS = (
    "title_region",
    "core_subject_region",
    "focus_information_region",
)
PROMOTIONAL_SIGNAL_KEYWORDS = (
    "报名",
    "扫码",
    "扫描",
    "立即",
    "限时",
    "活动",
    "register",
    "signup",
    "sign up",
    "scan",
    "qr",
    "cta",
    "event",
    "today",
)
ARGUMENT_SUPPORT_FRIENDLY_CLASSES = {
    "editorial_publication_asset",
    "editorial_cover_publication_asset",
    "mechanism_figure_publication_asset",
    "workflow_evidence_publication_asset",
}
VISUAL_QUALITY_DIMENSIONS = (
    "text_readability",
    "typographic_craft",
    "layout_hierarchy",
    "semantic_clarity",
    "publication_argument_support_visual",
    "series_consistency",
    "asset_distinctiveness",
    "polish_and_finish",
)
VISUAL_QUALITY_HARD_BLOCKERS = {
    "broken_word",
    "broken_chinese_line",
    "paragraph_overload",
    "template_sameness",
    "weak_article_support",
    "internal_draft_look",
}


def _lower_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return " ".join(_lower_text(item) for item in value)
    return str(value).strip().lower()


def is_editorial_publication_context(
    usage_context: str | None = None,
    deliverable_type: str | None = None,
    scene: str | None = None,
    tags: list[str] | None = None,
) -> bool:
    if _lower_text(deliverable_type) in EDITORIAL_DELIVERABLE_TYPES:
        return True
    haystack = " ".join(
        part
        for part in (
            _lower_text(usage_context),
            _lower_text(scene),
            _lower_text(tags or []),
        )
        if part
    )
    return any(keyword in haystack for keyword in EDITORIAL_USAGE_KEYWORDS)


def default_artifact_role_for_state(state: str) -> str:
    if state == "delivery_ready_visual":
        return "review_candidate"
    return "internal_candidate"


def editorial_region_names(protected_regions: list[dict[str, Any]] | None) -> set[str]:
    return {
        str(region.get("name", "")).strip().lower()
        for region in (protected_regions or [])
        if isinstance(region, dict) and region.get("name")
    }


def required_editorial_regions_present(protected_regions: list[dict[str, Any]] | None) -> bool:
    names = editorial_region_names(protected_regions)
    return all(name in names for name in REQUIRED_EDITORIAL_PROTECTED_REGIONS)


def collect_editorial_residues(
    cta_text: str | None = None,
    date_text: str | None = None,
    badge_text: str | None = None,
    qr_image: str | None = None,
    logo_image: str | None = None,
    allowed_fixed_elements: list[str] | None = None,
    extra_residues: list[str] | None = None,
) -> list[str]:
    allow = {str(item).strip().lower() for item in (allowed_fixed_elements or [])}
    residues = list(extra_residues or [])
    if cta_text and "cta" not in allow:
        residues.append("cta_text")
    if date_text and "date" not in allow:
        residues.append("date_text")
    if badge_text and "badge" not in allow:
        residues.append("badge_text")
    if qr_image and "qr" not in allow and "qr_code" not in allow:
        residues.append("qr_image")
    if logo_image and "logo" not in allow and "primary_logo" not in allow:
        residues.append("logo_image")
    return sorted(set(residues))


def infer_publication_argument_support(
    usage_context: str | None = None,
    deliverable_type: str | None = None,
    artifact_class: str | None = None,
    title: str | None = None,
    supporting_lines: list[str] | None = None,
    scene: str | None = None,
    tags: list[str] | None = None,
    cross_scene_residues: list[str] | None = None,
) -> str:
    if not is_editorial_publication_context(
        usage_context=usage_context,
        deliverable_type=deliverable_type,
        scene=scene,
        tags=tags,
    ):
        return "unclear"

    if cross_scene_residues:
        return "fail"

    combined_text = " ".join(
        part
        for part in (
            _lower_text(title),
            _lower_text(supporting_lines or []),
            _lower_text(scene),
            _lower_text(tags or []),
        )
        if part
    )

    if any(keyword in combined_text for keyword in PROMOTIONAL_SIGNAL_KEYWORDS):
        return "fail"

    if _lower_text(artifact_class) in ARGUMENT_SUPPORT_FRIENDLY_CLASSES and (title or supporting_lines):
        return "pass"

    if title and (supporting_lines or _lower_text(deliverable_type) in EDITORIAL_DELIVERABLE_TYPES):
        return "pass"

    if title:
        return "unclear"

    return "unclear"


def run_publication_readiness_review(
    artifact_role: str,
    artifact_class: str,
    asset_completion_mode: str,
    publication_argument_support: str,
    cross_scene_residues: list[str] | None = None,
    protected_regions: list[dict[str, Any]] | None = None,
    delivery_viability_result: str | None = None,
) -> dict[str, Any]:
    blockers: list[str] = []

    if artifact_role not in ARTIFACT_ROLES:
        raise ValueError(f"unsupported artifact_role: {artifact_role}")
    if publication_argument_support not in {"pass", "unclear", "fail"}:
        raise ValueError(f"unsupported publication_argument_support: {publication_argument_support}")

    residues = sorted(set(cross_scene_residues or []))
    regions_present = required_editorial_regions_present(protected_regions)

    if artifact_class in INTERNAL_ONLY_ARTIFACT_CLASSES:
        asset_identity_result = "fail"
        blockers.append(f"artifact_class_internal_only:{artifact_class}")
    elif asset_completion_mode != "complete_asset":
        asset_identity_result = "fail"
        blockers.append("asset_completion_mode_not_complete_asset")
    elif artifact_role != "publication_asset":
        asset_identity_result = "conditional_pass"
    else:
        asset_identity_result = "pass"

    if publication_argument_support == "pass":
        argument_support_result = "pass"
    elif publication_argument_support == "unclear":
        argument_support_result = "conditional_pass"
    else:
        argument_support_result = "fail"
        blockers.append("article_argument_support_not_established")

    if residues:
        cross_scene_residue_result = "fail"
        blockers.extend(f"cross_scene_residue:{item}" for item in residues)
    else:
        cross_scene_residue_result = "pass"

    if not regions_present:
        blockers.append("missing_required_editorial_protected_regions")

    if delivery_viability_result == "overlay_not_allowed_regenerate":
        blockers.append("delivery_viability_no_go")
    elif delivery_viability_result == "overlay_allowed_with_limits":
        blockers.append("delivery_viability_requires_limits")

    hard_fail = any(
        blocker.startswith("artifact_class_internal_only")
        or blocker == "asset_completion_mode_not_complete_asset"
        or blocker == "article_argument_support_not_established"
        or blocker == "missing_required_editorial_protected_regions"
        or blocker == "delivery_viability_no_go"
        or blocker.startswith("cross_scene_residue:")
        for blocker in blockers
    )

    if hard_fail:
        result = "fail"
    elif asset_identity_result == "conditional_pass" or argument_support_result == "conditional_pass" or blockers:
        result = "conditional_pass"
    else:
        result = "pass"

    return {
        "result": result,
        "asset_identity_result": asset_identity_result,
        "argument_support_result": argument_support_result,
        "cross_scene_residue_result": cross_scene_residue_result,
        "artifact_role_check": artifact_role,
        "artifact_class": artifact_class,
        "required_editorial_regions_present": regions_present,
        "delivery_viability_result": delivery_viability_result,
        "cross_scene_residues": residues,
        "publication_blockers": blockers,
    }


def run_visual_quality_review(
    dimension_scores: dict[str, Any],
    blockers: list[str] | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    normalized_scores: dict[str, float] = {}
    review_blockers = sorted(set(blockers or []))
    review_notes = list(notes or [])

    for dimension in VISUAL_QUALITY_DIMENSIONS:
        value = dimension_scores.get(dimension, 0)
        try:
            score = float(value)
        except (TypeError, ValueError):
            score = 0.0
        normalized_scores[dimension] = max(0.0, min(5.0, score))

    total = round(
        sum(normalized_scores.values()) / (len(VISUAL_QUALITY_DIMENSIONS) * 5.0) * 100.0,
        1,
    )
    hard_blockers = sorted(set(review_blockers) & VISUAL_QUALITY_HARD_BLOCKERS)

    if hard_blockers or total < 70:
        result = "fail"
    elif review_blockers or total < 85:
        result = "conditional_pass"
    else:
        result = "pass"

    return {
        "result": result,
        "score": total,
        "dimension_scores": normalized_scores,
        "visual_quality_blockers": review_blockers,
        "hard_visual_quality_blockers": hard_blockers,
        "notes": review_notes,
    }


def run_final_release_gate(
    production_preflight_result: str | None,
    publication_review_result: str | None,
    visual_quality_review_result: str | None,
    delivery_viability_result: str | None,
    runtime_capture_present: bool,
) -> dict[str, Any]:
    blockers: list[str] = []

    if production_preflight_result != "pass":
        blockers.append("production_preflight_not_pass")
    if publication_review_result != "pass":
        blockers.append("publication_review_not_pass")
    if visual_quality_review_result != "pass":
        blockers.append("visual_quality_review_not_pass")
    if delivery_viability_result == "overlay_not_allowed_regenerate":
        blockers.append("delivery_viability_no_go")
    if not runtime_capture_present:
        blockers.append("runtime_capture_missing")

    if not blockers:
        result = "pass"
    elif publication_review_result == "fail" or visual_quality_review_result == "fail":
        result = "fail"
    else:
        result = "conditional_pass"

    return {
        "result": result,
        "final_release_blockers": blockers,
        "production_preflight_result": production_preflight_result,
        "publication_review_result": publication_review_result,
        "visual_quality_review_result": visual_quality_review_result,
        "delivery_viability_result": delivery_viability_result,
        "runtime_capture_present": bool(runtime_capture_present),
    }
