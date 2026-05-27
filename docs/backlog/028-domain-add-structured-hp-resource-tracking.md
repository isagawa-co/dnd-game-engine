# Runtime Party Status Tracker (Live Delta from Character Templates)

## Status
Open

## Priority
High — without this, HP and resource changes live only in session notes as text. No structured way to track damage, healing, or ability usage per character during gameplay.

## Summary
Add a **runtime `party_status` tracker** to campaign_state.json that captures the **live delta** from character template files. The character JSON files (`characters/*.json`) already have comprehensive static data: hp, max_hp, hit_dice_detail (with remaining), class_features (with uses/recharge), inventory, ability scores, spell_slots. These are the **master templates** created by the character creation system (`character-creation-contract.json` in game-dev repo).

The problem: during gameplay, when Honu takes 8 damage, `honu-tortle-fighter.json` stays at `hp: 12`. The runtime state (current HP, abilities spent, conditions) lives nowhere structured — only in session_notes text. Resuming a session means parsing prose to reconstruct character state.

**This backlog does NOT recreate the character system.** It adds a lightweight runtime layer in campaign_state.json that tracks the live game delta.

## Architecture

```
characters/honu-tortle-fighter.json    ← Master template (static, never modified during play)
  hp: 12, max_hp: 12, class_features: [{Second Wind, uses: 1}]

campaign_state.json → party_status     ← Runtime delta (updated every action)
  honu-tortle-fighter:
    current_hp: 4          ← took 8 damage
    conditions: ["prone"]  ← knocked down
    abilities_used: {"second_wind": 1}  ← spent this rest cycle
    hit_dice_used: 0
```

To get full character state at any point: **read template + apply delta**.

## Requirements
- Add `party_status` object to campaign_state.json keyed by character_id
- Track per character: current_hp, temp_hp, conditions, abilities_used, hit_dice_used, death_saves (successes/failures)
- max_hp comes from the character template file — do NOT duplicate it in party_status
- Reset abilities_used on appropriate rest type (short rest vs long rest per recharge field)
- Update state-check skill to verify party_status updates after combat and rest
- Update game-state-enforcer hook to validate HP changes when combat ends
- Integrate with combat loop (Step 5 — Return Outcome) and rest loop
- On long rest: reset current_hp to max_hp, clear conditions, reset abilities_used, recover hit_dice

## References
- Character templates: `characters/*.json` (master data — hp, max_hp, class_features with uses/recharge)
- Character creation contract: game-dev repo `.claude/skills/character/contracts/character-creation-contract.json`
- Current campaign state: `campaigns/campaign-2026-05-27-002/campaign_state.json`
- Combat loop: `.claude/skills/combat/SKILL.md`
- Rest loop: `.claude/skills/rest/SKILL.md`
- State check: `.claude/skills/state-check/SKILL.md`

## Task Builder Input
- **Deliverable:** Runtime party_status tracker in campaign_state.json + skill/hook updates
- **Location:** workspace
- **Scope:** BUILD
- **Constraints:** Must not modify character template files during gameplay — they are static master data. Must not break existing campaign state format — additive only.
