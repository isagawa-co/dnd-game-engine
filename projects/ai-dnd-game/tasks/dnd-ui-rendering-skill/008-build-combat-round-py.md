# Task 008: Build combat_round.py

## Action
Create `src/ui_rendering/combat_round.py` — implements render_combat_round() function.

## Deliverable
`projects/ai-dnd-game/src/ui_rendering/combat_round.py`

## Acceptance Criteria
- [ ] File exists at correct path
- [ ] Contains render_combat_round(display_data, round_number) function
- [ ] Renders: initiative order sorted, highlights active combatant
- [ ] Renders: round counter
- [ ] Renders: HP for each combatant
- [ ] Renders: action log (last 5 entries)
- [ ] Renders: active conditions
- [ ] Uses unicode box-drawing characters
- [ ] Output width <= 80 columns

## Dependencies
003 (contract defines the schema)

## Gate
IMPL-003: `file_exists: projects/ai-dnd-game/src/ui_rendering/combat_round.py`
