## Backtesting Engine for Trading Strategies

files include:
- data folder holds all downloaded .csv data for relevent ticker symbols
- plots folder holds all plotted data
- venv folder holds virtual environment information in order to run the engine
- run main.py to execute programme
- functions.py contains all supporting functions 
- sims.py contains statistical simulations such as grid search and monte carlo bootstrapped returns
- strats.py contains trading strategies to backtest
- testing.py, empty folder to test new additions
  
Intructions (Linux environment):
- open virtual environment with 'source venv/bin/activate' 
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
