from google.adk.agents import LlmAgent
from google.adk.tools import Tool
from google.adk.models import LiteLlm
import os
from typing import List, Dict, Any, Optional

from .tools import (
    analyze_data,
    visualize_data,
    merge_and_analyze,
    merge_and_visualize,
    analyze_images
)

class CohortAgent:
    """
    An agent for analyzing multi-modal health data locally using ADK and LLaVA.
    """
    
    def __init__(self, model_name: str = "ollama/llava"):
        """
        Initialize the CohortAgent.
        
        Args:
            model_name: Name of the local Ollama model to use
        """
        # Initialize the local model via LiteLLM
        self.model = LiteLlm(model=model_name)
        
        # Define custom tools
        self.tools = [
            Tool(
                name="analyze_data",
                description="Perform statistical analysis on health data",
                function=analyze_data,
                parameters={
                    "file_path": "string", 
                    "analysis_type": "string",
                    "columns": "list[string]",
                    "groupby": "string"
                }
            ),
            Tool(
                name="visualize_data",
                description="Generate visualizations from health data",
                function=visualize_data,
                parameters={
                    "file_path": "string",
                    "plot_type": "string",
                    "columns": "list[string]",
                    "output_path": "string",
                    "groupby": "string",
                    "title": "string",
                    "figsize": "list[integer]",
                    "palette": "string"
                }
            ),
            Tool(
                name="merge_and_analyze",
                description="Merge multiple datasets and perform analysis",
                function=merge_and_analyze,
                parameters={
                    "file_paths": "list[string]",
                    "analysis_type": "string",
                    "merge_on": "string",
                    "columns": "list[string]",
                    "groupby": "string"
                }
            ),
            Tool(
                name="merge_and_visualize",
                description="Merge multiple datasets and create visualization",
                function=merge_and_visualize,
                parameters={
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
            ),
            Tool(
                name="analyze_images",
                description="Process and analyze medical images",
                function=analyze_images,
                parameters={
                    "image_paths": "list[string]"
                }
            )
        ]
        
        # Create the agent
        self.agent = LlmAgent(
            name="HealthDataAgent",
            instruction="Assist with analyzing and visualizing multimodal health data locally. "
                        "Process sensitive health information securely without internet access. "
                        "Work with lifestyle questionnaires, scans, blood biochemistry, gut microbiome, "
                        "proteomics, metabolomics, metallomics, and lipidomics data.",
            model=self.model,
            tools=self.tools
        )
    
    def run(self, query: str) -> str:
        """
        Run the agent with a given query.
        
        Args:
            query: The user's query string
            
        Returns:
            The agent's response
        """
        return self.agent.run(query)
