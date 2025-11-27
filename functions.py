import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import strats
import sys



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
            for i in range(3):
                print('...')
            df.reset_index(inplace=True)
            df.to_csv(f"data/{ticker}.csv", index=False)
            clean_csv(ticker)
            break
    return ticker

# Remove weird first row 
def clean_csv(ticker):
    df = pd.read_csv(f'data/{ticker}.csv')
    df = df.drop(index=0).reset_index(drop=True)
    df.to_csv(f"data/{ticker}.csv", index=False)

def atr(df, period=14):
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(period).mean()
    return df

def compute_returns(df):
    """Calculate daily and cumulative returns."""
    pass

def backtest(df):
    """Combine signals and returns to simulate a trading strategy."""
    pass

def exit_script():
    print('Data analysis finished')

    while True:
        user_input = input("Press Enter to exit script...")

        if user_input == "":
            sys.exit()
        else:
            print('Invalid input, script not closed')

