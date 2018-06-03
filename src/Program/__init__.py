# coding=UTF-8

import os
import sys

import Program.GlobalVar as gv
from AxisForm.AxisTradeCultForm import AxisTradeCultForm
from PyQt5.QtWidgets import QMainWindow, QApplication

from AxisPrediction.PredSoarCrash import *

if __name__ == "__main__":
    """
    gv.Init()
    app = QApplication(sys.argv)
    window = AxisTradeCultForm()
    window.show()
    sys.exit(app.exec_())
    """
    gv.Init()
    PredSoarCrashA("")
    print("!!")

