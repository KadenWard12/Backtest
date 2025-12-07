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

def grid_search(df, trades, chosen_strat, balance, risk, multiplier):
    # Check which strat has been chosen
    #if chosen_strat.__name__ == 'sma_cross':

    pass

def monte_carlo_price_path(df, trades, chosen_strat, balance, risk, multiplier):
    # Check which strat has been chosen
    if chosen_strat.__name__ == 'sma_cross':
        print('SMA DETECTED')
        # SMA_Cross will use fixed LongMA, and a range of ShortMA
        # up to five LongMA inputs at a time to generate one graph with five plots on the same x axis

    pass