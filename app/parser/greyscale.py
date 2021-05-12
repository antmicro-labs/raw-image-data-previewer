"""Parser implementation for greyscale pixel format"""

from ..image.image import Image
from .common import AbstractParser

import numpy
import cv2 as cv


class ParserGreyscale(AbstractParser):
    """A greyscale implementation of a parser"""
    def parse(self, raw_data, color_format, width, height=None):
        """Parses provided raw data to an image, calculating height from provided width.

        Keyword arguments:

            raw_data: bytes object
            color_format: target instance of ColorFormat
            width: target width to interpret
            height: (deprecated) target height to interpret, default: None

        Returns: instance of Image processed to chosen format
        """

        bits_per_grey = color_format.bits_per_components[0]
        curr_dtype = None
        if bits_per_grey <= 8:
            curr_dtype = '>u1'
        else:
            curr_dtype = '>u2'

        processed_data = numpy.frombuffer(raw_data, dtype=curr_dtype)
        if (processed_data.size % width != 0):
            processed_data = numpy.concatenate(
                (processed_data,
                 numpy.zeros(width - (processed_data.size % width))))

        return Image(raw_data, color_format, processed_data, width,
                     processed_data.size // width)

    def get_displayable(self, image):
        """Provides displayable image data (RGB formatted)

        Returns: Numpy array containing displayable data.
        """
        return_data = image.processed_data

        data_array = numpy.reshape(return_data,
                                   (image.height, image.width)).astype('float')

        data_array[:] = 255 * (
            data_array[:] / (2**image.color_format.bits_per_components[0] - 1))

        return_data = cv.cvtColor(data_array.astype('uint8'),
                                  cv.COLOR_GRAY2RGB)
        return return_data