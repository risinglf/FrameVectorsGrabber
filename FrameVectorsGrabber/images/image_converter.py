from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sip
import time
import cStringIO
from PIL import Image, ImageQt, ImageOps


Kb = 0.0722
Kr = 0.212

class ImageConverter(object):

    @classmethod
    def luminance_qimage(cls, qimage):
        print "FAST"
    #   for each pixel:
    #       get the RGB color
    #       transform the RGB color in the YUV (with zero U and V)
    #       transform the YUV color into RGB_new
    #       set the pixel of the new image to RGB_new

        width = qimage.width()
        height = qimage.height()

        pil_img =  ImageConverter.qtimage_to_pil_image(qimage)
        old_pixels = pil_img.load()

        new_img = Image.new( 'RGB', (width, height), "black") # create a new black image
        new_pixels = new_img.load() # create the pixel map


        for x in xrange(width):
            for y in xrange(height):
                gray_pixel = ImageConverter.luminance_pil_pixel(old_pixels[x, y])
                new_pixels[x, y] = gray_pixel

        return ImageQt.ImageQt(new_img)

    @classmethod
    def luminance_image(cls, image):
        #   for each pixel:
        #       get the RGB color
        #       transform the RGB color in the YUV (with zero U and V)
        #       transform the YUV color into RGB_new
        #       set the pixel of the new image to RGB_new
        start_time = time.time()

        new_image = ImageOps.grayscale(image)

        """
        width = image.size[0]
        height = image.size[1]

        old_pixels = image.load()

        new_image = Image.new( 'RGB', (width, height), "black") # create a new black image
        new_pixels = new_image.load() # create the pixel map

        for x in xrange(width):
            for y in xrange(height):
                gray_pixel = ImageConverter.luminance_pil_pixel(old_pixels[x, y])
                new_pixels[x, y] = gray_pixel
        """
        print "La conversione in luminanza ha impiegato: %.2f secondi" % (time.time()-start_time)

        return new_image

    @classmethod
    def qtimage_to_pil_image(cls, qimage):
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        qimage.save(buffer, "JPG")

        strio = cStringIO.StringIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        pil_img = Image.open(strio)
        return pil_img

    @classmethod
    def sub_pixels(cls, image_pixels, x_start, y_start, x_finish, y_finish):
        pixels = []
        for _x in range(int(x_start), int(x_finish)):
            for _y in range(int(y_start), int(y_finish)):
                pixels.append(image_pixels[_x, _y])

        return pixels

    @classmethod
    def luminance_qrgb(cls, qrgb):
        qcolor = QColor(qrgb)
        y = qcolor.redF()*Kr + (1-Kr-Kb)*qcolor.greenF() + qcolor.blueF()*Kb
        new_color = QColor()
        new_color.setRgbF(y, y, y)
        return new_color.rgb()

    @classmethod
    def luminance_pil_pixel(cls, pixel):
        red = pixel[0] /255.0
        green = pixel[1] /255.0
        blue = pixel[2] / 255.0

        gray = y = red*Kr + (1-Kr-Kb)*green + blue*Kb
        gray *= 255
        gray = int(gray)
        return (gray, gray, gray)

    @classmethod
    def draw_image_into_image(cls, source, destination, dest_x, dest_y):
        '''
        Draw the source image into x,y pos of destination
        '''

        for x in range(0, source.width()):
            for y in range(0, source.height()):
                source_pixel = source.pixel(x,y)
                destination.setPixel(x+dest_x, y+dest_y, source_pixel)

