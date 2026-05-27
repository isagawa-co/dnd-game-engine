# Task 003: Build Save Session Contract

## Action
Write `.claude/skills/game-session/contracts/save-session-contract.json`

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Session Save Contract section

## Deliverable
JSON contract file with:
- Input schema: campaign_id (string), campaign_state (object with phase, arc, party, npcs, loot_collected, time_elapsed_hours, timestamp)
- Output schema: success (bool), result_code (session_saved|save_failed|state_invalid), campaign_id, save_file, backup_files, save_metadata, narrative
- Validation rules: SAVE-001 (state valid JSON), SAVE-002 (atomic write with rename), SAVE-003 (checksum verified post-write), SAVE-004 (keep 3 most recent checkpoints)

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/contracts/save-session-contract.json`
- [ ] Valid JSON with $schema, input_schema, output_schema, validation_rules sections
- [ ] Input schema matches session-contract.md Session Save Contract
- [ ] Output schema matches session-contract.md Session Save Outcome Contract
- [ ] All 4 validation rules present (SAVE-001 through SAVE-004)
- [ ] File validates as JSON (no syntax errors)
