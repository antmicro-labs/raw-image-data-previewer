"""Parser implementation for RGBA pixel format"""

from ..image.color_format import *
from ..image.image import *
from .common import AbstractParser

import numpy


class ParserRGBA(AbstractParser):
    """An RGBA implementation of a parser"""
    def get_displayable(self, image):
        """Provides displayable image data (BGR formatted)

        Returns: Numpy array containing displayable data.
        """
        return_data = image.processed_data.astype('float64')

        if (image.color_format.bits_per_components[3] == 0):
            bpcs = 3
        else:
            bpcs = 4

        for i in range(bpcs):
            return_data[:, :, i] = (255 * return_data[:, :, i]) / (
                2**image.color_format.bits_per_components[i] - 1)

        return_data = return_data[:, :, [2, 1, 0, 3]]
        return return_data.astype('uint8')
