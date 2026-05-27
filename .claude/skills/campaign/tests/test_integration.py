"""
Integration Tests for Campaign Loop System

Tests the full campaign lifecycle:
- Load campaign from disk or create new
- Play campaign (sessions, scenes, combat)
- Save state to checkpoint
- Resume from checkpoint
- Verify state persistence and consistency across all 5 tiers

Integration tests validate the interaction between all modules:
- campaign-loop.py (CampaignLoop orchestration)
- state-manager.py (StateManager persistence)
- arc-transition.py (Arc progression mechanics)
"""

import pytest
import json
import tempfile
import importlib.util
from pathlib import Path
from datetime import datetime
from uuid import uuid4


# Import campaign modules
def load_campaign_modules():
    """Load campaign modules with importlib since filenames have hyphens."""
    campaign_dir = Path(__file__).parent.parent

    # Load campaign-loop.py
    spec = importlib.util.spec_from_file_location(
        "campaign_loop",
        campaign_dir / "campaign-loop.py"
    )
    campaign_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(campaign_module)

    # Load state-manager.py
    spec_sm = importlib.util.spec_from_file_location(
        "state_manager",
        campaign_dir / "state-manager.py"
    )
    state_module = importlib.util.module_from_spec(spec_sm)
    spec_sm.loader.exec_module(state_module)

    # Load arc-transition.py
    spec_at = importlib.util.spec_from_file_location(
        "arc_transition",
        campaign_dir / "arc-transition.py"
    )
    arc_module = importlib.util.module_from_spec(spec_at)
    spec_at.loader.exec_module(arc_module)

    return campaign_module, state_module, arc_module


campaign_module, state_module, arc_module = load_campaign_modules()

CampaignState = campaign_module.CampaignState
ArcState = campaign_module.ArcState
SessionState = campaign_module.SessionState
SceneState = campaign_module.SceneState
CombatState = campaign_module.CombatState
CampaignLoop = campaign_module.CampaignLoop
StateManager = state_module.StateManager
check_arc_completion = arc_module.check_arc_completion
advance_to_next_arc = arc_module.advance_to_next_arc
record_arc_completion = arc_module.record_arc_completion


# ============================================================================
# Campaign Load/Create Tests
# ============================================================================

class TestCampaignLoadCreate:
    """Test campaign loading and creation."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_create_new_campaign(self, temp_campaign_dir):
        """Test creating a new campaign from scratch."""
        loop = CampaignLoop(temp_campaign_dir)
        campaign = loop.load_campaign()

        assert campaign is not None
        assert campaign.campaign_id is not None
        assert campaign.campaign_name is not None
        assert campaign.total_encounters == 0
        assert campaign.total_arcs_completed == 0

    def test_campaign_has_valid_uuid(self, temp_campaign_dir):
        """Test new campaign has valid UUID."""
        loop = CampaignLoop(temp_campaign_dir)
        campaign = loop.load_campaign()

        # UUID is 36 characters with hyphens
        assert len(campaign.campaign_id) == 36
        assert campaign.campaign_id.count('-') == 4

    def test_campaign_initial_state_structure(self, temp_campaign_dir):
        """Test new campaign has correct initial state structure."""
        loop = CampaignLoop(temp_campaign_dir)
        campaign = loop.load_campaign()

        # All fields should be initialized
        assert hasattr(campaign, 'campaign_id')
        assert hasattr(campaign, 'campaign_name')
        assert hasattr(campaign, 'created_at')
        assert hasattr(campaign, 'total_encounters')
        assert hasattr(campaign, 'total_arcs_completed')
        assert hasattr(campaign, 'metadata')


# ============================================================================
# Campaign Session and State Tests
# ============================================================================

class TestCampaignSession:
    """Test campaign session management."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_new_session_creates_5_tiers(self, temp_campaign_dir):
        """Test that a new session initializes all 5 state tiers."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        assert 'campaign' in state
        assert 'arc' in state
        assert 'session' in state
        assert 'scene' in state
        assert state['campaign'] is not None
        assert state['arc'] is not None
        assert state['session'] is not None
        assert state['scene'] is not None

    def test_session_tier_hierarchy(self, temp_campaign_dir):
        """Test session tiers form correct parent-child hierarchy."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        campaign_id = state['campaign']['campaign_id']
        arc = state['arc']
        session = state['session']
        scene = state['scene']

        # Arc is child of campaign
        assert arc['parent_campaign_id'] == campaign_id

        # Session is child of arc
        assert session['parent_arc_id'] == arc['arc_id']

        # Scene is child of session
        assert scene['parent_session_id'] == session['session_id']

    def test_session_state_has_metadata(self, temp_campaign_dir):
        """Test session state includes metadata fields."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        session = state['session']
        assert 'session_id' in session
        assert 'parent_arc_id' in session
        assert 'encounters_this_session' in session
        assert 'started_at' in session
        assert 'metadata' in session


# ============================================================================
# State Save/Resume/Verify Cycle Tests
# ============================================================================

class TestSaveResumeCycle:
    """Test saving state and resuming from checkpoint."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_save_creates_checkpoint_file(self, temp_campaign_dir):
        """Test that saving state creates a checkpoint file."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        checkpoint_path = loop.save_checkpoint()
        assert checkpoint_path is not None
        assert Path(checkpoint_path).exists()

    def test_checkpoint_file_is_valid_json(self, temp_campaign_dir):
        """Test that checkpoint file contains valid JSON."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        checkpoint_path = loop.save_checkpoint()

        with open(checkpoint_path, 'r') as f:
            checkpoint_data = json.load(f)

        assert isinstance(checkpoint_data, dict)
        assert 'campaign' in checkpoint_data
        assert 'arc' in checkpoint_data

    def test_save_and_resume_preserves_campaign_id(self, temp_campaign_dir):
        """Test that campaign ID is preserved through save/resume."""
        # Create initial campaign
        loop1 = CampaignLoop(temp_campaign_dir)
        state1 = loop1.resume_session()
        campaign_id = state1['campaign']['campaign_id']
        checkpoint_path = loop1.save_checkpoint()

        # Resume from checkpoint
        loop2 = CampaignLoop(temp_campaign_dir)
        state2 = loop2.resume_session(checkpoint_path)
        assert state2['campaign']['campaign_id'] == campaign_id

    def test_save_and_resume_preserves_arc(self, temp_campaign_dir):
        """Test that arc state is preserved through save/resume."""
        loop1 = CampaignLoop(temp_campaign_dir)
        state1 = loop1.resume_session()
        arc_id = state1['arc']['arc_id']
        arc_name = state1['arc']['arc_name']
        checkpoint_path = loop1.save_checkpoint()

        loop2 = CampaignLoop(temp_campaign_dir)
        state2 = loop2.resume_session(checkpoint_path)
        assert state2['arc']['arc_id'] == arc_id
        assert state2['arc']['arc_name'] == arc_name

    def test_save_and_resume_preserves_session(self, temp_campaign_dir):
        """Test that session state is preserved through save/resume."""
        loop1 = CampaignLoop(temp_campaign_dir)
        state1 = loop1.resume_session()
        session_id = state1['session']['session_id']
        checkpoint_path = loop1.save_checkpoint()

        loop2 = CampaignLoop(temp_campaign_dir)
        state2 = loop2.resume_session(checkpoint_path)
        assert state2['session']['session_id'] == session_id

    def test_save_and_resume_preserves_scene(self, temp_campaign_dir):
        """Test that scene state is preserved through save/resume."""
        loop1 = CampaignLoop(temp_campaign_dir)
        state1 = loop1.resume_session()
        scene_id = state1['scene']['scene_id']
        checkpoint_path = loop1.save_checkpoint()

        loop2 = CampaignLoop(temp_campaign_dir)
        state2 = loop2.resume_session(checkpoint_path)
        assert state2['scene']['scene_id'] == scene_id


# ============================================================================
# Arc Progression Integration Tests
# ============================================================================

class TestArcProgression:
    """Test arc completion and advancement through the full system."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_detect_arc_completion_in_session(self, temp_campaign_dir):
        """Test detecting arc completion within a campaign session."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        arc = state['arc']
        arc['encounters_in_arc'] = 10

        # Check arc completion
        is_complete = check_arc_completion(arc, completion_threshold=10)
        assert is_complete is True

    def test_advance_arc_and_save(self, temp_campaign_dir):
        """Test advancing to next arc and saving state."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        campaign_dict = state['campaign']
        arc_dict = state['arc']

        # Record completion and advance
        success, error = record_arc_completion(campaign_dict, arc_dict)
        assert success is True
        assert error is None

        # Advance to next arc
        new_arc_dict = advance_to_next_arc(campaign_dict, arc_dict['arc_id'])
        assert new_arc_dict is not None
        assert campaign_dict['total_arcs_completed'] == 1

    def test_multiple_arc_cycles(self, temp_campaign_dir):
        """Test multiple arc completion cycles."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        campaign_dict = state['campaign']
        arc_ids = []

        # Simulate 3 arc completions
        for i in range(3):
            arc_dict = {
                'arc_id': str(uuid4()),
                'arc_name': f'Arc_{i}',
                'parent_campaign_id': campaign_dict['campaign_id'],
                'encounters_in_arc': 10 * (i + 1),
                'completed': False,
                'created_at': datetime.utcnow().isoformat()
            }
            arc_ids.append(arc_dict['arc_id'])

            # Record completion
            record_arc_completion(campaign_dict, arc_dict)

            # Advance if not last arc
            if i < 2:
                advance_to_next_arc(campaign_dict, arc_dict['arc_id'])

        # Verify all arcs were recorded
        assert campaign_dict['total_arcs_completed'] == 2  # Advanced 2 times
        assert len(campaign_dict.get('completed_arcs', [])) == 3


# ============================================================================
# Full Campaign Lifecycle Integration Tests
# ============================================================================

class TestFullCampaignLifecycle:
    """Test complete campaign lifecycle: create → play → save → resume → verify."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_complete_campaign_cycle(self, temp_campaign_dir):
        """Test full campaign cycle from creation to state persistence."""
        # Phase 1: Create campaign using CampaignLoop
        loop = CampaignLoop(temp_campaign_dir)
        initial_state = loop.resume_session()
        assert 'campaign' in initial_state
        assert 'arc' in initial_state
        assert 'session' in initial_state
        assert 'scene' in initial_state

        campaign_id = initial_state['campaign']['campaign_id']
        arc_id = initial_state['arc']['arc_id']
        session_id = initial_state['session']['session_id']

        # Phase 2: Validate state
        manager = StateManager(temp_campaign_dir)
        assert manager.validate_state(initial_state) is True

        # Phase 3: Save state to checkpoint
        checkpoint = loop.save_checkpoint()
        assert checkpoint is not None

        # Phase 4: Resume from checkpoint
        loop2 = CampaignLoop(temp_campaign_dir)
        resumed_state = loop2.resume_session(checkpoint)

        # Phase 5: Verify all state was preserved
        assert resumed_state['campaign']['campaign_id'] == campaign_id
        assert resumed_state['arc']['arc_id'] == arc_id
        assert resumed_state['session']['session_id'] == session_id

    def test_campaign_with_arc_completion(self, temp_campaign_dir):
        """Test campaign cycle including arc completion and advancement."""
        manager = StateManager(temp_campaign_dir)

        # Create and load initial campaign
        campaign = manager.load_campaign_state()
        state = manager.load_session_state()

        # Simulate arc completion
        state['arc']['encounters_in_arc'] = 15
        is_complete = check_arc_completion(state['arc'], completion_threshold=10)
        assert is_complete is True

        # Record completion and advance
        campaign_dict = state['campaign']
        arc_dict = state['arc']
        record_arc_completion(campaign_dict, arc_dict)
        new_arc = advance_to_next_arc(campaign_dict, arc_dict['arc_id'])

        # Verify advancement
        assert campaign_dict['total_arcs_completed'] == 1
        assert len(campaign_dict.get('completed_arcs', [])) == 1
        assert new_arc['parent_campaign_id'] == campaign_dict['campaign_id']

    def test_state_consistency_across_tiers(self, temp_campaign_dir):
        """Test that state is consistent across all 5 tiers after save/resume."""
        loop = CampaignLoop(temp_campaign_dir)
        state = loop.resume_session()

        # Capture IDs from all tiers
        campaign_id = state['campaign']['campaign_id']
        arc_id = state['arc']['arc_id']
        session_id = state['session']['session_id']
        scene_id = state['scene']['scene_id']

        # Save state
        checkpoint = loop.save_checkpoint()

        # Resume and verify hierarchy is intact
        manager = StateManager(temp_campaign_dir)
        resumed = manager.load_session_state(checkpoint)

        assert resumed['campaign']['campaign_id'] == campaign_id
        assert resumed['arc']['arc_id'] == arc_id
        assert resumed['arc']['parent_campaign_id'] == campaign_id
        assert resumed['session']['session_id'] == session_id
        assert resumed['session']['parent_arc_id'] == arc_id
        assert resumed['scene']['scene_id'] == scene_id
        assert resumed['scene']['parent_session_id'] == session_id


# ============================================================================
# State Validation and Error Handling Tests
# ============================================================================

class TestStateValidation:
    """Test state validation throughout lifecycle."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_validate_fresh_state(self, temp_campaign_dir):
        """Test that freshly created state validates successfully."""
        manager = StateManager(temp_campaign_dir)
        state = manager.load_session_state()

        assert manager.validate_state(state) is True

    def test_validate_after_update(self, temp_campaign_dir):
        """Test that state remains valid after updates."""
        manager = StateManager(temp_campaign_dir)
        state = manager.load_session_state()

        # Update some fields
        state['arc']['encounters_in_arc'] = 100
        state['session']['encounters_this_session'] = 50
        state['scene']['scene_description'] = "Updated scene"

        # Should still validate
        assert manager.validate_state(state) is True

    def test_invalid_state_breaks_hierarchy(self, temp_campaign_dir):
        """Test that state validation catches broken hierarchy."""
        manager = StateManager(temp_campaign_dir)
        invalid_state = manager.load_session_state()

        # Break the hierarchy
        invalid_state['arc']['parent_campaign_id'] = "wrong-campaign-id"

        with pytest.raises(ValueError, match="parent_campaign_id"):
            manager.validate_state(invalid_state)
