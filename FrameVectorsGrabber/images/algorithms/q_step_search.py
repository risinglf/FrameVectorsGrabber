__author__ = 'luca'

from searcher import Searcher
from images.image_comparator import ImageComparator
from images.image_converter import ImageConverter
from utils.logging import klog

class QStepSearch(Searcher):
    def __init__(self, block_size, pass_step = 6):
        self.block_size = block_size
        self.pass_step = pass_step
        super(QStepSearch, self).__init__()

    def search(self, image1_pixels, x_start, y_start, image2_pixels):

        self.reset_search()

        block_size = self.block_size
        pass_step = self.pass_step

        subimage_1_pixels = ImageConverter.sub_pixels(image1_pixels, x_start, y_start, x_start+block_size, y_start+block_size)


        p = pass_step
        ds = p/2
        s = 1
        xs = x_start
        ys = y_start
        xs_min = -1
        ys_min = -1
        best_local_MAD = 10000
        best_global_MAD = 10000
        best_x = -1
        best_y = -1

        klog("Check block from %d, %d" %(x_start, y_start))

        while ds >= 1:
            for x in [xs, xs+ds, xs-ds]:
                for y in [ys, ys+ds, ys-ds]:

                    if not ImageComparator.is_valid_coordinate(x, y, block_size, image2_pixels):
                        continue

                    MAD = self.calculate_MAD(subimage_1_pixels, image2_pixels, x, y, x+block_size, y+block_size)

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
            ds -= 1
            xs = xs_min
            ys = ys_min
        print "-"
        return best_x, best_y, best_global_MAD, self._MAD_checks_count
