import os
import sys
from assertpy import assert_that
    
import Program.GlobalVar as gv
from AxisForm.AxisTradeCultForm import AxisTradeCultForm
from PyQt5.QtWidgets import QMainWindow, QApplication
from AxisWeb.DownloadData import *


def test_Common():
    assert_that(gv.StockDataPoolPath).is_not_empty()
    assert_that(DownloadStockDataListFromQuandl('T', gv.StockDataPoolPath)).is_true()
    return True
