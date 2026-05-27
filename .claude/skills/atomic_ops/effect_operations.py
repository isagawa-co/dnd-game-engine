"""Effect Operations Module - Effect application, condition management, and concentration handling."""


def apply_condition(condition_name, target_state):
    """
    Apply a condition to a target state.

    Args:
        condition_name: The name of the condition (e.g., 'BLINDED', 'POISONED')
        target_state: A dictionary representing the target's state

    Returns:
        dict: The updated target_state dictionary with the condition set to True

    Raises:
        ValueError: If condition_name is invalid or target_state is not a dict
    """
    if not isinstance(target_state, dict):
        raise ValueError(f"target_state must be a dictionary: {type(target_state)}")
    if not isinstance(condition_name, str) or not condition_name:
        raise ValueError(f"condition_name must be a non-empty string: {condition_name}")

    target_state[condition_name] = True
    return target_state


def apply_effect(effect_name, target_state, effect_data=None):
    """
    Apply an effect to a target state.

    Args:
        effect_name: The name of the effect (e.g., 'fireball', 'haste')
        target_state: A dictionary representing the target's state
        effect_data: Optional dictionary containing effect parameters (duration, power, etc.)

    Returns:
        dict: The updated target_state dictionary with the effect applied

    Raises:
        ValueError: If effect_name is invalid, target_state is not a dict, or effect_data is invalid
    """
    if not isinstance(target_state, dict):
        raise ValueError(f"target_state must be a dictionary: {type(target_state)}")
    if not isinstance(effect_name, str) or not effect_name:
        raise ValueError(f"effect_name must be a non-empty string: {effect_name}")
    if effect_data is not None and not isinstance(effect_data, dict):
        raise ValueError(f"effect_data must be a dictionary or None: {type(effect_data)}")

    effect_entry = {"active": True}
    if effect_data:
        effect_entry.update(effect_data)

    if "effects" not in target_state:
        target_state["effects"] = {}

    target_state["effects"][effect_name] = effect_entry
    return target_state


def validate_effect(effect_name, effect_data=None, requires_concentration=False):
    """
    Validate that an effect is properly formed and has no conflicts.

    Args:
        effect_name: The name of the effect to validate
        effect_data: Optional dictionary containing effect parameters
        requires_concentration: Whether this effect requires concentration

    Returns:
        bool: True if the effect is valid, False otherwise

    Raises:
        ValueError: If validation fails with a descriptive error
    """
    if not isinstance(effect_name, str) or not effect_name:
        raise ValueError(f"effect_name must be a non-empty string: {effect_name}")

    if effect_data is not None and not isinstance(effect_data, dict):
        raise ValueError(f"effect_data must be a dictionary or None: {type(effect_data)}")

    if not isinstance(requires_concentration, bool):
        raise ValueError(f"requires_concentration must be a boolean: {requires_concentration}")

    # Validate concentration metadata if provided
    if effect_data and "concentration" in effect_data:
        if not isinstance(effect_data["concentration"], bool):
            raise ValueError(f"effect_data['concentration'] must be boolean: {effect_data['concentration']}")

    return True


def check_concentration_conflict(target_state):
    """
    Check if target has multiple active concentration effects.

    Args:
        target_state: A dictionary representing the target's state with effects

    Returns:
        bool: False if no conflict, True if multiple concentration effects detected

    Raises:
        ValueError: If target_state is not a dict
    """
    if not isinstance(target_state, dict):
        raise ValueError(f"target_state must be a dictionary: {type(target_state)}")

    if "effects" not in target_state:
        return False

    concentration_count = 0
    for effect_name, effect_data in target_state["effects"].items():
        if isinstance(effect_data, dict) and effect_data.get("concentration", False):
            if effect_data.get("active", False):
                concentration_count += 1

    return concentration_count > 1
