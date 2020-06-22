# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:14:49 2020

@author: Xzhao
"""
from datetime import datetime
import pandas
from Order_class import Order

class BT_platform:
    def __init__(self):
        pass
    #define a CSV filepath to open
    def csv_filepath(self, filepath):
        self.csv_filepath = filepath
    #set the startdate for CSV file
    def startdate(self,startdate):
        self.startdate = startdate
    #set the enddate for the CSV file
    def enddate(self,enddate):
        self.enddate = enddate
    #functions to set starting balance and get the current money
    def set_balance(self, balance):
        self.balance = balance
    def curr_balance (self):
        return self.balance
    
    def run(self):
        csv_file = pandas.read_csv(self.csv_filepath)
        dates = csv_file.set_index('Date',drop=False)
        self.Portfolio_balance = []
        self.shares_total = 0
        self.date_track = []
        for index,row in dates.iterrows():
            currdate = datetime.strptime(index, '%Y-%m-%d')
            #run only within the dates specified
            if currdate >= self.startdate and currdate <= self.enddate:
                curropen = row['Open']
                currclose = row['Close']
                
                #get order for open price
                openorder = self.strategy.open(curropen,self.balance,self.shares_total)
                if openorder:
                    if openorder.buy:
                        if openorder.shares * curropen > self.balance:
                            print("NOT ENOUGH CASH to fill BUY order")
                        else:
                            self.balance -= openorder.shares * curropen
                            self.shares_total += openorder.shares
                    else:
                        self.balance += openorder.shares * curropen
                        self.shares_total -= openorder.shares
                        
                #get order for close price
                closeorder = self.strategy.close(curropen,self.balance,self.shares_total)
                if closeorder:
                    if closeorder.buy:
                        if closeorder.shares * currclose > self.balance:
                            print("NOT ENOUGH CASH to fill BUY order")
                        else:
                            self.balance -= closeorder.shares * currclose
                            self.shares_total += closerorder.shares
                    else:
                        self.balance += closeorder.shares * currclose
                        self.shares_total -= closeorder.shares
                        
                #data keeping
                self.date_track.append(currdate)
                self.Portfolio_balance.append(self.balance + (self.shares_total * currclose))
        print("End portfolio value = ", self.balance +  (self.shares_total * currclose))
    def portfolio_y_data(self):
        return self.Portfolio_balance
    def portfolio_x_data(self):
        return self.date_track
    def set_strategy (self, strategy):
        self.strategy = strategy