import sys

from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import concurrent.futures

import Program.GlobalVar as gv
from Program.Common import *
from AxisWeb.DownloadData import *
from AxisForm.MessageInfo import *
from AxisForm.Common import *
from AxisPlot.Common import *


class OverviewStockPage(QMainWindow):

    def __init__(self, parent=None):   
        super(OverviewStockPage, self).__init__(parent)
        self.setupUIEvent()
        
    def setupUIEvent(self):
        gv.ReadStockGroups()
        
        self.OverviewStocklayout = QVBoxLayout() 

        self.parent().DisplayDate.setCalendarPopup(True)
        self.parent().DisplayDate.setDate(QDate.currentDate())
        self.parent().DisplayDate.dateChanged.connect(self.RefreshOverviewStock)      
        self.parent().UpdateButton.clicked.connect(self.DoUpdateButton)
        self.parent().AddButton.clicked.connect(self.DoAddButton)
        self.parent().StockGroupsComboBox.currentIndexChanged.connect(self.RefreshOverviewStock)
        self.parent().DelButton.clicked.connect(self.DoDelButton)
        self.parent().GraphSampleButton.setVisible(False)
        self.parent().StockCheckBox.setVisible(False)   
        self.parent().scrollAreaWidgetContents.setLayout(self.OverviewStocklayout)
        self.SetGraphTypeComboBoxItem()
        
        
        self.SetStockGroupsComboBoxItem()  
        self.RefreshOverviewStock()
    
    def SetGraphTypeComboBoxItem(self):
        self.parent().GraphTypeComboBox.clear()        
        self.parent().GraphTypeComboBox.addItem('Basic6M')
        self.parent().GraphTypeComboBox.addItem('Candle6M')
        self.parent().GraphTypeComboBox.addItem('BasicN')
        self.parent().GraphTypeComboBox.addItem('CandleN')
        
    def SetStockGroupsComboBoxItem(self):
        self.parent().StockGroupsComboBox.clear()
        self.parent().StockGroupsComboBox.addItems(gv.StockGroups.keys())
        self.parent().StockGroupsComboBox.addItem('New Group')
        

    def RefreshOverviewStock(self):
        if self.parent().StockGroupsComboBox.count() == 0:
            return False
                        
        if self.parent().StockGroupsComboBox.currentText() == 'New Group':
            response = QInputDialog().getText(None, "Create Group", "Please Input New Group Name:")

            self.parent().StockGroupsComboBox.setCurrentIndex(0)
            if response[1] == True and response[0] != '':
                gv.AddStockGroup(response[0])
                self.SetStockGroupsComboBoxItem()
                self.parent().StockGroupsComboBox.setCurrentIndex(self.parent().StockGroupsComboBox.count()-2)
                
            return True
              
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
            stockInfo = OverviewStockInfoWidget(self.parent(),stock,OverviewStocks[stock])
            stockInfo.setGeometry(QRect(0,0,stockInfo.widget_width,stockInfo.widget_height))
            stockInfo.setMinimumSize(stockInfo.widget_width, stockInfo.widget_height)
            
            stockInfo.setObjectName(stock)
                          
            self.OverviewStocklayout.addWidget(stockInfo)
            self.OverviewStocklayout.setSpacing(1)
            objectID+=1         
        
        self.OverviewStocklayout.setSpacing(5);
        self.OverviewStocklayout.setContentsMargins(10, 10, 0, 10);
               
    def DoAddButton(self):
        self.parent().AddButton.setEnabled(False)
        Symbol = self.parent().Stockline.text()
        NowGroup = self.parent().StockGroupsComboBox.currentText()

        if Symbol in gv.StockGroups[NowGroup]:
            msg = AddStockAlreadySymbolMessage
            msg[Str_setText] = msg[Str_setText].format(NowGroup,Symbol)       
            ShowInfoDialog(msg)
            self.parent().AddButton.setEnabled(True)
            return False
        
        if DownloadStockDataFromQuandl(Symbol,gv.StockDataPoolPath) is False:            
            msg = AddStockDownloadFailMessage            
            msg[Str_setText] = msg[Str_setText].format(Symbol)
            ShowInfoDialog(msg)
            self.parent().AddButton.setEnabled(True)
            return False
                            
        gv.AddStockInGroup(self.parent().StockGroupsComboBox.currentText(),Symbol)
        self.RefreshOverviewStock()
        self.parent().AddButton.setEnabled(True)     
        return True
    
    def DoDelButton(self):
        if self.parent().StockGroupsComboBox.count() <= 1:
            return False
        
        NowGroup = self.parent().StockGroupsComboBox.currentText()
        Stocks = gv.StockGroups[NowGroup]
                
        StockCheckBoxObjectNames = []
        for stock in Stocks: 
            StockCheckBoxObjectNames.append(stock)        
        
        for i in reversed(range(self.OverviewStocklayout.count())):  
            widgetToRemove = self.OverviewStocklayout.itemAt( i ).widget()
            if widgetToRemove.objectName() in StockCheckBoxObjectNames:
                if widgetToRemove.StockCheckBox.isChecked() is True:
                    Stocks.remove(widgetToRemove.objectName())
                    self.OverviewStocklayout.removeWidget( widgetToRemove )         
                    widgetToRemove.setParent( None )         

        if(len(Stocks) == len(StockCheckBoxObjectNames)):
            msg = DeleteGroupWarningMessage
            msg[Str_setText] = msg[Str_setText].format(NowGroup)     
            msg[Str_setDetailedText] = msg[Str_setDetailedText].format(Stocks)     
            if ShowWarningDialog(msg) == 'OK':
                select_index = self.parent().StockGroupsComboBox.currentIndex()
                gv.DeleteStockGroup(self.parent().StockGroupsComboBox.currentText())
                self.parent().StockGroupsComboBox.setCurrentIndex(0)
                self.parent().StockGroupsComboBox.removeItem(select_index)
            
            self.RefreshOverviewStock()            
            return True  
        
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
        self.RefreshOverviewStock()
        print ("finish!!")
      
    def UpdateProgressBarCount(self,val):
        self.parent().UpdateProgressBar.setValue(val)
        

class OverviewStockInfoWidget(QWidget):
  
    Symbol = ''
    TargetDate = ''
    GraphTypeComboBox = None
        
    def __init__(self,parent,id,data):      
        super(OverviewStockInfoWidget, self).__init__()        
        self.initUI(parent,id,data)
        
        self.Symbol = data["Symbol"]
        self.TargetDate = data["TargetDate"]
        self.GraphTypeComboBox = parent.GraphTypeComboBox

    def initUI(self,parent,id,data):
                  
        font = QFont()
        font.setPointSize(10)
        
        fontBold = QFont()   
        fontBold.setPointSize(10)           
        fontBold.setBold(True) 
        
        self.Layout = QFormLayout()
        
        self.offsetX = -1*parent.StockCheckBox.x()
        
        StockCheckBox = QCheckBox(self)
        StockCheckBox.setGeometry(QRect(parent.StockCheckBox.x()+self.offsetX, 0, parent.StockCheckBox.width(), parent.StockCheckBox.height()))
        StockCheckBox.setObjectName(parent.StockCheckBox.objectName()+id)
        StockCheckBox.setFont(font)
        OpenLabel = QLabel(self)
        OpenLabel.setGeometry(QRect(parent.OpenLabel.x()+self.offsetX, 0, parent.OpenLabel.width(), parent.OpenLabel.height()))
        OpenLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        OpenLabel.setObjectName(parent.OpenLabel.objectName()+id)
        OpenLabel.setFont(font)
        HightLabel = QLabel(self)
        HightLabel.setGeometry(QRect(parent.HightLabel.x()+self.offsetX, 0, parent.HightLabel.width(), parent.HightLabel.height()))
        HightLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        HightLabel.setObjectName(parent.HightLabel.objectName()+id)
        HightLabel.setFont(font)
        LowLabel = QLabel(self)
        LowLabel.setGeometry(QRect(parent.LowLabel.x()+self.offsetX, 0, parent.LowLabel.width(), parent.LowLabel.height()))
        LowLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        LowLabel.setObjectName(parent.LowLabel.objectName()+id)
        LowLabel.setFont(font)
        CloseLabel = QLabel(self)
        CloseLabel.setGeometry(QRect(parent.CloseLabel.x()+self.offsetX, 0, parent.CloseLabel.width(), parent.CloseLabel.height()))
        CloseLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        CloseLabel.setObjectName(parent.CloseLabel.objectName()+id)
        CloseLabel.setFont(font)
        VolumeLabel = QLabel(self)
        VolumeLabel.setGeometry(QRect(parent.VolumeLabel.x()+self.offsetX, 0, parent.VolumeLabel.width(), parent.VolumeLabel.height()))
        VolumeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        VolumeLabel.setObjectName(parent.VolumeLabel.objectName()+id)
        VolumeLabel.setFont(font)
        ChangeCLabel = QLabel(self)
        ChangeCLabel.setGeometry(QRect(parent.ChangeCLabel.x()+self.offsetX, 0, parent.ChangeCLabel.width(), parent.ChangeCLabel.height()))
        ChangeCLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        ChangeCLabel.setObjectName(parent.ChangeCLabel.objectName()+id)
        ChangeCLabel.setFont(fontBold)
        ChangeVLabel = QLabel(self)
        ChangeVLabel.setGeometry(QRect(parent.ChangeVLabel.x()+self.offsetX, 0, parent.ChangeVLabel.width(), parent.ChangeVLabel.height()))
        ChangeVLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        ChangeVLabel.setObjectName(parent.ChangeVLabel.objectName()+id)
        ChangeVLabel.setFont(fontBold)
        AvgC3MLabel = QLabel(self)
        AvgC3MLabel.setGeometry(QRect(parent.AvgC3MLabel.x()+self.offsetX, 0, parent.AvgC3MLabel.width(), parent.AvgC3MLabel.height()))
        AvgC3MLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        AvgC3MLabel.setObjectName(parent.AvgC3MLabel.objectName()+id)
        AvgC3MLabel.setFont(font)
        AvgV3MLabel = QLabel(self)
        AvgV3MLabel.setGeometry(QRect(parent.AvgV3MLabel.x()+self.offsetX, 0, parent.AvgV3MLabel.width(), parent.AvgV3MLabel.height()))
        AvgV3MLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        AvgV3MLabel.setObjectName(parent.AvgV3MLabel.objectName()+id)
        AvgV3MLabel.setFont(font)
        StrikePrice1YLabel = QLabel(self)
        StrikePrice1YLabel.setGeometry(QRect(parent.StrikePrice1YLabel.x()+self.offsetX, 0, parent.StrikePrice1YLabel.width(), parent.StrikePrice1YLabel.height()))
        StrikePrice1YLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        StrikePrice1YLabel.setObjectName(parent.StrikePrice1YLabel.objectName()+id)
        StrikePrice1YLabel.setFont(font)
        GraphSampleButton = QPushButton(self)
        GraphSampleButton.setEnabled(True)
        GraphSampleButton.setGeometry(QRect(parent.GraphSampleButton.x()+self.offsetX, 0, parent.GraphSampleButton.width(), parent.GraphSampleButton.height()))
        GraphSampleButton.setObjectName(parent.GraphSampleButton.objectName()+id)
        
        GraphSampleButton.clicked.connect(self.DoGraphButton)      
        
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
        
        self.Layout.addWidget(StockCheckBox)
        self.Layout.addWidget(OpenLabel)
        self.Layout.addWidget(HightLabel)
        self.Layout.addWidget(LowLabel)
        self.Layout.addWidget(CloseLabel)
        self.Layout.addWidget(VolumeLabel)
        self.Layout.addWidget(ChangeCLabel)
        self.Layout.addWidget(ChangeVLabel)
        self.Layout.addWidget(AvgC3MLabel)
        self.Layout.addWidget(AvgV3MLabel)
        self.Layout.addWidget(StrikePrice1YLabel)
        self.Layout.addWidget(GraphSampleButton)
        
        self.CalcWidgetSize()
   
    def CalcWidgetSize(self):
        min_x = sys.maxsize
        max_x = 0
        self.widget_height=0
        for i in range(self.Layout.count()):  
            widget = self.Layout.itemAt( i ).widget()            
            min_x = min(min_x, widget.x())
            max_x = max(max_x, widget.x()+widget.width())
            self.widget_height = max(self.widget_height, widget.height())
            
        self.widget_width = max_x - min_x
    
    def sizeHint( self ):
        return QSize( self.widget_width, self.widget_height )
    
    def DoGraphButton(self):    

        GraphType = self.GraphTypeComboBox.currentText()
        
        Back_N_Months=6
        if GraphType == 'BasicN' or GraphType == 'CandleN':
            response = QInputDialog().getText(None, "Back N Months", "Please Input Back N Months:")
            if response[1] == True and response[0] != '':
                Back_N_Months = int(response[0])
        
        TargetDate_back = self.TargetDate - pandas.DateOffset(months=Back_N_Months)
        df = GetStockPriceVolumeData(self.Symbol, gv.StockDataPoolPath, TargetDate_back, self.TargetDate)
        
        PlotType = ''
        if GraphType.find('Basic')!=-1:
            PlotType = 'Basic'
        elif GraphType.find('Candle')!=-1:
            PlotType = 'Candle'
   
        TechIndicators = []
        TechIndicators.append({strTechIndicatorKey:strMA ,             strParam:{strColor:'blue', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8}})
        TechIndicators.append({strTechIndicatorKey:strBollingerBands , strParam:{strColor:'grey', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8, strAreaColor: 'gold', strAreaAlpha:0.3}})        
        print(TechIndicators)
        
        PlotStockData(self.Symbol,df,PlotType,TechIndicators)
        
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
        