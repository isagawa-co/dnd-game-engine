# Task 001: Build UI Rendering SKILL.md

## Action
Create `.claude/skills/ui-rendering/SKILL.md` — the skill identity and reference file for the UI rendering module.

## Deliverable
`.claude/skills/ui-rendering/SKILL.md`

## Acceptance Criteria
- [ ] File exists at correct path
- [ ] Contains Identity table (skill name, purpose, type)
- [ ] Contains Renderers table (4 renderers: character_sheet, combat_round, encounter, inventory)
- [ ] Contains Contracts table linking to contract JSON files
- [ ] Contains Implementation table linking to Python source files
- [ ] Contains Rules section (width limit, unicode box drawing, no game logic)
- [ ] Follows tiered indexing pattern (parent file = index, points to contracts/implementations)

## Dependencies
None — first task

## Gate
SKILL-001: `file_exists: .claude/skills/ui-rendering/SKILL.md`
