import sys
from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot

import Program.GlobalVar as gv
from AxisWeb.DownloadData import *

class AxisTradeCultForm(QMainWindow, Ui_AxisTradeCultForm):
    def __init__(self, parent=None):
        super(AxisTradeCultForm, self).__init__(parent)
        self.setupUi(self)
        self.setupUIEvent(self)
    
    def setupUIEvent(self,AxisTradeCultForm):
        self.UpdateButton.clicked.connect(self.DoUpdateButton)
    
    @pyqtSlot()  
    def DoUpdateButton(self):
        DownloadAllStockGroupsFromQuandl(gv.StockDataPoolPath)