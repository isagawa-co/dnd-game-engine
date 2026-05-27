# Build Content SKILL.md

## Context
Create the content skill definition documenting 3-tier architecture, wiki-link resolution, and content contracts.

## Type
BUILD

## Execution
inline

## Dependencies
- 001-007

## Phase Gate
- [ ] All 6 contract schemas exist in `projects/ai-dnd-game/.claude/skills/content/contracts/`
- [ ] `projects/ai-dnd-game/.claude/skills/content/catalog.json` exists

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/content/SKILL.md`
- Document 3-tier loading architecture, wiki-link resolution, contracts, error handling
- Follow style of `projects/ai-dnd-game/.claude/skills/state/SKILL.md`

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/content/SKILL.md` exists
- [ ] References 3-tier architecture and wiki-link format

## Gates Satisfied
- BUILD-08

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
