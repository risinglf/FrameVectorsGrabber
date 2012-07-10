__author__ = 'luca'

from PyQt4.QtGui import QPixmap, QStyledItemDelegate
from PyQt4.QtCore import QSize

WIDTH = 240
HEIGHT = 180

class QFramesTimelineDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        qpixmap = QPixmap(index.data())#.scaled(WIDTH, HEIGHT)
        painter.save()
        painter.drawPixmap(option.rect.x(), option.rect.y(), qpixmap)
        painter.restore()

    def sizeHint(self, option, index):
        qimage = QPixmap(index.data())
        return qimage.size()
        #return QSize(WIDTH, HEIGHT)
