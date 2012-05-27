from PyQt4.QtGui import QMainWindow, QFileDialog, QImage, QGraphicsScene, QPainter, QPixmap
from qfvg_mainwindow_ui import Ui_MainWindow
from images.image_converter import ImageConverter


class QFVGMainWindow(QMainWindow):


    def __init__(self):

        self.image_1 = None
        self.image_1_luminance = None

        self.image_2 = None
        self.image_2_luminance = None

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Event handling
        self.ui.chooseFrame1PushButton.clicked.connect(self._choose_frame1)
        self.ui.chooseFrame2PushButton.clicked.connect(self._choose_frame2)
        self.ui.showLuminanceCheckBox.clicked.connect(self._show_frame_luminance)


    def _choose_frame1(self):
        self.image_1 = None
        self.image_1_luminance = None

        filename = QFileDialog.getOpenFileName(self, "Choose Image", "~", "Image Files (*.png *.jpg *.bmp)")
        self.image_1 = QImage(filename)

        if self.image_1:
            self._draw_frame(self.image_1, self.ui.frame1GraphicsView)

    def _choose_frame2(self):
        self.image_2 = None
        self.image_2_luminance = None

        filename = QFileDialog.getOpenFileName(self, "Choose Image", "~", "Image Files (*.png *.jpg *.bmp)")
        self.image_2 = QImage(filename)

        if self.image_2:
            self._draw_frame(self.image_2, self.ui.frame2GraphicsView)


    def _draw_frame(self, image, graphics_view):
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(image))
        graphics_view.setScene(scene)

    def _show_frame_luminance(self):
        if self.ui.showLuminanceCheckBox.isChecked():

            #Convert the image to the luminance image and show

            if self.image_1:
                if not self.image_1_luminance:
                    self.image_1_luminance = ImageConverter.luminance_qimage(self.image_1)
                self._draw_frame(self.image_1_luminance, self.ui.frame1GraphicsView)

            if self.image_2:
                if not self.image_2_luminance:
                    self.image_2_luminance = ImageConverter.luminance_qimage(self.image_2)
                self._draw_frame(self.image_2_luminance, self.ui.frame2GraphicsView)

        else:
            #Show the original coloured frame
            if self.image_1:
                self._draw_frame(self.image_1, self.ui.frame1GraphicsView)

            if self.image_2:
                self._draw_frame(self.image_2, self.ui.frame2GraphicsView)


