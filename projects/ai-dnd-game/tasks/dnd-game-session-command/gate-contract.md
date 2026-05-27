# Gate Contract — Game Session Command

## Gate Requirements

| Gate ID | Requirement | Verification |
|---------|-------------|--------------|
| SESSION-GATE-001 | 4 contract JSON files exist and validate | `python -c "import json; [json.load(open(f)) for f in ['create-campaign-contract.json', 'load-campaign-contract.json', 'save-session-contract.json', 'resume-session-contract.json']]"` |
| SESSION-GATE-002 | SKILL.md exists with all sections | File exists, contains Identity, Vocabulary, Contracts, Dependencies, Actions, Result Codes |
| SESSION-GATE-003 | campaign_manager.py has create_campaign and load_campaign | `python -c "from campaign_manager import create_campaign, load_campaign"` |
| SESSION-GATE-004 | session_persistence.py has save_session and resume_session | `python -c "from session_persistence import save_session, resume_session"` |
| SESSION-GATE-005 | checkpoint_manager.py has all 5 functions | `python -c "from checkpoint_manager import create_checkpoint, list_checkpoints, load_checkpoint, prune_checkpoints, verify_checkpoint"` |
| SESSION-GATE-006 | session_validator.py has all 6 validation functions | `python -c "from session_validator import validate_campaign_id, validate_party_count, validate_state_file, validate_file_integrity, validate_version_compatibility, validate_checkpoint_count"` |
| SESSION-GATE-007 | All tests pass | `pytest tests/test_game_session*.py -v` |

## Pass Criteria
All 7 gates must pass. No partial credit.
