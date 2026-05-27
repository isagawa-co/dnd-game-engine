# D&D Content System — Task Index

## Goal
Build the content pack system with wiki-link tiering (Tier 1-3), 6 content contracts, and Lost Mine of Phandelver as first pack.

## Source
→ [[backlog/002-dnd-build-content-system.md]]

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-monster-schema]] | BUILD | none | pending |
| 002 | [[002-build-spell-schema]] | BUILD | none | pending |
| 003 | [[003-build-item-schema]] | BUILD | none | pending |
| 004 | [[004-build-class-schema]] | BUILD | none | pending |
| 005 | [[005-build-race-schema]] | BUILD | none | pending |
| 006 | [[006-build-condition-schema]] | BUILD | none | pending |
| 007 | [[007-build-catalog-json]] | BUILD | none | pending |
| 008 | [[008-build-content-skill-md]] | BUILD | 001-007 | pending |
| 009 | [[009-build-pack-manifest]] | BUILD | 007 | pending |
| 010 | [[010-build-monsters-goblins]] | BUILD | 001, 009 | pending |
| 011 | [[011-build-monsters-humanoids]] | BUILD | 001, 009 | pending |
| 012 | [[012-build-monsters-beasts]] | BUILD | 001, 009 | pending |
| 013 | [[013-build-monsters-npcs]] | BUILD | 001, 009 | pending |
| 014 | [[014-build-monsters-undead-misc]] | BUILD | 001, 009 | pending |
| 015 | [[015-build-spells]] | BUILD | 002, 009 | pending |
| 016 | [[016-build-items-weapons]] | BUILD | 003, 009 | pending |
| 017 | [[017-build-items-armor-gear-magic]] | BUILD | 003, 009 | pending |
| 018 | [[018-test-validate-all-content]] | TEST | 001-017 | pending |

## Gate Contract
→ [[gate-contract.md]]

## Deliverables
- `.claude/skills/content/contracts/` — 6 JSON schemas
- `.claude/skills/content/catalog.json` — Tier 1 master index
- `.claude/skills/content/SKILL.md` — content skill definition
- `content/lost-mine-phandelver/` — complete pack (manifest + 45 content files)
