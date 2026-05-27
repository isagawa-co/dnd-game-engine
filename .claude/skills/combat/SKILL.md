# Combat — Skill Definition

**Type:** Reference
**Domain:** D&D Game Engine

## What

Combat loop sub-skill managing tactical combat encounters: roll initiative, execute rounds with action economy, resolve attacks and spells via atomic-ops, apply damage and conditions, track death saves, and return combat outcome to scene loop.

## Architecture — Combat Loop Flow

```
Scene Loop (007)
  └── Combat Encounter triggered
        └── Initialize: roll initiative (1d20 + dex_modifier per combatant)
              └── Sort turn order (highest initiative first)
                    └── Execute Rounds
                          ├── Each combatant acts in initiative order
                          │     ├── action: attack / cast_spell / ability_check / dodge / disengage / dash / help / ready
                          │     ├── resolve action → apply damage / effects
                          │     ├── check concentration (on damage taken)
                          │     └── advance conditions (reduce duration, remove expired)
                          ├── Check outcomes: all enemies dead? all PCs dead? escape? draw?
                          │     ├── victory → return xp_earned + loot
                          │     ├── defeat  → return defeated_pcs with death_save_results
                          │     ├── escape  → return surviving state, no XP
                          │     └── draw    → return surviving state, no XP
                          └── Increment round_number, repeat
```

## Contracts

| Contract | Location | Purpose |
|----------|----------|---------|
| combat-loop-contract.json | -> [[contracts/combat-loop-contract.json]] | Combat input/output schemas: party_pcs, enemies, terrain, outcome with result codes |
| combat-state-contract.json | -> [[contracts/combat-state-contract.json]] | Per-round state: combatant status, action economy, conditions, death saves |
| combat-action-contract.json | -> [[contracts/combat-action-contract.json]] | Action resolution: request/result schemas for all action types |

## Flow

1. **Initialize** — Receive combat_input (encounter_id, party_pcs, enemies, terrain). Roll initiative for each combatant. Sort by descending initiative. Set phase to "combat".
2. **Start Round** — Increment round_number. Reset action economy for all combatants (action=true, bonus_action=true, reaction=true, movement=base).
3. **Execute Turns** — For each combatant in turn_order:
   - Receive action_request (actor_id, action_type, target_id, parameters)
   - Resolve action via action_type_rules in combat-action-contract
   - Apply damage/healing via atomic_ops/damage_operations
   - Apply conditions via atomic_ops/effect_operations
   - Check concentration (DC = max(10, damage/2)) on damage taken
   - Advance condition durations (reduce by 1, remove if 0)
4. **Check Outcomes** — After each turn, check:
   - All enemies HP <= 0 → result_code: victory
   - All PCs HP <= 0 (or failed death saves) → result_code: defeat
   - Escape action successful → result_code: escape
   - Both sides cease → result_code: draw
5. **Return Outcome (MANDATORY — complete ALL sub-steps before any post-combat narration):**
   - a. Declare result_code (victory/defeat/draw/escape)
   - b. Calculate XP: sum all defeated enemy xp_values, divide by party size, show the math
   - c. Present loot from the act file's `loot` array — list every item with quantity
   - d. **Save to campaign_state.json** immediately:
     - Set `combat.active = false`
     - Write `combat.last_combat` with encounter id, result, rounds, xp_earned, xp_per_pc
     - Append items to `loot_collected`
     - Update `party_xp` for each PC
     - Update `spell_slots_used` for any casters who spent slots
   - e. Only AFTER saving state, proceed to post-combat narration
   - **ANTI-DRIFT RULE: Do NOT narrate post-combat scenes, present action menus, or transition to the next act until steps 5a-5d are complete. The user must see XP and loot before the scene moves on.**

## Death Save Mechanics

When a PC reaches 0 HP:
- Each turn at 0 HP: roll 1d20 (no modifiers)
- Roll >= 10: 1 success. Roll < 10: 1 failure
- Natural 20: regain 1 HP, become conscious
- Natural 1: counts as 2 failures
- 3 successes: stabilized (unconscious but alive)
- 3 failures: dead (permanently removed from combat)
- Damage at 0 HP: each hit = 1 failure (critical = 2 failures)

## Action Economy

Each combatant per turn receives:
- **Action** (1): attack, cast_spell, ability_check, dodge, disengage, dash, help, ready
- **Bonus Action** (1): certain spells, class abilities
- **Reaction** (1): opportunity attacks, readied actions, certain spells
- **Movement**: base speed in feet (typically 30)

## Action Prompt Integration

At each PC's turn, use the **action-prompt** skill (`.claude/skills/action-prompt/SKILL.md`) with `combat_turn` context. Personalize attacks with the PC's actual weapons, damage dice, and modifiers. Present bonus actions separately after the main action resolves.

## Integration

- **Scene Loop (007)** — Combat loop is invoked by scene loop when combat encounter triggers
- **Atomic Ops (003)** — Attack rolls via attack_operations, damage via damage_operations, effects via effect_operations, checks via check_operations
- **Party State** — Reads combatant HP, AC, conditions; writes HP changes, condition changes, death results
- **Action Prompt** — Uses action-prompt skill for standardized PC turn presentation

## Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| Invalid action_type | Not in allowed list | Error: "Invalid action type: [type]" |
| Target not found | target_id not in combatants | Error: "Target not found: [id]" |
| No action remaining | action already spent this turn | Error: "No action available" |
| Invalid target side | Attacking own side without override | Error: "Cannot target ally" |
| Dead combatant acting | Combatant at 0 HP tries to act | Skip turn, proceed to death saves |
