"""
Unit Tests for Campaign Loop, State Manager, and Arc Transition Modules

Tests cover:
- campaign-loop.py: CampaignState, ArcState, SessionState, SceneState, CombatState (to_dict serialization)
- state-manager.py: load_campaign_state, load_session_state, save_all_tiers, validate_state
- arc-transition.py: check_arc_completion, advance_to_next_arc, record_arc_completion
"""

import pytest
import json
import os
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
# Campaign-Loop State Tests (to_dict serialization)
# ============================================================================

class TestCampaignState:
    """Test CampaignState dataclass and serialization."""

    def test_campaign_state_creation(self):
        """Test creating a CampaignState instance."""
        state = CampaignState(
            campaign_id="test-camp-1",
            campaign_name="Test Campaign"
        )
        assert state.campaign_id == "test-camp-1"
        assert state.campaign_name == "Test Campaign"
        assert state.total_encounters == 0
        assert state.total_arcs_completed == 0
        assert isinstance(state.created_at, datetime)

    def test_campaign_state_to_dict(self):
        """Test CampaignState.to_dict() serialization."""
        state = CampaignState(
            campaign_id="camp-001",
            campaign_name="Epic Quest"
        )
        result = state.to_dict()

        assert isinstance(result, dict)
        assert result['campaign_id'] == "camp-001"
        assert result['campaign_name'] == "Epic Quest"
        assert 'created_at' in result
        assert isinstance(result['created_at'], str)  # ISO format

    def test_campaign_state_metadata(self):
        """Test CampaignState with custom metadata."""
        state = CampaignState(
            campaign_id="camp-002",
            campaign_name="Adventure",
            metadata={"difficulty": "hard", "setting": "fantasy"}
        )
        result = state.to_dict()
        assert result['metadata']['difficulty'] == "hard"


class TestArcState:
    """Test ArcState dataclass and serialization."""

    def test_arc_state_creation(self):
        """Test creating an ArcState instance."""
        state = ArcState(
            arc_id="arc-1",
            arc_name="First Arc",
            parent_campaign_id="camp-001"
        )
        assert state.arc_id == "arc-1"
        assert state.arc_name == "First Arc"
        assert state.parent_campaign_id == "camp-001"
        assert state.encounters_in_arc == 0
        assert state.completed is False

    def test_arc_state_to_dict(self):
        """Test ArcState.to_dict() serialization."""
        state = ArcState(
            arc_id="arc-100",
            arc_name="Dragon's Lair",
            parent_campaign_id="camp-001",
            encounters_in_arc=5,
            completed=True
        )
        result = state.to_dict()

        assert isinstance(result, dict)
        assert result['arc_id'] == "arc-100"
        assert result['encounters_in_arc'] == 5
        assert result['completed'] is True
        assert isinstance(result['created_at'], str)


class TestSessionState:
    """Test SessionState dataclass."""

    def test_session_state_creation(self):
        """Test creating a SessionState instance."""
        state = SessionState(
            session_id="sess-1",
            parent_arc_id="arc-1"
        )
        assert state.session_id == "sess-1"
        assert state.parent_arc_id == "arc-1"

    def test_session_state_to_dict(self):
        """Test SessionState.to_dict() serialization."""
        state = SessionState(
            session_id="sess-100",
            parent_arc_id="arc-100"
        )
        result = state.to_dict()
        assert result['session_id'] == "sess-100"
        assert result['parent_arc_id'] == "arc-100"


class TestSceneState:
    """Test SceneState dataclass."""

    def test_scene_state_creation(self):
        """Test creating a SceneState instance."""
        state = SceneState(
            scene_id="scene-1",
            parent_session_id="sess-1"
        )
        assert state.scene_id == "scene-1"
        assert state.parent_session_id == "sess-1"

    def test_scene_state_fields(self):
        """Test SceneState fields."""
        state = SceneState(
            scene_id="scene-100",
            parent_session_id="sess-100",
            scene_number=5,
            scene_description="Tavern"
        )
        assert state.scene_id == "scene-100"
        assert state.scene_number == 5
        assert state.scene_description == "Tavern"


class TestCombatState:
    """Test CombatState dataclass."""

    def test_combat_state_creation(self):
        """Test creating a CombatState instance."""
        state = CombatState(
            combat_id="combat-1",
            parent_scene_id="scene-1"
        )
        assert state.combat_id == "combat-1"
        assert state.parent_scene_id == "scene-1"

    def test_combat_state_fields(self):
        """Test CombatState fields."""
        state = CombatState(
            combat_id="combat-100",
            parent_scene_id="scene-100",
            round_number=3,
            active_combatants=["orc-1", "party"]
        )
        assert state.combat_id == "combat-100"
        assert state.round_number == 3
        assert len(state.active_combatants) == 2


# ============================================================================
# Campaign Loop Tests (load, resume, save, play, check_arc_completion)
# ============================================================================

class TestCampaignLoop:
    """Test CampaignLoop load, resume, save, and arc completion operations."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_campaign_loop_initialization(self, temp_campaign_dir):
        """Test CampaignLoop initialization."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        assert loop.campaign_dir == temp_campaign_dir
        assert loop.campaign is None
        assert loop.arc is None
        assert loop.session is None
        assert loop.scene is None
        assert loop.combat is None

    def test_load_campaign_new_campaign(self, temp_campaign_dir):
        """Test loading/creating a new campaign."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        campaign = loop.load_campaign()

        assert campaign is not None
        assert campaign.campaign_id is not None
        assert campaign.campaign_name is not None
        assert campaign.total_encounters == 0
        assert campaign.total_arcs_completed == 0
        assert loop.campaign == campaign

    def test_load_campaign_with_name(self, temp_campaign_dir):
        """Test loading campaign with specific name."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        campaign = loop.load_campaign("TestCampaign")

        assert campaign.campaign_name == "TestCampaign"
        assert campaign.campaign_id is not None

    def test_load_campaign_existing_from_disk(self, temp_campaign_dir):
        """Test loading existing campaign from disk."""
        # Create and save a campaign
        loop1 = CampaignLoop(campaign_dir=temp_campaign_dir)
        campaign1 = loop1.load_campaign("ExistingCampaign")
        campaign1.total_encounters = 5
        campaign1.total_arcs_completed = 2

        # Save to disk
        campaign_dir = os.path.join(temp_campaign_dir, "ExistingCampaign")
        os.makedirs(campaign_dir, exist_ok=True)
        campaign_json_path = os.path.join(campaign_dir, "campaign.json")
        with open(campaign_json_path, 'w') as f:
            json.dump(campaign1.to_dict(), f)

        # Load campaign in new loop
        loop2 = CampaignLoop(campaign_dir=temp_campaign_dir)
        campaign2 = loop2.load_campaign("ExistingCampaign")

        assert campaign2.campaign_id == campaign1.campaign_id
        assert campaign2.total_encounters == 5
        assert campaign2.total_arcs_completed == 2

    def test_resume_session_new(self, temp_campaign_dir):
        """Test resuming a new session creates all 5 tiers."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        state = loop.resume_session()

        assert state['campaign'] is not None
        assert state['arc'] is not None
        assert state['session'] is not None
        assert state['scene'] is not None
        assert loop.campaign is not None
        assert loop.arc is not None
        assert loop.session is not None
        assert loop.scene is not None

    def test_resume_session_hierarchy_relationships(self, temp_campaign_dir):
        """Test that resumed session has correct hierarchy relationships."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        state = loop.resume_session()

        assert state['arc']['parent_campaign_id'] == state['campaign']['campaign_id']
        assert state['session']['parent_arc_id'] == state['arc']['arc_id']
        assert state['scene']['parent_session_id'] == state['session']['session_id']

    def test_resume_session_from_checkpoint(self, temp_campaign_dir):
        """Test resuming session from checkpoint file."""
        # Create and save initial state
        loop1 = CampaignLoop(campaign_dir=temp_campaign_dir)
        state1 = loop1.resume_session()
        loop1.campaign.total_encounters = 3
        loop1.arc.encounters_in_arc = 3

        checkpoint_path = os.path.join(temp_campaign_dir, "checkpoint.json")
        loop1.save_checkpoint(checkpoint_path)

        # Resume from checkpoint in new loop
        loop2 = CampaignLoop(campaign_dir=temp_campaign_dir)
        state2 = loop2.resume_session(checkpoint_path)

        assert state2['campaign']['campaign_id'] == state1['campaign']['campaign_id']
        assert state2['arc']['arc_id'] == state1['arc']['arc_id']
        assert state2['campaign']['total_encounters'] == 3
        assert state2['arc']['encounters_in_arc'] == 3

    def test_save_checkpoint_creates_file(self, temp_campaign_dir):
        """Test save_checkpoint creates file."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()

        checkpoint_path = os.path.join(temp_campaign_dir, "test_checkpoint.json")
        saved_path = loop.save_checkpoint(checkpoint_path)

        assert os.path.exists(saved_path)
        with open(saved_path, 'r') as f:
            data = json.load(f)
        assert 'campaign' in data
        assert 'arc' in data
        assert 'session' in data
        assert 'scene' in data

    def test_save_checkpoint_auto_generated_path(self, temp_campaign_dir):
        """Test save_checkpoint generates path automatically."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()

        saved_path = loop.save_checkpoint()

        assert os.path.exists(saved_path)
        assert "checkpoint_" in os.path.basename(saved_path)

    def test_save_checkpoint_without_campaign(self, temp_campaign_dir):
        """Test save_checkpoint raises when campaign not initialized."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)

        with pytest.raises(ValueError, match="Campaign not initialized"):
            loop.save_checkpoint()

    def test_play_campaign_increments_encounters(self, temp_campaign_dir):
        """Test play_campaign increments encounter counters."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()
        initial_encounters = loop.campaign.total_encounters

        state = loop.play_campaign(num_rounds=3)

        assert loop.campaign.total_encounters == initial_encounters + 3
        assert loop.arc.encounters_in_arc == 3
        assert loop.session.encounters_this_session == 3

    def test_play_campaign_multiple_rounds(self, temp_campaign_dir):
        """Test play_campaign with multiple rounds."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()

        loop.play_campaign(num_rounds=5)

        assert loop.campaign.total_encounters == 5
        assert loop.arc.encounters_in_arc == 5
        assert loop.session.encounters_this_session == 5

    def test_play_campaign_without_session(self, temp_campaign_dir):
        """Test play_campaign raises without active session."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)

        with pytest.raises(ValueError, match="Session not initialized"):
            loop.play_campaign()

    def test_check_arc_completion_explicit_flag(self, temp_campaign_dir):
        """Test arc completion via explicit flag."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()
        loop.arc.completed = True

        assert loop.check_arc_completion() is True

    def test_check_arc_completion_encounter_threshold(self, temp_campaign_dir):
        """Test arc completion via encounter threshold."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()

        # Play enough rounds to reach default threshold of 10
        loop.play_campaign(num_rounds=10)

        assert loop.check_arc_completion() is True

    def test_check_arc_completion_not_complete(self, temp_campaign_dir):
        """Test arc not complete when below threshold."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()

        loop.play_campaign(num_rounds=5)

        assert loop.check_arc_completion() is False

    def test_check_arc_completion_no_arc(self, temp_campaign_dir):
        """Test check_arc_completion returns False when arc is None."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)

        assert loop.check_arc_completion() is False

    def test_get_state_snapshot(self, temp_campaign_dir):
        """Test _get_state_snapshot returns all tiers."""
        loop = CampaignLoop(campaign_dir=temp_campaign_dir)
        loop.resume_session()

        snapshot = loop._get_state_snapshot()

        assert 'campaign' in snapshot
        assert 'arc' in snapshot
        assert 'session' in snapshot
        assert 'scene' in snapshot
        assert 'combat' in snapshot


# ============================================================================
# State Manager Tests (load, resume, save, validate)
# ============================================================================

class TestStateManager:
    """Test StateManager load, resume, save, and validate operations."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_state_manager_initialization(self, temp_campaign_dir):
        """Test StateManager initialization."""
        manager = StateManager(temp_campaign_dir)
        assert manager.campaign_dir == temp_campaign_dir
        assert Path(temp_campaign_dir).exists()

    def test_load_campaign_state_creates_new(self, temp_campaign_dir):
        """Test load_campaign_state creates new campaign when none exists."""
        manager = StateManager(temp_campaign_dir)
        campaign = manager.load_campaign_state(campaign_name=None)

        assert campaign is not None
        assert hasattr(campaign, 'campaign_id')
        assert hasattr(campaign, 'campaign_name')

    def test_load_session_state_creates_new(self, temp_campaign_dir):
        """Test load_session_state creates new session when checkpoint is None."""
        manager = StateManager(temp_campaign_dir)
        state = manager.load_session_state(checkpoint_path=None)

        assert isinstance(state, dict)
        assert 'campaign' in state
        assert 'arc' in state
        assert 'session' in state
        assert 'scene' in state

    def test_validate_state_success(self, temp_campaign_dir):
        """Test validate_state with valid state dict."""
        manager = StateManager(temp_campaign_dir)
        state = manager.load_session_state()

        # This should not raise
        result = manager.validate_state(state)
        assert result is True

    def test_validate_state_missing_tier(self, temp_campaign_dir):
        """Test validate_state raises ValueError for missing tier."""
        manager = StateManager(temp_campaign_dir)
        invalid_state = {'campaign': {}}

        with pytest.raises(ValueError, match="Missing required tier"):
            manager.validate_state(invalid_state)

    def test_validate_state_missing_campaign_id(self, temp_campaign_dir):
        """Test validate_state raises ValueError when campaign_id missing."""
        manager = StateManager(temp_campaign_dir)
        invalid_state = {
            'campaign': {},
            'arc': {'arc_id': 'test'},
            'session': {'session_id': 'test'},
            'scene': {'scene_id': 'test'}
        }

        with pytest.raises(ValueError, match="campaign_id"):
            manager.validate_state(invalid_state)

    def test_validate_state_arc_parent_mismatch(self, temp_campaign_dir):
        """Test validate_state raises ValueError when arc parent_campaign_id doesn't match."""
        manager = StateManager(temp_campaign_dir)
        invalid_state = {
            'campaign': {'campaign_id': 'camp-1', 'campaign_name': 'test'},
            'arc': {'arc_id': 'arc-1', 'parent_campaign_id': 'camp-2'},
            'session': {'session_id': 'sess-1', 'parent_arc_id': 'arc-1'},
            'scene': {'scene_id': 'scene-1', 'parent_session_id': 'sess-1'}
        }

        with pytest.raises(ValueError, match="parent_campaign_id"):
            manager.validate_state(invalid_state)

    def test_save_all_tiers_creates_checkpoint(self, temp_campaign_dir):
        """Test save_all_tiers creates checkpoint file."""
        manager = StateManager(temp_campaign_dir)
        manager.load_session_state()

        checkpoint_path = os.path.join(temp_campaign_dir, "saved.json")
        saved_path = manager.save_all_tiers(checkpoint_path)

        assert os.path.exists(saved_path)
        with open(saved_path, 'r') as f:
            data = json.load(f)
        assert 'campaign' in data
        assert 'arc' in data
        assert 'session' in data
        assert 'scene' in data

    def test_save_all_tiers_auto_path(self, temp_campaign_dir):
        """Test save_all_tiers with auto-generated path."""
        manager = StateManager(temp_campaign_dir)
        manager.load_session_state()

        saved_path = manager.save_all_tiers()

        assert os.path.exists(saved_path)

    def test_validate_state_campaign_none(self, temp_campaign_dir):
        """Test validate_state raises when campaign is None."""
        manager = StateManager(temp_campaign_dir)
        invalid_state = {
            'campaign': None,
            'arc': {'arc_id': 'arc-1'},
            'session': {'session_id': 'sess-1'},
            'scene': {'scene_id': 'scene-1'}
        }

        with pytest.raises(ValueError, match="cannot be None"):
            manager.validate_state(invalid_state)

    def test_validate_state_session_parent_mismatch(self, temp_campaign_dir):
        """Test validate_state raises when session parent doesn't match arc."""
        manager = StateManager(temp_campaign_dir)
        invalid_state = {
            'campaign': {'campaign_id': 'camp-1', 'campaign_name': 'test'},
            'arc': {'arc_id': 'arc-1', 'parent_campaign_id': 'camp-1'},
            'session': {'session_id': 'sess-1', 'parent_arc_id': 'arc-2'},
            'scene': {'scene_id': 'scene-1', 'parent_session_id': 'sess-1'}
        }

        with pytest.raises(ValueError, match="parent_arc_id"):
            manager.validate_state(invalid_state)

    def test_validate_state_scene_parent_mismatch(self, temp_campaign_dir):
        """Test validate_state raises when scene parent doesn't match session."""
        manager = StateManager(temp_campaign_dir)
        invalid_state = {
            'campaign': {'campaign_id': 'camp-1', 'campaign_name': 'test'},
            'arc': {'arc_id': 'arc-1', 'parent_campaign_id': 'camp-1'},
            'session': {'session_id': 'sess-1', 'parent_arc_id': 'arc-1'},
            'scene': {'scene_id': 'scene-1', 'parent_session_id': 'sess-2'}
        }

        with pytest.raises(ValueError, match="parent_session_id"):
            manager.validate_state(invalid_state)

    def test_validate_state_with_combat(self, temp_campaign_dir):
        """Test validate_state with combat tier."""
        manager = StateManager(temp_campaign_dir)
        camp_id = 'camp-1'
        arc_id = 'arc-1'
        sess_id = 'sess-1'
        scene_id = 'scene-1'

        valid_state = {
            'campaign': {'campaign_id': camp_id, 'campaign_name': 'test'},
            'arc': {'arc_id': arc_id, 'parent_campaign_id': camp_id},
            'session': {'session_id': sess_id, 'parent_arc_id': arc_id},
            'scene': {'scene_id': scene_id, 'parent_session_id': sess_id},
            'combat': {'combat_id': 'combat-1', 'parent_scene_id': scene_id}
        }

        assert manager.validate_state(valid_state) is True

    def test_validate_state_combat_parent_mismatch(self, temp_campaign_dir):
        """Test validate_state raises when combat parent doesn't match scene."""
        manager = StateManager(temp_campaign_dir)
        camp_id = 'camp-1'
        arc_id = 'arc-1'
        sess_id = 'sess-1'
        scene_id = 'scene-1'

        invalid_state = {
            'campaign': {'campaign_id': camp_id, 'campaign_name': 'test'},
            'arc': {'arc_id': arc_id, 'parent_campaign_id': camp_id},
            'session': {'session_id': sess_id, 'parent_arc_id': arc_id},
            'scene': {'scene_id': scene_id, 'parent_session_id': sess_id},
            'combat': {'combat_id': 'combat-1', 'parent_scene_id': 'scene-2'}
        }

        with pytest.raises(ValueError, match="parent_scene_id"):
            manager.validate_state(invalid_state)


# ============================================================================
# Arc Transition Tests (check, advance, record)
# ============================================================================

class TestCheckArcCompletion:
    """Test check_arc_completion function."""

    def test_check_arc_explicit_completion(self):
        """Test arc completion when explicitly marked."""
        arc_state = {
            'completed': True,
            'encounters_in_arc': 0
        }
        result = check_arc_completion(arc_state)
        assert result is True

    def test_check_arc_threshold_completion(self):
        """Test arc completion when encounter threshold reached."""
        arc_state = {
            'completed': False,
            'encounters_in_arc': 10
        }
        result = check_arc_completion(arc_state, completion_threshold=10)
        assert result is True

    def test_check_arc_below_threshold(self):
        """Test arc not complete when below encounter threshold."""
        arc_state = {
            'completed': False,
            'encounters_in_arc': 5
        }
        result = check_arc_completion(arc_state, completion_threshold=10)
        assert result is False

    def test_check_arc_custom_threshold(self):
        """Test arc completion with custom threshold."""
        arc_state = {
            'completed': False,
            'encounters_in_arc': 7
        }
        result = check_arc_completion(arc_state, completion_threshold=5)
        assert result is True

    def test_check_arc_invalid_state_type(self):
        """Test check_arc_completion raises ValueError for non-dict state."""
        with pytest.raises(ValueError, match="must be a dict"):
            check_arc_completion("not a dict")

    def test_check_arc_missing_fields(self):
        """Test check_arc_completion raises ValueError for missing fields."""
        arc_state = {'completed': True}
        with pytest.raises(ValueError, match="missing required fields"):
            check_arc_completion(arc_state)


class TestAdvanceToNextArc:
    """Test advance_to_next_arc function."""

    def test_advance_to_next_arc_basic(self):
        """Test advancing to next arc creates valid new arc."""
        campaign_state = {
            'campaign_id': 'camp-001',
            'total_arcs_completed': 2
        }
        completed_arc_id = 'arc-1'

        new_arc = advance_to_next_arc(campaign_state, completed_arc_id)

        assert isinstance(new_arc, dict)
        assert 'arc_id' in new_arc
        assert 'arc_name' in new_arc
        assert new_arc['parent_campaign_id'] == 'camp-001'
        assert new_arc['encounters_in_arc'] == 0
        assert new_arc['completed'] is False

    def test_advance_increments_counter(self):
        """Test advancing to next arc increments campaign counter."""
        campaign_state = {
            'campaign_id': 'camp-001',
            'total_arcs_completed': 0
        }

        new_arc = advance_to_next_arc(campaign_state, 'arc-0')

        assert campaign_state['total_arcs_completed'] == 1
        # Arc name is generated as Arc_N where N = total_arcs_completed + 1
        assert 'Arc_2' in new_arc['arc_name']

    def test_advance_invalid_campaign_state_type(self):
        """Test advance_to_next_arc raises ValueError for non-dict state."""
        with pytest.raises(ValueError, match="must be a dict"):
            advance_to_next_arc("not a dict", "arc-1")

    def test_advance_missing_campaign_fields(self):
        """Test advance_to_next_arc raises ValueError for missing fields."""
        campaign_state = {'campaign_id': 'camp-001'}  # Missing total_arcs_completed

        with pytest.raises(ValueError, match="missing required fields"):
            advance_to_next_arc(campaign_state, "arc-1")

    def test_advance_preserves_metadata(self):
        """Test that new arc includes metadata with previous arc reference."""
        campaign_state = {
            'campaign_id': 'camp-001',
            'total_arcs_completed': 1
        }

        new_arc = advance_to_next_arc(campaign_state, 'arc-previous')

        assert 'metadata' in new_arc
        assert new_arc['metadata']['previous_arc_id'] == 'arc-previous'
        # arc_sequence is total_arcs_completed + 1 after increment
        assert new_arc['metadata']['arc_sequence'] == 3


class TestRecordArcCompletion:
    """Test record_arc_completion function."""

    def test_record_arc_completion_success(self):
        """Test recording arc completion succeeds with valid inputs."""
        campaign_state = {
            'campaign_id': 'camp-001'
        }
        completed_arc = {
            'arc_id': 'arc-1',
            'arc_name': 'First Arc',
            'encounters_in_arc': 10
        }

        success, error = record_arc_completion(campaign_state, completed_arc)

        assert success is True
        assert error is None
        assert 'completed_arcs' in campaign_state
        assert len(campaign_state['completed_arcs']) == 1

    def test_record_arc_invalid_campaign_state_type(self):
        """Test record_arc_completion handles non-dict campaign state."""
        result = record_arc_completion("not a dict", {'arc_id': 'arc-1', 'arc_name': 'test', 'encounters_in_arc': 0})

        assert result[0] is False
        assert "must be a dict" in result[1]

    def test_record_arc_invalid_arc_type(self):
        """Test record_arc_completion handles non-dict arc state."""
        campaign_state = {'campaign_id': 'camp-001'}
        result = record_arc_completion(campaign_state, "not a dict")

        assert result[0] is False
        assert "must be a dict" in result[1]

    def test_record_arc_missing_arc_fields(self):
        """Test record_arc_completion raises ValueError for missing arc fields."""
        campaign_state = {'campaign_id': 'camp-001'}
        incomplete_arc = {'arc_id': 'arc-1'}  # Missing arc_name and encounters_in_arc

        with pytest.raises(ValueError, match="missing required fields"):
            record_arc_completion(campaign_state, incomplete_arc)

    def test_record_arc_completion_updates_timestamp(self):
        """Test recording arc completion adds timestamp."""
        campaign_state = {'campaign_id': 'camp-001'}
        completed_arc = {
            'arc_id': 'arc-1',
            'arc_name': 'First Arc',
            'encounters_in_arc': 10
        }

        record_arc_completion(campaign_state, completed_arc)

        assert 'updated_at' in campaign_state
        assert isinstance(campaign_state['updated_at'], str)

    def test_record_arc_completion_appends(self):
        """Test recording multiple arc completions appends to list."""
        campaign_state = {'campaign_id': 'camp-001'}

        arc1 = {'arc_id': 'arc-1', 'arc_name': 'Arc 1', 'encounters_in_arc': 10}
        arc2 = {'arc_id': 'arc-2', 'arc_name': 'Arc 2', 'encounters_in_arc': 12}

        record_arc_completion(campaign_state, arc1)
        record_arc_completion(campaign_state, arc2)

        assert len(campaign_state['completed_arcs']) == 2
        assert campaign_state['completed_arcs'][0]['arc_id'] == 'arc-1'
        assert campaign_state['completed_arcs'][1]['arc_id'] == 'arc-2'


# ============================================================================
# Integration Tests
# ============================================================================

class TestCampaignIntegration:
    """Integration tests combining multiple modules."""

    @pytest.fixture
    def temp_campaign_dir(self):
        """Create a temporary campaign directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_campaign_load_validate_save_cycle(self, temp_campaign_dir):
        """Test full cycle: load campaign, validate, save."""
        manager = StateManager(temp_campaign_dir)

        # Load new session
        state = manager.load_session_state()

        # Validate state
        assert manager.validate_state(state) is True

    def test_arc_completion_flow(self, temp_campaign_dir):
        """Test arc completion detection and advancement."""
        # Setup initial state
        campaign_state = {
            'campaign_id': 'camp-001',
            'total_arcs_completed': 0
        }
        arc_state = {
            'arc_id': 'arc-1',
            'arc_name': 'First Arc',
            'parent_campaign_id': 'camp-001',
            'completed': False,
            'encounters_in_arc': 8
        }

        # Check not yet complete
        assert check_arc_completion(arc_state, completion_threshold=10) is False

        # Update encounters
        arc_state['encounters_in_arc'] = 10

        # Now should be complete
        assert check_arc_completion(arc_state, completion_threshold=10) is True

        # Record completion and advance
        record_arc_completion(campaign_state, arc_state)
        new_arc = advance_to_next_arc(campaign_state, arc_state['arc_id'])

        assert campaign_state['total_arcs_completed'] == 1
        # Arc name is Arc_N where N = total_arcs_completed + 1
        assert 'Arc_2' in new_arc['arc_name']
