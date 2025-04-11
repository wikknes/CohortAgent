import os
from typing import List, Dict, Any, Optional, Callable
import json

from .tools import (
    analyze_data,
    visualize_data,
    merge_and_analyze,
    merge_and_visualize,
    analyze_images
)

class CohortAgent:
    """
    A simplified agent for analyzing multi-modal health data locally.
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the CohortAgent.
        
        Args:
            model_name: Not used in this simplified version
        """
        # Define custom tools
        self.tools = {
            "analyze_data": {
                "function": analyze_data,
                "description": "Perform statistical analysis on health data",
                "parameters": {
                    "file_path": "string", 
                    "analysis_type": "string",
                    "columns": "list[string]",
                    "groupby": "string"
                }
            },
            "visualize_data": {
                "function": visualize_data,
                "description": "Generate visualizations from health data",
                "parameters": {
                    "file_path": "string",
                    "plot_type": "string",
                    "columns": "list[string]",
                    "output_path": "string",
                    "groupby": "string",
                    "title": "string",
                    "figsize": "list[integer]",
                    "palette": "string"
                }
            },
            "merge_and_analyze": {
                "function": merge_and_analyze,
                "description": "Merge multiple datasets and perform analysis",
                "parameters": {
                    "file_paths": "list[string]",
                    "analysis_type": "string",
                    "merge_on": "string",
                    "columns": "list[string]",
                    "groupby": "string"
                }
            },
            "merge_and_visualize": {
                "function": merge_and_visualize,
                "description": "Merge multiple datasets and create visualization",
                "parameters": {
                    "file_paths": "list[string]",
                    "plot_type": "string",
                    "columns": "list[string]",
                    "merge_on": "string",
                    "output_path": "string",
                    "groupby": "string",
                    "title": "string",
                    "figsize": "list[integer]",
                    "palette": "string"
                }
            },
            "analyze_images": {
                "function": analyze_images,
                "description": "Process and analyze medical images",
                "parameters": {
                    "image_paths": "list[string]"
                }
            }
        }
    
    def run(self, query: str) -> str:
        """
        Run the agent with a given query.
        
        In this simplified version, we just parse the query to extract the command
        and parameters, then run the appropriate tool function.
        
        Args:
            query: The user's query string
            
        Returns:
            The agent's response
        """
        # Parse the query to identify the tool and parameters
        if "analysis" in query.lower() or "summary" in query.lower() or "statistics" in query.lower():
            tool = "analyze_data"
            params = self._extract_params_from_query(query, tool)
            
            # Set some defaults if not specified
            if "analysis_type" not in params:
                params["analysis_type"] = "summary"
                
            # Call the function
            try:
                result = self.tools[tool]["function"](**params)
                return f"Analysis Results:\n\n{result}"
            except Exception as e:
                return f"Error performing analysis: {str(e)}"
                
        elif "visualization" in query.lower() or "plot" in query.lower() or "chart" in query.lower():
            tool = "visualize_data"
            params = self._extract_params_from_query(query, tool)
            
            # Set some defaults if not specified
            if "plot_type" not in params:
                params["plot_type"] = "scatter"
            if "output_path" not in params:
                params["output_path"] = "output/plot.png"
                
            # Call the function
            try:
                result = self.tools[tool]["function"](**params)
                return f"Visualization created and saved to: {result}"
            except Exception as e:
                return f"Error creating visualization: {str(e)}"
                
        elif "merge" in query.lower() and ("analysis" in query.lower() or "statistics" in query.lower()):
            tool = "merge_and_analyze"
            params = self._extract_params_from_query(query, tool)
            
            # Set some defaults if not specified
            if "analysis_type" not in params:
                params["analysis_type"] = "correlation"
            if "merge_on" not in params:
                params["merge_on"] = "id"
                
            # Call the function
            try:
                result = self.tools[tool]["function"](**params)
                return f"Merged Analysis Results:\n\n{result}"
            except Exception as e:
                return f"Error performing merged analysis: {str(e)}\nParams: {params}"
                
        elif "merge" in query.lower() and ("visualization" in query.lower() or "plot" in query.lower()):
            tool = "merge_and_visualize"
            params = self._extract_params_from_query(query, tool)
            
            # Set some defaults if not specified
            if "plot_type" not in params:
                params["plot_type"] = "heatmap"
            if "output_path" not in params:
                params["output_path"] = "output/merged_plot.png"
            if "merge_on" not in params:
                params["merge_on"] = "id"
                
            # Call the function
            try:
                result = self.tools[tool]["function"](**params)
                return f"Merged visualization created and saved to: {result}"
            except Exception as e:
                return f"Error creating merged visualization: {str(e)}\nParams: {params}"
                
        elif "image" in query.lower() or "scan" in query.lower():
            tool = "analyze_images"
            params = self._extract_params_from_query(query, tool)
            
            # Call the function
            try:
                result = self.tools[tool]["function"](**params)
                return f"Image Analysis Results:\n\n{result}"
            except Exception as e:
                return f"Error analyzing images: {str(e)}"
        
        else:
            # Help message if we can't determine the tool
            return """
            I can help with the following types of health data analysis:
            
            1. Data Analysis: Provide statistical analysis of health data files
            2. Visualization: Create plots and charts from health data
            3. Merged Analysis: Combine and analyze multiple datasets
            4. Merged Visualization: Create visualizations from multiple datasets
            5. Image Analysis: Process and analyze medical images
            
            Please provide specific files and parameters for your analysis.
            """
    
    def _extract_params_from_query(self, query: str, tool: str) -> Dict[str, Any]:
        """
        Simple parameter extractor from query text.
        This is a naive implementation. In a real system, you'd use NLP/LLM.
        """
        params = {}
        
        # Extract file paths if mentioned
        if "file" in query.lower() and ":" in query:
            file_part = query.split("file:")[1].split()[0].strip()
            if tool in ["merge_and_analyze", "merge_and_visualize"]:
                files = file_part.split(",")
                params["file_paths"] = [f.strip() for f in files]
            elif tool in ["analyze_images"]:
                files = file_part.split(",")
                params["image_paths"] = [f.strip() for f in files]
            else:
                params["file_path"] = file_part.strip()
        
        # Default to example data if no files specified
        if "file_path" not in params and tool in ["analyze_data", "visualize_data"]:
            params["file_path"] = "data/example/lifestyle_data.csv"
        if "file_paths" not in params and tool in ["merge_and_analyze", "merge_and_visualize"]:
            params["file_paths"] = ["data/example/lifestyle_data.csv", "data/example/blood_biochemistry.csv"]
        if "image_paths" not in params and tool == "analyze_images":
            # Just a placeholder since we don't have real image data
            params["image_paths"] = ["scans/sample/example.jpg"]
            
        # Extract columns if mentioned
        if "columns" in query.lower() and ":" in query:
            col_part = query.split("columns:")[1].split(".")[0].strip()
            cols = col_part.split(",")
            params["columns"] = [c.strip() for c in cols]
        
        # Default columns if not specified
        if "columns" not in params:
            if tool in ["analyze_data", "visualize_data"]:
                params["columns"] = ["age", "weight_kg", "height_cm"]
            elif tool in ["merge_and_analyze", "merge_and_visualize"]:
                params["columns"] = ["weight_kg", "Hemoglobin_g_dL"]
                
        # Extract plot type if mentioned
        if "plot type" in query.lower() and ":" in query:
            plot_part = query.split("plot type:")[1].split()[0].strip()
            params["plot_type"] = plot_part
        
        # Extract analysis type if mentioned
        if "analysis type" in query.lower() and ":" in query:
            analysis_part = query.split("analysis type:")[1].split()[0].strip()
            params["analysis_type"] = analysis_part
            
        # Extract merge column if mentioned
        if "merge on" in query.lower() and ":" in query:
            merge_part = query.split("merge on:")[1].split()[0].strip()
            params["merge_on"] = merge_part
        elif tool in ["merge_and_analyze", "merge_and_visualize"]:
            params["merge_on"] = "id"
            
        # Extract group by if mentioned
        if "group by" in query.lower() and ":" in query:
            group_part = query.split("group by:")[1].split()[0].strip()
            params["groupby"] = group_part
            
        # Extract title if mentioned for visualization
        if "title:" in query.lower():
            try:
                title_part = query.split("title:")[1].split(".")[0].strip()
                params["title"] = title_part
            except (IndexError, KeyError):
                # If there's an error parsing the title, try a different approach
                if "title" in query.lower():
                    # Just use what comes after "title:" as the title
                    parts = query.lower().split("title:")
                    if len(parts) > 1:
                        params["title"] = parts[1].strip()
            
        return params