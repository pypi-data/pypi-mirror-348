import re
from typing import Dict, List, Union

class QueryParser:
    def __init__(self):
        self.condition_map = {
    # Stock / Financial Metrics
    "Stock Industry": "industry",
    "Dividend Payout Ratio": "payoutRatio",
    "Five Year Avg Dividend Yield": "fiveYearAvgDividendYield",
    "Price to Sales Trailing 12 Months": "priceToSalesTrailing12Months",
    "Trailing Annual Dividend Rate": "trailingAnnualDividendRate",
    "Profit Margins": "profitMargins",
    "% Held by Insiders": "heldPercentInsiders",
    "% Held by Institutions": "heldPercentInstitutions",
    "Volume": "volume",
    "Regular Market Volume": "regularMarketVolume",
    "Average Volume": "averageVolume",
    "Average Volume 10 days": "averageVolume10days",
    "Average Daily Volume 10 Day": "averageDailyVolume10Day",
    "Return on Assets": "returnOnAssets",
    "Return on Assets (ttm)": "returnOnAssets",
    "Return on Equity (ttm)": "returnOnEquity",
    "Total Value": "totalValue",
    "Correlation with NSEI": "Correlation with ^NSEI",
    "Annualized Alpha (%)": "Annualized Alpha (%)",
    "Annualized Volatility (%)": "Annualized Volatility (%)",
    "Sharpe Ratio": "Sharpe Ratio",
    "Treynor Ratio": "Treynor Ratio",
    "Sortino Ratio": "Sortino Ratio",
    "Maximum Drawdown": "Maximum Drawdown",
    "R-Squared": "R-Squared",
    "Downside Deviation": "Downside Deviation",
    "Annualized Tracking Error (%)": "Annualized Tracking Error (%)",
    "VaR (95%)": "VaR (95%)",
    "50-Day Moving Average": "50-Day Moving Average",
    "200-Day Moving Average": "200-Day Moving Average",
    "New Haircut Margin": "New Haircut Margin",
    "Rating": "Rating",
    "Combined Score": "Combined Score",
    "New Collateral Value Percentage": "New Collateral Value Percentage",
    "Market Cap": "marketCap",
    "Enterprise Value": "enterpriseValue",
    "Trailing P/E": "trailingPE",
    "Forward P/E": "forwardPE",
    "PEG Ratio": "pegRatio",
    "Price/Sales": "priceToSalesTrailing12Months",
    "Price/Book": "priceToBook",
    "Enterprise Value/Revenue": "enterpriseToRevenue",
    "Enterprise Value/EBITDA": "enterpriseToEbitda",
    "Beta": "beta",
    "52-Week High": "fiftyTwoWeekHigh",
    "52-Week Low": "fiftyTwoWeekLow",
    "50-Day Average": "fiftyDayAverage",
    "200-Day Average": "twoHundredDayAverage",
    "Short Ratio": "shortRatio",
    "Short % of Float": "shortPercentOfFloat",
    "Shares Outstanding": "sharesOutstanding",
    "Float": "floatShares",
    "Shares Short": "sharesShort",
    "Short Ratio": "shortRatio",
    "Book Value": "bookValue",
    "Price/Book": "priceToBook",
    "EBITDA": "ebitda",
    "Revenue": "revenue",
    "Revenue Per Share": "revenuePerShare",
    "Gross Profit": "grossProfit",
    "Free Cash Flow": "freeCashflow",
    "Operating Cash Flow": "operatingCashflow",
    "Earnings Growth": "earningsGrowth",
    "Revenue Growth": "revenueGrowth",
    "Current Ratio": "currentRatio",
    "Quick Ratio": "quickRatio",
    "Debt to Equity": "debtToEquity",
    "Total Debt": "totalDebt",
    "Total Cash": "totalCash",
    "Total Cash Per Share": "totalCashPerShare",
    "CAGR": "CAGR",
    "ROI": "ROI",
    "EPS": "trailingEps",
    "EPS Growth": "epsGrowth",

    # Interpretations
    "Correlation with NSEI Interpretation": "Correlation with ^NSEI Interpretation",
    "Alpha Interpretation": "Annualized Alpha (%) Interpretation",
    "Volatility Interpretation": "Annualized Volatility (%) Interpretation",
    "Sharpe Ratio Interpretation": "Sharpe Ratio Interpretation",
    "Treynor Ratio Interpretation": "Treynor Ratio Interpretation",
    "Sortino Ratio Interpretation": "Sortino Ratio Interpretation",
    "Maximum Drawdown Interpretation": "Maximum Drawdown Interpretation",
    "R-Squared Interpretation": "R-Squared Interpretation",
    "Downside Deviation Interpretation": "Downside Deviation Interpretation",
    "Tracking Error Interpretation": "Annualized Tracking Error (%) Interpretation",
    "VaR Interpretation": "VaR (95%) Interpretation",
    "Moving Average Interpretation": "Moving Average Interpretation",
    "Valuation Interpretation": "Valuation Interpretation",

    # Company Info
    "Address": "address1",
    "City": "city",
    "Zip": "zip",
    "Country": "country",
    "Website": "website",
    "Sector": "sector",
    "Industry": "industry",
    "Business Summary": "longBusinessSummary",
    "Full Time Employees": "fullTimeEmployees",
    "Company Name": "shortName",
    "Exchange": "exchange",
    "Currency": "currency",
    "Quote Type": "quoteType",

    # Financial Statements
    "Income Statement (Quarterly)": "incomeStatementQuarterly",
    "Income Statement (Annual)": "incomeStatementAnnual",
    "Balance Sheet (Quarterly)": "balanceSheetQuarterly",
    "Balance Sheet (Annual)": "balanceSheetAnnual",
    "Cash Flow (Quarterly)": "cashflowStatementQuarterly",
    "Cash Flow (Annual)": "cashflowStatementAnnual",

    # Industry Comparisons
    "Industry Forward PE": "industry_forwardPE",
    "Industry Trailing PE": "industry_trailingPE",
    "Industry Debt to Equity": "industry_debtToEquity",
    "Industry Current Ratio": "industry_currentRatio",
    "Industry Quick Ratio": "industry_quickRatio",
    "Industry EBITDA": "industry_ebitda",
    "Industry Total Debt": "industry_totalDebt",
    "Industry Return on Assets": "industry_returnOnAssets",
    "Industry Return on Equity": "industry_returnOnEquity",
    "Industry Revenue Growth": "industry_revenueGrowth",
    "Industry Gross Margins": "industry_grossMargins",
    "Industry EBITDA Margins": "industry_ebitdaMargins",
    "Industry Operating Margins": "industry_operatingMargins",
    "Industry PEG Ratio": "industry_pegRatio",
    "Industry Price/Sales": "industry_priceToSales",
    "Industry Price/Book": "industry_priceToBook",

    # Technical Indicators
    "RSI": "rsi",
    "MACD": "macd",
    "Bollinger Bands": "bollingerBands",
    "Stochastic Oscillator": "stochasticOscillator",
    "ATR": "averageTrueRange",
    "OBV": "onBalanceVolume",
    "ADX": "averageDirectionalIndex",
    "CCI": "commodityChannelIndex",
    "Money Flow Index": "moneyFlowIndex",
    "Parabolic SAR": "parabolicSAR",
    "Ichimoku Cloud": "ichimokuCloud",

    # Alternative Names
    "PE Ratio": "trailingPE",
    "Price to Earnings": "trailingPE",
    "Price to Book Ratio": "priceToBook",
    "Price to Sales Ratio": "priceToSalesTrailing12Months",
    "Debt/Equity": "debtToEquity",
    "Current Assets": "totalCurrentAssets",
    "Current Liabilities": "totalCurrentLiabilities",
    "Total Assets": "totalAssets",
    "Total Liabilities": "totalLiabilities",
    "Shareholders Equity": "totalStockholderEquity",
    "Operating Income": "operatingIncome",
    "Net Income": "netIncome",
    "Diluted EPS": "trailingEps",
    "Basic EPS": "trailingEps",
    "Dividend Yield": "dividendYield",
    "Payout Ratio": "payoutRatio",
    "Enterprise Value to EBITDA": "enterpriseToEbitda",
    "Enterprise Value to Revenue": "enterpriseToRevenue",
    "EV/EBITDA": "enterpriseToEbitda",
    "EV/Revenue": "enterpriseToRevenue",
    "Quick Ratio": "quickRatio",
    "Acid Test Ratio": "quickRatio",
    "Working Capital": "workingCapital"
}
        
        
        # Reverse mapping for lookups
        self.reverse_condition_map = {v: k for k, v in self.condition_map.items()}
        
    def parse(self, query: str) -> Dict[str, Union[List[str], str, int]]:
        """
        Parse natural language query into structured components.
        
        Args:
            query (str): Natural language query string
            
        Returns:
            Dictionary containing parsed query components
        """
        query = query.lower()
        parsed = {
            'filters': [],
            'sort_by': None,
            'sort_order': 'desc',
            'limit': None,
            'group_by': None,
            'agg_functions': ['mean']
        }
        
        # Extract filters
        parsed['filters'] = self._extract_filters(query)
        
        # Extract sorting
        sort_info = self._extract_sorting(query)
        if sort_info:
            parsed['sort_by'], parsed['sort_order'] = sort_info
            
        # Extract limit
        parsed['limit'] = self._extract_limit(query)
        
        # Extract grouping
        group_info = self._extract_grouping(query)
        if group_info:
            parsed['group_by'], parsed['agg_functions'] = group_info
            
        return parsed
    
    def _extract_filters(self, query: str) -> List[Dict[str, str]]:
        """Extract filter conditions from query"""
        filters = []
        pattern = r'([a-zA-Z\s%\(\)]+)\s*(>|<|>=|<=|=|!=)\s*([\d\.%]+)'
        matches = re.findall(pattern, query)
        
        for match in matches:
            field, operator, value = match
            field = field.strip()
            value = value.strip()
            
            # Clean and standardize field name
            field = self._standardize_field_name(field)
            
            # Clean value
            if '%' in value:
                value = float(value.replace('%', '')) / 100
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass
                    
            filters.append({
                'field': field,
                'operator': operator,
                'value': value
            })
            
        return filters
    
    def _extract_sorting(self, query: str) -> tuple:
        """Extract sorting field and order from query"""
        sort_patterns = [
            r'rank (?:all )?stocks by ([\w\s]+)',
            r'sort by ([\w\s]+)',
            r'rank by ([\w\s]+)'
        ]
        
        for pattern in sort_patterns:
            match = re.search(pattern, query)
            if match:
                field = self._standardize_field_name(match.group(1).strip())
                order = 'desc' if 'desc' in query or 'high' in query else 'asc'
                return field, order
                
        return None
    
    def _extract_limit(self, query: str) -> Optional[int]:
        """Extract result limit from query"""
        limit_patterns = [
            r'top (\d+)',
            r'first (\d+)',
            r'limit (\d+)',
            r'return (\d+)'
        ]
        
        for pattern in limit_patterns:
            match = re.search(pattern, query)
            if match:
                return int(match.group(1))
                
        return None
    
    def _extract_grouping(self, query: str) -> Optional[tuple]:
        """Extract grouping information from query"""
        group_patterns = [
            r'cluster (?:all )?stocks by ([\w\s]+)',
            r'group by ([\w\s]+)',
            r'compare ([\w\s]+) across ([\w\s]+)'
        ]
        
        for pattern in group_patterns:
            match = re.search(pattern, query)
            if match:
                field = self._standardize_field_name(match.group(1).strip())
                agg_funcs = ['mean']
                
                if 'average' in query:
                    agg_funcs = ['mean']
                elif 'sum' in query:
                    agg_funcs = ['sum']
                    
                return field, agg_funcs
                
        return None
    
    def _standardize_field_name(self, field: str) -> str:
        """Convert human-readable field names to dataframe columns"""
        # First try exact matches
        for human_name, col_name in self.condition_map.items():
            if human_name.lower() == field.lower():
                return col_name
                
        # Then try partial matches
        for human_name, col_name in self.condition_map.items():
            if human_name.lower() in field.lower():
                return col_name
                
        # Default to returning the original field (will raise error if invalid)
        return field