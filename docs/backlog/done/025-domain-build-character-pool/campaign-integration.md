# Campaign Integration with Character Pool

## Status
NEW

## How Campaigns Use Characters

### Loading a Campaign (game-play)

```
1. Read campaigns/<id>/campaign_state.json
2. Read campaigns/<id>/party.json → get character_id list
3. For each character_id:
   a. Read characters/<character_id>.json
   b. If not found → error: "Character <id> not found in pool"
   c. Build in-memory party array
4. Pass resolved party to state evaluation + loop dispatch
```

### Creating Characters (character-creation-loop)

```
1. Create Tier 4 PC entity per contract
2. Save to characters/<character-id>.json (shared pool)
3. Add reference to campaigns/<id>/party.json
4. Update campaigns/<id>/campaign_state.json party array
```

### Leveling Up (during gameplay)

```
1. Level up modifies characters/<character-id>.json directly
2. Campaign party.json doesn't need updating (references by ID)
3. Character's campaign_history gets updated with new level
```

### Using Character in New Campaign

```
1. User specifies existing character ID for new campaign
2. Character-creation-loop checks characters/<id>.json exists
3. Adds reference to new campaign's party.json
4. Appends new entry to character's campaign_history
5. Optional: snapshot current level at join time
```

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Character dies in campaign | `campaign_history[].status` set to "dead". Character file remains (history). |
| Character used in 2 campaigns simultaneously | Each campaign references same character ID. Level changes in one affect both (shared state). |
| Character retired | `campaign_history[].status` set to "retired". Still loadable for reference. |
| Character deleted | Remove file from `characters/`. Campaigns referencing it will get load error. |

## Dependencies
- character-pool-contract.json defines the schemas
- game-play command handles the resolution logic
- character-creation-loop handles the save logic
