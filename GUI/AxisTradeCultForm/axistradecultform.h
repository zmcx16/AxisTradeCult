#ifndef AXISTRADECULTFORM_H
#define AXISTRADECULTFORM_H

#include <QMainWindow>

namespace Ui {
class AxisTradeCultForm;
}

class AxisTradeCultForm : public QMainWindow
{
    Q_OBJECT

public:
    explicit AxisTradeCultForm(QWidget *parent = 0);
    ~AxisTradeCultForm();

private:
    Ui::AxisTradeCultForm *ui;
};

#endif // AXISTRADECULTFORM_H
