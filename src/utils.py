import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from typing import List, Dict, Union, Optional, Tuple, Any

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame containing the data
    """
    return pd.read_csv(file_path)

def merge_dataframes(dataframes: List[pd.DataFrame], on: Optional[str] = None) -> pd.DataFrame:
    """
    Merge multiple dataframes.
    
    Args:
        dataframes: List of dataframes to merge
        on: Column name to merge on (if None, uses index)
        
    Returns:
        Merged dataframe
    """
    if not dataframes:
        return pd.DataFrame()
    
    result = dataframes[0].copy()
    for df in dataframes[1:]:
        if on:
            result = pd.merge(result, df, on=on)
        else:
            result = pd.concat([result, df], axis=1)
    
    return result

def save_plot(plot_path: str) -> str:
    """
    Save the current matplotlib figure to a file.
    
    Args:
        plot_path: Path where to save the plot
        
    Returns:
        Path to the saved plot
    """
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    return plot_path
