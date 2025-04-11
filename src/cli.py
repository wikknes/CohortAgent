import argparse
import os
import glob
import subprocess
import sys
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
    
    # Interactive modes
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--interactive', '-i', action='store_true',
                      help='Start in interactive CLI mode')
    group.add_argument('--gui', '-g', action='store_true',
                      help='Launch the interactive GUI')
    
    return parser.parse_args()

def launch_streamlit_gui(model_name, data_dir, scan_dir, output_dir):
    """Launch the Streamlit GUI."""
    try:
        # Check if streamlit is installed
        try:
            import streamlit
        except ImportError:
            print("Error: Streamlit is not installed. Please install it with:")
            print("  pip install streamlit plotly")
            sys.exit(1)
            
        # Set environment variables to pass to the GUI
        os.environ["MODEL_NAME"] = model_name
        os.environ["DATA_DIR"] = data_dir
        os.environ["SCAN_DIR"] = scan_dir
        os.environ["OUTPUT_DIR"] = output_dir
        
        # Create the launcher file
        launcher_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui_launcher.py")
        
        with open(launcher_path, "w") as f:
            f.write("""
import os
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Import the GUI main function
from src.gui import main

if __name__ == "__main__":
    main()
""")
        
        # Execute streamlit directly
        print("Launching CohortAgent GUI... (press Ctrl+C to exit)")
        print("\nIf the browser doesn't open automatically, go to the URL shown below")
        print("Typically: http://localhost:8501\n")
        os.system(f"streamlit run {launcher_path}")
        
    except Exception as e:
        print(f"Failed to launch GUI: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.gui:
        # Launch the GUI
        launch_streamlit_gui(args.model, args.data_dir, args.scan_dir, args.output_dir)
    else:
        # Initialize the agent for CLI mode
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
            print("No query provided. Use one of the following options:")
            print("  --query (-q): Provide a query to process")
            print("  --interactive (-i): Start interactive CLI mode")
            print("  --gui (-g): Launch the interactive GUI")
            print("Run with --help for more information.")

if __name__ == "__main__":
    main()
