#!/usr/bin/env python3
"""
Direct launcher for the CohortAgent GUI.
This can be run directly without the CLI wrapper.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Import the GUI
from src.gui import main

if __name__ == "__main__":
    # Set default environment variables
    os.environ.setdefault("MODEL_NAME", "ollama/llava")
    os.environ.setdefault("DATA_DIR", "./data")
    os.environ.setdefault("SCAN_DIR", "./scans")
    os.environ.setdefault("OUTPUT_DIR", "./output")
    
    # Run the GUI
    main()