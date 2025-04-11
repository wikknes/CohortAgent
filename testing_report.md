# CohortAgent Testing Report

## Overview
This report documents the testing methodology and results for the CohortAgent, a Python-based tool for analyzing multi-modal health data. The tests cover both statistical analysis and visualization capabilities across various data types including lifestyle data, biochemistry, immunology, and medical imaging.

## Test Environment Setup

### Prerequisites
- Python 3.6+
- Required packages: pandas, matplotlib, seaborn, numpy, pillow (PIL), scipy

### Installation
```bash
pip install -r requirements.txt
```

### Test Data Structure
The tests use example data organized in these folders:
- `data/example/` - Primary test datasets including:
  - blood_biochemistry.csv
  - gut_microbiome.csv
  - immuno_biochemistry.csv
  - lifestyle_data.csv
  - metabolomics_data.csv
  - metallomics_data.csv
  - proteomics_data.csv
  - scanning_data.csv
- `data/sample/` - Additional sample data
- `scans/sample/` - Example medical images (default example.jpg is created if it doesn't exist)

## Statistical Analysis Tests

### Basic Statistical Tests
| Test Name | Function | Description | Data Source |
|-----------|----------|-------------|------------|
| Basic Analysis | `test_basic_analysis()` | Summary statistics for age, weight, and height | lifestyle_data.csv |
| Correlation Analysis | `test_correlation_analysis()` | Correlation matrix for age, weight, height, and exercise | lifestyle_data.csv |
| Merged Data Analysis | `test_merge_analysis()` | Correlation between weight, hemoglobin, and ESR using merged datasets | lifestyle_data.csv, blood_biochemistry.csv |

### Sample Statistical Query Tests
```python
# Basic summary statistics
analyze_data(
    file_path="data/example/lifestyle_data.csv", 
    analysis_type="summary",
    columns=["age", "weight_kg", "height_cm"]
)

# Correlation analysis
analyze_data(
    file_path="data/example/lifestyle_data.csv", 
    analysis_type="correlation",
    columns=["age", "weight_kg", "height_cm", "exercise_min_per_week"]
)

# Merged dataset analysis
merge_and_analyze(
    file_paths=["data/example/lifestyle_data.csv", "data/example/blood_biochemistry.csv"],
    analysis_type="correlation",
    merge_on="id",
    columns=["weight_kg", "Hemoglobin_g_dL", "ESR_mm_hr"]
)
```

## Visualization Tests

### Basic Visualization Tests
| Test Name | Function | Description | Output File | Data Source |
|-----------|----------|-------------|------------|-------------|
| Scatter Plot | `test_visualization()` | Age vs. Weight scatter plot | output/age_vs_weight.png | lifestyle_data.csv |
| Regression Plot | `test_complex_visualization()` | Weight vs. CRP regression with trend line | output/weight_vs_crp.png | lifestyle_data.csv, immuno_biochemistry.csv |
| Heatmap | `test_heatmap_visualization()` | Correlation heatmap of key biomarkers | output/correlation_heatmap.png | lifestyle_data.csv, blood_biochemistry.csv |

### Sample Visualization Query Tests
```python
# Basic scatter plot
visualize_data(
    file_path="data/example/lifestyle_data.csv",
    plot_type="scatter",
    columns=["age", "weight_kg"],
    output_path="output/age_vs_weight.png",
    title="Age vs Weight"
)

# Regression plot with merged data
merge_and_visualize(
    file_paths=["data/example/lifestyle_data.csv", "data/example/immuno_biochemistry.csv"],
    plot_type="regression",
    columns=["weight_kg", "CRP_mg_L"],
    merge_on="id",
    output_path="output/weight_vs_crp.png",
    title="Weight vs C-Reactive Protein (Inflammation Marker)",
    figsize=(10, 6)
)

# Correlation heatmap
merge_and_visualize(
    file_paths=["data/example/lifestyle_data.csv", "data/example/blood_biochemistry.csv"],
    plot_type="heatmap",
    columns=["age", "weight_kg", "height_cm", "Hemoglobin_g_dL", "Estimated_Glucose_mg_dL", "Vitamin_D_25_OH_ng_mL"],
    merge_on="id",
    output_path="output/correlation_heatmap.png",
    title="Correlation Heatmap of Key Biomarkers"
)
```

## Agent Query Tests

The CohortAgent interface is tested with a series of natural language queries that test both statistical analysis and visualization capabilities:

| Query Type | Example Query | Expected Output |
|------------|---------------|----------------|
| Correlation | "Show me a correlation analysis of age, weight, and exercise from the lifestyle data." | Text correlation matrix |
| Basic Visualization | "Create a visualization showing the relationship between age and weight." | Saved visualization file |
| Merged Analysis | "Perform a merged analysis of lifestyle data and blood biochemistry data with correlation between weight and hemoglobin." | Text analysis results |
| Complex Visualization | "Generate a heatmap visualization by merging lifestyle data and blood biochemistry data, showing correlations between age, weight, height, hemoglobin, glucose, and vitamin D." | Saved heatmap file |
| Image Analysis | "Can you analyze images from the scans directory? file: scans/sample/example.jpg" | Image metadata analysis |
| Regression | "Show me a regression plot between weight and CRP levels using the lifestyle and immuno biochemistry data. Title: Weight vs Inflammation" | Saved regression plot file |

## Running the Tests

To run the tool-specific tests:
```bash
python test_tools.py
```

To run the agent interface tests:
```bash
python test_agent.py
```

## Expected Test Output

### Statistical Test Output
The statistical tests should print analysis results to the console, including:
- Summary statistics (mean, std, min, max, quantiles)
- Correlation matrices
- Regression analysis (slope, intercept, R², p-value)

### Visualization Test Output
The visualization tests should:
1. Create the output directory if it doesn't exist
2. Generate visualizations and save them to the output directory
3. Print confirmation messages with the file paths

## Troubleshooting Common Issues

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Missing data files | Data directory structure incorrect | Ensure data files exist in data/example/ directory |
| Visualization errors | Missing required packages | Verify matplotlib and seaborn are installed correctly |
| Permission errors | Write access to output directory | Check permissions for the output directory |
| Image analysis failures | Missing PIL/Pillow | Ensure PIL is installed with `pip install pillow` |
| DataFrame merge errors | Mismatched column names or types | Check that 'id' column exists in all datasets to be merged |

## Conclusion

The CohortAgent tests cover a comprehensive range of functionality including:
- Basic statistical analysis
- Correlation analysis
- Data visualization with various plot types
- Multi-modal data merging and analysis
- Image metadata extraction

A successful test run will generate both console output (statistical analysis) and visualization files in the output directory. The agent's natural language interface should correctly parse the test queries and execute the appropriate analysis functions.