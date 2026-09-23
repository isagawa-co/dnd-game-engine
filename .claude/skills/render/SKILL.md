# Render — Map Rendering Skill

## Identity

| Key | Value |
|-----|-------|
| Skill | render |
| Type | helper-skill (modular; called by any loop) |
| Parent | all spatial loops (combat, scene/exploration, travel, positional challenge) |
| Purpose | Draw an emoji grid of the CURRENT situation — dungeon or not — above the action-prompt menu |

## What it is (and is NOT)

Render is a **standalone, modular skill invoked as a render STEP** by whatever loop is active — like `action-prompt`, but for spatial layout. It is **DISPLAY-ONLY**.

- It has **NO `render.active` flag** and is **never dispatched** by `state-evaluation-contract.json`. It does not compete in the one-flag mutual-exclusion invariant that `loop-dispatch-enforcer` guards — you render *during* combat/exploration/travel, not *instead of* them.
- It resolves nothing; it emits the grid + legend and returns to the calling loop.

## Contracts

| Contract | File | Purpose |
|----------|------|---------|
| Render | → [[contracts/render-contract.json]] | `campaign_state.map` schema, generation + render rules, invocation rules |
| Avatars | → [[avatar-registry.json]] | party avatars (by character_id), monster avatars (by monster_id), category fallbacks, terrain tiles |

## Flow (execute in order)

1. **Get / build the map.** Read `campaign_state.map`. If absent for this scene, **generate it** (Option A): base tile from the act's `location.environment` (`terrain_key`), walls around the border, place enemy tokens from the encounter `position` strings, party at the entrance. Persist to `campaign_state.map`.
2. **Update positions.** On re-render, move tokens per what happened (combat movement, travel, a PC repositioning) — update `map.tokens` x/y; don't regenerate the whole layout unless the scene changed.
3. **Resolve tokens → emoji.** Each tile shows exactly ONE full-width emoji: topmost token if present, else its terrain feature, else the base floor tile. Party: `avatar-registry.party[character_id]`. Enemy: `monsters[monster_id]` → `category_fallbacks[type]` → `default`. Down/dead PCs render 💀 or dimmed.
4. **Draw the grid.** `frame` tiles wide × tall (default **20×10**; shrink/grow as the scene needs; never wrap the terminal). **No row/column labels.**
5. **Legend + placement.** One-line legend under the grid listing only what's shown. The map renders **above** the action-prompt ACTIONS block.

## Frame sizing

Default **20×10**. Use a smaller frame (e.g. 12×8) for a cramped corridor or a tight interior; a larger one for a big battlefield — as long as the row fits the terminal (~2 columns per emoji). One tile ≈ 5 ft.

## Alignment constraint (MANDATORY)

Every glyph on the grid MUST be a **full-width emoji without a variation selector (U+FE0F)**. Half-width glyphs (⚔️ 🛡️ ⛑️ ⬆️ ✝️) break column alignment. Use only tiles/avatars from `avatar-registry.json`. (The lone exception, 🕷️ for giant-spider, has a documented substitute 🦂.)

## Invocation

Called as a render step by:
- **combat** — each round, before presenting the turn
- **scene / exploration** — on entering a location
- **travel** — on arrival or when an encounter triggers
- **challenge** — when the challenge is positional (chase, hazard field)
- **on demand** — any time the player says "show map" / "map"

Non-spatial beats (a pure conversation, a shop menu) may skip the map or draw a simple room.

## Integration

- **Depends on:** avatar-registry (tokens), the active act file (terrain + positions), `campaign_state.map` (tracked positions), action-prompt (the map renders above its menu).
- **Returns to:** the calling loop (display only — nothing to resolve).
- **Canonical step:** the render step is defined once in → [[../campaign/references/loop-execution-protocol.md]]; loops call it there.
