/********************************************************************************
** Form generated from reading UI file 'setting.ui'
**
** Created by: Qt User Interface Compiler version 5.10.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SETTING_H
#define UI_SETTING_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>

QT_BEGIN_NAMESPACE

class Ui_SettingDialog
{
public:
    QDialogButtonBox *buttonBox;
    QGroupBox *ChartGroupBox;
    QLineEdit *ChartSizeFactorLineEdit;
    QLabel *label;

    void setupUi(QDialog *SettingDialog)
    {
        if (SettingDialog->objectName().isEmpty())
            SettingDialog->setObjectName(QStringLiteral("SettingDialog"));
        SettingDialog->resize(277, 185);
        buttonBox = new QDialogButtonBox(SettingDialog);
        buttonBox->setObjectName(QStringLiteral("buttonBox"));
        buttonBox->setGeometry(QRect(30, 140, 231, 32));
        buttonBox->setOrientation(Qt::Horizontal);
        buttonBox->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);
        ChartGroupBox = new QGroupBox(SettingDialog);
        ChartGroupBox->setObjectName(QStringLiteral("ChartGroupBox"));
        ChartGroupBox->setGeometry(QRect(10, 10, 251, 121));
        QFont font;
        font.setPointSize(11);
        ChartGroupBox->setFont(font);
        ChartSizeFactorLineEdit = new QLineEdit(ChartGroupBox);
        ChartSizeFactorLineEdit->setObjectName(QStringLiteral("ChartSizeFactorLineEdit"));
        ChartSizeFactorLineEdit->setGeometry(QRect(160, 40, 71, 23));
        label = new QLabel(ChartGroupBox);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(10, 40, 131, 21));

        retranslateUi(SettingDialog);
        QObject::connect(buttonBox, SIGNAL(accepted()), SettingDialog, SLOT(accept()));
        QObject::connect(buttonBox, SIGNAL(rejected()), SettingDialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(SettingDialog);
    } // setupUi

    void retranslateUi(QDialog *SettingDialog)
    {
        SettingDialog->setWindowTitle(QApplication::translate("SettingDialog", "Dialog", nullptr));
        ChartGroupBox->setTitle(QApplication::translate("SettingDialog", "Chart Setting", nullptr));
        ChartSizeFactorLineEdit->setText(QApplication::translate("SettingDialog", "2.5", nullptr));
        label->setText(QApplication::translate("SettingDialog", "Chart Size Factor", nullptr));
    } // retranslateUi

};

namespace Ui {
    class SettingDialog: public Ui_SettingDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SETTING_H
