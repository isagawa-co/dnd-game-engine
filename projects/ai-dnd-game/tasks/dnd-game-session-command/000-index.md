# D&D Game Session Command — Task Index

## Goal
Build the game-session command that manages campaign lifecycle: create, load, save, resume. Entry point for all gameplay.

## Source
-> [[docs/backlog/019-dnd-build-game-session-command.md]]
-> [[docs/backlog/019-dnd-build-game-session-command/session-contract.md]]

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-create-campaign-contract]] | BUILD | none | pending |
| 002 | [[002-build-load-campaign-contract]] | BUILD | none | pending |
| 003 | [[003-build-save-session-contract]] | BUILD | none | pending |
| 004 | [[004-build-resume-session-contract]] | BUILD | none | pending |
| 005 | [[005-build-game-session-skill-md]] | BUILD | 001-004 | pending |
| 006 | [[006-build-campaign-manager-create]] | BUILD | 001, 005 | pending |
| 007 | [[007-build-campaign-manager-load]] | BUILD | 002, 005 | pending |
| 008 | [[008-build-session-persistence-save]] | BUILD | 003, 005 | pending |
| 009 | [[009-build-session-persistence-resume]] | BUILD | 004, 005 | pending |
| 010 | [[010-build-checkpoint-manager]] | BUILD | 008 | pending |
| 011 | [[011-build-session-validator]] | BUILD | 006-010 | pending |
| 012 | [[012-test-campaign-create]] | TEST | 006 | pending |
| 013 | [[013-test-campaign-load]] | TEST | 007 | pending |
| 014 | [[014-test-session-save-resume]] | TEST | 008-010 | pending |
| 015 | [[015-test-validate-all]] | TEST | 011-014 | pending |

## Gate Contract
-> [[gate-contract.md]]

## Deliverables
- `projects/ai-dnd-game/.claude/skills/game-session/contracts/` — 4 JSON contracts
- `projects/ai-dnd-game/.claude/skills/game-session/SKILL.md` — game-session skill definition
- `projects/ai-dnd-game/.claude/skills/game-session/` — Python modules
- `projects/ai-dnd-game/tests/test_game_session.py` — comprehensive tests
