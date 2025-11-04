import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os

files = [f for f in os.listdir('data') if f.endswith('.csv')]
print(f'Available ticker symbols: {files}')

while True:
    chosen = input('Choose ticker symbol: ')
    if f'{chosen}.csv' in files:
        print(f'{chosen} data loading...')
        break
    else:
        print('Invalid ticker')

#clean_chosen = clean_csv(chosen)

data = pd.read_csv(f'data/{chosen}.csv', skiprows=3, parse_dates=['Date'])
print(start)