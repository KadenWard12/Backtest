import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # use this to plot graph as a popup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import strats
import functions
from tqdm import tqdm

def grid_search(df, trades, chosen_strat, balance, risk, multiplier, ticker):
    # Check which strat has been chosen
    if chosen_strat.__name__ == 'sma_cross':
        long_values = []
        while True:
            try:    
                div = int(input('How many long SMAs do you want to test: ').strip())
                for i in range(div):
                    long_SMA = int(input('Choose a value for long SMA: ').strip())
                    long_values.append(long_SMA)
            except ValueError:
                print('Invalid input, please enter an integer') 
                continue
            break

        short_values = {}
        for i in long_values:
            short_values[i] = list(range(1,i))

        results = {}

        for long_SMA, short_list in short_values.items():
            print(f"\nRunning long SMA = {long_SMA}")

            equity = []

            for short_SMA in tqdm(short_list):
                df_copy = df.copy()
                signals = strats.sma_cross(df_copy, ticker, not_sim=False, long_SMA=long_SMA, short_SMA=short_SMA)
                strat_df, trades = functions.backtest(signals, ticker, balance, risk, multiplier, not_sim=False)

                final_equity = trades.iloc[0]['Total PnL %']
                sharpe = trades.iloc[0]['Annualised Sharpe Ratio']

                equity.append((short_SMA, final_equity, sharpe))
            
            results[long_SMA] = equity


        for long_SMA, points in results.items():
            # Unpack tuples
            shorts = [p[0] for p in points]
            equity = [p[1] for p in points]
            sharpe = [p[2] for p in points]

            plt.plot(shorts, equity, label=f'Long SMA: {long_SMA}')

        # x axis
        max_short = max(p[0] for points in results.values() for p in points)
        plt.xlim(0, max_short)
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=20, integer=True))
        
        # Equity plot
        plt.title(f'{ticker} SMA Grid Search Equity Results')
        plt.ylabel('Final Equity %')
        plt.xlabel('Short SMA')
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.legend(fontsize=6, markerscale=0.8, handlelength=1.2)
        plt.axhline(0, linestyle='-', alpha=0.3)
        plt.tight_layout()
        
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
        print('Top 10 settings by equity:')
        print(top10_equity)
        top10_sharpe = results_df.sort_values(by='Sharpe Ratio', ascending=False).head(10).reset_index(drop=True)
        print('Top 10 settings by sharpe:')
        print(top10_sharpe)

        return results
    
def monte_carlo_price_path(df, trades, chosen_strat, balance, risk, multiplier, ticker):
    # Check which strat has been chosen
    if chosen_strat.__name__ == 'sma_cross':
        print('SMA DETECTED')
        # SMA_Cross will use fixed LongMA, and a range of ShortMA
        # up to five LongMA inputs at a time to generate one graph with five plots on the same x axis

    pass