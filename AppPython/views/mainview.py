from PySide2.QtWidgets import QCheckBox, QLineEdit, QComboBox, QApplication, QWidget, QPushButton, QVBoxLayout, \
    QGridLayout, QLabel, QListWidget, QHBoxLayout
from PySide2.QtCore import Qt
from PySide2 import QtGui, QtCore
import sys
from .matplotlibwidgetwithtoolbar import MplCanvas_trid
from .SliderWithTick import LabeledSlider


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setup_gui_settings()
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        #self.modify_layouts()
        #self.setup_connections()

    def clear(self):
        # self.totalelementsEditField.setReadOnly(False)
        self.totalelementsEditField.setReadOnly(False)
        self.totalelementsEditField.setEnabled(True)

        self.totalelementsEditField.setText("0")
        self.estimateddeviceprecisionEditField.setReadOnly(False)
        self.estimateddeviceprecisionEditField.setEnabled(True)

        self.estimateddeviceprecisionEditField.setText("0.1")
        self.measuredweightEditField.setReadOnly(True)
        self.measuredweightEditField.setEnabled(False)
        self.measuredweightEditField.setText("")
        self.measurementsdoneGauge.setEnabled(False)
        self.start_button.setEnabled(True)
        self.save_button.setEnabled(False)
        self.offsetelementCheckBox.setCheckable(True)
        self.offsetelementCheckBox.setCheckState(QtCore.Qt.Unchecked)

        self.listofmeasurementsListBox.clear()
        self.masselementsonscaleEditField.setText("")
        self.numberofelementsonscaleTextField.setText("")
        self.weighing_strategy_drop_down.setEnabled(True)

        # self.measurementsdoneGauge.maximum = 3
        # self.measurementsdoneGauge.labels = ["", "", "", ""]
        self.measurementsdoneGauge.minimum = 0
        self.measurementsdoneGauge.maximum = 5
        self.measurementsdoneGauge.labels = ["0", "1", "2", "3", "4", "5"]

        self.measurementsdoneGauge.sl.setValue(0)

    def setup_gui_settings(self):
        self.setMinimumSize(900, 500)
        icon = QtGui.QIcon("logo.png")

        self.setWindowIcon(icon)
        self.setWindowTitle("App")

    def create_widgets(self):
        self.totalelementsLabel = QLabel('total elements')
        self.totalelementsEditField = QLineEdit('0')
        self.offsetelementCheckBox = QCheckBox()
        self.offsetelementLabel = QLabel('offset element')
        self.reset_button = QPushButton("")
        self.icon_reset_button = QtGui.QIcon()
        self.reset_button.setIcon(QtGui.QIcon("reset.png"))

        self.estimateddeviceprecisionLabel = QLabel('estimated device precision')
        self.estimateddeviceprecisionEditField = QLineEdit('0.1')
        self.weighingstrategyLabel = QLabel('weighing strategy')
        self.weighing_strategy_drop_down = QComboBox()
        self.weighing_strategy_drop_down.addItems(["(nCH1)+1", "(nCH1)+2", "2^n", "3^n"])

        self.masselementLabel = QLabel('mass elements on scale')
        self.numberofelementsonscaleTextField = QLineEdit('0')
        self.masselementsonscaleEditField = QLineEdit('')

        self.removeelementsListBoxLabel = QLabel('remove element(s)')
        self.removeelementsListBoxLabel.setStyleSheet("color: red")

        self.addelementsListBoxLabel = QLabel('add elements(s)')
        self.addelementsListBoxLabel.setStyleSheet("color: green")

        self.removeelementsListBox = QListWidget()
        self.addelementsListBox = QListWidget()

        self.measuredweightLabel = QLabel('measured weight')

        self.start_button = QPushButton("Start")
        self.save_button = QPushButton("Save")
        self.measuredweightEditField = QLineEdit()
        self.listofmeasurementsListBox = QListWidget()
        self.measurementsdoneGauge = LabeledSlider(orientation=Qt.Vertical) # QSlider(Qt.Vertical)#SliderCustom(Qt.Vertical)
        self.plot = MplCanvas_trid()

    def modify_widgets(self):
        self.plot.ax1 = self.plot.add_subplot_bid(311)
        self.plot.ax2 = self.plot.add_subplot_bid(312)
        self.plot.ax3 = self.plot.add_subplot_bid(313)

    def create_layouts(self):
        self.layout = QGridLayout()  # GRID LAYOUT
        self.layout_2 = QHBoxLayout()
        self.layout_5 = QHBoxLayout()
        self.layout_6 = QHBoxLayout()
        self.layout_8 = QHBoxLayout()
        self.layout_3 = QVBoxLayout()
        self.layout_4 = QHBoxLayout()
        self.layout_7 = QVBoxLayout()

    def add_widgets_to_layouts(self):
        self.layout.addWidget(self.totalelementsLabel, 0, 0)  # Note the Row Column coordinates
        self.layout.addWidget(self.totalelementsEditField, 0, 1)  # Note the Row Column coordinates

        self.layout_2.addWidget(self.offsetelementCheckBox)
        self.layout_2.addWidget(self.offsetelementLabel)
        self.layout_2.addStretch()

        self.layout.addLayout(self.layout_2, 0, 2)
        self.layout.addWidget(self.reset_button, 0, 3)

        self.layout.addWidget(self.estimateddeviceprecisionLabel, 1, 0)  # Note the Row Column coordinates
        self.layout.addWidget(self.estimateddeviceprecisionEditField, 1, 1)  # Note the Row Column coordinates

        self.layout_5.addWidget(self.weighingstrategyLabel)  # Note the Row Column coordinates
        self.layout_5.addWidget(self.weighing_strategy_drop_down)
        self.layout.addLayout(self.layout_5, 1, 2, 1, 2)

        self.layout.addWidget(self.masselementLabel, 2, 0)  # Note the Row Column coordinates
        self.layout.addWidget(self.numberofelementsonscaleTextField, 2, 1)  # Note the Row Column coordinates
        self.layout.addWidget(self.masselementsonscaleEditField, 2, 2, 1, 2)  # Note the Row Column coordinates

        self.layout.addWidget(self.removeelementsListBoxLabel, 3, 0, 1, 2)
        self.layout.addWidget(self.addelementsListBoxLabel, 3, 2, 1, 2)

        self.layout.addWidget(self.removeelementsListBox, 4, 0, 2, 2)
        self.layout.addWidget(self.addelementsListBox, 4, 2, 2, 2)

        self.layout.addWidget(self.measuredweightLabel, 6, 2, 1, 2)
        self.listofmeasurementsListBox.setMaximumHeight(150)
        self.listofmeasurementsListBox.setMinimumWidth(600)

        self.layout_6.addWidget(self.start_button, 1)
        self.layout_6.addWidget(self.save_button, 1)
        self.layout_6.addWidget(self.measuredweightEditField, 1)

        self.layout_7.addLayout(self.layout_6)
        self.layout_7.addWidget(self.listofmeasurementsListBox)

        self.layout_8.addLayout(self.layout_7)
        self.layout_8.addWidget(self.measurementsdoneGauge)
        self.layout_8.addStretch()

        self.layout.addLayout(self.layout_8, 7, 0, 1, 3)

        self.layout_3.addWidget(self.plot)

        self.layout_4.addLayout(self.layout)
        self.layout_4.addLayout(self.layout_3)
        self.setLayout(self.layout_4)


if __name__ == "__main__":
    app = QApplication([])
    window = MainView()
    window.show()
    sys.exit(app.exec_())

