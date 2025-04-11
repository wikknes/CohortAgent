import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import List, Dict, Union, Optional, Tuple, Any
import numpy as np
from PIL import Image
from scipy import stats
from .utils import load_csv, merge_dataframes, save_plot

def analyze_data(file_path: str, analysis_type: str = "summary", 
                 columns: Optional[List[str]] = None,
                 groupby: Optional[str] = None) -> str:
    """
    Perform statistical analysis on health data.
    
    Args:
        file_path: Path to the CSV file containing the data
        analysis_type: Type of analysis to perform (summary, correlation, 
                      distribution, regression, anova, ttest)
        columns: Specific columns to analyze
        groupby: Column to group data by for group analysis
        
    Returns:
        String representation of the analysis results
    """
    data = load_csv(file_path)
    
    if columns:
        try:
            data = data[columns]
        except KeyError as e:
            return f"Column error: {str(e)}"
    
    if groupby and groupby in data.columns:
        grouped = data.groupby(groupby)
        
        if analysis_type == "summary":
            result = "Group Summary Statistics:\n\n"
            for name, group in grouped:
                result += f"Group: {name}\n"
                result += group.describe().to_string()
                result += "\n\n"
            return result
            
    if analysis_type == "summary":
        return data.describe().to_string()
    
    elif analysis_type == "correlation":
        return data.corr().to_string()
    
    elif analysis_type == "distribution":
        result = "Distribution Analysis:\n\n"
        numeric_cols = data.select_dtypes(include=np.number).columns
        
        for col in numeric_cols:
            skewness = stats.skew(data[col].dropna())
            kurtosis = stats.kurtosis(data[col].dropna())
            normality = stats.shapiro(data[col].dropna()) if len(data[col].dropna()) >= 3 else ("N/A", "N/A")
            
            result += f"Column: {col}\n"
            result += f"Skewness: {skewness:.4f}\n"
            result += f"Kurtosis: {kurtosis:.4f}\n"
            result += f"Shapiro-Wilk Test (normality): stat={normality[0]:.4f}, p={normality[1]:.4f}\n\n"
        
        return result
    
    elif analysis_type == "regression" and len(columns) >= 2:
        x = data[columns[0]]
        y = data[columns[1]]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        result = "Linear Regression Analysis:\n\n"
        result += f"Dependent variable: {columns[1]}\n"
        result += f"Independent variable: {columns[0]}\n"
        result += f"Slope: {slope:.4f}\n"
        result += f"Intercept: {intercept:.4f}\n"
        result += f"R-squared: {r_value**2:.4f}\n"
        result += f"P-value: {p_value:.4f}\n"
        result += f"Standard Error: {std_err:.4f}\n"
        
        return result
    
    elif analysis_type == "ttest" and len(columns) >= 2:
        result = "T-Test Analysis:\n\n"
        t_stat, p_value = stats.ttest_ind(data[columns[0]].dropna(), data[columns[1]].dropna())
        
        result += f"T-test between {columns[0]} and {columns[1]}:\n"
        result += f"T-statistic: {t_stat:.4f}\n"
        result += f"P-value: {p_value:.4f}\n"
        result += f"Significant difference: {'Yes' if p_value < 0.05 else 'No'}\n"
        
        return result
    
    elif analysis_type == "anova" and groupby:
        result = "ANOVA Analysis:\n\n"
        groups = [group[columns[0]].dropna() for name, group in data.groupby(groupby)]
        f_stat, p_value = stats.f_oneway(*groups)
        
        result += f"ANOVA for {columns[0]} across {groupby} groups:\n"
        result += f"F-statistic: {f_stat:.4f}\n"
        result += f"P-value: {p_value:.4f}\n"
        result += f"Significant difference: {'Yes' if p_value < 0.05 else 'No'}\n"
        
        return result
    
    else:
        return f"Unknown analysis type or insufficient parameters: {analysis_type}"

def visualize_data(file_path: str, plot_type: str = "histogram", 
                   columns: Optional[List[str]] = None, 
                   output_path: str = "output/plot.png",
                   groupby: Optional[str] = None,
                   title: Optional[str] = None,
                   figsize: Tuple[int, int] = (12, 8),
                   palette: str = "viridis") -> str:
    """
    Generate visualizations from health data.
    
    Args:
        file_path: Path to the CSV file containing the data
        plot_type: Type of plot to generate (histogram, scatter, heatmap, bar, box,
                  violin, swarm, joint, pair, density, line, regression)
        columns: List of columns to include in the visualization
        output_path: Path where to save the generated plot
        groupby: Column to group data by for grouped visualizations
        title: Title for the plot
        figsize: Figure size as (width, height)
        palette: Color palette to use for the plot
        
    Returns:
        Path to the saved visualization
    """
    data = load_csv(file_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Set the Seaborn style
    sns.set(style="whitegrid")
    
    # Filter columns if specified
    if columns:
        try:
            columns_to_use = [col for col in columns if col in data.columns]
            if not columns_to_use:
                plt.figure(figsize=(8, 6))
                plt.text(0.5, 0.5, f"None of the specified columns were found in the data",
                        horizontalalignment='center', verticalalignment='center')
                return save_plot(output_path)
            data = data[columns_to_use]
        except Exception as e:
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, f"Error selecting columns: {str(e)}",
                    horizontalalignment='center', verticalalignment='center')
            return save_plot(output_path)
    
    # Create the figure
    plt.figure(figsize=figsize)
    
    try:
        # Basic plots
        if plot_type == "histogram":
            if len(data.columns) > 10:
                # If too many columns, create a multi-page file
                data.hist(figsize=figsize)
            else:
                data.hist(figsize=figsize)
            plt.tight_layout()
            
        elif plot_type == "scatter" and len(columns) >= 2:
            if groupby and groupby in data.columns:
                for name, group in data.groupby(groupby):
                    plt.scatter(group[columns[0]], group[columns[1]], label=name, alpha=0.7)
                plt.legend(title=groupby)
            else:
                plt.scatter(data[columns[0]], data[columns[1]], alpha=0.7)
            plt.xlabel(columns[0])
            plt.ylabel(columns[1])
            
        elif plot_type == "heatmap":
            corr = data.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=.5)
            
        elif plot_type == "bar":
            if groupby and groupby in data.columns:
                data.groupby(groupby)[columns].mean().plot(kind='bar')
            elif columns:
                data[columns].plot(kind='bar')
            else:
                data.plot(kind='bar')
                
        elif plot_type == "box":
            if groupby and groupby in data.columns:
                sns.boxplot(x=groupby, y=columns[0], data=data.reset_index().melt(
                    id_vars=groupby, value_vars=columns))
            else:
                sns.boxplot(data=data)
                
        # Advanced plots
        elif plot_type == "violin" and columns:
            if groupby and groupby in data.columns:
                sns.violinplot(x=groupby, y=columns[0], data=data, palette=palette)
            else:
                sns.violinplot(data=data, palette=palette)
                
        elif plot_type == "swarm" and columns:
            if groupby and groupby in data.columns:
                sns.swarmplot(x=groupby, y=columns[0], data=data, palette=palette)
            else:
                plt.text(0.5, 0.5, "Swarm plot requires a groupby column", 
                        horizontalalignment='center', verticalalignment='center')
                
        elif plot_type == "joint" and len(columns) >= 2:
            # Create a new figure for the joint plot
            plt.close()
            joint_plot = sns.jointplot(
                x=columns[0], y=columns[1], data=data, kind="scatter", 
                marginal_kws=dict(bins=15, fill=True), height=8
            )
            joint_plot.fig.tight_layout()
            joint_plot.fig.savefig(output_path)
            plt.close()
            return output_path
            
        elif plot_type == "pair" and len(columns) >= 2:
            # Create a new figure for the pair plot
            plt.close()
            pair_plot = sns.pairplot(
                data=data, hue=groupby if groupby and groupby in data.columns else None,
                palette=palette, height=2.5
            )
            pair_plot.fig.tight_layout()
            pair_plot.fig.savefig(output_path)
            plt.close()
            return output_path
            
        elif plot_type == "density" and columns:
            for col in columns:
                if col in data.columns:
                    sns.kdeplot(data[col], label=col, fill=True, alpha=0.3)
            plt.legend()
            
        elif plot_type == "line" and columns:
            if "date" in data.columns or "time" in data.columns:
                date_col = "date" if "date" in data.columns else "time"
                for col in columns:
                    if col != date_col and col in data.columns:
                        plt.plot(data[date_col], data[col], label=col)
                plt.legend()
            else:
                plt.plot(data[columns])
                plt.legend(columns)
                
        elif plot_type == "regression" and len(columns) >= 2:
            sns.regplot(x=columns[0], y=columns[1], data=data)
            # Add regression equation
            x = data[columns[0]]
            y = data[columns[1]]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            plt.annotate(f'R² = {r_value**2:.3f}\ny = {slope:.3f}x + {intercept:.3f}',
                        xy=(0.05, 0.95), xycoords='axes fraction', 
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                
        else:
            plt.text(0.5, 0.5, f"Unsupported plot type: {plot_type}", 
                    horizontalalignment='center', verticalalignment='center')
        
        # Add title if provided
        if title:
            plt.title(title)
        
        plt.tight_layout()
        
        return save_plot(output_path)
    
    except Exception as e:
        plt.close()
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, f"Error creating {plot_type} plot: {str(e)}",
                horizontalalignment='center', verticalalignment='center')
        return save_plot(output_path)

def merge_and_analyze(file_paths: List[str], 
                      analysis_type: str = "summary", 
                      merge_on: Optional[str] = None,
                      columns: Optional[List[str]] = None,
                      groupby: Optional[str] = None) -> str:
    """
    Merge multiple datasets and perform analysis.
    
    Args:
        file_paths: List of paths to CSV files
        analysis_type: Type of analysis to perform (summary, correlation, distribution,
                      regression, anova, ttest)
        merge_on: Column name to use for merging datasets
        columns: Specific columns to analyze
        groupby: Column to group data by for group analysis
        
    Returns:
        String representation of the analysis results
    """
    try:
        dataframes = [load_csv(fp) for fp in file_paths]
        merged_data = merge_dataframes(dataframes, on=merge_on)
        
        if columns:
            try:
                merged_data = merged_data[columns]
            except KeyError as e:
                return f"Column error: {str(e)}"
        
        if groupby and groupby in merged_data.columns:
            grouped = merged_data.groupby(groupby)
            
            if analysis_type == "summary":
                result = "Group Summary Statistics:\n\n"
                for name, group in grouped:
                    result += f"Group: {name}\n"
                    result += group.describe().to_string()
                    result += "\n\n"
                return result
        
        if analysis_type == "summary":
            return merged_data.describe().to_string()
        
        elif analysis_type == "correlation":
            return merged_data.corr().to_string()
        
        elif analysis_type == "distribution":
            result = "Distribution Analysis:\n\n"
            numeric_cols = merged_data.select_dtypes(include=np.number).columns
            
            for col in numeric_cols:
                skewness = stats.skew(merged_data[col].dropna())
                kurtosis = stats.kurtosis(merged_data[col].dropna())
                normality = stats.shapiro(merged_data[col].dropna()) if len(merged_data[col].dropna()) >= 3 else ("N/A", "N/A")
                
                result += f"Column: {col}\n"
                result += f"Skewness: {skewness:.4f}\n"
                result += f"Kurtosis: {kurtosis:.4f}\n"
                result += f"Shapiro-Wilk Test (normality): stat={normality[0]:.4f}, p={normality[1]:.4f}\n\n"
            
            return result
        
        elif analysis_type == "regression" and len(columns) >= 2:
            x = merged_data[columns[0]]
            y = merged_data[columns[1]]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            result = "Linear Regression Analysis:\n\n"
            result += f"Dependent variable: {columns[1]}\n"
            result += f"Independent variable: {columns[0]}\n"
            result += f"Slope: {slope:.4f}\n"
            result += f"Intercept: {intercept:.4f}\n"
            result += f"R-squared: {r_value**2:.4f}\n"
            result += f"P-value: {p_value:.4f}\n"
            result += f"Standard Error: {std_err:.4f}\n"
            
            return result
        
        elif analysis_type == "ttest" and len(columns) >= 2:
            result = "T-Test Analysis:\n\n"
            t_stat, p_value = stats.ttest_ind(merged_data[columns[0]].dropna(), merged_data[columns[1]].dropna())
            
            result += f"T-test between {columns[0]} and {columns[1]}:\n"
            result += f"T-statistic: {t_stat:.4f}\n"
            result += f"P-value: {p_value:.4f}\n"
            result += f"Significant difference: {'Yes' if p_value < 0.05 else 'No'}\n"
            
            return result
        
        elif analysis_type == "anova" and groupby:
            result = "ANOVA Analysis:\n\n"
            groups = [group[columns[0]].dropna() for name, group in merged_data.groupby(groupby)]
            f_stat, p_value = stats.f_oneway(*groups)
            
            result += f"ANOVA for {columns[0]} across {groupby} groups:\n"
            result += f"F-statistic: {f_stat:.4f}\n"
            result += f"P-value: {p_value:.4f}\n"
            result += f"Significant difference: {'Yes' if p_value < 0.05 else 'No'}\n"
            
            return result
        
        else:
            return f"Unknown analysis type or insufficient parameters: {analysis_type}"
    
    except Exception as e:
        return f"Error in merge_and_analyze: {str(e)}"

def merge_and_visualize(file_paths: List[str], 
                        plot_type: str = "heatmap",
                        columns: Optional[List[str]] = None,
                        merge_on: Optional[str] = None,
                        output_path: str = "output/merged_plot.png",
                        groupby: Optional[str] = None,
                        title: Optional[str] = None,
                        figsize: Tuple[int, int] = (12, 8),
                        palette: str = "viridis") -> str:
    """
    Merge multiple datasets and create visualization.
    
    Args:
        file_paths: List of paths to CSV files
        plot_type: Type of plot to generate (histogram, scatter, heatmap, bar, box,
                  violin, swarm, joint, pair, density, line, regression)
        columns: List of columns to include in the visualization
        merge_on: Column name to use for merging datasets
        output_path: Path where to save the generated plot
        groupby: Column to group data by for grouped visualizations
        title: Title for the plot
        figsize: Figure size as (width, height)
        palette: Color palette to use for the plot
        
    Returns:
        Path to the saved visualization
    """
    try:
        dataframes = [load_csv(fp) for fp in file_paths]
        merged_data = merge_dataframes(dataframes, on=merge_on)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Set the Seaborn style
        sns.set(style="whitegrid")
        
        # Filter columns if specified
        if columns:
            try:
                columns_to_use = [col for col in columns if col in merged_data.columns]
                if not columns_to_use:
                    plt.figure(figsize=(8, 6))
                    plt.text(0.5, 0.5, f"None of the specified columns were found in the data",
                            horizontalalignment='center', verticalalignment='center')
                    return save_plot(output_path)
                merged_data = merged_data[columns_to_use]
            except Exception as e:
                plt.figure(figsize=(8, 6))
                plt.text(0.5, 0.5, f"Error selecting columns: {str(e)}",
                        horizontalalignment='center', verticalalignment='center')
                return save_plot(output_path)
        
        # Create the figure
        plt.figure(figsize=figsize)
        
        # Basic plots
        if plot_type == "histogram":
            if len(merged_data.columns) > 10:
                # If too many columns, create a multi-page file
                merged_data.hist(figsize=figsize)
            else:
                merged_data.hist(figsize=figsize)
            plt.tight_layout()
            
        elif plot_type == "scatter" and len(columns) >= 2:
            if groupby and groupby in merged_data.columns:
                for name, group in merged_data.groupby(groupby):
                    plt.scatter(group[columns[0]], group[columns[1]], label=name, alpha=0.7)
                plt.legend(title=groupby)
            else:
                plt.scatter(merged_data[columns[0]], merged_data[columns[1]], alpha=0.7)
            plt.xlabel(columns[0])
            plt.ylabel(columns[1])
            
        elif plot_type == "heatmap":
            corr = merged_data.corr()
            mask = np.triu(np.ones_like(corr, dtype=bool))  # Mask for upper triangle
            sns.heatmap(corr, annot=True, cmap='coolwarm', mask=mask, linewidths=.5, 
                      cbar_kws={"shrink": .8})
            
        elif plot_type == "bar":
            if groupby and groupby in merged_data.columns:
                merged_data.groupby(groupby)[columns].mean().plot(kind='bar')
            elif columns:
                merged_data[columns].plot(kind='bar')
            else:
                merged_data.plot(kind='bar')
                
        elif plot_type == "box":
            if groupby and groupby in merged_data.columns:
                sns.boxplot(x=groupby, y=columns[0], data=merged_data)
            else:
                sns.boxplot(data=merged_data)
                
        # Advanced plots
        elif plot_type == "violin" and columns:
            if groupby and groupby in merged_data.columns:
                sns.violinplot(x=groupby, y=columns[0], data=merged_data, palette=palette)
            else:
                sns.violinplot(data=merged_data, palette=palette)
                
        elif plot_type == "swarm" and columns:
            if groupby and groupby in merged_data.columns:
                sns.swarmplot(x=groupby, y=columns[0], data=merged_data, palette=palette)
            else:
                plt.text(0.5, 0.5, "Swarm plot requires a groupby column", 
                        horizontalalignment='center', verticalalignment='center')
                
        elif plot_type == "joint" and len(columns) >= 2:
            # Create a new figure for the joint plot
            plt.close()
            joint_plot = sns.jointplot(
                x=columns[0], y=columns[1], data=merged_data, kind="scatter", 
                marginal_kws=dict(bins=15, fill=True), height=8
            )
            if title:
                joint_plot.fig.suptitle(title, y=1.02)
            joint_plot.fig.tight_layout()
            joint_plot.fig.savefig(output_path)
            plt.close()
            return output_path
            
        elif plot_type == "pair" and len(columns) >= 2:
            # Create a new figure for the pair plot
            plt.close()
            pair_plot = sns.pairplot(
                data=merged_data, hue=groupby if groupby and groupby in merged_data.columns else None,
                palette=palette, height=2.5
            )
            if title:
                pair_plot.fig.suptitle(title, y=1.02)
            pair_plot.fig.tight_layout()
            pair_plot.fig.savefig(output_path)
            plt.close()
            return output_path
            
        elif plot_type == "density" and columns:
            for col in columns:
                if col in merged_data.columns:
                    sns.kdeplot(merged_data[col], label=col, fill=True, alpha=0.3)
            plt.legend()
            
        elif plot_type == "regression" and len(columns) >= 2:
            sns.regplot(x=columns[0], y=columns[1], data=merged_data)
            # Add regression equation
            x = merged_data[columns[0]]
            y = merged_data[columns[1]]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            plt.annotate(f'R² = {r_value**2:.3f}\ny = {slope:.3f}x + {intercept:.3f}',
                        xy=(0.05, 0.95), xycoords='axes fraction', 
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                
        elif plot_type == "clustermap" and merged_data.select_dtypes(include=np.number).shape[1] > 1:
            # Create a new figure for the cluster map
            plt.close()
            # Use numeric columns only
            numeric_data = merged_data.select_dtypes(include=np.number)
            g = sns.clustermap(
                numeric_data.corr(), annot=True, cmap="coolwarm", linewidths=.5,
                figsize=figsize, cbar_kws={"shrink": .5}
            )
            if title:
                g.fig.suptitle(title, y=1.02)
            g.fig.tight_layout()
            g.fig.savefig(output_path)
            plt.close()
            return output_path
            
        else:
            plt.text(0.5, 0.5, f"Unsupported plot type: {plot_type}", 
                    horizontalalignment='center', verticalalignment='center')
        
        # Add title if provided
        if title:
            plt.title(title)
        
        plt.tight_layout()
        
        return save_plot(output_path)
    
    except Exception as e:
        plt.close()
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, f"Error creating {plot_type} plot: {str(e)}",
                horizontalalignment='center', verticalalignment='center')
        return save_plot(output_path)

def analyze_images(image_paths: List[str]) -> str:
    """
    Process and analyze images using a local multimodal model.
    This function would typically call the local LLaVA model for image interpretation,
    but here we're providing a placeholder implementation.
    
    Args:
        image_paths: List of paths to image files
        
    Returns:
        Description of the images
    """
    # This is a placeholder. In a real implementation, this would connect
    # to the local LLaVA model for image processing
    result = "Image analysis results:\n"
    
    for path in image_paths:
        try:
            img = Image.open(path)
            result += f"\nImage: {path}\n"
            result += f"- Dimensions: {img.size[0]}x{img.size[1]}\n"
            result += f"- Format: {img.format}\n"
            # In a real implementation, the LLaVA model would analyze the image content
            result += "- Content: [This would be the model's interpretation of the image]\n"
        except Exception as e:
            result += f"\nFailed to analyze {path}: {str(e)}\n"
    
    return result
