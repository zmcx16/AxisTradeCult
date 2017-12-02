import os
import pandas
import numpy
from calendar import formatstring


def SymbolToPath(symbol, save_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(save_dir, "{}.csv".format(str(symbol)))

def CalChange(now,prev):
    return (now-prev)/prev

def FormatOverviewStockData(OverviewStocks):
    
    for stockInfo in OverviewStocks:
        OverviewStocks[stockInfo]['Open']   =  "{0:.2f}".format(OverviewStocks[stockInfo]['Open'])
        OverviewStocks[stockInfo]['High']   =  "{0:.2f}".format(OverviewStocks[stockInfo]['High'])
        OverviewStocks[stockInfo]['Low']    =   "{0:.2f}".format(OverviewStocks[stockInfo]['Low'])
        OverviewStocks[stockInfo]['Close']  = "{0:.2f}".format(OverviewStocks[stockInfo]['Close'])
        OverviewStocks[stockInfo]['Volume']   = "{0:}".format(OverviewStocks[stockInfo]['Volume'])
        OverviewStocks[stockInfo]['ChangeC']   = "{0:.2%}".format(OverviewStocks[stockInfo]['ChangeC'])
        OverviewStocks[stockInfo]['ChangeV']   = "{0:.2%}".format(OverviewStocks[stockInfo]['ChangeV'])
        OverviewStocks[stockInfo]['AvgC3M']   = "{0:.2f}".format(OverviewStocks[stockInfo]['AvgC3M'])
        OverviewStocks[stockInfo]['AvgV3M']   = "{0:}".format(OverviewStocks[stockInfo]['AvgV3M'])
        OverviewStocks[stockInfo]['StrikePrice1Y']   = "{0:.2f}-{0:.2f}".format(OverviewStocks[stockInfo]['StrikePrice1Y'][0],OverviewStocks[stockInfo]['StrikePrice1Y'][1]) 
        

def ReadOverviewStockData(stocks, StockDataPoolPath):
    
    OverviewStocks = {}
    
    for stock in stocks:
        try:
            StockDF = pandas.read_csv(SymbolToPath(stock,StockDataPoolPath) , parse_dates=True, index_col="Date",
                    usecols=["Date","Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"], na_values=["nan"])
        
        except Exception as exc:
            print('Generated an exception: %s' % exc)
            return False            
                
        latestDate = pandas.to_datetime(numpy.array(StockDF.index.to_pydatetime(), dtype=numpy.datetime64)[0])      
        latestDate_back3m = latestDate - pandas.DateOffset(months=3)
        latestDate_back1y = latestDate - pandas.DateOffset(years=1)
        
        DatePeriod3M = pandas.DataFrame(index=pandas.date_range(latestDate_back3m, latestDate))    
        DatePeriod1Y = pandas.DataFrame(index=pandas.date_range(latestDate_back1y, latestDate)) 
        
        DF3M = DatePeriod3M.join(StockDF)
        DF1Y = DatePeriod1Y.join(StockDF)
                     
        DF3M = DF3M.dropna()
        DF1Y = DF1Y.dropna()
        
        OverviewStock = {'Symbol': stock,'Open':StockDF['Adj. Open'][0], 'High':StockDF['Adj. High'][0], 'Low':StockDF['Adj. Low'][0], 'Close':StockDF['Adj. Close'][0], 'Volume':StockDF['Adj. Volume'][0]
                         ,'ChangeC':CalChange(now=StockDF['Adj. Close'][0], prev=StockDF['Adj. Close'][1]), 'ChangeV':CalChange(now=StockDF['Adj. Volume'][0], prev=StockDF['Adj. Volume'][1])
                         ,'AvgC3M':DF3M['Adj. Close'].mean(), 'AvgV3M':DF3M['Adj. Volume'].mean()
                         ,'StrikePrice1Y':[DF1Y['Adj. Low'].min() , DF1Y['Adj. High'].max()]}
        
        OverviewStocks[stock] = OverviewStock
    
    return OverviewStocks