import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import pandas as pd
import numpy as np
import os
import yfinance as yf
from functions import download_data

df = pd.read_csv(f'data/AAPL.csv')
df = df.drop([0, 1])

df = df.reset_index(drop=True)

df['Date'] = pd.to_datetime(df['Date'])

print(df.head(5))