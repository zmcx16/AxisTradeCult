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
from _testcapi import INT_MAX

class OverviewStockPage(QMainWindow, Ui_AxisTradeCultForm):

    def __init__(self, parent=None):   
        super(OverviewStockPage, self).__init__(parent)
        self.setupUIEvent()
        
    def setupUIEvent(self):
        self.OverviewStocklayout = QVBoxLayout() 
        self.OverviewStocklayout.setSpacing(0);
        self.OverviewStocklayout.setContentsMargins(0, 0, 0, 0);
        
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

         
        self.parent().scrollAreaWidgetContents.setLayout(self.OverviewStocklayout)

        self.RefreshOverviewStock()
    
        
        #self.layout = QVBoxLayout()
        #self.layout.addWidget(self.scrollAreaWidgetContents)

        

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
            #self.AddOverviewStockInfo(self.parent(),str(objectID),OverviewStocks[stock],30*(objectID)) 
            stockInfo = OverviewStockInfoWidget(self.parent(),str(objectID),OverviewStocks[stock],30*(objectID))
            stockInfo.setGeometry(QRect(0,0,stockInfo.widget_width,stockInfo.widget_height))
            stockInfo.setMinimumSize(stockInfo.widget_width, stockInfo.widget_height)
            
            stockInfo.setObjectName("XXX"+str(objectID))
            
            #stockInfo.setFixedWidth(stockInfo.widget_width)
            #stockInfo.setFixedWidth(stockInfo.widget_height)
            
            #stockInfo.resize(QSize(300,300))            
            #stockInfo.setMinimumSize(stockInfo.widget_width, 100)
            #stockInfo.setMaximumSize(stockInfo.widget_width, 200)
            #stockInfo.setMinimumSize(876, 1000)
            #stockInfo.setMinimumSize(stockInfo.widget_width, stockInfo.widget_height)            
            #stockInfo.setMaximumSize(stockInfo.widget_width, stockInfo.widget_height)            
            print(stockInfo.widget_width," ", stockInfo.widget_height)
            
            
    
            self.OverviewStocklayout.addWidget(stockInfo)
            self.OverviewStocklayout.setSpacing(1)
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
    

class OverviewStockInfoWidget(QWidget):
  
    def __init__(self,parent,id,data,offset):      
        super(OverviewStockInfoWidget, self).__init__()        
        self.initUI(parent,id,data,offset)
        
    def initUI(self,parent,id,data,offset):
          
        print ("start")
                
        font = QFont()
        font.setPointSize(10)
        
        fontBold = QFont()   
        fontBold.setPointSize(10)           
        fontBold.setBold(True) 
        
        self.Layout = QFormLayout()
        
        self.offsetX = -6
        self.offsetY = 10
        
        self.StockCheckBox = QCheckBox(self)
        self.StockCheckBox.setGeometry(QRect(parent.StockCheckBox.x()+self.offsetX, self.offsetY, parent.StockCheckBox.width(), parent.StockCheckBox.height()))
        self.StockCheckBox.setObjectName(parent.StockCheckBox.objectName()+id)
        self.StockCheckBox.setFont(font)
        self.OpenLabel = QLabel(self)
        self.OpenLabel.setGeometry(QRect(parent.OpenLabel.x()+self.offsetX, self.offsetY, parent.OpenLabel.width(), parent.OpenLabel.height()))
        self.OpenLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.OpenLabel.setObjectName(parent.OpenLabel.objectName()+id)
        self.OpenLabel.setFont(font)
        self.HightLabel = QLabel(self)
        self.HightLabel.setGeometry(QRect(parent.HightLabel.x()+self.offsetX, self.offsetY, parent.HightLabel.width(), parent.HightLabel.height()))
        self.HightLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.HightLabel.setObjectName(parent.HightLabel.objectName()+id)
        self.HightLabel.setFont(font)
        self.LowLabel = QLabel(self)
        self.LowLabel.setGeometry(QRect(parent.LowLabel.x()+self.offsetX, self.offsetY, parent.LowLabel.width(), parent.LowLabel.height()))
        self.LowLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.LowLabel.setObjectName(parent.LowLabel.objectName()+id)
        self.LowLabel.setFont(font)
        self.CloseLabel = QLabel(self)
        self.CloseLabel.setGeometry(QRect(parent.CloseLabel.x()+self.offsetX, self.offsetY, parent.CloseLabel.width(), parent.CloseLabel.height()))
        self.CloseLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.CloseLabel.setObjectName(parent.CloseLabel.objectName()+id)
        self.CloseLabel.setFont(font)
        self.VolumeLabel = QLabel(self)
        self.VolumeLabel.setGeometry(QRect(parent.VolumeLabel.x()+self.offsetX, self.offsetY, parent.VolumeLabel.width(), parent.VolumeLabel.height()))
        self.VolumeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.VolumeLabel.setObjectName(parent.VolumeLabel.objectName()+id)
        self.VolumeLabel.setFont(font)
        self.ChangeCLabel = QLabel(self)
        self.ChangeCLabel.setGeometry(QRect(parent.ChangeCLabel.x()+self.offsetX, self.offsetY, parent.ChangeCLabel.width(), parent.ChangeCLabel.height()))
        self.ChangeCLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ChangeCLabel.setObjectName(parent.ChangeCLabel.objectName()+id)
        self.ChangeCLabel.setFont(fontBold)
        self.ChangeVLabel = QLabel(self)
        self.ChangeVLabel.setGeometry(QRect(parent.ChangeVLabel.x()+self.offsetX, self.offsetY, parent.ChangeVLabel.width(), parent.ChangeVLabel.height()))
        self.ChangeVLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ChangeVLabel.setObjectName(parent.ChangeVLabel.objectName()+id)
        self.ChangeVLabel.setFont(fontBold)
        self.AvgC3MLabel = QLabel(self)
        self.AvgC3MLabel.setGeometry(QRect(parent.AvgC3MLabel.x()+self.offsetX, self.offsetY, parent.AvgC3MLabel.width(), parent.AvgC3MLabel.height()))
        self.AvgC3MLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.AvgC3MLabel.setObjectName(parent.AvgC3MLabel.objectName()+id)
        self.AvgC3MLabel.setFont(font)
        self.AvgV3MLabel = QLabel(self)
        self.AvgV3MLabel.setGeometry(QRect(parent.AvgV3MLabel.x()+self.offsetX, self.offsetY, parent.AvgV3MLabel.width(), parent.AvgV3MLabel.height()))
        self.AvgV3MLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.AvgV3MLabel.setObjectName(parent.AvgV3MLabel.objectName()+id)
        self.AvgV3MLabel.setFont(font)
        self.StrikePrice1YLabel = QLabel(self)
        self.StrikePrice1YLabel.setGeometry(QRect(parent.StrikePrice1YLabel.x()+self.offsetX, self.offsetY, parent.StrikePrice1YLabel.width(), parent.StrikePrice1YLabel.height()))
        self.StrikePrice1YLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.StrikePrice1YLabel.setObjectName(parent.StrikePrice1YLabel.objectName()+id)
        self.StrikePrice1YLabel.setFont(font)
        self.GraphSampleButton = QPushButton(self)
        self.GraphSampleButton.setEnabled(True)
        self.GraphSampleButton.setGeometry(QRect(parent.GraphSampleButton.x()+self.offsetX, self.offsetY, parent.GraphSampleButton.width(), parent.GraphSampleButton.height()))
        self.GraphSampleButton.setObjectName(parent.GraphSampleButton.objectName()+id)
        
        _translate = QCoreApplication.translate
        self.StockCheckBox.setText(_translate("AxisTradeCultForm", data["Symbol"]))        
        self.OpenLabel.setText(_translate("AxisTradeCultForm", data["Open"]))
        self.HightLabel.setText(_translate("AxisTradeCultForm", data["High"]))
        self.LowLabel.setText(_translate("AxisTradeCultForm", data["Low"]))
        self.CloseLabel.setText(_translate("AxisTradeCultForm", data["Close"]))
        self.VolumeLabel.setText(_translate("AxisTradeCultForm", data["Volume"]))
        self.ChangeCLabel.setText(_translate("AxisTradeCultForm", data["ChangeC"]))
        self.ChangeVLabel.setText(_translate("AxisTradeCultForm", data["ChangeV"]))
        self.AvgC3MLabel.setText(_translate("AxisTradeCultForm", data["AvgC3M"]))
        self.AvgV3MLabel.setText(_translate("AxisTradeCultForm", data["AvgV3M"]))
        self.StrikePrice1YLabel.setText(_translate("AxisTradeCultForm", data["StrikePrice1Y"]))
        self.GraphSampleButton.setText(_translate("AxisTradeCultForm", "Graph"))   
        
  
        if float(self.ChangeCLabel.text().replace(r"%", "")) > 0:
            SetQLineEditColor(self.ChangeCLabel,r=8,g=180,b=8)
        elif float(self.ChangeCLabel.text().replace(r"%", "")) < 0:
            SetQLineEditColor(self.ChangeCLabel,r=238,g=4,b=4)

        if float(self.ChangeVLabel.text().replace(r"%", "")) > 0:
            SetQLineEditColor(self.ChangeVLabel,r=8,g=180,b=8)
        elif float(self.ChangeVLabel.text().replace(r"%", "")) < 0:
            SetQLineEditColor(self.ChangeVLabel,r=238,g=4,b=4)        
        
        self.Layout.addWidget(self.StockCheckBox)
        self.Layout.addWidget(self.OpenLabel)
        self.Layout.addWidget(self.HightLabel)
        self.Layout.addWidget(self.LowLabel)
        self.Layout.addWidget(self.CloseLabel)
        self.Layout.addWidget(self.VolumeLabel)
        self.Layout.addWidget(self.ChangeCLabel)
        self.Layout.addWidget(self.ChangeVLabel)
        self.Layout.addWidget(self.AvgC3MLabel)
        self.Layout.addWidget(self.AvgV3MLabel)
        self.Layout.addWidget(self.StrikePrice1YLabel)
        self.Layout.addWidget(self.GraphSampleButton)
        
        self.CalcWidgetSize()
        
        print ("End")
   
    def CalcWidgetSize(self):
        min_x=INT_MAX
        max_x=0
        self.widget_height=0
        for i in range(self.Layout.count()):  
            widget = self.Layout.itemAt( i ).widget()            
            min_x = min(min_x, widget.x())
            max_x = max(max_x, widget.x()+widget.width())
            self.widget_height = max(self.widget_height, widget.height())
            
        self.widget_width = max_x - min_x
        self.widget_height += self.offsetY
    
    def sizeHint( self ):
        return QSize( self.widget_width, self.widget_height )
        
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
        