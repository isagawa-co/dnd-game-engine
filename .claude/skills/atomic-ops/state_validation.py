"""State Validation Module - HP, spell slots, conditions, and immutability enforcement."""


def validate_hp(current_hp, max_hp):
    """
    Validate that HP is within the valid range [0, max_hp].

    Args:
        current_hp: The current HP value
        max_hp: The maximum HP value

    Returns:
        bool: True if HP is valid (0 <= current_hp <= max_hp), False otherwise

    Raises:
        ValueError: If max_hp is invalid or inputs are not numeric
    """
    if not isinstance(current_hp, (int, float)):
        raise ValueError(f"current_hp must be numeric: {type(current_hp)}")
    if not isinstance(max_hp, (int, float)):
        raise ValueError(f"max_hp must be numeric: {type(max_hp)}")
    if max_hp < 0:
        raise ValueError(f"max_hp must be non-negative: {max_hp}")

    return 0 <= current_hp <= max_hp


def validate_spell_slots(current_slots, max_slots):
    """
    Validate that spell slots are within the valid range [0, max_slots].

    Args:
        current_slots: The current number of spell slots available
        max_slots: The maximum number of spell slots

    Returns:
        bool: True if slots are valid (0 <= current_slots <= max_slots), False otherwise

    Raises:
        ValueError: If max_slots is invalid or inputs are not numeric
    """
    if not isinstance(current_slots, (int, float)):
        raise ValueError(f"current_slots must be numeric: {type(current_slots)}")
    if not isinstance(max_slots, (int, float)):
        raise ValueError(f"max_slots must be numeric: {type(max_slots)}")
    if max_slots < 0:
        raise ValueError(f"max_slots must be non-negative: {max_slots}")

    return 0 <= current_slots <= max_slots


def validate_conditions(conditions):
    """
    Validate that all conditions have a duration >= 0.

    Args:
        conditions: A dictionary of conditions where keys are condition names
                   and values are dictionaries with 'duration' key (or integers representing duration)

    Returns:
        bool: True if all conditions have duration >= 0, False otherwise

    Raises:
        ValueError: If conditions is not a dict or condition format is invalid
    """
    if not isinstance(conditions, dict):
        raise ValueError(f"conditions must be a dictionary: {type(conditions)}")

    for condition_name, condition_data in conditions.items():
        if isinstance(condition_data, dict):
            # If condition_data is a dict, check for 'duration' key
            if "duration" in condition_data:
                duration = condition_data["duration"]
                if not isinstance(duration, (int, float)):
                    raise ValueError(f"Duration for condition '{condition_name}' must be numeric: {type(duration)}")
                if duration < 0:
                    return False
        elif isinstance(condition_data, (int, float)):
            # If condition_data is just a number, treat it as duration
            if condition_data < 0:
                return False
        else:
            raise ValueError(f"Condition '{condition_name}' has invalid format: {type(condition_data)}")

    return True


def enforce_immutability(state):
    """
    Enforce immutability on a state object by creating a frozen copy.

    Args:
        state: A dictionary representing the state to be made immutable

    Returns:
        object: A frozen/immutable version of the state (as a frozenset of items for dict)

    Raises:
        ValueError: If state is not a dictionary
    """
    if not isinstance(state, dict):
        raise ValueError(f"state must be a dictionary: {type(state)}")

    # Convert dict to a frozenset of items for immutability
    # This creates an immutable representation of the state
    immutable_state = frozenset(state.items())
    return immutable_state
