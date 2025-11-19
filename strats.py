import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import yfinance as yf
import matplotlib
matplotlib.use('TkAgg')  # use this to plot graph as a popup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# SMA crossover signal
def sma_cross(df, short_SMA, long_SMA):
    # Makes sure short SMA < Long SMA
    if short_SMA >= long_SMA:
        raise ValueError('Long SMA must be > short SMA')

    # Add signal column to DataFrame
    df['Short'] = df['Close'].rolling(window=short_SMA).mean() 
    df['Long'] = df['Close'].rolling(window=long_SMA).mean() 
    df['Signal'] = np.where(df['Short'] > df['Long'], 1, 0)

    # Plotting price and moving averages
    plt.ion()
    fig = plt.figure()

    plt.plot(df['Date'], df['Close'], label='Close')
    plt.plot(df['Date'], df['Short'], label=f'{short_SMA} SMA')
    plt.plot(df['Date'], df['Long'], label=f'{long_SMA} SMA')

    plt.title(f'Moving Average Crossover: {short_SMA} SMA & {long_SMA} SMA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    # Improve x-axis
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=30)

    fig.canvas.draw()
    fig.canvas.flush_events()



    return df