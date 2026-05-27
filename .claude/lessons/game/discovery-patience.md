# Discovery Patience

<!-- Seeded: expert knowledge for Phase 1 HITL collaboration -->

## The Problem

Overwhelming users with checklists or multiple questions per turn causes disengagement. Users feel interrogated, not guided. They give shallow answers to finish faster, producing a vague GDD.

## Why It Fails

- Multiple questions per turn → user answers the easy ones, skips the hard ones
- Checklist format → feels like homework, not collaboration
- No suggestions → user doesn't know what good options look like
- No tradeoffs → user makes uninformed decisions that cause problems later

## Correct Approach

**One question at a time.** For each question:
1. **Suggest** 2-3 concrete options with names and descriptions
2. **Recommend** one option and explain why
3. **Show tradeoffs** — what each option gives up
4. **Reference examples** — "Here's how Tiny Civ handles this"
5. **Wait** for the user's answer before asking the next question

**Bad:** "What combat system do you want? What about damage? Modifiers? Turn-based or real-time?"
**Good:** "Is combat turn-based or real-time? For a 4X game, I recommend turn-based — it allows more strategic depth and pairs well with hex grids. Real-time adds excitement but requires careful balance and is harder to implement. What do you prefer?"

The agent is a **collaborator**, not a questionnaire.

## Source

Design principle from backlog 007: design-principles.md (HITL Collaboration Principle)
