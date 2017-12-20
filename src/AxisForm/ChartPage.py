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
        self.TechIndicatorslayout = QVBoxLayout() 
        
        self.parent().ChartStartDate.setCalendarPopup(True)     
        self.parent().ChartStartDate.setDate(self.SetBackQDate(QDate.currentDate(),months=6))
        self.parent().ChartEndDate.setCalendarPopup(True)
        self.parent().ChartEndDate.setDate(QDate.currentDate())
        
        self.parent().scrollAreaWidgetContents_2.setLayout(self.TechIndicatorslayout)

        """
        test0 = TechIndicatorsWidget(self)
        self.TechIndicatorslayout.addWidget(test0)
        test1 = TechIndicatorsWidget(self)
        self.TechIndicatorslayout.addWidget(test1)
        """
        
        TechIndicatorsWidget_width = self.parent().scrollAreaWidgetContents_2.width() - 20
        
        """
        for i in range(10): 
            Indicator = TechIndicatorsWidget(self,[],TechIndicatorsWidget_width)
            Indicator.setGeometry(QRect(0,0,Indicator.widget_width,Indicator.widget_height))
            Indicator.setMinimumSize(Indicator.widget_width, Indicator.widget_height)
            
            Indicator.setObjectName('Indicator'+str(i))
                          
            self.TechIndicatorslayout.addWidget(Indicator)
            self.TechIndicatorslayout.setSpacing(1)     
        """
        
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
        
    def SetBackQDate(self, srcDate, years=0, months=3, days=0):
        pyDate = QDate.toPyDate(srcDate)
        pdDate = pandas.to_datetime(pyDate)
        TargetDate = pdDate - pandas.DateOffset(months=months,days=days,years=years)
        return QDate(TargetDate.year,TargetDate.month,TargetDate.day)

    def AddIndicatorToGroup(self,TechIndicatorParam):
        print(TechIndicatorParam)
    
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
        
        TechIndicatorParam = {}
        GetAllWidgetValInLayout(self.gridlayout)
        
        teee = {'key':5,'kk':6}
        self.TechIndicatorSignal.emit(teee)
        