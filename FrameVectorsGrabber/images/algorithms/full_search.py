__author__ = 'luca'
from images.image_comparator import ImageComparator
from images.image_converter import ImageConverter

class FullSearch(object):
    def __init__(self, block_size, margin_size):
        self.block_size = block_size
        self.margin_size = margin_size


    def search(self, image1_pixels, x_start, y_start, image2_pixels):

        MAD_checks_count = 0
        block_size = self.block_size
        margin_size = self.margin_size
        best_MAD = 1000000
        best_x = None
        best_y = None

        subimage_1_pixels = ImageConverter.sub_pixels(image1_pixels, x_start, y_start, x_start+block_size, y_start+block_size)

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

                #Create the subimages
                subimage_2_pixels = ImageConverter.sub_pixels(image2_pixels, px, py, px+block_size, py+block_size)

                #Calculate the MAD
                MAD = ImageComparator.calculate_MAD_v2(subimage_1_pixels, subimage_2_pixels)
                MAD_checks_count += 1


                #klog("MAD found: %f" % MAD)

                if MAD < best_MAD:
                    #klog("Best MAD found: %f, at (%f,%f)" % (MAD, px, py))
                    best_MAD = MAD
                    best_x = px
                    best_y = py

        return best_x, best_y, best_MAD, MAD_checks_count
