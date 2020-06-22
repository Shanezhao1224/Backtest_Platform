# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:02:04 2020

@author: Xzhao
"""
from Platform_class import BT_platform
from BOSC_strategy import BOSC
from datetime import datetime
import matplotlib.pyplot as plt

Backtest_platform = BT_platform()
BOSC_strat = BOSC()

filepath = r'C:\Users\Xzhao\source\Backtrader\csv_files\SPY_1993_2020.csv'
fromdate = datetime(1900,1,1)
todate = datetime(2020,6,30)
Backtest_platform.csv_filepath(filepath)
Backtest_platform.startdate(fromdate)
Backtest_platform.enddate(todate)
Backtest_platform.set_balance(10000.0)
Backtest_platform.set_strategy(BOSC_strat)
Backtest_platform.run()

xdata = Backtest_platform.portfolio_x_data()
ydata = Backtest_platform.portfolio_y_data()
plt.plot(xdata,ydata,label = "Buy Open, Sell Close")
plt.title("Portfolio performance for a SPY")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.legend()
plt.show()