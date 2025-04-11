# CohortAgent

A multimodal agent for analyzing health data locally using Google's ADK framework and Ollama's LLaVA model.

## Features

- Processes diverse data types (CSV files, images) locally for privacy
- Performs statistical analysis and visualization of health data
- Maintains data privacy by keeping all operations local
- Handles lifestyle questionnaires, scans, blood biochemistry, and various omics datasets
- Interactive GUI with data visualization and treemap data exploration
- Natural language interface for data analysis and visualization

## Installation

1. Clone this repository
2. Create a virtual environment and install the package:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate.bat
pip install -e .
```

3. Install Ollama from [Ollama's website](https://ollama.ai/download)
4. Pull the LLaVA model:

```bash
ollama pull llava
```

## Usage

### Command Line

```bash
# Run with a direct query
cohortagent --query "Analyze the correlation between lifestyle and biochemistry data"

# Run in interactive CLI mode
cohortagent --interactive

# Launch the interactive GUI dashboard
cohortagent --gui

# Specify custom paths
cohortagent --data-dir /path/to/data --scan-dir /path/to/scans --output-dir /path/to/output
```

### Interactive GUI Dashboard

The GUI provides a rich interface for interacting with the CohortAgent:

- **Query Interface**: Natural language query input with visualization display
- **Data Explorer**: Interactive treemap visualization of available datasets
- **Results History**: Browse and download past analysis results

To launch the GUI:

```bash
# Using the CLI tool
cohortagent --gui

# Or use the provided script
./launch_gui.sh
```

### Python API

```python
from src.agent import CohortAgent

# Initialize the agent
agent = CohortAgent(model_name="ollama/llava")

# Run a query
response = agent.run("Analyze the relationship between lifestyle and proteomics data")
print(response)

# For GUI applications
from src.gui import CohortAgentGUI

# Initialize and run the GUI
gui = CohortAgentGUI(model_name="ollama/llava")
gui.run()  # This starts the Streamlit application
```

## Sample Data

Sample datasets are provided in the `data/sample/` directory:

- `lifestyle.csv`: Lifestyle questionnaire data
- `biochemistry.csv`: Blood biochemistry measurements
- `proteomics.csv`: Proteomics data

## For more information, see the [Cookbook](cookbook.md) for detailed usage examples.
