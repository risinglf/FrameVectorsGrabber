from PyQt4.QtGui import QColor
from utils.logging import klog

class ImageComparator(object):
    def __init__(self, image):
        self.image = image

    def get_motion_vectors(self, image2, block_size = 8, search_window_size = 10):
        '''
        1)  Divide self.image into blocks of 8x8 pixels
        2)  for each block:
        4)      get the X and Y
        5)      search block in image2 from X and Y, moving from 0 to P pixel right, left, top, bottom
        6)      block found?
        7)          if yes, get the new X and Y
        8)          if no, return 0
        '''

        vectors = []


        for block_x_num in range(0, self.image.width()/block_size):
            block_x_pos = block_size*block_x_num

            for block_y_num in range(0, self.image.height()/block_size):

                block_y_pos = block_size*block_y_num

                (new_x, new_y, MAD) = ImageComparator.search_block(self.image, block_x_pos, block_y_pos, image2, block_size, search_window_size)

                #if (block_x_pos != new_x) or (block_y_pos != new_y):
                vector = { 'x': block_x_pos, 'y': block_y_pos, 'to_x' : new_x, 'to_y': new_y, 'MAD': MAD}
                vectors.append(vector)

        return vectors


    @classmethod
    def search_block(cls, image1, x_start, y_start, image2, block_size, margin_size):

        best_MAD = 1000000
        best_x = None
        best_y = None
        subimage_1 = image1.copy(x_start, y_start, block_size, block_size)

        for py in range(y_start-margin_size, y_start+margin_size):

            if py < 0:
                continue #il blocco esce in su dall'immagine, avanza con il prossimo py incrementato

            if py+block_size > image2.height():
                break #il blocco esce in giu dall'immagine, esci


            for px in range(x_start-margin_size, x_start+margin_size):


                if px < 0:
                    continue #il blocco esce a sinistra dall'immagine, avanza con il prossimo px incrementato

                if px+block_size > image2.width():
                    break #il blocco esce a destra dall'immagine, esci

                klog("Valuating block (%f,%f)" %(px, py))

                #Create the subimages
                subimage_2 = image2.copy(px, py, block_size, block_size)

                #Calculate the MAD
                MAD = ImageComparator.calculate_MAD(subimage_1, subimage_2)

                klog("MAD found: %f" % MAD)

                if MAD < best_MAD:
                    klog("Best MAD found: %f, at (%f,%f)" % (MAD, px, py))
                    best_MAD = MAD
                    best_x = px
                    best_y = py

        return (best_x, best_y, best_MAD)

    @classmethod
    def calculate_MAD(cls, image1, image2):
        if image1.width() != image2.width() or image1.height() != image2.height():
            raise Exception("Images with different width or height")


        width = image1.width()
        height = image1.height()
        sum_MAD = 0.0

        for x in range(1, width):
            for y in range(1, height):

                luminance_1 = QColor.fromRgb(image1.pixel(x,y)).redF() #is already in luminance mode (red=green=blue)
                luminance_2 = QColor.fromRgb(image2.pixel(x,y)).redF() #already in luminance mode (red=green=blue)

                sum_MAD += abs( luminance_1-luminance_2 )

        return sum_MAD/(width*height)
