from PyQt4.QtCore import Qt
from PyQt4.QtGui import *
from qfvg_mainwindow_ui import Ui_MainWindow
from images.image_converter import ImageConverter
from images.image_comparator import ImageComparator


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
        self.ui.findVectorsPushButton.clicked.connect(self._find_frame_vectors)

        self._load_sample_images_from_HD()

    def _load_sample_images_from_HD(self):
        self.image_1 = QImage("samples/images/car/car1.png")
        self._draw_frame(self.image_1, self.ui.frame1GraphicsView)

        self.image_2 = QImage("samples/images/car/car2.png")
        self._draw_frame(self.image_2, self.ui.frame2GraphicsView)



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
        if image:
            scene = QGraphicsScene()
            scene.addPixmap(QPixmap.fromImage(image))
            graphics_view.setScene(scene)

    def _show_frame_luminance(self):
        if self.ui.showLuminanceCheckBox.isChecked():
            #Show the image with only the luminance component
            self._draw_frame(self.get_image1_luminance(), self.ui.frame1GraphicsView)
            self._draw_frame(self.get_image2_luminance(), self.ui.frame2GraphicsView)

        else:
            #Show the original coloured frame
            self._draw_frame(self.image_1, self.ui.frame1GraphicsView)
            self._draw_frame(self.image_2, self.ui.frame2GraphicsView)

    def get_image1_luminance(self):
        if self.image_1:
            if not self.image_1_luminance:
                self.image_1_luminance = ImageConverter.luminance_qimage(self.image_1)
            return self.image_1_luminance
        else:
            return None

    def get_image2_luminance(self):
        if self.image_2:
            if not self.image_2_luminance:
                self.image_2_luminance = ImageConverter.luminance_qimage(self.image_2)
            return self.image_2_luminance
        else:
            return None


    def _find_frame_vectors(self):
        if self.get_image1_luminance() and self.get_image2_luminance():
            comp = ImageComparator(self.image_1_luminance)

            vectors = comp.get_motion_vectors(self.image_2_luminance, 8)
            self._draw_motion_vectors(vectors)

    def _draw_motion_vectors(self, vectors):
        scene = self.ui.frame2GraphicsView.scene()

        pen = QPen(Qt.red, 2, Qt.SolidLine)

        for v in vectors:
            x = int(v["x"])
            y = int(v["y"])
            to_x = int(v["to_x"])
            to_y = int(v["to_y"])

            print "(%d, %d) => (%d, %d)" % (x,y, to_x, to_y)

            if scene:
                scene.addLine(x,y,to_x, to_y, pen)


