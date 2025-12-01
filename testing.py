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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('AAPL.csv')
trades = pd.read_csv('trades.csv')
ticker = 'AAPL'

def test(df, trades, ticker):
    while True:
        try:    
            long_SMA = int(input('Choose a value for long SMA starting position: ').strip())
            div = int(input('How many long SMA variations do you want: ').strip())
        except ValueError:
            print('Invalid input, please enter an integer') 
            continue
        break
    
    long_values = []
    long1 = int(long_SMA / div)
    long_values.append(long1)

    if div != 1:
        for i in range(2, div + 1):
            long_values.append(long1 * i)

    print(long_values)

    short_values = {}
    for i in long_values:
        short_values[i] = list(range(1,i))

    print(short_values)

    results = {}
    for long_SMA, short_list in short_values.items():

        print(f"\nRunning long SMA = {long_SMA}")

        for short_SMA in short_list:
            signals = strats.sma_cross(df, ticker, not_sim=False, long_SMA=long_SMA, short_SMA=short_SMA)
            result = functions.backtest(signals, ticker, not_sim=False)
        

test(df, trades)