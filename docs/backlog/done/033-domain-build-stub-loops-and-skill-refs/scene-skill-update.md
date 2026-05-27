# Scene SKILL.md — Contract Table Update

## Status
EXISTS — needs enhancement

## Location
`.claude/skills/scene/SKILL.md`

## What
Scene SKILL.md currently lists only 2 contracts in its Contracts table (scene-action-contract, scene-outcome-contract). Two additional contracts exist in the contracts folder but aren't referenced: scene-dispatch-contract and scene-encounter-types.

## Current Contracts Table
```
| Contract | File |
|----------|------|
| Input | → [[contracts/scene-action-contract.json]] |
| Output | → [[contracts/scene-outcome-contract.json]] |
```

## Updated Contracts Table
```
| Contract | File |
|----------|------|
| Input | → [[contracts/scene-action-contract.json]] |
| Output | → [[contracts/scene-outcome-contract.json]] |
| Dispatch | → [[contracts/scene-dispatch-contract.json]] |
| Encounter Types | → [[contracts/scene-encounter-types.json]] |
```

## Also Update
- Change 7 Encounter Types table: update social, merchant, travel, item-use from "stub" to "built" with links to new SKILL.md files
