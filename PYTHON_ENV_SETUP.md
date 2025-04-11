# Python Environment Setup for CohortAgent Testing

## Prerequisites
- Python 3.6+
- pip (Python package installer)
- Ollama (for local LLM deployment)

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

### 3. Set Up Ollama for Local Multimodal LLM

```bash
# Install Ollama
# Download from https://ollama.ai/download

# Pull the LLaVA model (required for image processing functionality)
ollama pull llava

# Verify Ollama is running
# Ollama should run as a service on http://localhost:11434
```

### 4. Verify Installation

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

### 5. Running Tests

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

If you have issues with the LLM functionality:

1. Verify Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```
2. Check that the LLaVA model is properly installed:
   ```bash
   ollama list
   ```
3. If needed, restart the Ollama service

### Cleaning Up

When you're done testing, deactivate the virtual environment:

```bash
deactivate
```