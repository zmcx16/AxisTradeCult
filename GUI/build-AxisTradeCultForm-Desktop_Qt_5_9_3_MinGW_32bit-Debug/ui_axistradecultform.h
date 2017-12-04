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
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDateEdit>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
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
    QProgressBar *UpdateProgressBar;
    QLabel *SymbolLabel;
    QLabel *OpenLabel;
    QLabel *HightLabel;
    QLabel *LowLabel;
    QLabel *CloseLabel;
    QLabel *VolumeLabel;
    QLabel *ChangeCLabel;
    QLabel *ChangeVLabel;
    QLabel *AvgC3MLabel;
    QLabel *AvgV3MLabel;
    QPushButton *GraphSampleButton;
    QFrame *line;
    QLabel *StrikePrice1YLabel;
    QLineEdit *Stockline;
    QPushButton *AddButton;
    QCheckBox *StockCheckBox;
    QPushButton *DelButton;
    QScrollArea *OverviewScrollArea;
    QWidget *scrollAreaWidgetContents;
    QWidget *tab_2;
    QMenuBar *menuBar;
    QMenu *menuSetting;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *AxisTradeCultForm)
    {
        if (AxisTradeCultForm->objectName().isEmpty())
            AxisTradeCultForm->setObjectName(QStringLiteral("AxisTradeCultForm"));
        AxisTradeCultForm->resize(968, 533);
        actionDataManager = new QAction(AxisTradeCultForm);
        actionDataManager->setObjectName(QStringLiteral("actionDataManager"));
        centralWidget = new QWidget(AxisTradeCultForm);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        tabWidget = new QTabWidget(centralWidget);
        tabWidget->setObjectName(QStringLiteral("tabWidget"));
        tabWidget->setGeometry(QRect(10, 10, 951, 471));
        tabOverview = new QWidget();
        tabOverview->setObjectName(QStringLiteral("tabOverview"));
        DisplayDate = new QDateEdit(tabOverview);
        DisplayDate->setObjectName(QStringLiteral("DisplayDate"));
        DisplayDate->setGeometry(QRect(70, 10, 110, 31));
        StockGroupsComboBox = new QComboBox(tabOverview);
        StockGroupsComboBox->setObjectName(QStringLiteral("StockGroupsComboBox"));
        StockGroupsComboBox->setGeometry(QRect(200, 10, 141, 31));
        UpdateButton = new QPushButton(tabOverview);
        UpdateButton->setObjectName(QStringLiteral("UpdateButton"));
        UpdateButton->setGeometry(QRect(800, 10, 91, 31));
        UpdateProgressBar = new QProgressBar(tabOverview);
        UpdateProgressBar->setObjectName(QStringLiteral("UpdateProgressBar"));
        UpdateProgressBar->setGeometry(QRect(360, 10, 181, 31));
        UpdateProgressBar->setValue(0);
        SymbolLabel = new QLabel(tabOverview);
        SymbolLabel->setObjectName(QStringLiteral("SymbolLabel"));
        SymbolLabel->setGeometry(QRect(20, 50, 60, 31));
        SymbolLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        OpenLabel = new QLabel(tabOverview);
        OpenLabel->setObjectName(QStringLiteral("OpenLabel"));
        OpenLabel->setGeometry(QRect(90, 50, 60, 31));
        OpenLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        HightLabel = new QLabel(tabOverview);
        HightLabel->setObjectName(QStringLiteral("HightLabel"));
        HightLabel->setGeometry(QRect(160, 50, 60, 31));
        HightLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        LowLabel = new QLabel(tabOverview);
        LowLabel->setObjectName(QStringLiteral("LowLabel"));
        LowLabel->setGeometry(QRect(230, 50, 60, 31));
        LowLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        CloseLabel = new QLabel(tabOverview);
        CloseLabel->setObjectName(QStringLiteral("CloseLabel"));
        CloseLabel->setGeometry(QRect(300, 50, 60, 31));
        CloseLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        VolumeLabel = new QLabel(tabOverview);
        VolumeLabel->setObjectName(QStringLiteral("VolumeLabel"));
        VolumeLabel->setGeometry(QRect(510, 50, 60, 31));
        VolumeLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        ChangeCLabel = new QLabel(tabOverview);
        ChangeCLabel->setObjectName(QStringLiteral("ChangeCLabel"));
        ChangeCLabel->setGeometry(QRect(370, 50, 60, 31));
        ChangeCLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        ChangeVLabel = new QLabel(tabOverview);
        ChangeVLabel->setObjectName(QStringLiteral("ChangeVLabel"));
        ChangeVLabel->setGeometry(QRect(580, 50, 60, 31));
        ChangeVLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        AvgC3MLabel = new QLabel(tabOverview);
        AvgC3MLabel->setObjectName(QStringLiteral("AvgC3MLabel"));
        AvgC3MLabel->setGeometry(QRect(440, 50, 60, 31));
        AvgC3MLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        AvgV3MLabel = new QLabel(tabOverview);
        AvgV3MLabel->setObjectName(QStringLiteral("AvgV3MLabel"));
        AvgV3MLabel->setGeometry(QRect(650, 50, 60, 31));
        AvgV3MLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        GraphSampleButton = new QPushButton(tabOverview);
        GraphSampleButton->setObjectName(QStringLiteral("GraphSampleButton"));
        GraphSampleButton->setEnabled(true);
        GraphSampleButton->setGeometry(QRect(840, 53, 51, 25));
        line = new QFrame(tabOverview);
        line->setObjectName(QStringLiteral("line"));
        line->setGeometry(QRect(30, 70, 791, 20));
        line->setFrameShape(QFrame::HLine);
        line->setFrameShadow(QFrame::Sunken);
        StrikePrice1YLabel = new QLabel(tabOverview);
        StrikePrice1YLabel->setObjectName(QStringLiteral("StrikePrice1YLabel"));
        StrikePrice1YLabel->setGeometry(QRect(700, 50, 120, 31));
        StrikePrice1YLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        Stockline = new QLineEdit(tabOverview);
        Stockline->setObjectName(QStringLiteral("Stockline"));
        Stockline->setGeometry(QRect(560, 10, 71, 31));
        AddButton = new QPushButton(tabOverview);
        AddButton->setObjectName(QStringLiteral("AddButton"));
        AddButton->setGeometry(QRect(650, 10, 71, 31));
        StockCheckBox = new QCheckBox(tabOverview);
        StockCheckBox->setObjectName(QStringLiteral("StockCheckBox"));
        StockCheckBox->setGeometry(QRect(15, 50, 80, 31));
        DelButton = new QPushButton(tabOverview);
        DelButton->setObjectName(QStringLiteral("DelButton"));
        DelButton->setGeometry(QRect(10, 10, 41, 31));
        OverviewScrollArea = new QScrollArea(tabOverview);
        OverviewScrollArea->setObjectName(QStringLiteral("OverviewScrollArea"));
        OverviewScrollArea->setGeometry(QRect(5, 90, 931, 341));
        OverviewScrollArea->setStyleSheet(QStringLiteral("background-color:rgb(240,240,240)"));
        OverviewScrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName(QStringLiteral("scrollAreaWidgetContents"));
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 929, 339));
        OverviewScrollArea->setWidget(scrollAreaWidgetContents);
        tabWidget->addTab(tabOverview, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QStringLiteral("tab_2"));
        tabWidget->addTab(tab_2, QString());
        AxisTradeCultForm->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(AxisTradeCultForm);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 968, 26));
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
        SymbolLabel->setText(QApplication::translate("AxisTradeCultForm", "Symbol", Q_NULLPTR));
        OpenLabel->setText(QApplication::translate("AxisTradeCultForm", "Open", Q_NULLPTR));
        HightLabel->setText(QApplication::translate("AxisTradeCultForm", "High", Q_NULLPTR));
        LowLabel->setText(QApplication::translate("AxisTradeCultForm", "Low", Q_NULLPTR));
        CloseLabel->setText(QApplication::translate("AxisTradeCultForm", "Close", Q_NULLPTR));
        VolumeLabel->setText(QApplication::translate("AxisTradeCultForm", "Volume", Q_NULLPTR));
        ChangeCLabel->setText(QApplication::translate("AxisTradeCultForm", "Change", Q_NULLPTR));
        ChangeVLabel->setText(QApplication::translate("AxisTradeCultForm", "Change", Q_NULLPTR));
        AvgC3MLabel->setText(QApplication::translate("AxisTradeCultForm", "Avg(3M)", Q_NULLPTR));
        AvgV3MLabel->setText(QApplication::translate("AxisTradeCultForm", "Avg(3M)", Q_NULLPTR));
        GraphSampleButton->setText(QApplication::translate("AxisTradeCultForm", "Graph", Q_NULLPTR));
        StrikePrice1YLabel->setText(QApplication::translate("AxisTradeCultForm", "Strike Price(1Y)", Q_NULLPTR));
        AddButton->setText(QApplication::translate("AxisTradeCultForm", "Add", Q_NULLPTR));
        StockCheckBox->setText(QString());
        DelButton->setText(QApplication::translate("AxisTradeCultForm", "Del", Q_NULLPTR));
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
