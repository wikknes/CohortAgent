# CohortAgent GUI Quick Start

This guide provides quick setup and usage instructions for the CohortAgent interactive GUI.

## Setup

1. **Install dependencies**:
   ```bash
   # In project root
   pip install -e .
   ```

2. **Verify Streamlit installation**:
   ```bash
   streamlit --version
   ```

## Running the GUI

Choose one method:

**Method 1**: CLI command
```bash
cohortagent --gui
```

**Method 2**: Launcher script
```bash
./launch_gui.sh
```

**Method 3**: Direct execution
```bash
streamlit run run_gui.py
```

Once launched, the GUI will open in your browser. If not, navigate to http://localhost:8501.

## GUI Features

The interface is divided into three tabs:

### 1. Query Tab
- Enter natural language queries
- Example: "Create a scatter plot of age vs. weight from lifestyle data"
- View responses and visualizations

### 2. Data Explorer Tab
- Interactive treemap of available datasets
- Dataset previews with statistics
- Correlation analysis

### 3. Results History Tab
- Browse previously generated outputs
- Download result files
- View visualizations

## Sample Queries

Try these queries to test the GUI:

```
Show me a correlation heatmap of blood biochemistry data
```

```
Create a scatter plot of weight vs. CRP from data/example/blood_biochemistry.csv
```

```
Analyze the relationship between age and BMI in lifestyle data
```

## Customization

Use the sidebar to configure:
- Model selection
- Data, scan, and output directories
- Default visualization types

For full documentation, see [GUI_GUIDE.md](GUI_GUIDE.md).