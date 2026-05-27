"""
Campaign Loop — Level 0 Campaign Orchestration

Implements the 5-step campaign lifecycle:
1. Load campaign from disk or initialize new
2. Resume session (restore all 5 state tiers)
3. Play campaign (invoke scene loop, track encounters)
4. Check arc completion (detect when arc is done)
5. Save and exit

The campaign loop coordinates between campaign, arc, session, scene, and combat tiers.
Follows D&D 5e rules and project tier conventions.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass
class CampaignState:
    """Tier 1: Campaign-level state (persists across all arcs)"""
    campaign_id: str
    campaign_name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    total_encounters: int = 0
    total_arcs_completed: int = 0
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        """Convert to dict, handling datetime serialization"""
        d = asdict(self)
        d['created_at'] = d['created_at'].isoformat()
        return d


@dataclass
class ArcState:
    """Tier 2: Arc-level state (current story arc)"""
    arc_id: str
    arc_name: str
    parent_campaign_id: str
    encounters_in_arc: int = 0
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        """Convert to dict, handling datetime serialization"""
        d = asdict(self)
        d['created_at'] = d['created_at'].isoformat()
        return d


@dataclass
class SessionState:
    """Tier 3: Session-level state (single play session)"""
    session_id: str
    parent_arc_id: str
    session_number: int = 1
    encounters_this_session: int = 0
    started_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        """Convert to dict, handling datetime serialization"""
        d = asdict(self)
        d['started_at'] = d['started_at'].isoformat()
        return d


@dataclass
class SceneState:
    """Tier 4: Scene-level state (scene within a session)"""
    scene_id: str
    parent_session_id: str
    scene_number: int = 1
    scene_description: str = ""
    completed: bool = False
    metadata: Dict = field(default_factory=dict)


@dataclass
class CombatState:
    """Tier 5: Combat-level state (ephemeral, current combat only)"""
    combat_id: str
    parent_scene_id: str
    round_number: int = 1
    active_combatants: List[str] = field(default_factory=list)
    completed: bool = False
    metadata: Dict = field(default_factory=dict)


class CampaignLoop:
    """
    Campaign orchestration engine — manages 5-tier game state hierarchy.

    Responsibilities:
    - Load/save campaign state to disk
    - Resume from checkpoint (restore all 5 tiers)
    - Coordinate campaign progression
    - Track encounters and arc completion
    """

    def __init__(self, campaign_dir: str = "./campaigns"):
        """
        Initialize campaign loop.

        Args:
            campaign_dir: Root directory for campaign data
        """
        self.campaign_dir = campaign_dir
        self.campaign: Optional[CampaignState] = None
        self.arc: Optional[ArcState] = None
        self.session: Optional[SessionState] = None
        self.scene: Optional[SceneState] = None
        self.combat: Optional[CombatState] = None

    def load_campaign(self, campaign_name: str = None) -> CampaignState:
        """
        Load campaign from disk or initialize new.

        Args:
            campaign_name: Name of campaign to load. If None, creates new.

        Returns:
            CampaignState object
        """
        if campaign_name:
            # Load existing campaign from disk
            campaign_path = os.path.join(self.campaign_dir, campaign_name, "campaign.json")
            if os.path.exists(campaign_path):
                with open(campaign_path, 'r') as f:
                    data = json.load(f)
                self.campaign = CampaignState(
                    campaign_id=data['campaign_id'],
                    campaign_name=data['campaign_name'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    total_encounters=data['total_encounters'],
                    total_arcs_completed=data['total_arcs_completed'],
                    metadata=data.get('metadata', {})
                )
                return self.campaign

        # Create new campaign
        campaign_id = str(uuid4())
        self.campaign = CampaignState(
            campaign_id=campaign_id,
            campaign_name=campaign_name or f"Campaign_{campaign_id[:8]}"
        )

        # Create campaign directory
        campaign_path = os.path.join(self.campaign_dir, self.campaign.campaign_name)
        os.makedirs(campaign_path, exist_ok=True)

        return self.campaign

    def resume_session(self, checkpoint_path: str = None) -> Dict:
        """
        Resume session from checkpoint, restoring all 5 state tiers.

        Restores:
        - Campaign (Tier 1)
        - Arc (Tier 2)
        - Session (Tier 3)
        - Scene (Tier 4)
        - Combat (Tier 5)

        Args:
            checkpoint_path: Path to checkpoint file. If None, creates new session.

        Returns:
            Dict with restored state for all 5 tiers
        """
        if checkpoint_path and os.path.exists(checkpoint_path):
            # Load all tiers from checkpoint
            with open(checkpoint_path, 'r') as f:
                data = json.load(f)

            # Restore campaign tier
            camp_data = data.get('campaign', {})
            self.campaign = CampaignState(
                campaign_id=camp_data['campaign_id'],
                campaign_name=camp_data['campaign_name'],
                created_at=datetime.fromisoformat(camp_data['created_at']),
                total_encounters=camp_data['total_encounters'],
                total_arcs_completed=camp_data['total_arcs_completed'],
                metadata=camp_data.get('metadata', {})
            )

            # Restore arc tier
            arc_data = data.get('arc', {})
            self.arc = ArcState(
                arc_id=arc_data['arc_id'],
                arc_name=arc_data['arc_name'],
                parent_campaign_id=arc_data['parent_campaign_id'],
                encounters_in_arc=arc_data['encounters_in_arc'],
                completed=arc_data['completed'],
                created_at=datetime.fromisoformat(arc_data['created_at']),
                metadata=arc_data.get('metadata', {})
            )

            # Restore session tier
            sess_data = data.get('session', {})
            self.session = SessionState(
                session_id=sess_data['session_id'],
                parent_arc_id=sess_data['parent_arc_id'],
                session_number=sess_data['session_number'],
                encounters_this_session=sess_data['encounters_this_session'],
                started_at=datetime.fromisoformat(sess_data['started_at']),
                metadata=sess_data.get('metadata', {})
            )

            # Restore scene tier
            scene_data = data.get('scene', {})
            self.scene = SceneState(
                scene_id=scene_data['scene_id'],
                parent_session_id=scene_data['parent_session_id'],
                scene_number=scene_data['scene_number'],
                scene_description=scene_data['scene_description'],
                completed=scene_data['completed'],
                metadata=scene_data.get('metadata', {})
            )

            # Restore combat tier (may be None if not in combat)
            combat_data = data.get('combat')
            if combat_data:
                self.combat = CombatState(
                    combat_id=combat_data['combat_id'],
                    parent_scene_id=combat_data['parent_scene_id'],
                    round_number=combat_data['round_number'],
                    active_combatants=combat_data['active_combatants'],
                    completed=combat_data['completed'],
                    metadata=combat_data.get('metadata', {})
                )
        else:
            # Create new session if no checkpoint or campaign exists
            if not self.campaign:
                self.load_campaign()

            # Create new arc if none exists
            if not self.arc:
                arc_id = str(uuid4())
                self.arc = ArcState(
                    arc_id=arc_id,
                    arc_name=f"Arc_{arc_id[:8]}",
                    parent_campaign_id=self.campaign.campaign_id
                )

            # Create new session
            session_id = str(uuid4())
            self.session = SessionState(
                session_id=session_id,
                parent_arc_id=self.arc.arc_id,
                session_number=1
            )

            # Create new scene
            scene_id = str(uuid4())
            self.scene = SceneState(
                scene_id=scene_id,
                parent_session_id=self.session.session_id,
                scene_number=1
            )

        return self._get_state_snapshot()

    def play_campaign(self, num_rounds: int = 1) -> Dict:
        """
        Play campaign for specified number of rounds.

        Invokes scene loop, tracks encounters, manages progression.

        Args:
            num_rounds: Number of game rounds to play

        Returns:
            Updated state after play
        """
        if not self.session:
            raise ValueError("Session not initialized. Call resume_session() first.")

        for _ in range(num_rounds):
            # Simulate scene progression
            if self.scene:
                self.scene.completed = True

            # Track encounter
            if self.session:
                self.session.encounters_this_session += 1
            if self.arc:
                self.arc.encounters_in_arc += 1
            if self.campaign:
                self.campaign.total_encounters += 1

        return self._get_state_snapshot()

    def check_arc_completion(self) -> bool:
        """
        Check if current arc is complete.

        Criteria:
        - Arc marked as completed, OR
        - Arc encounters exceed threshold

        Returns:
            True if arc is complete, False otherwise
        """
        if not self.arc:
            return False

        # Arc completion based on encounter count or explicit marking
        # Convention: 10+ encounters in arc = arc complete
        completion_threshold = 10
        return self.arc.completed or self.arc.encounters_in_arc >= completion_threshold

    def save_checkpoint(self, checkpoint_path: str = None) -> str:
        """
        Save all 5 state tiers to checkpoint file.

        Args:
            checkpoint_path: Path to save checkpoint. If None, auto-generates.

        Returns:
            Path where checkpoint was saved
        """
        if not checkpoint_path:
            if not self.campaign:
                raise ValueError("Campaign not initialized")

            campaign_dir = os.path.join(
                self.campaign_dir,
                self.campaign.campaign_name
            )
            os.makedirs(campaign_dir, exist_ok=True)

            timestamp = datetime.utcnow().isoformat().replace(':', '-').replace('.', '_')
            checkpoint_path = os.path.join(
                campaign_dir,
                f"checkpoint_{timestamp}.json"
            )

        # Build state snapshot
        checkpoint = {
            'timestamp': datetime.utcnow().isoformat(),
            'campaign': self.campaign.to_dict() if self.campaign else None,
            'arc': self.arc.to_dict() if self.arc else None,
            'session': self.session.to_dict() if self.session else None,
            'scene': asdict(self.scene) if self.scene else None,
            'combat': asdict(self.combat) if self.combat else None,
        }

        # Ensure directory exists
        os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)

        # Write checkpoint
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2, default=str)

        return checkpoint_path

    def _get_state_snapshot(self) -> Dict:
        """Get snapshot of all 5 state tiers"""
        return {
            'campaign': asdict(self.campaign) if self.campaign else None,
            'arc': asdict(self.arc) if self.arc else None,
            'session': asdict(self.session) if self.session else None,
            'scene': asdict(self.scene) if self.scene else None,
            'combat': asdict(self.combat) if self.combat else None,
        }


# Module-level convenience functions
def load_campaign(campaign_name: str = None) -> CampaignState:
    """Load campaign from disk or initialize new."""
    loop = CampaignLoop()
    return loop.load_campaign(campaign_name)


def resume_session(checkpoint_path: str = None) -> Dict:
    """Resume session from checkpoint."""
    loop = CampaignLoop()
    return loop.resume_session(checkpoint_path)


def play_campaign(num_rounds: int = 1) -> Dict:
    """Play campaign rounds (requires active session)."""
    loop = CampaignLoop()
    loop.resume_session()
    return loop.play_campaign(num_rounds)


def check_arc_completion() -> bool:
    """Check if current arc is complete."""
    loop = CampaignLoop()
    loop.resume_session()
    return loop.check_arc_completion()


def save_checkpoint(checkpoint_path: str = None) -> str:
    """Save state checkpoint."""
    loop = CampaignLoop()
    loop.resume_session()
    return loop.save_checkpoint(checkpoint_path)
