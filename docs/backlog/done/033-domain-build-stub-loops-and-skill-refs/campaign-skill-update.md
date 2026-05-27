# Campaign SKILL.md — Add Contracts Table

## Status
EXISTS — needs enhancement

## Location
`.claude/skills/campaign/SKILL.md`

## What
Campaign SKILL.md has no Contracts table. Six contracts exist in `.claude/skills/campaign/contracts/` but the skill file doesn't reference them. The agent won't know they exist unless it browses the folder.

## Contracts Table to Add
Add after the "Action Prompt Integration" section:

```
## Contracts

| Contract | File | Purpose |
|----------|------|---------|
| Campaign Loop | → [[contracts/campaign-loop-contract.json]] | 5-tier state hierarchy and loop orchestration |
| Campaign Action | → [[contracts/campaign-action-contract.json]] | Input schema for campaign actions |
| Campaign Outcome | → [[contracts/campaign-outcome-contract.json]] | Output schema for campaign results |
| Arc Progression | → [[contracts/arc-progression-contract.json]] | Arc completion conditions and transitions |
| Session Management | → [[contracts/session-management-contract.json]] | Session save/load/resume contracts |
| State Mutation | → [[contracts/state-mutation-contract.json]] | Atomic state update rules and validation |
```
