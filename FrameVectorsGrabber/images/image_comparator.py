from PyQt4.QtGui import QColor
from images.image_converter import ImageConverter
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


        image1 = ImageConverter.qtimage_to_pil_image(self.image)
        images1_pixels = image1.load()

        image2 = ImageConverter.qtimage_to_pil_image(image2)
        images2_pixels = image2.load()

        width = image1.size[0]
        height = image1.size[1]

        vectors = []


        for block_x_num in range(0, width/searcher.block_size):
            block_x_pos = searcher.block_size*block_x_num

            for block_y_num in range(0, height/searcher.block_size):

                block_y_pos = searcher.block_size*block_y_num

                (new_x, new_y, MAD, MAD_checks_count) = searcher.search(images1_pixels, block_x_pos, block_y_pos, images2_pixels)

                #if (block_x_pos != new_x) or (block_y_pos != new_y):
                vector = { 'x': block_x_pos, 'y': block_y_pos, 'to_x' : new_x, 'to_y': new_y, 'MAD': MAD, 'MAD_checks_count': MAD_checks_count}
                vectors.append(vector)

        return vectors


    @classmethod
    def calculate_MAD_v2(cls, image1_pixels, image2_pixels):
        sum_MAD = 0.0
        pixels_count = len(image1_pixels)

        for p in range(pixels_count):

                luminance_1 = image1_pixels[p][0] #is already in luminance mode (red=green=blue)
                luminance_2 = image2_pixels[p][0] #already in luminance mode (red=green=blue)

                sum_MAD += abs( luminance_1-luminance_2 )

        return sum_MAD/pixels_count


    @classmethod
    def calculate_MAD(cls, image1_pixels, image2_pixels, width, height):
        sum_MAD = 0.0

        for x in range(1, width):
            for y in range(1, height):

                luminance_1 = image1_pixels[x,y][0] #is already in luminance mode (red=green=blue)
                luminance_2 = image2_pixels[x,y][0] #already in luminance mode (red=green=blue)

                sum_MAD += abs( luminance_1-luminance_2 )

        return sum_MAD/(width*height)

    @classmethod
    def is_valid_coordinate(cls, x, y, block_size, pixels):
        try:
            ok1 = pixels[x, y]
            ok2 = pixels[x+block_size-1, y+block_size-1]
            return True
        except Exception, ex:
            return False

    @classmethod
    def is_valid_x_coordinate(cls, x, block_size, image):
        return x >=0 and x+block_size <= image.size[0]

    @classmethod
    def is_valid_y_coordinate(cls, y, block_size, image):
        return y >=0 and y+block_size <= image.size[1]
