#!/usr/bin/env python3
"""
Loop Dispatch Enforcer — Hard enforcement for correct loop flow.

Companion to game-state-enforcer.py (which enforces SAVE discipline).
This hook enforces DISPATCH CORRECTNESS — that the right loop runs at the
right time, and that loops fire sequentially instead of being improvised
from memory.

Enforces on Write to campaign_state.json (PreToolUse):
  GATE 1  Mutual exclusion — at most ONE encounter loop flag active.
  GATE 2  active_loop sync  — active_loop.loop matches the single active flag.
  GATE 3  No missing handler — active_loop.loop must have a skill directory.

Validation happens on the NEW content of a Write (full JSON). Edit (partial
patch) is best-effort skipped, matching game-state-enforcer's pattern.

Fires on PreToolUse for Write, Edit.
"""

import json
import sys
from pathlib import Path

_HOOK_DIR = Path(__file__).resolve().parent
_WORKSPACE_ROOT = _HOOK_DIR.parent.parent
SKILLS_DIR = _WORKSPACE_ROOT / '.claude' / 'skills'

# Encounter loop flags that must be mutually exclusive.
LOOP_FLAGS = ['combat', 'social', 'challenge', 'rest', 'travel', 'exploration']

# active_loop.loop values that require a backing skill directory.
# (merchant / item-use are dispatched via scene encounter_type, no top-level flag,
#  but they still need a handler when named as the active loop.)
HANDLER_LOOPS = ['combat', 'social', 'challenge', 'rest', 'travel', 'merchant', 'item-use']


def is_campaign_state_file(file_path: str) -> bool:
    normalized = file_path.replace('\\', '/')
    return normalized.endswith('campaign_state.json') and '/campaigns/' in normalized


def active_flags(state: dict) -> list:
    """Return the list of encounter loop flags currently set true."""
    found = []
    for flag in LOOP_FLAGS:
        section = state.get(flag)
        if isinstance(section, dict) and section.get('active') is True:
            found.append(flag)
    return found


def validate_dispatch(state: dict) -> list:
    errors = []

    # --- GATE 1: Mutual exclusion ---
    on = active_flags(state)
    if len(on) > 1:
        errors.append(
            f"Multiple loop flags active at once: {', '.join(on)}. "
            "Exactly one of {combat,social,challenge,rest,travel,exploration} may be active. "
            "On loop entry, set that loop's flag true AND clear all others."
        )

    # --- GATE 2 & 3 depend on active_loop ---
    active_loop = state.get('active_loop')
    if not isinstance(active_loop, dict):
        # active_loop is required for dispatch tracking.
        errors.append(
            "active_loop pointer missing. Add active_loop {loop, step, round, turn_actor, resume_hint} "
            "so loops resume from the exact step instead of improvising from memory. "
            "See campaign-loop-contract.json -> active_loop_schema."
        )
        return errors

    loop = active_loop.get('loop')

    # --- GATE 2: active_loop matches the single active flag ---
    if len(on) == 1:
        if loop != on[0]:
            errors.append(
                f"active_loop.loop ('{loop}') does not match the active flag ('{on[0]}'). "
                "The pointer and the flags are two views of one fact — they must agree."
            )
    elif len(on) == 0:
        # No encounter flag set: active_loop must be exploration, a scene-only
        # loop (merchant/item-use), or null (between sessions).
        if loop not in ('exploration', 'merchant', 'item-use', None):
            errors.append(
                f"No encounter flag is active but active_loop.loop is '{loop}'. "
                "When no combat/social/challenge/rest/travel flag is set, active_loop.loop "
                "must be 'exploration', 'merchant'/'item-use' (scene-dispatched), or null."
            )

    # --- GATE 3: No dispatch to a missing handler ---
    if loop in HANDLER_LOOPS:
        skill_path = SKILLS_DIR / loop
        if not skill_path.is_dir():
            errors.append(
                f"active_loop.loop '{loop}' has no skill directory at .claude/skills/{loop}/. "
                "Never dispatch to a stub or missing handler."
            )

    return errors


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    if tool_name not in ('Write', 'Edit'):
        sys.exit(0)

    file_path = tool_input.get('file_path', '')
    if not is_campaign_state_file(file_path):
        sys.exit(0)

    # Only validate Write (full content). Edit is a partial patch — best-effort skip.
    if tool_name != 'Write':
        sys.exit(0)

    try:
        new_state = json.loads(tool_input.get('content', '{}'))
    except Exception:
        sys.exit(0)  # Don't block on unparseable content — best effort.

    if not isinstance(new_state, dict):
        sys.exit(0)

    errors = validate_dispatch(new_state)
    if errors:
        error_list = '\n'.join(f'  - {e}' for e in errors)
        sys.stderr.write(f"""BLOCKED: Loop dispatch invariant violation.

Your campaign_state.json write breaks the loop-flow rules:
{error_list}

FIX:
1. Re-read .claude/skills/campaign/references/loop-execution-protocol.md
2. Ensure exactly one loop flag is active and active_loop.loop matches it
3. Then retry your save

See: .claude/skills/campaign/contracts/campaign-loop-contract.json -> dispatch_invariants
""")
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
