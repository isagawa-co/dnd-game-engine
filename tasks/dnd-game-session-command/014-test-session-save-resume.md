# Task 014: Test Session Save and Resume

## Action
Write `tests/test_game_session_save_resume.py`

## Source
Tasks 008-010 (session_persistence.py, checkpoint_manager.py)

## Deliverable
Test file with:
- test_save_session_success: Valid state saves with session_saved result
- test_save_session_atomic_write: Temp file + rename pattern used
- test_save_session_checksum: SHA256 checksum verified post-write
- test_save_session_checkpoint_pruning: Only 3 most recent checkpoints kept
- test_resume_session_success: Resume from latest checkpoint returns session_resumed
- test_resume_session_not_found: Non-existent campaign returns checkpoint_missing
- test_resume_session_party_status: Party status correctly populated

## Acceptance Criteria
- [ ] File exists at `tests/test_game_session_save_resume.py`
- [ ] 7 test functions present
- [ ] Tests validate save success, atomicity, checksum, pruning
- [ ] Tests validate resume success and failure paths
- [ ] Tests verify party status on resume
