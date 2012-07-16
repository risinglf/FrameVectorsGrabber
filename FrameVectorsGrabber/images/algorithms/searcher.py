from images.image_comparator import ImageComparator
from images.image_converter import ImageConverter
from utils.logging import klog


class Searcher(object):
    def __init__(self):
        self._coordinates_checked = {}
        self._MAD_checks_count = 0

    def calculate_MAD(self, subimage_1_pixels, image2_pixels, x, y, to_x, to_y):
        """
            subimage_1_pixels is the the image to be found
            image2_pixels is the pixels of the image that should contain sub_pixels_1
            x, y is the upper coordinate of pixels_2 to be checked
            x+block_size, y+block_size is the lower coordinate of pixels_2 to be checked
        """
        MAD = self._get_saved_MAD(x, y)

        if not MAD:
            subimage_2_pixels = ImageConverter.sub_pixels(image2_pixels, x, y, to_x, to_y)

            #Calculate the MAD
            MAD = ImageComparator.calculate_MAD_v2(subimage_1_pixels, subimage_2_pixels)
            self._coordinates_checked["%dx%d" %(x,y)] = MAD
            self._MAD_checks_count += 1

        klog("%d,%d\t\t\t\tMAD-> %f" %(x,y, MAD))
        return MAD


    def _get_saved_MAD(self, x, y):
        if self._coordinates_checked.has_key("%dx%d" %(x,y)):
            return self._coordinates_checked["%dx%d" %(x,y)]
        else:
            return None

