#!/bin/bash

REPO="D:/my_ai_projects/project_test_repos/game-dev"
TASKS=("narration-system" "anti-drift-enforcement" "ui-scene-display" "combat-hud-status")
LOG_DIR="$REPO/.claude/state"

echo "Phase 4 Execution Monitor"
echo "========================="
echo "Monitoring 4 tasks:"
echo "  1. 018: Narration Framework & Log (narration-system)"
echo "  2. 019: Narration Anti-Drift (anti-drift-enforcement)"
echo "  3. 020: UI Scene & Encounter (ui-scene-display)"
echo "  4. 021: UI Combat HUD (combat-hud-status)"
echo ""

# Check for task folders
for task in "${TASKS[@]}"; do
  if [ -d "$REPO/tasks/$task" ]; then
    echo "[OK] Task folder exists: $task"
    if [ -f "$REPO/tasks/$task/000-index.md" ]; then
      echo "     └─ Index created"
      task_count=$(grep -c "^### " "$REPO/tasks/$task/000-index.md" 2>/dev/null || echo "?")
      echo "     └─ Tasks: $task_count"
    fi
  else
    echo "[..] Task folder pending: $task"
  fi
done

echo ""
echo "Check logs with:"
echo "  tail -f $LOG_DIR/narration-system_iteration_*.log"
echo "  tail -f $LOG_DIR/anti-drift-enforcement_iteration_*.log"
echo "  tail -f $LOG_DIR/ui-scene-display_iteration_*.log"
echo "  tail -f $LOG_DIR/combat-hud-status_iteration_*.log"

