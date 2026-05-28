#!/usr/bin/env python3
"""
Game State Enforcer — Hard enforcement for campaign state persistence.

Defense in depth Layer 2. Paired with state-check skill (Layer 1 / soft).

Three enforcement mechanisms:
1. Scene transition gate: blocks Read of act files if state not saved since last act read
2. State write validation: validates campaign_state.json writes are complete
3. Periodic save gate: blocks after N game actions without a state save

Fires on PreToolUse for Read, Write, Edit.
"""

import json
import os
import sys
import time
from pathlib import Path

_HOOK_DIR = Path(__file__).resolve().parent
_WORKSPACE_ROOT = _HOOK_DIR.parent.parent
STATE_DIR = _WORKSPACE_ROOT / '.claude' / 'state'
GAME_STATE_FILE = STATE_DIR / 'game_state_enforcer.json'
CAMPAIGNS_DIR = _WORKSPACE_ROOT / 'campaigns'

# How many game actions (Write/Edit to non-.claude, non-state files) before forcing a save
ACTIONS_BEFORE_FORCED_SAVE = 5


def read_enforcer_state() -> dict:
    if not GAME_STATE_FILE.exists():
        return {
            "last_act_read_time": 0,
            "last_state_save_time": 0,
            "game_actions_since_save": 0,
            "last_campaign_state_hash": "",
            "active": False
        }
    try:
        return json.loads(GAME_STATE_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {
            "last_act_read_time": 0,
            "last_state_save_time": 0,
            "game_actions_since_save": 0,
            "last_campaign_state_hash": "",
            "active": False
        }


def write_enforcer_state(state: dict):
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        GAME_STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')
    except Exception:
        pass


def is_act_file(file_path: str) -> bool:
    """Check if file is an adventure act file."""
    normalized = file_path.replace('\\', '/')
    return '/adventures/' in normalized and '/scenes/' in normalized and 'act-' in normalized and normalized.endswith('.json')


def is_campaign_state_file(file_path: str) -> bool:
    """Check if file is a campaign_state.json."""
    normalized = file_path.replace('\\', '/')
    return normalized.endswith('campaign_state.json') and '/campaigns/' in normalized


def is_game_file(file_path: str) -> bool:
    """Check if file is a game-related file that should trigger periodic save enforcement.

    Excludes character template files — editing characters/*.json during leveling
    is a progression update, not a gameplay state change requiring campaign_state save.
    """
    normalized = file_path.replace('\\', '/')
    if '/.claude/' in normalized:
        return False
    # Exclude character template files from periodic save gate
    if '/characters/' in normalized:
        return False
    # Game files that require periodic saves: campaigns/, adventures/
    return any(segment in normalized for segment in ['/campaigns/', '/adventures/'])


def is_gameplay_active() -> bool:
    """Check if a gameplay session is active by reading session state."""
    session_state_file = STATE_DIR / 'session_state.json'
    if not session_state_file.exists():
        return False
    try:
        session = json.loads(session_state_file.read_text(encoding='utf-8'))
        context = session.get('context', {})
        if isinstance(context, dict):
            current_task = context.get('current_task', '')
            # Gameplay is active if context mentions gameplay or campaign
            if current_task and ('combat' in current_task.lower() or 'game' in current_task.lower()):
                return True
        return False
    except Exception:
        return False


def validate_combat_end(old_state: dict, new_state: dict) -> list:
    """Validate that combat end writes include required fields."""
    errors = []
    old_combat_active = old_state.get('combat', {}).get('active', False)
    new_combat_active = new_state.get('combat', {}).get('active', False)

    if old_combat_active and not new_combat_active:
        # Combat just ended — validate required fields
        last_combat = new_state.get('combat', {}).get('last_combat', {})
        if not last_combat:
            errors.append("combat.last_combat missing — must include encounter, result, rounds, xp_earned, xp_per_pc")
        else:
            for field in ['encounter', 'result', 'rounds', 'xp_earned', 'xp_per_pc']:
                if field not in last_combat:
                    errors.append(f"combat.last_combat.{field} missing")

        if not new_state.get('party_xp'):
            errors.append("party_xp missing — must award XP to each PC")

        if not new_state.get('loot_collected') and new_state.get('loot_collected') != []:
            errors.append("loot_collected missing — must include loot from encounter (use [] if none)")

    return errors


def validate_act_transition(old_state: dict, new_state: dict) -> list:
    """Validate that act transitions include required fields."""
    errors = []
    old_act = old_state.get('current_act_id', '')
    new_act = new_state.get('current_act_id', '')

    if old_act and new_act and old_act != new_act:
        if not new_state.get('session_notes'):
            errors.append("session_notes missing — must summarize completed act before transitioning")

    return errors


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})

    # Only enforce on Read, Write, Edit
    if tool_name not in ('Read', 'Write', 'Edit'):
        sys.exit(0)

    enforcer_state = read_enforcer_state()

    # --- GATE 1: Scene Transition Gate ---
    # Block reading act files if state hasn't been saved since last act read
    if tool_name == 'Read':
        file_path = tool_input.get('file_path', '')
        if is_act_file(file_path):
            last_act_read = enforcer_state.get('last_act_read_time', 0)
            last_state_save = enforcer_state.get('last_state_save_time', 0)

            if last_act_read > 0 and last_state_save < last_act_read:
                sys.stderr.write("""BLOCKED: Scene transition without state save.

You read an act file but haven't saved campaign_state.json since then.
The state-check skill requires saving state before loading the next scene.

FIX:
1. Run the state-check checklist (HP, resources, loot, XP, quests, location, NPCs, conditions, combat, act progress)
2. Save campaign_state.json with all updates
3. Then read the next act file

See: .claude/skills/state-check/SKILL.md
""")
                sys.exit(2)

            # Update last act read time
            enforcer_state['last_act_read_time'] = time.time()
            enforcer_state['active'] = True
            write_enforcer_state(enforcer_state)
        sys.exit(0)

    # --- For Write/Edit ---
    file_path = tool_input.get('file_path', '')

    # Track campaign_state.json saves
    if is_campaign_state_file(file_path):
        enforcer_state['last_state_save_time'] = time.time()
        enforcer_state['game_actions_since_save'] = 0

        # --- GATE 2: State Write Validation ---
        # Read old state and compare to detect incomplete saves
        normalized_path = file_path.replace('\\', '/')
        try:
            old_state_path = Path(file_path)
            if old_state_path.exists():
                old_state = json.loads(old_state_path.read_text(encoding='utf-8'))

                # For Write tool, parse the new content from tool_input
                if tool_name == 'Write':
                    new_content = tool_input.get('content', '{}')
                    try:
                        new_state = json.loads(new_content)
                    except Exception:
                        new_state = {}

                    # Validate combat end
                    errors = validate_combat_end(old_state, new_state)
                    if errors:
                        error_list = '\n'.join(f'  - {e}' for e in errors)
                        sys.stderr.write(f"""BLOCKED: Incomplete combat state save.

Combat ended (active: true → false) but required fields are missing:
{error_list}

FIX:
1. Run the state-check checklist
2. Include all required fields in your campaign_state.json write
3. Required: combat.last_combat (encounter, result, rounds, xp_earned, xp_per_pc), party_xp, loot_collected

See: .claude/skills/state-check/contracts/state-check-contract.json → combat_end_required_fields
""")
                        sys.exit(2)

                    # Validate act transition
                    errors = validate_act_transition(old_state, new_state)
                    if errors:
                        error_list = '\n'.join(f'  - {e}' for e in errors)
                        sys.stderr.write(f"""BLOCKED: Incomplete act transition save.

Act changed ({old_state.get('current_act_id')} → {new_state.get('current_act_id')}) but required fields are missing:
{error_list}

FIX:
1. Add session_notes summarizing the completed act
2. Then retry your save

See: .claude/skills/state-check/contracts/state-check-contract.json → act_transition_required_fields
""")
                        sys.exit(2)
        except Exception:
            pass  # Don't block on validation errors — best effort

        write_enforcer_state(enforcer_state)
        sys.exit(0)

    # --- GATE 3: Periodic Save Enforcement ---
    # Track game actions and block if too many without a save
    if is_game_file(file_path) and enforcer_state.get('active', False):
        enforcer_state['game_actions_since_save'] = enforcer_state.get('game_actions_since_save', 0) + 1

        if enforcer_state['game_actions_since_save'] >= ACTIONS_BEFORE_FORCED_SAVE:
            write_enforcer_state(enforcer_state)
            sys.stderr.write(f"""BLOCKED: {ACTIONS_BEFORE_FORCED_SAVE} game actions without saving campaign state.

You've made {enforcer_state['game_actions_since_save']} changes to game files without saving campaign_state.json.

FIX:
1. Run the state-check checklist
2. Save campaign_state.json with current game state
3. Then continue

See: .claude/skills/state-check/SKILL.md
""")
            sys.exit(2)

        write_enforcer_state(enforcer_state)

    sys.exit(0)


if __name__ == '__main__':
    main()
