# Task 001: Build Create Campaign Contract

## Action
Write `.claude/skills/game-session/contracts/create-campaign-contract.json`

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Campaign Creation Contract section

## Deliverable
JSON contract file with:
- Input schema: campaign_name (string), content_pack (string), party_count (int 3-6), starting_level (int 1-20), campaign_metadata (object), party_pcs (array of PC objects)
- Output schema: success (bool), result_code (campaign_created|validation_failed), campaign_id, campaign_file, state_file, party_count, starting_level, state_mutations, narrative
- Validation rules: SESSION-001 (party_count 3-6), SESSION-002 (content_pack exists), SESSION-003 (starting_level 1-20)

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/contracts/create-campaign-contract.json`
- [ ] Valid JSON with $schema, input_schema, output_schema, validation_rules sections
- [ ] Input schema matches session-contract.md Campaign Creation Contract
- [ ] Output schema matches session-contract.md Campaign Creation Outcome Contract
- [ ] All 3 validation rules present (SESSION-001, SESSION-002, SESSION-003)
- [ ] File validates as JSON (no syntax errors)
