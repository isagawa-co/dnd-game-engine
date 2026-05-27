# Task 012: Test Campaign Creation

## Action
Write `tests/test_game_session_create.py`

## Source
Task 006 (campaign_manager.py create_campaign)

## Deliverable
Test file with:
- test_create_campaign_success: Valid inputs produce campaign_created result
- test_create_campaign_party_count_invalid: party_count outside 3-6 returns validation_failed
- test_create_campaign_level_invalid: starting_level outside 1-20 returns validation_failed
- test_create_campaign_files_created: campaign.json and campaign_state.json exist after creation
- test_create_campaign_state_initialized: Initial state has phase session_0, arc_number 1

## Acceptance Criteria
- [ ] File exists at `tests/test_game_session_create.py`
- [ ] 5 test functions present
- [ ] Tests validate success and failure paths
- [ ] Tests verify file creation
- [ ] Tests verify initial state values
