# coding=UTF-8

import os
import sys

import Program.GlobalVar as gv
from AxisWeb.DownloadData import *
from AxisForm.AxisTradeCultForm import AxisTradeCultForm
from PyQt5.QtWidgets import QMainWindow, QApplication


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = AxisTradeCultForm()
    window.show()
    sys.exit(app.exec_())

#gv.ReadStockGroups()
#DownloadAllStockGroupsFromQuandl(gv.StockDataPoolPath)    
