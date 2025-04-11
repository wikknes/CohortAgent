import argparse
import os
import glob
from typing import List, Optional

from .agent import CohortAgent

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='CohortAgent: Analyze multimodal health data locally')
    
    # Main arguments
    parser.add_argument('--query', '-q', type=str, help='Query for the agent to process')
    parser.add_argument('--model', '-m', type=str, default='ollama/llava', 
                        help='Local model to use (default: ollama/llava)')
    
    # Data paths
    parser.add_argument('--data-dir', '-d', type=str, default='./data',
                        help='Directory containing data files (default: ./data)')
    parser.add_argument('--scan-dir', '-s', type=str, default='./scans',
                        help='Directory containing scan images (default: ./scans)')
    parser.add_argument('--output-dir', '-o', type=str, default='./output',
                        help='Directory for saving outputs (default: ./output)')
    
    # Interactive mode
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Start in interactive mode')
    
    return parser.parse_args()

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize the agent
    agent = CohortAgent(model_name=args.model)
    
    if args.interactive:
        print("CohortAgent Interactive Mode")
        print("Type 'exit' or 'quit' to end the session")
        print("-----------------------------------")
        
        while True:
            query = input("\nEnter your query: ")
            if query.lower() in ['exit', 'quit']:
                break
                
            response = agent.run(query)
            print(f"\nResponse:\n{response}")
    
    elif args.query:
        response = agent.run(args.query)
        print(response)
    
    else:
        print("No query provided. Use --query to provide a query or --interactive for interactive mode.")
        print("Run with --help for more information.")

if __name__ == "__main__":
    main()
