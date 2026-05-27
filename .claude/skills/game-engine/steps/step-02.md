---
step: 2
name: Genre Section Selection
requires: game_profile
produces: applicable_sections_list
---

# Step 2: Genre Section Selection

## Purpose

Determine which of the 20 GDD sections apply to this game based on genre, scope, and user preferences. Not all genres need all sections — a puzzle game skips combat and AI opponents, a card game skips world space and physics.

## Input

- `docs/game-design/profile.md` — game profile from Step 1
- `references/genre-mapping.md` — section relevance matrix by genre
- `references/gdd-template.md` — full 20-section template with descriptions

## Actions

1. **Read** profile and genre-mapping reference
2. **Look up genre** in the mapping matrix to get default applicable sections
3. **Present sections** to user in three groups:
   - **Core** (always included): Game Loop, World Space, Entities, Player Actions, Rules/Mechanics, Progression, Win/Lose Conditions, Architecture
   - **Genre-dependent** (suggested based on genre): Combat, AI Opponents, Economy, Narrative, Multiplayer, Physics
   - **Infrastructure** (always included): UI/Rendering, Data Model, Configuration, Balance, Scope/Phases, External Dependencies
4. **Recommend** which genre-dependent sections to include/skip based on their game
5. **HITL gate** — user confirms or adjusts the section list
6. **Save** applicable sections list to state file
7. **Generate** `docs/game-design/index.md` with section list and "pending" status for each

## Output

- Updated state with `gdd_sections_applicable` array
- `docs/game-design/index.md` created with all section entries marked "pending"

## Verification

- [ ] Section list reviewed against genre mapping
- [ ] User confirmed section selection
- [ ] State file updated with applicable sections
- [ ] `index.md` created with correct section count

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Too many sections for scope | Tiny scope + 18 sections | Suggest reducing to core + 2-3 genre sections |
| Missing critical section | User skips Rules/Mechanics | Explain why it's needed, offer minimal version |
| Genre not in mapping | Custom genre hybrid | Combine closest two genres, let user adjust |

## Example

**Input:** 4X Strategy, Medium scope

**Genre mapping lookup → default sections:**
Core (8): 1-8 all apply
Genre-dependent: Combat (yes), AI Opponents (yes), Economy (yes), Narrative (optional), Multiplayer (no), Physics (no)
Infrastructure (6): all apply

**Presented to user:**
"For your 4X strategy game, I recommend 17 of 20 sections. Skipping: Multiplayer (not in scope), Physics (turn-based, no physics), and Narrative is optional — want a history log? Let me know if you'd add or remove any."

**Output:** `gdd_sections_applicable: [1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19]`
