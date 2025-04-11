import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from typing import List, Dict, Any, Optional
import json
import glob

from .agent import CohortAgent

class CohortAgentGUI:
    """Interactive GUI for CohortAgent using Streamlit"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the CohortAgentGUI.
        
        Args:
            model_name: Model name to use
        """
        self.agent = CohortAgent(model_name=model_name)
        self.data_dir = "./data"
        self.scan_dir = "./scans"
        self.output_dir = "./output"
        
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_treemap(self, data_dir: str) -> go.Figure:
        """
        Create an interactive treemap visualization of available datasets
        
        Args:
            data_dir: Directory containing data files
            
        Returns:
            Plotly figure with treemap visualization
        """
        # Scan for data files
        data_files = glob.glob(f"{data_dir}/**/*.csv", recursive=True)
        
        # Group data by categories
        treemap_data = []
        
        for file_path in data_files:
            # Get relative path from data directory
            rel_path = os.path.relpath(file_path, data_dir)
            
            # Get directory levels and filename
            path_parts = rel_path.split(os.sep)
            filename = path_parts[-1]
            category = path_parts[0] if len(path_parts) > 1 else "root"
            subcategory = path_parts[1] if len(path_parts) > 2 else ""
            
            # Try to read the file to get the number of records and columns
            try:
                df = pd.read_csv(file_path)
                records = len(df)
                columns = len(df.columns)
                col_names = ", ".join(df.columns[:5])
                if len(df.columns) > 5:
                    col_names += "..."
            except Exception:
                records = 0
                columns = 0
                col_names = "Error reading file"
            
            # Create entry for treemap
            entry = {
                "category": category,
                "subcategory": subcategory,
                "dataset": filename,
                "records": records,
                "columns": columns,
                "path": file_path,
                "details": f"Records: {records}, Columns: {columns}",
                "column_names": col_names
            }
            treemap_data.append(entry)
        
        # Convert to DataFrame for plotly
        df_treemap = pd.DataFrame(treemap_data)
        
        if df_treemap.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No data files found",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Create hierarchical structure for treemap
        df_treemap["size"] = df_treemap["records"] * df_treemap["columns"] + 10  # Ensure all items are visible
        
        # Create custom hover text
        df_treemap["hover_text"] = df_treemap.apply(
            lambda row: f"<b>{row['dataset']}</b><br>"
                       f"Category: {row['category']}<br>"
                       f"Records: {row['records']}<br>"
                       f"Columns: {row['columns']}<br>"
                       f"Path: {row['path']}<br>"
                       f"Column names: {row['column_names']}",
            axis=1
        )
        
        # Create treemap figure
        fig = px.treemap(
            df_treemap,
            path=['category', 'subcategory', 'dataset'],
            values='size',
            color='columns',
            color_continuous_scale='Viridis',
            hover_data=['records', 'columns'],
            custom_data=['path', 'hover_text'],
            title="Available Datasets"
        )
        
        # Customize hover template
        fig.update_traces(
            hovertemplate='%{customdata[1]}<extra></extra>'
        )
        
        # Update layout for better aesthetics
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            coloraxis_colorbar=dict(
                title="Columns",
            ),
            font=dict(family="Arial", size=12),
        )
        
        return fig
    
    def run(self):
        """Run the Streamlit GUI application"""
        st.set_page_config(
            page_title="CohortAgent GUI",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply custom styling
        st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            background-color: #f8f9fa;
        }
        .css-1d391kg {
            background-color: #e9ecef;
        }
        .css-18e3th9 {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .st-bw {
            background-color: #ffffff;
        }
        h1, h2, h3 {
            color: #343a40;
        }
        .stTextInput > div > div > input {
            border-radius: 5px;
        }
        .stButton > button {
            border-radius: 5px;
            background-color: #007bff;
            color: white;
        }
        .stButton > button:hover {
            background-color: #0069d9;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Title and intro
        st.title("CohortAgent Interactive Dashboard")
        st.subheader("Analyze multimodal health data with natural language queries")
        
        # Sidebar for configuration
        with st.sidebar:
            st.header("Configuration")
            
            # Model selection
            model_selection = st.selectbox(
                "Model",
                options=["ollama/llava", "local/llama", "custom"],
                index=0
            )
            
            # Data directory selection
            data_dir = st.text_input("Data Directory", value=self.data_dir)
            
            # Scan directory selection
            scan_dir = st.text_input("Scan Directory", value=self.scan_dir)
            
            # Output directory selection
            output_dir = st.text_input("Output Directory", value=self.output_dir)
            
            # Visualization configuration
            st.header("Visualization Options")
            
            viz_type = st.selectbox(
                "Default Visualization",
                options=["heatmap", "scatter", "histogram", "bar", "box", "line", "pair", "regression"],
                index=0
            )
            
            # Apply button
            if st.button("Apply Settings"):
                self.data_dir = data_dir
                self.scan_dir = scan_dir
                self.output_dir = output_dir
                st.success("Settings applied!")
        
        # Main panel with tabs
        tab1, tab2, tab3 = st.tabs(["Query", "Data Explorer", "Results History"])
        
        # Query tab
        with tab1:
            st.header("Ask a question about your health data")
            
            # Query input
            query = st.text_area(
                "Enter your query:",
                height=100,
                help="Ask a question or request an analysis of your health data",
                placeholder="Example: Create a visualization of age vs weight from lifestyle data"
            )
            
            # Run button
            if st.button("Run Query"):
                if query:
                    with st.spinner("Processing query..."):
                        try:
                            # Run the query through the agent
                            response = self.agent.run(query)
                            
                            # Display the response
                            st.subheader("Response:")
                            st.write(response)
                            
                            # Check if visualization was created
                            if "visualization" in query.lower() and "saved to:" in response:
                                image_path = response.split("saved to:")[1].strip()
                                if os.path.exists(image_path):
                                    st.image(image_path, caption="Generated Visualization")
                        except Exception as e:
                            st.error(f"Error processing query: {str(e)}")
                else:
                    st.warning("Please enter a query.")
        
        # Data Explorer tab
        with tab2:
            st.header("Data Explorer")
            
            # Create treemap visualization
            treemap_fig = self.create_treemap(self.data_dir)
            
            # Display the treemap
            st.plotly_chart(treemap_fig, use_container_width=True)
            
            # Add section for preview of selected dataset
            st.subheader("Dataset Preview")
            
            # Let user select a file to preview
            data_files = glob.glob(f"{self.data_dir}/**/*.csv", recursive=True)
            if data_files:
                selected_file = st.selectbox("Select a dataset to preview:", data_files)
                
                if selected_file:
                    try:
                        # Read the file and display a preview
                        df = pd.read_csv(selected_file)
                        
                        # Display file info
                        st.write(f"**File Path:** {selected_file}")
                        st.write(f"**Records:** {len(df)}, **Columns:** {len(df.columns)}")
                        
                        # Show the dataframe preview
                        st.dataframe(df.head(10))
                        
                        # Display basic statistics
                        st.write("### Basic Statistics")
                        
                        # Select numeric columns for statistics
                        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                        
                        if numeric_cols:
                            # Display descriptive statistics
                            st.dataframe(df[numeric_cols].describe())
                            
                            # Create a simple correlation heatmap for numeric columns
                            if len(numeric_cols) > 1:
                                st.write("### Correlation Heatmap")
                                corr = df[numeric_cols].corr()
                                
                                # Create correlation heatmap
                                fig = px.imshow(
                                    corr,
                                    color_continuous_scale="RdBu_r",
                                    labels=dict(color="Correlation"),
                                    title="Correlation between variables"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No numeric columns found for statistics.")
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
            else:
                st.info("No data files found. Please check the data directory.")
        
        # Results History tab
        with tab3:
            st.header("Results History")
            
            # Display output files
            output_files = glob.glob(f"{self.output_dir}/**/*.*", recursive=True)
            
            if output_files:
                st.write(f"Found {len(output_files)} result files")
                
                # Group by file type
                output_by_type = {}
                for f in output_files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext not in output_by_type:
                        output_by_type[ext] = []
                    output_by_type[ext].append(f)
                
                # Create expandable sections for each type
                for ext, files in output_by_type.items():
                    with st.expander(f"{ext.upper()} Files ({len(files)})"):
                        for f in files:
                            filename = os.path.basename(f)
                            col1, col2 = st.columns([4, 1])
                            
                            with col1:
                                st.write(f"**{filename}**")
                                st.write(f"Path: {f}")
                                
                                # If image, display it
                                if ext.lower() in ['.png', '.jpg', '.jpeg', '.gif']:
                                    st.image(f, caption=filename)
                            
                            with col2:
                                st.download_button(
                                    label="Download",
                                    data=open(f, 'rb').read(),
                                    file_name=filename,
                                    mime=f"application/{ext.replace('.', '')}"
                                )
            else:
                st.info("No output files found yet. Run some queries to generate results.")

def main():
    """Main entry point for the GUI application"""
    # Get configuration from environment variables if available
    model_name = os.environ.get("MODEL_NAME", "ollama/llava")
    data_dir = os.environ.get("DATA_DIR", "./data")
    scan_dir = os.environ.get("SCAN_DIR", "./scans")
    output_dir = os.environ.get("OUTPUT_DIR", "./output")
    
    # Initialize the GUI with the configuration
    gui = CohortAgentGUI(model_name=model_name)
    gui.data_dir = data_dir
    gui.scan_dir = scan_dir
    gui.output_dir = output_dir
    
    # Run the GUI
    gui.run()

if __name__ == "__main__":
    main()