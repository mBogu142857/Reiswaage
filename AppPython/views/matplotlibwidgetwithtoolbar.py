from PySide2.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PySide2.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as Toolbar
from matplotlib.widgets import Slider
import functools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MplCanvas(Canvas):
    def __init__(self, parent: QWidget = None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        Canvas.__init__(self, self.fig)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def add_interactive_note(self, ax, line, str, fig, str_event='button_press_event'):
        return NoteBuilder(ax, line, str, fig, str_event)

    def add_slider(self, ax_link1, ax_link2, label, valmin, valmax, orientation):
        self.slider = Slider(ax=ax_link1, label=label, valmin=valmin, valmax=valmax, orientation=orientation, valinit=4000)
        # self.slider.on_changed(functools.partial(self.set_axis, ax_link2))
        return self.slider

    def set_axis(self, ax, val):
        # print(self.slider.val)
        # self.axes1.set(xlim=(0, 100), ylim=(0, self.slider.val))
        ax.set(ylim=(0, self.slider.val))

class MplWidget_custom(QWidget):
    """ Customized Matplotlib widget used as promoted widget in QT designer"""

    def __init__(self, parent: QWidget = None, width=5, height=4, dpi=65):
        QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas_custom(self, width, height, dpi)  # Create canvas object

        self.vbl = QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
       # self.addToolbar = Toolbar(self.canvas, self)  # add toolbar to plot
       # self.vbl.addWidget(self.addToolbar)
       # self.vbl.setAlignment(self.addToolbar, Qt.AlignCenter)

        self.setLayout(self.vbl)

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

class MplWidgetWithToolBar(QWidget):

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

class MplCanvas_trid(Canvas):
    def __init__(self, parent=None, width=8, height=4, dpi=65):
        self.fig = plt.figure(tight_layout=True, figsize=(width, height), dpi=dpi)
        self.fig.tight_layout()
        # super(MplCanvas_custom, self).__init__(self.fig)
        Canvas.__init__(self, self.fig)

        self.setParent(parent)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def add_subplot(self, num, type):
        return self.fig.add_subplot(num, projection='3d')

    def add_subplot_bid(self, num):
        return self.fig.add_subplot(num)

class MplCanvas_custom(Canvas):

    def __init__(self, parent=None, width=5, height=4, dpi=65):
        self.fig = Figure(tight_layout=True, figsize=(width, height), dpi=dpi)
        self.fig.tight_layout()
        # super(MplCanvas_custom, self).__init__(self.fig)
        Canvas.__init__(self, self.fig)

        self.setParent(parent)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def add_axes_x(self, x, y, xx, yy, ax_link=None):
        return self.fig.add_axes([x, y, xx, yy], sharex=ax_link)

    def add_axes_y(self, x, y, xx, yy, ax_link=None):
        return self.fig.add_axes([x, y, xx, yy], sharey=ax_link)

    def add_interactive_note(self, ax, line, str, fig, str_event = 'button_press_event'):
        return NoteBuilder(ax, line, str, fig, str_event)

    def add_slider(self, ax_link1, ax_link2, label, valmin, valmax, orientation):
        self.slider = Slider(ax=ax_link1, label=label, valmin=valmin, valmax=valmax, orientation=orientation, valinit=4000)
        #self.slider.on_changed(functools.partial(self.set_axis, ax_link2))
        return self.slider

    def set_axis(self, ax, val):
        #print(self.slider.val)
        # self.axes1.set(xlim=(0, 100), ylim=(0, self.slider.val))
        ax.set(ylim=(0, self.slider.val))

class MplWidgetWithToolBar_custom(QWidget):
    """ Customized Matplotlib widget used as promoted widget in QT designer"""

    def __init__(self, parent: QWidget = None, width=5, height=4, dpi=65):
        QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas_custom(self, width, height, dpi)  # Create canvas object

        self.vbl = QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.addToolbar = Toolbar(self.canvas, self)  # add toolbar to plot
        self.vbl.addWidget(self.addToolbar)
        self.vbl.setAlignment(self.addToolbar, Qt.AlignCenter)

        self.setLayout(self.vbl)

class NoteBuilder:
    def __init__(self, ax, line, str, fig, str_event = 'button_press_event'):

        self.fig = fig
        self.ax = ax
        self.line = line
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w", ec="w"),
                            arrowprops=dict(arrowstyle='wedge', fc="k", ec="k"))

        self.annot.set_visible(False)
        self.str = str
        # self.cid = line.figure.canvas.mpl_connect('motion_notify_event', self.annotate)

        self.cid = line.figure.canvas.mpl_connect(str_event, self.annotate)

    def update_line(self, line):
        self.line = line

    def change_annot(self, str):
        self.str = str
        # self.annot.set_visible(False)

    def update_annot(self, x, y, ind):
            self.annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])

            if type(self.str) == list:
                text = self.str[ind["ind"][0]]
                self.annot.set_text(text)

            else:
                self.annot.set_text(self.str)

            self.annot.get_bbox_patch().set_alpha(0.4)

    def annotate(self, event):
        if event.inaxes == self.ax:
            cont, ind = self.line.contains(event)

            if cont:
                x, y = self.line.get_data()
                self.update_annot(x, y, ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()