#!/usr/bin/env python3
"""Game Engine Gate Enforcer - thin orchestrator using shared validators."""

import json
import sys
from pathlib import Path

# Resolve isagawa-kernel path: hook is at workspace/.claude/hooks/this.py
# parents[2] = workspace, parents[3] = project_test_repos, parents[4] = my_ai_projects
kernel_path = str(Path(__file__).resolve().parents[4] / 'isagawa-kernel')
sys.path.insert(0, kernel_path)

try:
    from lib.validators import code_quality, state_validation, bash_validation, common
except ImportError:
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    if tool_name in ('Write', 'Edit'):
        file_path = tool_input.get('file_path', '').replace('\\', '/')
        if common.should_skip(file_path):
            sys.exit(0)

        session_state_path = Path('.claude/state/session_state.json')
        violations = state_validation.check(str(session_state_path))
        if violations:
            common.state_block(violations)

        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        if content:
            violations = code_quality.check(file_path, content)
            if violations:
                common.smart_block(violations, "Code quality")

    elif tool_name == 'Bash':
        command = tool_input.get('command', '')
        violations = bash_validation.check(command)
        if violations:
            common.bash_block(violations)

    sys.exit(0)


if __name__ == '__main__':
    main()
