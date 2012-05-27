# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/qfvgwindow.ui'
#
# Created: Sun May 27 15:58:42 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 60, 62, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 60, 62, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.frame1GraphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.frame1GraphicsView.setGeometry(QtCore.QRect(20, 81, 256, 191))
        self.frame1GraphicsView.setObjectName(_fromUtf8("frame1GraphicsView"))
        self.frame2GraphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.frame2GraphicsView.setGeometry(QtCore.QRect(330, 80, 256, 192))
        self.frame2GraphicsView.setObjectName(_fromUtf8("frame2GraphicsView"))
        self.chooseFrame1PushButton = QtGui.QPushButton(self.centralwidget)
        self.chooseFrame1PushButton.setGeometry(QtCore.QRect(143, 280, 141, 32))
        self.chooseFrame1PushButton.setObjectName(_fromUtf8("chooseFrame1PushButton"))
        self.chooseFrame2PushButton = QtGui.QPushButton(self.centralwidget)
        self.chooseFrame2PushButton.setGeometry(QtCore.QRect(460, 280, 131, 32))
        self.chooseFrame2PushButton.setObjectName(_fromUtf8("chooseFrame2PushButton"))
        self.showLuminanceCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.showLuminanceCheckBox.setGeometry(QtCore.QRect(20, 350, 171, 20))
        self.showLuminanceCheckBox.setObjectName(_fromUtf8("showLuminanceCheckBox"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Frame #1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Frame #2", None, QtGui.QApplication.UnicodeUTF8))
        self.chooseFrame1PushButton.setText(QtGui.QApplication.translate("MainWindow", "Choose frame #1", None, QtGui.QApplication.UnicodeUTF8))
        self.chooseFrame2PushButton.setText(QtGui.QApplication.translate("MainWindow", "Choose frame #2", None, QtGui.QApplication.UnicodeUTF8))
        self.showLuminanceCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Show only luminance", None, QtGui.QApplication.UnicodeUTF8))

