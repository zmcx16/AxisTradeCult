# coding=UTF-8

from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AxisForm.OverviewStockPage import OverviewStockPage
from AxisForm.ChartPage import ChartPage

from AxisForm.SettingDialog import *


class AxisTradeCultForm(QMainWindow):
    def __init__(self, parent=None):
        super(AxisTradeCultForm, self).__init__(parent)
        self.ui = Ui_AxisTradeCultForm()
        self.ui.setupUi(self)

        self.setupUIEvent()
        self.setupAxisWidget()

    def setupUIEvent(self):
        self.ui.menuSetting.triggered[QAction].connect(Do_actionSetting)

    def setupAxisWidget(self):
        gv.ReadSettingArgs()

        self.OverviewStockPage = OverviewStockPage(self)
        self.ChartPage = ChartPage(self)
        # self.ChartPage.setFocusPolicy(Qt.StrongFocus)
        # self.setFocusProxy(self.ChartPage)

    def keyPressEvent(self, event):
        if self.ui.tabWidget.currentWidget() == self.ui.tabChart:
            self.ChartPage.keyPressEvent(event)
