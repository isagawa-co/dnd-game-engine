"""Atomic Operations Package - D20 game mechanics operations."""

from .roll_operations import validate_roll, apply_advantage, apply_disadvantage
from .check_operations import ability_check, saving_throw, attack_roll
from .damage_operations import calculate_damage, apply_resistance, apply_immunity, cap_hp_change
from .effect_operations import apply_condition, apply_effect, validate_effect, check_concentration_conflict
from .state_validation import validate_hp, validate_spell_slots, validate_conditions, enforce_immutability

__all__ = [
    'validate_roll',
    'apply_advantage',
    'apply_disadvantage',
    'ability_check',
    'saving_throw',
    'attack_roll',
    'calculate_damage',
    'apply_resistance',
    'apply_immunity',
    'cap_hp_change',
    'apply_condition',
    'apply_effect',
    'validate_effect',
    'check_concentration_conflict',
    'validate_hp',
    'validate_spell_slots',
    'validate_conditions',
    'enforce_immutability',
]
