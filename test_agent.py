from src.agent import CohortAgent
import os
from PIL import Image
import numpy as np

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Create a mock medical image for testing
if not os.path.exists("scans/sample/example.jpg"):
    img = Image.new('RGB', (512, 512), color=(73, 109, 137))
    img.save("scans/sample/example.jpg")

# Initialize the agent
agent = CohortAgent()

# Test queries
queries = [
    "Show me a correlation analysis of age, weight, and exercise from the lifestyle data.",
    "Create a visualization showing the relationship between age and weight.",
    "Perform a merged analysis of lifestyle data and blood biochemistry data with correlation between weight and hemoglobin.",
    "Generate a heatmap visualization by merging lifestyle data and blood biochemistry data, showing correlations between age, weight, height, hemoglobin, glucose, and vitamin D.",
    "Can you analyze images from the scans directory? file: scans/sample/example.jpg",
    "Show me a regression plot between weight and CRP levels using the lifestyle and immuno biochemistry data. Title: Weight vs Inflammation"
]

# Run each query and print the response
for i, query in enumerate(queries):
    print(f"Query {i+1}: {query}")
    response = agent.run(query)
    print(f"\nResponse:\n{response}")
    print("\n" + "="*80 + "\n")