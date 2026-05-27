"""Tests for challenge resolution module."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from challenge.challenge_resolution import (
    determine_dc,
    compute_outcome_code,
    compute_consequence,
    resolve_challenge,
)


# --- determine_dc tests ---

def test_determine_dc_moderate():
    assert determine_dc("climb", "moderate") == 12


def test_determine_dc_hard():
    assert determine_dc("pick_lock", "hard") == 15


def test_determine_dc_very_hard():
    assert determine_dc("swim", "very_hard") == 18


def test_determine_dc_investigate():
    assert determine_dc("investigate", "moderate") == 10
    assert determine_dc("investigate", "hard") == 13
    assert determine_dc("investigate", "very_hard") == 16


# --- compute_outcome_code tests ---

def test_outcome_code_success():
    assert compute_outcome_code(15, 12) == "success"
    assert compute_outcome_code(12, 12) == "success"


def test_outcome_code_partial_success():
    assert compute_outcome_code(11, 12) == "partial_success"
    assert compute_outcome_code(10, 12) == "partial_success"


def test_outcome_code_failure():
    assert compute_outcome_code(9, 12) == "failure"
    assert compute_outcome_code(5, 12) == "failure"


def test_outcome_code_critical_failure():
    assert compute_outcome_code(8, 12, d20_roll=1) == "critical_failure"


# --- compute_consequence tests ---

def test_consequence_climb_failure():
    result = compute_consequence("climb", "failure", -4)
    assert result["type"] == "damage"
    assert result["damage_amount"] > 0


def test_consequence_pick_lock_failure():
    result = compute_consequence("pick_lock", "failure", -3)
    assert result["type"] == "time_loss"


def test_consequence_success_no_cost():
    result = compute_consequence("climb", "success", 5)
    assert result["type"] == "none"
    assert result["damage_amount"] == 0


# --- resolve_challenge tests ---

def test_resolve_challenge_success():
    action = {
        "challenge_type": "climb",
        "challenge_name": "Cliff Face",
        "actor_pc": "pc-1",
        "skill_used": "athletics",
        "difficulty_class": 12,
        "roll_result": {"d20_roll": 15, "modifiers_total": 4, "total": 19},
    }
    result = resolve_challenge(action)
    assert result["success"] is True
    assert result["result_code"] == "success"
    assert result["margin"] == 7
    assert result["challenge_type"] == "climb"
    assert result["challenge_name"] == "Cliff Face"
    assert isinstance(result["consequence"], dict)
    assert isinstance(result["state_mutations"], dict)
    assert result["state_mutations"]["obstacle_cleared"] is True


def test_resolve_challenge_failure():
    action = {
        "challenge_type": "disable_trap",
        "challenge_name": "Poison Dart Trap",
        "actor_pc": "pc-rogue",
        "skill_used": "investigation",
        "difficulty_class": 15,
        "roll_result": {"d20_roll": 5, "modifiers_total": 3, "total": 8},
    }
    result = resolve_challenge(action)
    assert result["success"] is False
    assert result["result_code"] == "failure"
    assert result["margin"] == -7
    assert result["consequence"]["type"] == "damage"
    assert result["consequence"]["damage_amount"] > 0
    assert result["state_mutations"]["obstacle_cleared"] is False
    assert result["state_mutations"]["pc_hp_changes"]["pc-rogue"] < 0
