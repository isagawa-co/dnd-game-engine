# Encounter Auto-Scaling

## Status
Open

## Priority
Medium — currently manual "+50% enemy count" rule. A real engine should calculate CR vs party level and auto-scale encounters from act files.

## Summary
Replace the manual scaling note in campaign_state.json with an automated encounter scaling system. When the agent reads an act file encounter, auto-calculate the appropriate enemy count and difficulty based on party size and average party level using D&D 5e CR/XP thresholds.

## Requirements
- Build scaling contract with D&D 5e XP thresholds per level (easy/medium/hard/deadly)
- Calculate party XP threshold based on party size and level
- Compare encounter XP budget to party threshold
- Auto-adjust enemy count to match target difficulty
- Support difficulty override (e.g. "make this encounter deadly")
- Log scaling decisions in session notes

## References
- Current scaling: `campaign_state.json → scaling` object
- Act files: `adventures/lmop/scenes/*/act-*.json → encounters`
- Monster data: `adventures/lmop/monsters/*.json` (has XP values)
- D&D 5e DMG Chapter 3: encounter building rules

## Task Builder Input
- **Deliverable:** Encounter scaling contract + integration with game-play skill
- **Location:** workspace
- **Scope:** BUILD
- **Constraints:** Must work with existing act file format — read encounter, scale, present
