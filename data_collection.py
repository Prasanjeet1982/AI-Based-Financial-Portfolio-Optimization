import yfinance as yf
from pandas import DataFrame
from typing import List

def fetch_data(tickers: List[str], start: str, end: str) -> DataFrame:
    try:
        data = yf.download(tickers, start=start, end=end)['Adj Close']
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
