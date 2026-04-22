from __future__ import annotations

import argparse

from runtime_memory_lib import ensure_runtime_root, resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize image2-design-director runtime memory.")
    parser.add_argument("--host", default=None, help="Optional host id for metadata or host-specific env resolution.")
    parser.add_argument("--root", default=None, help="Override the runtime root")
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    result = ensure_runtime_root(resolution.runtime_root, resolution)
    print(
        "initialized runtime root: "
        f"{result['runtime_root']} "
        f"(host={resolution.host_id}, source={resolution.source}, tier={resolution.support_tier})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
