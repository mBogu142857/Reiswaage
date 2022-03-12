from marshmallow import Schema, fields, post_load, post_dump, pprint
import numpy as np
import matplotlib.pyplot as plt

import copy

class Measure:
    def __init__(self, bin_matrix: int = [], measValues: float = [], timestamp: str = [],
                 linRegRes: float = [], current_on_scale: int = 0, last_on_scale: int = 0,
                 B_out: int = [], sorted_binMtrx: int = [], T_out: int = [],
                 current_measurement: int = 0, measurements_idx: int = 0, color_tot_values=[],
                 color_evaluation_values=[], b_ternary: bool = False):

        self.measValues = measValues
        self.timestamp = timestamp
        self.linRegRes = linRegRes
        self.current_on_scale = current_on_scale  # holds current elements-on-scale status
        self.last_on_scale = last_on_scale

        self.bin_matrix = bin_matrix
        self.B_out = B_out
        self.sorted_binMtrx = sorted_binMtrx
        self.T_out = T_out
        self.current_measurement = current_measurement
        self.measurements_idx = measurements_idx  # index list of performed measurements
        self.color_tot_values = color_tot_values  # colors for plotting
        self.color_evaluation_values = color_evaluation_values  # colors for plotting
        self.b_ternary = b_ternary  # boolean for sequence basis selection: true for ternary, false for binary

        # n_el % number of elements
        # b_offs % boolean for offset status
        # est_prec % estimated precision (reading precision) of measuring device
        # binMatrix % array of binary rows indicating the relevant mass elements per measurement
        # currentonscale % holds current elements-on-scale status
        # lastonscale % holds previous elements-on-scale status
        # currMsrmt % index of current measurement
        # measurementsidx % index list of performed measurements
        # linRegRes % list of linear regression results after n measurements
        # Clr_totVal % colors for plotting
        # Clr_elVal % colors for plotting
        # b_ternary % boolean for sequence basis selection: true for ternary, false for binary

        # measValues % vector of measured values
        # timeStamp % time vector of recorded data

    def __repr__(self):
        return "<Measure measValues={self.measValues}, timeStamp={self.timeStamp}, linRegRes={self.linRegRes}, " \
               "lastonscle={self.lastonscle}, bin_matrix={self.bin_matrix}, B_out={self.B_out}, " \
               "sorted_binMtrx={self.sorted_binMtrx}, T_out={self.T_out}>".format(self=self)

    def clear(self):
        self.measValues: float = []
        self.timeStamp: float = []
        self.linRegRes: float = []
        self.lastonscle: int = []

        self.bin_matrix: int = []
        self.B_out: int = []
        self.sorted_binMtrx: int = []
        self.T_out: int = []

    def get_bin_matrix(self, k_strat, elem_list, settings):
        """

        :param k_strat:
        :param elem_list:
        :return: None
        """

        if k_strat < len(elem_list) and k_strat > 0:
            self.bin_matrix = self.get_bin_matrix_one_diff(settings.n_el)

            if k_strat < len(elem_list) - 2:
                k = k_strat
                self.bin_matrix = self.bin_matrix[(np.sum(self.bin_matrix, axis=1) == k) |
                                                  (np.sum(self.bin_matrix, axis=1) == 0), :]

                self.sorted_binMtrx = self.sort_bin_matrix_4_experiment(bin_matrix=self.bin_matrix, o_show=0)

        else:
            self.bin_matrix = self.create_ternary_matrix(settings.n_el)

        if settings.b_offs == 1:
            self.bin_matrix = np.column_stack((np.ones((np.size(self.bin_matrix, 0), 1)), self.bin_matrix))

        self.measValues = np.empty((np.size(self.bin_matrix, 0), 1))
        self.measValues[:] = np.NaN

        # self.timestamp = np.empty((np.size(self.bin_matrix, 0), 1))
        # self.timestamp[:] = np.NaN
        self.timestamp = ["" for i in range(np.size(self.bin_matrix, 0))]

        self.linRegRes = np.empty((np.size(self.bin_matrix, 1), len(self.measValues)))
        self.linRegRes[:] = np.NaN


        self.color_tot_values = 0.8 * np.array(plt.cm.hsv(np.size(self.measValues)))
        self.color_evaluation_values = 0.8 * np.array(plt.cm.hsv(np.size(self.bin_matrix, 1) + 1))
        self.last_on_scale = np.zeros((1, np.size(self.bin_matrix, 1)))

        #     function
        #     bM = getBinMatrix(app)
        #     k_strat = app.weighingstrategyDropDown.Value;
        #
        #     if k_strat < numel(app.weighingstrategyDropDown.ItemsData)
        #         bM = createBinMtrx_oneDiff(app.n_el); % % % external function
        #
        #         if k_strat < numel(app.weighingstrategyDropDown.ItemsData) - 2
        #             k = k_strat;
        #             bM = bM(sum(bM, 2) == k | sum(bM, 2) == 0,:);
        #             bM = sort_BinMtrx4Experiment(bM, 0); % % % external
        #             function
        #         end
        #
        #     else
        #         bM = createTernaryMtrx(app.n_el); % % % external function
        #     end
        #
        #     if app.b_offs == 1
        #         bM = [ones(size(bM, 1), 1) bM];
        #     end
        #
        #
        # end

    def get_bin_matrix_one_diff(self, n):
        """

        :param n:
        :return: B_out
        """

        oldB = np.zeros((1, n), dtype=bool)


        for kk in range(0, n):
            newB = np.flipud(copy.deepcopy(oldB))
            newB[:, kk] = ~newB[:, kk]
            oldB = np.row_stack((oldB, newB))

        B_out = oldB * 1
        return B_out

        # function
        # B_out = createBinMtrx_oneDiff(n)
        #
        # oldB = false(1, n);
        #
        # for kk = 1:n
        # newB = flipud(oldB);
        # newB(:, kk) = ~newB(:, kk);
        # oldB = [oldB;
        # newB];
        # end
        # B_out = oldB;

    def sort_bin_matrix_4_experiment(self, bin_matrix, o_show=0, b_rand=False):
        """

        :param bin_matrix:
        :param o_show:
        :param b_rand:
        :return: sorted_binMtrx
        """

        sz_binM = np.size(bin_matrix, 0)

        af_remRow = lambda M, n: np.delete(M, n, axis=0) ## QUI

        k = 0
        new_row = bin_matrix[k, :]
        bin_matrix = af_remRow(bin_matrix, k)

        """
        if o_show > 0:
            h_fig = figure(33)
            subplot(221)
            h_im1 = imagesc(sorted_binMtrx)
            subplot(222)
            h_im2 = imagesc(bin_matrix)
            subplot(313)
            h_pl1 = plot(1, nan)
        """

        sorted_binMtrx = np.zeros((0, np.size(new_row)))
        while sz_binM >= 1:
            sorted_binMtrx = np.row_stack((sorted_binMtrx, new_row))
            sel_crit = np.sum(np.abs(bin_matrix - sorted_binMtrx[-1, :]), axis=1)
            k = np.argmin(sel_crit)
            new_row = bin_matrix[k, :]
            if o_show > 1:
                diff_bin_matrix = bin_matrix
                diff_bin_matrix[k, :] = 3 * diff_bin_matrix[k, :]
                v_elMoved = np.sum(np.abs(np.diff(sorted_binMtrx, axis=0)), axis=1)

                """
                set(h_im1, 'CData', sorted_binMtrx)
                set(h_im2, 'CData', diff_bin_matrix)
                set(h_pl1, 'XData', 1 : length(v_elMoved), 'YData', v_elMoved)
                drawnow
                % pause(0.1)
                """

            bin_matrix = af_remRow(bin_matrix, k)
            sz_binM = np.size(bin_matrix, 0)

            if b_rand:
                bin_matrix = bin_matrix[np.random.perm(sz_binM), :]

        sorted_binMtrx = np.row_stack((sorted_binMtrx, new_row))

        if o_show > 0:
            v_elMoved = np.sum(np.abs(np.diff(sorted_binMtrx, axis=0)), axis=1)
            """
            set(h_im1, 'CData', sorted_binMtrx);
            set(h_im2, 'CData', bin_matrix);
            set(h_pl1, 'XData', 1: length(v_elMoved), 'YData', v_elMoved);
            """
        return sorted_binMtrx

    def create_ternary_matrix(self, n):
        """

        :param n:
        :return: T_out
        """

        T_old = np.zeros((3, 1))
        T_old[0] = -1
        T_old[-1] = 1

        for ii in range(1, n):
            T_new = np.row_stack((np.column_stack((-1*np.ones((np.size(T_old, 0), 1)), T_old)),
                                  np.column_stack((np.zeros((np.size(T_old, 0), 1)), T_old)),
                                  np.column_stack((np.ones((np.size(T_old, 0), 1)), T_old))))

            T_old = T_new

        return T_old

        # function
        # T_out = createTernaryMtrx(n)
        #
        # T_old = (-1:1)
        # ';
        # for ii = 1:n - 1
        # T_new = [-ones(size(T_old, 1), 1), T_old;
        # ...
        # zeros(size(T_old, 1), 1), T_old;
        # ...
        # ones(size(T_old, 1), 1), T_old];
        # T_old = T_new;
        #
        #
        # end
        # T_out = T_old;
        # end


class MeasureSchema(Schema):
    class Meta:
        ordered = True


    bin_matrix = fields.List(fields.Int(required=True))
    B_out = fields.List(fields.Int(required=True))
    sorted_binMtrx = fields.List(fields.Int(required=True))
    T_out = fields.List(fields.Int(required=True))


@post_load
def load_measure(self, data, **kwargs):
    return Measure(**data)


if __name__ == "__main__":
    daObject = Measure()
    schema = MeasureSchema()

    result = MeasureSchema().dumps(daObject)
    pprint(result)

    newObject = schema.loads(result)
    print(str(newObject))
