__author__ = 'luca'

from images.image_comparator import ImageComparator

class QStepSearch(object):
    def __init__(self, block_size, pass_step = 6):
        self.block_size = block_size
        self.pass_step = pass_step

    def search(self, image1, x_start, y_start, image2):

        block_size = self.block_size
        pass_step = self.pass_step

        subimage_1 = image1.copy(x_start, y_start, block_size, block_size)

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

        while ds >= 1:
            for x in [xs, xs+ds, xs-ds]:
                for y in [ys, ys+ds, ys+ds]:

                    #Create the subimages
                    subimage_2 = image2.copy(x, y, block_size, block_size)

                    #Calculate the MAD
                    MAD = ImageComparator.calculate_MAD(subimage_1, subimage_2)

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

        return best_x, best_y, best_global_MAD
