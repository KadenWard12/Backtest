import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import yfinance as yf
from functions import download_data

# List all .csv files
files = [f for f in os.listdir('data') if f.endswith('.csv')]
print(f'Available ticker symbols: {files}')

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
                    break
                else:
                    print('Ticker symbol not found in existing data.')
            break
        elif x in ('N', 'NO'):
            ticker = download_data()
            break
        else:
            print('Incorrect answer')
            continue
     # If no files prompt for new ticker symbol
    else:
        ticker = download_data()

