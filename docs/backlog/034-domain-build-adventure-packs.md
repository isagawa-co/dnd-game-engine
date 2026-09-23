# Build Adventure Packs: Dragon of Icespire Peak + Forge of Fury

## Status
Open

## Priority
High — The game loop can only follow one adventure (LMoP). A 6-PC party at Level 4 needs level-appropriate, dungeon-crawl content to continue play. Both packs must exist in the formatted `adventures/<id>/` structure the loops pick up.

## Summary
Generate two new adventure packs from training knowledge, each conforming to `contracts/adventure-scene-contract.json` and mirroring the structure of `adventures/lmop/` (manifest.json + monsters/ + scenes/chapter-N/act-*.json). Dragon of Icespire Peak (levels 1–7) continues the Phandalin/Sword Coast setting; Forge of Fury (levels 3–5) is a self-contained multi-level dungeon crawl. Both are scaled for a 6-PC party.

## Design Documents

| Document | Purpose |
|----------|---------|
| [[034-domain-build-adventure-packs/dragon-of-icespire-peak]] | DoIP pack — chapters, acts, encounters, NPCs, loot |
| [[034-domain-build-adventure-packs/forge-of-fury]] | Forge of Fury pack — 4-level dungeon crawl, encounters, loot |
| [[034-domain-build-adventure-packs/party-scaling]] | Cross-cutting: 6-PC + high-power-item scaling rules for both packs |

## Architecture

```
adventures/dragon-of-icespire-peak/
  manifest.json            ← stat block index (monsters/items/spells)
  monsters/                ← stat blocks referenced by act files
  scenes/
    chapter-1-phandalin-hub/act-I.json
    chapter-2-starting-quests/act-{I,II,III}.json
    chapter-3-followup-quests/act-{I,II,III}.json
    chapter-4-advanced-quests/act-{I,II,III}.json
    chapter-5-icespire-hold/act-I.json
adventures/forge-of-fury/
  manifest.json
  monsters/
  scenes/
    chapter-1-mountain-door/act-{I,II}.json
    chapter-2-glitterhame/act-{I,II}.json
    chapter-3-the-foundry/act-{I,II}.json
    chapter-4-black-lake/act-I.json
```

## Requirements
- Every act file conforms to `contracts/adventure-scene-contract.json` (act_id, chapter, act, title, read_aloud, encounters, npcs, loot, skill_checks, transitions, dm_notes).
- Each pack has a `manifest.json` indexing all monster_ids used by its act files, plus a `monsters/` directory with a stat block per id.
- Content generated from training knowledge of the official modules — no invented plot; flavor/dialog allowed.
- All encounters carry a `scaling` note for a 6-PC party (see party-scaling sub-doc).
- Dungeon-crawl emphasis: prioritize the site-based dungeon chapters (Forge of Fury entirely; DoIP's Axeholm, Dragon Barrow, Icespire Hold).

## References
- Existing pattern: `adventures/lmop/` and `docs/backlog/done/027-domain-build-adventure-pack-system.md`
- Schema: `contracts/adventure-scene-contract.json`
- Loop pickup: `.claude/commands/game-play.md` Step 2.5; `.claude/skills/campaign/references/loop-execution-protocol.md`

## Task Builder Input
- **Deliverable:** Two complete adventure packs under `adventures/` (manifests, monsters, and all act files) ready for `game-play`.
- **Location:** workspace:adventures/
- **Scope:** BUILD
- **Constraints:** One act file = one task (atomic). One manifest per pack = one task. Monster stat blocks may be grouped per pack into one task each or per-monster. Must follow adventure-scene-contract schema. No kernel intent-chain available in this repo (lib/attestation absent) — skip intent recording.
