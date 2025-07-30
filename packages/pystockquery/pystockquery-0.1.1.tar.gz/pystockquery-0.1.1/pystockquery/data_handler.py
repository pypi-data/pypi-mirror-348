import pandas as pd
from typing import List, Dict, Union
import json

class DataHandler:
    def __init__(self, data_path: str):
        self.data_path = data_path
        
    def load_data(self) -> pd.DataFrame:
        """Load the stock data from Excel file"""
        return pd.read_excel(self.data_path)
    
    def apply_filters(self, data: pd.DataFrame, filters: List[Dict[str, str]]) -> pd.DataFrame:
        """Apply multiple filters to the dataframe"""
        if not filters:
            return data
            
        filtered_data = data.copy()
        
        for filter_cond in filters:
            field = filter_cond['field']
            operator = filter_cond['operator']
            value = filter_cond['value']
            
            if operator == '>':
                filtered_data = filtered_data[filtered_data[field] > value]
            elif operator == '<':
                filtered_data = filtered_data[filtered_data[field] < value]
            elif operator == '>=':
                filtered_data = filtered_data[filtered_data[field] >= value]
            elif operator == '<=':
                filtered_data = filtered_data[filtered_data[field] <= value]
            elif operator == '=':
                filtered_data = filtered_data[filtered_data[field] == value]
            elif operator == '!=':
                filtered_data = filtered_data[filtered_data[field] != value]
                
        return filtered_data
    
    def apply_sorting(self, data: pd.DataFrame, sort_by: str, order: str = 'desc') -> pd.DataFrame:
        """Sort the dataframe by specified field"""
        return data.sort_values(by=sort_by, ascending=(order == 'asc'))
    
    def apply_grouping(self, data: pd.DataFrame, group_by: str, agg_funcs: List[str] = ['mean']) -> pd.DataFrame:
        """Group data by specified field and apply aggregation"""
        # Convert string function names to actual functions
        agg_dict = {}
        for col in data.select_dtypes(include=['number']).columns:
            agg_dict[col] = agg_funcs
            
        return data.groupby(group_by).agg(agg_dict).reset_index()
    
    def export_data(self, data: pd.DataFrame, file_path: str, format: str = 'excel') -> None:
        """Export data to specified format"""
        if format == 'excel':
            data.to_excel(file_path, index=False)
        elif format == 'csv':
            data.to_csv(file_path, index=False)
        elif format == 'json':
            data.to_json(file_path, orient='records', indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")