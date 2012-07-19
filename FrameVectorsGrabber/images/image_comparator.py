from PyQt4.QtGui import QColor, QImage
from images.image_converter import ImageConverter
#from utils.logging import klog
import math
import time

class ImageComparator(object):
    def __init__(self, image):
        self.image = image

    def get_motion_vectors(self, image2, searcher, MAD_threshold = None):
        """
        1)  Divide self.image into blocks of 8x8 pixels
        2)  for each block:
        4)      get the X and Y
        5)      search block in image2 from X and Y, moving from 0 to P pixel right, left, top, bottom
        6)      block found?
        7)          if yes, get the new X and Y
        8)          if no, return 0
        """


        if isinstance(self.image, QImage):
            image1 = ImageConverter.qtimage_to_pil_image(self.image)
        else:
            image1 = self.image

        images1_pixels = image1.load()

        if isinstance(image2, QImage):
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

                valid_vector = True

                if MAD_threshold and MAD > MAD_threshold:
                    #Discard the vector if the MAD is over ranged
                    valid_vector = False

                if valid_vector:
                    #if (block_x_pos != new_x) or (block_y_pos != new_y):
                    vector = { 'x': block_x_pos, 'y': block_y_pos, 'to_x' : new_x, 'to_y': new_y, 'MAD': MAD, 'MAD_checks_count': MAD_checks_count}
                    vectors.append(vector)

        return vectors


    @classmethod
    def calculate_MAD_v2(cls, image1_pixels, image2_pixels):
        sum_MAD = 0.0
        pixels_count = len(image1_pixels)

        for p in range(pixels_count):
            pixel_1 = image1_pixels[p]
            pixel_2 = image2_pixels[p]

            if isinstance(pixel_1, tuple):
                luminance_1 = pixel_1[0] #is already in luminance mode (red=green=blue)
                luminance_2 = pixel_2[0] #already in luminance mode (red=green=blue)
            else:
                luminance_1 = pixel_1
                luminance_2 = pixel_2

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
    def calculate_PSNR(cls, image1, image2, width, height):
        image1_pixels = image1.load()
        image2_pixels = image2.load()

        MSE = 0
        MAX = 255

        for x in range(1, width):
            for y in range(1, height):

                red_1 = image1_pixels[x,y][0]
                red_2 = image2_pixels[x,y][0]
                delta_red = math.pow(red_1-red_2, 2)

                green_1 = image1_pixels[x,y][1]
                green_2 = image2_pixels[x,y][1]
                delta_green = math.pow(green_1-green_2, 2)

                blue_1 = image1_pixels[x,y][2]
                blue_2 = image2_pixels[x,y][2]
                delta_blue = math.pow(blue_1-blue_2, 2)


                MSE += delta_red + delta_green +delta_blue


        MSE /= (width*height*3)
        if MSE != 0:
            PSNR = 10* math.log( math.pow(MAX, 2)/MSE, 10)
        else:
            #Perfect Image, avoid division by zero
            PSNR = 100000
        return PSNR

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


    @classmethod
    def longest_motion_vector(cls, motion_vectors):
        longest_vector = {}
        max_distance = 0

        for vector in motion_vectors:
            distance = math.sqrt( math.pow(vector['x']-vector['to_x'], 2) + math.pow(vector['y']-vector['to_y'], 2) )

            if distance > max_distance:
                max_distance = distance
                longest_vector = vector

        return (longest_vector, max_distance)
