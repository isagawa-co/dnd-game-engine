"""Challenge Resolution Module — resolves environmental obstacles and skill challenges."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from atomic_ops.check_operations import ability_check


# DC mapping: challenge_type -> {difficulty_tier: dc_value}
# Default tiers: moderate=12, hard=15, very_hard=18
# Investigation-type challenges use lower DCs: moderate=10, hard=13, very_hard=16
_INVESTIGATE_TYPES = {"investigate", "arcana", "history", "religion", "nature", "perception", "insight"}

_DEFAULT_DC = {"moderate": 12, "hard": 15, "very_hard": 18}
_INVESTIGATE_DC = {"moderate": 10, "hard": 13, "very_hard": 16}

# Consequence mapping per challenge type on failure
_FAILURE_CONSEQUENCES = {
    "climb": {"type": "damage", "damage_amount": 7, "narrative": "You lose your grip and fall."},
    "swim": {"type": "exhaustion", "exhaustion_level": 1, "narrative": "The current overwhelms you. You are swept downstream."},
    "jump": {"type": "damage", "damage_amount": 3, "narrative": "You misjudge the distance and land hard."},
    "balance": {"type": "damage", "damage_amount": 3, "narrative": "You lose your footing and tumble."},
    "push_pull": {"type": "time_loss", "time_cost_minutes": 10, "narrative": "You strain but cannot move it."},
    "hide": {"type": "enemy_alert", "narrative": "You are spotted! Enemies are alerted."},
    "sneak": {"type": "enemy_alert", "narrative": "A misstep gives away your position."},
    "pick_lock": {"type": "time_loss", "time_cost_minutes": 5, "narrative": "The lock resists your efforts."},
    "break_door": {"type": "time_loss", "time_cost_minutes": 5, "narrative": "The door holds firm."},
    "disable_trap": {"type": "damage", "damage_amount": 7, "narrative": "The trap triggers as you fumble!"},
    "investigate": {"type": "time_loss", "time_cost_minutes": 10, "narrative": "You search but find nothing useful."},
    "arcana": {"type": "none", "narrative": "The magical nature of this eludes you."},
    "history": {"type": "none", "narrative": "You cannot recall anything relevant."},
    "religion": {"type": "none", "narrative": "The divine significance escapes you."},
    "nature": {"type": "none", "narrative": "The natural world offers no answers."},
    "perception": {"type": "none", "narrative": "You fail to notice anything unusual."},
    "insight": {"type": "none", "narrative": "Their intentions remain unclear to you."},
}


def determine_dc(challenge_type, difficulty="moderate"):
    """
    Determine the DC for a challenge based on type and difficulty tier.

    Args:
        challenge_type: The challenge type string
        difficulty: Difficulty tier — "moderate", "hard", or "very_hard"

    Returns:
        int: The difficulty class value
    """
    if difficulty not in ("moderate", "hard", "very_hard"):
        raise ValueError(f"Invalid difficulty tier: {difficulty}")

    if challenge_type in _INVESTIGATE_TYPES:
        return _INVESTIGATE_DC[difficulty]
    return _DEFAULT_DC[difficulty]


def compute_outcome_code(roll_total, dc, d20_roll=None):
    """
    Classify the outcome of a challenge attempt.

    Args:
        roll_total: The final roll total (d20 + modifiers)
        dc: The difficulty class
        d20_roll: The raw d20 roll (for critical failure detection). If None, critical failure is not checked.

    Returns:
        str: One of "success", "partial_success", "failure", "critical_failure"
    """
    if d20_roll == 1:
        return "critical_failure"
    if roll_total >= dc:
        return "success"
    if roll_total >= dc - 2:
        return "partial_success"
    return "failure"


def compute_consequence(challenge_type, result_code, margin):
    """
    Compute the consequence of a challenge attempt based on type and result.

    Args:
        challenge_type: The challenge type string
        result_code: The outcome code (success/partial_success/failure/critical_failure)
        margin: Difference between roll total and DC

    Returns:
        dict: Consequence with type, damage_amount, exhaustion_level, time_cost_minutes, narrative
    """
    base = {
        "type": "none",
        "damage_amount": 0,
        "exhaustion_level": 0,
        "time_cost_minutes": 0,
        "narrative": ""
    }

    if result_code == "success":
        if margin >= 5:
            base["narrative"] = "Exceptional success! You accomplish the task with ease."
        else:
            base["narrative"] = "You succeed at the challenge."
        return base

    # Get failure consequence template for this challenge type
    template = _FAILURE_CONSEQUENCES.get(challenge_type, {"type": "none", "narrative": "You fail the challenge."})

    base["type"] = template.get("type", "none")
    base["narrative"] = template.get("narrative", "You fail the challenge.")
    base["damage_amount"] = template.get("damage_amount", 0)
    base["exhaustion_level"] = template.get("exhaustion_level", 0)
    base["time_cost_minutes"] = template.get("time_cost_minutes", 0)

    if result_code == "partial_success":
        # Partial success: reduced consequence
        base["damage_amount"] = max(1, base["damage_amount"] // 2)
        base["exhaustion_level"] = min(1, base["exhaustion_level"])
        base["time_cost_minutes"] = max(0, base["time_cost_minutes"] // 2)
        base["narrative"] = "Partial success — " + base["narrative"]

    if result_code == "critical_failure":
        # Critical failure: amplified consequence
        base["damage_amount"] = base["damage_amount"] * 2
        base["exhaustion_level"] = min(6, base["exhaustion_level"] + 1) if base["exhaustion_level"] > 0 else 0
        base["time_cost_minutes"] = base["time_cost_minutes"] * 2
        base["narrative"] = "Critical failure! " + base["narrative"]

    return base


def resolve_challenge(action):
    """
    Resolve a full challenge encounter.

    Args:
        action: dict matching challenge-action-contract.json schema

    Returns:
        dict: Outcome matching challenge-outcome-contract.json schema
    """
    challenge_type = action["challenge_type"]
    dc = action["difficulty_class"]
    roll_result = action["roll_result"]
    d20_roll = roll_result["d20_roll"]
    roll_total = roll_result["total"]

    result_code = compute_outcome_code(roll_total, dc, d20_roll=d20_roll)
    margin = roll_total - dc
    success = result_code in ("success", "partial_success")
    consequence = compute_consequence(challenge_type, result_code, margin)

    # Build state mutations
    state_mutations = {
        "obstacle_cleared": result_code == "success",
        "pc_hp_changes": {},
    }

    # Apply damage to PC if consequence involves damage
    if consequence["damage_amount"] > 0:
        actor = action["actor_pc"]
        state_mutations["pc_hp_changes"][actor] = -consequence["damage_amount"]

    outcome = {
        "challenge_type": challenge_type,
        "success": success,
        "result_code": result_code,
        "margin": margin,
        "challenge_name": action.get("challenge_name", challenge_type),
        "consequence": consequence,
        "state_mutations": state_mutations,
    }

    return outcome
