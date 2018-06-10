# coding=UTF-8

import os
import sys

import Program.GlobalVar as gv
from AxisForm.AxisTradeCultForm import AxisTradeCultForm
from PyQt5.QtWidgets import QMainWindow, QApplication

from AxisPrediction.PredSoarCrash import *
from AxisPrediction.PredTrend import *

if __name__ == "__main__":
    gv.Init()
    PredTrendA("")