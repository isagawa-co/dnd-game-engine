---
step: 1
name: Initial Discovery
requires: user_game_idea
produces: game_profile
---

# Step 1: Initial Discovery

## Purpose

Extract the user's game idea into a structured Game Profile — genre, scope, platform, art style. This profile determines which GDD sections apply (Step 2) and which platform spec drives the build (Phase 3). Discovery is collaborative: suggest options, explain tradeoffs, recommend approaches.

## Input

- User's game idea (free-form text, anything from "I want a 4X game" to a detailed pitch)
- `references/genre-mapping.md` — section relevance by genre
- `references/discovery-questions.md` — initial discovery question set

## Actions

1. **Read** `references/discovery-questions.md` (initial section) and `references/genre-mapping.md`
2. **Greet** the user and acknowledge their idea. Summarize what you understood.
3. **Ask genre question** — present 2-3 genre options that fit their idea, with:
   - Name and brief description
   - Best for (what kind of player experience)
   - Scope implications (small/medium/large)
   - Your recommendation based on what they described
4. **Ask scope question** — after genre is set:
   - Tiny (1-2 systems, weekend project)
   - Small (3-5 systems, ~1 week)
   - Medium (6-10 systems, ~2 weeks)
   - Large (10+ systems, multi-week)
   - Recommend based on their experience level and idea complexity
5. **Ask platform question** — present stack options relevant to genre:
   - Python/Pygame (good for beginners, terminal or 2D)
   - Godot/GDScript (2D/3D, visual editor)
   - TypeScript/Phaser (browser-based, 2D)
   - Lua/LOVE (lightweight 2D)
   - Explain tradeoffs: learning curve, output quality, community support
6. **Ask art style question** — ASCII, pixel art, simple shapes, etc.
7. **Generate profile** — compile answers into `docs/game-design/profile.md`
8. **HITL gate** — present profile summary to user for approval
9. **Save** approved profile to `docs/game-design/profile.md`
10. **Update state** — set `discovery_complete: true`, `game_profile_approved: true`

## Output

- `docs/game-design/profile.md` with genre, scope, platform, art style, idea summary
- State updated with discovery completion

## Verification

- [ ] Genre selected with user confirmation
- [ ] Scope level determined
- [ ] Platform/stack chosen
- [ ] Art style decided
- [ ] Profile saved to `docs/game-design/profile.md`
- [ ] State file reflects `discovery_complete: true`

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| User can't decide genre | "I'm not sure" or long deliberation | Offer 2-3 concrete options with your recommendation |
| Idea too vague | "I want a fun game" | Ask about favorite games, what they enjoy, narrow from there |
| Scope mismatch | User wants AAA scope with solo dev | Gently explain scope realities, suggest phased approach |
| Platform confusion | User unfamiliar with any stack | Recommend Python/Pygame for beginners, explain why |

## Example

**Input:** "I want to make a civilization-style 4X game that runs in the terminal"

**Discovery flow:**
- Genre → 4X Strategy (confirmed: explore, expand, exploit, exterminate)
- Scope → Medium (6-10 systems: map, units, combat, tech, economy, AI, diplomacy, cities)
- Platform → Python/Pygame with terminal rendering
- Art style → ASCII art with Unicode characters

**Output profile.md:**
```yaml
genre: 4x-strategy
scope: medium
platform: python-pygame
art_style: ascii
idea: "Terminal-based 4X civilization game with exploration, city-building, tech trees, and turn-based combat"
systems_estimated: 8
discovery_date: 2026-04-07
```
