# Task 008: Build Session Persistence — Save Session

## Action
Write `.claude/skills/game-session/session_persistence.py` — save_session function

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Session Save Contract

## Deliverable
Python module with save_session() function that:
- Accepts campaign_id, campaign_state
- Validates state is valid JSON (SAVE-001)
- Uses atomic write pattern: write to temp file, rename to target (SAVE-002)
- Verifies SHA256 checksum after write (SAVE-003)
- Keeps 3 most recent checkpoints, deletes oldest (SAVE-004)
- Creates checkpoint file in campaigns/{campaign_id}/checkpoints/
- Returns outcome dict matching save-session-contract.json output schema

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/session_persistence.py`
- [ ] save_session() function accepts campaign_id and campaign_state
- [ ] Uses atomic write (temp file + rename) pattern
- [ ] Verifies checksum post-write
- [ ] Maintains max 3 checkpoints
- [ ] Returns outcome dict matching contract output schema
