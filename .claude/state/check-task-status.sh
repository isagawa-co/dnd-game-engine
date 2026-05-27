#!/bin/bash
REPO="/d/my_ai_projects/project_test_repos/game-dev"
TASK_FOLDER="$1"

if [ -z "$TASK_FOLDER" ]; then
  echo "Usage: check-task-status.sh <task_folder>"
  exit 1
fi

cd "$REPO"
python3 << 'PYEOF'
import json
import sys
from pathlib import Path

task_folder = sys.argv[1]
state_file = Path(".claude/state/game-engine_workflow.json")

if not state_file.exists():
  print("incomplete")
  sys.exit(0)

state = json.loads(state_file.read_text())
total = state.get("total_tasks", 0)
completed = len(state.get("completed_tasks", []))
skipped = len(state.get("skipped_tasks", []))

if total > 0 and (completed + skipped) >= total:
  print("complete")
else:
  print("incomplete")
PYEOF
