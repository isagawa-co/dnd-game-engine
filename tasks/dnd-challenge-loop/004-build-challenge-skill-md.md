# Build Challenge SKILL.md

## Context
Create the SKILL.md orchestrator file for the challenge sub-loop skill.

## Type
BUILD

## Execution
inline

## Dependencies
- 001-build-challenge-action-contract
- 002-build-challenge-outcome-contract
- 003-build-challenge-resolution-py

## Requirements
- Create `.claude/skills/challenge/SKILL.md`
- Sections: Identity, Vocabulary, Contracts (links to action + outcome contracts), Resolution Flow, Integration (returns to scene loop)
- References design doc via wikilink
- Index-style: points to files, no inline implementation

## Acceptance Criteria
- [ ] `.claude/skills/challenge/SKILL.md` exists
- [ ] Contains links to both contracts
- [ ] Contains resolution flow description
- [ ] Uses wikilink tiered indexing (no inline implementation detail)

## Gates Satisfied
- BUILD-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
