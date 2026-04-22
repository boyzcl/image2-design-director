from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime_memory_lib import append_capture, enrich_capture_record, resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Append one image2-design-director runtime capture.")
    parser.add_argument("--record-file", required=True, help="Path to a JSON file containing one record.")
    parser.add_argument("--host", default=None, help="Optional host id for metadata or host-specific env resolution.")
    parser.add_argument("--root", default=None, help="Override the runtime root")
    args = parser.parse_args()

    record_path = Path(args.record_file).expanduser()
    record = json.loads(record_path.read_text(encoding="utf-8"))
    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    record = enrich_capture_record(record, resolution)
    capture_path = append_capture(resolution.runtime_root, record)
    print(capture_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
