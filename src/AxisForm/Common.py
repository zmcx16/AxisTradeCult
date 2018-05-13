from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


def ClearAllWidgetInLayout(layout):
    for i in reversed(range(layout.count())):
        widgetToRemove = layout.itemAt(i).widget()
        layout.removeWidget(widgetToRemove)  # remove it from the layout list
        widgetToRemove.setParent(None)  # remove it from the gui


def ClearWidgetInLayoutByNames(layout, ObjectNames):
    for i in reversed(range(layout.count())):
        widgetToRemove = layout.itemAt(i).widget()
        if(widgetToRemove.objectName() in ObjectNames):
            layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)


def SetQLineEditColor(widget, r, g, b):
    SetColor = "color: rgb({0}, {1}, {2});".format(r, g, b)
    widget.setStyleSheet(SetColor)


def GetAllWidgetValInLayout(layout, TechIndicatorParam):
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if type(widget) == QLineEdit:
            TechIndicatorParam[widget.objectName()] = widget.text()
        elif type(widget) == QComboBox:
            TechIndicatorParam[widget.objectName()] = widget.currentText()


class ScrollableWindow(QMainWindow):

    def __init__(self, fig = None, parent = None):
        super(ScrollableWindow, self).__init__(parent)

        QMainWindow.__init__(self)
        self.setWindowTitle('Wanna join the Axis Cult?')
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QVBoxLayout())
        self.widget.layout().setContentsMargins(0, 0, 0, 0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        size = fig.get_size_inches() * fig.dpi
        self.resize(QSize(size[0] + 100, size[1] + 100))
