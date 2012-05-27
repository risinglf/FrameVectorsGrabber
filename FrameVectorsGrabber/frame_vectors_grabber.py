import sys
from PyQt4.QtGui import QApplication
from ui.qfvg_mainwindow import QFVGMainWindow


if __name__ == "__main__":

    #Setup the UI
    app = QApplication(sys.argv)

    ui = QFVGMainWindow()
    ui.show()
    ui.raise_()

    sys.exit(app.exec_())
