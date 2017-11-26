import os

import Program.GlobalVar as gv
from AxisWeb.DownloadData import *


gv.ReadStockGroups()
DownloadAllStockGroupsFromQuandl(gv.StockDataPoolPath)    