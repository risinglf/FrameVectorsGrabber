from PyQt4.QtCore import Qt, QPointF
from PyQt4.QtGui import *
from qfvg_mainwindow_ui import Ui_MainWindow
from images.image_converter import ImageConverter
from images.image_comparator import ImageComparator
from images.algorithms.full_search import FullSearch
from images.algorithms.q_step_search import QStepSearch
from images.algorithms.logarithmic_2d_search import Logarithmic2DSearch
from images.algorithms.orthogonal_search import OrthogonalSearch
from utils.logging import klog

from frames_timeline.qframes_timeline_listmodel import QFramesTimelineListModel
from frames_timeline.qframes_timeline_delegate import QFramesTimelineDelegate
from frames_timeline.qanalyzed_frames_timeline_listmodel import QAnalyzedFramesTimelineListModel
from videos.video_comparator import VideoComparator
from videos.video_interpolator import VideoInterpolator

from videos.video import Video
import time, math


class QFVGMainWindow(QMainWindow):


    def __init__(self):

        self.image_1 = None
        self.image_1_luminance = None

        self.image_2 = None
        self.image_2_luminance = None

        self.video = None

        self.vectors = []
        self._discared_frames = []

        self._wait_dialog = None

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Event handling
        self.ui.actionOpen_video.triggered.connect(self._choose_video_file)
        self.ui.chooseFrame1PushButton.clicked.connect(self._choose_frame1)
        self.ui.chooseFrame2PushButton.clicked.connect(self._choose_frame2)
        self.ui.showLuminanceCheckBox.clicked.connect(self._show_frame_luminance)
        self.ui.findVectorsPushButton.clicked.connect(self._find_frame_vectors)
        self.ui.reconstructFrame2PushButton.clicked.connect(self._draw_compressed_frame2)
        self.ui.searchTypeComboBox.currentIndexChanged.connect(self._show_hide_search_parameters)
        self.ui.zoomInPushButton.clicked.connect(self._zoom_in_views)
        self.ui.zoomOutPushButton.clicked.connect(self._zoom_out_views)
        self.ui.analyzeVideoPushButton.clicked.connect(self._analyzeVideo)
        self.ui.interpolateVideoPushButton.clicked.connect(self._interpolateVideo)

        self.ui.searchTypeComboBox.setCurrentIndex(3)
        #self._show_hide_search_parameters(1)

        #TODO: REMOVE ME
        self._load_sample_images_from_HD()

        #TODO: REMOVE ME
        #self.video = Video("/Users/luca/Dropbox/ComunicazioniMul2/Mazzini/Videos/Coldplay_mini_charlie_brownHD.mov")
        self.video = Video("/Users/luca/Dropbox/ComunicazioniMul2/Mazzini/Videos/Pallone/pallone.mov")
        self.video.load(self._frames_created)

        self.ui.framesTimelineListView.pressed.connect(self._frame_clicked)

    def _frame_clicked(self, index):
        model = self.ui.framesTimelineListView.model()

        if QApplication.mouseButtons() & Qt.LeftButton:
            #Left button choose the Frame #1
            self.image_1 = model.data(index, Qt.DisplayRole).toImage()
            self.image_1_luminance = None

            self._draw_frame(self.image_1, self.ui.frame1GraphicsView)
            QMessageBox(QMessageBox.Information, "Frame Choosed", "Frame 1 changed!").exec_()

        elif QApplication.mouseButtons() & Qt.RightButton:
            #Right button choose the Frame #2
            self.image_2 = model.data(index, Qt.DisplayRole).toImage()
            self.image_2_luminance = None

            self._draw_frame(self.image_2, self.ui.frame2GraphicsView)
            QMessageBox(QMessageBox.Information, "Frame Choosed", "Frame 2 changed!").exec_()

    def _interpolateVideo(self):
        print "Interpolating video..."
        dialog = QMessageBox(self)
        dialog.setText("Attendi mentre ricostruisco il video...")
        dialog.show()

        start_time = time.time()
        interpolator = VideoInterpolator(self.video)

        #self._discared_frames = [1, 2, 3] #TODO: remove me
        frames_path = interpolator.interpolate(self._discared_frames, self.searcher(), self.ui.blockSizeSpinBox.value(), self.ui.MADThresholdSpingBox.value())
        klog("L'interpolazione del video ha impiegato: %.2f secondi" % (time.time()-start_time))


        interpolated_video = Video(frames_path=frames_path)
        #interpolated_video = Video(frames_path="/tmp/pallone.mov.interpolated")
        interpolated_video.load()
        dialog.close()

        self.ui.interpolatedFramesTimelineListView.setModel( QFramesTimelineListModel( interpolated_video ) )
        self.ui.interpolatedFramesTimelineListView.setItemDelegate( QFramesTimelineDelegate() )


    def searcher(self):
        search_type = self.ui.searchTypeComboBox.currentText()
        if search_type == "Full":
            searcher = FullSearch(self.ui.blockSizeSpinBox.value(), self.ui.searchWindowSizeSpinBox.value())
        elif search_type == "Q-Step":
            searcher = QStepSearch(self.ui.blockSizeSpinBox.value(), self.ui.searchStepSpinBox.value())
        elif search_type == "2D Logarithmic":
            searcher = Logarithmic2DSearch(self.ui.blockSizeSpinBox.value(), self.ui.searchStepSpinBox.value())
        elif search_type == "Orthogonal":
            searcher = OrthogonalSearch(self.ui.blockSizeSpinBox.value(), self.ui.searchStepSpinBox.value())
        else:
            searcher = OrthogonalSearch(16, 6)

        return searcher


    def _analyzeVideo(self):
        if not self.video:
            print "Please first choose a video"
        else:
            dialog = QMessageBox(self)
            dialog.setText("Attendi mentre analizzo il video...")
            dialog.show()

            start_time = time.time()
            comparator = VideoComparator(self.video, self.searcher())
            holden_frames, self._discared_frames = comparator.compared_frames_statuses(self.ui.maxVectDistThreSpinBox.value(), self.ui.MADThresholdSpingBox.value())
            klog("L'analisi del video ha impiegato: %.2f secondi" % (time.time()-start_time))
            print "Holden frames: "+ str(holden_frames)
            print "Discared frames: "+ str(self._discared_frames)
            dialog.close()

            model = QAnalyzedFramesTimelineListModel(self.video, self._discared_frames)
            self.ui.analyzedFramesTimelineListView.setModel(model)
            self.ui.analyzedFramesTimelineListView.setItemDelegate(QFramesTimelineDelegate())

    def _draw_frames_timeline(self):
        model = QFramesTimelineListModel(self.video)
        delegate = QFramesTimelineDelegate()

        self.ui.framesTimelineListView.setModel(model)
        self.ui.framesCountLabel.setText(str(model.rowCount(None)))
        self.ui.framesTimelineListView.setItemDelegate(delegate)

        self.ui.framesTimelineListView2.setModel(model)
        self.ui.framesTimelineListView2.setItemDelegate(delegate)

    def _frames_created(self, success):
        if self._wait_dialog:
            self._wait_dialog.close()

        if success:
            self._draw_frames_timeline()
        else:
            print "Qualcosa e andato storto"

    def _choose_video_file(self):
        input_file_name = str(QFileDialog.getOpenFileName(self, 'Open file'))
        if input_file_name:
            self._wait_dialog = QMessageBox(self)
            self._wait_dialog.setText("Attendi mentre apro il video...")
            self._wait_dialog.show()
            self.video = Video(input_file_name)
            self.video.load(self._frames_created)

    def _load_sample_images_from_HD(self):
        self.image_1 = QImage("samples/images/cat/cat1.png")
        self._draw_frame(self.image_1, self.ui.frame1GraphicsView)

        self.image_2 = QImage("samples/images/cat/cat2.png")
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
            scene = graphics_view.scene()

            if not scene:
                scene = QGraphicsScene()
                graphics_view.setScene(scene)

            scene.clear()
            scene.addPixmap(QPixmap.fromImage(image))

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
                start_time = time.time()
                self.image_1_luminance = ImageConverter.luminance_qimage(self.image_1)
                klog("La conversione in luminanza ha impiegato: %.2f secondi" % (time.time()-start_time))

            return self.image_1_luminance
        else:
            return None

    def get_image2_luminance(self):
        if self.image_2:
            if not self.image_2_luminance:
                start_time = time.time()
                self.image_2_luminance = ImageConverter.luminance_qimage(self.image_2)
                klog("La conversione in luminanza ha impiegato: %.2f secondi" % (time.time()-start_time))
            return self.image_2_luminance
        else:
            return None


    def _find_frame_vectors(self):
        if self.get_image1_luminance() and self.get_image2_luminance():

            klog("Evaluating image with size: %dx%d" %(self.get_image1_luminance().width(), self.get_image2_luminance().height() ))
            comp = ImageComparator(self.image_1_luminance)

            start_time = time.time()

            self.vectors = comp.get_motion_vectors(self.image_2_luminance, self.searcher())

            elasped_time = time.time() - start_time
            self.ui.searchElapsedTimeLabel.setText("%.2f seconds" %elasped_time)

            self._draw_compressed_frame2()

    def _draw_motion_vectors(self):

        sze = 3
        scene = self.ui.frame2GraphicsView.scene()
        scene.clear()
        self._draw_frame(self.image_2, self.ui.frame2GraphicsView)

        pen = QPen(Qt.red, 1, Qt.SolidLine)

        for v in self.vectors:

            x = int(v["x"])
            y = int(v["y"])
            to_x = int(v["to_x"])
            to_y = int(v["to_y"])
            MAD = v["MAD"]

            klog( "(%d, %d) => (%d, %d)" % (x,y, to_x, to_y) )


            if scene:
                if MAD < self.ui.MADThresholdSpingBox.value() and (x != to_x or y != to_y):
                    scene.addLine(x,y,to_x, to_y, pen)
                    M_PI = math.pi
                    curr_x = x - to_x
                    curr_y = y - to_y
                    if curr_x != 0 or curr_y != 0:#altrimenti la linea e lunga 0!!!
                        alpha = math.atan2 (curr_y, curr_x)
                        pa_x = sze * math.cos (alpha + M_PI / 7) + to_x
                        pa_y = sze * math.sin (alpha + M_PI / 7) + to_y
                        pb_x = sze * math.cos (alpha - M_PI / 7) + to_x
                        pb_y = sze * math.sin (alpha - M_PI / 7) + to_y

                        #scene.addLine(to_x, to_y,pa_x, pa_y)
                        #scene.addLine(to_x, to_y,pb_x, pb_y)

                        polygon = QPolygonF([QPointF(to_x-sze * math.cos (alpha), to_y-sze * math.sin (alpha)),QPointF(pa_x, pa_y),QPointF(pb_x, pb_y)])
                        scene.addPolygon(polygon, pen)


        longest_vector, max_distance = ImageComparator.longest_motion_vector(self.vectors)
        print "Max motion vector distance: %f" % max_distance



    def _draw_motion_vectors_old(self):
        scene = self.ui.frame2GraphicsView.scene()
        scene.clear()
        self._draw_frame(self.image_2, self.ui.frame2GraphicsView)

        pen = QPen(Qt.red, 1, Qt.SolidLine)

        for v in self.vectors:
            x = int(v["x"])
            y = int(v["y"])
            to_x = int(v["to_x"])
            to_y = int(v["to_y"])
            MAD = v["MAD"]

            klog( "(%d, %d) => (%d, %d)" % (x,y, to_x, to_y) )

            if scene:
                if MAD < self.ui.MADThresholdSpingBox.value() and (x != to_x or y != to_y):
                    scene.addLine(x,y,to_x, to_y, pen)

    def _draw_compressed_frame2(self):
        if len(self.vectors) > 0:

            self._draw_motion_vectors()
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

                        moved_block_image = self.image_1.copy(x,y, self.get_block_size(), self.get_block_size())
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

            total_mads_checked = 0
            for v in self.vectors:
                total_mads_checked += v["MAD_checks_count"]

            self.ui.MADsCheckedLabel.setText("%d" %total_mads_checked)

    def _show_hide_search_parameters(self, search_type):
        if search_type == 0:
            #Full search
            self.ui.searchStepLabel.hide()
            self.ui.searchStepSpinBox.hide()
            self.ui.searchWindowSizeLabel.show()
            self.ui.searchWindowSizeSpinBox.show()

        else:
            self.ui.searchStepLabel.show()
            self.ui.searchStepSpinBox.show()
            self.ui.searchWindowSizeLabel.hide()
            self.ui.searchWindowSizeSpinBox.hide()

    def _zoom_in_views(self):
        self.ui.frame1GraphicsView.scale(2, 2)
        self.ui.frame2GraphicsView.scale(2, 2)
        self.ui.frame2CompressedGraphicsView.scale(2, 2)
        self.ui.frame2ReconstructedGraphicsView.scale(2, 2)

    def _zoom_out_views(self):
        self.ui.frame1GraphicsView.scale(0.5, 0.5)
        self.ui.frame2GraphicsView.scale(0.5, 0.5)
        self.ui.frame2CompressedGraphicsView.scale(0.5, 0.5)
        self.ui.frame2ReconstructedGraphicsView.scale(0.5, 0.5)

    def get_block_size(self):
        return self.ui.blockSizeSpinBox.value()

    def get_search_window_size(self):
        return self.ui.searchWindowSizeSpinBox.value()
