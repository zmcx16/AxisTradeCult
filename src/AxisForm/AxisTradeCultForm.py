# coding=UTF-8

import sys
from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AxisForm.OverviewStockPage import OverviewStockPage
from AxisForm.ChartPage import ChartPage

class AxisTradeCultForm(QMainWindow, Ui_AxisTradeCultForm):
    def __init__(self, parent=None):
        super(AxisTradeCultForm, self).__init__(parent)
        self.setupUi(self)
        self.setupUIEvent()
        self.setupAxisWidget()
        
    def setupUIEvent(self):
        pass
    
    def setupAxisWidget(self):
        self.OverviewStockPage = OverviewStockPage(self)
        self.ChartPage = ChartPage(self)