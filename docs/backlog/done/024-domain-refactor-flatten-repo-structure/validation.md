# Validation

## Status
NEW

## Post-Restructure Verification Checklist

### 1. Zero Stale References
```bash
grep -r "projects/ai-dnd-game" . --include="*.md" --include="*.json" | grep -v ".git/"
```
Expected: zero results.

### 2. Directory Structure Correct
```
campaigns/          exists, contains campaign-2026-05-27-001/, campaign-2026-05-27-002/
content/            exists, contains all-races.json, all-classes.json, lost-mine-phandelver/
contracts/          exists, contains state-evaluation-contract.json
config/             exists (or created)
tasks/              exists, contains dnd-* folders + completed/
characters/         does NOT exist yet (created by 025)
projects/           does NOT exist
_test/              does NOT exist
```

### 3. JSON Validity
All `.json` files parse without error:
```bash
find . -name "*.json" -not -path "./.git/*" -exec python -c "import json; json.load(open('{}'))" \;
```

### 4. Skill References Resolve
Each skill's referenced contract/registry path exists at the new location.

### 5. Game Commands Work
- `/game-play` can find campaign state at `campaigns/`
- Character creation loop can find registries at `content/all-races.json`, `content/all-classes.json`
- State evaluation contract found at `contracts/state-evaluation-contract.json`
