"""Roll Operations Module - D20 roll validation and advantage/disadvantage."""


def validate_roll(roll_value):
    """
    Validate that a roll value is within the valid D20 range [1-20].

    Args:
        roll_value: The roll result to validate

    Returns:
        bool: True if roll is valid (1-20), False otherwise
    """
    if not isinstance(roll_value, int):
        return False
    return 1 <= roll_value <= 20


def apply_advantage(roll1, roll2):
    """
    Apply advantage: take the higher of two rolls.

    Args:
        roll1: First D20 roll
        roll2: Second D20 roll

    Returns:
        int: The higher of the two rolls
    """
    if not (validate_roll(roll1) and validate_roll(roll2)):
        raise ValueError(f"Invalid rolls for advantage: {roll1}, {roll2}")
    return max(roll1, roll2)


def apply_disadvantage(roll1, roll2):
    """
    Apply disadvantage: take the lower of two rolls.

    Args:
        roll1: First D20 roll
        roll2: Second D20 roll

    Returns:
        int: The lower of the two rolls
    """
    if not (validate_roll(roll1) and validate_roll(roll2)):
        raise ValueError(f"Invalid rolls for disadvantage: {roll1}, {roll2}")
    return min(roll1, roll2)
