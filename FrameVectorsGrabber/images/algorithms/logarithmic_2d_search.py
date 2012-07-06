from utils.logging import klog
from images.image_converter import ImageConverter

__author__ = 'luca'

from images.image_comparator import ImageComparator
import math

class Logarithmic2DSearch(object):
    def __init__(self, block_size, pass_step = 6):
        self.block_size = block_size
        self.pass_step = pass_step

    def search(self, image1_pixels, x_start, y_start, image2_pixels):

        block_size = self.block_size
        pass_step = self.pass_step

        #subimage_1 = image1.copy(x_start, y_start, block_size, block_size)
        subimage_1_pixels = ImageConverter.sub_pixels(image1_pixels, x_start, y_start, x_start+block_size, y_start+block_size)

        MAD_checks_count = 0
        p = pass_step
        ds = math.pow(2, math.floor( math.log(p,2))-1 )
        s = 1
        xs = x_start
        ys = y_start
        xs_min = -1
        ys_min = -1
        best_local_MAD = 10000
        best_global_MAD = 10000
        best_x = -1
        best_y = -1

        while ds >= 1:

            if ds != 1:

                for (x,y) in [(xs, ys), (xs-ds,ys), (xs+ds, ys), (xs, ys+ds), (xs,ys-ds)]:

                    if not ImageComparator.is_valid_coordinate(x, y, block_size, image2_pixels):
                        continue

                    #Create the subimages
                    subimage_2_pixels = ImageConverter.sub_pixels(image2_pixels, x, y, x+block_size, y+block_size)

                    #Calculate the MAD
                    MAD = ImageComparator.calculate_MAD_v2(subimage_1_pixels, subimage_2_pixels)
                    MAD_checks_count += 1

                    klog("%d,%d\t\t\t\tMAD-> %f" %(x,y, MAD))

                    if MAD < best_local_MAD:
                        best_local_MAD = MAD
                        xs_min = x
                        ys_min = y

                    #Check if the local MAD is the best global MAD
                    if MAD < best_global_MAD:
                        best_global_MAD = MAD
                        best_x = x
                        best_y = y

                s += 1

                #Check if the xs_min and ys_min are the central point of the fives checked
                print "ds: %d" %ds
                if xs_min == xs and ys_min == ys:
                    ds = ds/2

                xs = xs_min
                ys = ys_min


            else: #ds==1 last step

                for x in [xs, xs+ds, xs-ds]:

                    for y in [ys, ys+ds, ys-ds]:

                        #TODO: CODE HERE IS COPY-PASTED!! THIS SUCKS! secondo me va bene!
                        if not ImageComparator.is_valid_coordinate(x, y, block_size, image2_pixels):
                            continue

                        #Create the subimages
                        #subimage_2 = image2.copy(x, y, block_size, block_size)
                        subimage_2_pixels = ImageConverter.sub_pixels(image2_pixels, x, y, x+block_size, y+block_size)

                        #Calculate the MAD
                        MAD = ImageComparator.calculate_MAD_v2(subimage_1_pixels, subimage_2_pixels)
                        MAD_checks_count += 1

                        klog("%d,%d\t\t\t\tMAD-> %f" %(x,y, MAD))

                        if MAD < best_local_MAD:
                            best_local_MAD = MAD
                            xs_min = x
                            ys_min = y

                        #Check if the local MAD is the best global MAD
                        if MAD < best_global_MAD:
                            best_global_MAD = MAD
                            best_x = x
                            best_y = y

                ds = 0
                s += 1

                print "ds: %d" %ds


        return best_x, best_y, best_global_MAD, MAD_checks_count
