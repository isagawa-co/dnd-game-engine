"""Tests for rest loop — L1/L2/L3 coverage."""

import sys
import os
import random

# Add parent directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rest_operations import long_rest, short_rest, roll_hit_die, restore_spell_slots, restore_hit_dice
from condition_removal import remove_conditions_long_rest, remove_conditions_short_rest, is_removable_by_long_rest
from interruption import check_interruption, get_location_cost


# --- L1: Existence tests ---

def test_l1_rest_operations_import():
    """L1: rest_operations module imports without error."""
    assert long_rest is not None
    assert short_rest is not None
    assert roll_hit_die is not None
    assert restore_spell_slots is not None
    assert restore_hit_dice is not None


def test_l1_condition_removal_import():
    """L1: condition_removal module imports without error."""
    assert remove_conditions_long_rest is not None
    assert remove_conditions_short_rest is not None
    assert is_removable_by_long_rest is not None


def test_l1_interruption_import():
    """L1: interruption module imports without error."""
    assert check_interruption is not None
    assert get_location_cost is not None


# --- L2: Execution tests ---

def test_l2_roll_hit_die_returns_dict():
    """L2: roll_hit_die returns dict with expected keys."""
    rng = random.Random(42)
    result = roll_hit_die('d10', 2, rng)
    assert isinstance(result, dict)
    assert 'die_type' in result
    assert 'roll' in result
    assert 'con_modifier' in result
    assert 'total' in result


def test_l2_long_rest_returns_dict():
    """L2: long_rest returns dict with result_code."""
    party = {'pcs': [_make_pc('pc-1', hp=5, max_hp=20)]}
    result = long_rest(party)
    assert isinstance(result, dict)
    assert result['result_code'] == 'long_rest_completed'
    assert 'party_recovery' in result


def test_l2_short_rest_returns_dict():
    """L2: short_rest returns dict with result_code."""
    rng = random.Random(42)
    party = {'pcs': [_make_pc('pc-1', hp=5, max_hp=20)]}
    result = short_rest(party, rng)
    assert isinstance(result, dict)
    assert result['result_code'] == 'short_rest_completed'


def test_l2_check_interruption_returns_dict():
    """L2: check_interruption returns dict with interrupted and cost_gold."""
    result = check_interruption('safe_inn')
    assert isinstance(result, dict)
    assert 'interrupted' in result
    assert 'cost_gold' in result


# --- L3: Correctness tests ---

def test_l3_long_rest_full_hp_recovery():
    """L3: Long rest restores HP to maximum."""
    party = {'pcs': [_make_pc('pc-1', hp=5, max_hp=20)]}
    result = long_rest(party)
    recovery = result['party_recovery']['pc-1']
    assert recovery['hp_before'] == 5
    assert recovery['hp_after'] == 20
    assert recovery['hp_restored'] == 15


def test_l3_long_rest_spell_slot_recovery():
    """L3: Long rest restores all spell slots."""
    pc = _make_pc('pc-1', hp=10, max_hp=20)
    pc['spell_slots'] = {'level_1': 1, 'level_2': 0}
    pc['max_spell_slots'] = {'level_1': 3, 'level_2': 2}
    party = {'pcs': [pc]}
    result = long_rest(party)
    slots = result['party_recovery']['pc-1']['spell_slots_restored']
    assert slots['level_1'] == 3
    assert slots['level_2'] == 2


def test_l3_long_rest_condition_removal():
    """L3: Long rest removes exhaustion, poisoned, stunned, charmed but keeps blinded."""
    pc = _make_pc('pc-1', hp=10, max_hp=20)
    pc['conditions'] = ['exhaustion', 'poisoned', 'blinded']
    party = {'pcs': [pc]}
    result = long_rest(party)
    recovery = result['party_recovery']['pc-1']
    assert 'exhaustion' in recovery['conditions_removed']
    assert 'poisoned' in recovery['conditions_removed']
    assert 'blinded' in recovery['conditions_remaining']
    assert 'blinded' not in recovery['conditions_removed']


def test_l3_long_rest_hit_dice_recovery():
    """L3: Long rest restores hit dice up to level amount."""
    pc = _make_pc('pc-1', hp=10, max_hp=20)
    pc['level'] = 5
    pc['hit_dice_remaining'] = 2
    party = {'pcs': [pc]}
    result = long_rest(party)
    dice = result['party_recovery']['pc-1']['hit_dice_restored']
    assert dice['remaining'] == 5
    assert dice['recovered'] == 3


def test_l3_short_rest_hit_die_roll():
    """L3: Short rest rolls 1 hit die for HP recovery."""
    rng = random.Random(42)
    pc = _make_pc('pc-1', hp=5, max_hp=20)
    pc['hit_dice_remaining'] = 2
    pc['hit_die'] = 'd10'
    pc['con_modifier'] = 2
    party = {'pcs': [pc]}
    result = short_rest(party, rng)
    recovery = result['party_recovery']['pc-1']
    assert recovery['hp_after'] > recovery['hp_before'] or recovery['hp_restored'] == 0
    assert 'hit_die_rolled' in recovery
    assert recovery['hit_die_rolled']['die_type'] == 'd10'


def test_l3_short_rest_no_hit_dice():
    """L3: Short rest with no hit dice remaining gives 0 recovery."""
    rng = random.Random(42)
    pc = _make_pc('pc-1', hp=5, max_hp=20)
    pc['hit_dice_remaining'] = 0
    party = {'pcs': [pc]}
    result = short_rest(party, rng)
    recovery = result['party_recovery']['pc-1']
    assert recovery['hp_restored'] == 0
    assert recovery['hp_after'] == 5
    assert 'hit_die_rolled' not in recovery


def test_l3_short_rest_no_overheal():
    """L3: Short rest HP recovery capped at max_hp."""
    rng = random.Random(42)
    pc = _make_pc('pc-1', hp=19, max_hp=20)
    pc['hit_dice_remaining'] = 1
    pc['hit_die'] = 'd12'
    pc['con_modifier'] = 5
    party = {'pcs': [pc]}
    result = short_rest(party, rng)
    recovery = result['party_recovery']['pc-1']
    assert recovery['hp_after'] <= 20


def test_l3_condition_removal_short_rest_keeps_all():
    """L3: Short rest does not remove any conditions."""
    conditions = ['exhaustion', 'poisoned', 'blinded']
    result = remove_conditions_short_rest(conditions)
    assert result == ['exhaustion', 'poisoned', 'blinded']


def test_l3_safe_inn_never_interrupted():
    """L3: Safe inn always returns interrupted=False."""
    for _ in range(100):
        result = check_interruption('safe_inn', random.Random())
        assert result['interrupted'] is False
    assert result['cost_gold'] == 5


def test_l3_dangerous_area_interruption_rate():
    """L3: Dangerous area has ~50% interruption chance."""
    rng = random.Random(12345)
    interrupted_count = sum(
        1 for _ in range(1000)
        if check_interruption('dangerous_area', rng)['interrupted']
    )
    assert 400 < interrupted_count < 600


def test_l3_location_costs():
    """L3: Location costs match spec."""
    assert get_location_cost('safe_inn') == 5
    assert get_location_cost('adventurers_guild') == 2
    assert get_location_cost('camp_fire') == 0
    assert get_location_cost('dangerous_area') == 0


def test_l3_is_removable_by_long_rest():
    """L3: Correct conditions are removable by long rest."""
    assert is_removable_by_long_rest('exhaustion') is True
    assert is_removable_by_long_rest('poisoned') is True
    assert is_removable_by_long_rest('stunned') is True
    assert is_removable_by_long_rest('charmed') is True
    assert is_removable_by_long_rest('blinded') is False
    assert is_removable_by_long_rest('frightened') is False


def test_l3_roll_hit_die_range():
    """L3: Hit die rolls are within valid range."""
    rng = random.Random(99)
    for die_type, max_val in [('d6', 6), ('d8', 8), ('d10', 10), ('d12', 12)]:
        for _ in range(50):
            result = roll_hit_die(die_type, 0, rng)
            assert 1 <= result['roll'] <= max_val
            assert result['total'] == result['roll']


def test_l3_multiple_pcs_long_rest():
    """L3: Long rest processes multiple PCs correctly."""
    party = {'pcs': [
        _make_pc('pc-1', hp=5, max_hp=20),
        _make_pc('pc-2', hp=15, max_hp=25),
        _make_pc('pc-3', hp=1, max_hp=10),
    ]}
    result = long_rest(party)
    assert result['party_recovery']['pc-1']['hp_after'] == 20
    assert result['party_recovery']['pc-2']['hp_after'] == 25
    assert result['party_recovery']['pc-3']['hp_after'] == 10


# --- Helper ---

def _make_pc(pc_id, hp=10, max_hp=20):
    return {
        'id': pc_id,
        'hp': hp,
        'max_hp': max_hp,
        'level': 3,
        'hit_die': 'd10',
        'con_modifier': 2,
        'spell_slots': {},
        'max_spell_slots': {},
        'hit_dice_remaining': 3,
        'conditions': [],
    }
