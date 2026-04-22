from __future__ import annotations

import argparse
import json

from runtime_memory_lib import resolve_runtime_resolution, review_pending


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Review pending image2-design-director runtime captures and "
            "auto-promote eligible notes into the local skill reference layer."
        )
    )
    parser.add_argument("--host", default=None, help="Optional host id for metadata or host-specific env resolution.")
    parser.add_argument("--root", default=None, help="Override the runtime root")
    args = parser.parse_args()

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    result = review_pending(resolution.runtime_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
