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

df = pd.read_csv('data/AAPL.csv')
trades = pd.read_csv('trades.csv')
ticker = 'AAPL'
balance = 50000
risk = 1
multiplier = 1.5

def test(df, trades, ticker, balance, risk, multiplier):
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

        equity = []

        for short_SMA in short_list:
            print(f"\nRunning short SMA = {short_SMA}")
            df_copy = df.copy(deep=True)
            signals = strats.sma_cross(df_copy, ticker, not_sim=False, long_SMA=long_SMA, short_SMA=short_SMA)
            strat_df, trades = functions.backtest(signals, ticker, balance, risk, multiplier, not_sim=False)

            final_equity = trades.iloc[-1]['Cumulative %']
            sharpe = trades.iloc[0]['Annualised Sharpe Ratio']

            equity.append((short_SMA, final_equity, sharpe))
        
        results[long_SMA] = equity

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    for long_SMA, points in results.items():
        # Unpack tuples
        shorts = [p[0] for p in points]
        equity = [p[1] for p in points]
        sharpe = [p[2] for p in points]

        ax1.plot(shorts, equity, label=f'Long SMA: {long_SMA}')
        ax2.plot(shorts, sharpe, label=f'Long SMA: {long_SMA}')

    # x axis
    max_short = max(p[0] for points in results.values() for p in points)
    ax1.set_xlim(0, max_short)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=20, integer=True))
    
    # Equity plot
    ax1.set_title(f'{ticker} SMA Grid Search Equity Results')
    ax1.set_ylabel('Final Equity %')
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(fontsize=6, markerscale=0.8, handlelength=1.2)
    ax1.axhline(0, linestyle='-', alpha=0.3)

    # Sharpe plot
    ax2.set_ylabel('Sharpe Ratio')
    ax2.set_xlabel('Short SMA')
    ax2.set_ylim(-0.5, None)   # None = autoscale top
    ax2.grid(True, linestyle='--', alpha=0.4)
    ax2.axhline(0, linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    plt.savefig(f'plots/{ticker}_grid_search_equity.png', dpi=200)
    plt.close()

    # Print top 10 equity returns
    top_values = []
    for long_SMA, points in results.items():
        for short_SMA, equity, sharpe in points:
            top_values.append({
                'Long SMA': long_SMA,
                'Short SMA': short_SMA,
                'Final Equity %': round(float(equity), 2),
                'Sharpe Ratio': round(float(sharpe), 2)
            })
    
    results_df = pd.DataFrame(top_values)
    top10_equity = results_df.sort_values(by='Final Equity %', ascending=False).head(10).reset_index(drop=True)
    print(top10_equity)
    top10_sharpe = results_df.sort_values(by='Sharpe Ratio', ascending=False).head(10).reset_index(drop=True)
    print(top10_sharpe)

    return results

test(df, trades, ticker, balance, risk, multiplier)