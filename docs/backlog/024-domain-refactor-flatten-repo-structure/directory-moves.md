# Directory Moves

## Status
NEW

## Operations

Execute in order:

| Step | Source | Destination | Notes |
|------|--------|-------------|-------|
| 1 | `projects/ai-dnd-game/campaigns/` | `campaigns/` | 2 campaigns inside |
| 2 | `projects/ai-dnd-game/content/` | `content/` | all-races.json, all-classes.json, lost-mine-phandelver/ |
| 3 | `projects/ai-dnd-game/contracts/` | `contracts/` | state-evaluation-contract.json |
| 4 | `projects/ai-dnd-game/config/` | `config/` | player-settings.json (create dir if missing) |
| 5 | `projects/ai-dnd-game/tasks/` | `tasks/` | All dnd-* task folders + completed/ |
| 6 | Remove `projects/` | — | Empty after moves |
| 7 | Remove `_test/` | — | Empty directory, unused |

## Git Commands

```bash
git mv projects/ai-dnd-game/campaigns campaigns
git mv projects/ai-dnd-game/content content
git mv projects/ai-dnd-game/contracts contracts
git mv projects/ai-dnd-game/tasks tasks
# config may need mkdir + mv if it doesn't exist yet
rm -rf projects/
rm -rf _test/
```

## Dependencies
- Must complete BEFORE path-reference-updates (paths need to exist at new locations)
- Must complete BEFORE 025 (character pool) since it creates `characters/` at root
