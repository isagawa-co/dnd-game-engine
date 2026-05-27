# Task 013: Test Campaign Load

## Action
Write `tests/test_game_session_load.py`

## Source
Task 007 (campaign_manager.py load_campaign)

## Deliverable
Test file with:
- test_load_campaign_success: Existing campaign returns campaign_loaded
- test_load_campaign_not_found: Non-existent campaign returns not_found
- test_load_campaign_corrupted: Invalid state file returns state_corrupted
- test_load_campaign_party_summary: Party summary array populated correctly
- test_load_campaign_metadata: Campaign metadata fields present and correct

## Acceptance Criteria
- [ ] File exists at `tests/test_game_session_load.py`
- [ ] 5 test functions present
- [ ] Tests validate success, not_found, and corrupted paths
- [ ] Tests verify party summary
- [ ] Tests verify metadata
