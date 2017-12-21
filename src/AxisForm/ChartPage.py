import sys
import random

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
                
        self.parent().scrollAreaWidgetContents_2.setLayout(self.TechIndicatorslayout)
        TechIndicatorsWidget_width = self.parent().scrollAreaWidgetContents_2.width() - 20        
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
        
        print(TechIndicators)
        
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
                ComboBox.setCurrentIndex(random.randint(0,len(value[strComboList])))
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
        