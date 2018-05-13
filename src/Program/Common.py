import os
import pandas
import numpy
from calendar import formatstring


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
        OverviewStocks[stockInfo]['Open'] = "{:.2f}".format(OverviewStocks[stockInfo]['Open'])
        OverviewStocks[stockInfo]['High'] = "{:.2f}".format(OverviewStocks[stockInfo]['High'])
        OverviewStocks[stockInfo]['Low'] = "{:.2f}".format(OverviewStocks[stockInfo]['Low'])
        OverviewStocks[stockInfo]['Close'] = "{:.2f}".format(OverviewStocks[stockInfo]['Close'])
        OverviewStocks[stockInfo]['Volume'] = human_format(OverviewStocks[stockInfo]['Volume'])
        OverviewStocks[stockInfo]['ChangeC'] = "{:.2%}".format(OverviewStocks[stockInfo]['ChangeC'])
        OverviewStocks[stockInfo]['ChangeV'] = "{:.1%}".format(OverviewStocks[stockInfo]['ChangeV'])
        OverviewStocks[stockInfo]['AvgC3M'] = "{:.2f}".format(OverviewStocks[stockInfo]['AvgC3M'])
        OverviewStocks[stockInfo]['AvgV3M'] = human_format(OverviewStocks[stockInfo]['AvgV3M'])
        OverviewStocks[stockInfo]['StrikePrice1Y'] = "{0:.2f}-{1:.2f}".format(OverviewStocks[stockInfo]['StrikePrice1Y'][0], OverviewStocks[stockInfo]['StrikePrice1Y'][1])


def ReadOverviewStockData(stocks, ChooseDate, StockDataPoolPath):

    OverviewStocks = {}

    for stock in stocks:
        try:
            StockDF = pandas.read_csv(SymbolToPath(stock, StockDataPoolPath) , parse_dates = True, index_col = "Date",
                    usecols = ["Date", "Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"], na_values = ["nan"])

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
                         , 'Symbol': stock, 'Open':DF3M['Adj. Open'][0], 'High':DF3M['Adj. High'][0], 'Low':DF3M['Adj. Low'][0], 'Close':DF3M['Adj. Close'][0], 'Volume':DF3M['Adj. Volume'][0]
                         , 'ChangeC':CalChange(now = DF3M['Adj. Close'][0], prev = DF3M['Adj. Close'][1]), 'ChangeV':CalChange(now = DF3M['Adj. Volume'][0], prev = DF3M['Adj. Volume'][1])
                         , 'AvgC3M':DF3M['Adj. Close'].mean(), 'AvgV3M':DF3M['Adj. Volume'].mean()
                         , 'StrikePrice1Y':[DF1Y['Adj. Low'].min() , DF1Y['Adj. High'].max()]}

        OverviewStocks[stock] = OverviewStock

    return OverviewStocks


def GetStockPriceVolumeData(stock, StockDataPoolPath, start_date, end_date):
    df = pandas.read_csv(SymbolToPath(stock, StockDataPoolPath), index_col = 'Date',
            parse_dates = True, usecols = ['Date', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume'], na_values = ['nan'])

    DatePeriod = pandas.DataFrame(index = pandas.date_range(start_date, end_date))
    DF = DatePeriod.join(df)
    DF = DF.dropna()
    return DF
