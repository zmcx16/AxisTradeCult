import sys
from AxisForm.AxisTradeCultForm import AxisTradeCultForm
from PyQt5.QtWidgets import QMainWindow, QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AxisTradeCultForm()
    window.show()
    sys.exit(app.exec_())
