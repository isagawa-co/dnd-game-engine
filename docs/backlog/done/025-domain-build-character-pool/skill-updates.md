# Skill Updates for Character Pool

## Status
NEW

## Files to Update

### 1. Character Creation Loop (`.claude/skills/character-creation-loop/character-creation-loop.md`)

**Part 5: Save to Campaign** — currently saves everything to `campaigns/<id>/party.json`. Change to:

1. Save each PC entity to `characters/<character-id>.json` (shared pool)
2. Update `campaigns/<id>/party.json` with character ID references (not full entities)
3. Update `campaigns/<id>/campaign_state.json` party array with character IDs
4. Add `creation_metadata` to each character (method, date, source campaign)

**Part 3: Party Assembly** — currently collects PC entities into campaign.party array. Change to:
1. Collect character IDs instead of full entities
2. Write references to party.json
3. Full entities already saved in step above

### 2. Character SKILL.md (`.claude/skills/character/SKILL.md`)

**Resolution Flow > Character Creation > Step 8 Output** — update to mention saving to character pool.

**Add Integration entry:**
| Direction | System | Interface |
|-----------|--------|-----------|
| Produces | Character Pool | Writes to `characters/<id>.json` |

### 3. Character Creation Contract (`.claude/skills/character/contracts/character-creation-contract.json`)

**output_schema** — add `creation_metadata` object to the character output:
```json
"creation_metadata": {
  "type": "object",
  "properties": {
    "creation_method": { "type": "string" },
    "created_date": { "type": "string" },
    "source_campaign": { "type": "string" }
  }
}
```

### 4. Game-Play Command (`.claude/commands/game-play.md`)

**Step 2: Load campaign state** — add character resolution step:
- After loading campaign state, resolve character IDs from `characters/` directory
- Build in-memory party array from resolved character entities
- Pass resolved party to loop systems

## Dependencies
- Character pool contract (025/character-pool-contract) must be defined first
- 024 (flatten) must complete first so paths are at repo root
