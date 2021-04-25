"""Parser implementation for  pixel format"""

from ..image.color_format import *
from ..image.image import *
from .common import AbstractParser

import numpy
import cv2 as cv
import math


class ParserYUV420(AbstractParser):
    """A semi-planar YUV420 implementation of a parser"""
    def parse(self, raw_data, color_format, width, height):

        max_value = max(color_format.bits_per_components)
        curr_dtype = numpy.uint8

        data_array = []
        try:
            if len(set(color_format.bits_per_components)
                   ) == 2 and max_value % 8 == 0:
                data_array = numpy.frombuffer(raw_data,
                                              dtype=curr_dtype,
                                              count=(int(height * width *
                                                         1.5)))
            else:
                raise NotImplementedError(
                    "Other than 8-bit YUVs are not currently supported")
        except ValueError:
            raise ValueError(
                "Not enough values in buffer to construct image of resolution {} x {}"
                .format(width, height))

        processed_data = numpy.array(data_array, dtype=curr_dtype)
        return Image(raw_data, color_format, processed_data, width, height)

    def get_displayable(self, image):
        """Provides displayable image data (BGR formatted)

        Returns: Numpy array containing displayable data.
        """
        return_data = image.processed_data

        conversion_const = None
        if image.color_format.pixel_format == PixelFormat.YUV:
            conversion_const = cv.COLOR_YUV2BGR_NV12
        elif image.color_format.pixel_format == PixelFormat.YVU:
            conversion_const = cv.COLOR_YUV2BGR_NV21

        return_data = cv.cvtColor(
            numpy.reshape(
                return_data,
                (int(image.height * 1.5), image.width)).astype('uint8'),
            conversion_const)
        return return_data


class ParserYUV422(AbstractParser):
    """A packed YUV422 implementation of a parser"""
    def parse(self, raw_data, color_format, width, height):
        max_value = max(color_format.bits_per_components)
        curr_dtype = numpy.uint8

        data_array = []
        try:
            if len(set(color_format.bits_per_components)
                   ) == 1 and max_value % 8 == 0:
                data_array = numpy.frombuffer(raw_data,
                                              dtype=curr_dtype,
                                              count=(int(height * width * 2)))
            else:
                raise NotImplementedError(
                    "Other than 8-bit YUVs are not currently supported")
        except ValueError:
            raise ValueError(
                "Not enough values in buffer to construct image of resolution {} x {}"
                .format(width, height))

        processed_data = numpy.array(data_array, dtype=curr_dtype)
        return Image(raw_data, color_format, processed_data, width, height)

    def get_displayable(self, image):
        """Provides displayable image data (BGR formatted)

        Returns: Numpy array containing displayable data.
        """
        return_data = numpy.reshape(image.processed_data,
                                    (image.height, int(image.width / 2), 4))

        conversion_const = None
        if image.color_format.pixel_format == PixelFormat.YUYV:
            conversion_const = cv.COLOR_YUV2BGR_YUYV
        elif image.color_format.pixel_format == PixelFormat.UYVY:
            conversion_const = cv.COLOR_YUV2BGR_UYVY

        return_data = cv.cvtColor(
            numpy.reshape(return_data,
                          (image.height, image.width, 2)).astype('uint8'),
            conversion_const)
        return return_data
