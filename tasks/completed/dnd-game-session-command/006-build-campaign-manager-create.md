# Task 006: Build Campaign Manager — Create Campaign

## Action
Write `.claude/skills/game-session/campaign_manager.py` — create_campaign function

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Campaign Creation Contract

## Deliverable
Python module with create_campaign() function that:
- Accepts campaign_name, content_pack, party_count, starting_level, campaign_metadata, party_pcs
- Validates party_count (3-6), starting_level (1-20), content_pack exists
- Creates campaign directory structure: campaigns/{campaign_id}/
- Writes campaign.json (metadata) and campaign_state.json (initial state)
- Returns outcome dict matching create-campaign-contract.json output schema

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/campaign_manager.py`
- [ ] create_campaign() function accepts all input schema fields
- [ ] Validates party_count 3-6 (SESSION-001)
- [ ] Validates content_pack exists (SESSION-002)
- [ ] Validates starting_level 1-20 (SESSION-003)
- [ ] Creates campaign directory and files
- [ ] Returns outcome dict matching contract output schema
