from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "state" / "execution-progress.json"
PLAN_PATH = ROOT / "docs" / "execution-plan.md"

VALID_STATUSES = {"pending", "in_progress", "completed", "blocked"}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_state() -> dict[str, Any]:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_plan(state: dict[str, Any]) -> str:
    tasks = state["tasks"]
    counts = {status: 0 for status in VALID_STATUSES}
    for task in tasks:
        counts[task["status"]] += 1

    lines: list[str] = []
    lines.append("# Execution Plan")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("这份文档由 `scripts/update_execution_progress.py` 自动回写。")
    lines.append("它的作用是让执行阶段始终围绕升级路线推进，并把当前进度回写成可读状态。")
    lines.append("")
    lines.append("## Current Status")
    lines.append("")
    lines.append(f"- updated_at: `{state['updated_at']}`")
    lines.append(f"- current_focus: `{state.get('current_focus', 'n/a')}`")
    lines.append(f"- pending: `{counts['pending']}`")
    lines.append(f"- in_progress: `{counts['in_progress']}`")
    lines.append(f"- completed: `{counts['completed']}`")
    lines.append(f"- blocked: `{counts['blocked']}`")
    lines.append("")
    lines.append("## Source Docs")
    lines.append("")
    for path in state.get("source_docs", []):
        lines.append(f"- `{path}`")
    lines.append("")
    lines.append("## Task Board")
    lines.append("")
    lines.append("| id | milestone | title | status | outputs | next_step |")
    lines.append("|---|---|---|---|---|---|")
    for task in tasks:
        outputs = "<br>".join(task.get("outputs", [])) or "-"
        next_step = task.get("next_step", "-")
        lines.append(
            f"| `{task['id']}` | {task['milestone']} | {task['title']} | `{task['status']}` | {outputs} | {next_step} |"
        )
    lines.append("")
    lines.append("## Task Details")
    lines.append("")
    for task in tasks:
        lines.append(f"### {task['id']} - {task['title']}")
        lines.append("")
        lines.append(f"- milestone: `{task['milestone']}`")
        lines.append(f"- status: `{task['status']}`")
        depends_on = ", ".join(f"`{item}`" for item in task.get("depends_on", [])) or "`none`"
        lines.append(f"- depends_on: {depends_on}")
        lines.append(f"- summary: {task['summary']}")
        outputs = ", ".join(f"`{item}`" for item in task.get("outputs", [])) or "`none`"
        lines.append(f"- outputs: {outputs}")
        lines.append(f"- next_step: {task.get('next_step', 'n/a')}")
        notes = task.get("notes", [])
        if notes:
            lines.append("- notes:")
            for note in notes:
                lines.append(f"  - {note}")
        else:
            lines.append("- notes: none")
        lines.append("")
    lines.append("## Update Command")
    lines.append("")
    lines.append("```bash")
    lines.append("python scripts/update_execution_progress.py --task <task-id> --status <pending|in_progress|completed|blocked> --note \"progress note\"")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def write_plan(state: dict[str, Any]) -> None:
    PLAN_PATH.write_text(render_plan(state), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update execution progress and rewrite the execution plan.")
    parser.add_argument("--task", default=None, help="Task id to update")
    parser.add_argument("--status", choices=sorted(VALID_STATUSES), default=None, help="New task status")
    parser.add_argument("--note", default=None, help="Append a progress note to the task")
    parser.add_argument("--next-step", default=None, help="Replace the next_step field for the task")
    parser.add_argument("--focus", default=None, help="Update the current focus task id")
    parser.add_argument("--render-only", action="store_true", help="Only rewrite the markdown plan from current JSON state")
    args = parser.parse_args()

    state = load_state()

    if not args.render_only:
        if not args.task:
            raise SystemExit("--task is required unless --render-only is used")
        task = next((item for item in state["tasks"] if item["id"] == args.task), None)
        if not task:
            raise SystemExit(f"unknown task id: {args.task}")
        if args.status:
            task["status"] = args.status
        if args.note:
            task.setdefault("notes", []).append(f"{now_iso()} - {args.note}")
        if args.next_step:
            task["next_step"] = args.next_step

    if args.focus:
        state["current_focus"] = args.focus

    save_state(state)
    write_plan(state)
    print(json.dumps({"state_path": str(STATE_PATH), "plan_path": str(PLAN_PATH), "updated_at": state["updated_at"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
