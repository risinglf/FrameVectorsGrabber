__author__ = 'luca'
from searcher import Searcher
from images.image_comparator import ImageComparator
from images.image_converter import ImageConverter

class FullSearch(Searcher):
    def __init__(self, block_size, margin_size):
        self.block_size = block_size
        self.margin_size = margin_size
        super(FullSearch, self).__init__()


    def search(self, image1_pixels, x_start, y_start, image2_pixels):

        self.reset_search()

        block_size = self.block_size
        margin_size = self.margin_size
        best_MAD = 1000000
        best_x = None
        best_y = None

        subimage_1_pixels = ImageConverter.sub_pixels(image1_pixels, x_start, y_start, x_start+block_size, y_start+block_size)


        #Start with the center
        if ImageComparator.is_valid_coordinate(x_start, y_start, block_size, image2_pixels):
            MAD = self.calculate_MAD(subimage_1_pixels, image2_pixels, x_start, y_start, x_start+block_size, y_start+block_size)
            if MAD < best_MAD:
                #klog("Best MAD found: %f, at (%f,%f)" % (MAD, px, py))
                best_MAD = MAD
                best_x = x_start
                best_y = y_start
            if best_MAD == 0:
                return best_x, best_y, best_MAD, self._MAD_checks_count


        for py in range(y_start-margin_size, y_start+margin_size):

            if py < 0:
                continue #il blocco esce in su dall'immagine, avanza con il prossimo py incrementato

            #CHECK!!
            if not ImageComparator.is_valid_coordinate(0, py, block_size, image2_pixels):
                break #il blocco esce in giu dall'immagine, esci

            for px in range(x_start-margin_size, x_start+margin_size):

                if px < 0:
                    continue #il blocco esce a sinistra dall'immagine, avanza con il prossimo px incrementato

                #CHECK!!
                if not ImageComparator.is_valid_coordinate(px, py, block_size, image2_pixels):
                    break #il blocco esce in giu dall'immagine, esci

                #if px+block_size > image2.width():
                #    break #il blocco esce a destra dall'immagine, esci

                #klog("Valuating block (%f,%f)" %(px, py))

                MAD = self.calculate_MAD(subimage_1_pixels, image2_pixels, px, py, px+block_size, py+block_size)

                if MAD < best_MAD:
                    #klog("Best MAD found: %f, at (%f,%f)" % (MAD, px, py))
                    best_MAD = MAD
                    best_x = px
                    best_y = py

                if best_MAD == 0:
                    return best_x, best_y, best_MAD, self._MAD_checks_count


        return best_x, best_y, best_MAD, self._MAD_checks_count
