from PySide2.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PySide2.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as Toolbar


class MplCanvas(Canvas):
    def __init__(self, parent: QWidget = None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        Canvas.__init__(self, self.fig)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class MplWidget(QWidget):
    """ Customized Matplotlib widget used as promoted widget in QT designer"""

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas()  # Create canvas object

        self.vbl = QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
       # self.addToolbar = Toolbar(self.canvas, self)  # add toolbar to plot
       # self.vbl.addWidget(self.addToolbar)
       # self.vbl.setAlignment(self.addToolbar, Qt.AlignCenter)

        self.setLayout(self.vbl)


class MplWidget2(QWidget):
    """ Customized Matplotlib widget used as promoted widget in QT designer"""

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas()  # Create canvas object

        self.vbl = QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.addToolbar = Toolbar(self.canvas, self)  # add toolbar to plot
        self.vbl.addWidget(self.addToolbar)
        self.vbl.setAlignment(self.addToolbar, Qt.AlignCenter)

        self.setLayout(self.vbl)