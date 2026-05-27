---
name: game-create
type: command
domain: game-engine
kernel_loop: true
---

# /game-create

Guided GDD creation — turn a game idea into a complete Game Design Document through collaborative discovery.

## Kernel Loop Integration

```
/kernel/anchor -> this command -> /kernel/complete
```

## Instructions

1. **Read skill files:**
   - `.claude/skills/game-engine/SKILL.md`
   - `.claude/skills/game-engine/workflow.md`

2. **Check for existing state:**
   - Read `.claude/state/game_create_state.json`
   - If exists: resume from last position (show progress, pick up where left off)
   - If not: fresh start

3. **Execute Phase 1 steps:**
   - Step 1: Initial Discovery (genre, scope, platform, art style)
   - Step 2: Genre Section Selection (which GDD sections apply)
   - Step 3: GDD Section Walkthrough (per-section discovery + generation)
   - Step 4: GDD Review (completeness check, user approval)

4. **On failure:**
   - Read `steps/on-failure.md` for diagnosis
   - Fix → `/kernel/learn` → retry (max 3)

5. **On completion:**
   - Report: "GDD complete — N sections, M REQ IDs. Run /game-build to start building."
   - `/kernel/complete`

## Usage

```
/game-create
/game-create I want to build a 4X strategy game in the terminal
```

Arguments are optional. If provided, the idea text seeds the initial discovery.
