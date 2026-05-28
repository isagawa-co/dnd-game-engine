# Flatten Repo Structure — Task Index

## Goal
Move  contents to repo root. Update all path references. Remove empty directories.

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-move-directories]] | BUILD | none | pending |
| 002 | [[002-build-remove-empty-dirs]] | BUILD | 001 | pending |
| 003 | [[003-build-update-claude-md]] | BUILD | 001 | pending |
| 004 | [[004-build-update-game-play-cmd]] | BUILD | 001 | pending |
| 005 | [[005-build-update-char-creation-loop]] | BUILD | 001 | pending |
| 006 | [[006-build-update-char-skill]] | BUILD | 001 | pending |
| 007 | [[007-build-update-char-contract]] | BUILD | 001 | pending |
| 008 | [[008-build-update-scene-skill]] | BUILD | 001 | pending |
| 009 | [[009-build-update-config-skill]] | BUILD | 001 | pending |
| 010 | [[010-build-update-backlog-refs]] | BUILD | 001 | pending |
| 011 | [[011-build-update-task-files]] | BUILD | 001 | pending |
| 012 | [[012-test-verify-zero-refs]] | TEST | 003-011 | pending |

## Gate Contract
→ [[gate-contract.md]]

## Deliverables
- Flat repo structure with campaigns/, content/, contracts/, tasks/ at root
- Zero references to projects/ai-dnd-game in any .md or .json file
- projects/ and _test/ directories removed
