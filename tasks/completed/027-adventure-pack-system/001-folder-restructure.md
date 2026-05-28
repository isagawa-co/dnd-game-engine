# Task 001: Folder Restructure

## Type
BUILD

## Goal
Rename `content/` to `adventures/`, rename `lost-mine-phandelver/` to `lmop/`, create `scenes/` directory, update all references.

## Steps
1. Rename `content/` → `adventures/`
2. Rename `adventures/lost-mine-phandelver/` → `adventures/lmop/`
3. Create `adventures/lmop/scenes/` directory
4. Update all file references from `content/` to `adventures/`
5. Update campaign.json `content_pack` → `adventure_id: "lmop"`

## Files to Update
- `campaigns/campaign-2026-05-27-002/campaign.json`
- `.claude/skills/character-creation-loop/character-creation-loop.md`
- `.claude/skills/scene/SKILL.md`
- `CLAUDE.md`
- Any contracts referencing content/

## Verification
- `adventures/lmop/manifest.json` exists
- `adventures/lmop/monsters/goblin.json` exists
- `content/` directory no longer exists
- No remaining references to `content/` in skills or contracts
