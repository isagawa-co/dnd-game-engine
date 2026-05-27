"""Damage Operations Module - Damage calculation, resistance, immunities, and HP capping."""


def calculate_damage(base_damage, multiplier=1.0):
    """
    Calculate total damage from a base value and optional multiplier.

    Args:
        base_damage: The base damage value (non-negative)
        multiplier: Damage multiplier (default 1.0)

    Returns:
        int: The calculated total damage (always >= 0)

    Raises:
        ValueError: If base_damage is negative or multiplier is invalid
    """
    if not isinstance(base_damage, (int, float)) or base_damage < 0:
        raise ValueError(f"Base damage must be non-negative: {base_damage}")
    if not isinstance(multiplier, (int, float)) or multiplier < 0:
        raise ValueError(f"Multiplier must be non-negative: {multiplier}")

    result = int(base_damage * multiplier)
    return max(0, result)


def apply_resistance(damage, resistance_level=0.5):
    """
    Apply damage resistance, reducing incoming damage.

    Args:
        damage: The incoming damage value
        resistance_level: Fraction of damage to negate (default 0.5 for half damage)

    Returns:
        int: The reduced damage after resistance (always >= 0)

    Raises:
        ValueError: If damage is negative or resistance_level is invalid
    """
    if not isinstance(damage, (int, float)) or damage < 0:
        raise ValueError(f"Damage must be non-negative: {damage}")
    if not isinstance(resistance_level, (int, float)) or not (0 <= resistance_level <= 1):
        raise ValueError(f"Resistance level must be between 0 and 1: {resistance_level}")

    reduced = damage * (1 - resistance_level)
    result = int(reduced)
    return max(0, result)


def apply_immunity(damage, is_immune=False):
    """
    Apply damage immunity, negating all damage if immune.

    Args:
        damage: The incoming damage value
        is_immune: Whether the target is immune to this damage (default False)

    Returns:
        int: Zero if immune, otherwise the original damage (always >= 0)

    Raises:
        ValueError: If damage is negative
    """
    if not isinstance(damage, (int, float)) or damage < 0:
        raise ValueError(f"Damage must be non-negative: {damage}")
    if not isinstance(is_immune, bool):
        raise ValueError(f"is_immune must be boolean: {is_immune}")

    if is_immune:
        return 0
    return max(0, int(damage))


def cap_hp_change(damage, max_hp=100):
    """
    Cap damage to not exceed maximum HP change (prevent overkill).

    Args:
        damage: The damage value to apply
        max_hp: Maximum HP that can be changed (default 100)

    Returns:
        int: The capped damage (never exceeds max_hp, always >= 0)

    Raises:
        ValueError: If damage or max_hp is negative
    """
    if not isinstance(damage, (int, float)) or damage < 0:
        raise ValueError(f"Damage must be non-negative: {damage}")
    if not isinstance(max_hp, (int, float)) or max_hp < 0:
        raise ValueError(f"max_hp must be non-negative: {max_hp}")

    capped = min(int(damage), int(max_hp))
    return max(0, capped)
