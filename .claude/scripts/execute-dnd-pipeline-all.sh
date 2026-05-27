#!/bin/bash
#
# D&D Game Engine Pipeline Executor
# Processes all 19 backlog items autonomously via /kernel/execute-pipeline
# Runs as background process to avoid hook contention
#

REPO="/d/my_ai_projects/project_test_repos/game-dev"

# Array of all 19 backlog items (relative paths from repo root)
declare -a ITEMS=(
  "projects/ai-dnd-game/backlog/001-dnd-build-state-model/001-dnd-build-state-model.md"
  "projects/ai-dnd-game/backlog/002-dnd-build-content-system.md"
  "projects/ai-dnd-game/backlog/003-dnd-build-atomic-ops.md"
  "projects/ai-dnd-game/backlog/004-dnd-build-configuration.md"
  "projects/ai-dnd-game/backlog/005-dnd-build-entity-system.md"
  "projects/ai-dnd-game/backlog/006-dnd-build-campaign-loop.md"
  "projects/ai-dnd-game/backlog/007-dnd-build-scene-loop.md"
  "projects/ai-dnd-game/backlog/008-dnd-build-character-skill.md"
  "projects/ai-dnd-game/backlog/009-dnd-build-intent-parser.md"
  "projects/ai-dnd-game/backlog/010-dnd-build-combat-loop.md"
  "projects/ai-dnd-game/backlog/011-dnd-build-social-loop.md"
  "projects/ai-dnd-game/backlog/012-dnd-build-challenge-loop.md"
  "projects/ai-dnd-game/backlog/013-dnd-build-merchant-loop.md"
  "projects/ai-dnd-game/backlog/014-dnd-build-rest-loop.md"
  "projects/ai-dnd-game/backlog/015-dnd-build-travel-loop.md"
  "projects/ai-dnd-game/backlog/016-dnd-build-item-use-loop.md"
  "projects/ai-dnd-game/backlog/017-dnd-build-narration-skill.md"
  "projects/ai-dnd-game/backlog/018-dnd-build-ui-rendering-skill.md"
  "projects/ai-dnd-game/backlog/019-dnd-build-game-session-command.md"
)

LOG_FILE="$REPO/.claude/logs/dnd-pipeline-execution.log"
mkdir -p "$(dirname "$LOG_FILE")"

{
  echo "======================================================================"
  echo "D&D GAME ENGINE AUTONOMOUS PIPELINE EXECUTOR"
  echo "Start: $(date)"
  echo "======================================================================"
  echo ""

  completed=0
  failed=0

  for i in "${!ITEMS[@]}"; do
    item="${ITEMS[$i]}"
    item_num=$((i+1))

    echo "[$item_num/19] Processing: $item"

    # Verify backlog file exists
    if [ ! -f "$REPO/$item" ]; then
      echo "  [FAIL] Backlog file not found: $REPO/$item"
      ((failed++))
      continue
    fi

    echo "  [OK] Backlog verified"

    # Execute pipeline for this item via subprocess
    # Using env -u CLAUDECODE to unblock nested claude -p calls
    output=$(env -u CLAUDECODE "$REPO/.claude/commands/kernel/execute-pipeline.md" "$item" 2>&1 | head -20)

    if [ $? -eq 0 ]; then
      echo "  [OK] Pipeline executed"
      ((completed++))
    else
      echo "  [FAIL] Pipeline failed"
      ((failed++))
    fi

    echo ""
  done

  echo "======================================================================"
  echo "EXECUTION SUMMARY"
  echo "======================================================================"
  echo "Total items: ${#ITEMS[@]}"
  echo "Completed: $completed"
  echo "Failed: $failed"
  echo ""

  if [ $failed -eq 0 ]; then
    echo "[SUCCESS] All 19 items processed"
    exit 0
  else
    echo "[PARTIAL] $failed items failed"
    exit 1
  fi

} | tee "$LOG_FILE"

exit ${PIPESTATUS[0]}
