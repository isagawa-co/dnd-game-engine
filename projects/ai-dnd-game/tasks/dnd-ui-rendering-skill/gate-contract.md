# Gate Contract — UI Rendering Skill

## Gates

| Gate ID | Task | Check | Method |
|---------|------|-------|--------|
| SKILL-001 | 001 | SKILL.md exists | `file_exists: projects/ai-dnd-game/.claude/skills/ui-rendering/SKILL.md` |
| CONTRACT-001 | 002 | character-sheet-contract.json exists | `file_exists: projects/ai-dnd-game/.claude/skills/ui-rendering/contracts/character-sheet-contract.json` |
| CONTRACT-002 | 003 | combat-round-contract.json exists | `file_exists: projects/ai-dnd-game/.claude/skills/ui-rendering/contracts/combat-round-contract.json` |
| CONTRACT-003 | 004 | encounter-contract.json exists | `file_exists: projects/ai-dnd-game/.claude/skills/ui-rendering/contracts/encounter-contract.json` |
| CONTRACT-004 | 005 | inventory-contract.json exists | `file_exists: projects/ai-dnd-game/.claude/skills/ui-rendering/contracts/inventory-contract.json` |
| IMPL-001 | 006 | __init__.py exports render functions | `grep: "render_character_sheet" projects/ai-dnd-game/src/ui_rendering/__init__.py` |
| IMPL-002 | 007 | character_sheet.py exists | `file_exists: projects/ai-dnd-game/src/ui_rendering/character_sheet.py` |
| IMPL-003 | 008 | combat_round.py exists | `file_exists: projects/ai-dnd-game/src/ui_rendering/combat_round.py` |
| IMPL-004 | 009 | encounter.py exists | `file_exists: projects/ai-dnd-game/src/ui_rendering/encounter.py` |
| IMPL-005 | 010 | inventory.py exists | `file_exists: projects/ai-dnd-game/src/ui_rendering/inventory.py` |
| TEST-001 | 011 | Tests pass (5+ tests) | `run_test: python -m pytest projects/ai-dnd-game/tests/test_ui_rendering.py -v` |
