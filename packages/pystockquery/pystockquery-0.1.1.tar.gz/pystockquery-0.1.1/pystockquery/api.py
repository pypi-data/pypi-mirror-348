import pandas as pd
from typing import List, Dict, Union, Optional
from .query_parser import QueryParser
from .data_handler import DataHandler
from .visualization import StockVisualizer

class StockParameterAPI:
    def __init__(self, data_path: str = 'data/merged_stock_data.xlsx'):
        """
        Initialize the Stock API with data loading and condition mapping.
        
        Args:
            data_path (str): Path to the stock data Excel file
        """
        self.data_handler = DataHandler(data_path)
        self.query_parser = QueryParser()
        self.visualizer = StockVisualizer()
        
        # Load data
        self.data = self.data_handler.load_data()
        
    def query(self, query: str, return_type: str = 'dataframe') -> Union[pd.DataFrame, Dict]:
        """
        Execute a natural language query against the stock data.
        
        Args:
            query (str): Natural language query string
            return_type (str): 'dataframe' or 'dict' return format
            
        Returns:
            Filtered and processed stock data
        """
        # Parse the query
        parsed = self.query_parser.parse(query)
        
        # Apply filters
        filtered_data = self.data_handler.apply_filters(
            self.data, 
            parsed.get('filters', [])
        )
        
        # Apply sorting
        if 'sort_by' in parsed:
            filtered_data = self.data_handler.apply_sorting(
                filtered_data, 
                parsed['sort_by'], 
                parsed.get('sort_order', 'desc')
            )
        
        # Apply limit
        if 'limit' in parsed:
            filtered_data = filtered_data.head(parsed['limit'])
            
        # Apply grouping
        if 'group_by' in parsed:
            filtered_data = self.data_handler.apply_grouping(
                filtered_data, 
                parsed['group_by'], 
                parsed.get('agg_functions', ['mean'])
            )
            
        # Convert to desired return type
        if return_type == 'dict':
            return filtered_data.to_dict('records')
        return filtered_data
    
    def visualize(self, query: str, plot_type: Optional[str] = None) -> None:
        """
        Generate visualizations based on the query.
        
        Args:
            query (str): Natural language query
            plot_type (str): Optional override for plot type
        """
        data = self.query(query)
        self.visualizer.plot(data, query, plot_type)
        
    def export(self, query: str, file_path: str, format: str = 'excel') -> None:
        """
        Export query results to a file.
        
        Args:
            query (str): Natural language query
            file_path (str): Output file path
            format (str): 'excel', 'csv', or 'json'
        """
        data = self.query(query)
        self.data_handler.export_data(data, file_path, format)