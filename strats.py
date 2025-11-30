import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import functions

""" Make sure every strat includes:
- strat_name (for file names will use '_' for spaces)
- strat_title (for chart titles such as equity curves, will not use '_')
- 'Signal' column in the dataframe that has values 1=long, 0=hold, -1=short
- each strat should only input the initial df and ticker, so every other variable to be defined inside
"""

# SMA crossover 
def sma_cross(df, ticker):
    # Define short and long SMA
    while True:
        try:    
            short_SMA = int(input('Choose a value for short SMA: ').strip())
            long_SMA = int(input('Choose a value for long SMA: ').strip())
        except ValueError:
            print('Invalid input, please enter an integer') 
            continue
        if short_SMA <= 0 or long_SMA <= 0:
            print("Please enter integers greater than 0")
            continue
        if short_SMA >= long_SMA:
            print("Long SMA must be greater than Short SMA")
            continue
        break

    # Add signal column to DataFrame
    df['Short'] = df['Close'].rolling(window=short_SMA).mean() 
    df['Long'] = df['Close'].rolling(window=long_SMA).mean() 
    df.loc[0, 'Signal'] = 0 # hold position

    for i in range(1, len(df)):
        if (df.loc[i-1, 'Short'] < df.loc[i-1, 'Long']) and (df.loc[i, 'Short'] > df.loc[i, 'Long']):
            # Buy
            df.loc[i, 'Signal'] = 1
        elif (df.loc[i-1, 'Short'] > df.loc[i-1, 'Long']) and (df.loc[i, 'Short'] < df.loc[i, 'Long']):
            # Sell
            df.loc[i, 'Signal'] = -1
        else:
            # Hold position
            df.loc[i, 'Signal'] = 0
    
    strat_name = f'{ticker}_{short_SMA}_{long_SMA}_SMA_cross'
    df.loc[0, 'name'] = strat_name
    strat_title = f'{ticker} Moving Average Crossover: {short_SMA} SMA & {long_SMA} SMA'
    df.loc[0, 'title'] = strat_title

    # Run ATR
    functions.atr(df)

    # Plotting price and moving averages
    fig, (ax1, ax2) = plt.subplots(
        2,                  # rows
        1,                  # columns
        figsize=(12,8),
        sharex=True,        
        gridspec_kw={'height_ratios':[3,1]}  
    )

    # Main plot
    ax1.plot(df['Date'], df['Close'], label='Close')
    ax1.plot(df['Date'], df['Short'], label=f'{short_SMA} SMA')
    ax1.plot(df['Date'], df['Long'], label=f'{long_SMA} SMA')

    ax1.set_title(f'{strat_title}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    # ATR plot
    ax2.plot(df['Date'], df['ATR'], label='ATR')
    ax2.set_ylabel('ATR')
    ax2.set_xlabel('Date')
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.legend()

    # Improve x-axis
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=30)

    plt.tight_layout() # Remove white space
    ax1.set_xlim(df['Date'].iloc[0], df['Date'].iloc[-1]) # Set graph to origin
    plt.subplots_adjust(hspace=0) # remove space inbetween ATR and main plot
    plt.savefig(f'plots/{strat_name}.png', dpi=200)
    plt.close()

    return df