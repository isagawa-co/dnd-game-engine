# Path Reference Updates

## Status
NEW

## Scope
~176 files reference `projects/ai-dnd-game`. After directory moves, every reference must be updated.

## Primary Files (Critical — Break Gameplay If Wrong)

| File | Reference Count | What Changes |
|------|----------------|--------------|
| `CLAUDE.md` | 3 | `projects/ai-dnd-game/contracts/` → `contracts/`, etc. |
| `.claude/commands/game-play.md` | 7 | All contract and campaign path references |
| `.claude/skills/character-creation-loop/character-creation-loop.md` | 8 | Registry paths, config paths, src paths |
| `.claude/skills/character/SKILL.md` | 4 | Module paths, test paths |
| `.claude/skills/character/contracts/character-creation-contract.json` | 2 | Registry reference paths |
| `.claude/skills/scene/SKILL.md` | 1 | Backlog reference path |
| `.claude/skills/configuration/SKILL.md` | 1 | Config directory path |
| `docs/backlog/023-game-refactor-orchestration-contract-driven.md` | 1 | Contract path |

## Secondary Files (Task definitions — internal references)

All files in `tasks/` (formerly `projects/ai-dnd-game/tasks/`) that reference paths with the old prefix. These are gate-contract.md files and task definition .md files.

## Pattern

Simple find-and-replace: `projects/ai-dnd-game/` → `` (empty string, since content is now at root).

Special cases:
- `projects/ai-dnd-game/.claude/skills/` → `.claude/skills/` (these were always wrong — skills live in `.claude/`, not under projects)
- `projects/ai-dnd-game/src/` → references to Python modules (testing infrastructure, paths may need updating to match actual location)
- `projects/ai-dnd-game/config/` → `config/`
- `projects/ai-dnd-game/content/` → `content/`
- `projects/ai-dnd-game/campaigns/` → `campaigns/`
- `projects/ai-dnd-game/contracts/` → `contracts/`

## Validation
- `grep -r "projects/ai-dnd-game" . --include="*.md" --include="*.json" | grep -v ".git/"` must return zero results
- All skill/command markdown files parse correctly
- Contract JSON files validate as valid JSON after edits
