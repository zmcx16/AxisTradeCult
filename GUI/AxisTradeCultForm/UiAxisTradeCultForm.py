# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'axistradecultform.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AxisTradeCultForm(object):
    def setupUi(self, AxisTradeCultForm):
        AxisTradeCultForm.setObjectName("AxisTradeCultForm")
        AxisTradeCultForm.resize(908, 533)
        self.centralWidget = QtWidgets.QWidget(AxisTradeCultForm)
        self.centralWidget.setObjectName("centralWidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 891, 471))
        self.tabWidget.setObjectName("tabWidget")
        self.tabOverview = QtWidgets.QWidget()
        self.tabOverview.setObjectName("tabOverview")
        self.DisplayDate = QtWidgets.QDateEdit(self.tabOverview)
        self.DisplayDate.setGeometry(QtCore.QRect(10, 10, 110, 31))
        self.DisplayDate.setObjectName("DisplayDate")
        self.StockGroupsComboBox = QtWidgets.QComboBox(self.tabOverview)
        self.StockGroupsComboBox.setGeometry(QtCore.QRect(140, 10, 141, 31))
        self.StockGroupsComboBox.setObjectName("StockGroupsComboBox")
        self.UpdateButton = QtWidgets.QPushButton(self.tabOverview)
        self.UpdateButton.setGeometry(QtCore.QRect(490, 10, 101, 31))
        self.UpdateButton.setObjectName("UpdateButton")
        self.listView = QtWidgets.QListView(self.tabOverview)
        self.listView.setGeometry(QtCore.QRect(5, 50, 871, 381))
        self.listView.setObjectName("listView")
        self.UpdateProgressBar = QtWidgets.QProgressBar(self.tabOverview)
        self.UpdateProgressBar.setGeometry(QtCore.QRect(300, 10, 181, 31))
        self.UpdateProgressBar.setProperty("value", 0)
        self.UpdateProgressBar.setObjectName("UpdateProgressBar")
        self.tabWidget.addTab(self.tabOverview, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        AxisTradeCultForm.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(AxisTradeCultForm)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 908, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuSetting = QtWidgets.QMenu(self.menuBar)
        self.menuSetting.setObjectName("menuSetting")
        AxisTradeCultForm.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(AxisTradeCultForm)
        self.statusBar.setObjectName("statusBar")
        AxisTradeCultForm.setStatusBar(self.statusBar)
        self.actionDataManager = QtWidgets.QAction(AxisTradeCultForm)
        self.actionDataManager.setObjectName("actionDataManager")
        self.menuSetting.addAction(self.actionDataManager)
        self.menuBar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(AxisTradeCultForm)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AxisTradeCultForm)

    def retranslateUi(self, AxisTradeCultForm):
        _translate = QtCore.QCoreApplication.translate
        AxisTradeCultForm.setWindowTitle(_translate("AxisTradeCultForm", "AxisTradeCultForm"))
        self.UpdateButton.setText(_translate("AxisTradeCultForm", "Update"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOverview), _translate("AxisTradeCultForm", "Overview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AxisTradeCultForm", "Tab 2"))
        self.menuSetting.setTitle(_translate("AxisTradeCultForm", "Setting"))
        self.actionDataManager.setText(_translate("AxisTradeCultForm", "DataManager"))

