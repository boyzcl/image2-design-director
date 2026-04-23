from __future__ import annotations

import argparse
import json

from runtime_memory_lib import resolve_runtime_resolution, search_runtime_context


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read related runtime context for image2-design-director."
    )
    parser.add_argument("--host", default=None, help="Optional host id for metadata or host-specific env resolution.")
    parser.add_argument("--root", default=None, help="Override the runtime root")
    parser.add_argument("--scene", default=None, help="Scene substring to match")
    parser.add_argument("--failure-mode", default=None, help="Failure class substring to match")
    parser.add_argument("--domain-direction", default=None, help="Domain direction substring to match")
    parser.add_argument("--matched-profile", default=None, help="Matched profile to match")
    parser.add_argument("--support-tier", default=None, help="Support tier to match")
    parser.add_argument("--deliverable-type", default=None, help="Deliverable type substring to match")
    parser.add_argument("--asset-completion-mode", default=None, help="Asset completion mode to match")
    parser.add_argument("--content-language", default=None, help="Content language to match")
    parser.add_argument("--layout-owner", default=None, help="Layout owner to match")
    parser.add_argument("--allowed-text-scope", default=None, help="Allowed text scope substring to match")
    parser.add_argument("--contract-alignment-result", default=None, help="Contract alignment result to match")
    parser.add_argument("--completion-readiness-result", default=None, help="Completion readiness result to match")
    parser.add_argument("--repair-class", default=None, help="Repair class to match")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of matches")
    parser.add_argument(
        "--raw-only",
        action="store_true",
        help="Skip the local skill reference layer and read only field notes plus raw captures.",
    )
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    result = search_runtime_context(
        resolution.runtime_root,
        scene=args.scene,
        failure_mode=args.failure_mode,
        domain_direction=args.domain_direction,
        matched_profile=args.matched_profile,
        support_tier=args.support_tier,
        deliverable_type=args.deliverable_type,
        asset_completion_mode=args.asset_completion_mode,
        content_language=args.content_language,
        layout_owner=args.layout_owner,
        allowed_text_scope=args.allowed_text_scope,
        contract_alignment_result=args.contract_alignment_result,
        completion_readiness_result=args.completion_readiness_result,
        repair_class=args.repair_class,
        limit=args.limit,
        include_local_skill=not args.raw_only,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
