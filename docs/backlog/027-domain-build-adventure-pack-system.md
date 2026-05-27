# Build Adventure Pack System

## Status
Open

## Priority
High — Game loop cannot follow official adventures without structured scene data. Agent drifts into improvisation without it.

## Summary
Create the adventure pack architecture that sits between stat blocks and campaign state. Rename `content/` to `adventures/`, define the adventure scene contract (act schema), update the game loop to build and traverse scenes per chapter, and populate LMoP as the first adventure. This prevents agent drift by giving the game loop a structured script to follow.

## Design Documents

| Document | Purpose |
|----------|---------|
| [[027-domain-build-adventure-pack-system/folder-restructure]] | Rename content/ to adventures/, new folder layout with scenes/ per adventure |
| [[027-domain-build-adventure-pack-system/adventure-scene-contract]] | JSON schema for act files — encounters, transitions, read-aloud text, loot |
| [[027-domain-build-adventure-pack-system/game-loop-integration]] | Update game-play flow to build scenes if missing and traverse them |
| [[027-domain-build-adventure-pack-system/lmop-adventure-build]] | Populate LMoP chapters 1-4 with act files using training knowledge |
| [[027-domain-build-adventure-pack-system/campaign-reset]] | Reset campaign-2026-05-27-002 to use new adventure structure |

## Architecture

```
adventures/lmop/
  manifest.json                    ← stat block index (migrated from content/)
  monsters/                        ← migrated
  items/                           ← migrated
  spells/                          ← migrated
  scenes/                          ← NEW
    chapter-1-goblin-arrows/
      act-I.json
      act-II.json
      act-III.json
    chapter-2-phandalin/
      act-I.json
      act-II.json
      act-III.json
    chapter-3-spiders-web/
      act-I.json
      act-II.json
    chapter-4-wave-echo-cave/
      act-I.json
      act-II.json
      act-III.json
```

## Game Loop Flow (Updated)

```
/game-play [campaign-id]
  1. Load campaign state → get current chapter + act
  2. Load adventure manifest → verify adventure exists
  3. Check if current chapter scenes exist → if not, build them
  4. Read current act.json → follow the script
  5. Present read_aloud + action menu (action-prompt skill)
  6. Resolve encounters using monster stat blocks from adventures/[id]/monsters/
  7. Follow transitions to next act or chapter
  8. Save campaign state with updated position
```

## Requirements
- Rename `content/` → `adventures/` across all references
- Adventure scene contract defines act schema
- Game loop reads act files sequentially — agent narrates WITHIN the act, does not invent outside it
- LMoP chapters 1-4 fully populated with acts
- Campaign state tracks `current_chapter` and `current_act` for resume
- Future adventures follow same pattern

## References
- Current content pack: `content/lost-mine-phandelver/`
- Game-play command: `.claude/commands/game-play.md`
- Action prompt skill: `.claude/skills/action-prompt/SKILL.md`
- Campaign loop skill: `.claude/skills/campaign/SKILL.md`

## Task Builder Input
- **Deliverable:** Adventure pack system — contract, folder restructure, game loop integration, LMoP scenes
- **Location:** `workspace`
- **Scope:** BUILD
- **Constraints:** Must not break existing campaign state. LMoP content from agent training knowledge. All `content/` references updated to `adventures/`.
