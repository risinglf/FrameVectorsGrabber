__author__ = 'luca'

from PyQt4.QtCore import *
from PyQt4.QtGui import QPixmap


class QFramesTimelineListModel(QAbstractListModel):
    def __init__(self, video):
        self.video = video
        self.pixmaps = {}
        super(QFramesTimelineListModel, self).__init__()

    def rowCount(self, parent):
        return self.video.frames_count()

    def data(self, index, role):
        if role == Qt.DisplayRole:

            if not self.pixmaps.has_key(index.row()):
                frame = self.video.frames[index.row()]
                pixmap = QPixmap(frame.path())
                self.pixmaps[index.row()] = pixmap #.scaled(300, 250, Qt.KeepAspectRatio)

            return self.pixmaps[index.row()]
        else:
            return QVariant()
