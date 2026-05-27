# State Check — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | state-check |
| Type | helper-skill (soft enforcement) |
| Parent | all game loops |
| Purpose | Mandatory post-action state validation and persistence |
| Enforcement | Paired with `game-state-enforcer.py` hook (hard enforcement) |

## Core Rule

**After every resolved game action, the agent MUST run this checklist and save campaign_state.json BEFORE narrating the result or presenting the next action prompt.**

This is Layer 1 (soft). Layer 2 (hard) is the `game-state-enforcer.py` hook which blocks scene transitions and validates state writes.

## When to Run

| Context | Trigger | Frequency |
|---------|---------|-----------|
| Combat | End of combat (victory/defeat/escape/draw) | Once per encounter |
| Combat | End of each round | Once per round |
| Exploration | After each player action resolves | Each action |
| Social | After each exchange with NPC | Each exchange |
| Challenge | After skill check resolves | Each check |
| Rest | After rest completes | Once per rest |
| Travel | After travel segment completes | Each segment |
| Loot | After loot is collected | Each collection |

## The Checklist

After resolving an action, check every row. If the answer is YES, update the field in campaign_state.json.

| # | Check | Field to Update | Example |
|---|-------|----------------|---------|
| 1 | Did any PC or enemy take damage? | `combat.enemies[].hp_remaining`, PC hp in character files | Goblin took 12 damage → hp 7→0 |
| 2 | Did anyone spend a resource? | `spell_slots_used`, class feature uses, ammo count | Raistlin cast Sleep → 1st-level slot spent |
| 3 | Was loot gained? | `loot_collected` | 8gp + 6 shortbows collected |
| 4 | Was XP earned? | `party_xp` | 50 XP per PC from goblin fight |
| 5 | Did a quest update? | `quests[].status` or new quest added | Found Gundren's map case → new quest |
| 6 | Did location change? | `current_location` | Moved from trail to ambush site |
| 7 | Was an NPC encountered? | `npcs` array | Met Sildar Hallwinter |
| 8 | Did conditions change? | Character conditions, exhaustion | PC poisoned, goblin asleep |
| 9 | Did combat state change? | `combat.active`, `combat.enemies`, `combat.round` | Combat ended → active: false |
| 10 | Did act/chapter progress? | `current_act`, `current_act_id`, `current_chapter` | Completed Act II → Act III |

## Output Format

After running the checklist, the agent outputs:

```
STATE CHECK:
- [x] HP: Goblin G1 0/7, G2 0/7
- [x] Resources: Raistlin 1st-level slot (1/2 remaining)
- [x] Loot: +8gp, +6 shortbows, +6 scimitars
- [x] XP: +50 per PC (300 total)
- [x] Quest: "Rescue Gundren" added
- [ ] Location: no change
- [ ] NPCs: no change
- [ ] Conditions: no change
- [x] Combat: active → false
- [ ] Act progress: no change

Saving campaign state...
```

Then saves campaign_state.json. Then narrates.

## Integration with Calling Loops

Each loop calls this skill at its resolution point:

| Loop | When It Calls State Check |
|------|--------------------------|
| Combat Loop | Step 5 (Return Outcome) — before post-combat narration |
| Campaign Loop | After Step 3 resolves any encounter |
| Scene Loop | After dispatch_encounter returns outcome |
| Challenge Loop | After skill check result is determined |
| Rest Loop | After rest effects are applied |
| Social Loop | After NPC attitude or quest state changes |
| Travel Loop | After travel segment or random encounter |

## Relationship to Hard Enforcement

This skill is the instruction manual. The `game-state-enforcer.py` hook is the lock:

| Layer | What | How |
|-------|------|-----|
| Soft (this skill) | Tells agent what to check | Agent reads and follows checklist |
| Hard (hook) | Blocks agent if it skips | Hook validates writes and blocks scene transitions |

If the agent follows this skill correctly, the hook never fires. If the agent drifts, the hook catches it.
