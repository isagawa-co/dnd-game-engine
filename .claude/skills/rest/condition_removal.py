"""Condition Removal — Rules for removing conditions during rest."""

# Conditions removed by long rest
LONG_REST_REMOVABLE = frozenset([
    'exhaustion',
    'poisoned',
    'stunned',
    'charmed',
])


def is_removable_by_long_rest(condition):
    """Check if a condition is removed by long rest.

    Args:
        condition: Condition name string

    Returns:
        True if condition is removed by long rest
    """
    return condition.lower() in LONG_REST_REMOVABLE


def remove_conditions_long_rest(conditions):
    """Remove qualifying conditions after a long rest.

    Removes: exhaustion, poisoned, stunned, charmed
    Keeps: blinded, frightened, unconscious, and any others

    Args:
        conditions: List of condition name strings

    Returns:
        List of remaining conditions (not removed by long rest)
    """
    return [c for c in conditions if not is_removable_by_long_rest(c)]


def remove_conditions_short_rest(conditions):
    """Process conditions after a short rest.

    Short rest does NOT remove any conditions automatically.

    Args:
        conditions: List of condition name strings

    Returns:
        Same list of conditions (unchanged)
    """
    return list(conditions)
