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
from tqdm import tqdm

df = pd.read_csv('data/AAPL.csv')
trades = pd.read_csv('trades.csv')
ticker = 'AAPL'
balance = 50000
risk = 1
multiplier = 1.5
chosen_strat = strats.sma_cross

def test(df, trades, ticker, balance, risk, multiplier):
    while True:
        # Prompt for number of simulations
        while True:
            try:    
                num_sims = int(input('How many simulations do you want to run, max 10,000: ').strip())
                if num_sims > 0 and num_sims <= 10000:
                    break
                elif num_sims > 10000:
                    print('Enter a number less than 10,000')
                else:
                    print('Please enter integer greater than 0')
            except ValueError:
                print('Invalid input, please enter an integer') 
        
        returns = trades['Return'].iloc[1:].values 
        sim_returns = []

        for i in range(num_sims):
            equity = balance
            equity_curve = [equity]
            sampled_returns = np.random.choice(returns, size=len(returns), replace=True)
            for r in sampled_returns:
                equity *= (1 + r)  # sequential compounding
                equity_curve.append(equity)
            sim_returns.append(equity_curve)

        sim_returns = np.array(sim_returns)
        sim_curves = (sim_returns - balance) / balance * 100
        
        for curve in sim_curves:
            plt.plot(curve, color='blue', alpha=0.2, linewidth=0.6)
        # x axis
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=20, integer=True))
        plt.xlim(0, len(trades)-1)

        # Calculate statistics
        mean = np.mean(sim_curves, axis=0)
        percentile_5 = np.percentile(sim_curves, 5, axis=0)
        percentile_95 = np.percentile(sim_curves, 95, axis=0)
        plt.plot(mean, color='orange', linewidth=1.5, label='Mean')
        plt.plot(percentile_5, color='red', linestyle='-', linewidth=1.5, label='5th Percentile')
        plt.plot(percentile_95, color='green', linestyle='-', linewidth=1.5, label='95th Percentile')
        plt.legend()

        plt.title(f'{ticker} {chosen_strat.__name__} Monte Carlo Simulated Equity Curves')
        plt.xlabel('Trade Number')
        plt.ylabel('Equity %')
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.axhline(0, linestyle='-', color='black', linewidth=0.5)
        plt.tight_layout()

        plt.savefig(f'plots/{ticker} Monte Carlo for {chosen_strat.__name__}', dpi=200)
        plt.close()

        # Summary table
        def compute_max_drawdown(equity_curve):
            peak = np.maximum.accumulate(equity_curve)
            drawdowns = (equity_curve - peak) / peak
            return drawdowns.min() * 100

        def compute_sharpe(returns):
            # Avoids dividing by 0 error
            if returns.std() == 0:
                sharpe_ratio = 0
            else:
                sharpe_ratio = returns.mean() / returns.std()

            # Annualisation
            df['Date'] = pd.to_datetime(df['Date'])
            start_date = df['Date'].iloc[0]
            end_date   = df['Date'].iloc[-1]
            days = (end_date - start_date).days

            if days == 0:
                trades_per_year = len(trades) - 1
            else:
                trades_per_year = ((len(trades) - 1) / days) * 365

            return sharpe_ratio * np.sqrt(trades_per_year)

        final_equities = []
        sharpes = []
        max_drawdowns = []

        for curve in sim_returns:
            final_equities.append((curve[-1] - balance) / balance * 100)

            step_returns = curve[1:] / curve[:-1] - 1
            sharpes.append(compute_sharpe(step_returns))

            max_drawdowns.append(compute_max_drawdown(curve))

        summary = pd.DataFrame({
            "Equity Gain %": [
                np.mean(final_equities),
                np.percentile(final_equities, 5),
                np.percentile(final_equities, 95)
            ],
            "Sharpe Ratio": [
                np.mean(sharpes),
                np.percentile(sharpes, 5),
                np.percentile(sharpes, 95)
            ],
            "Max Drawdown %": [
                np.mean(max_drawdowns),
                np.percentile(max_drawdowns, 5),
                np.percentile(max_drawdowns, 95)
            ]
        }, index=["Mean", "5%", "95%"])

        print("\nMonte Carlo Summary:")
        print(summary)
        print()

        no = False
        while True:
            x = input('Do you want to run another Monte Carlo simulation? [y/n]: ').strip().upper()
            if x in ('Y', 'YES'):
                break
            elif x in ('N', 'NO'):
                no = True
                break
            else:
                print('Incorrect answer')
                continue
        if no:
            break

test(df, trades, ticker, balance, risk, multiplier)