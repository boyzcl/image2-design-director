from __future__ import annotations

import argparse
import json

from runtime_memory_lib import append_capture, enrich_capture_record, resolve_runtime_resolution


def main() -> int:
    parser = argparse.ArgumentParser(description="Log one Image2 generation run into image2-design-director runtime memory.")
    parser.add_argument("--host", default=None, help="Host id, for example: codex")
    parser.add_argument("--root", default=None, help="Override the runtime root")
    parser.add_argument("--session-id", default=None, help="Optional stable session id")
    parser.add_argument("--scene", required=True, help="Short description of this image-generation scene")
    parser.add_argument("--domain-direction", required=True, help="Open-ended domain or asset direction for this run")
    parser.add_argument("--matched-profile", default="none", help="Matched profile, for example: social-creative")
    parser.add_argument(
        "--support-tier",
        default="exploratory",
        choices=["accelerated", "standard", "exploratory"],
        help="Scene support tier for this run",
    )
    parser.add_argument(
        "--legacy-use-case",
        "--use-case",
        dest="legacy_use_case",
        default=None,
        help="Compatibility field for older use-case classification",
    )
    parser.add_argument("--route", required=True, help="Route used: direct, brief-first, or repair")
    parser.add_argument("--initial-brief", required=True, help="Original user brief")
    parser.add_argument("--final-prompt", required=True, help="Structured final prompt used for the run")
    parser.add_argument("--image-prompt", default=None, help="Exact prompt sent to the image API; defaults to final prompt")
    parser.add_argument("--image-generation-id", default=None, help="Generation batch id or request id")
    parser.add_argument("--image-generation-dir", default=None, help="Directory that stores generated images")
    parser.add_argument("--image-output-path", action="append", default=[], help="Path to one generated image; repeat for multiple outputs")
    parser.add_argument("--result-status", default="review", help="Status such as review, pass, fail, or candidate")
    parser.add_argument("--evaluation-summary", default=None, help="Short summary of the quality judgment")
    parser.add_argument("--failure-class", default="none", help="Failure mode label if relevant")
    parser.add_argument("--what-worked", action="append", default=[], help="What worked in this run; repeat for multiple points")
    parser.add_argument("--what-failed", action="append", default=[], help="What failed in this run; repeat for multiple points")
    parser.add_argument("--correction-rule", default=None, help="Correction rule for the next round")
    parser.add_argument("--next-input", default=None, help="Suggested next prompt or next-round change")
    parser.add_argument("--promotion-hint", default="review", help="Promotion hint for the review queue")
    parser.add_argument("--prompt-version", default=None, help="Optional prompt version label")
    parser.add_argument("--score", type=float, default=None, help="Optional numeric score")
    args = parser.parse_args()

    record = {
        "session_id": args.session_id,
        "scene": args.scene,
        "domain_direction": args.domain_direction,
        "matched_profile": args.matched_profile,
        "support_tier": args.support_tier,
        "legacy_use_case": args.legacy_use_case,
        "route": args.route,
        "initial_brief": args.initial_brief,
        "final_prompt": args.final_prompt,
        "image_prompt": args.image_prompt or args.final_prompt,
        "image_generation_id": args.image_generation_id,
        "image_generation_dir": args.image_generation_dir,
        "image_output_paths": args.image_output_path,
        "image_outputs": [{"path": path} for path in args.image_output_path],
        "result_status": args.result_status,
        "evaluation_summary": args.evaluation_summary,
        "failure_class": args.failure_class,
        "what_worked": args.what_worked,
        "what_failed": args.what_failed,
        "correction_rule": args.correction_rule,
        "next_input": args.next_input,
        "promotion_hint": args.promotion_hint,
        "prompt_version": args.prompt_version,
        "score": args.score,
    }
    record = {key: value for key, value in record.items() if value not in (None, "", [], {})}

    resolution = resolve_runtime_resolution(host=args.host, root=args.root)
    record = enrich_capture_record(record, resolution)
    capture_path = append_capture(resolution.runtime_root, record)
    print(json.dumps({"capture_path": str(capture_path), "session_id": record["session_id"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
