from sys import exit, argv
from os import environ
from PySide2.QtWidgets import QApplication
import warnings
from controllers import MainController

environ['QT_API'] = 'pyside2'


class App(QApplication):
    def __init__(self, sys_argv: list):
        super().__init__(sys_argv)
        self.main_ctrl = MainController()


def run_app(sys_argv: list):
    app = App(sys_argv)
    exit(app.exec_())


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    run_app(argv)
