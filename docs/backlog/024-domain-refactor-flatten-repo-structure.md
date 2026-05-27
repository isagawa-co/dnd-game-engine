# Flatten Repo Structure — Remove projects/ai-dnd-game Nesting

## Status
Open

## Priority
High — This repo IS the D&D game engine. The `projects/ai-dnd-game/` nesting implies it's a sub-project inside a larger workspace. Every path reference is wrong.

## Summary
Eliminate the `projects/ai-dnd-game/` directory by moving its contents to repo root. This repo is the standalone golden master D&D game engine — not a parent of multiple projects. All path references across skills, commands, contracts, lessons, and CLAUDE.md must be updated. The `_test/` directory should also be removed (empty, unused). Tasks should live at repo root as `tasks/`.

## Current Structure (Wrong)
```
dnd-game-engine-test/
├── projects/
│   └── ai-dnd-game/
│       ├── campaigns/
│       ├── content/
│       ├── contracts/
│       ├── config/          (referenced but may not exist yet)
│       └── tasks/
├── _test/                   (empty, remove)
└── docs/
```

## Target Structure (Correct)
```
dnd-game-engine-test/
├── campaigns/
├── content/
├── contracts/
├── config/
├── tasks/
├── docs/
└── .claude/
```

## Design Documents

| Document | Purpose |
|----------|---------|
| [[024-domain-refactor-flatten-repo-structure/directory-moves]] | Exact move operations for each directory |
| [[024-domain-refactor-flatten-repo-structure/path-reference-updates]] | All files containing `projects/ai-dnd-game` that need updating |
| [[024-domain-refactor-flatten-repo-structure/validation]] | How to verify no broken references remain |

## Requirements
- Move `projects/ai-dnd-game/campaigns/` to `campaigns/`
- Move `projects/ai-dnd-game/content/` to `content/`
- Move `projects/ai-dnd-game/contracts/` to `contracts/`
- Move `projects/ai-dnd-game/config/` to `config/` (create if doesn't exist)
- Move `projects/ai-dnd-game/tasks/` to `tasks/`
- Remove `projects/` directory entirely after moves
- Remove `_test/` directory (empty)
- Update ~176 files referencing `projects/ai-dnd-game` paths
- Update CLAUDE.md directory references
- Update all skill .md files with corrected paths
- Update all command .md files with corrected paths
- Update all contract .json files with corrected paths
- Grep verify: zero remaining `projects/ai-dnd-game` references after completion

## References
- Audit identified 176 files with `projects/ai-dnd-game` references
- Key files: CLAUDE.md, game-play.md, character-creation-loop.md, character SKILL.md, character-creation-contract.json, scene SKILL.md, configuration SKILL.md

## Task Builder Input
- **Deliverable:** Flattened repo structure with all paths updated and verified
- **Location:** workspace
- **Scope:** REFACTOR
- **Constraints:** Must be done before character modularization (025). Git history will show the move. All skills/commands must work after restructuring.
