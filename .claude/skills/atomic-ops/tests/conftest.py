"""Pytest configuration for atomic-ops tests."""

import sys
from pathlib import Path

# Add the parent directory (atomic-ops) to the path so imports work
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
