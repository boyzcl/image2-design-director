from __future__ import annotations

from typing import Any


SUPPORTED_FIGURE_ROLES = {
    "editorial_cover",
    "base_visual",
    "mechanism_figure",
    "workflow_evidence",
    "advance_figure",
    "evidence_figure",
    "data_figure",
    "price_figure",
    "ranking_figure",
}
SUPPORTED_REPRESENTATION_MODES = {
    "model_direct_visual",
    "model_visual_with_limited_text",
    "visual_base_plus_post",
    "hybrid_visual_plus_deterministic_overlay",
    "deterministic_render",
}
SUPPORTED_LAYOUT_OWNERS = {"model", "deterministic_renderer", "hybrid"}
SUPPORTED_TEXT_OWNERS = {"model", "deterministic_overlay", "deterministic_renderer"}
SUPPORTED_CANDIDATE_POLICIES = {"single", "multi_candidate"}
SUPPORTED_REPAIR_POLICIES = {"micro_repair", "regenerate", "contract_realign"}
DIRECT_FIRST_FIGURE_ROLES = {
    "editorial_cover",
    "base_visual",
    "mechanism_figure",
    "workflow_evidence",
    "advance_figure",
    "evidence_figure",
    "data_figure",
    "price_figure",
    "ranking_figure",
}
FACT_SENSITIVE_FIGURE_ROLES = {"data_figure", "price_figure", "ranking_figure"}
SURGICAL_POSTPROCESS_SCOPES = {
    "none",
    "qr_code",
    "logo",
    "exact_copy",
    "locked_value_replacement",
    "export_adaptation",
}

REQUIRED_WORKFLOW_EVIDENCE = {
    "runtime_capture",
    "scorecard",
    "delivery_bundle",
    "route_trace",
    "accepted_asset_state",
}


def _as_text(value: Any) -> str:
    return str(value or "").strip()


def _as_set(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        return {_as_text(value)}
    if isinstance(value, (list, tuple, set)):
        return {_as_text(item) for item in value if _as_text(item)}
    return {_as_text(value)}


def _budget(packet: dict[str, Any], key: str, default: int = 0) -> int:
    text_budget = packet.get("text_budget") or {}
    if not isinstance(text_budget, dict):
        return default
    try:
        return int(text_budget.get(key, default) or 0)
    except (TypeError, ValueError):
        return default


def _has_override(packet: dict[str, Any], override: str) -> bool:
    return override in _as_set(packet.get("explicit_overrides"))


def run_production_preflight(packet: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []

    figure_role = _as_text(packet.get("figure_role"))
    representation_mode = _as_text(packet.get("representation_mode"))
    layout_owner = _as_text(packet.get("layout_owner"))
    text_owner = _as_text(packet.get("text_owner"))
    candidate_policy = _as_text(packet.get("candidate_policy"))
    repair_policy = _as_text(packet.get("repair_policy"))
    asset_goal = _as_text(packet.get("asset_goal"))
    visual_structure = _as_text(packet.get("visual_structure"))
    forbidden_drift = _as_set(packet.get("forbidden_drift"))
    required_visual_evidence = _as_set(packet.get("required_visual_evidence"))
    postprocess_scope = _as_set(packet.get("postprocess_scope"))
    reliability_gate_result = _as_text(packet.get("information_reliability_gate_result"))

    if figure_role not in SUPPORTED_FIGURE_ROLES:
        blockers.append("unsupported_or_missing_figure_role")
    if not asset_goal:
        blockers.append("missing_asset_goal")
    if representation_mode not in SUPPORTED_REPRESENTATION_MODES:
        blockers.append("unsupported_or_missing_representation_mode")
    if layout_owner not in SUPPORTED_LAYOUT_OWNERS:
        blockers.append("unsupported_or_missing_layout_owner")
    if text_owner not in SUPPORTED_TEXT_OWNERS:
        blockers.append("unsupported_or_missing_text_owner")
    if candidate_policy not in SUPPORTED_CANDIDATE_POLICIES:
        blockers.append("unsupported_or_missing_candidate_policy")
    if repair_policy and repair_policy not in SUPPORTED_REPAIR_POLICIES:
        blockers.append("unsupported_repair_policy")
    if not repair_policy:
        warnings.append("missing_repair_policy")
    if not visual_structure:
        warnings.append("missing_visual_structure")
    if not forbidden_drift:
        blockers.append("missing_forbidden_drift")
    unsupported_postprocess_scopes = sorted(postprocess_scope - SURGICAL_POSTPROCESS_SCOPES)
    if unsupported_postprocess_scopes:
        blockers.extend(f"unsupported_postprocess_scope:{item}" for item in unsupported_postprocess_scopes)
    if "full_layout_rebuild" in postprocess_scope:
        blockers.append("postprocess_scope_full_layout_rebuild")

    headline_budget = _budget(packet, "headline")
    subtitle_budget = _budget(packet, "subtitle")
    node_labels_budget = _budget(packet, "node_labels")
    paragraphs_budget = _budget(packet, "paragraphs")

    if headline_budget > 1:
        blockers.append("headline_budget_too_high")
    if subtitle_budget > 1:
        warnings.append("subtitle_budget_above_default")
    if paragraphs_budget > 0:
        warnings.append("paragraph_text_budget_present")

    if figure_role in DIRECT_FIRST_FIGURE_ROLES:
        direct_first_mode = representation_mode in {"model_direct_visual", "model_visual_with_limited_text"}
        surgical_postprocess_mode = representation_mode in {
            "visual_base_plus_post",
            "hybrid_visual_plus_deterministic_overlay",
        } and bool(postprocess_scope & (SURGICAL_POSTPROCESS_SCOPES - {"none"}))
        explicit_deterministic = representation_mode == "deterministic_render" and _has_override(
            packet,
            "allow_deterministic_render",
        )
        if not (direct_first_mode or surgical_postprocess_mode or explicit_deterministic):
            blockers.append("direct_first_route_not_established")

    if figure_role in FACT_SENSITIVE_FIGURE_ROLES:
        if reliability_gate_result != "verified_fact":
            blockers.append("information_reliability_gate_not_verified")

    if figure_role == "editorial_cover":
        if representation_mode == "deterministic_render" and not _has_override(packet, "allow_deterministic_cover"):
            blockers.append("cover_visual_energy_risk")
        if candidate_policy != "multi_candidate":
            blockers.append("cover_requires_multi_candidate")

    if figure_role == "mechanism_figure":
        if paragraphs_budget > 0:
            blockers.append("mechanism_text_density_too_high")
        if node_labels_budget > 8:
            warnings.append("mechanism_node_label_budget_high")

    if figure_role == "workflow_evidence":
        missing_evidence = sorted(REQUIRED_WORKFLOW_EVIDENCE - required_visual_evidence)
        if missing_evidence:
            blockers.extend(f"workflow_evidence_object_missing:{item}" for item in missing_evidence)
        if candidate_policy != "multi_candidate":
            blockers.append("workflow_evidence_requires_multi_candidate")
        if representation_mode == "deterministic_render" and not _has_override(packet, "allow_deterministic_workflow"):
            blockers.append("workflow_needs_hybrid_evidence_visual")
        if representation_mode == "deterministic_render" and _has_override(packet, "allow_deterministic_workflow"):
            warnings.append("workflow_deterministic_override_used")

    if blockers:
        result = "fail"
    elif warnings:
        result = "conditional_pass"
    else:
        result = "pass"

    return {
        "production_preflight_result": result,
        "production_preflight_blockers": blockers,
        "production_preflight_warnings": warnings,
        "figure_role": figure_role,
        "representation_mode": representation_mode,
        "layout_owner": layout_owner,
        "text_owner": text_owner,
        "candidate_policy": candidate_policy,
        "repair_policy": repair_policy,
        "postprocess_scope": sorted(postprocess_scope),
        "information_reliability_gate_result": reliability_gate_result or None,
    }
