import pandas as pd
import requests
import xlsxwriter
import math

def chunks(lst,n):
    for i in range (0,len(lst),n):
        yield lst[i:i +n]

'''This script will create a excel spreadsheet of buy orders using an user input portfolio balance that mimics an equal weight SP500 fund.
It uses IEX API to get stock prices and a spreadsheet for current SP500 stocks.
It will output the final buy orders as an excel spreadsheet.
'''

#API TOKEN
from secrets import IEX_CLOUD_API_TOKEN

#currently using a preset file with list of sp500 instead of gathering the list of stocks from some API
sp500_list_csv_filepath = "sp_500_stocks.csv"
sp500_stocklist = pd.read_csv(sp500_list_csv_filepath)

#the current batch API of IEX only accepts at most 100 stock tickers. We are splitting the stock list up
symbol_groups = list(chunks(sp500_stocklist['Ticker'],100))
symbol_strings = []
for i in range(len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
    
my_columns = ['Ticker', 'Stock Price', ' Market Cap', 'Number of shares to buy']
final_df= pd.DataFrame(columns = my_columns)

#Extract stock price using IEX API
base_url = 'https://sandbox.iexapis.com/stable'
for stocklist in symbol_strings:  
    request = f'/stock/market/batch?symbols={stocklist}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    final_url = base_url + request
    data = requests.get(final_url).json()
    for symbol in stocklist.split(','): 
        price = data[symbol]['quote']['latestPrice']
        mkt_cap = data[symbol]['quote']['marketCap']/(10**9)
        final_df = final_df.append(
            pd.Series([symbol, price, mkt_cap, 'N/A'],index = my_columns), ignore_index=True,
        )

#user input section to get a portfolio value
portfolio_balance = input('Enter portfolio value : ')
try:
    val = float(portfolio_balance)
except ValueError:
    print("Please enter a number")
    portfolio_balance = input('Enter portfolio value : ')
    val = float(portfolio_balance)
    
position_size = val/len(final_df.index)
num_shares = position_size
for i in range(len(final_df.index)):
    final_df.loc[i,'Number of shares to buy'] = math.floor(position_size/final_df.loc[i,'Stock Price'])
    
#write to the excel spreadsheet
writer = pd.ExcelWriter('sp500_trades.xlsx',engine = 'xlsxwriter')
final_df.to_excel(writer, 'SP500 trades',index = False)
background_color = '#ffffff'
font_color = '#000000'

string_format = writer.book.add_format({
    'font_color':font_color,
    'bg_color': background_color,
    'border' : 1      
})

dollar_format = writer.book.add_format({
    'num_format' : '$0.00',
    'font_color':font_color,
    'bg_color': background_color,
    'border' : 1      
})

integer_format = writer.book.add_format({
     'num_format' : '0',
    'font_color':font_color,
    'bg_color': background_color,
    'border' : 1      
})
column_formats = {
    'A': ['Ticker', string_format],
    'B': ['Stock Price', dollar_format],
    'C': ['Market Cap', integer_format],
    'D': ['Number of Shares to Buy', integer_format]
}
for column in column_formats.keys():
    writer.sheets['SP500 trades'].set_column(f'{column}:{column}',18,column_formats[column][1])
writer.save()