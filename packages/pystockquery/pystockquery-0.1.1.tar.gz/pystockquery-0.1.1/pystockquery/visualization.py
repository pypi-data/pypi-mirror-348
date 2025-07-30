import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional

class StockVisualizer:
    def plot(self, data: pd.DataFrame, query: str, plot_type: Optional[str] = None) -> None:
        """
        Generate appropriate visualization based on data and query.
        
        Args:
            data (pd.DataFrame): Data to visualize
            query (str): Original query for context
            plot_type (str): Optional override for plot type
        """
        if not plot_type:
            plot_type = self._determine_plot_type(query)
            
        if plot_type == 'scatter':
            self._create_scatter_plot(data, query)
        elif plot_type == 'bar':
            self._create_bar_plot(data, query)
        elif plot_type == 'histogram':
            self._create_histogram(data, query)
        elif plot_type == 'box':
            self._create_box_plot(data, query)
        else:
            self._create_default_plot(data, query)
            
        plt.tight_layout()
        plt.show()
    
    def _determine_plot_type(self, query: str) -> str:
        """Determine the best plot type based on query content"""
        query = query.lower()
        
        if 'scatter' in query or 'vs' in query or 'versus' in query:
            return 'scatter'
        elif 'histogram' in query or 'distribution' in query:
            return 'histogram'
        elif 'compare' in query or 'across' in query:
            return 'bar'
        elif 'range' in query or 'variation' in query:
            return 'box'
        else:
            return 'scatter'  # default
    
    def _create_scatter_plot(self, data: pd.DataFrame, query: str) -> None:
        """Create scatter plot from data"""
        if 'vs' in query:
            parts = query.split('vs')
            x_col = parts[0].strip()
            y_col = parts[1].strip()
        else:
            x_col = data.columns[0]
            y_col = data.columns[1]
            
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=x_col, y=y_col, hue=data.index)
        plt.title(f"{y_col} vs {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        
    def _create_bar_plot(self, data: pd.DataFrame, query: str) -> None:
        """Create bar plot from data"""
        if len(data.columns) > 1:
            # Multiple columns - use grouped bar plot
            data.plot(kind='bar', figsize=(12, 6))
        else:
            # Single column - simple bar plot
            data.plot(kind='bar', figsize=(10, 6))
        plt.title("Comparison Plot")
        
    def _create_histogram(self, data: pd.DataFrame, query: str) -> None:
        """Create histogram from data"""
        numeric_cols = data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            plt.figure(figsize=(10, 6))
            sns.histplot(data[col], kde=True)
            plt.title(f"Distribution of {col}")
            
    def _create_box_plot(self, data: pd.DataFrame, query: str) -> None:
        """Create box plot from data"""
        numeric_cols = data.select_dtypes(include=['number']).columns
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=data[numeric_cols])
        plt.title("Value Distribution")
        
    def _create_default_plot(self, data: pd.DataFrame, query: str) -> None:
        """Default plot when type can't be determined"""
        if len(data.columns) >= 2:
            self._create_scatter_plot(data, query)
        else:
            self._create_bar_plot(data, query)