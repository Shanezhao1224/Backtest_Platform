import pandas as pd
import requests
from scipy import stats
import xlsxwriter
import math

'''This Python file implements an equal weight high momentum portfolio strategy based on the stocks included in the sp500.
It will extract data from IEX using its API.
The buy information will be output into a excel spreadsheet. It can easily be extended to work on a specfic broker service
'''



#function for portfolio input 
def Portfolio_input():
    portfolio_balance = input('Enter portfolio value : ')
    try:
        val = float(portfolio_balance)
    except ValueError:
        print("Please enter a number")
        portfolio_balance = input('Enter portfolio value : ')
        val = float(portfolio_balance)
    return val

#This function calculates the number of shares to buy given a portfolio size and Panda dataframe
def calc_shares(portfolio_val,dataframe):
    position_size = portfolio_val/len(dataframe.index)
    num_shares = position_size
    for i in range(len(dataframe.index)):
        dataframe.loc[i,'Number of Shares to Buy'] = math.floor(position_size/dataframe.loc[i,'Price'])
    return dataframe
# Function sourced from 
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]   
    return
def main():
    from secrets import IEX_CLOUD_API_TOKEN
    sp500_list_csv_filepath = "sp_500_stocks.csv"
    sp500_stocklist = pd.read_csv(sp500_list_csv_filepath)
    my_columns = ['Ticker', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']
    #create the strategy using quantitative momentum as our signal
    hqm_columns = [
        'Ticker', 'Price', 'Number of Shares to Buy', '1-year Price Return', '1-year Return Percentile', 
        '6-month Price Return', '6-month Return Percentile', '3-month Price Return', '3-month Return Percentile',
        '1-month Price Return', '1-month Return Percentile', 'HQM SCORE'
    ]
    base_url = 'https://sandbox.iexapis.com/stable'
    hqm_df = pd.DataFrame(columns = hqm_columns)
    symbol_groups = list(chunks(sp500_stocklist['Ticker'], 100))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))
    #extract stock data using API
    for stocklist in symbol_strings:  
        request = f'/stock/market/batch?symbols={stocklist}&types=stats,quote&token={IEX_CLOUD_API_TOKEN}'
        final_url = base_url + request
        data = requests.get(final_url).json()
        for symbol in stocklist.split(','): 
            price = data[symbol]['quote']['latestPrice']
            yearlyreturn = data[symbol]['stats']['year1ChangePercent']
            if yearlyreturn == None:
                yearlyreturn = 0
            month6return =data[symbol]['stats']['month6ChangePercent']
            if month6return == None:
                month6return = 0
            month3return = data[symbol]['stats']['month3ChangePercent']
            if month3return == None:
                month3return = 0
            monthreturn = data[symbol]['stats']['month1ChangePercent']
            if monthreturn == None:
                monthreturn = 0
            hqm_df = hqm_df.append(
                pd.Series([symbol, price, 'N/A',
                          yearlyreturn, 'N/A',
                          month6return, 'N/A',
                          month3return, 'N/A',
                          monthreturn, 'N/A','N/A'],index = hqm_columns), ignore_index=True,
            )
            
    #calculate percentile data for each stock
    time_periods = ['1-year','6-month', '3-month', '1-month']
    for row in hqm_df.index:
        for time_period in time_periods:
            hqm_df.loc[row,f'{time_period} Return Percentile'] = \
            stats.percentileofscore(hqm_df[f'{time_period} Price Return'],hqm_df.loc[row,f'{time_period} Price Return'])
            
    hqm_df.sort_values('HQM SCORE',ascending = False, inplace=True)
    hqm_df = hqm_df[:50]
    hqm_df.reset_index(inplace=True,drop=True)
    pf_val = Portfolio_input()
    hqm_df = calc_shares(pf_val,hqm_df)
    
    #write to the excel file
    writer = pd.ExcelWriter('Momentum_strategy.xlsx',engine='xlsxwriter')
    hqm_df.to_excel(writer,sheet_name= "buy")
    background_color = '#ffffff'
    font_color = '#000000'

    string_template = writer.book.add_format(
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    dollar_template = writer.book.add_format(
        {
            'num_format':'$0.00',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    integer_template = writer.book.add_format(
        {
            'num_format':'0',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    percent_template = writer.book.add_format(
        {
            'num_format':'0.0%',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )
    column_formats = {
    'A': ['Ticker', string_template],
    'B': ['Price', dollar_template],
    'C':['Number of Shares to Buy', integer_template],
    'D':['1-year Price Return', percent_template],
    'E':['1-year Return Percentile', percent_template],
    'F':['6-month Price Return', percent_template], 
    'G':['6-month Return Percentile', percent_template],
    'H':['3-month Price Return', percent_template],
    'I':['3-month Return Percentile', percent_template],
    'J':['1-month Price Return', percent_template],
    'K':['1-month Return Percentile', percent_template], 
    'L':['HQM SCORE', percent_template]
}
    for column in column_formats.keys():
        writer.sheets['buy'].set_column(f'{column}:{column}',25,column_formats[column][1])
    writer.save()
    print("Finished")
    return
if __name__ == "__main__":
    main()
