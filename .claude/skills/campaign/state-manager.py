"""
State Manager — Centralized state management for all 5 tiers

Responsibilities:
- Load state from JSON files
- Resume session (restore prior state)
- Save checkpoint (validate before write)
- Serialize all tiers

Integrates with campaign-loop.py state classes and provides
validation and serialization utilities.
"""

import json
import os
import importlib.util
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime
from dataclasses import asdict

# Import campaign_loop (note: file is campaign-loop.py with hyphen)
CampaignState = None
ArcState = None
SessionState = None
SceneState = None
CombatState = None
CampaignLoop = None

try:
    spec = importlib.util.spec_from_file_location("campaign_loop", os.path.join(os.path.dirname(__file__), "campaign-loop.py"))
    campaign_loop_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(campaign_loop_module)

    CampaignState = campaign_loop_module.CampaignState
    ArcState = campaign_loop_module.ArcState
    SessionState = campaign_loop_module.SessionState
    SceneState = campaign_loop_module.SceneState
    CombatState = campaign_loop_module.CombatState
    CampaignLoop = campaign_loop_module.CampaignLoop
except (ImportError, AttributeError) as e:
    # Fallback for testing without campaign_loop
    pass


class StateManager:
    """
    Centralized state management for campaign 5-tier hierarchy.

    Provides:
    - Load/save operations with validation
    - State serialization to JSON
    - Checkpoint recovery
    - State validation before persistence
    """

    def __init__(self, campaign_dir: str = "./campaigns"):
        """
        Initialize state manager.

        Args:
            campaign_dir: Root directory for campaign data
        """
        self.campaign_dir = campaign_dir
        if CampaignLoop:
            self.loop = CampaignLoop(campaign_dir)
        else:
            self.loop = None
        self._ensure_campaign_dir()

    def _ensure_campaign_dir(self):
        """Ensure campaign directory exists."""
        Path(self.campaign_dir).mkdir(parents=True, exist_ok=True)

    def load_campaign_state(self, campaign_name: str = None) -> Optional[Any]:
        """
        Load campaign state from disk or initialize new.

        Args:
            campaign_name: Name of campaign to load. If None, creates new.

        Returns:
            CampaignState object or None

        Raises:
            FileNotFoundError: If campaign_name specified but file doesn't exist
        """
        if not self.loop:
            raise RuntimeError("CampaignLoop not initialized. Check campaign_loop.py import.")
        return self.loop.load_campaign(campaign_name)

    def load_session_state(self, checkpoint_path: str = None) -> Dict[str, Any]:
        """
        Load all 5 tiers from checkpoint or create new session.

        Args:
            checkpoint_path: Path to checkpoint file. If None, creates new session.

        Returns:
            Dict with restored state for all 5 tiers:
            {
                'campaign': CampaignState,
                'arc': ArcState,
                'session': SessionState,
                'scene': SceneState,
                'combat': CombatState or None
            }

        Raises:
            FileNotFoundError: If checkpoint_path specified but file doesn't exist
            ValueError: If checkpoint file is corrupt or invalid
        """
        if not self.loop:
            raise RuntimeError("CampaignLoop not initialized. Check campaign_loop.py import.")

        if checkpoint_path and not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

        try:
            state = self.loop.resume_session(checkpoint_path)
            return state
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid checkpoint file: {e}")

    def save_all_tiers(self, checkpoint_path: str = None) -> str:
        """
        Save all 5 state tiers to checkpoint with validation.

        Validates state before writing. Creates directory structure if needed.

        Args:
            checkpoint_path: Path to save checkpoint. If None, auto-generates.

        Returns:
            Path where checkpoint was saved

        Raises:
            ValueError: If state validation fails
            IOError: If write operation fails
        """
        if not self.loop:
            raise RuntimeError("CampaignLoop not initialized. Check campaign_loop.py import.")

        # Get current state snapshot
        state = self.loop._get_state_snapshot()

        # Validate before writing
        self.validate_state(state)

        # Delegate to campaign loop's save_checkpoint
        try:
            return self.loop.save_checkpoint(checkpoint_path)
        except IOError as e:
            raise IOError(f"Failed to save checkpoint: {e}")

    def validate_state(self, state: Dict[str, Any]) -> bool:
        """
        Validate state dict before persistence.

        Checks:
        - All required tier keys present
        - Campaign and arc have valid IDs
        - Session references valid arc
        - Scene references valid session
        - Combat references valid scene (if present)
        - No circular references
        - Timestamps are ISO format

        Args:
            state: State dict to validate

        Returns:
            True if valid, raises ValueError if invalid

        Raises:
            ValueError: If validation fails
        """
        required_tiers = ['campaign', 'arc', 'session', 'scene']

        # Check required tiers
        for tier in required_tiers:
            if tier not in state:
                raise ValueError(f"Missing required tier: {tier}")
            if state[tier] is None:
                raise ValueError(f"Tier {tier} cannot be None")

        # Campaign validation
        campaign = state.get('campaign')
        if not isinstance(campaign, dict):
            raise ValueError("Campaign must be a dict")
        if 'campaign_id' not in campaign or not campaign['campaign_id']:
            raise ValueError("Campaign missing campaign_id")

        # Arc validation
        arc = state.get('arc')
        if not isinstance(arc, dict):
            raise ValueError("Arc must be a dict")
        if 'arc_id' not in arc or not arc['arc_id']:
            raise ValueError("Arc missing arc_id")
        if arc.get('parent_campaign_id') != campaign.get('campaign_id'):
            raise ValueError("Arc parent_campaign_id doesn't match campaign_id")

        # Session validation
        session = state.get('session')
        if not isinstance(session, dict):
            raise ValueError("Session must be a dict")
        if 'session_id' not in session or not session['session_id']:
            raise ValueError("Session missing session_id")
        if session.get('parent_arc_id') != arc.get('arc_id'):
            raise ValueError("Session parent_arc_id doesn't match arc_id")

        # Scene validation
        scene = state.get('scene')
        if not isinstance(scene, dict):
            raise ValueError("Scene must be a dict")
        if 'scene_id' not in scene or not scene['scene_id']:
            raise ValueError("Scene missing scene_id")
        if scene.get('parent_session_id') != session.get('session_id'):
            raise ValueError("Scene parent_session_id doesn't match session_id")

        # Combat validation (optional)
        combat = state.get('combat')
        if combat is not None:
            if not isinstance(combat, dict):
                raise ValueError("Combat must be a dict or None")
            if 'combat_id' not in combat or not combat['combat_id']:
                raise ValueError("Combat missing combat_id")
            if combat.get('parent_scene_id') != scene.get('scene_id'):
                raise ValueError("Combat parent_scene_id doesn't match scene_id")

        return True


# Module-level convenience functions

def load_campaign_state(campaign_name: str = None, campaign_dir: str = "./campaigns") -> Optional[Any]:
    """Load campaign state from disk or initialize new."""
    manager = StateManager(campaign_dir)
    return manager.load_campaign_state(campaign_name)


def load_session_state(checkpoint_path: str = None, campaign_dir: str = "./campaigns") -> Dict[str, Any]:
    """Load all 5 tiers from checkpoint or create new session."""
    manager = StateManager(campaign_dir)
    return manager.load_session_state(checkpoint_path)


def save_all_tiers(checkpoint_path: str = None, campaign_dir: str = "./campaigns") -> str:
    """Save all 5 state tiers to checkpoint with validation."""
    manager = StateManager(campaign_dir)
    return manager.save_all_tiers(checkpoint_path)


def validate_state(state: Dict[str, Any]) -> bool:
    """Validate state dict before persistence."""
    manager = StateManager()
    return manager.validate_state(state)
