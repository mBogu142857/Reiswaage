import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

#Example from https://stackoverflow.com/questions/54244990/is-it-possible-to-expand-the-drawable-area-around-the-qslider
# https://www.sliderrevolution.com/resources/css-range-slider/
slider_x = 150
slider_y = 200

slider_step = [0, "", "", "", "", 0.5, "", "", "", "", 1, "", "", "", "", 1.5, "", "", "", "", 2, "", "", "", "", 2.5, "", "", "", "", 3]
slider_step_2 = [0,  0.5,  1,  1.5,  2,  2.5,  3]

groove_y = 150
handle_height = 10


class SliderCustom(QSlider):
    def __init__(self, type, parent=None):
        super().__init__()
        self.parent = parent
        self.Type = type
        self.setStyleSheet("""
            QSlider::handle:vertical {
                border:5px solid rgba(255,255,255,0);
                border-right-color:#888;
                left:-31px;
            }
            QSlider::groove:vertical {
                 border: 0px solid black;
                 height: """ + str(groove_y) + """ px;
                 border-radius: 2px;
            }
        """)


    def paintEvent(self, event):
        super(SliderCustom, self).paintEvent(event)
        qp = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(Qt.black)

        qp.setPen(pen)
        font = QFont('Times', 10)
        qp.setFont(font)
        self.setContentsMargins(50, 50, 50, 50)
        self.setFixedSize(QSize(slider_x, slider_y))
        contents = self.contentsRect()
        max = self.maximum()
        min = self.minimum()

        self.Type = "step_size"
        self.setMaximum(len(slider_step))
        self.setMinimum(1)
        self.setSingleStep(1)
        self.setTickInterval(1)

        y_inc = slider_y - (slider_y - groove_y) / 2
        for i in range(len(slider_step)):
            if slider_step[i] != "":
                qp.drawText(contents.x() + 7 * font.pointSize(), y_inc + font.pointSize() / 2, '{0:3}'.format(slider_step[i]))
                qp.drawLine(contents.x() + 2 * font.pointSize(), y_inc, contents.x() + contents.width(), y_inc)
                y_inc -= groove_y / (max - min)
            else:
                qp.drawText(contents.x() + 7 * font.pointSize(), y_inc + font.pointSize() / 2, '{0:3}'.format(slider_step[i]))
                qp.drawLine(contents.x() + 2 * font.pointSize(), y_inc, contents.x() + contents.width()-15, y_inc)
                y_inc -= groove_y / (max - min)


class Window(QWidget):
    """ Inherits from QWidget """
    def __init__(self):
        super().__init__()
        self.title = 'Control Stages'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.AxesMapping = [0, 1, 2, 3]
        self.initUI()

    def initUI(self):
        """ Initializes the GUI either using the grid layout or the absolute position layout"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        Comp4 = SliderCustom(Qt.Vertical)
        layout = QHBoxLayout()
        layout.addWidget(Comp4)
        #layout.addStretch()
        self.setLayout(layout)
        self.show()

    @staticmethod
    def sliderChanged(Slider):
        print("Slider value changed to ", Slider.value(), "slider type is ", Slider.Type)
        if Slider.Type == "step_size":
            print("this is a step size slider")
        elif Slider.Type == "speed":
            print("this is a speed slider")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())