#!/bin/bash
#
# D&D Game Engine - Real Pipeline Executor
# Actually invokes /kernel/execute-pipeline via claude -p subprocess
# Designed to run as background process
#

REPO="/d/my_ai_projects/project_test_repos/game-dev"
LOG_DIR="$REPO/.claude/logs"
LOG_FILE="$LOG_DIR/dnd-pipeline-real-execution.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# All 19 backlog items (relative to repo root)
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

{
  echo "======================================================================"
  echo "D&D GAME ENGINE - REAL PIPELINE EXECUTOR"
  echo "Start time: $(date)"
  echo "Repository: $REPO"
  echo "======================================================================"
  echo ""

  completed=0
  failed=0

  for i in "${!ITEMS[@]}"; do
    item="${ITEMS[$i]}"
    item_num=$((i+1))
    item_name=$(basename "$(dirname "$item")" | sed 's/.*-//')
    item_short=$(echo "$item" | grep -o '[0-9][0-9][0-9]-' | head -1 | sed 's/-//')

    echo "[$item_num/19] Processing: Item $item_short"
    echo "  Path: $item"

    # Verify backlog file exists in the repo
    if [ ! -f "$REPO/$item" ]; then
      echo "  [FAIL] Backlog file not found"
      ((failed++))
      continue
    fi

    echo "  [OK] Backlog file verified"

    # EXECUTE PIPELINE via subprocess
    # Pattern: cd [repo] && env -u CLAUDECODE claude -p "[command]"
    # The cd inside the background subprocess is safe - doesn't affect parent cwd

    echo "  Executing: /kernel/execute-pipeline $item"

    output=$(cd "$REPO" && env -u CLAUDECODE claude -p "/kernel/execute-pipeline $item" 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
      echo "  [OK] Pipeline completed successfully"
      echo "  Output (first 500 chars): ${output:0:500}"
      ((completed++))
    else
      echo "  [FAIL] Pipeline failed with exit code $exit_code"
      echo "  Error: ${output:0:200}"
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
  echo "Success rate: $(echo "scale=1; $completed * 100 / ${#ITEMS[@]}" | bc)%"
  echo "End time: $(date)"
  echo ""

  if [ $failed -eq 0 ]; then
    echo "[SUCCESS] All 19 items processed through full pipeline"
    exit 0
  else
    echo "[PARTIAL] $failed items failed processing"
    exit 1
  fi

} | tee -a "$LOG_FILE"

exit_status=${PIPESTATUS[0]}
echo "" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"
exit $exit_status
