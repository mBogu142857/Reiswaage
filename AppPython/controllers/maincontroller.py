from PySide2.QtCore import QObject
from views import MainView
from PySide2 import QtCore
from tkinter import filedialog
import numpy as np
from time import strftime
from tkinter import messagebox as mbox
from tkinter import Tk
import matplotlib.pyplot as plt
import matplotlib.colors as col
import copy
import time

from scipy.special import comb

from model.back_engine import BackEngine


class MainController(QObject):
    def __init__(self):
        super().__init__()

        # Initialization
        self.back_engine = BackEngine()

        # Initialisation of the view
        self.main_view = MainView()

        # Start-up function
        self.main_view.clear()

        # Make visible the GUI
        self.main_view.show()

        # Create a link between controller and signals
        self.connect_controller_slots_to_signals()

    def connect_controller_slots_to_signals(self):

        # Buttons
        self.main_view.totalelementsEditField.editingFinished.connect(self.totalelementsEditFieldValueChanged)
        self.main_view.reset_button.clicked.connect(self.reset_button_pushed)

        self.main_view.measuredweightEditField.returnPressed.connect(self.measured_weight_edit_field_value_changed)
        self.main_view.measuredweightEditField.textChanged[str].connect(self.measured_weight_edit_field_value_changing)

        self.main_view.weighing_strategy_drop_down.activated.connect(self.weighing_strategy_drop_down_value_changed)
        self.main_view.start_button.clicked.connect(self.start_button_pushed)
        self.main_view.save_button.clicked.connect(self.save_button_pushed)
        self.main_view.listofmeasurementsListBox.itemSelectionChanged.connect(self.list_of_measurements_value_changed)

    def start_button_pushed(self):
        self.main_view.totalelementsEditField.setEnabled(False)
        self.main_view.estimateddeviceprecisionEditField.setEnabled(False)
        self.main_view.measuredweightEditField.setEnabled(True)
        self.main_view.measuredweightEditField.setReadOnly(False)
        self.main_view.measurementsdoneGauge.setEnabled(True)

        self.main_view.start_button.setEnabled(False)
        self.main_view.save_button.setEnabled(True)
        self.main_view.offsetelementCheckBox.setEnabled(False)
        self.main_view.weighing_strategy_drop_down.setEnabled(False)

        n_el = int(self.main_view.totalelementsEditField.text())
        if self.main_view.offsetelementCheckBox.checkState() == 0:
            b_offs = 0

        else:
            b_offs = 1

        est_prec = float(self.main_view.estimateddeviceprecisionEditField.text())
        self.back_engine.measure.k_strat = self.main_view.weighing_strategy_drop_down.currentIndex() + 1

        self.back_engine.measure.elem_list = [self.main_view.weighing_strategy_drop_down.itemText(i) for i
                                              in range(self.main_view.weighing_strategy_drop_down.count())]

        self.back_engine.set_settings_param(n_el, b_offs, est_prec)

        self.back_engine.measure.get_bin_matrix(self.back_engine.measure.k_strat,
                                                self.back_engine.measure.elem_list,
                                                self.back_engine.settings)

        ListItems = []
        for ind in range(0, len(self.back_engine.measure.bin_matrix)):
            ListItems.append(str(ind) + ': ' + str(self.back_engine.measure.bin_matrix[ind, :]))

        self.main_view.listofmeasurementsListBox.clear()
        self.main_view.listofmeasurementsListBox.addItems(ListItems)

        self.main_view.measurementsdoneGauge.maximum = int(len(ListItems))
        self.main_view.measurementsdoneGauge.labels = [str(x) for x in range(0, int(len(ListItems)) + 1)]
        self.main_view.measurementsdoneGauge.sl.setValue(0)

        self.main_view.listofmeasurementsListBox.setCurrentRow(0)

        self.perform_measurement

        # plot preparation
        self.main_view.plotAx1_content.XData = [0, np.size(self.back_engine.measure.bin_matrix, 0) + 1]
        self.main_view.plotAx1_content.YData = np.array([1, 1]) * self.back_engine.settings.est_prec / 2
        self.main_view.plotAx1_content.XLim = [0, np.size(self.back_engine.measure.bin_matrix, 0) + 1]

        self.main_view.plotAx1.canvas.ax.plot(self.main_view.plotAx1_content.XData,
                                              self.main_view.plotAx1_content.YData, 'r:',
                                              self.main_view.plotAx1_content.XData,
                                              -self.main_view.plotAx1_content.YData, 'r:')

        title_content = np.empty((1, np.size(self.back_engine.measure.bin_matrix, 1)))
        title_content[:] = np.NaN
        self.main_view.plotAx1.canvas.ax.set_xlabel("# measurement")
        self.main_view.plotAx1.canvas.ax.set_ylabel("residuals")
        self.main_view.plotAx1.canvas.ax.set_xlim(self.main_view.plotAx1_content.XLim)
        self.main_view.plotAx1.canvas.draw()

        self.main_view.plotAx2_content.XData = np.NaN * np.ones((np.size(self.back_engine.measure.bin_matrix, 1), 1))
        self.main_view.plotAx2_content.YData = np.ones((np.size(self.back_engine.measure.bin_matrix, 1), 1))
        self.main_view.plotAx2_content.XLim = [0, np.size(self.back_engine.measure.bin_matrix, 0) + 1]

        self.main_view.plotAx2.canvas.ax.plot(self.main_view.plotAx2_content.XData,
                                              self.main_view.plotAx2_content.YData, 'r-')

        self.main_view.plotAx2.canvas.ax.set_xlabel("# measurement")
        self.main_view.plotAx2.canvas.ax.set_title("element value difference to initial value")
        self.main_view.plotAx2.canvas.ax.set_ylabel("m - m_0")
        self.main_view.plotAx2.canvas.ax.set_xlim(self.main_view.plotAx2_content.XLim)
        self.main_view.plotAx2.canvas.draw()

        self.main_view.plotAx3.canvas.ax.clear()
        self.main_view.plotAx3_content.XData = np.NaN
        self.main_view.plotAx3_content.YData = 1
        self.main_view.plotAx4_1_content.XLim = [-1, 1]
        self.main_view.plotAx4_1_content.YLim = [-1, 1]
        self.main_view.plotAx4_2_content.XLim = [-1, 1]
        self.main_view.plotAx4_2_content.YLim = [-1, 1]

        self.main_view.plotAx3_2_content.XData = np.array([np.NaN, np.NaN])
        self.main_view.plotAx3_2_content.YData = np.array([1, 1]) * self.back_engine.settings.est_prec / 2

        self.main_view.plotAx3.canvas.ax.scatter(self.main_view.plotAx3_content.XData,
                                                 self.main_view.plotAx3_content.YData,
                                                 s=12, alpha=.5)

        self.main_view.plotAx3.canvas.ax.scatter(np.NaN, 1, s=24)

        self.main_view.plotAx4_1_content.XData = np.NaN * np.ones((np.size(self.back_engine.measure.bin_matrix, 1), 1))
        self.main_view.plotAx4_1_content.YData = self.back_engine.settings.est_prec / 2

        self.main_view.plotAx4_2_content.XData = np.NaN * np.ones((np.size(self.back_engine.measure.bin_matrix, 1), 1))
        self.main_view.plotAx4_2_content.YData = -self.back_engine.settings.est_prec / 2

        self.main_view.plotAx3.canvas.ax.plot(self.main_view.plotAx3_2_content.XData,
                                              self.main_view.plotAx3_2_content.YData, 'r:',
                                              self.main_view.plotAx3_2_content.XData,
                                              -self.main_view.plotAx3_2_content.YData, 'r:')

        self.main_view.plotAx3.canvas.ax.set_xlabel("measurement value")
        self.main_view.plotAx3.canvas.ax.set_ylabel("residuals")
        self.main_view.plotAx3.canvas.draw()

    def measured_weight_edit_field_value_changed(self):
        """
        Callback for the modification to the edit file measured_weight:
        - update of the selection of the listbox with instructions
        - update of the measure
        - update of the slider (measurement Gauge)
        - update of the graphs
        :return: None
        """
        try:
            float(self.main_view.measuredweightEditField.text())

        except:
            return

        self.back_engine.measure.measValues[self.back_engine.measure.current_measurement] = \
            float(self.main_view.measuredweightEditField.text())

        self.back_engine.measure.timestamp[self.back_engine.measure.current_measurement] = strftime("%T")
        self.back_engine.measure.last_on_scale = self.back_engine.measure.current_on_scale

        if np.sum(np.isnan(self.back_engine.measure.measValues)) == 0:
            root = Tk()
            root.withdraw()
            mbox.showinfo('Measurements done', 'All measurements were performed. Change data for currently selected'
                                               ' measurement or click Save button for data export.')
            root.update()
        else:
            lw = self.main_view.listofmeasurementsListBox
            items = []
            for x in range(lw.count() - 1):
                items.append(lw.item(x))

            if self.main_view.listofmeasurementsListBox.selectedIndexes()[0].row() == np.size(items) \
                    or ~np.isnan(self.back_engine.measure.measValues[
                                     self.main_view.listofmeasurementsListBox.selectedIndexes()[0].row() + 1]):

                self.main_view.listofmeasurementsListBox.setCurrentRow(
                    np.where(np.isnan(self.back_engine.measure.measValues) == 1)[0][0])

            else:
                self.main_view.listofmeasurementsListBox.setCurrentRow(
                    self.main_view.listofmeasurementsListBox.selectedIndexes()[0].row() + 1)

        self.list_of_measurements_value_changed()
        self.back_engine.measure.measurements_idx = np.column_stack((self.back_engine.measure.measurements_idx,
                                                                     np.sum(~np.isnan(
                                                                         self.back_engine.measure.measValues))))

        self.perform_measurement()
        self.plot_current_results()

    def plot_current_results(self):
        perfMeas = np.ones(np.size(self.back_engine.measure.measValues, 0))
        perfMeas = np.multiply(perfMeas.T, (~np.isnan(self.back_engine.measure.measValues)).T)[0]

        lm = np.sum(~np.isnan(self.back_engine.measure.measValues)) - 1

        this_bin_matrix = self.back_engine.measure.bin_matrix[np.where(perfMeas > 0)[0], :]
        this_meas_data = self.back_engine.measure.measValues[np.where(perfMeas > 0)[0]]

        # Left matrix division
        this_linRegRes, resid, rank, s = np.linalg.lstsq(this_bin_matrix, this_meas_data)
        self.back_engine.measure.linRegRes[:, [lm]] = this_linRegRes

        result_Matrix = np.matmul(this_bin_matrix, this_linRegRes)  # this_bin_matrix * this_linRegRes
        Delta_totMass = (this_meas_data - result_Matrix)

        lw = self.main_view.listofmeasurementsListBox
        items = []
        for x in range(lw.count()):
            items.append(x)

        items = np.array(items) + 1

        self.main_view.plotAx1.canvas.ax.clear()
        self.main_view.plotAx1_content.XData = [0, np.size(self.back_engine.measure.bin_matrix, 0) + 1]
        self.main_view.plotAx1_content.YData = np.array([1, 1]) * self.back_engine.settings.est_prec / 2
        self.main_view.plotAx1_content.XLim = [0, np.size(self.back_engine.measure.bin_matrix, 0) + 1]

        self.main_view.plotAx1.canvas.ax.plot(self.main_view.plotAx1_content.XData,
                                              self.main_view.plotAx1_content.YData, 'r:',
                                              self.main_view.plotAx1_content.XData,
                                              -self.main_view.plotAx1_content.YData, 'r:')

        self.main_view.plotAx1_content.XData = items[np.where(perfMeas > 0)]
        self.main_view.plotAx1_content.YData = Delta_totMass
        if np.size(self.main_view.plotAx1_content.XData) > 0 and np.size(self.main_view.plotAx1_content.YData) > 0:
            self.main_view.plotAx1_content.CData = np.column_stack((np.multiply(abs(Delta_totMass) >
                                                                                self.back_engine.settings.est_prec / 2,
                                                                                1)[0],
                                                                    np.zeros((np.size(Delta_totMass, 1), 2))))

            self.main_view.plotAx1.canvas.ax.scatter(self.main_view.plotAx1_content.XData,
                                                     self.main_view.plotAx1_content.YData,
                                                     c=self.main_view.plotAx1_content.CData)

            self.main_view.plotAx1.canvas.ax.set_xlabel("# measurement")
            self.main_view.plotAx1.canvas.ax.set_ylabel("residuals")
            # self.main_view.plotAx1.canvas.ax.set_title(("| %2.3g |" % this_linRegRes))
            self.main_view.plotAx1.canvas.draw()

            self.main_view.plotAx2.canvas.ax.clear()
            self.main_view.plotAx2.canvas.ax.set_xlabel("# measurement")
            self.main_view.plotAx2.canvas.ax.set_title("element value difference to initial value")
            self.main_view.plotAx2.canvas.ax.set_ylabel("m - m_0")

            self.main_view.plotAx2_content.Color = np.zeros((np.size(self.back_engine.measure.bin_matrix, 0), 3))
            for jj in range(0, np.size(self.back_engine.measure.bin_matrix, 1)):
                if lm == 1:
                    self.main_view.plotAx2_content.Color[jj, :] = self.back_engine.measure.color_evaluation_values[jj,
                                                                  1:]

                self.main_view.plotAx2_content.XData = np.row_stack((self.main_view.plotAx2_content.XData, lm))
                self.main_view.plotAx2_content.YData = np.row_stack((self.main_view.plotAx2_content.YData,
                                                                     self.back_engine.measure.linRegRes[jj, lm] - \
                                                                     self.back_engine.measure.linRegRes[jj, 0]))

            self.main_view.plotAx2.canvas.ax.plot(self.main_view.plotAx2_content.XData,
                                                  self.main_view.plotAx2_content.YData)
            self.main_view.plotAx2.canvas.draw()

            self.main_view.plotAx3.canvas.ax.clear()
            self.main_view.plotAx3.canvas.ax.set_xlabel("measurement value")
            self.main_view.plotAx3.canvas.ax.set_ylabel("residuals")
            self.main_view.plotAx3.canvas.ax.set_title("Residual vs total mass")

            self.main_view.plotAx3_content.XData = [0, np.size(self.back_engine.measure.bin_matrix, 0) + 1]
            self.main_view.plotAx3_content.YData = np.array([1, 1]) * self.back_engine.settings.est_prec / 2
            self.main_view.plotAx3.canvas.ax.plot(self.main_view.plotAx3_content.XData,
                                                  self.main_view.plotAx3_content.YData, 'r:',
                                                  self.main_view.plotAx3_content.XData,
                                                  -self.main_view.plotAx3_content.YData, 'r:')

            self.main_view.plotAx3_content.XData = this_meas_data
            self.main_view.plotAx3_content.YData = Delta_totMass
            self.main_view.plotAx3_content.CData = (self.back_engine.measure.color_tot_values[np.where(perfMeas > 0)][
                0])[1:]

            self.main_view.plotAx3_2_content.XData = this_meas_data[-1]
            self.main_view.plotAx3_2_content.YData = Delta_totMass[-1]
            self.main_view.plotAx3_2_content.CData = self.back_engine.measure.color_tot_values[lm, 1:]

            if ~(self.main_view.plotAx4_1_content.XData == self.main_view.plotAx3_content.XLim):
                self.main_view.plotAx4_1_content.XData = self.main_view.plotAx3_content.XLim
                self.main_view.plotAx4_2_content.XData = self.main_view.plotAx3_content.XLim

            self.main_view.plotAx3.canvas.ax.scatter(self.main_view.plotAx3_content.XData,
                                                     self.main_view.plotAx3_content.YData,
                                                     c=col.hsv_to_rgb(self.main_view.plotAx3_content.CData))

            self.main_view.plotAx3.canvas.ax.scatter(self.main_view.plotAx3_2_content.XData,
                                                     self.main_view.plotAx3_2_content.YData,
                                                     c=col.hsv_to_rgb(self.main_view.plotAx3_2_content.CData))

            # self.main_view.plotAx3.canvas.ax.plot(self.main_view.plotAx4_1_content.XData,
            #                                       self.main_view.plotAx4_1_content.YData)
            #
            # self.main_view.plotAx3.canvas.ax.plot(self.main_view.plotAx4_2_content.XData,
            #                                       self.main_view.plotAx4_2_content.YData)
            self.main_view.plotAx3.canvas.ax.set_xlim([0, 1])
            self.main_view.plotAx3.canvas.draw()

    def list_of_measurements_value_changed(self):
        # self.back_engine.compute_measure()

        self.main_view.measurementsdoneGauge.sl.setValue(np.sum(~np.isnan(self.back_engine.measure.measValues)))

        self.back_engine.measure.measurements_idx = np.column_stack((self.back_engine.measure.measurements_idx,
                                                                     np.sum(~np.isnan(
                                                                         self.back_engine.measure.measValues))))
        self.perform_measurement()
        self.plot_current_results()

    def save_button_pushed(self):
        """
        Callback of the save button
        :return: None
        """

        output_matrix = np.column_stack((self.back_engine.measure.timestamp, self.back_engine.measure.bin_matrix,
                                         self.back_engine.measure.measValues))

        file = filedialog.asksaveasfile(mode='w', defaultextension=".csv")

        if file:
            file.write(str(output_matrix))
            file.close()

    def reset_button_pushed(self):
        """
        Callback of the reset button
        :return: None
        """
        self.main_view.clear()
        self.back_engine.clear()

    def totalelementsEditFieldValueChanged(self):
        """
        :return: None
        """
        n = int(self.main_view.totalelementsEditField.text())

        nCHk_ItmData = np.linspace(1, n + 1, n + 1)
        nCHk_List = []
        for i in range(0, len(nCHk_ItmData) - 2):
            k_in = nCHk_ItmData[i]
            nCHk_List.append("N = (%1iCH%1i)+1 = %1i" % (n, k_in, comb(n, k_in, exact=True) + 1))

        nCHk_List.append("N = 2^%1i = %1i" % (n, np.power(2, n)))
        nCHk_List.append("N = 3^%1i = %1i" % (n, np.power(3, n)))

        self.main_view.weighing_strategy_drop_down.clear()
        for ind in range(0, len(nCHk_ItmData)):
            self.main_view.weighing_strategy_drop_down.addItem(nCHk_List[ind], nCHk_ItmData[ind])

    def measured_weight_edit_field_value_changing(self):
        """

        :return:
        """
        pass

    def weighing_strategy_drop_down_value_changed(self):
        value = self.main_view.weighing_strategy_drop_down.currentIndex()

        if (value == int(self.main_view.totalelementsEditField.text())):
            self.back_engine.measure.b_ternary = True
            self.main_view.removeelementsListBoxLabel.setText("negative element(s)")
            self.main_view.addelementsListBoxLabel.setText("positive element(s)")

        else:
            self.back_engine.measure.b_ternary = False
            self.main_view.removeelementsListBoxLabel.setText("remove element(s)")
            self.main_view.addelementsListBoxLabel.setText("add element(s)")

    def perform_measurement(self):
        if len(self.main_view.listofmeasurementsListBox.selectedIndexes()) > 0:
            self.back_engine.measure.current_measurement = self.main_view.listofmeasurementsListBox.selectedIndexes()[
                0].row()

            if np.isnan(self.back_engine.measure.measValues[self.back_engine.measure.current_measurement - 1]):
                self.main_view.measuredweightEditField.setText("")

            else:
                self.main_view.measuredweightEditField.setText((str(self.back_engine.measure.measValues[
                                                                        self.back_engine.measure.current_measurement - 1][
                                                                        0])))  # + "%11.4g"

            self.back_engine.measure.current_on_scale = self.back_engine.measure.bin_matrix[
                                                        self.back_engine.measure.current_measurement - 1, :]

            if self.back_engine.measure.b_ternary:
                list_toAdd = np.where(self.back_engine.measure.current_on_scale == 1)[0] + 1 - \
                             self.back_engine.settings.b_offs

                list_toRemove = np.where(self.back_engine.measure.current_on_scale == -1)[0] + 1 - \
                                self.back_engine.settings.b_offs

                self.main_view.masselementsonscaleEditField.setText(
                    "%s | %s" % ((np.where(self.back_engine.measure.last_on_scale == -1)[0] -
                                  self.back_engine.settings.b_offs) + 1,
                                 (np.where(self.back_engine.measure.last_on_scale == 1)[0] -
                                  self.back_engine.settings.b_offs) + 1))

                self.main_view.numberofelementsonscaleTextField.setText(
                    "%1i | %1i" % (np.sum(self.back_engine.measure.last_on_scale < 0),
                                   np.sum(self.back_engine.measure.last_on_scale > 0)))

            else:

                self.main_view.masselementsonscaleEditField.setText(
                    str(np.where(~(self.back_engine.measure.last_on_scale == np.NaN))[0] \
                        + 1 - self.back_engine.settings.b_offs))

                self.main_view.numberofelementsonscaleTextField.setText(
                    "%1i" % (np.sum(self.back_engine.measure.last_on_scale) - \
                             self.back_engine.settings.b_offs))

                list_toAdd = np.where((self.back_engine.measure.current_on_scale -
                                       self.back_engine.measure.last_on_scale) == 1)[0] + 1 - \
                             self.back_engine.settings.b_offs

                list_toRemove = np.where((self.back_engine.measure.current_on_scale -
                                          self.back_engine.measure.last_on_scale) == -1)[0] + 1 - \
                                self.back_engine.settings.b_offs

            if len(list_toAdd) > 0:
                self.main_view.addelementsListBox.clear()
                self.main_view.addelementsListBox.addItems(list_toAdd.astype(str))

            else:
                self.main_view.addelementsListBox.clear()

            if len(list_toRemove) > 0:
                self.main_view.removeelementsListBox.clear()

                self.main_view.removeelementsListBox.addItems(list_toRemove.astype(str))

            else:
                self.main_view.removeelementsListBox.clear()
