# Clean Non-D&D Content From Repo

## Status
Done

## Priority
High — This is the golden master D&D game engine. Non-D&D artifacts confuse scope and pollute the repo.

## Summary
Remove all content that doesn't belong in a standalone D&D 5e game engine repo. This includes the website-cloner skill, stale football/NFL attestations, duplicate skill directories, and any other non-D&D artifacts. The GDD reference (Tiny Civ) is intentionally kept — it's a calibration example for the game-engine design tool, not D&D content contamination.

## Requirements

### Remove Entirely
- `.claude/skills/website-cloner/` — entire directory (web cloning, not game-related)
- `.claude/state/attestations/020-20260428T000002Z.json` — stale football project attestation
- `.claude/skills/atomic_ops/` — duplicate of `.claude/skills/atomic-ops/` (underscore vs hyphen; keep the hyphenated version)
- All `__pycache__/` directories — should be in `.gitignore`, not committed

### Keep (Intentional)
- `.claude/skills/game-engine/references/gdd-reference/` — Tiny Civ is a GDD calibration example (multi-genre design tool)
- Python files in `.claude/hooks/`, `.claude/skills/*/tests/` — testing infrastructure per CLAUDE.md
- Lesson files mentioning NFL/football — educational cross-project pattern references

### Verify
- No remaining references to `website-cloner` in any skill or command
- No remaining references to `atomic_ops` (underscore) after removing duplicate
- `.gitignore` updated to exclude `__pycache__/`, `*.pyc`

## References
- Audit found 55 files with football/NFL/sports references (mostly in state logs — keep logs, remove attestation)
- Website-cloner: 7 files in `.claude/skills/website-cloner/`
- Duplicate atomic_ops: `.claude/skills/atomic_ops/` mirrors `.claude/skills/atomic-ops/`

## Task Builder Input
- **Deliverable:** Clean repo with only D&D game engine content
- **Location:** workspace
- **Scope:** REFACTOR
- **Constraints:** Can run in parallel with 024 (flatten). Non-destructive to any D&D content. Verify no skill references break after removals.
