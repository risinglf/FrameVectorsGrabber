import sys
from PyQt4.QtGui import QApplication


if __name__ == "__main__":

    #Setup the UI
    app = QApplication(sys.argv)

    ui = QFVGWindow()
    ui.show()
    ui.raise_()

    sys.exit(app.exec_())
