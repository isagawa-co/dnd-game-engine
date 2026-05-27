# Gate Contract — D&D Content System

## Gates

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| BUILD-01 | monster-schema.json exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/contracts/monster-schema.json` | Create file |
| BUILD-02 | spell-schema.json exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/contracts/spell-schema.json` | Create file |
| BUILD-03 | item-schema.json exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/contracts/item-schema.json` | Create file |
| BUILD-04 | class-schema.json exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/contracts/class-schema.json` | Create file |
| BUILD-05 | race-schema.json exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/contracts/race-schema.json` | Create file |
| BUILD-06 | condition-schema.json exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/contracts/condition-schema.json` | Create file |
| BUILD-07 | catalog.json exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/catalog.json` | Create file |
| BUILD-08 | SKILL.md exists | file_exists | `test -f projects/ai-dnd-game/.claude/skills/content/SKILL.md` | Create file |
| BUILD-09 | pack manifest exists | file_exists | `test -f projects/ai-dnd-game/content/lost-mine-phandelver/manifest.json` | Create file |
| BUILD-10 | 24 monster files exist | run_code | `ls projects/ai-dnd-game/content/lost-mine-phandelver/monsters/*.json \| wc -l` returns 24 | Create missing files |
| BUILD-11 | 3 spell files exist | run_code | `ls projects/ai-dnd-game/content/lost-mine-phandelver/spells/*.json \| wc -l` returns 3 | Create missing files |
| BUILD-12 | 18 item files exist | run_code | `ls projects/ai-dnd-game/content/lost-mine-phandelver/items/*.json \| wc -l` returns 18 | Create missing files |
| FUNC-01 | All schemas valid JSON | run_code | `python -c "import json, glob; [json.load(open(f)) for f in glob.glob('projects/ai-dnd-game/.claude/skills/content/contracts/*.json')]"` exits 0 | Fix JSON |
| FUNC-02 | catalog.json valid JSON | run_code | `python -c "import json; json.load(open('projects/ai-dnd-game/.claude/skills/content/catalog.json'))"` exits 0 | Fix JSON |
| FUNC-03 | manifest.json valid JSON | run_code | `python -c "import json; json.load(open('projects/ai-dnd-game/content/lost-mine-phandelver/manifest.json'))"` exits 0 | Fix JSON |
| FUNC-04 | All monster files valid JSON | run_code | All monster .json files parse without error | Fix JSON |
| FUNC-05 | All spell files valid JSON | run_code | All spell .json files parse without error | Fix JSON |
| FUNC-06 | All item files valid JSON | run_code | All item .json files parse without error | Fix JSON |
| FUNC-07 | Monster files have required fields | run_code | All monsters have id, name, armor_class, hp, ability_scores, speed, challenge | Add missing fields |
| FUNC-08 | Manifest counts match catalog | run_code | catalog content_count matches manifest array lengths | Fix counts |
| TEST-01 | All content validates against schemas | run_test | Validation script exits 0 | Fix non-conforming files |

## Requirements Coverage
Each gate maps to task acceptance criteria. All 18 tasks covered.
