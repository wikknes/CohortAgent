# CohortAgent Cookbook

This cookbook provides detailed information on how CohortAgent works, including how to run the code, available functions, customization options, and editing mechanisms.

## Table of Contents

1. [How CohortAgent Works](#how-cohortagent-works)
2. [Installation and Setup](#installation-and-setup)
3. [Running the Code](#running-the-code)
4. [Available Functions](#available-functions)
5. [Customization Options](#customization-options)
6. [Editing and Extending](#editing-and-extending)
7. [Example Workflows](#example-workflows)

## How CohortAgent Works

CohortAgent is a multimodal agent designed to process and analyze health data locally, ensuring privacy and security of sensitive information. The agent is built using:

1. **Google's Agent Development Kit (ADK)**: Provides the framework for building the agent with tools and capabilities
2. **Local Multimodal Model (LLaVA via Ollama)**: Processes both text and image data without requiring internet access
3. **Custom Tools**: Performs data analysis, visualization, and image processing

### Architecture

![CohortAgent Architecture (conceptual diagram)]

The key components of CohortAgent are:

1. **LLM Agent**: The core agent built with ADK, using a local LLaVA model for inference
2. **Custom Tools**: A suite of Python functions for data processing, analysis, and visualization
3. **Data Handlers**: Utilities to load, process, and merge multiple data types
4. **Command Line Interface**: For easy interaction with the agent

All processing happens locally, ensuring that sensitive health data never leaves your system.

## Installation and Setup

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/download) for local model inference

### Installation Steps

1. **Clone the repository and create a virtual environment**:

```bash
git clone https://github.com/your-username/CohortAgent.git
cd CohortAgent
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate.bat
```

2. **Install the package and dependencies**:

```bash
pip install -e .
```

3. **Install Ollama from [ollama.ai/download](https://ollama.ai/download)**

4. **Pull the LLaVA model**:

```bash
ollama pull llava
```

5. **Start the Ollama server**:
   - The Ollama server should start automatically on installation
   - It typically runs at http://localhost:11434

## Running the Code

### Command Line Interface

CohortAgent provides a command-line interface for easy interaction:

```bash
# Run with a direct query
cohortagent --query "Analyze the correlation between lifestyle and biochemistry data"

# Interactive mode
cohortagent --interactive

# Specify custom data directories
cohortagent --data-dir /path/to/data --scan-dir /path/to/scans --output-dir /path/to/output

# Use a different local model
cohortagent --model "ollama/llama2"
```

### Python API

You can also use CohortAgent directly in your Python code:

```python
from src.agent import CohortAgent

# Initialize the agent
agent = CohortAgent(model_name="ollama/llava")

# Run a query
response = agent.run("Analyze the relationship between lifestyle and proteomics data")
print(response)
```

## Available Functions

CohortAgent includes several built-in tools for data analysis and visualization:

### Data Analysis Tools

1. **analyze_data**: Perform statistical analysis on a single dataset
   ```python
   # Basic summary statistics
   analyze_data(file_path="data/lifestyle.csv", analysis_type="summary")
   
   # Correlation analysis
   analyze_data(file_path="data/biochemistry.csv", analysis_type="correlation")
   
   # Distribution analysis
   analyze_data(
       file_path="data/biochemistry.csv", 
       analysis_type="distribution",
       columns=["glucose_mg_dl", "cholesterol_total_mg_dl"]
   )
   
   # Regression analysis
   analyze_data(
       file_path="data/lifestyle.csv", 
       analysis_type="regression",
       columns=["exercise_hours_per_week", "sleep_hours_per_day"]
   )
   
   # T-test analysis
   analyze_data(
       file_path="data/biochemistry.csv", 
       analysis_type="ttest",
       columns=["glucose_mg_dl", "cholesterol_total_mg_dl"]
   )
   
   # ANOVA analysis
   analyze_data(
       file_path="data/lifestyle.csv", 
       analysis_type="anova",
       columns=["exercise_hours_per_week"],
       groupby="gender"
   )
   
   # Group-based summary statistics
   analyze_data(
       file_path="data/biochemistry.csv", 
       analysis_type="summary",
       groupby="gender"
   )
   ```

2. **merge_and_analyze**: Merge multiple datasets and perform analysis
   ```python
   # Basic correlation analysis with merged data
   merge_and_analyze(
       file_paths=["data/lifestyle.csv", "data/biochemistry.csv"],
       analysis_type="correlation",
       merge_on="patient_id"
   )
   
   # Advanced regression analysis on merged data
   merge_and_analyze(
       file_paths=["data/lifestyle.csv", "data/biochemistry.csv"],
       analysis_type="regression",
       columns=["exercise_hours_per_week", "glucose_mg_dl"],
       merge_on="patient_id"
   )
   
   # Group-based analysis on merged data
   merge_and_analyze(
       file_paths=["data/lifestyle.csv", "data/biochemistry.csv"],
       analysis_type="summary",
       merge_on="patient_id",
       groupby="gender"
   )
   ```

### Visualization Tools

1. **visualize_data**: Generate visualizations from a single dataset
   ```python
   # Basic histogram
   visualize_data(
       file_path="data/biochemistry.csv",
       plot_type="histogram",
       columns=["glucose_mg_dl", "cholesterol_total_mg_dl"],
       output_path="output/biochem_hist.png"
   )
   
   # Scatter plot
   visualize_data(
       file_path="data/lifestyle.csv",
       plot_type="scatter",
       columns=["exercise_hours_per_week", "sleep_hours_per_day"],
       output_path="output/lifestyle_scatter.png",
       title="Exercise vs Sleep Hours"
   )
   
   # Correlation heatmap
   visualize_data(
       file_path="data/biochemistry.csv",
       plot_type="heatmap",
       output_path="output/biochem_heatmap.png"
   )
   
   # Box plot with grouping
   visualize_data(
       file_path="data/biochemistry.csv",
       plot_type="box",
       columns=["glucose_mg_dl", "cholesterol_total_mg_dl"],
       groupby="gender",
       output_path="output/biochem_box.png"
   )
   
   # Violin plot
   visualize_data(
       file_path="data/biochemistry.csv",
       plot_type="violin",
       columns=["glucose_mg_dl"],
       groupby="gender",
       output_path="output/glucose_violin.png",
       palette="Set2"
   )
   
   # Pair plot
   visualize_data(
       file_path="data/lifestyle.csv",
       plot_type="pair",
       columns=["exercise_hours_per_week", "sleep_hours_per_day", "stress_level"],
       groupby="gender",
       output_path="output/lifestyle_pair.png"
   )
   
   # Regression plot with equation
   visualize_data(
       file_path="data/lifestyle.csv",
       plot_type="regression",
       columns=["exercise_hours_per_week", "stress_level"],
       output_path="output/exercise_stress_regression.png",
       title="Impact of Exercise on Stress"
   )
   ```

2. **merge_and_visualize**: Merge multiple datasets and create visualization
   ```python
   # Scatter plot of merged data
   merge_and_visualize(
       file_paths=["data/lifestyle.csv", "data/biochemistry.csv"],
       plot_type="scatter",
       columns=["exercise_hours_per_week", "glucose_mg_dl"],
       merge_on="patient_id",
       output_path="output/exercise_glucose.png",
       title="Impact of Exercise on Blood Glucose"
   )
   
   # Advanced heatmap with clustering
   merge_and_visualize(
       file_paths=["data/lifestyle.csv", "data/biochemistry.csv"],
       plot_type="clustermap",
       merge_on="patient_id",
       output_path="output/lifestyle_biochem_clusters.png"
   )
   
   # Grouped box plots
   merge_and_visualize(
       file_paths=["data/lifestyle.csv", "data/biochemistry.csv"],
       plot_type="box",
       columns=["glucose_mg_dl", "cholesterol_total_mg_dl"],
       merge_on="patient_id",
       groupby="gender",
       output_path="output/grouped_biochem_box.png"
   )
   
   # Joint plot
   merge_and_visualize(
       file_paths=["data/lifestyle.csv", "data/biochemistry.csv"],
       plot_type="joint",
       columns=["exercise_hours_per_week", "glucose_mg_dl"],
       merge_on="patient_id",
       output_path="output/exercise_glucose_joint.png"
   )
   ```

### Image Analysis Tools

1. **analyze_images**: Process and analyze medical images
   ```python
   analyze_images(image_paths=["scans/patient1_mri.jpg", "scans/patient2_mri.jpg"])
   ```

## Customization Options

CohortAgent is designed to be customizable to fit different health data analysis needs. Here are the main customization options:

### 1. Changing the Local Model

You can use any multimodal model available in Ollama:

```python
agent = CohortAgent(model_name="ollama/bakllava")  # Use Bakllava instead of LLaVA
```

### 2. Adding Custom Tools

You can extend CohortAgent with your own custom tools by following these steps:

1. **Define a new tool function** in `src/tools.py`
2. **Register the tool** in the `CohortAgent` class in `src/agent.py`:

```python
# Example of adding a custom tool
from google.adk.tools import Tool

# In the __init__ method of CohortAgent
self.tools.append(
    Tool(
        name="my_custom_tool",
        description="Description of what my tool does",
        function=my_custom_tool_function,
        parameters={
            "param1": "string",
            "param2": "integer"
        }
    )
)
```

### 3. Customizing Visualizations

You can customize the default visualization styles by editing the visualization functions in `src/tools.py`. For example:

```python
# In visualize_data function
plt.figure(figsize=(14, 8))  # Change figure size
plt.style.use('seaborn-dark')  # Use a different style
```

## Editing and Extending

CohortAgent is designed to be easily extended with new capabilities. Here are some common ways to modify and extend the agent:

### Adding Support for New Data Types

1. **Create a new data loader** in `src/utils.py`:
   ```python
   def load_json(file_path):
       """Load data from a JSON file."""
       import json
       with open(file_path, 'r') as f:
           return json.load(f)
   ```

2. **Create tools that use the new data loader** in `src/tools.py`
3. **Register the new tools** in the `CohortAgent` class

### Implementing New Analysis Methods

1. **Add new analysis functions** to `src/tools.py`:
   ```python
   def perform_pca(file_path, n_components=2, output_path="output/pca.png"):
       """Perform Principal Component Analysis and plot results."""
       from sklearn.decomposition import PCA
       import matplotlib.pyplot as plt
       
       data = load_csv(file_path)
       # Preprocess data...
       pca = PCA(n_components=n_components)
       pca_result = pca.fit_transform(data)
       
       # Plot results
       plt.figure(figsize=(10, 8))
       plt.scatter(pca_result[:, 0], pca_result[:, 1])
       plt.xlabel('PC1')
       plt.ylabel('PC2')
       plt.title('PCA Result')
       
       return save_plot(output_path)
   ```

2. **Register the new analysis tool** in the `CohortAgent` class

### Using a Different Local Model Provider

If you want to use a different model provider instead of Ollama:

1. **Update the model initialization** in `src/agent.py`:
   ```python
   # Example for using a different local model provider
   from google.adk.models import LiteLlm
   
   # In the CohortAgent.__init__ method:
   self.model = LiteLlm(model="replicate/llava-13b")  # Or any other provider
   ```

## Example Workflows

Here are some example workflows to demonstrate how to use CohortAgent effectively:

### Example 1: Basic Statistical Analysis

```python
# Initialize the agent
from src.agent import CohortAgent
agent = CohortAgent()

# Run a query for basic analysis
response = agent.run("Give me a statistical summary of the lifestyle data")
print(response)
```

### Example 2: Finding Correlations Between Datasets

```bash
# Using the command line interface
cohortagent --query "Analyze the correlation between exercise hours and glucose levels, then visualize it"
```

### Example 3: Complex Multi-Step Analysis

For complex analyses that require multiple steps, you can provide detailed instructions:

```bash
cohortagent --query "First analyze the relationship between lifestyle factors and proteomics data. Then identify key lifestyle factors that correlate with protein_3 levels. Finally, create a visualization showing these relationships."
```

### Example 4: Working with Image Data

To analyze medical images along with tabular data:

```bash
cohortagent --query "Look at the MRI scans in the scans directory and tell me if there are any abnormalities. Then correlate these findings with the patient's biochemistry data."
```

### Example 5: Custom Analysis Script

You can also create custom scripts that use CohortAgent for specific analyses:

```python
# custom_analysis.py
from src.agent import CohortAgent
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the agent
agent = CohortAgent()

# Step 1: Get statistical summary
summary_response = agent.run("Give me a statistical summary of the biochemistry data")
print("Summary:\n", summary_response)

# Step 2: Ask for specific correlations
correlation_response = agent.run("What lifestyle factors correlate most strongly with glucose levels?")
print("\nCorrelations:\n", correlation_response)

# Step 3: Generate visualizations
visualization_response = agent.run("Create a scatter plot of exercise hours vs glucose levels")
print("\nVisualization generated:", visualization_response)

# You can then add your own custom post-processing here...
```

## Performance Considerations

When working with large datasets (e.g., high-dimensional omics data), consider:

1. **Memory Management**: Load data in chunks when dealing with very large files
2. **Visualization Optimization**: Limit the number of features in visualizations
3. **Model Selection**: Choose a smaller multimodal model if performance is an issue

---

For more information or to report issues, please visit the [GitHub repository](https://github.com/your-username/CohortAgent).
