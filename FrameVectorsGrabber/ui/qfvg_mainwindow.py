from PyQt4.QtCore import Qt
from PyQt4.QtGui import *
from qfvg_mainwindow_ui import Ui_MainWindow
from images.image_converter import ImageConverter
from images.image_comparator import ImageComparator
from utils.logging import klog


class QFVGMainWindow(QMainWindow):


    def __init__(self):

        self.image_1 = None
        self.image_1_luminance = None

        self.image_2 = None
        self.image_2_luminance = None

        self.vectors = []

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Event handling
        self.ui.chooseFrame1PushButton.clicked.connect(self._choose_frame1)
        self.ui.chooseFrame2PushButton.clicked.connect(self._choose_frame2)
        self.ui.showLuminanceCheckBox.clicked.connect(self._show_frame_luminance)
        self.ui.findVectorsPushButton.clicked.connect(self._find_frame_vectors)
        self.ui.reconstructFrame2PushButton.clicked.connect(self._drawCompressedFrame2)

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

            self.vectors = comp.get_motion_vectors(self.image_2_luminance, self.get_block_size(), self.get_search_window_size())
            self._draw_motion_vectors()

    def _draw_motion_vectors(self):
        scene = self.ui.frame2GraphicsView.scene()

        pen = QPen(Qt.red, 1, Qt.SolidLine)

        for v in self.vectors:
            x = int(v["x"])
            y = int(v["y"])
            to_x = int(v["to_x"])
            to_y = int(v["to_y"])
            MAD = v["MAD"]

            klog( "(%d, %d) => (%d, %d)" % (x,y, to_x, to_y) )

            if scene:
                if MAD < self.ui.MADThresholdSpingBox.value() and (x != to_x or y == to_y):
                    scene.addLine(x,y,to_x, to_y, pen)

        self._drawCompressedFrame2()


    def _drawCompressedFrame2(self):
        if len(self.vectors) > 0:

            zero_vectors_blocks_count = 0
            new_blocks_count = 0
            moved_vectors_blocks_count = 0

            self._draw_frame(self.image_2, self.ui.frame2CompressedGraphicsView)

            scene = self.ui.frame2CompressedGraphicsView.scene()
            image2_new = QImage(self.image_2)

            sameBlockPen = QPen(Qt.black, 1, Qt.SolidLine)
            movedBlockPen = QPen(Qt.green, 1, Qt.SolidLine)


            for v in self.vectors:
                x = int(v["x"])
                y = int(v["y"])
                to_x = int(v["to_x"])
                to_y = int(v["to_y"])
                MAD = v["MAD"]

                if x == to_x and y == to_y:
                    #The block is the same of the previous frame. Transmit a zero vector
                    zero_vectors_blocks_count += 1
                    scene.addRect(x, y, self.get_block_size(), self.get_block_size(), sameBlockPen, QBrush(Qt.SolidPattern))
                else:
                    if MAD < self.ui.MADThresholdSpingBox.value():
                        #The block is moved
                        moved_vectors_blocks_count += 1

                        scene.addRect(x, y, self.get_block_size(), self.get_block_size(), movedBlockPen, QBrush(Qt.green, Qt.SolidPattern))

                        moved_block_image = self.image_2.copy(x,y, self.get_block_size(), self.get_block_size())
                        ImageConverter.draw_image_into_image(moved_block_image, image2_new, to_x, to_y)
                    else:
                        #A new block of the frame is needed
                        new_blocks_count += 1

            #Draw the reconstructed Frame
            scene = QGraphicsScene()
            scene.addPixmap(QPixmap.fromImage(image2_new))
            self.ui.frame2ReconstructedGraphicsView.setScene(scene)

            #Show the statistics
            zero_vectors_blocks_percent = (zero_vectors_blocks_count*100/len(self.vectors))
            new_blocks_percent = (new_blocks_count*100/len(self.vectors))
            moved_vectors_blocks_percent = (moved_vectors_blocks_count*100/len(self.vectors))

            compression_ratio = 100 - new_blocks_percent - moved_vectors_blocks_percent/3

            self.ui.zeroVectorsPercentLabel.setText("%d %%" %zero_vectors_blocks_percent )
            self.ui.newBlocksPercentLabel.setText("%d %%" % new_blocks_percent)
            self.ui.movedVectorsPercentLabel.setText("%d %%" % moved_vectors_blocks_percent)
            self.ui.compressionRatioLabel.setText("%d %%" %compression_ratio)


    def get_block_size(self):
        return self.ui.blockSizeSpinBox.value()

    def get_search_window_size(self):
        return self.ui.searchWindowSizeSpinBox.value()

    def _drawReconstructedFrame2(self):
        pass