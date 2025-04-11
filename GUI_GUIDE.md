# CohortAgent GUI Guide

This guide provides detailed instructions for using the CohortAgent interactive GUI module.

## Overview

The CohortAgent GUI is a web-based dashboard that provides an intuitive interface for analyzing multimodal health data. It features:

- Natural language query interface
- Interactive data visualizations
- Dataset explorer with treemap visualization
- Results history browser

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/CohortAgent.git
   cd CohortAgent
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   
   # On macOS/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install the package with its dependencies**:
   ```bash
   pip install -e .
   ```

   This will install all required dependencies, including:
   - streamlit (for the GUI)
   - plotly (for interactive visualizations)
   - pandas, numpy, scikit-learn (for data analysis)
   - matplotlib, seaborn (for static visualizations)

4. **Verify installation**:
   ```bash
   # Check that streamlit is installed
   streamlit --version
   ```

## Running the GUI

You have several options to launch the CohortAgent GUI:

### Option 1: Using the CLI Command

The simplest way to launch the GUI:

```bash
cohortagent --gui
```

You can customize the paths for data, scans, and output:

```bash
cohortagent --gui --data-dir path/to/data --scan-dir path/to/scans --output-dir path/to/output
```

### Option 2: Using the Launcher Script

For convenience, a launcher script is provided:

```bash
# Make sure it's executable
chmod +x launch_gui.sh

# Run it
./launch_gui.sh
```

### Option 3: Direct Streamlit Execution

You can also run the GUI directly with Streamlit:

```bash
streamlit run run_gui.py
```

## Using the GUI

Once launched, the GUI will open in your default web browser. If it doesn't open automatically, navigate to the URL shown in the terminal (typically http://localhost:8501).

### GUI Sections

The interface is divided into three main tabs:

#### 1. Query Tab

This is where you can interact with the CohortAgent through natural language queries:

- Enter your query in the text area (e.g., "Create a visualization of weight vs. age from lifestyle data")
- Click "Run Query" to process your request
- View the response and any generated visualizations below

Example queries:
- "Show me a correlation heatmap of blood biochemistry data"
- "Analyze the relationship between weight and C-reactive protein"
- "Create a scatter plot of age vs. BMI from lifestyle data"

#### 2. Data Explorer Tab

This tab provides an interactive way to explore available datasets:

- **Treemap Visualization**: Shows hierarchical view of all datasets with size indicating data volume
- **Dataset Preview**: Select any dataset to see a preview and basic statistics
- **Correlation Analysis**: For numerical data, see correlation heatmaps automatically

Hover over treemap segments to see details about each dataset.

#### 3. Results History Tab

Browse previously generated results:

- View all output files organized by type
- Download any result file
- View generated images directly in the browser

### Configuration

The sidebar provides configuration options:

- **Model Selection**: Choose which model to use for analysis
- **Directory Paths**: Customize data, scan, and output directories
- **Visualization Options**: Set default visualization preferences

## Data Structure

The GUI expects data to be organized in a specific way:

```
data/
  ├── category1/
  │   ├── dataset1.csv
  │   └── dataset2.csv
  ├── category2/
  │   └── dataset3.csv
  └── ...

scans/
  ├── category1/
  │   ├── scan1.jpg
  │   └── scan2.png
  └── ...

output/
  ├── visualization1.png
  ├── visualization2.png
  └── ...
```

- CSV files should have headers in the first row
- Image files should be in common formats (JPG, PNG)

## Troubleshooting

Common issues and their solutions:

### GUI Doesn't Launch

- Make sure streamlit is installed: `pip install streamlit plotly`
- Check if the port 8501 is already in use: `lsof -i :8501`
- Try a different port: `streamlit run run_gui.py --server.port 8502`

### Data Not Showing in Treemap

- Verify data files are in CSV format
- Check that the data directory path is correctly specified
- Ensure data files have proper headers and content

### Query Not Returning Results

- Check that the query is properly formulated
- Verify the model is correctly specified and available
- Ensure required data is available in the data directory

## Advanced Usage

### Customizing the GUI

You can customize the appearance of the GUI by editing the CSS in the `src/gui.py` file. Look for the `st.markdown("""<style>...</style>""", unsafe_allow_html=True)` section.

### Adding New Visualizations

To add new visualization types:

1. Add the plot functionality in `src/tools.py`
2. Update the `visualize_data` function
3. Modify the agent to recognize new visualization types

### Extending the GUI

The GUI is built with Streamlit, making it easy to extend:

1. Add new tabs with `st.tabs()`
2. Create new interactive elements with Streamlit widgets
3. Add new data processing capabilities by extending the `tools.py` module

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## License

This project is licensed under the terms of the MIT license.