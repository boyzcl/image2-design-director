from __future__ import annotations

import argparse
import json
from pathlib import Path

from publication_production_lib import run_production_preflight


def main() -> int:
    parser = argparse.ArgumentParser(description="Run production preflight for an editorial publication asset packet.")
    parser.add_argument("--packet", required=True, help="JSON production packet.")
    parser.add_argument("--write-result", default=None, help="Optional path to write the preflight result JSON.")
    args = parser.parse_args()

    packet_path = Path(args.packet).expanduser().resolve()
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    if not isinstance(packet, dict):
        raise ValueError("production packet must be a JSON object")

    result = run_production_preflight(packet)
    payload = {"production_packet": packet, "production_preflight": result}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)

    if args.write_result:
        output_path = Path(args.write_result).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")

    return 0 if result["production_preflight_result"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
