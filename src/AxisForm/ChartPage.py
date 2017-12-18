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
        
        TechIndicatorsWidget_width = self.parent().scrollAreaWidgetContents_2.width() - 40
        
        for i in range(10): 
            Indicator = TechIndicatorsWidget(self,TechIndicatorsWidget_width)
            Indicator.setGeometry(QRect(0,0,Indicator.widget_width,Indicator.widget_height))
            Indicator.setMinimumSize(Indicator.widget_width, Indicator.widget_height)
            
            Indicator.setObjectName('Indicator'+str(i))
                          
            self.TechIndicatorslayout.addWidget(Indicator)
            self.TechIndicatorslayout.setSpacing(1)     
         
        
        self.TechIndicatorslayout.setSpacing(5);
        self.TechIndicatorslayout.setContentsMargins(10, 10, 0, 10);        
        
    def SetBackQDate(self, srcDate, years=0, months=3, days=0):
        pyDate = QDate.toPyDate(srcDate)
        pdDate = pandas.to_datetime(pyDate)
        TargetDate = pdDate - pandas.DateOffset(months=months,days=days,years=years)
        return QDate(TargetDate.year,TargetDate.month,TargetDate.day)
    
    def test(self):
        print('xxx')

class TechIndicatorsWidget(QWidget):


    #TechIndicators.append({strTechIndicatorKey:strMA ,             strParam:{strColor:'blue', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8}})
    #TechIndicators.append({strTechIndicatorKey:strBollingerBands , strParam:{strColor:'grey', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8, strAreaColor: 'gold', strAreaAlpha:0.3}}) 


    base_height = 50    
    widget_width = 0
    widget_height = 0 
    
    def __init__(self,parent,width):      
        super(TechIndicatorsWidget, self).__init__(parent) 
        self.widget_width = width    
        self.initUI()
        
    def initUI(self):
        
        self.gridGroupBox = QGroupBox(self);  
        self.gridlayout = QGridLayout(self)
        print(self.gridGroupBox.size())
                
        self.ColorLabel = QLabel(self);
        self.ColorComboBox = QComboBox(self);        
        self.WindowLabel = QLabel(self);
        self.WindowLineEdit = QLineEdit(self);   
        self.LineWidthLabel = QLabel(self);
        self.LineWidthLineEdit = QLineEdit(self);         
        self.AlphaLabel = QLabel(self);
        self.AlphaLineEdit = QLineEdit(self);         
                
        for color in ColorList:
            self.ColorComboBox.addItem(color)
            
        _translate = QCoreApplication.translate
        self.ColorLabel.setText(_translate("AxisTradeCultForm", strColor))
        self.ColorComboBox.setCurrentIndex(random.randint(0,len(ColorList)))        
        self.WindowLabel.setText(_translate("AxisTradeCultForm", strWindow))  
        self.WindowLineEdit.setText(str(20))   
        self.LineWidthLabel.setText(_translate("AxisTradeCultForm", strLineWidth))  
        self.LineWidthLineEdit.setText(str(0.8))  
        self.AlphaLabel.setText(_translate("AxisTradeCultForm", strAlpha))  
        self.AlphaLineEdit.setText(str(0.8))                  
            
        self.widget_height += self.base_height
        self.gridlayout.addWidget(self.ColorLabel, 1, 0);
        self.gridlayout.addWidget(self.ColorComboBox, 1, 1);
        self.gridlayout.addWidget(self.WindowLabel, 1, 3);
        self.gridlayout.addWidget(self.WindowLineEdit, 1, 4);

        self.gridlayout.addWidget(self.LineWidthLabel, 1, 6);
        self.gridlayout.addWidget(self.LineWidthLineEdit, 1,7);
        self.widget_height += self.base_height
        self.gridlayout.addWidget(self.AlphaLabel, 2, 0);
        self.gridlayout.addWidget(self.AlphaLineEdit, 2, 1);        
        
        self.gridGroupBox.resize(self.widget_width,self.widget_height)        
        self.gridGroupBox.setLayout(self.gridlayout);
       
    def sizeHint( self ):
        return QSize(self.gridGroupBox.size())