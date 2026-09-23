# Party Scaling — 6-PC High-Power Group

## Status
NEW (cross-cutting design concern for both packs)

## Location
Applies to every act file in both `adventures/dragon-of-icespire-peak/` and `adventures/forge-of-fury/`.

## Why
Both modules assume a 4-PC party. Campaign-2026-05-27-002 is **6 PCs at Level 4**, running an unusually high-power build (Forge-of-Spells magic items, Battle Master + Champion + Divination wizard + Vengeance paladin + Assassin + Life cleric). Default encounters will be trivial. Scaling must be baked into each act's encounter data.

## Scaling Rules (put a `scaling` block in every act file)
- **Enemy count:** +50% minimum on mook groups (round up). Boss fights: add 1–2 lieutenant/elite adds rather than inflating the boss alone.
- **Deadly gates:** for finale bosses (Cryovain, Nightscale), keep the boss as-written but add terrain hazards + adds so the fight is a real threat to 6 optimized PCs.
- **XP:** divide encounter XP by 6 (party size) for `xp_per_pc`; keep total `reward_xp` as the sum of scaled enemy values.
- **Loot:** keep signature magic items as-written (do not multiply); scale consumables/gold modestly (~+25%).
- **Record it:** each act file's `scaling` object = `{ "party_size": 6, "encounter_scaling": "+50% enemy count", "note": "..." }` — same pattern as LMoP campaign_state `scaling`.

## Dependencies
- Consumed by both pack sub-docs during act-file authoring.
