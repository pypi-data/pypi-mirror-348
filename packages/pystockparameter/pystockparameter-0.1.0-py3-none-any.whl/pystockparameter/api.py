import pandas as pd
import os

class StockData:
    def __init__(self):
        file_path = os.path.join(os.path.dirname(__file__), "data", "merged_stock_data.xlsx")
        self.df = pd.read_excel(file_path)

    def get_stock_details(self, symbol):
        result = self.df[self.df['Stock Symbol'].str.upper() == symbol.upper()]
        if result.empty:
            return f"No data found for stock symbol: {symbol}"
        return result.to_dict(orient='records')[0]

    def list_symbols(self):
        return self.df['Stock Symbol'].unique().tolist()
