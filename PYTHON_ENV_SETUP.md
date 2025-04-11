# Python Environment Setup for CohortAgent Testing

## Prerequisites
- Python 3.6+
- pip (Python package installer)

## Setting Up the Environment

### 1. Create a Virtual Environment

```bash
# Create a virtual environment named .venv
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### 3. Verify Installation

Ensure all dependencies are correctly installed by checking:

```bash
pip list
```

You should see all the required packages installed:
- google-adk
- litellm
- pandas
- matplotlib
- seaborn
- pillow (PIL)
- numpy
- scipy
- scikit-learn

### 4. Running Tests

```bash
# To run tool-specific tests
python test_tools.py

# To run agent interface tests
python test_agent.py
```

### Troubleshooting

If you encounter the error `ModuleNotFoundError: No module named 'seaborn'` or similar:

1. Make sure your virtual environment is activated
2. Reinstall the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For specific missing modules, install them directly:
   ```bash
   pip install seaborn
   pip install matplotlib
   # etc.
   ```

### Cleaning Up

When you're done testing, deactivate the virtual environment:

```bash
deactivate
```