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
import sims

# List all .csv files
files = [f for f in os.listdir('data') if f.endswith('.csv')]
print(f'Available ticker symbols: {files}')

# Ensure plot folder exists
if not os.path.exists('plots'):
    os.makedirs('plots')

# Prompt a file to be chosen
while True:
    if len(files) > 0:
        x = input('Do you want to use existing data [y/n]: ').strip().upper()
        # Choose existing or not
        if x in ('Y', 'YES'):
            while True:
                ticker = input('Input existing ticker symbol: ').strip().upper()
                if f'{ticker}.csv' in files:
                    print(f'Using data for {ticker}')
                    for i in range(3):
                        print('...')
                    break
                else:
                    print('Ticker symbol not found in existing data.')
            break
        elif x in ('N', 'NO'):
            ticker = functions.download_data()
            break
        else:
            print('Incorrect answer')
            continue
     # If no files prompt for new ticker symbol
    else:
        ticker = functions.download_data()
        break

# Choose a strategy to test
strategies = inspect.getmembers(strats, inspect.isfunction)
strategy_names = {name.lower(): func for name, func in strategies}

# Check if stratergies are available
if len(strategies) > 0:
    print('Available strategies to test:')
    for name, func in strategies:
        print(name)  
    while True:
        strat = input('Choose a strategy: ').strip().lower()
        # Check if chosen strat matches available
        if strat in strategy_names:
            print(f'Using {strat} strategy')
            for i in range(3):
                print('...')
            chosen_strat = strategy_names[strat]
            break
        else:
            print('Strategy not found, try again.')
else:
    print('No strategies found.')
    sys.exit()
    
df = pd.read_csv(f'data/{ticker}.csv')

# Run strategy
result_df = chosen_strat(df, ticker)

# Backtest
try:
    df, trades = functions.backtest(result_df, ticker)
    print(trades)
    print('...')
except ValueError as error:
    for i in range(3):
        print('...')
    print(f'{error}, different DataFrame needed')
    print('...')

df.to_csv('results.csv', index=False)
trades.to_csv('trades.csv', index=False)

# Run a statistical simulation
simulations = inspect.getmembers(sims, inspect.isfunction)
simulation_names = {name.lower(): func for name, func in simulations}
sim_answer = False
# yes or no for running sim, make bool flag
while True:
    if len(simulations) > 0:
        x = input('Do you want to run a simulation [y/n]: ').strip().upper()
        if x in ('Y', 'YES'):
            sim_answer = True
            break
        elif x in ('N', 'NO'):
            break
        else:
            print('Incorrect answer')
            continue

# Choose a simulation to test
if sim_answer:
    # Check if simulations are available
    if len(simulations) > 0:
        print('Available simulations to use:')
        for name, func in simulations:
            print(name)  
        while True:
            sim = input('Choose a simulation: ').strip().lower()
            # Check if chosen sim matches available
            if sim in simulation_names:
                print(f'Using {sim} simulation')
                for i in range(3):
                    print('...')
                chosen_sim = simulation_names[sim]
                break
            else:
                print('Simulation not found, try again.')
    else:
        print('No simulations found.')
        sys.exit()

    chosen_sim(df, trades, chosen_strat)

# Closes script
functions.exit_script()