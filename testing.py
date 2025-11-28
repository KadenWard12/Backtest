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

    # Calculate ATR if not done already
    if 'ATR' not in df:
        atr(df)

    # Prompt starting balance
    while True:
        try:    
            balance = int(input('Input a starting balance: ').strip())
            if balance > 0:
                break
            else:
                print('Please enter integer greater than 0')
        except ValueError:
            print('Invalid input, please enter a number')        

    # Prompt risk
    while True:
        try:    
            risk = float(input('Input risk %: ').strip())
            if risk > 0 and risk <= 100:
                break
            else:
                print('Please enter number greater than 0 and less than or equal to 100')
        except ValueError:
            print('Invalid input, please enter a number')
    
    # Prompt ATR multiplier    
    while True:
        try:
            multiplier = float(input('Input ATR multiplier: ').strip())
            if multiplier > 0:
                break
            else:
                print('Please enter number greater than 0')
        except ValueError:
            print('Invalid input, please enter a number') 

    
    # Create empty trade df
    trades = pd.DataFrame(columns=['Date', 'Time', 'Type', 'PnL'])

    dollar_pip = 0
    row_index = 0
    first_candle = True
    # Loop through each row of the dataframe
    for i in range(1, len(df)):
        # Set the distance moved by each candle
        df.loc[i, 'candle_move'] = df.loc[i, 'Close'] - df.loc[i-1, 'Close']
        
        # Check for long
        if df.loc[i, 'Signal'] == 1:
            if not first_candle:
                # PnL for each candle
                df.loc[i, 'dollar_candle'] = dollar_pip * df.loc[i, 'candle_move']
                # Sum of PnL for trade
                trades.loc[row_index, 'PnL'] = trades.loc[row_index, 'PnL'] + df.loc[i, 'dollar_candle']
                # Reset trade
                first_candle = True
                row_index += 1
            # Variables
            pips = df.loc[i, 'ATR'] * multiplier
            stop = df.loc[i, 'Close'] - pips
            dollar_pip = (balance * (risk/100)) / pips
            # Append to trades dataframe
            if 'Date' in df:
                trades.loc[row_index, 'Date'] = df.loc[i, 'Date']
            if 'Time' in df:
                trades.loc[row_index, 'Time'] = df.loc[i, 'Time']
            trades.loc[row_index, 'Type'] = 'Buy'

        # Check for short
        elif df.loc[i, 'Signal'] == -1:
            if not first_candle:
                # PnL for each candle
                df.loc[i, 'dollar_candle'] = dollar_pip * df.loc[i, 'candle_move']
                # Sum of PnL for trade
                trades.loc[row_index, 'PnL'] = trades.loc[row_index, 'PnL'] + df.loc[i, 'dollar_candle']
                # Reset trade
                first_candle = True
                row_index += 1
            # Variables
            pips = df.loc[i, 'ATR'] * multiplier
            stop = df.loc[i, 'Close'] + pips
            dollar_pip = (balance * (risk/100)) / pips
            # Append to trades dataframe
            if 'Date' in df:
                trades.loc[row_index, 'Date'] = df.loc[i, 'Date']
            if 'Time' in df:
                trades.loc[row_index, 'Time'] = df.loc[i, 'Time']
            trades.loc[row_index, 'Type'] = 'Sell'

        # Check for hold
        elif df.loc[i, 'Signal'] == 0:
            if first_candle:
                trades.loc[row_index, 'PnL'] = 0
                first_candle = False
            # PnL for each candle
            df.loc[i, 'dollar_candle'] = dollar_pip * df.loc[i, 'candle_move']
            # Sum of PnL for trade
            trades.loc[row_index, 'PnL'] = trades.loc[row_index, 'PnL'] + df.loc[i, 'dollar_candle']



        # 5. Process entry (size position, set stop-loss)



        # 6. Check for exit event (signal flips to sell)



        # 7. Process signal-based exit (close trade)



        # 8. Check for stop-loss hit



        # 9. Process stop-loss exit



        # 10. Record state for this row (equity, pnl, etc.)

    

    # 11. Return the full dataframe
    return df, trades
                

# Catch errors
try:
    df, trades = test(df)
except ValueError as error:
    for i in range(3):
        print('...')
    print(f'{error}, different DataFrame needed')
    print('...')



print(df.loc[100:300, ['Date', 'Signal']])
print(trades.head(50))

"""
Having issues with setting the right row in the trades df
"""