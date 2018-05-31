import os
import pandas
import numpy
from calendar import formatstring

from CommonDef.DefStr import *

def SymbolToPath(symbol, save_dir = "data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(save_dir, "{}.csv".format(str(symbol)))


def CalChange(now, prev):
    return (now - prev) / prev


def human_format(num):
    num = float('{:.5g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def FormatOverviewStockData(OverviewStocks):

    for stockInfo in OverviewStocks:
        OverviewStocks[stockInfo][strOpen] = "{:.2f}".format(OverviewStocks[stockInfo][strOpen])
        OverviewStocks[stockInfo][strHigh] = "{:.2f}".format(OverviewStocks[stockInfo][strHigh])
        OverviewStocks[stockInfo][strLow] = "{:.2f}".format(OverviewStocks[stockInfo][strLow])
        OverviewStocks[stockInfo][strClose] = "{:.2f}".format(OverviewStocks[stockInfo][strClose])
        OverviewStocks[stockInfo][strVolume] = human_format(OverviewStocks[stockInfo][strVolume])
        OverviewStocks[stockInfo]['ChangeC'] = "{:.2%}".format(OverviewStocks[stockInfo]['ChangeC'])
        OverviewStocks[stockInfo]['ChangeV'] = "{:.1%}".format(OverviewStocks[stockInfo]['ChangeV'])
        OverviewStocks[stockInfo]['AvgC3M'] = "{:.2f}".format(OverviewStocks[stockInfo]['AvgC3M'])
        OverviewStocks[stockInfo]['AvgV3M'] = human_format(OverviewStocks[stockInfo]['AvgV3M'])
        OverviewStocks[stockInfo]['StrikePrice1Y'] = "{0:.2f}-{1:.2f}".format(OverviewStocks[stockInfo]['StrikePrice1Y'][0], OverviewStocks[stockInfo]['StrikePrice1Y'][1])


def ReadOverviewStockData(stocks, ChooseDate, StockDataPoolPath):

    OverviewStocks = {}

    for stock in stocks:
        try:
            StockDF = pandas.read_csv(SymbolToPath(stock, StockDataPoolPath) , parse_dates = True, index_col = strDate,
                    usecols = [strDate, strOpen, strHigh, strLow, strClose, strVolume], na_values = ["nan"])

        except Exception as exc:
            print('Generated an exception: %s' % exc)
            return False

        # latestDate = pandas.to_datetime(numpy.array(StockDF.index.to_pydatetime(), dtype=numpy.datetime64)[0])
        TargetDate = pandas.to_datetime(ChooseDate)
        TargetDate_back3m = TargetDate - pandas.DateOffset(months = 3)
        TargetDate_back1y = TargetDate - pandas.DateOffset(years = 1)

        DatePeriod3M = pandas.DataFrame(index = pandas.date_range(TargetDate_back3m, TargetDate))
        DatePeriod1Y = pandas.DataFrame(index = pandas.date_range(TargetDate_back1y, TargetDate))

        DF3M = DatePeriod3M.join(StockDF)
        DF1Y = DatePeriod1Y.join(StockDF)

        DF3M = DF3M.dropna()
        DF1Y = DF1Y.dropna()

        DF3M = pandas.DataFrame.sort_index(DF3M, ascending = False)
        DF1Y = pandas.DataFrame.sort_index(DF1Y, ascending = False)

        OverviewStock = { 'TargetDate':TargetDate
                         , 'Symbol': stock, strOpen:DF3M[strOpen][0], strHigh:DF3M[strHigh][0], strLow:DF3M[strLow][0], strClose:DF3M[strClose][0], strVolume:DF3M[strVolume][0]
                         , 'ChangeC':CalChange(now = DF3M[strClose][0], prev = DF3M[strClose][1]), 'ChangeV':CalChange(now = DF3M[strVolume][0], prev = DF3M[strVolume][1])
                         , 'AvgC3M':DF3M[strClose].mean(), 'AvgV3M':DF3M[strVolume].mean()
                         , 'StrikePrice1Y':[DF1Y[strLow].min() , DF1Y[strHigh].max()]}

        OverviewStocks[stock] = OverviewStock

    return OverviewStocks


def GetStockPriceVolumeData(stock, StockDataPoolPath, start_date, end_date):
    df = pandas.read_csv(SymbolToPath(stock, StockDataPoolPath), index_col = strDate,
            parse_dates = True, usecols = [strDate, strOpen, strHigh, strLow, strClose, strVolume], na_values = ['nan'])

    DatePeriod = pandas.DataFrame(index = pandas.date_range(start_date, end_date))
    DF = DatePeriod.join(df)
    DF = DF.dropna()
    return DF
