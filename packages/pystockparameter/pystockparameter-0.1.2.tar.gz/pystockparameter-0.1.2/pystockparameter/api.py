import pandas as pd
import os

class StockData:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "data", "merged_stock_data.xlsx")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found at {file_path}")
        self.df = pd.read_excel(file_path)

    def list_symbols(self):
        return self.df["Stock Symbol"].dropna().unique().tolist()

    def get_stock_details(self, symbol):
        filtered = self.df[self.df["Stock Symbol"] == symbol]
        if not filtered.empty:
            return filtered.iloc[0].to_dict()
        else:
            return f"No data found for symbol: {symbol}"
