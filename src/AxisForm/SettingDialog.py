from AxisForm.UiSetting import Ui_SettingDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Program.DefStr import *
import Program.GlobalVar as gv


def Do_actionSetting(self):
    self.SettingDialog = SettingDialog()
    self.SettingDialog.show()
    if self.SettingDialog.exec_():
        gv.SettingArgs[StrChartSizeFactor] = float(self.SettingDialog.getInputs())
        gv.SaveSettingArgs()


class SettingDialog(QDialog, Ui_SettingDialog):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.LoadSettingArgs()

    def LoadSettingArgs(self):
        self.ChartSizeFactorLineEdit.setText(str(gv.SettingArgs[StrChartSizeFactor]))

    def getInputs(self):
        return self.ChartSizeFactorLineEdit.text()
