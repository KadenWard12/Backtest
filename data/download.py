import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

import yfinance as yf

while True:
    ticker = input('Input the ticker symbol: ')
    df = yf.download(ticker, start="2023-01-01", end='2025-01-01')
    if df.empty:
        print('No data found for that ticker')
    else:
        print('Data successfully stored')
        break

print(df.head(4))
print(df[['Open', 'High', 'Close']].head(5))

df.reset_index(inplace=True)
print(df.head(4))

print(df[['Date', 'High', 'Close']].head(5))
df.to_csv(f"{ticker}.csv", index=False)

print(df['Date'].iloc[[0,1,2]])
#print(df['Date'].head(3))