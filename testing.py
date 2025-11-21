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


#function
def test(df):
    # Catch errors
    if 'Signal' not in df.columns:
        raise ValueError('Signal column not found in DataFrame')

    if 'Close' not in df.columns:
        raise ValueError('Price column not found in DataFrame')
    """
    if 'Position' not in df.columns:
        raise ValueError('Position column not found in DataFrame')
    """
    # Calculates daily returns of asset
    df['Daily_pnl'] = (df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1)

    # Calculates the times in which the strat enters, holds, and exits
    # PUT THIS IN THE STRAT FILE SO EACH STRAT HAS DIFFERENT POSITIONS, E.G SELLS
    prev_signal = df.loc[0, 'Signal']
    df['Position'] = 0

    for i in range(len(df)):
        current_signal = df.loc[i, 'Signal']

        if prev_signal == 0 and current_signal == 1:
            df.loc[i, 'Position'] = 1
        elif prev_signal == 1 and current_signal == 0:
            df.loc[i, 'Position'] = 0
        else:
            df.loc[i, 'Position'] = df.loc[i-1, 'Position'] if i > 0 else 0

        prev_signal = current_signal

    # Multiplies by position to show what return the stratergy nets
    df['Strategy_pnl'] = df['Daily_pnl'] * df['Position'].shift(1)

    # Works out return if just bought and held for the the ran time 
    for i in range(len(df)):
        if i == 0:
            df.loc[i, 'Control_pnl'] = 0
        else:
            df.loc[i, 'Control_pnl'] = df.loc[i, 'Daily_pnl'] + df.loc[i-1, 'Control_pnl']
                
    # Calculates the whole stratergy return, combining all stratergy returns
    for i in range(len(df)):
        if i == 0:
            df.loc[i, 'Cumalative_pnl'] = 0
        else:
            df.loc[i, 'Cumalative_pnl'] = df.loc[i, 'Strategy_pnl'] + df.loc[i-1, 'Cumalative_pnl']

# Catch errors
try:
    test(df)
except ValueError as error:
    for i in range(3):
        print('...')
    print(f'{error}, different DataFrame needed')
    print('...')


print(df.head(50))

""" 
need to do trading or investing mode, 
trading has non cumalative addition of pnl
investing has cumalitive mode 

"""