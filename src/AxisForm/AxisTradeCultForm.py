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
        
        
    def DoUpdateButton(self):
        self.UpdateButton.setEnabled(False)
        
        stocksSet = set() 
        for key in gv.StockGroups:
            for symbol in gv.StockGroups[key]:
                if symbol not in stocksSet:
                    stocksSet.add(symbol)
                        
        self.UpdateProgressBar.setRange(0,100)
        
        self.update_stocks_thread = UpdateStocksThread(stocksSet)       
        self.update_stocks_thread.FinishUpdateStocksSignal.connect(self.FinishUpdateStocks)     
        self.update_stocks_thread.UpdateProgressBarCountSignal.connect(self.UpdateProgressBarCount)
        self.update_stocks_thread.start()     
    

    def FinishUpdateStocks(self):
        self.UpdateButton.setEnabled(True)  
        print ("finish!!")
      
    def UpdateProgressBarCount(self,val):
        self.UpdateProgressBar.setValue(val)
        
    @pyqtSlot()
    def on_UpdateButton_clicked(self):
        print ("test pyqtSlot!!")
    
class UpdateStocksThread(QThread):
    
    FinishUpdateStocksSignal = pyqtSignal(str)
    UpdateProgressBarCountSignal = pyqtSignal(int)
    
    FinishNum = 0  
    def __init__(self,stocksSet):
        QThread.__init__(self)
        self.stocksSet = stocksSet
        
    def __del__(self):
        self.wait()
        
    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_download = {executor.submit(DownloadStockDataFromQuandl, symbol,gv.StockDataPoolPath): symbol for symbol in self.stocksSet}
            for future in concurrent.futures.as_completed(future_to_download):
                try:
                    data = future.result()
                except Exception as exc:
                    print('Generated an exception: %s' % exc)
                else:
                    if data:
                        previous_progress   = self.FinishNum / len(self.stocksSet) * 100
                        self.FinishNum      += 1
                        now_progress        = self.FinishNum / len(self.stocksSet) * 100
                        if int(now_progress) != int(previous_progress):
                            self.UpdateProgressBarCountSignal.emit(int(now_progress))

        self.FinishUpdateStocksSignal.emit("FinishUpdateStocksSignal")
        
        
