from PyQt4.QtGui import QColor
#from utils.logging import klog

class ImageComparator(object):
    def __init__(self, image):
        self.image = image

    def get_motion_vectors(self, image2, searcher):
        """
        1)  Divide self.image into blocks of 8x8 pixels
        2)  for each block:
        4)      get the X and Y
        5)      search block in image2 from X and Y, moving from 0 to P pixel right, left, top, bottom
        6)      block found?
        7)          if yes, get the new X and Y
        8)          if no, return 0
        """

        vectors = []


        for block_x_num in range(0, self.image.width()/searcher.block_size):
            block_x_pos = searcher.block_size*block_x_num

            for block_y_num in range(0, self.image.height()/searcher.block_size):

                block_y_pos = searcher.block_size*block_y_num

                (new_x, new_y, MAD, MAD_checks_count) = searcher.search(self.image, block_x_pos, block_y_pos, image2)
                #(new_x, new_y, MAD) = ImageComparator.q_step_search_block(self.image, block_x_pos, block_y_pos, image2, block_size)

                #if (block_x_pos != new_x) or (block_y_pos != new_y):
                vector = { 'x': block_x_pos, 'y': block_y_pos, 'to_x' : new_x, 'to_y': new_y, 'MAD': MAD, 'MAD_checks_count': MAD_checks_count}
                vectors.append(vector)

        return vectors


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

    @classmethod
    def is_valid_x_coordinate(cls, x, block_size, image):
        return x >=0 and x+block_size <= image.width()

    @classmethod
    def is_valid_y_coordinate(cls, y, block_size, image):
        return y >=0 and y+block_size <= image.height()
