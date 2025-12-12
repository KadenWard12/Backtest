## Backtesting Engine for Trading Strategies

Description:

A modular Python backtesting engine designed for evaluating trading strategies using historical market data.

This engine supports multiple strategies and statistical simulations, of which currently include a SMA crossover strategy, grid search, and Monte Carlo bootstrapped returns simulations. Each run produces performance statistics and relevant plots, which can be seen below in the example outputs. Due to the dynamic structure, new strategies and simulations can easily be developed and appended to the engine.


Folder layout:
```
.
├── README.md
├── data/            # downloaded .csv data for relevent ticker symbols
├── functions.py     # helper functions
├── main.py          # main script, run to execute engine
├── plots/           # plotted data 
├── requirements.txt # virtual environment dependencies
├── sims.py          # statistical simulations 
├── strats.py        # trading strategies to backtest
└── testing.py       # empty folder to test new additions
```

Usage (Linux environment):
- create and run a virtual environment:
  - create with 'python3 -m venv venv'
  - activate with 'source venv/bin/activate'
  - install dependencies with 'pip install -r requirements.txt'
- run main script with 'python3 main.py'
- either choose predownloaded data or retrieve new based on yahoo finance ticker symbols (**_currently downloads two years of hourly data_**)
- input desired strategy to backtest
- input account starting balance
- input risk per trade
- input ATR multiplier, used to set stop losses
- choose a statistical simulation to run

### Example output
<ins>SMA Crossover<ins>

<img width="640" height="480" alt="NVDA_20_50_SMA_cross" src="https://github.com/user-attachments/assets/67c41857-978f-4090-9d31-03920ef5ccec" />

<ins>Backtested Equity Graph<ins>

<img width="640" height="480" alt="AAPL_238_250_SMA_cross_equity_curve" src="https://github.com/user-attachments/assets/a9fa75a0-9ea9-44e1-9abc-0d3a1a882df7" />

<ins>Grid Search on SMA Crossover<ins>

<img width="640" height="480" alt="AAPL_grid_search_equity" src="https://github.com/user-attachments/assets/34b34ecc-60c4-4e9a-ae26-a3bb1fdedf3e" />

<ins>Monte Carlo Bootstrapped Returns<ins>

<img width="640" height="480" alt="AAPL Monte Carlo for sma_cross" src="https://github.com/user-attachments/assets/78b158a9-16e5-4630-8206-8b11d439edb6" />

<ins>Backtest Summary<ins>

<img width="1733" height="373" alt="Example backtesting summary table" src="https://github.com/user-attachments/assets/37bbaaed-eab2-4f51-8cc4-0ea358ab1143" />

<ins>Grid Search Summary<ins>

<img width="508" height="532" alt="Grid search output" src="https://github.com/user-attachments/assets/7863ab07-81e2-4f4f-a188-186714c65ab5" />

<ins>Monte Carlo Bootstrapped Returns Summary<ins>

<img width="470" height="142" alt="EURUSD Monte Carlo Summary " src="https://github.com/user-attachments/assets/565322a4-068f-4767-b65d-1feedd384548" />
