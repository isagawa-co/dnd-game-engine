# Task 009: Build Session Persistence — Resume Session

## Action
Write resume_session() function in `.claude/skills/game-session/session_persistence.py`

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Session Resume Contract

## Deliverable
Add resume_session() function that:
- Accepts campaign_id
- Validates campaign exists (RESUME-001)
- Loads most recent checkpoint (RESUME-002)
- Validates party state is recoverable (RESUME-003)
- Returns party_status with location, party_pcs, enemies_in_scene
- Calculates time_elapsed_since_save
- Returns outcome dict matching resume-session-contract.json output schema

## Acceptance Criteria
- [ ] resume_session() function exists in session_persistence.py
- [ ] Validates campaign exists (RESUME-001)
- [ ] Loads most recent valid checkpoint (RESUME-002)
- [ ] Validates party state recoverable (RESUME-003)
- [ ] Returns party_status object
- [ ] Returns correct result_code for each case
