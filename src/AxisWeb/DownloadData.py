import os
import requests

import Program.GlobalVar as gv
from Program.Common import *
    
def DownloadStockDataFromQuandl(symbol, save_dir):
    res = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/{}/data.csv'.format(str(symbol)))
    os.makedirs(save_dir,exist_ok=True)
    f = open(SymbolToPath(symbol, save_dir),'w')
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
