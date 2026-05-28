# Gate Contract — Flatten Repo Structure

## Gates

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| BUILD-01 | campaigns/ at root | file_exists | `test -d campaigns/` | Move directory |
| BUILD-02 | content/ at root | file_exists | `test -d content/` | Move directory |
| BUILD-03 | contracts/ at root | file_exists | `test -d contracts/` | Move directory |
| BUILD-04 | tasks/ at root | file_exists | `test -d tasks/` | Move directory |
| BUILD-05 | projects/ removed | run_code | `! test -d projects/` | Remove directory |
| BUILD-06 | _test/ removed | run_code | `! test -d _test/` | Remove directory |
| BUILD-07 | CLAUDE.md updated | grep | `! grep -q "projects/ai-dnd-game" CLAUDE.md` | Fix references |
| BUILD-08 | game-play.md updated | grep | `! grep -q "projects/ai-dnd-game" .claude/commands/game-play.md` | Fix references |
| BUILD-09 | char-creation-loop updated | grep | `! grep -q "projects/ai-dnd-game" .claude/skills/character-creation-loop/character-creation-loop.md` | Fix references |
| BUILD-10 | char SKILL.md updated | grep | `! grep -q "projects/ai-dnd-game" .claude/skills/character/SKILL.md` | Fix references |
| BUILD-11 | char contract updated | grep | `! grep -q "projects/ai-dnd-game" .claude/skills/character/contracts/character-creation-contract.json` | Fix references |
| TEST-01 | Zero stale references | run_code | `grep -r "projects/ai-dnd-game" . --include="*.md" --include="*.json" \| grep -v ".git/" \| wc -l` returns 0 | Fix remaining refs |
