# Task 015: Test Validate All — Integration

## Action
Write `tests/test_game_session_integration.py`

## Source
All game-session tasks (001-014)

## Deliverable
Integration test file with:
- test_full_campaign_lifecycle: Create -> Save -> Resume -> Load full cycle
- test_campaign_recovery: Create -> Save -> Corrupt -> Detect -> Rollback to checkpoint
- test_validator_all_rules: All 6 validation rules enforced correctly
- test_checkpoint_lifecycle: Create 5 checkpoints, verify only 3 remain
- test_concurrent_save_guard: Verify atomic write prevents partial state

## Acceptance Criteria
- [ ] File exists at `tests/test_game_session_integration.py`
- [ ] 5 integration test functions present
- [ ] Full lifecycle test covers create -> save -> resume -> load
- [ ] Recovery test verifies rollback to checkpoint
- [ ] All validators tested
- [ ] Checkpoint pruning verified
