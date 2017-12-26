import sys
import random
import copy

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


class ChartPage(QMainWindow):

    def __init__(self, parent=None):   
        super(ChartPage, self).__init__(parent)
        self.setupUIEvent()
        
    def setupUIEvent(self):
        gv.ReadTechIndicatorGroups()
        
        self.TechIndicatorslayout = QVBoxLayout() 
        
        self.parent().ChartStartDate.setCalendarPopup(True)     
        self.parent().ChartStartDate.setDate(self.SetBackQDate(QDate.currentDate(),months=6))
        self.parent().ChartEndDate.setCalendarPopup(True)
        self.parent().ChartEndDate.setDate(QDate.currentDate())
        self.parent().ChartGroupsComboBox.currentIndexChanged.connect(self.RefreshTechIndicatorsList)
        self.parent().ChartPageStockGroupsComboBox.currentIndexChanged.connect(self.RefreshStockInGroup)
        self.parent().DelChartGroupButton.clicked.connect(self.DoDelButton)
        self.parent().ShowButton.clicked.connect(self.DoShowButton)
         
        self.parent().scrollAreaWidgetContents_2.setLayout(self.TechIndicatorslayout)
        TechIndicatorsWidget_width = self.parent().scrollAreaWidgetContents_2.width() - 40        
        for key,value in TechIndicatorWidgetParam.items():
            Indicator = TechIndicatorWidget(self, key, value,TechIndicatorsWidget_width)
            Indicator.setGeometry(QRect(0,0,Indicator.widget_width,Indicator.widget_height))
            Indicator.setMinimumSize(Indicator.widget_width, Indicator.widget_height)            
            Indicator.setObjectName(key)
            Indicator.TechIndicatorSignal.connect(self.AddIndicatorToGroup)
            
            self.TechIndicatorslayout.addWidget(Indicator)
            self.TechIndicatorslayout.setSpacing(1)             
  
        self.TechIndicatorslayout.setSpacing(5);
        self.TechIndicatorslayout.setContentsMargins(10, 10, 0, 10);        
        
        self.SetChartGroupsComboBoxItem()
        self.SetStockGroupsComboBoxItem()
        self.SetGraphTypeComboBoxItem()
        
    def SetGraphTypeComboBoxItem(self):
        self.parent().ChartPageGraphTypeComboBox.clear()        
        self.parent().ChartPageGraphTypeComboBox.addItem('Basic')
        self.parent().ChartPageGraphTypeComboBox.addItem('Candle')

    def SetStockGroupsComboBoxItem(self):
        self.parent().ChartPageStockGroupsComboBox.clear()        
        self.parent().ChartPageStockInGroupComboBox.clear() 
        self.parent().ChartPageStockGroupsComboBox.addItems(gv.StockGroups.keys())     
        self.parent().ChartPageStockGroupsComboBox.setCurrentIndex(0)
        self.parent().ChartPageStockInGroupComboBox.addItems(gv.StockGroups[self.parent().ChartPageStockGroupsComboBox.currentText()])          

    def RefreshStockInGroup(self):
        self.parent().ChartPageStockInGroupComboBox.clear()
        self.parent().ChartPageStockInGroupComboBox.addItems(gv.StockGroups[self.parent().ChartPageStockGroupsComboBox.currentText()])          
     
        
    def SetChartGroupsComboBoxItem(self):
        self.parent().ChartGroupsComboBox.clear()
        self.parent().ChartGroupsComboBox.addItems(gv.TechIndicatorGroups.keys())
        self.parent().ChartGroupsComboBox.addItem('New Group')
    
    def RefreshTechIndicatorsList(self):
        if self.parent().ChartGroupsComboBox.count() == 0:
            return False
                        
        if self.parent().ChartGroupsComboBox.currentText() == 'New Group':
            response = QInputDialog().getText(None, "Create Group", "Please Input New Group Name:")

            self.parent().ChartGroupsComboBox.setCurrentIndex(0)
            if response[1] == True and response[0] != '':
                gv.AddTechIndicatorGroup(response[0])
                self.SetChartGroupsComboBoxItem()
                self.parent().ChartGroupsComboBox.setCurrentIndex(self.parent().ChartGroupsComboBox.count()-2)         
            return True
        
        self.parent().TechIndicatorsListWidget.clear()
        SelectGroupName = self.parent().ChartGroupsComboBox.currentText()
        TechIndicators = gv.TechIndicatorGroups[SelectGroupName]
        
        #print(TechIndicators)
        
        for TechIndicator in TechIndicators:   
            IndicatorContent = self.FormatIndicatorParamString(TechIndicator.copy())
            item = QListWidgetItem(IndicatorContent);
            item.setIcon(QIcon(gv.ImgTsubasaPath));      
            self.parent().TechIndicatorsListWidget.addItem(item)
                
    def SetBackQDate(self, srcDate, years=0, months=3, days=0):
        pyDate = QDate.toPyDate(srcDate)
        pdDate = pandas.to_datetime(pyDate)
        TargetDate = pdDate - pandas.DateOffset(months=months,days=days,years=years)
        return QDate(TargetDate.year,TargetDate.month,TargetDate.day)

    def FormatIndicatorParamString(self, Indicator):
        formatStr = '|<{0}>|   '.format(Indicator.pop(strName))
        for key,value in Indicator.items():
            formatStr+='[{0}: {1}], '.format(key,value)
        return formatStr[:-2]

    def AddIndicatorToGroup(self,TechIndicatorParam):
        print(TechIndicatorParam)
        NowGroup = self.parent().ChartGroupsComboBox.currentText()                            
        gv.AddTechIndicatorInGroup(NowGroup,TechIndicatorParam)
        self.RefreshTechIndicatorsList()        
        
    def DoDelButton(self):
        if self.parent().ChartGroupsComboBox.count() <= 1:
            return False
        
        NowGroup = self.parent().ChartGroupsComboBox.currentText()
        
        msg = DeleteGroupWarningMessage
        msg[Str_setText] = msg[Str_setText].format(NowGroup)     
        msg[Str_setDetailedText] = 'None'     
        if ShowWarningDialog(msg) == 'OK':
            select_index = self.parent().ChartGroupsComboBox.currentIndex()
            gv.DeleteTechIndicatorGroup(NowGroup)
            self.parent().ChartGroupsComboBox.setCurrentIndex(0)
            self.parent().ChartGroupsComboBox.removeItem(select_index)
        
        self.RefreshTechIndicatorsList()            
        return True  


    def DelIndicatorInGroup(self):
        SelectGroupName = self.parent().ChartGroupsComboBox.currentText()
        TechIndicators = gv.TechIndicatorGroups[SelectGroupName]
        current_ListWidget_index = self.parent().TechIndicatorsListWidget.currentRow()
        if current_ListWidget_index >=0:
            del TechIndicators[current_ListWidget_index]
            self.parent().TechIndicatorsListWidget.takeItem(current_ListWidget_index) 
            gv.ResetTechIndicatorInGroup(SelectGroupName,TechIndicators)            

    def TechIndicatorGroupToFuncDict(self, TechIndicatorGroup):
        OutputTechIndicators = []
        for TechIndicator in TechIndicatorGroup: 
            IndicatorName = TechIndicator.pop(strName,None)
            IndicatorParam = {}
            for key,value in TechIndicator.items(): 
                IndicatorParam[key] = value
            
            OutputTechIndicators.append({strName:IndicatorName,strParam:IndicatorParam})
        
        return OutputTechIndicators
        
    def DoShowButton(self):    

        StockSymbol = self.parent().ChartPageStockInGroupComboBox.currentText()
        
        StartDate = pandas.to_datetime(QDate.toPyDate(self.parent().ChartStartDate.date()))
        EndDate = pandas.to_datetime(QDate.toPyDate(self.parent().ChartEndDate.date()))
        df = GetStockPriceVolumeData(StockSymbol, gv.StockDataPoolPath, StartDate, EndDate)
        
        PlotType = self.parent().ChartPageGraphTypeComboBox.currentText()

        SelectGroupName = self.parent().ChartGroupsComboBox.currentText()       
        TechIndicators = self.TechIndicatorGroupToFuncDict(copy.deepcopy(gv.TechIndicatorGroups[SelectGroupName]))  
        print(TechIndicators)
       
        PlotStockData(StockSymbol,df,PlotType,TechIndicators)            
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.DelIndicatorInGroup()

    def test(self):
        print('xxx')

class TechIndicatorWidget(QWidget):

    base_height = 50    
    widget_width = 0
    widget_height = base_height 
    MaxcolumnNum = 6
    IndicatorName = None
    IndicatorParam = None
    
    TechIndicatorSignal = pyqtSignal(dict)
    
    def __init__(self,parent,IndicatorName,IndicatorParam,width):      
        super(TechIndicatorWidget, self).__init__(parent) 
        self.widget_width = width
        self.IndicatorName = IndicatorName  
        self.IndicatorParam = IndicatorParam   
        self.initUI()
        
    def initUI(self):
        
        self.gridGroupBox = QGroupBox(self.IndicatorName,self); 
        self.gridlayout = QGridLayout(self)
        
        row_index=0
        col_index=0
        for key,value in self.IndicatorParam.items():            
            if value[strType] == strComboBox:
                Label = QLabel(self)
                Label.setText(key)
                ComboBox = QComboBox(self)  
                ComboBox.setObjectName(key)
                for item in value[strComboList]:
                    ComboBox.addItem(item)
                ComboBox.setCurrentIndex(random.randint(0,len(value[strComboList])-1))
                self.gridlayout.addWidget(Label, row_index, col_index); 
                col_index+=1
                self.gridlayout.addWidget(ComboBox, row_index, col_index); 
                col_index+=1                  
            elif value[strType] == strLineEdit:
                Label = QLabel(self)
                Label.setText(key)
                LineEdit = QLineEdit(self)
                LineEdit.setText(str(value[strValue]))
                LineEdit.setObjectName(key)
                self.gridlayout.addWidget(Label, row_index, col_index); 
                col_index+=1
                self.gridlayout.addWidget(LineEdit, row_index, col_index); 
                col_index+=1                        

            if col_index >= self.MaxcolumnNum:
                col_index=0
                row_index+=1
                self.widget_height += self.base_height
                     
        Button = QPushButton(self)
        Button.setText(strAdd)
        Button.setObjectName(strButton)  
        Button.clicked.connect(self.AddTechIndicator)        
        self.gridlayout.addWidget(Button, row_index, self.MaxcolumnNum-1); 
        
        self.gridGroupBox.resize(self.widget_width,self.widget_height)        
        self.gridGroupBox.setLayout(self.gridlayout);       
        
    def sizeHint( self ):
        return QSize(self.gridGroupBox.size())
    
    def AddTechIndicator(self):      
        OutputParam = {}
        OutputParam[strName] = self.IndicatorName
        GetAllWidgetValInLayout(self.gridlayout,OutputParam)
        self.TechIndicatorSignal.emit(OutputParam)
        