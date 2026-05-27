#!/usr/bin/env python3
"""
Agent Inline Execution Blocker — Prevents spawning agents to execute tasks directly.

Triggered on: Agent tool calls
Pattern: If the agent prompt contains task execution keywords (execute, implement,
         write code, build, run tests) for numbered task files BUT does NOT reference
         run-task.sh, block it.

The correct pattern is: background Agent + env -u CLAUDECODE + run-task.sh
Inline task execution is a recurring violation (4 occurrences as of 2026-04-08).

Escalation source: recurrence registry pattern_key 85fa9b9e2dcf71c6
"""

import json
import re
import sys


# Keywords that indicate task execution (not research or exploration)
TASK_EXECUTION_PATTERNS = [
    r"execute\s+(all\s+)?\d+\s+tasks",
    r"execute\s+tasks?\s+\d+",
    r"tasks?\s+0\d{2}\s+through\s+0\d{2}",
    r"implement\s+what\s+each\s+(task\s+)?requires",
    r"read\s+each\s+task\s+file.*implement",
    r"execute\s+everything",
    r"start\s+with\s+task\s+0\d{2}",
    r"resume.*from\s+task\s+0\d{2}",
    r"tasks/[a-z-]+/\d{3}-",  # References to numbered task files in a task folder
]

# The correct pattern — if present, allow
CORRECT_PATTERNS = [
    r"run-task\.sh",
    r"run-task-batch\.sh",
    r"env\s+-u\s+CLAUDECODE",
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only check Agent tool calls
    if tool_name != "Agent":
        sys.exit(0)

    prompt = tool_input.get("prompt", "").lower()

    if not prompt:
        sys.exit(0)

    # Check if this looks like task execution
    is_task_execution = False
    matched_pattern = None
    for pattern in TASK_EXECUTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            is_task_execution = True
            matched_pattern = pattern
            break

    if not is_task_execution:
        sys.exit(0)

    # Check if it's using the correct pattern (run-task.sh)
    for pattern in CORRECT_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            sys.exit(0)  # Correct pattern — allow

    # BLOCK: inline task execution without run-task.sh
    message = """BLOCKED: Inline task execution detected (Agent tool without run-task.sh)

This is a recurring violation (4+ occurrences). Tasks MUST be executed via run-task.sh.

FIX:
1. Use: Agent(run_in_background=true, prompt="env -u CLAUDECODE bash run-task.sh [repo] [iterations] [subfolder]")
2. Do NOT spawn agents to read task files and implement them directly
3. Re-read: .claude/skills/execute-pipeline/references/step-04-execute-tasks.md

Pattern Key: 85fa9b9e2dcf71c6
"""
    sys.stderr.write(message)
    sys.exit(2)


if __name__ == "__main__":
    main()
