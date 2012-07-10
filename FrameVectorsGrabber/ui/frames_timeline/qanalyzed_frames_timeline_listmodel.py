__author__ = 'luca'
from PyQt4.QtCore import *
from PyQt4.QtGui import QPixmap

class QAnalyzedFramesTimelineListModel(QAbstractListModel):

    def __init__(self, video, discared_frames):
        self.video = video
        self._discared_frames = discared_frames
        self.pixmaps = {}
        super(QAnalyzedFramesTimelineListModel, self).__init__()

    def rowCount(self, parent):
        return self.video.frames_count()

    def data(self, index, role):
        if role == Qt.DisplayRole:

            if not self.pixmaps.has_key(index.row()):

                #Check if the frame is discared, if so create a blank pixmap
                if int(index.row()) in self._discared_frames:
                    #Blank frame
                    pixmap = QPixmap(1, 1).scaled(self.video.width(), self.video.height())
                    pixmap.fill(Qt.black)
                else:
                    frame = self.video.frames[index.row()]
                    pixmap = QPixmap(frame.path())#.scaled(200, 100, Qt.KeepAspectRatio)
                self.pixmaps[index.row()] = pixmap

            return self.pixmaps[index.row()]
        else:
            return QVariant()
