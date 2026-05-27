# Task 011: Build test_ui_rendering.py

## Action
Create `tests/test_ui_rendering.py` — test suite for all 4 render functions.

## Deliverable
`tests/test_ui_rendering.py`

## Acceptance Criteria
- [ ] File exists at correct path
- [ ] 5+ tests that all pass
- [ ] Tests render_character_sheet with sample PC data
- [ ] Tests render_combat_round with sample initiative and action log
- [ ] Tests render_encounter with sample location and enemies
- [ ] Tests render_inventory with sample items
- [ ] Verifies output is string type
- [ ] Verifies output contains expected content (character name, round number, location, item names)
- [ ] Verifies output width <= 80 columns per line

## Dependencies
006-010 (implementations must exist)

## Gate
TEST-001: `run_test: python -m pytest tests/test_ui_rendering.py -v`
