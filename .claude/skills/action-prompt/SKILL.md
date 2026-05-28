# Action Prompt — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | action-prompt |
| Type | helper-skill |
| Parent | all loops (campaign, scene, combat, challenge, social, travel, rest, merchant) |
| Purpose | Standardized presentation of player choices at every decision point in the game |

## Contract

| Contract | Path | Purpose |
|----------|------|---------|
| Action Prompt | `contracts/action-prompt-contract.json` | Action menu schema, context defaults, option structure |

## Core Rule

**Every time the agent reaches a decision point where the user must choose an action, the agent MUST use this skill's presentation format. No exceptions.**

This applies to:
- Exploration scenes ("What do you do?")
- Combat turns ("It's your turn. What do you do?")
- Social encounters ("How do you respond?")
- Travel decisions ("The road forks. Which way?")
- Rest choices ("You find a clearing. Do you rest?")
- Loot/merchant interactions
- Any other moment where the user has agency

## Presentation Format (MANDATORY)

Every action prompt follows this exact structure:

```
[Narration of current situation — what the user sees, hears, feels]

---

ACTIONS:
1. [Action label] ([hint if applicable])
2. [Action label]
3. [Action label]
4. [Action label]
5. [Action label]

Or describe what you'd like to do.

---
```

### Format Rules

1. **Narration first** — Always describe the situation before showing options. The user needs context to decide.
2. **Horizontal rules** — Use `---` to visually separate narration from the action menu and the action menu from the custom input line.
3. **Numbered list** — Actions are always a numbered list (1, 2, 3...). Never bullets, never lettered.
4. **Hints in parentheses** — If an action requires a skill check, spell, or has a prerequisite, show it: `1. Persuade (CHA — Persuasion)`.
5. **Custom input last** — Always end with `Or describe what you'd like to do.` on its own line after the numbered list.
6. **Minimum 3 options, maximum 8** — Fewer than 3 feels restrictive. More than 8 causes decision paralysis.
7. **No "other" option** — The custom input line replaces a generic "other" option. Don't put "Do something else" as a numbered choice.

## Building the Action Menu

### Step 1: Determine Context

Identify which context applies from the contract:
- `exploration` — free roam, no active encounter
- `combat_turn` — active combat, PC's turn
- `social` — talking to an NPC
- `travel` — moving between locations
- `rest` — deciding whether/how to rest
- `merchant` — shopping interaction
- `loot` — post-combat or discovery
- `party_decision` — fork in the road, group choice
- `level_up` — level-up choices

### Step 2: Load Context Defaults

Read `context_defaults` from `contracts/action-prompt-contract.json` for the matching context. These are your starting options.

### Step 3: Adapt to Situation

Modify the defaults based on the actual game state:

| Situation | Adaptation |
|-----------|------------|
| NPC present | Replace generic "Talk to NPC" with NPC's name: "Talk to Aldric" |
| Locked door visible | Add: "Pick the lock (requires Thieves' Tools)" |
| Party member injured | Add: "Heal [name] (requires healing spell or potion)" |
| Specific object present | Add: "Examine the [object]" |
| Option not applicable | Remove it (e.g., remove "Attack (ranged)" if no ranged weapon equipped) |
| Environmental feature | Add: "Climb the wall", "Swim across", "Jump the gap" |

**Always adapt.** Generic defaults alone feel robotic. The menu should reflect what's actually in front of the party.

### Step 4: Present

Use the mandatory format from above. Ensure hints are included for any action that will trigger a roll.

## Environment Detail Rule (MANDATORY)

Every scene description — combat, exploration, social, travel, any context — MUST include **3+ interactable elements** in the environment. These are things the party can use, manipulate, or exploit creatively.

Examples:
- Combat: "Oil barrels against the wall, a rickety wooden platform above, a narrow choke point between two pillars"
- Exploration: "A rusted iron gate, thick vines covering the east wall, a stream running through a crack in the floor"
- Social: "A crowded tavern with a bard performing, a back exit behind the bar, a drunk guard at the next table"
- Travel: "Dense tree cover on both sides, a steep ravine to the left, an abandoned cart blocking half the road"

**Why:** The user can't be creative if the scene is bare. Interactable elements are the raw material for improvised solutions — kicking barrels, collapsing platforms, using terrain for advantage. Describe the space like a real place, not an empty room with enemies in it.

## Party Toolkit (MANDATORY — show at every decision point)

Before presenting the action menu, show a concise summary of what the **entire party** can do. This gives the user the building blocks to combine into creative solutions.

Format:

```
PARTY TOOLKIT:
  Honu: Shell Defense (AC 21), Second Wind (1d10+2), Action Surge, STR grapple (+5), rope 50ft
  Bron: Charge (bonus attack after 30ft), Equine Build (carry/push double), hooves (1d4+4), javelin x4
  Raistlin: Portent (2 pre-rolled d20s), Find Familiar (scout), Mage Hand (30ft), Minor Illusion, Identify (ritual), Absorb Elements (reaction), 3 spell slots
  Dain: Divine Sense (detect undead/fiends), Lay on Hands (10 HP), Divine Smite (2d8 on hit), shield
  Ala: Thieves' Tools, caltrops, crowbar, rope 50ft, Cunning Action (Hide/Dash/Disengage), Darkvision 60ft, bell + string
  Sweeney: Guidance (+1d4 any check), Spare the Dying, Healing Word (bonus action heal), Channel Divinity: Preserve Life (10 HP split), torches, rope 50ft
```

### Toolkit Rules
- **Show at every decision point** — not just combat. Exploration, social, travel, challenges — everywhere the user chooses what to do
- **Include non-obvious capabilities** — racial features (Darkvision, Shell Defense, Charge), tools (thieves' tools, caltrops, rope), utility spells (Mage Hand, Find Familiar, Guidance), inventory items (oil, crowbar, bell)
- **Skip the obvious** — don't list basic weapon attacks here (those go in the action menu). Focus on the creative building blocks
- **Mark spent resources** — if Portent dice are used, spell slots spent, Lay on Hands depleted, show it: `Portent (0 remaining)`, `spell slots: 1/3`
- **Keep it concise** — one line per character, comma-separated capabilities. No descriptions, just names. The user can ask for details
- **On request** — if the user asks "what can we do?" or "remind me of our abilities," show the full toolkit even outside a decision point

## Creative Action Resolution

When the user describes an improvised or creative action not covered by standard rules:

1. **Never say no** — find a way to attempt it. If truly impossible, explain why in-character
2. **Pick the closest skill** — map the action to the most relevant ability check (Athletics for physical feats, Arcana for magical improvisation, etc.)
3. **Set DC by difficulty:**
   - Trivial (auto-success): no roll needed
   - Easy (DC 10): reasonable idea, minor risk
   - Medium (DC 15): clever but uncertain
   - Hard (DC 20): ambitious, requires skill
   - Near-impossible (DC 25): desperate long shot
4. **Grant advantage for clever combos** — if the user combines multiple party capabilities in a smart way (e.g., "Raistlin uses Mage Hand to pull the lever while Ala sneaks past with caltrops behind her"), give advantage on the key roll
5. **Narrate the attempt cinematically** — creative actions deserve creative narration, whether they succeed or fail

## Handling User Response

### Numbered Selection

User types a number (e.g., `3`):
- Map to the corresponding action from the menu
- Proceed with that action in the calling loop
- If the action requires a roll, prompt for the roll immediately

### Custom Action

User types free text (e.g., "I want to check if the ceiling has any markings"):
- Parse the intent
- Determine if it maps to an existing action type from the contract (`investigate`, `skill_check`, etc.)
- If it requires a roll, determine the appropriate check and prompt
- If it's purely narrative (no roll needed), resolve it through narration
- Never reject a custom action — always attempt to resolve it. If it's impossible, explain why in-character ("You reach for the ceiling but it's 30 feet up — you'd need to climb first.")

### Ambiguous Input

If the user's input is unclear:
- Ask a single clarifying question
- Re-present the action menu with the clarification
- Do NOT re-present the full narration — just the menu

## Combat-Specific Rules

During combat, the action menu reflects D&D 5e action economy:

```
ACTIONS (your turn):
1. Attack — Mace (1d6+3 bludgeoning, melee)
2. Attack — Light Crossbow (1d8+2 piercing, range 80/320)
3. Cast a spell
4. Dash (double movement)
5. Dodge (attacks against you have disadvantage)
6. Help (give an ally advantage)
7. Use an item

Or describe what you'd like to do.
```

- **Personalize attacks** — Show the PC's actual weapons with damage dice and modifiers, not generic "melee attack"
- **Show spell option** — If the PC has spell slots remaining, include "Cast a spell". When selected, show a sub-menu of available spells.
- **Bonus actions** — If the PC has bonus action options (e.g., Cunning Action, offhand attack), present them AFTER the main action resolves: "You still have your bonus action."
- **Movement** — Don't present movement as an action choice. Handle it naturally: "You're 30 feet from the goblin. Do you close in or stay back?"

## Social-Specific Rules

During social encounters, adapt options to the NPC's attitude:

| NPC Attitude | Available Options |
|-------------|-------------------|
| Hostile | Intimidate, Deceive, Flee, Attack |
| Unfriendly | Persuade, Intimidate, Deceive, Insight, Leave |
| Neutral | Persuade, Insight, Ask questions, Leave |
| Friendly | Ask questions, Request help, Trade, Leave |
| Allied | Plan together, Share information, Request aid |

## Multi-Character Decisions

When the action affects the whole party (e.g., "Which way do you go?"), present once for the party leader or let the user decide for the group. Don't ask each character individually unless it's combat.

When individual PC actions matter (combat, individual skill checks), specify which PC is acting:

```
ALA'S TURN:
1. Attack — Rapier (1d8+4 piercing, finesse)
2. Attack — Shortbow (1d6+4 piercing, range 80/320)
3. Sneak Attack setup — move to flank position
4. Cunning Action — Hide / Dash / Disengage
5. Use Thieves' Tools on the chest

Or describe what Ala does.
```

## Integration with Calling Loops

Each loop calls this skill at its decision point. The loop does NOT need to implement its own presentation logic — it delegates to this skill.

| Loop | When It Calls Action Prompt |
|------|-----------------------------|
| Campaign Loop | Step 4 — "Prompt user for action" |
| Scene Loop | After describing the scene, before encounter resolution |
| Combat Loop | Each PC's turn |
| Challenge Loop | When the PC chooses how to approach the challenge |
| Social Loop | Each exchange in dialog |
| Travel Loop | At decision points during travel |
| Rest Loop | When choosing rest type and watch order |

The calling loop resumes after the user responds and the action is resolved.
