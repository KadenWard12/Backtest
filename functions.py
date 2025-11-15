import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import yfinance as yf

# Download price data as .csv
def download_data():
    while True:
        ticker = input('Choose new ticker symbol: ').strip().upper()
        df = yf.download(ticker, start="2023-01-01", end='2025-01-01')
        if df.empty:
            print('No data found for that ticker')
            continue
        else:
            print(f'{ticker} data successfully stored')
            df.to_csv(f"data/{ticker}.csv")
            break
    return ticker

def generate_signals(df, short_window, long_window):
    """Create trading signals (e.g., moving average crossover)."""
    
    pass

def compute_returns(df):
    """Calculate daily and cumulative returns."""
    pass

def backtest(df):
    """Combine signals and returns to simulate a trading strategy."""
    pass

