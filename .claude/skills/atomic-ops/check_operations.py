"""Check Operations Module - Ability checks, saving throws, and attack rolls."""


def ability_check(roll_value, modifier=0):
    """
    Perform an ability check (d20 + ability modifier).

    Args:
        roll_value: The d20 roll result (1-20)
        modifier: Ability modifier to add to the roll (default 0)

    Returns:
        dict: Result with keys:
            - roll: The d20 roll value
            - modifier: The ability modifier applied
            - total: The final result (roll + modifier)
            - success: Boolean indicating if total >= 10 (DC 10 baseline)
    """
    if not isinstance(roll_value, int) or not (1 <= roll_value <= 20):
        raise ValueError(f"Invalid roll value for ability check: {roll_value}")
    if not isinstance(modifier, int):
        raise ValueError(f"Invalid modifier: {modifier}")

    total = roll_value + modifier
    return {
        "roll": roll_value,
        "modifier": modifier,
        "total": total,
        "success": total >= 10
    }


def saving_throw(roll_value, modifier=0, proficiency=0):
    """
    Perform a saving throw (d20 + ability modifier + proficiency bonus).

    Args:
        roll_value: The d20 roll result (1-20)
        modifier: Ability modifier (default 0)
        proficiency: Proficiency bonus if proficient (default 0)

    Returns:
        dict: Result with keys:
            - roll: The d20 roll value
            - modifier: The ability modifier applied
            - proficiency: The proficiency bonus applied
            - total: The final result (roll + modifier + proficiency)
            - success: Boolean indicating if total >= 10 (DC 10 baseline)
    """
    if not isinstance(roll_value, int) or not (1 <= roll_value <= 20):
        raise ValueError(f"Invalid roll value for saving throw: {roll_value}")
    if not isinstance(modifier, int):
        raise ValueError(f"Invalid modifier: {modifier}")
    if not isinstance(proficiency, int) or proficiency < 0:
        raise ValueError(f"Invalid proficiency bonus: {proficiency}")

    total = roll_value + modifier + proficiency
    return {
        "roll": roll_value,
        "modifier": modifier,
        "proficiency": proficiency,
        "total": total,
        "success": total >= 10
    }


def attack_roll(roll_value, attack_bonus=0):
    """
    Perform an attack roll (d20 + attack bonus).

    Args:
        roll_value: The d20 roll result (1-20)
        attack_bonus: Total attack bonus (ability + proficiency + items, default 0)

    Returns:
        dict: Result with keys:
            - roll: The d20 roll value
            - attack_bonus: The attack bonus applied
            - total: The final result (roll + attack_bonus)
            - is_critical_hit: Boolean indicating if natural 20
            - is_critical_miss: Boolean indicating if natural 1
            - hits_ac_10: Boolean indicating if total >= 10 (AC 10 baseline)
    """
    if not isinstance(roll_value, int) or not (1 <= roll_value <= 20):
        raise ValueError(f"Invalid roll value for attack roll: {roll_value}")
    if not isinstance(attack_bonus, int):
        raise ValueError(f"Invalid attack bonus: {attack_bonus}")

    total = roll_value + attack_bonus
    return {
        "roll": roll_value,
        "attack_bonus": attack_bonus,
        "total": total,
        "is_critical_hit": roll_value == 20,
        "is_critical_miss": roll_value == 1,
        "hits_ac_10": total >= 10
    }
