# Task 002: Build Load Campaign Contract

## Action
Write `.claude/skills/game-session/contracts/load-campaign-contract.json`

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Campaign Load Contract section

## Deliverable
JSON contract file with:
- Input schema: campaign_id (string)
- Output schema: success (bool), result_code (campaign_loaded|state_corrupted|not_found), campaign_id, campaign_metadata, current_state, party_summary
- Validation rules: LOAD-001 (campaign_id exists), LOAD-002 (state file valid JSON), LOAD-003 (version compatible)

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/contracts/load-campaign-contract.json`
- [ ] Valid JSON with $schema, input_schema, output_schema, validation_rules sections
- [ ] Input schema matches session-contract.md Campaign Load Contract
- [ ] Output schema matches session-contract.md Campaign Load Outcome Contract
- [ ] All 3 validation rules present (LOAD-001, LOAD-002, LOAD-003)
- [ ] File validates as JSON (no syntax errors)
