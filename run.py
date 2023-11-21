import logging

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


from main import Ui_Main




class MainApplication(QMainWindow, Ui_Main):
    def __init__(self):
        super(MainApplication, self).__init__()
        self.setupUi(self)


def run_application():
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
