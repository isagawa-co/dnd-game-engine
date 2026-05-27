# Tactical Zone System

## Status
Open

## Priority
Low — theater of the mind works for now but limits tactical depth. A simple zone system would enable better positioning, flanking, and area-of-effect decisions.

## Summary
Add a lightweight zone-based positioning system for combat. Not a full grid — just named zones (front line, back line, flanking, elevated, cover) that track where combatants are relative to each other. This enables meaningful tactical choices like "move to flanking position" or "retreat to cover" without requiring a visual map.

## Requirements
- Define zone types: melee range, ranged (near), ranged (far), elevated, cover, flanking
- Track combatant positions in combat state
- Movement between zones costs movement speed
- Zones affect combat: flanking grants advantage, cover grants +2/+5 AC, elevated grants advantage on ranged
- Integrate with combat loop turn resolution
- Act file encounters can define starting zones per enemy group

## References
- Combat state contract: `.claude/skills/combat/contracts/combat-state-contract.json`
- Combat loop: `.claude/skills/combat/SKILL.md`
- D&D 5e PHB: cover rules, flanking optional rule

## Task Builder Input
- **Deliverable:** Zone system contract + combat loop integration
- **Location:** workspace
- **Scope:** BUILD
- **Constraints:** Must be simple — 4-6 zone types max. Not a grid system.
