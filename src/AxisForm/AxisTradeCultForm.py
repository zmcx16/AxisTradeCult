# coding=UTF-8

import sys
from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *

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
        self.GraphSampleButton.setVisible(False)
        
        self.OverviewStock1 = OverviewStock(self) 
        """
        self.SymbolLabel1 = QLabel(self.tabOverview)       
        self.SymbolLabel1.setGeometry(QRect(200, 200, 60, 31))
        self.SymbolLabel1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SymbolLabel1.setObjectName("SymbolLabel1")
        _translate1 = QCoreApplication.translate
        self.SymbolLabel1.setText(_translate1("AxisTradeCultForm", "Symbol"))
        """
                
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

class OverviewStock(Ui_AxisTradeCultForm):
    def __init__(self,parent):
        
        offset = 40
        
        self.SymbolLabel1 = QLabel(parent.tabOverview)
        self.SymbolLabel1.setGeometry(QRect(parent.SymbolLabel.x(),parent.SymbolLabel.y()+offset, parent.SymbolLabel.width(), parent.SymbolLabel.height()))
        self.SymbolLabel1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SymbolLabel1.setObjectName("SymbolLabel1")
        
        _translate1 = QCoreApplication.translate
        self.SymbolLabel1.setText(_translate1("AxisTradeCultForm", "Symbol"))
               
        """
        self.SymbolLabel = QLabel(self.tabOverview)
        self.SymbolLabel.setGeometry(QRect(10, 50, 60, 31))
        self.SymbolLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SymbolLabel.setObjectName("SymbolLabel")
        self.OpenLabel = QLabel(self.tabOverview)
        self.OpenLabel.setGeometry(QRect(80, 50, 60, 31))
        self.OpenLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.OpenLabel.setObjectName("OpenLabel")
        self.HightLabel = QLabel(self.tabOverview)
        self.HightLabel.setGeometry(QRect(150, 50, 60, 31))
        self.HightLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.HightLabel.setObjectName("HightLabel")
        self.LowLabel = QLabel(self.tabOverview)
        self.LowLabel.setGeometry(QRect(220, 50, 60, 31))
        self.LowLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.LowLabel.setObjectName("LowLabel")
        self.CloseLabel = QLabel(self.tabOverview)
        self.CloseLabel.setGeometry(QRect(290, 50, 60, 31))
        self.CloseLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.CloseLabel.setObjectName("CloseLabel")
        self.VolumeLabel = QLabel(self.tabOverview)
        self.VolumeLabel.setGeometry(QRect(500, 50, 60, 31))
        self.VolumeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.VolumeLabel.setObjectName("VolumeLabel")
        self.ChangeCLabel = QLabel(self.tabOverview)
        self.ChangeCLabel.setGeometry(QRect(360, 50, 60, 31))
        self.ChangeCLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ChangeCLabel.setObjectName("ChangeCLabel")
        self.ChangeVLabel = QLabel(self.tabOverview)
        self.ChangeVLabel.setGeometry(QRect(570, 50, 60, 31))
        self.ChangeVLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ChangeVLabel.setObjectName("ChangeVLabel")
        self.AvgCLabel = QLabel(self.tabOverview)
        self.AvgCLabel.setGeometry(QRect(430, 50, 60, 31))
        self.AvgCLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.AvgCLabel.setObjectName("AvgCLabel")
        self.AvgVLabel = QLabel(self.tabOverview)
        self.AvgVLabel.setGeometry(QRect(640, 50, 60, 31))
        self.AvgVLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.AvgVLabel.setObjectName("AvgVLabel")
        self.StrikePrice1YLabel = QLabel(self.tabOverview)
        self.StrikePrice1YLabel.setGeometry(QRect(690, 50, 120, 31))
        self.StrikePrice1YLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.StrikePrice1YLabel.setObjectName("StrikePrice1YLabel")
        self.GraphSampleButton = QPushButton(self.tabOverview)
        self.GraphSampleButton.setEnabled(True)
        self.GraphSampleButton.setGeometry(QRect(820, 50, 51, 31))
        self.GraphSampleButton.setObjectName("GraphSampleButton")
        """
    
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
        
        
