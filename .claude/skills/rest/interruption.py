"""Interruption — Location safety and rest interruption mechanics."""

import random

# Location safety table: interruption chance and gold cost
LOCATION_TABLE = {
    'safe_inn': {'interruption_chance': 0.0, 'cost_gold': 5},
    'adventurers_guild': {'interruption_chance': 0.05, 'cost_gold': 2},
    'camp_fire': {'interruption_chance': 0.20, 'cost_gold': 0},
    'dangerous_area': {'interruption_chance': 0.50, 'cost_gold': 0},
}


def get_location_cost(location_safety):
    """Get the gold cost for resting at a location.

    Args:
        location_safety: Location safety key (safe_inn, adventurers_guild, camp_fire, dangerous_area)

    Returns:
        Gold cost as int
    """
    if location_safety not in LOCATION_TABLE:
        raise ValueError(f"Unknown location safety: {location_safety}")
    return LOCATION_TABLE[location_safety]['cost_gold']


def check_interruption(location_safety, rng=None):
    """Check if rest is interrupted based on location safety.

    Args:
        location_safety: Location safety key
        rng: Optional random.Random instance for seeded rolls

    Returns:
        dict with 'interrupted' (bool) and 'cost_gold' (int)
    """
    if location_safety not in LOCATION_TABLE:
        raise ValueError(f"Unknown location safety: {location_safety}")

    entry = LOCATION_TABLE[location_safety]
    chance = entry['interruption_chance']
    cost = entry['cost_gold']

    if chance == 0.0:
        return {'interrupted': False, 'cost_gold': cost}

    if rng is None:
        rng = random.Random()

    roll = rng.random()
    interrupted = roll < chance

    return {'interrupted': interrupted, 'cost_gold': cost}
