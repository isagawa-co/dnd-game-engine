---
step: 3
name: GDD Section Walkthrough
requires: applicable_sections_list, gdd_reference
produces: completed_gdd_sections
---

# Step 3: GDD Section Walkthrough

## Purpose

Walk through each applicable GDD section with the user: present the concept, ask discovery questions, generate the section with REQ IDs, and gate on user approval. This is the main loop of Phase 1 — where the real game design happens.

## Input

- State file with `gdd_sections_applicable` and `gdd_sections_complete`
- `references/discovery-questions.md` — per-section question sets
- `references/gdd-reference/NN-*.md` — reference section for calibration
- `docs/game-design/index.md` — current completion status

## Actions

For each section in `gdd_sections_applicable` that is not yet complete:

1. **Read reference** — load `references/gdd-reference/NN-*.md` for the matching section. Use it to calibrate expected granularity. Do NOT show raw reference to user.
2. **Read questions** — load the matching question set from `references/discovery-questions.md`
3. **Present concept** — explain what this section covers, why it matters for their game, and what kind of decisions they'll make
4. **Ask questions one at a time:**
   - Present one focused question per turn
   - For each question: suggest 2-3 options with tradeoffs and your recommendation
   - Reference how similar games handle this decision
   - Wait for user answer before next question
   - Adapt depth based on engagement (skip obvious questions, go deeper on complex ones)
5. **Generate section** with:
   - Data tables with concrete values
   - Formulas with exact math
   - Complete enumerations (no "such as")
   - REQ IDs for every testable behavior (format: `REQ-SYSTEM-NNN`)
   - Edge cases at boundaries
6. **Present section summary** — show key decisions, REQ IDs, and ask for approval
7. **HITL gate** — user approves, requests changes, or wants more discovery
8. **Save section** — write to `docs/game-design/sections/NN-name.md`
9. **Update index** — mark section complete in `docs/game-design/index.md`
10. **Update state** — add section number to `gdd_sections_complete`

### Partial Save (on pause)

If user stops mid-section:
1. Save to `docs/game-design/sections/NN-name.partial.md`
2. Include `## Discovery Progress` block with answered/remaining questions
3. Update state with section in `gdd_sections_in_progress`
4. On resume: read partial file, continue from last unanswered question

### Section Revision

If user wants to revise a completed section:
1. Copy current to `docs/game-design/history/NN-name.vN.md`
2. Walk through only changed aspects (not full re-discovery)
3. Update REQ IDs if behavior changed (add `.vN` suffix)
4. Save updated section, log change in `history/changelog.md`

## Output

- `docs/game-design/sections/NN-name.md` per completed section
- Updated `docs/game-design/index.md` with completion status
- Updated state file with sections complete/in-progress

## Verification

- [ ] Each section has data tables with concrete values
- [ ] Each section has formulas (where applicable)
- [ ] Each section has complete enumerations
- [ ] Each section has REQ IDs for every testable behavior
- [ ] Each section has edge cases documented
- [ ] User approved each section at HITL gate
- [ ] No `.partial.md` files remain for completed sections
- [ ] `index.md` reflects current completion status

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Section too vague | No data tables, only descriptions | Re-read gdd-reference for calibration, ask specific follow-up questions |
| User overwhelmed | Too many questions, disengagement | Offer to use defaults based on genre, reduce question depth |
| Missing REQ IDs | Section generated without REQ IDs | Scan for testable behaviors, assign REQ IDs retroactively |
| Context window filling | Many sections in one session | Save progress, suggest continuing next session |

## Example

**Section: Rules/Mechanics — Combat**

Q1: "Is combat turn-based or real-time? For a 4X game, I recommend turn-based — it allows more strategic depth and is simpler to implement. Real-time adds complexity with timing and balance."
→ User: "Turn-based"

Q2: "What's your damage model? Options:
- **Strength ratio** (Civ-style): `damage = base * (attacker/defender) * modifiers`. Simple, predictable.
- **Dice-based** (D&D-style): `damage = roll(NdM) + bonus`. More variance, exciting but swingy.
- **Fixed damage** (Chess-style): attacking piece always wins. Simplest, purely positional.
I recommend strength ratio for a 4X — it rewards smart army composition."
→ User: "Strength ratio"

**Generated section excerpt:**
```markdown
## 5.1 Combat Resolution
damage = base_damage * (attacker_strength / defender_strength) * modifier_product

### Modifiers
| Modifier | Value | Stacks |
|----------|-------|--------|
| Terrain (forest/hill) | +25% defender | No |
| Fortified (1 turn) | +25% defender | No |
| City walls | +50% defender | No |
| Flanking | +10% per adjacent ally | Yes (max 3) |

REQ-COMBAT-001: Damage = base * (atk_str / def_str) * modifier_product
REQ-COMBAT-002: Terrain modifier applies +25% to defender in forest/hill
REQ-COMBAT-003: Flanking bonus caps at +30% (3 adjacent allies)
```
