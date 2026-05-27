# Requirements Traceability Approach — From Tiny Civ Blog (Part 2)

## The Problem
When a project's code exceeds the context window, the LLM can't reason about the entire project. Design changes (95% due to missing requirements) cause Claude to lose coherence.

## The Solution
Requirements-driven development with traceability from design → requirements → tests → coverage report.

## How It Works

### 1. GDD as Source of Truth
The Game Design Document describes features at a high level. Over time, breaks into smaller documents.

### 2. Requirements Files
Each GDD section decomposes into requirements stored in `/docs/requirements/`:

```markdown
# Turn System

## REQ 1-0100: Game starts in PlayerActions phase
The initial game state has TurnPhase set to PlayerActions.

## REQ 1-0101: Turn advance runs all phases and increments counter
Calling advanceTurnPhase runs through all phases (EndOfTurn, StartOfTurn) and increments the turn counter.

## REQ 1-0102: Turn counter increments on each advance cycle
Each call to advanceTurnPhase increments the turn number by 1.

## REQ 1-0103: Phase returns to PlayerActions after advance
After advanceTurnPhase completes, the turn phase is always PlayerActions.

## REQ 1-0104: Start-of-turn hooks refresh unit movement
Default start-of-turn hooks restore each unit's movementLeft and reset hasMoved to false.

## REQ 1-0105: Custom start-of-turn hooks run in registration order
Multiple start-of-turn hooks execute in the order they were registered.
```

### 3. REQ IDs in Test Names
Tests include the requirement ID they verify:

```typescript
it('should advance through all phases and increment the turn counter [REQ-1-0101]', () => {
  const state = makeState();
  registerDefaultHooks();
  expect(state.turn).toBe(1);

  advanceTurnPhase(state);

  expect(state.turn).toBe(2);
  expect(state.turnPhase).toBe(TurnPhase.PlayerActions);
});
```

### 4. Coverage Report
Script cross-references REQ IDs → test names → pass/fail:

```
✅ REQ 1-0054: Multiple units combine sight coverage
Test    File
FogOfWar — Unit Sight > should combine sight coverage    tests/systems/fogOfWar.test.ts

✅ REQ 1-0055: Visibility calculation filtered by player ID
Test    File
FogOfWar — Unit Sight > should only use units belonging    tests/systems/fogOfWar.test.ts

❌ REQ 1-1200: Three map size presets
No test coverage
```

### 5. Feedback Loop
Coverage report referenced by Claude to address missing requirements — go back, implement, test.

## Key Insight from the Author
> "I may be able to do away with the GDD doc entirely and use the requirements documents as the source of truth. That way I don't have the issue of the GDD file and requirements files diverging over time."

This aligns with the spec factory approach: the GDD + REQ IDs ARE the source of truth. A human-readable summary can be generated, but it's not authoritative.

## How This Maps to the Game Engine Spec
- GDD sections → generate REQ IDs during Phase 1 discovery
- REQ IDs → gate contract rows (1:1 mapping)
- Gate contract rows → test functions with REQ IDs in names
- Coverage script → validates no orphaned REQs or tests
- Phase 2 decomposition is mechanical because REQ IDs are already in the GDD
