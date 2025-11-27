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

# Ensure plot folder exists
if not os.path.exists('plots'):
    os.makedirs('plots')

# SMA crossover signal
def sma_cross(df, short_SMA, long_SMA):
    # Makes sure short SMA < Long SMA
    if short_SMA >= long_SMA:
        raise ValueError('Long SMA must be > short SMA')

    # Add signal column to DataFrame
    df['Short'] = df['Close'].rolling(window=short_SMA).mean() 
    df['Long'] = df['Close'].rolling(window=long_SMA).mean() 
    df['Signal'] = np.where(df['Short'] > df['Long'], 1, 0)

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

    ax1.set_title(f'Moving Average Crossover: {short_SMA} SMA & {long_SMA} SMA')
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
    plt.savefig(f'plots/{short_SMA}_{long_SMA}_SMA_cross.png', dpi=200)
    plt.close()

    return df