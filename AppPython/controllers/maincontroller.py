from PySide2.QtCore import QObject
from views import MainView
from PySide2 import QtCore
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

import time
from model.back_engine import BackEngine

import copy
from scipy.special import comb

class MainController(QObject):
    def __init__(self):
        super().__init__()

        # Initialization
        self.back_engine = BackEngine()

        # Initialisation of the view
        self.main_view = MainView()

        # Start-up function
        self.startup_function()

        # Make visible the GUI
        self.main_view.show()

        # Create a link between controller and signals
        self.connect_controller_slots_to_signals()

    def connect_controller_slots_to_signals(self):

        # Buttons
        self.main_view.totalelementsEditField.returnPressed.connect(self.totalelementsEditFieldValueChanged)
        self.main_view.reset_button.clicked.connect(self.reset_button_pushed)
        self.main_view.measuredweightEditField.returnPressed.connect(self.measured_weight_edit_field_value_changed)
        self.main_view.measuredweightEditField.textChanged[str].connect(self.measured_weight_edit_field_value_changing)

        self.main_view.weighing_strategy_drop_down.activated.connect(self.weighing_strategy_drop_down_value_changed)
        self.main_view.start_button.clicked.connect(self.start_button_pushed)
        self.main_view.save_button.clicked.connect(self.save_button_pushed)
        
    def startup_function(self):
        self.main_view.totalelementsEditField.setReadOnly(False)
        self.main_view.totalelementsEditField.setText("0")

        self.main_view.estimateddeviceprecisionEditField.setReadOnly(False)
        self.main_view.estimateddeviceprecisionEditField.setText("0.1")

        self.main_view.measuredweightEditField.setReadOnly(False)
        self.main_view.measuredweightEditField.setText("")

        self.main_view.measurementsdoneGauge.setEnabled(False)
        #self.main_view.measurementsdoneGauge.Limits = [0 100];

        self.main_view.start_button.setEnabled(True)
        self.main_view.save_button.setEnabled(False)

        self.main_view.offsetelementCheckBox.setCheckable(True)
        self.main_view.offsetelementCheckBox.setCheckState(QtCore.Qt.Unchecked)

        self.main_view.listofmeasurementsListBox.clear()
        self.main_view.masselementsonscaleEditField.setText("")
        self.main_view.numberofelementsonscaleTextField.setText("")
        self.main_view.weighing_strategy_drop_down.setEnabled(True)

    def start_button_pushed(self):
        self.main_view.totalelementsEditField.setEnabled(False)
        self.main_view.estimateddeviceprecisionEditField.setEnabled(False)
        self.main_view.measuredweightEditField.setEnabled(True)
        self.main_view.measurementsdoneGauge.setEnabled(True)
        #self.main_view.measurementsdoneGauge.setText("0") ## QUI
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
        self.back_engine.measure.k_strat = self.main_view.weighing_strategy_drop_down.currentIndex()+1
        self.back_engine.measure.elem_list = [self.main_view.weighing_strategy_drop_down.itemText(i) for i
                                              in range(self.main_view.weighing_strategy_drop_down.count())]
        self.back_engine.set_settings_param(n_el, b_offs, est_prec)
        self.back_engine.measure.get_bin_matrix(self.back_engine.measure.k_strat,
                                                self.back_engine.measure.elem_list,
                                                self.back_engine.settings)

        ## Need to modify the widget file a bit to make this working, to add a setLimits function or to check if it exists already
        #self.main_view.measurementsdoneGauge.setLimits([0, np.size(self.back_engine.measure.bin_matrix)[0]])

        ListItems = []
        for ind in range(0, len(self.back_engine.measure.bin_matrix)):
            ListItems.append(str(ind) + ': ' + str(self.back_engine.measure.bin_matrix[ind, :]))

        self.main_view.listofmeasurementsListBox.clear()
        self.main_view.listofmeasurementsListBox.addItems(ListItems)

        ## Not sure of the difference between addItemsData and addItems
        # self.main_view.listofmeasurementsListBox.addItems(
        #     list(np.linspace(1, np.size(self.back_engine.measure.bin_matrix, 0),
        #                      np.size(self.back_engine.measure.bin_matrix, 0))))

        self.main_view.listofmeasurementsListBox.setCurrentRow(0)

        self.perform_measurement

        """ started to convert the code but still a bit to do
        # plot preparation
        #self.main_view.plot.ax3.scatter(np.NaN, 1, 16, 'filled')
        # hold(app.UIAxes1, 'on');
        self.main_view.plot.ax1([0, np.size(self.back_engine.measure.bin_matrix, 0) + 1],
                                       [1, 1] * self.back_engine.settings.est_prec / 2, 'r:',
                                       [0, np.size(self.back_engine.measure.bin_matrix, 0) + 1],
                                       [1, 1] * (-self.back_engine.settings.est_prec / 2), 'r:')
        # hold(app.UIAxes1, 'off');
        self.main_view.plot.ax1.title(("%g " + np.NaN(1, np.size(self.back_engine.measure.bin_matrix, 1))))
        self.main_view.plot.ax1.xlabel("# measurement")
        self.main_view.plot.ax1.ylabel("residuals")
        self.main_view.plot.ax1.xlim([0, np.size(self.back_engine.measure.bin_matrix, 0) + 1])
        # box(app.UIAxes1, 'on');

        # plot(app.UIAxes2, nan, ones(size(app.bin_matrix, 2), 1), '-'); ## QUI
        self.main_view.plot.ax2.xlabel("# measurement")
        self.main_view.plot.ax2.title("element value difference to initial value")
        self.main_view.plot.ax2.ylabel("m - m_0")
        self.main_view.plot.ax1.xlim([0, np.size(self.back_engine.measure.bin_matrix, 0) + 1])
        # box(app.UIAxes2, 'on');

        self.main_view.plot.ax3.scatter(np.NaN, 1, 12, 'filled', 'MarkerFaceAlpha', .5)
        # hold(app.UIAxes3, 'on');
        self.main_view.plot.ax3.plot(np.NaN, 1, '.', 'MarkerSize', 24)
        self.main_view.plot.ax3.plot([np.NaN, np.NaN], [1, 1] * self.back_engine.settings.est_prec / 2, 'r:',
                                            [np.NaN, np.NaN], [1, 1] * (-self.back_engine.settings.est_prec / 2), 'r:')
        # hold(app.UIAxes3, 'off');
        self.main_view.plot.ax3.xlabel("measurement value")
        self.main_view.plot.ax3.ylabel("residuals")
        # box(app.UIAxes3, 'on');
    """

        # % Button  pushed function: StartButton
        # function  StartButtonPushed(app, event)
        #         app.totalelementsEditField.Editable = false;
        #         app.estimateddeviceprecisionEditField.Editable = false;
        #         app.measuredweightEditField.Editable = true;
        #         app.measurementsdoneGauge.Enable = true;
        #         app.measurementsdoneGauge.Value = 0;
        #         app.StartButton.Enable = false;
        #         app.SaveButton.Enable = true;
        #         app.offsetelementCheckBox.Enable = false;
        #         app.weighingstrategyDropDown.Enable = false;
        #
        #         app.n_el = app.totalelementsEditField.Value;
        #         app.b_offs = app.offsetelementCheckBox.Value;
        #         app.est_prec = app.estimateddeviceprecisionEditField.Value;
        #
        #         app.binMatrix = app.getBinMatrix();
        #         app.measValues = nan(size(app.binMatrix, 1), 1);
        #         app.timeStamp = nan(size(app.binMatrix, 1), 1);
        #         app.linRegRes = nan(size(app.binMatrix, 2), numel(app.measValues));
        #
        #         app.measurementsdoneGauge.Limits = [0 size(app.binMatrix, 1)];
        #
        # % app.listofmeasurementsListBox.Items = mat2cell(num2str(app.binMatrix), ones(1, size(app.binMatrix, 1)));
        # app.listofmeasurementsListBox.Items = cellfun(@ (n, s) sprintf('%1i: %s', n, s), num2cell((1:size(app.binMatrix, 1))'), ...
        # mat2cell(num2str(app.binMatrix), ones(1, size(app.binMatrix, 1))), 'UniformOutput', false);
        # app.listofmeasurementsListBox.ItemsData = 1:size(app.binMatrix, 1);
        # app.listofmeasurementsListBox.Value = app.listofmeasurementsListBox.ItemsData(1);
        # app.lastonscale = zeros(1, size(app.binMatrix, 2));
        #
        # app.Clr_totVal = .8 * hsv(numel(app.measValues));
        # app.Clr_elVal = .8 * hsv(size(app.binMatrix, 2) + 1);
        #
        # app.performMeasurement;
        #
        # % % % plot
        # preparation
        # scatter(app.UIAxes1, nan, 1, 16, 'filled');
        # hold(app.UIAxes1, 'on');
        # plot(app.UIAxes1, [0 size(app.binMatrix, 1) + 1], [1 1] * app.est_prec / 2, 'r:', [0 size(app.binMatrix, 1) + 1],
        #      [1 1] * (-app.est_prec / 2), 'r:');
        # hold(app.UIAxes1, 'off');
        # title(app.UIAxes1, sprintf('%g ', nan(1, size(app.binMatrix, 2))));
        # xlabel(app.UIAxes1, '# measurement');
        # ylabel(app.UIAxes1, 'residuals');
        # set(app.UIAxes1, 'XLim', [0 size(app.binMatrix, 1) + 1]);
        # box(app.UIAxes1, 'on');
        #
        # plot(app.UIAxes2, nan, ones(size(app.binMatrix, 2), 1), '-');
        # xlabel(app.UIAxes2, '# measurement');
        # title(app.UIAxes2, 'element value difference to initial value');
        # ylabel(app.UIAxes2, 'm - m_0')
        # set(app.UIAxes2, 'XLim', [0 size(app.binMatrix, 1) + 1]);
        # box(app.UIAxes2, 'on');
        #
        # scatter(app.UIAxes3, nan, 1, 12, 'filled', 'MarkerFaceAlpha', .5);
        # hold(app.UIAxes3, 'on');
        # plot(app.UIAxes3, nan, 1, '.', 'MarkerSize', 24);
        # plot(app.UIAxes3, [nan nan], [1 1] * app.est_prec / 2, 'r:', [nan nan], [1 1] * (-app.est_prec / 2), 'r:');
        # hold(app.UIAxes3, 'off');
        # xlabel(app.UIAxes3, 'measurement value');
        # ylabel(app.UIAxes3, 'residuals');
        # box(app.UIAxes3, 'on');
        #
        # end

    def measured_weight_edit_field_value_changed(self):

        self.back_engine.measure.measValues[self.back_engine.measure.currMsrmt] = \
            float(self.main_view.measuredweightEditField.Value)

        # % Value
        # changed
        # function: measuredweightEditField
        # function
        # EnterButtonPushed(app, event)
        # app.measValues(app.currMsrmt) = str2double(app.measuredweightEditField.Value);
        # app.timeStamp(app.currMsrmt) = now;
        # app.lastonscale = app.currentonscale;
        # if sum(isnan(app.measValues)) == 0
        # uialert(app.UIFigure,
        #         'All measurements were performed. Change data for currently selected measurement or click Save button for data export.',
        #         'Measurements done', 'Icon', 'success');
        # else
        # if app.listofmeasurementsListBox.Value == numel(app.listofmeasurementsListBox.ItemsData) | | ...
        # ~isnan(app.measValues(app.listofmeasurementsListBox.Value + 1))
        # app.listofmeasurementsListBox.Value = find(isnan(app.measValues), 1);
        # else
        # app.listofmeasurementsListBox.Value = app.listofmeasurementsListBox.Value + 1;
        # end
        # end
        #
        # app.measurementsdoneGauge.Value = sum(~isnan(app.measValues));
        # app.listofmeasurementsListBox.scroll(app.listofmeasurementsListBox.Value);
        #
        # app.measurementsidx =[app.measurementsidx app.measurementsdoneGauge.Value];
        #
        # app.performMeasurement;
        # app.plotCurrentResults;
        # end

    def list_of_measurements_value_changed(self):
        self.back_engine.compute_measure()

    def save_button_pushed(self):
        """
        Callback of the save button
        :return: None
        """

        # To check if it actually works
        output_matrix = [self.back_engine.settings.timeStamp,
                         self.back_engine.measure.binMatrix,
                         self.back_engine.measure.measValues]
        file = filedialog.asksaveasfile(filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv")))
        file.write(output_matrix)
        file.close()

        #     [file, path] = uiputfile({'*.xlsx'; '*.csv'}, 'Save file');
        #     writematrix([app.timeStamp, app.binMatrix, app.measValues], fullfile(path, file));
        # end

    def reset_button_pushed(self):
        """
        Callback of the reset button
        :return: None
        """
        self.main_view.plot.ax1.clear()
        self.main_view.plot.ax2.clear()
        self.main_view.plot.ax2.clear()
        self.startup_function

    def totalelementsEditFieldValueChanged(self):
        """
        :return: None
        """
        n = int(self.main_view.totalelementsEditField.text())

        nCHk_ItmData = np.linspace(1, n + 1, n + 1)
        nCHk_List = []
        for i in range(0, len(nCHk_ItmData)-2):
            k_in = nCHk_ItmData[i]
            nCHk_List.append("N = (%1iCH%1i)+1 = %1i" % (n, k_in, comb(n, k_in + 1, exact=True) + 1))

        nCHk_List.append("N = 2^%1i = %1i" % (n, 2 ^ n))
        nCHk_List.append("N = 3^%1i = %1i" % (n, 3 ^ n))

        self.main_view.weighing_strategy_drop_down.clear()
        for ind in range(0, len(nCHk_ItmData)):
            self.main_view.weighing_strategy_drop_down.addItem(nCHk_List[ind], nCHk_ItmData[ind])



        # n = app.totalelementsEditField.Value;
        # nCHk_ItmData = num2cell(1:n+1);
        # nCHk_List = cell(1,n+1);
        # nCHk_List(1:end-2) = cellfun(@(k_in) sprintf('N = (%1iCH%1i)+1 = %1i', n, k_in, nchoosek(n, k_in)+1), nCHk_ItmData(1:end-2), 'UniformOutput',false);
        # nCHk_List{end-1} = sprintf('N = 2^%1i = %1i', n, 2^n);
        # nCHk_List{end} = sprintf('N = 3^%1i = %1i', n, 3^n);
        # app.weighingstrategyDropDown.Items = nCHk_List;
        # app.weighingstrategyDropDown.ItemsData = nCHk_ItmData;

    def measured_weight_edit_field_value_changing(self):
        """

        :return:
        """
        changing_value = int(self.main_view.measuredweightEditField.text())
        print(changing_value)
        # % Value
        # changing
        # function: measuredweightEditField
        # function
        # measuredweightEditFieldValueChanging(app, event)
        # changingValue = event.Value;
        # end

    def weighing_strategy_drop_down_value_changed(self):
        value = self.main_view.weighing_strategy_drop_down.currentIndex()

        if (value == self.main_view.weighing_strategy_drop_down.itemData(int(self.main_view.totalelementsEditField.text()))):
            self.b_ternary = True
            self.main_view.removeelementsListBoxLabel.setText("negative element(s)")
            self.main_view.addelementsListBoxLabel.setText("positive element(s)")

        else:
            self.b_ternary = False
            self.main_view.removeelementsListBoxLabel.setText("remove element(s)")
            self.main_view.addelementsListBoxLabel.setText("add element(s)")

        # % Value
        # changed
        # function: weighingstrategyDropDown
        # function
        # weighingstrategyDropDownValueChanged(app, event)
        # value = app.weighingstrategyDropDown.Value;
        # if value == app.weighingstrategyDropDown.ItemsData
        # {end}
        # app.b_ternary = true;
        # app.removeelementsListBoxLabel.Text = 'negative element(s)';
        # app.addelementsListBoxLabel.Text = 'positive element(s)';
        # else
        # app.b_ternary = false;
        # app.removeelementsListBoxLabel.Text = 'remove element(s)';
        # app.addelementsListBoxLabel.Text = 'add element(s)';
        # end
        #
        # end
        # end

    def perform_measurement(self):
        print("Here")
        self.back_engine.measure.currMsrmt = self.main_view.listofmeasurementsListBox.Value

        if len(self.back_engine.measure.currMsrmt) >= 0:
            self.main_view.measuredweightEditField.Value("")

        else:
            self.main_view.measuredweightEditField.setText((self.back_engine.measure.measValues(
                self.back_engine.measure.currMsrmt) + "%11.4g"))

        self.back_engine.measure.currentonscale = self.back_engine.measure.bin_matrix[
                                                  self.back_engine.measure.currMsrmt, :]

        if self.back_engine.measure.b_ternary:
            list_toAdd = np.where(self.back_engine.measure.currentonscale == 1)[0] - \
                         self.back_engine.measure.b_offs.T

            list_toRemove = np.where(self.back_engine.measure.currentonscale == -1)[0] - \
                            self.back_engine.measure.b_offs.T

            self.main_view.masselementsonscaleEditField.setText(
                "%s | %s" % (-(np.where(self.back_engine.measure.lastonscale == -1) -
                               self.back_engine.measure.b_offs.T),
                             -(np.where(self.back_engine.measure.lastonscale == 1) -
                               self.back_engine.measure.b_offs.T)))

            self.main_view.numberofelementsonscaleTextField.setText(
                "%1i | %1i" % (np.sum(self.back_engine.measure.lastonscale < 0),
                                     np.sum(self.back_engine.measure.lastonscale > 0)))

        else:
            self.main_view.masselementsonscaleEditField.Value = str(np.where(self.back_engine.measure.lastonscale) -
                                                                    self.back_engine.measure.b_offs)

            self.main_view.numberofelementsonscaleTextField.Value = str(sum(self.back_engine.measure.lastonscale))

            list_toAdd = np.where((self.back_engine.measure.currentonscale -
                                   self.back_engine.measure.lastonscale) == 1) - \
                         self.back_engine.measure.b_offs.T

            list_toRemove = np.where((self.back_engine.measure.currentonscale -
                                      self.back_engine.measure.lastonscale) == -1) - \
                            self.back_engine.measure.b_offs.T

        if len(list_toAdd) >= 0:
            self.main_view.addelementsListBox.clear()
            self.main_view.addelementsListBox.addItems([""])

        else:
            self.main_view.addelementsListBox.Items = list(str(list_toAdd),
                                                           np.ones((1, np.size(list_toAdd)[0])))
    #
        if len(list_toRemove) >= 0:
            self.main_view.removeelementsListBox.Items = {}

        else:
            self.main_view.removeelementsListBox.Items = list(str(list_toRemove),
                                                              np.ones((1, np.size(list_toRemove)[0])))

        # function
        # performMeasurement(app)
        # app.currMsrmt = app.listofmeasurementsListBox.Value;
        #
        # if isnan(app.measValues(app.currMsrmt))
        #     app.measuredweightEditField.Value = '';
        # else
        #     app.measuredweightEditField.Value = num2str(app.measValues(app.currMsrmt), '%11.4g');
        # end
        #
        # app.currentonscale = app.binMatrix(app.currMsrmt,:);
        #
        # if app.b_ternary
        #     list_toAdd = find(app.currentonscale == 1) - app.b_offs
        #     ';
        #     list_toRemove = find(app.currentonscale == -1) - app.b_offs
        #     ';
        #
        #     app.masselementsonscaleEditField.Value = ...
        #     sprintf('%s | %s', ...
        #     num2str(-(find(app.lastonscale == -1) - app.b_offs')), ...
        #     num2str(-(find(app.lastonscale == 1) - app.b_offs
        #     ')));
        #     app.numberofelementsonscaleTextField.Value = sprintf('%1i | %1i', sum(app.lastonscale < 0),
        #                                                          sum(app.lastonscale > 0));
        #
        #     else
        #     app.masselementsonscaleEditField.Value = num2str(find(app.lastonscale) - app.b_offs);
        #     app.numberofelementsonscaleTextField.Value = num2str(sum(app.lastonscale));
        #
        #     list_toAdd = find((app.currentonscale - app.lastonscale) == 1) - app.b_offs
        #     ';
        #     list_toRemove = find((app.currentonscale - app.lastonscale) == -1) - app.b_offs
        #     ';
        #     end
        #
        #     if isempty(list_toAdd)
        #     app.addelementsListBox.Items = {};
        #     else
        #     app.addelementsListBox.Items = mat2cell(num2str(list_toAdd), ones(1, size(list_toAdd, 1)));
        #     end
        #
        #     if isempty(list_toRemove)
        #     app.removeelementsListBox.Items = {};
        #     else
        #     app.removeelementsListBox.Items = mat2cell(num2str(list_toRemove), ones(1, size(list_toRemove, 1)));
        #     end
        #
        #     end