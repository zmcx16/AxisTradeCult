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
        
        
        
    def SetBackQDate(self, srcDate, years=0, months=3, days=0):
        pyDate = QDate.toPyDate(srcDate)
        pdDate = pandas.to_datetime(pyDate)
        TargetDate = pdDate - pandas.DateOffset(months=months,days=days,years=years)
        return QDate(TargetDate.year,TargetDate.month,TargetDate.day)
    

class TechIndicatorsWidget(QWidget):
  
    def __init__(self,parent):      
        super(TechIndicatorsWidget, self).__init__()        
        self.initUI(parent)
        
    def initUI(self,parent):

        
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
    