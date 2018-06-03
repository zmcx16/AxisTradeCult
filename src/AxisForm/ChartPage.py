import sys
import random
import copy

from AxisForm.UiAxisTradeCultForm import Ui_AxisTradeCultForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import concurrent.futures

from CommonDef.DefStr import *
import Program.GlobalVar as gv
from Program.Common import *
from AxisWeb.DownloadData import *
from AxisForm.MessageInfo import *
from AxisForm.Common import *
from AxisPlot.Plot import *


class ChartPage(QMainWindow):

    def __init__(self, parent = None):
        super(ChartPage, self).__init__(parent)
        self.setupUIEvent()

    def setupUIEvent(self):
        gv.ReadTechIndicatorGroups()

        self.TechIndicatorslayout = QVBoxLayout()

        self.parent().ui.ChartStartDate.setCalendarPopup(True)
        self.parent().ui.ChartStartDate.setDate(self.SetBackQDate(QDate.currentDate(), months = 6))
        self.parent().ui.ChartEndDate.setCalendarPopup(True)
        self.parent().ui.ChartEndDate.setDate(QDate.currentDate())
        self.parent().ui.DelChartGroupButton.clicked.connect(self.DoDelButton)
        self.parent().ui.ShowButton.clicked.connect(self.DoShowButton)

        self.parent().ui.scrollAreaWidgetContents_2.setLayout(self.TechIndicatorslayout)
        TechIndicatorsWidget_width = self.parent().ui.scrollAreaWidgetContents_2.width() - 40
        for key, value in TechIndicatorWidgetParam.items():
            Indicator = TechIndicatorWidget(self, key, value, TechIndicatorsWidget_width)
            Indicator.setGeometry(QRect(0, 0, Indicator.widget_width, Indicator.widget_height))
            Indicator.setMinimumSize(Indicator.widget_width, Indicator.widget_height)
            Indicator.setObjectName(key)
            Indicator.TechIndicatorSignal.connect(self.AddIndicatorToGroup)

            self.TechIndicatorslayout.addWidget(Indicator)
            self.TechIndicatorslayout.setSpacing(1)

        self.TechIndicatorslayout.setSpacing(5);
        self.TechIndicatorslayout.setContentsMargins(10, 10, 0, 10);

        self.SetStockGroupsComboBoxItem()
        self.SetChartGroupsComboBoxItem()
        self.SetGraphTypeComboBoxItem()
        
        self.RefreshStockInGroup()
        self.RefreshTechIndicatorsList()

    def SetGraphTypeComboBoxItem(self):
        self.parent().ui.ChartPageGraphTypeComboBox.clear()
        self.parent().ui.ChartPageGraphTypeComboBox.addItem('Basic')
        self.parent().ui.ChartPageGraphTypeComboBox.addItem('Candle')

    def SetStockGroupsComboBoxItem(self):
        try: self.parent().ui.ChartPageStockGroupsComboBox.currentIndexChanged.disconnect()
        except Exception: pass
        
        self.parent().ui.ChartPageStockGroupsComboBox.clear()
        self.parent().ui.ChartPageStockInGroupComboBox.clear()
        self.parent().ui.ChartPageStockGroupsComboBox.addItems(gv.StockGroups.keys())
        self.parent().ui.ChartPageStockGroupsComboBox.setCurrentIndex(0)
        self.parent().ui.ChartPageStockInGroupComboBox.addItems(gv.StockGroups[self.parent().ui.ChartPageStockGroupsComboBox.currentText()])
        
        self.parent().ui.ChartPageStockGroupsComboBox.currentIndexChanged.connect(self.RefreshStockInGroup)

    def RefreshStockInGroup(self):
        self.parent().ui.ChartPageStockInGroupComboBox.clear()
        self.parent().ui.ChartPageStockInGroupComboBox.addItems(gv.StockGroups[self.parent().ui.ChartPageStockGroupsComboBox.currentText()])

    def SetChartGroupsComboBoxItem(self):
        try: self.parent().ui.ChartGroupsComboBox.currentIndexChanged.disconnect()
        except Exception: pass
                
        self.parent().ui.ChartGroupsComboBox.clear()
        self.parent().ui.ChartGroupsComboBox.addItems(gv.TechIndicatorGroups.keys())
        self.parent().ui.ChartGroupsComboBox.setCurrentIndex(0)
        self.parent().ui.ChartGroupsComboBox.addItem('New Group')
        
        self.parent().ui.ChartGroupsComboBox.currentIndexChanged.connect(self.RefreshTechIndicatorsList)

    def RefreshTechIndicatorsList(self):
        if self.parent().ui.ChartGroupsComboBox.count() == 0:
            return False

        if self.parent().ui.ChartGroupsComboBox.currentText() == 'New Group':
            response = QInputDialog().getText(None, "Create Group", "Please Input New TechIndicatorsList Group Name:")

            self.parent().ui.ChartGroupsComboBox.setCurrentIndex(0)
            if response[1] == True and response[0] != '':
                gv.AddTechIndicatorGroup(response[0])
                self.SetChartGroupsComboBoxItem()
                self.parent().ui.ChartGroupsComboBox.setCurrentIndex(self.parent().ui.ChartGroupsComboBox.count() - 2)
            return True

        self.parent().ui.TechIndicatorsListWidget.clear()
        SelectGroupName = self.parent().ui.ChartGroupsComboBox.currentText()
        TechIndicators = gv.TechIndicatorGroups[SelectGroupName]

        # print(Statistics_TechIndicators)

        for TechIndicator in TechIndicators:
            IndicatorContent = self.FormatIndicatorParamString(TechIndicator.copy())
            item = QListWidgetItem(IndicatorContent);
            item.setIcon(QIcon(gv.ImgTsubasaPath));
            self.parent().ui.TechIndicatorsListWidget.addItem(item)

    def SetBackQDate(self, srcDate, years = 0, months = 3, days = 0):
        pyDate = QDate.toPyDate(srcDate)
        pdDate = pandas.to_datetime(pyDate)
        TargetDate = pdDate - pandas.DateOffset(months = months, days = days, years = years)
        return QDate(TargetDate.year, TargetDate.month, TargetDate.day)

    def FormatIndicatorParamString(self, Indicator):
        formatStr = '|<{0}>|   '.format(Indicator.pop(strName))
        for key, value in Indicator.items():
            formatStr += '[{0}: {1}], '.format(key, value)
        return formatStr[:-2]

    def AddIndicatorToGroup(self, TechIndicatorParam):
        print(TechIndicatorParam)
        NowGroup = self.parent().ui.ChartGroupsComboBox.currentText()
        gv.AddTechIndicatorInGroup(NowGroup, TechIndicatorParam)
        self.RefreshTechIndicatorsList()

    def DoDelButton(self):
        if self.parent().ui.ChartGroupsComboBox.count() <= 1:
            return False

        NowGroup = self.parent().ui.ChartGroupsComboBox.currentText()

        msg = DeleteGroupWarningMessage
        msg[Str_setText] = msg[Str_setText].format(NowGroup)
        msg[Str_setDetailedText] = 'None'
        if ShowWarningDialog(msg) == 'OK':
            select_index = self.parent().ui.ChartGroupsComboBox.currentIndex()
            gv.DeleteTechIndicatorGroup(NowGroup)
            self.parent().ui.ChartGroupsComboBox.setCurrentIndex(0)
            self.parent().ui.ChartGroupsComboBox.removeItem(select_index)

        self.RefreshTechIndicatorsList()
        return True

    def DelIndicatorInGroup(self):
        SelectGroupName = self.parent().ui.ChartGroupsComboBox.currentText()
        TechIndicators = gv.TechIndicatorGroups[SelectGroupName]
        current_ListWidget_index = self.parent().ui.TechIndicatorsListWidget.currentRow()
        if current_ListWidget_index >= 0:
            del TechIndicators[current_ListWidget_index]
            self.parent().ui.TechIndicatorsListWidget.takeItem(current_ListWidget_index)
            gv.ResetTechIndicatorInGroup(SelectGroupName, TechIndicators)

    def TechIndicatorGroupToFuncDict(self, TechIndicatorGroup):
        OutputTechIndicators = []
        for TechIndicator in TechIndicatorGroup:
            IndicatorName = TechIndicator.pop(strName, None)
            IndicatorParam = {}
            for key, value in TechIndicator.items():
                IndicatorParam[key] = value

            OutputTechIndicators.append({strName:IndicatorName, strParam:IndicatorParam})

        return OutputTechIndicators

    def DoShowButton(self):

        StockSymbol = self.parent().ui.ChartPageStockInGroupComboBox.currentText()

        StartDate = pandas.to_datetime(QDate.toPyDate(self.parent().ui.ChartStartDate.date()))
        EndDate = pandas.to_datetime(QDate.toPyDate(self.parent().ui.ChartEndDate.date()))
        df = GetStockPriceVolumeData(StockSymbol, gv.StockDataPoolPath, StartDate, EndDate)

        PlotType = self.parent().ui.ChartPageGraphTypeComboBox.currentText()

        SelectGroupName = self.parent().ui.ChartGroupsComboBox.currentText()
        TechIndicators = self.TechIndicatorGroupToFuncDict(copy.deepcopy(gv.TechIndicatorGroups[SelectGroupName]))
        print(TechIndicators)

        self.graph = ScrollableWindow(PlotStockData(StockSymbol, df, PlotType, TechIndicators, gv.SettingArgs[StrChartSizeFactor]))
        self.graph.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.DelIndicatorInGroup()

    def test(self):
        print('test')


class TechIndicatorWidget(QWidget):

    base_height = 50
    widget_width = 0
    widget_height = base_height
    MaxcolumnNum = 6
    IndicatorName = None
    IndicatorParam = None

    TechIndicatorSignal = pyqtSignal(dict)

    def __init__(self, parent, IndicatorName, IndicatorParam, width):
        super(TechIndicatorWidget, self).__init__(parent)
        self.widget_width = width
        self.IndicatorName = IndicatorName
        self.IndicatorParam = IndicatorParam
        self.initUI()

    def initUI(self):

        self.gridGroupBox = QGroupBox(self.IndicatorName, self);
        self.gridlayout = QGridLayout(self)

        row_index = 0
        col_index = 0
        for key, value in self.IndicatorParam.items():
            if value[strType] == strComboBox:
                Label = QLabel(self)
                Label.setText(key)
                ComboBox = QComboBox(self)
                ComboBox.setObjectName(key)
                for item in value[strComboList]:
                    ComboBox.addItem(item)
                ComboBox.setCurrentIndex(random.randint(0, len(value[strComboList]) - 1))
                self.gridlayout.addWidget(Label, row_index, col_index);
                col_index += 1
                self.gridlayout.addWidget(ComboBox, row_index, col_index);
                col_index += 1
            elif value[strType] == strLineEdit:
                Label = QLabel(self)
                Label.setText(key)
                LineEdit = QLineEdit(self)
                LineEdit.setText(str(value[strValue]))
                LineEdit.setObjectName(key)
                self.gridlayout.addWidget(Label, row_index, col_index);
                col_index += 1
                self.gridlayout.addWidget(LineEdit, row_index, col_index);
                col_index += 1

            if col_index >= self.MaxcolumnNum:
                col_index = 0
                row_index += 1
                self.widget_height += self.base_height

        Button = QPushButton(self)
        Button.setText(strAdd)
        Button.setObjectName(strButton)
        Button.clicked.connect(self.AddTechIndicator)
        self.gridlayout.addWidget(Button, row_index, self.MaxcolumnNum - 1);

        self.gridGroupBox.resize(self.widget_width, self.widget_height)
        self.gridGroupBox.setLayout(self.gridlayout);

    def sizeHint(self):
        return QSize(self.gridGroupBox.size())

    def AddTechIndicator(self):
        OutputParam = {}
        OutputParam[strName] = self.IndicatorName
        GetAllWidgetValInLayout(self.gridlayout, OutputParam)
        self.TechIndicatorSignal.emit(OutputParam)
