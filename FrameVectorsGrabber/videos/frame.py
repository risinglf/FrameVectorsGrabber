__author__ = 'luca'

from PIL import Image
from images.image_converter import ImageConverter

class Frame(object):
    def __init__(self, path):
        self._path = path
        self._image = None
        self._grayscaled_image = None

    def path(self):
        return self._path

    def image(self):
        if not self._image:
            self._image = Image.open(self._path)

        return self._image

    def grayscaled_image(self):
        if not self._grayscaled_image:
            self._grayscaled_image = ImageConverter.luminance_image(self.image())

        return self._grayscaled_image

    def width(self):
        return self.image().size[0]

    def height(self):
        return self.image().size[1]
