import os
from src.tools import analyze_data, visualize_data, merge_and_analyze, merge_and_visualize
from src.utils import load_csv, merge_dataframes

# Test basic analysis
def test_basic_analysis():
    print("Testing analyze_data...")
    result = analyze_data(
        file_path="data/example/lifestyle_data.csv", 
        analysis_type="summary",
        columns=["age", "weight_kg", "height_cm"]
    )
    print(result)
    print("\n" + "-"*50 + "\n")

# Test correlation analysis
def test_correlation_analysis():
    print("Testing correlation analysis...")
    result = analyze_data(
        file_path="data/example/lifestyle_data.csv", 
        analysis_type="correlation",
        columns=["age", "weight_kg", "height_cm", "exercise_min_per_week"]
    )
    print(result)
    print("\n" + "-"*50 + "\n")

# Test visualization
def test_visualization():
    print("Testing visualization...")
    result = visualize_data(
        file_path="data/example/lifestyle_data.csv",
        plot_type="scatter",
        columns=["age", "weight_kg"],
        output_path="output/age_vs_weight.png",
        title="Age vs Weight"
    )
    print(f"Visualization saved to: {result}")
    print("\n" + "-"*50 + "\n")

# Test merged data analysis
def test_merge_analysis():
    print("Testing merge_and_analyze...")
    result = merge_and_analyze(
        file_paths=["data/example/lifestyle_data.csv", "data/example/blood_biochemistry.csv"],
        analysis_type="correlation",
        merge_on="id",
        columns=["weight_kg", "Hemoglobin_g_dL", "ESR_mm_hr"]
    )
    print(result)
    print("\n" + "-"*50 + "\n")

# Test complex visualization
def test_complex_visualization():
    print("Testing complex visualization...")
    result = merge_and_visualize(
        file_paths=["data/example/lifestyle_data.csv", "data/example/immuno_biochemistry.csv"],
        plot_type="regression",
        columns=["weight_kg", "CRP_mg_L"],
        merge_on="id",
        output_path="output/weight_vs_crp.png",
        title="Weight vs C-Reactive Protein (Inflammation Marker)",
        figsize=(10, 6)
    )
    print(f"Complex visualization saved to: {result}")
    print("\n" + "-"*50 + "\n")

# Test heatmap visualization
def test_heatmap_visualization():
    print("Testing heatmap visualization...")
    result = merge_and_visualize(
        file_paths=["data/example/lifestyle_data.csv", "data/example/blood_biochemistry.csv"],
        plot_type="heatmap",
        columns=["age", "weight_kg", "height_cm", "Hemoglobin_g_dL", "Estimated_Glucose_mg_dL", "Vitamin_D_25_OH_ng_mL"],
        merge_on="id",
        output_path="output/correlation_heatmap.png",
        title="Correlation Heatmap of Key Biomarkers"
    )
    print(f"Heatmap visualization saved to: {result}")

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Run tests
    test_basic_analysis()
    test_correlation_analysis()
    test_visualization()
    test_merge_analysis()
    test_complex_visualization()
    test_heatmap_visualization()