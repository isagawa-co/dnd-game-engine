"""Rest Operations — Long rest, short rest, hit dice recovery."""

import random
import math

from condition_removal import remove_conditions_long_rest, remove_conditions_short_rest


# Hit die type to max roll mapping
HIT_DIE_MAX = {
    'd6': 6,
    'd8': 8,
    'd10': 10,
    'd12': 12,
}


def roll_hit_die(die_type, con_modifier, rng=None):
    """Roll a hit die and add CON modifier for HP recovery.

    Args:
        die_type: Hit die type (d6, d8, d10, d12)
        con_modifier: Constitution modifier
        rng: Optional random.Random instance for seeded rolls

    Returns:
        dict with die_type, roll, con_modifier, total (min 0)
    """
    if die_type not in HIT_DIE_MAX:
        raise ValueError(f"Invalid hit die type: {die_type}")

    max_val = HIT_DIE_MAX[die_type]
    if rng is None:
        rng = random.Random()
    roll = rng.randint(1, max_val)
    total = max(0, roll + con_modifier)

    return {
        'die_type': die_type,
        'roll': roll,
        'con_modifier': con_modifier,
        'total': total,
    }


def restore_spell_slots(pc_state):
    """Restore all spell slots to maximum.

    Args:
        pc_state: PC dict with spell_slots and max_spell_slots

    Returns:
        dict of restored spell slots {level_N: int}
    """
    max_slots = pc_state.get('max_spell_slots', {})
    restored = {}
    for level, max_val in max_slots.items():
        restored[level] = max_val
    return restored


def restore_hit_dice(pc_state):
    """Restore hit dice up to level amount on long rest.

    Args:
        pc_state: PC dict with hit_dice_remaining and level

    Returns:
        dict with remaining and recovered counts
    """
    level = pc_state.get('level', 1)
    remaining = pc_state.get('hit_dice_remaining', 0)
    recovered = level - remaining
    if recovered < 0:
        recovered = 0

    return {
        'remaining': min(remaining + recovered, level),
        'recovered': recovered,
    }


def long_rest(party_state, rng=None):
    """Process a long rest (8 hours) for the party.

    Full recovery: restore all HP, spell slots, hit dice.
    Remove qualifying conditions.

    Args:
        party_state: dict with 'pcs' list of PC state dicts

    Returns:
        dict with result_code, party_recovery
    """
    pcs = party_state.get('pcs', [])
    party_recovery = {}

    for pc in pcs:
        pc_id = pc['id']
        hp_before = pc['hp']
        max_hp = pc['max_hp']
        hp_after = max_hp
        hp_restored = hp_after - hp_before

        slots_restored = restore_spell_slots(pc)
        dice_restored = restore_hit_dice(pc)
        conditions = pc.get('conditions', [])
        remaining_conditions = remove_conditions_long_rest(list(conditions))
        removed_conditions = [c for c in conditions if c not in remaining_conditions]

        party_recovery[pc_id] = {
            'hp_before': hp_before,
            'hp_restored': hp_restored,
            'hp_after': hp_after,
            'spell_slots_restored': slots_restored,
            'hit_dice_restored': dice_restored,
            'conditions_removed': removed_conditions,
            'conditions_remaining': remaining_conditions,
        }

    return {
        'rest_type': 'long_rest',
        'success': True,
        'result_code': 'long_rest_completed',
        'duration_hours': 8,
        'party_recovery': party_recovery,
        'time_elapsed': 480,
    }


def short_rest(party_state, rng=None):
    """Process a short rest (1 hour) for the party.

    Partial recovery: each PC can roll 1 hit die for HP.

    Args:
        party_state: dict with 'pcs' list of PC state dicts
        rng: Optional random.Random for seeded rolls

    Returns:
        dict with result_code, party_recovery
    """
    pcs = party_state.get('pcs', [])
    party_recovery = {}

    for pc in pcs:
        pc_id = pc['id']
        hp_before = pc['hp']
        max_hp = pc['max_hp']
        hit_dice_remaining = pc.get('hit_dice_remaining', 0)

        hit_die_result = None
        hp_restored = 0

        if hit_dice_remaining > 0:
            die_type = pc.get('hit_die', 'd8')
            con_mod = pc.get('con_modifier', 0)
            hit_die_result = roll_hit_die(die_type, con_mod, rng)
            hp_restored = min(hit_die_result['total'], max_hp - hp_before)

        hp_after = min(hp_before + hp_restored, max_hp)

        recovery = {
            'hp_before': hp_before,
            'hp_restored': hp_restored,
            'hp_after': hp_after,
        }
        if hit_die_result:
            recovery['hit_die_rolled'] = hit_die_result

        party_recovery[pc_id] = recovery

    return {
        'rest_type': 'short_rest',
        'success': True,
        'result_code': 'short_rest_completed',
        'duration_hours': 1,
        'party_recovery': party_recovery,
        'time_elapsed': 60,
    }
