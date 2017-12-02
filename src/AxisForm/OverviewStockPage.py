from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import concurrent.futures
import time

import Program.GlobalVar as gv
from Program.Common import *
from AxisWeb.DownloadData import *
from AxisForm.MessageInfo import *
from AxisForm.Common import *

class OverviewStockPage(QMainWindow, Ui_AxisTradeCultForm):

    def __init__(self, parent=None):   
        super(OverviewStockPage, self).__init__(parent)
        self.setupUIEvent()
        
    def setupUIEvent(self):
        self.OverviewStocklayout = QHBoxLayout() 
        self.parent().DisplayDate.setCalendarPopup(True)
        self.parent().DisplayDate.setDate(QDate.currentDate())
        self.parent().DisplayDate.dateChanged.connect(self.RefreshOverviewStock)      
        self.parent().UpdateButton.clicked.connect(self.DoUpdateButton)
        self.parent().AddButton.clicked.connect(self.DoAddButton)
        self.parent().StockGroupsComboBox.currentIndexChanged.connect(self.RefreshOverviewStock)
        self.parent().DelButton.clicked.connect(self.DoDelButton)
        self.parent().GraphSampleButton.setVisible(False)
        self.parent().StockCheckBox.setVisible(False) 
        self.SetStockGroupsComboBoxItem() 
        self.RefreshOverviewStock()


    def SetStockGroupsComboBoxItem(self):
        self.parent().StockGroupsComboBox.addItems(gv.StockGroups.keys())
        

    def RefreshOverviewStock(self):         
        ClearAllWidgetInLayout(self.OverviewStocklayout)      
        SelectGroupName = self.parent().StockGroupsComboBox.currentText()
        Stocks = gv.StockGroups[SelectGroupName]      
        
        ChooseDateTime = self.parent().DisplayDate.date()       
        if self.parent().DisplayDate.date() > QDate.currentDate():
            ChooseDateTime = QDate.currentDate()
        else:
            ChooseDateTime = self.parent().DisplayDate.date()
         
        OverviewStocks = ReadOverviewStockData(Stocks, QDate.toPyDate(ChooseDateTime), gv.StockDataPoolPath)  
        if OverviewStocks is False:
            return False
            
        FormatOverviewStockData(OverviewStocks);               
        objectID = 1
        for stock in OverviewStocks: 
            self.AddOverviewStockInfo(self.parent(),str(objectID),OverviewStocks[stock],30*(objectID)) 
            objectID+=1         

    def DoAddButton(self):
        self.parent().AddButton.setEnabled(False)
        Symbol = self.parent().Stockline.text()
        NowGroup = self.parent().StockGroupsComboBox.currentText()

        if Symbol in gv.StockGroups[NowGroup]:
            msg = AddStockAlreadySymbolMessage
            msg[Str_setText] = msg[Str_setText].format(NowGroup,Symbol)       
            showdialog(AddStockAlreadySymbolMessage)
            self.parent().AddButton.setEnabled(True)
            return False
        
        if DownloadStockDataFromQuandl(Symbol,gv.StockDataPoolPath) is False:            
            msg = AddStockDownloadFailMessage            
            msg[Str_setText] = msg[Str_setText].format(Symbol)
            showdialog(AddStockDownloadFailMessage)
            self.parent().AddButton.setEnabled(True)
            return False
                            
        gv.AddStockInGroup(self.parent().StockGroupsComboBox.currentText(),Symbol)
        self.RefreshOverviewStock()
        self.parent().AddButton.setEnabled(True)     
        return True
    
    def DoDelButton(self):
        NowGroup = self.parent().StockGroupsComboBox.currentText()
        Stocks = gv.StockGroups[NowGroup]
                
        StockCheckBoxObjectNames = []
        for objectID in range(1, len(Stocks)+1): 
            StockCheckBoxObjectNames.append(self.parent().StockCheckBox.objectName() + str(objectID))        
        
        for i in reversed(range(self.OverviewStocklayout.count())):  
            widgetToRemove = self.OverviewStocklayout.itemAt( i ).widget()
            if widgetToRemove.objectName() in StockCheckBoxObjectNames:
                if widgetToRemove.isChecked() is True:
                    Stocks.remove(widgetToRemove.text())
                    self.OverviewStocklayout.removeWidget( widgetToRemove )         
                    widgetToRemove.setParent( None )           
        
        gv.ResetStockInGroup(self.parent().StockGroupsComboBox.currentText(),Stocks)
        self.RefreshOverviewStock()
        return True   
         
    def DoUpdateButton(self):
        
        self.parent().UpdateButton.setEnabled(False)     
        stocksSet = {symbol for key in gv.StockGroups for symbol in gv.StockGroups[key]}          
        self.parent().UpdateProgressBar.setRange(0,100)   
        self.update_stocks_thread = UpdateStocksThread(stocksSet)       
        self.update_stocks_thread.FinishUpdateStocksSignal.connect(self.FinishUpdateStocks)     
        self.update_stocks_thread.UpdateProgressBarCountSignal.connect(self.UpdateProgressBarCount)
        self.update_stocks_thread.start()     
        
    def FinishUpdateStocks(self):
        self.parent().UpdateButton.setEnabled(True)  
        print ("finish!!")
      
    def UpdateProgressBarCount(self,val):
        self.parent().UpdateProgressBar.setValue(val)
        
    @pyqtSlot()
    def on_UpdateButton_clicked(self):
        print ("test pyqtSlot!!")     


    def AddOverviewStockInfo(self,parent,id,data,offset):
        
        global OverviewStockList
        OverviewStockList = {}
           
        font = QFont()
        font.setPointSize(10)
        
        fontBold = QFont()   
        fontBold.setPointSize(10)           
        fontBold.setBold(True) 
                
        StockCheckBox = QCheckBox(parent.tabOverview)
        StockCheckBox.setGeometry(QRect(parent.StockCheckBox.x(),parent.StockCheckBox.y()+offset, parent.StockCheckBox.width(), parent.StockCheckBox.height()))
        StockCheckBox.setObjectName(parent.StockCheckBox.objectName()+id)
        StockCheckBox.setFont(font)
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
        ChangeCLabel.setFont(fontBold)
        ChangeVLabel = QLabel(parent.tabOverview)
        ChangeVLabel.setGeometry(QRect(parent.ChangeVLabel.x(),parent.ChangeVLabel.y()+offset, parent.ChangeVLabel.width(), parent.ChangeVLabel.height()))
        ChangeVLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        ChangeVLabel.setObjectName(parent.ChangeVLabel.objectName()+id)
        ChangeVLabel.setFont(fontBold)
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
        StockCheckBox.setText(_translate("AxisTradeCultForm", data["Symbol"]))        
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
        
  
        if float(ChangeCLabel.text().replace(r"%", "")) > 0:
            SetQLineEditColor(ChangeCLabel,r=8,g=180,b=8)
        elif float(ChangeCLabel.text().replace(r"%", "")) < 0:
            SetQLineEditColor(ChangeCLabel,r=238,g=4,b=4)

        if float(ChangeVLabel.text().replace(r"%", "")) > 0:
            SetQLineEditColor(ChangeVLabel,r=8,g=180,b=8)
        elif float(ChangeVLabel.text().replace(r"%", "")) < 0:
            SetQLineEditColor(ChangeVLabel,r=238,g=4,b=4)        

                  
        self.OverviewStocklayout.addWidget(StockCheckBox) 
        self.OverviewStocklayout.addWidget(OpenLabel) 
        self.OverviewStocklayout.addWidget(HightLabel) 
        self.OverviewStocklayout.addWidget(LowLabel) 
        self.OverviewStocklayout.addWidget(CloseLabel) 
        self.OverviewStocklayout.addWidget(VolumeLabel) 
        self.OverviewStocklayout.addWidget(ChangeCLabel) 
        self.OverviewStocklayout.addWidget(ChangeVLabel) 
        self.OverviewStocklayout.addWidget(AvgC3MLabel) 
        self.OverviewStocklayout.addWidget(AvgV3MLabel) 
        self.OverviewStocklayout.addWidget(StrikePrice1YLabel) 
        self.OverviewStocklayout.addWidget(GraphSampleButton) 
        
        for i in range(self.OverviewStocklayout.count()): 
            self.OverviewStocklayout.itemAt( i ).widget().show()  
        
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
                    if data is True:
                        previous_progress   = self.FinishNum / len(self.stocksSet) * 100
                        self.FinishNum      += 1
                        now_progress        = self.FinishNum / len(self.stocksSet) * 100
                        if int(now_progress) != int(previous_progress):
                            self.UpdateProgressBarCountSignal.emit(int(now_progress))

        self.FinishUpdateStocksSignal.emit("FinishUpdateStocksSignal")
        