"""Unit tests for atomic operations module - D&D mechanics."""

import pytest
import sys
from pathlib import Path

# For pytest to find the atomic_ops module, add the skills directory to path
_skills_dir = Path(__file__).parent.parent
if str(_skills_dir) not in sys.path:
    sys.path.insert(0, str(_skills_dir))

# Now we can import from atomic_ops
from roll_operations import validate_roll, apply_advantage, apply_disadvantage
from check_operations import ability_check, saving_throw, attack_roll
from damage_operations import calculate_damage, apply_resistance, apply_immunity, cap_hp_change
from effect_operations import apply_condition, apply_effect, validate_effect, check_concentration_conflict
from state_validation import validate_hp, validate_spell_slots, validate_conditions, enforce_immutability


# ============================================================================
# ROLL OPERATIONS TESTS
# ============================================================================

class TestRollOperations:
    """Test roll validation and advantage/disadvantage mechanics."""

    def test_validate_roll_valid(self):
        """Test valid roll values [1-20]."""
        assert validate_roll(1) is True
        assert validate_roll(10) is True
        assert validate_roll(20) is True

    def test_validate_roll_invalid(self):
        """Test invalid roll values."""
        assert validate_roll(0) is False
        assert validate_roll(21) is False
        assert validate_roll(-5) is False

    def test_validate_roll_non_integer(self):
        """Test non-integer roll values."""
        assert validate_roll(10.5) is False
        assert validate_roll("10") is False

    def test_apply_advantage(self):
        """Test advantage: select higher roll."""
        assert apply_advantage(10, 15) == 15
        assert apply_advantage(20, 5) == 20
        assert apply_advantage(12, 12) == 12

    def test_apply_advantage_invalid(self):
        """Test advantage with invalid rolls."""
        with pytest.raises(ValueError):
            apply_advantage(25, 10)  # Invalid first roll
        with pytest.raises(ValueError):
            apply_advantage(10, 0)   # Invalid second roll

    def test_apply_disadvantage(self):
        """Test disadvantage: select lower roll."""
        assert apply_disadvantage(10, 15) == 10
        assert apply_disadvantage(20, 5) == 5
        assert apply_disadvantage(12, 12) == 12

    def test_apply_disadvantage_invalid(self):
        """Test disadvantage with invalid rolls."""
        with pytest.raises(ValueError):
            apply_disadvantage(21, 10)


# ============================================================================
# CHECK OPERATIONS TESTS
# ============================================================================

class TestCheckOperations:
    """Test ability checks, saving throws, and attack rolls."""

    def test_ability_check_success(self):
        """Test ability check that succeeds."""
        result = ability_check(15, 3, 10)
        assert result['total'] == 18
        assert result['success'] is True

    def test_ability_check_failure(self):
        """Test ability check that fails."""
        result = ability_check(5, 1, 15)
        assert result['total'] == 6
        assert result['success'] is False

    def test_ability_check_at_dc(self):
        """Test ability check exactly at DC."""
        result = ability_check(12, 3, 15)
        assert result['total'] == 15
        assert result['success'] is True

    def test_saving_throw_success(self):
        """Test saving throw that succeeds."""
        result = saving_throw(18, 4, 12)
        assert result['total'] == 22
        assert result['success'] is True

    def test_saving_throw_failure(self):
        """Test saving throw that fails."""
        result = saving_throw(8, 2, 14)
        assert result['total'] == 10
        assert result['success'] is False

    def test_attack_roll_hit(self):
        """Test attack roll that hits."""
        result = attack_roll(12, 5, 15)
        assert result['total'] == 17
        assert result['hit'] is True

    def test_attack_roll_miss(self):
        """Test attack roll that misses."""
        result = attack_roll(8, 2, 14)
        assert result['total'] == 10
        assert result['hit'] is False


# ============================================================================
# DAMAGE OPERATIONS TESTS
# ============================================================================

class TestDamageOperations:
    """Test damage calculation and resistance/immunity."""

    def test_calculate_damage(self):
        """Test basic damage calculation."""
        damage = calculate_damage(6, "slashing", [2, 1])
        assert damage == 9  # 6 + 2 + 1

    def test_calculate_damage_no_modifiers(self):
        """Test damage calculation without modifiers."""
        damage = calculate_damage(8, "piercing", [])
        assert damage == 8

    def test_apply_resistance(self):
        """Test damage resistance (halved, rounded down)."""
        assert apply_resistance(10, "fire") == 5
        assert apply_resistance(11, "cold") == 5
        assert apply_resistance(1, "acid") == 0

    def test_apply_immunity(self):
        """Test damage immunity (negates all)."""
        assert apply_immunity(100, "poison") == 0
        assert apply_immunity(5, "necrotic") == 0

    def test_cap_hp_change_valid(self):
        """Test capping HP within bounds."""
        # HP within valid range
        assert cap_hp_change(50, -10, 100) == 40
        assert cap_hp_change(10, 5, 50) == 15

    def test_cap_hp_change_below_zero(self):
        """Test capping HP below zero."""
        assert cap_hp_change(10, -20, 50) == 0

    def test_cap_hp_change_above_max(self):
        """Test capping HP above maximum."""
        assert cap_hp_change(80, 30, 100) == 100

    def test_cap_hp_change_exact_bounds(self):
        """Test exact boundary conditions."""
        assert cap_hp_change(0, 0, 100) == 0
        assert cap_hp_change(100, 0, 100) == 100


# ============================================================================
# EFFECT OPERATIONS TESTS
# ============================================================================

class TestEffectOperations:
    """Test effect and condition application."""

    def test_apply_condition(self):
        """Test applying a condition to target state."""
        state = {}
        result = apply_condition("BLINDED", state)
        assert result["BLINDED"] is True

    def test_apply_condition_invalid_state(self):
        """Test applying condition to invalid state."""
        with pytest.raises(ValueError):
            apply_condition("BLINDED", "not_a_dict")

    def test_apply_effect(self):
        """Test applying an effect with metadata."""
        state = {}
        result = apply_effect("fireball", state, {"duration": 3, "damage": 8})
        assert "effects" in result
        assert "fireball" in result["effects"]
        assert result["effects"]["fireball"]["duration"] == 3

    def test_validate_effect_valid(self):
        """Test effect validation."""
        assert validate_effect("haste") is True
        assert validate_effect("web", {"concentration": True}) is True

    def test_validate_effect_invalid_name(self):
        """Test effect validation with invalid name."""
        with pytest.raises(ValueError):
            validate_effect("")

    def test_check_concentration_conflict_no_conflict(self):
        """Test no concentration conflict."""
        state = {
            "effects": {
                "haste": {"active": True, "concentration": True},
                "shield": {"active": True, "concentration": False}
            }
        }
        assert check_concentration_conflict(state) is False

    def test_check_concentration_conflict_with_conflict(self):
        """Test concentration conflict detection."""
        state = {
            "effects": {
                "haste": {"active": True, "concentration": True},
                "fly": {"active": True, "concentration": True}
            }
        }
        assert check_concentration_conflict(state) is True

    def test_check_concentration_conflict_empty_state(self):
        """Test concentration check on empty state."""
        assert check_concentration_conflict({}) is False


# ============================================================================
# STATE VALIDATION TESTS
# ============================================================================

class TestStateValidation:
    """Test character state validation and immutability."""

    def test_validate_hp_valid(self):
        """Test valid HP values."""
        assert validate_hp(50, 100) is True
        assert validate_hp(0, 100) is True
        assert validate_hp(100, 100) is True

    def test_validate_hp_invalid(self):
        """Test invalid HP values."""
        assert validate_hp(-1, 100) is False
        assert validate_hp(101, 100) is False
        assert validate_hp(150, 100) is False

    def test_validate_hp_invalid_type(self):
        """Test HP validation with invalid types."""
        with pytest.raises(ValueError):
            validate_hp("50", 100)
        with pytest.raises(ValueError):
            validate_hp(50, "100")

    def test_validate_spell_slots_valid(self):
        """Test valid spell slot values."""
        assert validate_spell_slots(3, 5) is True
        assert validate_spell_slots(0, 5) is True
        assert validate_spell_slots(5, 5) is True

    def test_validate_spell_slots_invalid(self):
        """Test invalid spell slot values."""
        assert validate_spell_slots(-1, 5) is False
        assert validate_spell_slots(6, 5) is False

    def test_validate_conditions_valid(self):
        """Test valid conditions."""
        conditions = {
            "BLINDED": {"duration": 3},
            "POISONED": {"duration": 0},
            "STUNNED": 2
        }
        assert validate_conditions(conditions) is True

    def test_validate_conditions_negative_duration(self):
        """Test conditions with negative duration."""
        conditions = {"POISONED": {"duration": -1}}
        assert validate_conditions(conditions) is False

    def test_validate_conditions_invalid_type(self):
        """Test conditions validation with invalid type."""
        with pytest.raises(ValueError):
            validate_conditions("not_a_dict")

    def test_enforce_immutability(self):
        """Test immutability enforcement."""
        state = {"hp": 50, "max_hp": 100, "level": 5}
        immutable = enforce_immutability(state)
        assert isinstance(immutable, frozenset)
        # Verify all items are present
        assert ("hp", 50) in immutable
        assert ("max_hp", 100) in immutable

    def test_enforce_immutability_invalid_input(self):
        """Test immutability enforcement with invalid input."""
        with pytest.raises(ValueError):
            enforce_immutability([1, 2, 3])


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple operations."""

    def test_full_ability_check_workflow(self):
        """Test a complete ability check scenario."""
        roll = 14
        modifier = 3
        dc = 12

        # Validate roll is legal
        assert validate_roll(roll)

        # Execute ability check
        result = ability_check(roll, modifier, dc)

        # Verify result structure
        assert isinstance(result, dict)
        assert "total" in result
        assert "success" in result
        assert result["total"] == 17
        assert result["success"] is True

    def test_combat_round_workflow(self):
        """Test a typical combat round scenario."""
        # Character with AC 15, HP 50
        target_ac = 15
        target_hp = 50
        target_max_hp = 50

        # Attacker rolls and adds modifier
        attack_roll_result = attack_roll(12, 4, target_ac)
        assert attack_roll_result["hit"] is True

        # Calculate damage and apply
        damage = calculate_damage(6, "slashing", [2])
        new_hp = cap_hp_change(target_hp, -damage, target_max_hp)
        assert new_hp == 42

        # Verify HP is still valid
        assert validate_hp(new_hp, target_max_hp)

    def test_effect_concentration_workflow(self):
        """Test applying concentration effect."""
        state = {}

        # Apply a concentration effect
        state = apply_effect("haste", state, {"duration": 10, "concentration": True})
        assert validate_effect("haste", {"concentration": True})
        assert check_concentration_conflict(state) is False

        # Try to apply another concentration effect
        state = apply_effect("fly", state, {"duration": 5, "concentration": True})
        assert check_concentration_conflict(state) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
