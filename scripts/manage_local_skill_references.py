from __future__ import annotations

import argparse
import json

from runtime_memory_lib import (
    load_local_skill_manifest,
    resolve_runtime_resolution,
    rollback_local_skill_reference,
    set_local_skill_reference_status,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage active, disabled, archived, and rolled-back local skill references."
    )
    parser.add_argument("--host", default=None, help="Optional host id for metadata or host-specific env resolution.")
    parser.add_argument("--root", default=None, help="Override the runtime root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show the local skill reference manifest.")

    disable_parser = subparsers.add_parser("disable", help="Disable a local skill reference.")
    disable_parser.add_argument("--slug", required=True, help="Local skill reference slug.")
    disable_parser.add_argument("--reason", default=None, help="Optional disable reason.")

    enable_parser = subparsers.add_parser("enable", help="Re-enable a disabled or archived local skill reference.")
    enable_parser.add_argument("--slug", required=True, help="Local skill reference slug.")
    enable_parser.add_argument("--reason", default=None, help="Optional enable reason.")

    archive_parser = subparsers.add_parser("archive", help="Archive a local skill reference.")
    archive_parser.add_argument("--slug", required=True, help="Local skill reference slug.")
    archive_parser.add_argument("--reason", default=None, help="Optional archive reason.")

    rollback_parser = subparsers.add_parser("rollback", help="Restore the latest saved local skill snapshot.")
    rollback_parser.add_argument("--slug", required=True, help="Local skill reference slug.")

    args = parser.parse_args()
    resolution = resolve_runtime_resolution(host=args.host, root=args.root)

    if args.command == "status":
        print(json.dumps(load_local_skill_manifest(resolution.runtime_root), ensure_ascii=False, indent=2))
        return 0

    if args.command == "disable":
        result = set_local_skill_reference_status(
            resolution.runtime_root,
            args.slug,
            "disabled",
            reason=args.reason,
        )
    elif args.command == "enable":
        result = set_local_skill_reference_status(
            resolution.runtime_root,
            args.slug,
            "active",
            reason=args.reason,
        )
    elif args.command == "archive":
        result = set_local_skill_reference_status(
            resolution.runtime_root,
            args.slug,
            "archived",
            reason=args.reason,
        )
    else:
        result = rollback_local_skill_reference(resolution.runtime_root, args.slug)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
