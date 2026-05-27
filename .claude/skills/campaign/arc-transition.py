"""
Arc Transition Logic — Arc Completion Detection and Progression

Implements arc completion detection and progression mechanics:
- Evaluate arc completion conditions (encounter threshold, explicit marking)
- Trigger arc transition to next arc
- Record completed arc in campaign state

Integrates with CampaignLoop for state hierarchy and StateManager for persistence.
"""

from typing import Dict, Optional, Tuple
from uuid import uuid4
from datetime import datetime


def check_arc_completion(
    arc_state: Dict,
    completion_threshold: int = 10
) -> bool:
    """
    Evaluate arc completion conditions.

    Checks if arc meets completion criteria:
    - Arc marked as completed (explicit flag), OR
    - Arc encounters exceed threshold

    Args:
        arc_state: Arc state dict with 'completed' and 'encounters_in_arc' fields
        completion_threshold: Encounter count needed for automatic completion (default: 10)

    Returns:
        True if arc meets completion criteria, False otherwise

    Raises:
        ValueError: If arc_state is missing required fields
    """
    if not isinstance(arc_state, dict):
        raise ValueError("arc_state must be a dict")

    # Validate required fields
    required_fields = ['completed', 'encounters_in_arc']
    missing = [f for f in required_fields if f not in arc_state]
    if missing:
        raise ValueError(f"arc_state missing required fields: {missing}")

    # Check explicit completion flag
    if arc_state.get('completed'):
        return True

    # Check encounter threshold
    encounters = arc_state.get('encounters_in_arc', 0)
    if encounters >= completion_threshold:
        return True

    return False


def advance_to_next_arc(
    campaign_state: Dict,
    completed_arc_id: str
) -> Dict:
    """
    Trigger arc transition on completion.

    Creates new arc and updates campaign progression:
    - Increment total_arcs_completed counter
    - Generate new arc with unique ID
    - Set new arc as current in campaign state
    - Preserve campaign metadata

    Args:
        campaign_state: Campaign state dict with 'campaign_id' and 'total_arcs_completed'
        completed_arc_id: ID of arc that was just completed

    Returns:
        New arc state dict ready for next arc play session

    Raises:
        ValueError: If campaign_state is missing required fields
    """
    if not isinstance(campaign_state, dict):
        raise ValueError("campaign_state must be a dict")

    # Validate required fields
    required_fields = ['campaign_id', 'total_arcs_completed']
    missing = [f for f in required_fields if f not in campaign_state]
    if missing:
        raise ValueError(f"campaign_state missing required fields: {missing}")

    # Increment arc counter
    campaign_state['total_arcs_completed'] += 1

    # Generate new arc
    arc_id = str(uuid4())
    arc_number = campaign_state['total_arcs_completed'] + 1

    new_arc = {
        'arc_id': arc_id,
        'arc_name': f"Arc_{arc_number}",
        'parent_campaign_id': campaign_state['campaign_id'],
        'encounters_in_arc': 0,
        'completed': False,
        'created_at': datetime.utcnow().isoformat(),
        'metadata': {
            'previous_arc_id': completed_arc_id,
            'arc_sequence': arc_number
        }
    }

    return new_arc


def record_arc_completion(
    campaign_state: Dict,
    completed_arc: Dict,
    state_manager=None
) -> Tuple[bool, Optional[str]]:
    """
    Record completed arc in campaign state.

    Persists arc completion to campaign state and optionally saves via state manager:
    - Validates completed arc data
    - Updates campaign timestamps
    - Calls state_manager.save_all_tiers() if provided

    Args:
        campaign_state: Campaign state dict to update
        completed_arc: Completed arc state dict with 'arc_id', 'arc_name', 'encounters_in_arc'
        state_manager: Optional StateManager instance for persistence

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
        - (True, None) if recording succeeded
        - (False, error_msg) if validation or save failed

    Raises:
        ValueError: If completed_arc is missing required fields
    """
    if not isinstance(campaign_state, dict):
        return False, "campaign_state must be a dict"

    if not isinstance(completed_arc, dict):
        return False, "completed_arc must be a dict"

    # Validate completed arc has required fields
    required_arc_fields = ['arc_id', 'arc_name', 'encounters_in_arc']
    missing = [f for f in required_arc_fields if f not in completed_arc]
    if missing:
        raise ValueError(f"completed_arc missing required fields: {missing}")

    # Update campaign metadata with completed arc
    if 'completed_arcs' not in campaign_state:
        campaign_state['completed_arcs'] = []

    campaign_state['completed_arcs'].append({
        'arc_id': completed_arc['arc_id'],
        'arc_name': completed_arc['arc_name'],
        'encounters': completed_arc['encounters_in_arc'],
        'completed_at': datetime.utcnow().isoformat()
    })

    # Update campaign timestamp
    campaign_state['updated_at'] = datetime.utcnow().isoformat()

    # Persist via state manager if provided
    if state_manager:
        try:
            campaign_id = campaign_state['campaign_id']
            tier_states = {
                'campaign': campaign_state,
                'arc': completed_arc
            }
            state_manager.save_all_tiers(campaign_id, tier_states)
        except Exception as e:
            return False, f"Failed to save arc completion: {str(e)}"

    return True, None
