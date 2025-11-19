import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import yfinance as yf
import functions
import strats
import inspect
import sys

df = pd.read_csv('results.csv')
"""
Parameters:
    - df: DataFrame with price and signal
    - price_col: column name of price (default "Close")
    - signal_col: column name of signals (default "Signal", 1=buy,0=flat)

Returns:
    - df: DataFrame with new columns:
    - Return
    - Strategy_Return
    - Cumulative_Return
    - Cumulative_Strategy
    """

#function
if Signal not in df.columns:
    raise ValueError('Signal column not found in DataFrame')

# Calculates daily returns
df['Return'] = (df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1)

# Multiplies by position to show what return the stratergy nets
df['Strategy_Return'] = df['Return'] * df['Signal'].shift(1)







