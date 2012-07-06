__author__ = 'luca'

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import QPixmap

class QFramesTimelineListModel(QAbstractListModel):
    def __init__(self, frames_folder):
        self.frames_folder = frames_folder
        self.frames_files = []
        self.pixmaps = {}


        for file_name in os.listdir(frames_folder):
            if file_name.endswith(".png") or file_name.endswith(".jpg"):
                self.frames_files.append(self.frames_folder+"/"+file_name)

                #REMOVE ME, ONLY TO DEBUG
                # if len(self.frames_files) > 1:
                #    break

        super(QFramesTimelineListModel, self).__init__()

    def rowCount(self, parent):
        return len(self.frames_files)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if not self.pixmaps.has_key(index.row()):
                pixmap = QPixmap(self.frames_files[index.row()])
                self.pixmaps[index.row()] = pixmap#.scaled(300, 250, Qt.KeepAspectRatio)

            return self.pixmaps[index.row()]
        else:
            return QVariant()
