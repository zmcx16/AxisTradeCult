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

def ClearAllWidgetInLayout(layout):
    for i in reversed(range(layout.count())): 
        layout.itemAt(i).widget().setParent(None)   

class AxisTradeCultForm(QMainWindow, Ui_AxisTradeCultForm):
    def __init__(self, parent=None):
        super(AxisTradeCultForm, self).__init__(parent)
        self.setupUi(self)
        self.setupUIEvent(self)
        
    def setupUIEvent(self,AxisTradeCultForm):
        self.UpdateButton.clicked.connect(self.DoUpdateButton)
        self.GraphSampleButton.setVisible(False)
        self.OverviewStocklayout = QHBoxLayout()
        self.SetStockGroupsComboBoxItem()
        
        self.RefreshOverviewStock()
        #stock_data = {'Symbol':'T','Open':'10','High':'15','Low':'8','Close':'12','Volume':'11','ChangeC':'3%','ChangeV':'10%','AvgC3M':'15','AvgV3M':'13','StrikePrice1Y':'10.5 ~ 20.4'}
        
        #self.OverviewStock1 = OverviewStock(self,str(1),stock_data,30) 
        #self.OverviewStock2 = OverviewStock(self,str(2),stock_data,60) 

    def SetStockGroupsComboBoxItem(self):
        self.StockGroupsComboBox.addItems(gv.StockGroups.keys())

    def RefreshOverviewStock(self):
        ClearAllWidgetInLayout(self.OverviewStocklayout)
        SelectGroupName = self.StockGroupsComboBox.currentText()
        Stocks = gv.StockGroups[SelectGroupName]
                
        for i in range(len(Stocks)):
            stock_data = {'Symbol':'T','Open':'10','High':'15','Low':'8','Close':'12','Volume':'11','ChangeC':'3%','ChangeV':'10%','AvgC3M':'15','AvgV3M':'13','StrikePrice1Y':'10.5 ~ 20.4'}        
            self.OverviewStock = OverviewStock(self,str(i),stock_data,30*(i+1))    
        
         
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
        

class OverviewStock(Ui_AxisTradeCultForm):
    def __init__(self,parent,id,data,offset):
                
        font = QFont()
        font.setPointSize(10)
                
        SymbolLabel = QLabel(parent.tabOverview)
        SymbolLabel.setGeometry(QRect(parent.SymbolLabel.x(),parent.SymbolLabel.y()+offset, parent.SymbolLabel.width(), parent.SymbolLabel.height()))
        SymbolLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        SymbolLabel.setObjectName(parent.SymbolLabel.objectName()+id)
        SymbolLabel.setFont(font)
        OpenLabel = QLabel(parent.tabOverview)
        OpenLabel.setGeometry(QRect(parent.OpenLabel.x(),parent.OpenLabel.y()+offset, parent.OpenLabel.width(), parent.OpenLabel.height()))
        OpenLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        OpenLabel.setObjectName(parent.OpenLabel.objectName()+id)
        OpenLabel.setFont(font)
        HightLabel = QLabel(parent.tabOverview)
        HightLabel.setGeometry(QRect(parent.HightLabel.x(),parent.HightLabel.y()+offset, parent.HightLabel.width(), parent.HightLabel.height()))
        HightLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        HightLabel.setObjectName(parent.HightLabel.objectName()+id)
        HightLabel.setFont(font)
        LowLabel = QLabel(parent.tabOverview)
        LowLabel.setGeometry(QRect(parent.LowLabel.x(),parent.LowLabel.y()+offset, parent.LowLabel.width(), parent.LowLabel.height()))
        LowLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        LowLabel.setObjectName(parent.LowLabel.objectName()+id)
        LowLabel.setFont(font)
        CloseLabel = QLabel(parent.tabOverview)
        CloseLabel.setGeometry(QRect(parent.CloseLabel.x(),parent.CloseLabel.y()+offset, parent.CloseLabel.width(), parent.CloseLabel.height()))
        CloseLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        CloseLabel.setObjectName(parent.CloseLabel.objectName()+id)
        CloseLabel.setFont(font)
        VolumeLabel = QLabel(parent.tabOverview)
        VolumeLabel.setGeometry(QRect(parent.VolumeLabel.x(),parent.VolumeLabel.y()+offset, parent.VolumeLabel.width(), parent.VolumeLabel.height()))
        VolumeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        VolumeLabel.setObjectName(parent.VolumeLabel.objectName()+id)
        VolumeLabel.setFont(font)
        ChangeCLabel = QLabel(parent.tabOverview)
        ChangeCLabel.setGeometry(QRect(parent.ChangeCLabel.x(),parent.ChangeCLabel.y()+offset, parent.ChangeCLabel.width(), parent.ChangeCLabel.height()))
        ChangeCLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        ChangeCLabel.setObjectName(parent.ChangeCLabel.objectName()+id)
        ChangeCLabel.setFont(font)
        ChangeVLabel = QLabel(parent.tabOverview)
        ChangeVLabel.setGeometry(QRect(parent.ChangeVLabel.x(),parent.ChangeVLabel.y()+offset, parent.ChangeVLabel.width(), parent.ChangeVLabel.height()))
        ChangeVLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        ChangeVLabel.setObjectName(parent.ChangeVLabel.objectName()+id)
        ChangeVLabel.setFont(font)
        AvgC3MLabel = QLabel(parent.tabOverview)
        AvgC3MLabel.setGeometry(QRect(parent.AvgC3MLabel.x(),parent.AvgC3MLabel.y()+offset, parent.AvgC3MLabel.width(), parent.AvgC3MLabel.height()))
        AvgC3MLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        AvgC3MLabel.setObjectName(parent.AvgC3MLabel.objectName()+id)
        AvgC3MLabel.setFont(font)
        AvgV3MLabel = QLabel(parent.tabOverview)
        AvgV3MLabel.setGeometry(QRect(parent.AvgV3MLabel.x(),parent.AvgV3MLabel.y()+offset, parent.AvgV3MLabel.width(), parent.AvgV3MLabel.height()))
        AvgV3MLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        AvgV3MLabel.setObjectName(parent.AvgV3MLabel.objectName()+id)
        AvgV3MLabel.setFont(font)
        StrikePrice1YLabel = QLabel(parent.tabOverview)
        StrikePrice1YLabel.setGeometry(QRect(parent.StrikePrice1YLabel.x(),parent.StrikePrice1YLabel.y()+offset, parent.StrikePrice1YLabel.width(), parent.StrikePrice1YLabel.height()))
        StrikePrice1YLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        StrikePrice1YLabel.setObjectName(parent.StrikePrice1YLabel.objectName()+id)
        StrikePrice1YLabel.setFont(font)
        GraphSampleButton = QPushButton(parent.tabOverview)
        GraphSampleButton.setEnabled(True)
        GraphSampleButton.setGeometry(QRect(parent.GraphSampleButton.x(),parent.GraphSampleButton.y()+offset, parent.GraphSampleButton.width(), parent.GraphSampleButton.height()))
        GraphSampleButton.setObjectName(parent.GraphSampleButton.objectName()+id)
        
        
        _translate = QCoreApplication.translate
        SymbolLabel.setText(_translate("AxisTradeCultForm", data["Symbol"]))
        OpenLabel.setText(_translate("AxisTradeCultForm", data["Open"]))
        HightLabel.setText(_translate("AxisTradeCultForm", data["High"]))
        LowLabel.setText(_translate("AxisTradeCultForm", data["Low"]))
        CloseLabel.setText(_translate("AxisTradeCultForm", data["Close"]))
        VolumeLabel.setText(_translate("AxisTradeCultForm", data["Volume"]))
        ChangeCLabel.setText(_translate("AxisTradeCultForm", data["ChangeC"]))
        ChangeVLabel.setText(_translate("AxisTradeCultForm", data["ChangeV"]))
        AvgC3MLabel.setText(_translate("AxisTradeCultForm", data["AvgC3M"]))
        AvgV3MLabel.setText(_translate("AxisTradeCultForm", data["AvgV3M"]))
        StrikePrice1YLabel.setText(_translate("AxisTradeCultForm", data["StrikePrice1Y"]))
        GraphSampleButton.setText(_translate("AxisTradeCultForm", "Graph"))   
        
        parent.OverviewStocklayout.addWidget(SymbolLabel) 
        parent.OverviewStocklayout.addWidget(OpenLabel) 
        parent.OverviewStocklayout.addWidget(HightLabel) 
        parent.OverviewStocklayout.addWidget(LowLabel) 
        parent.OverviewStocklayout.addWidget(CloseLabel) 
        parent.OverviewStocklayout.addWidget(VolumeLabel) 
        parent.OverviewStocklayout.addWidget(ChangeCLabel) 
        parent.OverviewStocklayout.addWidget(ChangeVLabel) 
        parent.OverviewStocklayout.addWidget(AvgC3MLabel) 
        parent.OverviewStocklayout.addWidget(AvgV3MLabel) 
        parent.OverviewStocklayout.addWidget(StrikePrice1YLabel) 
        parent.OverviewStocklayout.addWidget(GraphSampleButton) 