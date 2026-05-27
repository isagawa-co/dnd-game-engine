# Task 010: Build Checkpoint Manager

## Action
Write `.claude/skills/game-session/checkpoint_manager.py`

## Source
`docs/backlog/019-dnd-build-game-session-command/session-contract.md` — Checkpoint Management section

## Deliverable
Python module with checkpoint management functions:
- create_checkpoint(): Write checkpoint file with metadata (save_time, session_number, party_location, game_hours)
- list_checkpoints(): List available checkpoints for a campaign, sorted by timestamp
- load_checkpoint(): Load specific checkpoint by filename
- prune_checkpoints(): Keep only 3 most recent, delete oldest
- verify_checkpoint(): SHA256 checksum verification

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/checkpoint_manager.py`
- [ ] create_checkpoint() writes checkpoint with metadata
- [ ] list_checkpoints() returns sorted checkpoint list
- [ ] load_checkpoint() loads specific checkpoint
- [ ] prune_checkpoints() keeps 3 most recent
- [ ] verify_checkpoint() validates SHA256 checksum
