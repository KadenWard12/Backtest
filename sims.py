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

def grid_search(df, trades, chosen_strat, balance, risk, multiplier, ticker, df_copy):
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

            plt.plot(shorts, equity, linewidth=1, label=f'Long SMA: {long_SMA}')

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
        plt.axhline(0, linestyle='-', color='black', linewidth=1, alpha=0.8)
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
    
def monte_carlo_bootstrap(df, trades, chosen_strat, balance, risk, multiplier, ticker, df_copy):
     while True:
        # Prompt to keep the same input or not
        while True:
            x = input('Do you want to use the previously entered strategy inputs? [y/n]: ').strip().upper()
            if len(trades) == 0:
                print('Strategy produced no trades to analyse, choose different inputs.')
                print()
            if x in ('Y', 'YES') and len(trades) > 0:
                break
            elif x in ('N', 'NO') or len(trades) == 0:
                while True:
                    df_copy2 = df_copy
                    df = chosen_strat(df_copy2, ticker)
                    df, trades = functions.backtest(df, ticker, balance, risk, multiplier)
                    if len(trades) == 0:
                        print('Strategy produced no trades to analyse, choose different inputs.')
                        continue
                    else:
                        break
                break
            else:
                print('Incorrect answer')
                continue
    

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
        
        returns = trades['Return'].dropna().iloc[1:].values 
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
        
        print('Building chart...')
        for curve in tqdm(sim_curves):
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

        print()
        print('Analysing data...')
        for curve in tqdm(sim_returns):
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