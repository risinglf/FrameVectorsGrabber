from PyQt4.QtGui import QImage, QColor


Kb = 0.0722
Kr = 0.212

class ImageConverter(object):

    @classmethod
    def luminance_qimage(cls, qimage):
        #   for each pixel:
        #       get the RGB color
        #       transform the RGB color in the YUV (with zero U and V)
        #       transform the YUV color into RGB_new
        #       set the pixel of the new image to RGB_new

        new_qimage = QImage(qimage.size(), qimage.format())
        for h in xrange(qimage.height()):
            for w in xrange(qimage.width()):
                pixel = qimage.pixel(w,h)

                rgb_new = ImageConverter.luminance_qrgb(pixel)
                new_qimage.setPixel(w, h, rgb_new)

        return new_qimage

    @classmethod
    def luminance_qrgb(cls, qrgb):
        qcolor = QColor(qrgb)
        y = qcolor.redF()*Kr + (1-Kr-Kb)*qcolor.greenF() + qcolor.blueF()*Kb
        new_color = QColor()
        new_color.setRgbF(y, y, y)
        return new_color.rgb()

