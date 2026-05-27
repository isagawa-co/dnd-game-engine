# Task 004: Build Resume Session Contract

## Action
Write `.claude/skills/game-session/contracts/resume-session-contract.json`

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Session Resume Contract section

## Deliverable
JSON contract file with:
- Input schema: campaign_id (string)
- Output schema: success (bool), result_code (session_resumed|state_corrupted|checkpoint_missing), campaign_id, resumed_from_checkpoint, party_status, time_elapsed_since_save, narrative
- Validation rules: RESUME-001 (campaign exists), RESUME-002 (checkpoint file valid), RESUME-003 (party state recoverable)

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/contracts/resume-session-contract.json`
- [ ] Valid JSON with $schema, input_schema, output_schema, validation_rules sections
- [ ] Input schema matches session-contract.md Session Resume Contract
- [ ] Output schema matches session-contract.md Session Resume Outcome Contract
- [ ] All 3 validation rules present (RESUME-001, RESUME-002, RESUME-003)
- [ ] File validates as JSON (no syntax errors)
