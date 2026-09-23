# Loop Execution Protocol (canonical)

**Applies to:** every gameplay loop — campaign, scene, combat, social, challenge, rest, travel, merchant, item-use.

**Why this exists:** loops were being run *from memory* — the agent recalled "combat is a thing" and free-formed, skipping steps (initiative order, concentration checks, XP/loot save). This protocol makes every loop iteration a precise, resumable, re-read sequence. **Read this at the start of every loop iteration.**

---

## The 5 rules

### 1. Resume from the pointer, never from memory
`campaign_state.active_loop` records `{loop, step, round, turn_actor, resume_hint}`. Before acting, READ it and continue the **exact** step it names. After each step, UPDATE it. If it says `combat / step 3 / round 3 / turn_actor bron`, you resolve Bron's turn — you do not re-improvise the fight.

### 2. Re-read the loop's SKILL, then step
On entering (or re-entering) a loop iteration, RE-READ that loop's `SKILL.md` Flow and execute its numbered steps **in order**. Do not skip, bundle, or reorder. The steps exist because skipping them lost data before. (This is the gameplay form of the kernel lesson *"NEVER IMPROVISE. FOLLOW THE STEPS."*)

### 3. Outer before inner (strict layering)
Control flows **down** one layer at a time and **returns up** explicitly:
```
Campaign (load state + act file)  →  Scene (read encounter → identify → validate → dispatch)
   →  Sub-loop (combat/social/…: run its steps → Return Outcome)  →  Atomic Ops (single mechanic)
```
- Campaign steps 1–2 finish before any scene dispatch.
- Scene steps (read → identify → validate) finish before a sub-loop fires.
- A sub-loop runs to its **Return Outcome** step (and saves) before control returns up.
- Never skip a layer (e.g., jumping from "there are goblins" straight to narrating attacks).

### 4. Read BOTH sources every iteration — compute from canonical, display from derived
| Purpose | Read | Authoritative for |
|---------|------|-------------------|
| **COMPUTE** mechanics (rolls, to-hit, damage, save DC, AC, recovery) | `characters/<id>.json` + `campaign_state.json` | numbers |
| **DECIDE & DISPLAY** tactics (options, signature moves, synergies) | `campaigns/<id>/party_toolkit.json` + `battle-plans/` | strategy |

Read the acting character's **sheet** for static numbers (max_hp, mods, dice, AC, attacks) and **campaign_state** for their current volatile values (`current_hp`, `hit_dice_used`, `spell_slots_used`, `ammo`, `conditions`) — then render the **toolkit** turn-card for options/synergies. Never resolve math off the toolkit; never treat the toolkit as the source of truth.

### 5. Single-source each fact — and never write volatile state to the shared sheet
`characters/<id>.json` is a **SHARED POOL** referenced by multiple campaigns. Writing per-play state to it corrupts every other campaign using that character. See campaign-loop-contract `state_ownership`.
- **Static numbers** (max_hp, ability mods, AC formula, to-hit, damage dice, total hit dice) are canonical on the **sheet**. Changed ONLY by creation and level-up.
- **Volatile numbers** (`current_hp`, `hit_dice_used`, `spell_slots_used`, `ammo`, `conditions`, `party_xp`) are canonical in **campaign_state.json**. Every gameplay loop writes these HERE, never to the sheet.
- **Strategy** (move framing, party synergies, battle plans) is canonical in the **toolkit**.
- The toolkit *mirrors* static numbers and must not disagree; regenerate it from sheet + state on level-up / new item. Never hand-edit a number into only one place.

---

## Entry / exit checklist for any loop

**On entry:** set this loop's `*.active = true`, clear all other loop flags, set `active_loop.loop` to this loop, `step = 1`. (Mutual exclusion — see campaign-loop-contract `dispatch_invariants`.)

**Each iteration:** read `active_loop` → re-read SKILL step → read sheet+state (compute) + toolkit (display) → resolve via atomic-ops → write state → advance `active_loop.step`.

**On exit (Return Outcome):** complete the loop's mandatory return steps (e.g., combat 5a–5e: result → XP math → loot → SAVE → then narrate), clear this loop's `*.active`, set `active_loop.loop` to the parent context (usually `exploration` or the next dispatched loop), and return control up.

---

## Output formatting

All player-facing output MUST follow `.claude/skills/action-prompt/SKILL.md`: narration (with 3+ interactable elements) → `---` → numbered `ACTIONS:` → `Or describe what you'd like to do.` → `---`, plus the context-appropriate PARTY TOOLKIT / combat turn-card (`NAME'S TURN`, `AC | HP | stat`, `TOOLKIT:`, `SYNERGIES: ← / →`).
