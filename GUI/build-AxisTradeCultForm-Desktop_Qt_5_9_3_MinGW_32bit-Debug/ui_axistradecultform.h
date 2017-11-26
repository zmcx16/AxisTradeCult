/********************************************************************************
** Form generated from reading UI file 'axistradecultform.ui'
**
** Created by: Qt User Interface Compiler version 5.9.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_AXISTRADECULTFORM_H
#define UI_AXISTRADECULTFORM_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDateEdit>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QListView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_AxisTradeCultForm
{
public:
    QAction *actionDataManager;
    QWidget *centralWidget;
    QTabWidget *tabWidget;
    QWidget *tabOverview;
    QDateEdit *DisplayDate;
    QComboBox *StockGroupsComboBox;
    QPushButton *UpdateButton;
    QListView *listView;
    QWidget *tab_2;
    QMenuBar *menuBar;
    QMenu *menuSetting;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *AxisTradeCultForm)
    {
        if (AxisTradeCultForm->objectName().isEmpty())
            AxisTradeCultForm->setObjectName(QStringLiteral("AxisTradeCultForm"));
        AxisTradeCultForm->resize(908, 533);
        actionDataManager = new QAction(AxisTradeCultForm);
        actionDataManager->setObjectName(QStringLiteral("actionDataManager"));
        centralWidget = new QWidget(AxisTradeCultForm);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        tabWidget = new QTabWidget(centralWidget);
        tabWidget->setObjectName(QStringLiteral("tabWidget"));
        tabWidget->setGeometry(QRect(10, 10, 891, 471));
        tabOverview = new QWidget();
        tabOverview->setObjectName(QStringLiteral("tabOverview"));
        DisplayDate = new QDateEdit(tabOverview);
        DisplayDate->setObjectName(QStringLiteral("DisplayDate"));
        DisplayDate->setGeometry(QRect(10, 10, 110, 31));
        StockGroupsComboBox = new QComboBox(tabOverview);
        StockGroupsComboBox->setObjectName(QStringLiteral("StockGroupsComboBox"));
        StockGroupsComboBox->setGeometry(QRect(140, 10, 141, 31));
        UpdateButton = new QPushButton(tabOverview);
        UpdateButton->setObjectName(QStringLiteral("UpdateButton"));
        UpdateButton->setGeometry(QRect(770, 10, 101, 31));
        listView = new QListView(tabOverview);
        listView->setObjectName(QStringLiteral("listView"));
        listView->setGeometry(QRect(5, 50, 871, 381));
        tabWidget->addTab(tabOverview, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QStringLiteral("tab_2"));
        tabWidget->addTab(tab_2, QString());
        AxisTradeCultForm->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(AxisTradeCultForm);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 908, 26));
        menuSetting = new QMenu(menuBar);
        menuSetting->setObjectName(QStringLiteral("menuSetting"));
        AxisTradeCultForm->setMenuBar(menuBar);
        statusBar = new QStatusBar(AxisTradeCultForm);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        AxisTradeCultForm->setStatusBar(statusBar);

        menuBar->addAction(menuSetting->menuAction());
        menuSetting->addAction(actionDataManager);

        retranslateUi(AxisTradeCultForm);

        tabWidget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(AxisTradeCultForm);
    } // setupUi

    void retranslateUi(QMainWindow *AxisTradeCultForm)
    {
        AxisTradeCultForm->setWindowTitle(QApplication::translate("AxisTradeCultForm", "AxisTradeCultForm", Q_NULLPTR));
        actionDataManager->setText(QApplication::translate("AxisTradeCultForm", "DataManager", Q_NULLPTR));
        UpdateButton->setText(QApplication::translate("AxisTradeCultForm", "Update", Q_NULLPTR));
        tabWidget->setTabText(tabWidget->indexOf(tabOverview), QApplication::translate("AxisTradeCultForm", "Overview", Q_NULLPTR));
        tabWidget->setTabText(tabWidget->indexOf(tab_2), QApplication::translate("AxisTradeCultForm", "Tab 2", Q_NULLPTR));
        menuSetting->setTitle(QApplication::translate("AxisTradeCultForm", "Setting", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class AxisTradeCultForm: public Ui_AxisTradeCultForm {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_AXISTRADECULTFORM_H
