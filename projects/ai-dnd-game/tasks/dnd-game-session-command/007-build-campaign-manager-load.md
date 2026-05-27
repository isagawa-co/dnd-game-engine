# Task 007: Build Campaign Manager — Load Campaign

## Action
Write load_campaign() function in `.claude/skills/game-session/campaign_manager.py`

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Campaign Load Contract

## Deliverable
Add load_campaign() function that:
- Accepts campaign_id
- Validates campaign exists (folder and files)
- Loads campaign.json and campaign_state.json
- Validates state integrity and version compatibility
- Returns outcome dict matching load-campaign-contract.json output schema
- Returns not_found if campaign doesn't exist
- Returns state_corrupted if state file invalid

## Acceptance Criteria
- [ ] load_campaign() function exists in campaign_manager.py
- [ ] Validates campaign_id maps to existing folder (LOAD-001)
- [ ] Validates state file is valid JSON (LOAD-002)
- [ ] Validates version compatibility (LOAD-003)
- [ ] Returns correct result_code for each case
- [ ] Returns party_summary array
