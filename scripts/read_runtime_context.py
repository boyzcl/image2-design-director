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
        limit=args.limit,
        include_local_skill=not args.raw_only,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
