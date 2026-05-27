#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime

repo_root = Path("D:/my_ai_projects/project_test_repos/game-dev")
tasks_root = repo_root / "tasks"
state_dir = repo_root / ".claude/state"
backlog_root = repo_root / "projects/ai-dnd-game/backlog"

phase4_items = [
    ("018", "narration-system", "narration-framework-and-log.md"),
    ("019", "anti-drift-enforcement", "narration-anti-drift-enforcement.md"),
    ("020", "ui-scene-display", "ui-scene-and-encounter-display.md"),
    ("021", "combat-hud-status", "ui-combat-hud-and-status-display.md"),
]

print("=" * 70)
print("PHASE 4 STATUS CHECK")
print("=" * 70)
print()

for num, folder, backlog_name in phase4_items:
    print(f"Task {num}: {backlog_name}")
    print("-" * 70)
    
    # Check backlog
    backlog_path = backlog_root / f"{num}-{backlog_name}"
    if backlog_path.exists():
        print(f"  ✓ Backlog file exists")
    else:
        print(f"  ✗ Backlog file NOT found")
    
    # Check task folder
    task_folder = tasks_root / folder
    if task_folder.exists():
        print(f"  ✓ Task folder exists: tasks/{folder}/")
        
        # Check key files
        index = task_folder / "000-index.md"
        gate = task_folder / "gate-contract.md"
        
        if index.exists():
            print(f"    ✓ 000-index.md created")
        else:
            print(f"    ✗ 000-index.md NOT created")
            
        if gate.exists():
            print(f"    ✓ gate-contract.md created")
        else:
            print(f"    ✗ gate-contract.md NOT created")
        
        # Count task files
        task_files = list(task_folder.glob("00[1-9]-*.md"))
        if task_files:
            print(f"    ✓ {len(task_files)} task files created")
        else:
            print(f"    ✗ No task files created yet")
    else:
        print(f"  ✗ Task folder does not exist yet")
    
    # Check log files
    iter_logs = list(state_dir.glob(f"{folder}_iteration_*.log"))
    if iter_logs:
        print(f"  ✓ Iteration logs: {len(iter_logs)} file(s)")
        # Get latest and size
        latest = max(iter_logs, key=os.path.getmtime)
        size = latest.stat().st_size
        if size > 0:
            print(f"    └─ Latest: {latest.name} ({size} bytes)")
        else:
            print(f"    └─ Latest: {latest.name} (empty)")
    else:
        print(f"  ✗ No iteration logs found")
    
    print()

print("=" * 70)
print(f"Generated at: {datetime.now().isoformat()}")
print("=" * 70)

