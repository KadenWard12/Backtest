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
    trades = pd.DataFrame(columns=['Date', 'Time', 'Closed', 'Type', 'PnL', 'SL Hit','Cumalative PnL', 'W/L', 'Total PnL'])

    dollar_pip = 0
    row_index = 0
    first_candle = True
    buy = False
    sell = False
    # Loop through each row of the dataframe
    for i in range(1, len(df)):
        # Set the distance moved by each candle
        df.loc[i, 'candle_move'] = df.loc[i, 'Close'] - df.loc[i-1, 'Close']
        
        # Check for long
        if df.loc[i, 'Signal'] == 1:
            if not first_candle:
                # PnL for each candle
                df.loc[i, 'dollar_candle'] = dollar_pip * df.loc[i, 'candle_move'] * -1
                # Sum of PnL for trade
                trades.loc[row_index, 'PnL'] = trades.loc[row_index, 'PnL'] + df.loc[i, 'dollar_candle']
                # Date trade closed
                trades.loc[row_index, 'Closed'] = df.loc[i, 'Date']
                # Stoploss not hit
                trades.loc[row_index, 'SL Hit'] = False
                # Reset trade
                first_candle = True
                row_index += 1
            # Variables
            pips = df.loc[i, 'ATR'] * multiplier
            stop = df.loc[i, 'Close'] - pips
            dollar_pip = (balance * (risk/100)) / pips
            # Append to trades dataframe
            if 'Date' in df.columns:
                trades.loc[row_index, 'Date'] = df.loc[i, 'Date']
            if 'Time' in df.columns:
                trades.loc[row_index, 'Time'] = df.loc[i, 'Time']
            trades.loc[row_index, 'Type'] = 'Buy'
            sell = False
            buy = True

        # Check for short
        elif df.loc[i, 'Signal'] == -1:
            if not first_candle:
                # PnL for each candle
                df.loc[i, 'dollar_candle'] = dollar_pip * df.loc[i, 'candle_move']
                # Sum of PnL for trade
                trades.loc[row_index, 'PnL'] = trades.loc[row_index, 'PnL'] + df.loc[i, 'dollar_candle']
                # Date trade closed
                trades.loc[row_index, 'Closed'] = df.loc[i, 'Date']
                # Stoploss not hit
                trades.loc[row_index, 'SL Hit'] = False
                # Reset trade
                first_candle = True
                row_index += 1
            # Variables
            pips = df.loc[i, 'ATR'] * multiplier
            stop = df.loc[i, 'Close'] + pips
            dollar_pip = (balance * (risk/100)) / pips
            # Append to trades dataframe
            if 'Date' in df.columns:
                trades.loc[row_index, 'Date'] = df.loc[i, 'Date']
            if 'Time' in df.columns:
                trades.loc[row_index, 'Time'] = df.loc[i, 'Time']
            trades.loc[row_index, 'Type'] = 'Sell'
            sell = True
            buy = False

        # Check for hold
        elif df.loc[i, 'Signal'] == 0:
            if first_candle and (buy or sell):
                trades.loc[row_index, 'PnL'] = 0
                first_candle = False
            if buy:
                # PnL for each candle
                df.loc[i, 'dollar_candle'] = dollar_pip * df.loc[i, 'candle_move']
                # Sum of PnL for trade
                trades.loc[row_index, 'PnL'] = trades.loc[row_index, 'PnL'] + df.loc[i, 'dollar_candle']
            if sell:
                # PnL for each candle
                df.loc[i, 'dollar_candle'] = dollar_pip * df.loc[i, 'candle_move'] * -1
                # Sum of PnL for trade
                trades.loc[row_index, 'PnL'] = trades.loc[row_index, 'PnL'] + df.loc[i, 'dollar_candle']

        # Check if stoploss has been hit
        if buy:
            if df.loc[i, 'Low'] <= stop:
                trades.loc[row_index, 'PnL'] = pips * dollar_pip * -1
                # Date trade closed
                trades.loc[row_index, 'Closed'] = df.loc[i, 'Date']
                # Stoploss not hit
                trades.loc[row_index, 'SL Hit'] = True
                # Reset trade
                buy = False
                first_candle = True
                row_index += 1
        if sell:
            if df.loc[i, 'High'] >= stop:
                trades.loc[row_index, 'PnL'] = pips * dollar_pip * -1
                # Date trade closed
                trades.loc[row_index, 'Closed'] = df.loc[i, 'Date']
                # Stoploss not hit
                trades.loc[row_index, 'SL Hit'] = True
                # Reset trade
                sell = False
                first_candle = True
                row_index += 1

    # Last columns
    trades.loc[0, 'Cumalative PnL'] = trades.loc[0, 'PnL']
    for i in range(1, len(trades)):
        trades.loc[i, 'Cumalative PnL'] = trades.loc[i-1, 'Cumalative PnL'] + trades.loc[i, 'PnL']
    trades.loc[0, 'Total PnL'] = trades.iloc[-1]['Cumalative PnL']
    trades.loc[0, 'W/L'] = (trades['PnL'] >= 0).sum() / len(trades)

    return df, trades
                
# Catch errors
try:
    df, trades = test(df)
except ValueError as error:
    for i in range(3):
        print('...')
    print(f'{error}, different DataFrame needed')
    print('...')



print(df[['Date', 'Signal']])
df[['Date', 'Signal']].to_csv('signal.csv')
print(trades.head(50))

"""
plot equity curve
sharpe ratio
max drawdown
anything else???
"""