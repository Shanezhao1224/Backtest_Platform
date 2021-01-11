# Backtest_Platform

## This is my basic stock backtesting platform

Right now it has the currently capabilities:

1. Read an OHLC bar (Open High Low Close) csv file
2. Use a specific user implemented strategy class
3. Simulate portfolio results over the OHLC file over the date range

A basic BUY open, SELL close (BOSC) strategy is given as an example.
To get started the Tutorial_main.py script is given, which will run the simulation with the BOSC strategy and graph the results.

# Strategies

There are two uploaded simple strategies from when I started. The two algorithms take an list of stocks as input and using IEX (stock broker) API will retrieve stock data and perform the necessary analysis. The two strategies will output an excel spreadsheet with the number of shares to buy for each stock selected based on the analysis. 

The two stratgies are an equal weight SP500 and an High quantitative momentum strategy.

They are located in the Strategy folder and when run will prompt an portfolio balance input and then output the excel spreadsheet with the list of stocks to buy. 

