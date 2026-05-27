# Combat Loop — Gate Contract

## Gates

| Gate ID | Description | Method | Check |
|---------|-------------|--------|-------|
| BUILD-01 | Combat loop contract exists | file_exists | `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-loop-contract.json` |
| BUILD-02 | Combat state contract exists | file_exists | `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-state-contract.json` |
| BUILD-03 | Combat action contract exists | file_exists | `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-action-contract.json` |
| BUILD-04 | Combat SKILL.md exists | file_exists | `projects/ai-dnd-game/.claude/skills/combat/SKILL.md` |
| TEST-01 | All contracts valid JSON | run_code | `python3 -c "import json; [json.load(open(f'projects/ai-dnd-game/.claude/skills/combat/contracts/{c}')) for c in ['combat-loop-contract.json','combat-state-contract.json','combat-action-contract.json']]"` |
