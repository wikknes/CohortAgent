
import os
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Import the GUI main function
from src.gui import main

if __name__ == "__main__":
    main()
