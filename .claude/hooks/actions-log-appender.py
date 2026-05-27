#!/usr/bin/env python3
"""
Actions Log Appender — PostToolUse hook that appends to actions.jsonl and session_state.json.

Logs every Edit, Write, and Bash action so anchor Part B has data to review.
Skips .claude/ Write/Edit paths (infrastructure writes don't count as reviewable work).

Primary log: .claude/state/actions.jsonl (append-only JSONL, 200-line retention cap)
Backward-compatible summary: actions_log array in session_state.json (last 10 entries)
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_HOOK_DIR = Path(__file__).resolve().parent
_WORKSPACE_ROOT = _HOOK_DIR.parent.parent
STATE_DIR = _WORKSPACE_ROOT / '.claude' / 'state'
SESSION_STATE = STATE_DIR / 'session_state.json'
ACTIONS_LOG = STATE_DIR / 'actions.jsonl'


def read_state() -> dict:
    if not SESSION_STATE.exists():
        return {}
    try:
        return json.loads(SESSION_STATE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def write_state(state: dict):
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        SESSION_STATE.write_text(json.dumps(state, indent=2), encoding='utf-8')
    except Exception:
        pass


def enforce_retention(log_file: Path, max_lines: int = 200):
    if not log_file.exists():
        return
    lines = log_file.read_text(encoding='utf-8').strip().split('\n')
    if len(lines) > max_lines:
        log_file.write_text('\n'.join(lines[-max_lines:]) + '\n', encoding='utf-8')


def append_jsonl(entry: str, tool_name: str):
    """Append a single JSON line to actions.jsonl."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "tool": tool_name,
        "entry": entry,
        "session": "current"
    }
    with open(ACTIONS_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record) + '\n')
    enforce_retention(ACTIONS_LOG)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    if tool_name not in ('Write', 'Edit', 'Bash'):
        sys.exit(0)

    tool_input = data.get('tool_input', {})

    # Build log entry
    if tool_name in ('Write', 'Edit'):
        file_path = tool_input.get('file_path', '').replace('\\', '/')

        # Skip .claude/ paths — infrastructure, not reviewable work
        if '/.claude/' in file_path or file_path.startswith('.claude/'):
            sys.exit(0)

        # Extract just the filename for brevity
        short_path = file_path.split('/')[-1] if '/' in file_path else file_path
        entry = f"{tool_name}: {short_path}"

    elif tool_name == 'Bash':
        command = tool_input.get('command', '')
        entry = f"Bash: {command[:80]}"

    else:
        sys.exit(0)

    # Append to actions.jsonl (primary log)
    append_jsonl(entry, tool_name)

    # Backward-compatible summary in session_state.json (last 10 entries)
    state = read_state()
    if 'actions_log' not in state:
        state['actions_log'] = []
    state['actions_log'].append(entry)
    # Keep only last 10 for backward compatibility
    state['actions_log'] = state['actions_log'][-10:]
    write_state(state)

    sys.exit(0)


if __name__ == '__main__':
    main()
