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

# Compute ATR
def atr(df, period=14):
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(period).mean()
    return df

# Backtest for PnL, drawdown, equity curve, sharpe ratio etc
def backtest(df, ticker):
    print('Backtesting...')
    for i in range(3):
        print('...')
        
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
            print('Invalid input, please enter an integer')        

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
    trades = pd.DataFrame(columns=['Date', 'Time', 'Closed', 'Type', 'PnL', 'PnL %', 'SL Hit', 'Cumulative PnL', 'Cumulative %', 'W/L', 'Total PnL', 'Total PnL %'])

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

    # Cumulative PnL for equity curve
    trades.loc[0, 'Cumulative PnL'] = trades.loc[0, 'PnL']
    for i in range(1, len(trades)):
        trades.loc[i, 'Cumulative PnL'] = trades.loc[i-1, 'Cumulative PnL'] + trades.loc[i, 'PnL']
    for i in range(len(trades)):
        trades.loc[i, 'Cumulative %'] = (trades.loc[i, 'Cumulative PnL'] / balance) * 100

    # Add new empty row at index=0 for equity curve
    new_row = {col: 0 for col in trades.columns}   # keeps correct order
    trades = pd.concat([pd.DataFrame([new_row]), trades], ignore_index=True)
    trades['Cumulative %'] = pd.to_numeric(trades['Cumulative %'], errors='coerce')

    # W/L, PnL %, Total PnL, Total PnL %
    trades['PnL %'] = (trades['PnL'] / balance) * 100
    trades.loc[0, 'Total PnL'] = trades.iloc[-1]['Cumulative PnL']
    trades.loc[0, 'Total PnL %'] = (trades.loc[0, 'Total PnL'] / balance) * 100 
    trades.loc[0, 'W/L'] = (trades['PnL'] > 0).sum() / (len(trades) - 1)

    # Plot equity curve
    plt.plot(trades.index, trades['Cumulative %'], label='Equity')
    plt.legend()
    plt.xlim(0, len(trades)-1)
    # Zero line
    plt.axhline(0, linestyle='--', alpha=0.5)
    plt.title(f'{df.loc[0, 'title']} equity curve')
    plt.xlabel('Trade number')
    plt.ylabel('Equity / %')
    plt.grid(True, linestyle='--', alpha = 0.3)
    # Integer ticks 
    plt.xticks(range(len(trades)))

    # Shading below and above zero line
    y = trades['Cumulative %']
    x = trades.index
    plt.fill_between(x, y, 0, where=(y >= 0), color='green', alpha=0.3, interpolate=True)
    plt.fill_between(x, y, 0, where=(y <= 0), color='red', alpha=0.3, interpolate=True)

    plt.tight_layout() # Remove white space
    plt.savefig(f'plots/{df.loc[0, 'name']}_equity_curve.png', dpi=200)
    plt.close()

    # Max drawdown
    equity = trades['Cumulative %'] + 100
    cummax = equity.cummax()
    drawdown = (equity - cummax) / cummax * 100
    trades.loc[0, 'Max Drawdown %'] = drawdown.min()
        
    # Sharpe ratio annualised
    sharpe_pnl = trades.iloc[1:]['PnL %'] / 100
    mean_pnl = sharpe_pnl.mean()
    std_pnl = sharpe_pnl.std()

    # Avoids dividing by 0 error
    if std_pnl == 0:
        sharpe_ratio = 0
    else:
        sharpe_ratio = mean_pnl / std_pnl

    # Annualisation
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = df['Date'].iloc[0]
    end_date   = df['Date'].iloc[-1]
    days = (end_date - start_date).days

    if days == 0:
        trades_per_year = len(trades) - 1
    else:
        trades_per_year = ((len(trades) - 1) / days) * 365

    annual_sharpe_ratio = sharpe_ratio * np.sqrt(trades_per_year)
    trades.loc[0, 'Annualised Sharpe Ratio'] = annual_sharpe_ratio
    
    return df, trades
    
def exit_script():
    print('Data analysis finished')
    while True:
        user_input = input("Press Enter to exit script...")

        if user_input == "":
            sys.exit()
        else:
            print('Invalid input, script not closed')

