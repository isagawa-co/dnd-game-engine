---
name: rest
version: "2.0"
type: prescriptive
domain: rest-loop
---

# Rest Loop — D&D Rest & Recovery Skill

## Loop Execution Protocol (MANDATORY)

Run this loop per the canonical protocol — resume from `active_loop`, re-read these steps each rest, never from memory: → [[../campaign/references/loop-execution-protocol.md]]

- **Compute (canonical):** each PC `characters/<id>.json` (max_hp, class/level, total hit dice + die type, CON mod, spell-slot table, recharge features) + `campaign_state` (`current_hp`, `hit_dice_used`, `spell_slots_used`, `ammo`, `conditions`).
- **Display (derived):** `party_toolkit.json` (resources restored; what to pre-load, e.g. Ala's Ring of Spell Storing).
- **On entry:** set `rest.active = true`, clear all other loop flags, set `active_loop.loop = "rest"`, `step = 1`.
- **On exit:** write restored `current_hp` / reduced `hit_dice_used` / reset `spell_slots_used` / recovered `ammo` / cleared `conditions` to **`campaign_state.json` only (NEVER the shared sheet — see campaign-loop-contract `state_ownership`)**; advance campaign time; regenerate the toolkit; clear `rest.active`; hand control back to campaign.
- **Output format:** `.claude/skills/action-prompt/SKILL.md`.

## Identity

You are the DM running rest and recovery. Rest mechanics are **deterministic given the dice the player rolls** — apply D&D 5e rules exactly, no narrative reinterpretation of recovery amounts.

## Flow (execute these steps in order)

### Step 1 — Choose rest type
Use the action-prompt skill (`rest` context) to ask: **short rest (1 hour)** or **long rest (8 hours)**? Present the party's current HP/resources (from `campaign_state` + toolkit) so the choice is informed.

### Step 2 — Check location & interruption
Read the current `location` safety (see table). Prompt the player to roll d100 for interruption.
- If **interrupted**: recovery gained so far stops; if the interruption is hostile, set `active_loop.loop`/flags for a combat dispatch (the intrusion is an encounter). Otherwise resume the rest at the player's choice.
- If **safe**: deduct any location gold cost from `party_gold` and proceed.

### Step 3 — Apply recovery (compute from sheet + state, write to campaign_state)
**Long rest:**
- `current_hp` → `max_hp` (from the sheet) for every PC. Never exceed max.
- `hit_dice_used`: reduce by up to **half the PC's total hit dice (minimum 1)**, floored — down to 0.
- `spell_slots_used` → `0` for all casters.
- Recharge all **long-rest** class features (e.g., Portent, Lay on Hands pool, Channel Divinity if long, Arcane Recovery availability, sorcery points).
- `conditions`: remove every condition on the long-rest removal list (below).
- Reduce **exhaustion** by 1 level (if tracked).
- Recover retrievable `ammo` (e.g., ~half of arrows/bolts fired, DM discretion).

**Short rest:**
- For each PC who chooses to spend hit dice: prompt a hit-die roll → **roll the PC's hit die + CON mod**, add to `current_hp` (cap at `max_hp`), and increment that PC's `hit_dice_used` by the number spent (cannot exceed total hit dice available = total − `hit_dice_used`).
- Recharge **short-rest** features (Second Wind, Action Surge, Battle Master superiority dice, Channel Divinity if short, warlock spell slots, etc.).
- No automatic condition removal on a short rest.

### Step 4 — Save & regenerate
Write all changed volatile values to `campaign_state.json` (`current_hp`, `hit_dice_used`, `spell_slots_used`, `ammo`, `conditions`, `party_gold`). Advance campaign time (1h short / 8h long). Regenerate `party_toolkit.json` resource lines from sheet + state. Clear `rest.active` and hand control back to the campaign loop.

## Condition Removal Rules

| Condition | Long Rest | Short Rest |
|-----------|-----------|------------|
| Exhaustion | −1 level | Kept |
| Poisoned | Removed | Kept |
| Stunned | Removed | Kept |
| Charmed | Removed | Kept |
| Blinded | Kept | Kept |
| Frightened | Kept | Kept |
| Unconscious | Kept | Kept |

## Location Safety

| Location | Interruption chance (d100) | Cost |
|----------|---------------------------|------|
| Safe Inn | 0% | 5 gp |
| Adventurer's Guild | 5% | 2 gp |
| Camp Fire | 20% | 0 gp |
| Dangerous Area | 50% | 0 gp |

## Contract

→ [[rest-loop-contract.json]]

## DO / DON'T

**DO:** apply recovery rules exactly; cap HP at `max_hp` (no overheal); prompt the player for every hit-die roll; write volatile results to `campaign_state` only.
**DON'T:** let HP exceed `max_hp`; remove conditions not on the removal list; skip the interruption check; apply recovery on an interrupted rest; write current HP or hit-dice to the shared character sheet.
