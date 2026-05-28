# Task 006: Build ui_rendering __init__.py

## Action
Create `src/ui_rendering/__init__.py` — package init that exports all 4 render functions.

## Deliverable
`src/ui_rendering/__init__.py`

## Acceptance Criteria
- [ ] File exists at correct path
- [ ] Exports: render_character_sheet, render_combat_round, render_encounter, render_inventory
- [ ] Imports from sibling modules

## Dependencies
007, 008, 009, 010 (implementations must exist)

## Gate
IMPL-001: `grep: "render_character_sheet" src/ui_rendering/__init__.py`
