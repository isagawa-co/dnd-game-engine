# Task 007 — Test Narration Skill

## Action
Write `projects/ai-dnd-game/tests/test_narration_skill.py`

## Acceptance Criteria
- File exists at specified path
- L1 tests: Verify all skill files exist (SKILL.md, 2 contracts, 3 references)
- L2 tests: Verify contracts are valid JSON, request contract has 6 narration types, output contract has required fields
- L3 tests: Verify prompt templates cover all 6 narration types, fallback templates have variants for each type
- At least 5 test functions
- All tests pass with `python -m pytest projects/ai-dnd-game/tests/test_narration_skill.py -v`

## Gate
TEST-001, TEST-002, TEST-003
