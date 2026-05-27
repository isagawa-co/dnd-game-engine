# Task 007: Build character_sheet.py

## Action
Create `src/ui_rendering/character_sheet.py` — implements render_character_sheet() function.

## Deliverable
`projects/ai-dnd-game/src/ui_rendering/character_sheet.py`

## Acceptance Criteria
- [ ] File exists at correct path
- [ ] Contains render_character_sheet(display_data) function
- [ ] Renders: name, class, level, race, HP, AC, initiative
- [ ] Renders: ability scores with modifiers
- [ ] Renders: proficiencies (skills, saving throws)
- [ ] Renders: spell slots per level
- [ ] Renders: conditions list
- [ ] Renders: inventory with weight
- [ ] Uses unicode box-drawing characters
- [ ] Output width <= 80 columns

## Dependencies
002 (contract defines the schema)

## Gate
IMPL-002: `file_exists: projects/ai-dnd-game/src/ui_rendering/character_sheet.py`
