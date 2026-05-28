# Campaign Reset

## Status
NEW

## Location
`workspace:campaigns/campaign-2026-05-27-002/`

## What It Does
Reset campaign-2026-05-27-002 to use the new adventure pack structure. Remove the improvised "Forgotten Throne" story data and point the campaign at LMoP Chapter 1, Act I.

## Changes

### campaign.json
- Update `content_pack` → `adventure_id`: `"lmop"`
- Update `campaign_name` → `"Lost Mine of Phandelver"`
- Update `party_pcs` to reflect all 6 characters

### campaign_state.json
- Reset to session 1 start
- Add `adventure_id`, `current_chapter`, `current_act`, `current_act_id`
- Clear `loot_collected` (Forgotten Throne loot doesn't apply)
- Clear `npcs` (Forgotten Throne NPCs don't apply)
- Clear `quests`
- Reset `campaign_time_elapsed_hours` to 0
- Keep `party` array (characters carry over)

### Remove
- `session-1-intel.json` — Forgotten Throne intel, not applicable

### Keep
- `party.json` — party composition is unchanged
- All character files in `characters/` — party carries over to LMoP

## Dependencies
- folder-restructure (adventure_id must reference adventures/lmop/)
- lmop-adventure-build (scenes must exist before play)
