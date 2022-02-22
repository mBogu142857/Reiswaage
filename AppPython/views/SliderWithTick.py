import sys
from PySide2 import QtWidgets
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QStyle, QStyleOptionSlider
from PySide2.QtCore import QRect, QPoint, Qt


class LabeledSlider(QtWidgets.QWidget):
    def __init__(self, minimum=0, maximum=1, interval=1, orientation=Qt.Horizontal,
            labels=None, parent=None):
        super(LabeledSlider, self).__init__(parent=parent)
        self.minimum = minimum
        self.maximum = maximum
        self.levels=range(minimum, maximum+interval, interval)
        self.labels = labels
        if self.labels is not None:
            if not isinstance(self.labels, (tuple, list)):
                raise Exception("<labels> is a list or tuple.")
            if len(self.labels) != len(self.levels):
                raise Exception("Size of <labels> doesn't match levels.")
            self.levels=list(zip(self.levels,labels))
        else:
            self.levels=list(zip(self.levels,map(str,self.levels)))

        if orientation==Qt.Horizontal:
            self.layout=QtWidgets.QVBoxLayout(self)
        elif orientation==Qt.Vertical:
            self.layout=QtWidgets.QHBoxLayout(self)
        else:
            raise Exception("<orientation> wrong.")

        # gives some space to print labels
        self.left_margin=10
        self.top_margin=10
        self.right_margin=10
        self.bottom_margin=10

        self.layout.setContentsMargins(self.left_margin,self.top_margin,
                self.right_margin,self.bottom_margin)

        self.sl=QtWidgets.QSlider(orientation, self)
        self.sl.setMinimum(minimum)
        self.sl.setMaximum(maximum)
        self.sl.setValue(minimum)
        if orientation==Qt.Horizontal:
            self.sl.setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.sl.setMinimumWidth(300) # just to make it easier to read
        else:
            self.sl.setTickPosition(QtWidgets.QSlider.TicksLeft)
            self.sl.setMinimumHeight(300) # just to make it easier to read
        self.sl.setTickInterval(interval)
        self.sl.setSingleStep(1)

        self.layout.addWidget(self.sl)

    def paintEvent(self, e):

        super(LabeledSlider, self).paintEvent(e)

        self.levels = range(self.minimum, self.maximum + 1, 1)

        if self.labels is not None:
            if not isinstance(self.labels, (tuple, list)):
                raise Exception("<labels> is a list or tuple.")
            if len(self.labels) != len(self.levels):
                raise Exception("Size of <labels> doesn't match levels.")
            self.levels = list(zip(self.levels, self.labels))
        else:
            self.levels = list(zip(self.levels, map(str, self.levels)))

        self.sl.setMinimum(self.minimum)
        self.sl.setMaximum(self.maximum)

        self.sl.setSingleStep(1)
        self.sl.setTickInterval(1)

        style=self.sl.style()
        painter=QPainter(self)
        st_slider=QStyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation=self.sl.orientation()

        length=style.pixelMetric(QStyle.PM_SliderLength, st_slider, self.sl)
        available=style.pixelMetric(QStyle.PM_SliderSpaceAvailable, st_slider, self.sl)

        for v, v_str in self.levels:

            # get the size of the label
            rect=painter.drawText(QRect(), Qt.TextDontPrint, v_str)

            if self.sl.orientation()==Qt.Horizontal:
                # I assume the offset is half the length of slider, therefore
                # + length//2
                x_loc=QStyle.sliderPositionFromValue(self.sl.minimum(),
                        self.sl.maximum(), v, available)+length//2

                # left bound of the text = center - half of text width + L_margin
                left=x_loc-rect.width()//2+self.left_margin
                bottom=self.rect().bottom()

                # enlarge margins if clipping
                if v==self.sl.minimum():
                    if left<=0:
                        self.left_margin=rect.width()//2-x_loc
                    if self.bottom_margin<=rect.height():
                        self.bottom_margin=rect.height()

                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

                if v==self.sl.maximum() and rect.width()//2>=self.right_margin:
                    self.right_margin=rect.width()//2
                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

            else:
                y_loc=QStyle.sliderPositionFromValue(self.sl.minimum(),
                        self.sl.maximum(), v, available, upsideDown=True)

                bottom=y_loc+length//2+rect.height()//2+self.top_margin-3
                # there is a 3 px offset that I can't attribute to any metric

                left=self.left_margin-rect.width()
                if left<=0:
                    self.left_margin=rect.width()+2
                    self.layout.setContentsMargins(self.left_margin,
                            self.top_margin, self.right_margin,
                            self.bottom_margin)

            pos=QPoint(left, bottom)
            painter.drawText(pos, v_str)

        return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    frame=QtWidgets.QWidget()
    ha=QtWidgets.QHBoxLayout()
    frame.setLayout(ha)

    w = LabeledSlider(1, 10 , 1, orientation=Qt.Vertical)
    w.minimum = 0
    w.maximum = 5
    w.labels = ["0", "1", "2", "3", "4"]


    ha.addWidget(w)
    frame.show()
    sys.exit(app.exec_())