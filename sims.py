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

def monte():
    # Use input for different stratergies
        # SMA_Cross will use fixed LongMA, and a range of ShortMA
        # up to five LongMA inputs at a time to generate one graph with five plots on the same x axis
    pass