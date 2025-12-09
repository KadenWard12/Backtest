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

def test(df, trades, ticker, balance, risk, multiplier):
    # Prompt for number of simulations
    while True:
        try:    
            num_sims = int(input('How many simulations do you want to run: ').strip())
            if num_sims > 0:
                break
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
    plt.plot(percentile_5, color='red', linestyle='--', linewidth=1.2, label='5th Percentile')
    plt.plot(percentile_95, color='green', linestyle='--', linewidth=1.2, label='95th Percentile')
    plt.legend()

    plt.title('Monte Carlo Simulated Equity Curves')
    plt.xlabel('Trade Number')
    plt.ylabel('Equity %')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.axhline(0, linestyle='-', color='black', linewidth=0.5)
    plt.tight_layout()


    plt.savefig('plots/{ticker} Monte Carlo', dpi=200)
    plt.close()

test(df, trades, ticker, balance, risk, multiplier)