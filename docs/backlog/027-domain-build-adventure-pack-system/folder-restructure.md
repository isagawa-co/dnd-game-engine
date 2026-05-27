# Folder Restructure — content/ to adventures/

## Status
NEW

## Location
`workspace` — root-level rename + all references

## What It Does
Rename `content/` to `adventures/` and restructure the folder to include a `scenes/` directory per adventure. Update all references across contracts, skills, campaign files, and manifests.

## Changes Required

### Rename
- `content/` → `adventures/`
- `content/lost-mine-phandelver/` → `adventures/lmop/`
- `content/all-classes.json` → `adventures/all-classes.json` (shared registry, stays at root)
- `content/all-races.json` → `adventures/all-races.json` (shared registry, stays at root)

### New Directory
- `adventures/lmop/scenes/` — empty, populated by lmop-adventure-build

### References to Update
- `campaigns/campaign-2026-05-27-002/campaign.json` — `content_pack` field
- `.claude/skills/character-creation-loop/character-creation-loop.md` — registry paths
- `.claude/skills/scene/SKILL.md` — content references
- `contracts/` — any content pack references
- `CLAUDE.md` — documentation references
- Any other file referencing `content/`

## Dependencies
- None — this is the first task, everything else depends on it
