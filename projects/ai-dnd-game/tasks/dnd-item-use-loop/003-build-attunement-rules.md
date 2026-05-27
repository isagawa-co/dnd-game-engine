# Build Attunement Rules

## Context
Create the attunement-rules.json — defines D&D 5e attunement constraints for magical items.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/item-use/contracts/attunement-rules.json`
- Max 3 attuned items per PC
- Attunement takes 1 hour of rest/meditation
- Attunement breaks if PC leaves item for 24 hours
- Attunement is PC-specific (can't share)
- Include validation rules with rule IDs (ATT-001 through ATT-004)

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/item-use/contracts/attunement-rules.json` exists
- [ ] File is valid JSON
- [ ] Contains 4 attunement rules with rule IDs
- [ ] Max slots, duration, break condition, and PC-specificity defined

## Gates Satisfied
- BUILD-03, FUNC-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
