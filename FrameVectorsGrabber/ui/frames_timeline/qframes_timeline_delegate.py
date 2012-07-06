__author__ = 'luca'

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class QFramesTimelineDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        qimage = QPixmap(index.data())
        painter.save()
        painter.drawPixmap(option.rect.x(), option.rect.y(), qimage)
        painter.restore()

    def sizeHint(self, option, index):
        qimage = QPixmap(index.data())
        s =  qimage.size()
        return qimage.size()
