# Roll Input Validation

## Status
Open

## Priority
Medium — currently no validation on user-provided dice rolls. User could type 97 for a d20. Trust is fine for casual play but a game engine should enforce bounds.

## Summary
Add validation for user-provided dice rolls. When the agent prompts "roll d20" and the user provides a number, validate it falls within the die's range (1-20 for d20, 1-6 for d6, etc.). Also validate damage rolls against expected dice (e.g. 2d6 should be 2-12). Reject out-of-range values with a clear message.

## Requirements
- Define roll validation rules in a contract (die type → valid range)
- Agent checks user input against expected die type before applying
- Clear error message: "That roll (97) is out of range for a d20 (1-20). Please re-roll."
- Support compound rolls: "4d6 drop lowest" should validate each die is 1-6
- Optional: offer auto-roll mode where agent generates random numbers

## References
- Combat loop: `.claude/skills/combat/SKILL.md`
- Challenge loop: `.claude/skills/challenge/SKILL.md`
- Atomic ops: `.claude/skills/atomic-ops/`

## Task Builder Input
- **Deliverable:** Roll validation contract + skill updates for combat/challenge loops
- **Location:** workspace
- **Scope:** BUILD
- **Constraints:** Must not slow down gameplay — validation should be instant and non-intrusive
