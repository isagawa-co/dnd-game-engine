"""State Validation Module - Pre-write checks and immutability enforcement."""


def validate_hp(current_hp, max_hp):
    """
    Validate that current HP is within the valid range [0, max_hp].

    Args:
        current_hp: The current HP value to validate
        max_hp: The maximum HP value

    Returns:
        bool: True if HP is valid (0 <= current_hp <= max_hp)

    Raises:
        ValueError: If validation fails with a descriptive error
    """
    if not isinstance(current_hp, int):
        raise ValueError(f"current_hp must be an integer: {type(current_hp)}")
    if not isinstance(max_hp, int):
        raise ValueError(f"max_hp must be an integer: {type(max_hp)}")
    if max_hp <= 0:
        raise ValueError(f"max_hp must be positive: {max_hp}")
    if not (0 <= current_hp <= max_hp):
        raise ValueError(f"current_hp must be in range [0, {max_hp}]: {current_hp}")

    return True


def validate_spell_slots(spell_slots, max_slots):
    """
    Validate that spell slots are within the valid range [0, max_slots].

    Args:
        spell_slots: A dictionary mapping spell levels to available slots (e.g., {1: 2, 2: 1})
        max_slots: A dictionary mapping spell levels to maximum slots (e.g., {1: 4, 2: 3})

    Returns:
        bool: True if all spell slots are valid

    Raises:
        ValueError: If validation fails with a descriptive error
    """
    if not isinstance(spell_slots, dict):
        raise ValueError(f"spell_slots must be a dictionary: {type(spell_slots)}")
    if not isinstance(max_slots, dict):
        raise ValueError(f"max_slots must be a dictionary: {type(max_slots)}")

    for level, current in spell_slots.items():
        if not isinstance(level, int):
            raise ValueError(f"spell level must be an integer: {level}")
        if not isinstance(current, int):
            raise ValueError(f"spell slots for level {level} must be an integer: {type(current)}")

        if level not in max_slots:
            raise ValueError(f"spell level {level} not found in max_slots: {max_slots.keys()}")

        max_val = max_slots[level]
        if not isinstance(max_val, int):
            raise ValueError(f"max slots for level {level} must be an integer: {type(max_val)}")
        if max_val < 0:
            raise ValueError(f"max slots for level {level} must be non-negative: {max_val}")
        if not (0 <= current <= max_val):
            raise ValueError(f"spell slots for level {level} must be in range [0, {max_val}]: {current}")

    return True


def validate_conditions(conditions):
    """
    Validate that all conditions have valid durations (>= 0).

    Args:
        conditions: A dictionary mapping condition names to their duration values
                   (e.g., {'blinded': 2, 'poisoned': 1})

    Returns:
        bool: True if all conditions are valid

    Raises:
        ValueError: If validation fails with a descriptive error
    """
    if not isinstance(conditions, dict):
        raise ValueError(f"conditions must be a dictionary: {type(conditions)}")

    for condition_name, duration in conditions.items():
        if not isinstance(condition_name, str) or not condition_name:
            raise ValueError(f"condition name must be a non-empty string: {condition_name}")
        if not isinstance(duration, int):
            raise ValueError(f"duration for condition '{condition_name}' must be an integer: {type(duration)}")
        if duration < 0:
            raise ValueError(f"duration for condition '{condition_name}' must be >= 0: {duration}")

    return True


def enforce_immutability(state_dict):
    """
    Enforce immutability of protected state fields by returning a copy that should not be modified.

    Args:
        state_dict: The state dictionary to protect

    Returns:
        dict: A deep copy of the state dictionary (caller should treat as immutable)

    Raises:
        ValueError: If state_dict is not a dictionary
    """
    if not isinstance(state_dict, dict):
        raise ValueError(f"state_dict must be a dictionary: {type(state_dict)}")

    # Return a deep copy to prevent unintended mutations
    import copy
    return copy.deepcopy(state_dict)
