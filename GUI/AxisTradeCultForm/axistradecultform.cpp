#include "axistradecultform.h"
#include "ui_axistradecultform.h"

AxisTradeCultForm::AxisTradeCultForm(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::AxisTradeCultForm)
{
    ui->setupUi(this);
}

AxisTradeCultForm::~AxisTradeCultForm()
{
    delete ui;
}
