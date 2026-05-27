# Task 002: Build Character Sheet Contract

## Action
Create `contracts/character-sheet-contract.json` — JSON schema for character sheet display input/output.

## Deliverable
`projects/ai-dnd-game/.claude/skills/ui-rendering/contracts/character-sheet-contract.json`

## Acceptance Criteria
- [ ] File exists at correct path
- [ ] Valid JSON schema with input_schema and output_schema
- [ ] Input covers: name, class, level, race, hp, ac, initiative, stats, proficiencies, spell_slots, conditions, inventory
- [ ] Output specifies terminal_text format with 80-column width
- [ ] Includes validation rules and example

## Dependencies
001 (SKILL.md references this contract)

## Gate
CONTRACT-001: `file_exists: projects/ai-dnd-game/.claude/skills/ui-rendering/contracts/character-sheet-contract.json`
