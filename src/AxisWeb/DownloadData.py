import os
import requests

import Program.GlobalVar as gv
from Program.Common import *

#-------------------------------------------------------------------------
# AlphaVantage API
def DownloadStockDataFromAlphaVantage(symbol, save_dir):
    try:
        res = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey=...&datatype=csv'.format(str(symbol)))
        res.raise_for_status()
    except Exception as exc:
        print('Generated an exception: %s' % exc)
        return False

    os.makedirs(save_dir, exist_ok = True)
    f = open(SymbolToPath(symbol, save_dir), 'w')
    f.write(res.text)
    f.closed
    return True


def DownloadStockDataListFromAlphaVantage(symbols, save_dir):
    for symbol in symbols:
        DownloadStockDataFromAlphaVantage(symbol, save_dir)
    return True


def DownloadAllStockGroupsFromAlphaVantage(save_dir):
    for key in gv.StockGroups:
        DownloadStockDataListFromAlphaVantage(gv.StockGroups[key], save_dir)
    return True


#-------------------------------------------------------------------------
# Quandl WIKI API Only Support to 2018/3/27, Only use it for old data
def DownloadStockDataFromQuandl(symbol, save_dir):
    try:
        res = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/{}/data.csv'.format(str(symbol)))
        res.raise_for_status()
    except Exception as exc:
        print('Generated an exception: %s' % exc)
        return False

    os.makedirs(save_dir, exist_ok = True)
    f = open(SymbolToPath(symbol, save_dir), 'w')
    f.write(res.text)
    f.closed
    return True


def DownloadStockDataListFromQuandl(symbols, save_dir):
    for symbol in symbols:
        DownloadStockDataFromQuandl(symbol, save_dir)
    return True


def DownloadAllStockGroupsFromQuandl(save_dir):
    for key in gv.StockGroups:
        DownloadStockDataListFromQuandl(gv.StockGroups[key], save_dir)
    return True
#-------------------------------------------------------------------------
