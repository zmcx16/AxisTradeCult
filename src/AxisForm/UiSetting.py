# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        SettingDialog.setObjectName("SettingDialog")
        SettingDialog.resize(277, 185)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 140, 231, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.ChartGroupBox = QtWidgets.QGroupBox(SettingDialog)
        self.ChartGroupBox.setGeometry(QtCore.QRect(10, 10, 251, 121))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ChartGroupBox.setFont(font)
        self.ChartGroupBox.setObjectName("ChartGroupBox")
        self.ChartSizeFactorLineEdit = QtWidgets.QLineEdit(self.ChartGroupBox)
        self.ChartSizeFactorLineEdit.setGeometry(QtCore.QRect(160, 40, 71, 23))
        self.ChartSizeFactorLineEdit.setObjectName("ChartSizeFactorLineEdit")
        self.label = QtWidgets.QLabel(self.ChartGroupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 131, 21))
        self.label.setObjectName("label")

        self.retranslateUi(SettingDialog)
        self.buttonBox.accepted.connect(SettingDialog.accept)
        self.buttonBox.rejected.connect(SettingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingDialog)

    def retranslateUi(self, SettingDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingDialog.setWindowTitle(_translate("SettingDialog", "Dialog"))
        self.ChartGroupBox.setTitle(_translate("SettingDialog", "Chart Setting"))
        self.ChartSizeFactorLineEdit.setText(_translate("SettingDialog", "2.5"))
        self.label.setText(_translate("SettingDialog", "Chart Size Factor"))

