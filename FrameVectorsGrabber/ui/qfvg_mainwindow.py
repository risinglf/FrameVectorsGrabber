from PyQt4.QtGui import QMainWindow
from qfvg_mainwindow_ui import Ui_MainWindow

class QFVGMainWindow(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)