# coding=UTF-8

import sys
from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import concurrent.futures
import time

import Program.GlobalVar as gv
from AxisWeb.DownloadData import *


class AxisTradeCultForm(QMainWindow, Ui_AxisTradeCultForm):
    def __init__(self, parent=None):
        super(AxisTradeCultForm, self).__init__(parent)
        self.setupUi(self)
        self.setupUIEvent(self)
        
    def setupUIEvent(self,AxisTradeCultForm):
        self.UpdateButton.clicked.connect(self.DoUpdateButton)
        

    
    @pyqtSlot()  
    def DoUpdateButton(self):
        self.UpdateButton.setEnabled(False)
        self.update_stocks_thread = UpdateStocksThread()       
        self.update_stocks_thread.FinishUpdateStocksSignal.connect(self.FinishUpdateStocks)     
        self.update_stocks_thread.start()     
    
    def FinishUpdateStocks(self):
        self.UpdateButton.setEnabled(True)   

class UpdateStocksThread(QThread):
    
    FinishUpdateStocksSignal = pyqtSignal(str)
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        DownloadAllStockGroupsFromQuandl(gv.StockDataPoolPath)
        self.FinishUpdateStocksSignal.emit("FinishUpdateStocksSignal")
        
