# GDD Granularity

<!-- Seeded: expert knowledge for GDD section quality -->

## The Problem

GDD sections that describe behavior vaguely ("combat uses a damage formula with modifiers") invite drift during Phase 3. The task-builder has to invent behavior, producing code that doesn't match the user's intent.

## Why It Fails

- Vague descriptions have multiple valid implementations
- Different agents interpret the same description differently
- The user's mental model diverges from what gets built
- Bug reports become "it doesn't feel right" — untestable

## Correct Approach

Every GDD section must contain:
- **Data tables** — concrete values, not descriptions (unit stats, building costs, terrain yields)
- **Formulas** — exact math, not "uses a formula" (damage = base * (atk/def) * modifiers)
- **Enumerations** — complete lists, not "such as" (ALL terrain types, ALL unit types)
- **REQ IDs** — one per testable behavior
- **Edge cases** — what happens at boundaries (0 HP, last tech researched, empty inventory)

**Bad:** "Combat uses a damage formula with modifiers"
**Good:** "damage = base_damage * (attacker_strength / defender_strength) * modifier_product. Modifiers: terrain +25%, fortified +25%, walls +50%, flanking +10%/flanker (max 3). REQ-COMBAT-001."

**Test:** Can a developer implement this section without asking a single clarifying question?

## Source

Design principle from backlog 007: design-principles.md (Granularity Principle)
