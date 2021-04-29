"""Parser implementation for  pixel format"""

from ..image.color_format import *
from ..image.image import *
from .common import AbstractParser

import numpy
import cv2 as cv
import math


class ParserYUV420(AbstractParser):
    """A semi-planar YUV420 implementation of a parser"""
    def parse(self, raw_data, color_format, width, height=None):
        """Parses provided raw data to an image, calculating height from provided width.

        Keyword arguments:

            raw_data: bytes object
            color_format: target instance of ColorFormat
            width: target width to interpret
            height: (deprecated) target height to interpret, default: None

        Returns: instance of Image processed to chosen format
        """

        max_value = max(color_format.bits_per_components)
        curr_dtype = numpy.uint8

        data_array = []
        if len(set(
                color_format.bits_per_components)) == 2 and max_value % 8 == 0:
            data_array = numpy.frombuffer(raw_data, dtype=curr_dtype)
        else:
            raise NotImplementedError(
                "Other than 8-bit YUVs are not currently supported")

        processed_data = numpy.array(data_array, dtype=curr_dtype)

        def normal_round(n):
            if n - math.floor(n) < 0.5:
                return int(math.floor(n))
            return int(math.ceil(n))

        if (processed_data.size % width != 0):
            processed_data = numpy.concatenate(
                (processed_data,
                 numpy.zeros(width - (processed_data.size % width))))

        new_height = normal_round(math.ceil(processed_data.size / width) / 1.5)
        return Image(raw_data, color_format, processed_data, width, new_height)

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

        data_array = numpy.reshape(
            return_data,
            (int(return_data.size / image.width), image.width)).astype('uint8')

        if (data_array.shape[0] % 3 != 0):
            data_array = numpy.concatenate(
                (data_array,
                 numpy.zeros(
                     (3 - (data_array.shape[0] % 3), data_array.shape[1]),
                     dtype=numpy.uint8)))
        if (data_array.shape[1] % 2 != 0):
            data_array = numpy.concatenate(
                (data_array,
                 numpy.zeros((data_array.shape[0], 1), dtype=numpy.uint8)),
                axis=1)

        return_data = cv.cvtColor(data_array, conversion_const)
        return return_data


class ParserYUV422(AbstractParser):
    """A packed YUV422 implementation of a parser"""
    def parse(self, raw_data, color_format, width, height=None):
        """Parses provided raw data to an image, calculating height from provided width.

        Keyword arguments:

            raw_data: bytes object
            color_format: target instance of ColorFormat
            width: target width to interpret
            height: (deprecated) target height to interpret, default: None

        Returns: instance of Image processed to chosen format
        """
        max_value = max(color_format.bits_per_components)
        curr_dtype = numpy.uint8

        data_array = []

        if len(set(
                color_format.bits_per_components)) == 1 and max_value % 8 == 0:
            data_array = numpy.frombuffer(raw_data, dtype=curr_dtype)
        else:
            raise NotImplementedError(
                "Other than 8-bit YUVs are not currently supported")

        processed_data = numpy.array(data_array, dtype=curr_dtype)

        if (processed_data.size % (width * 2) != 0):
            processed_data = numpy.concatenate(
                (processed_data,
                 numpy.zeros((width * 2) - (processed_data.size %
                                            (width * 2)))))

        return Image(raw_data, color_format, processed_data, width,
                     processed_data.size // (width * 2))

    def get_displayable(self, image):
        """Provides displayable image data (BGR formatted)

        Returns: Numpy array containing displayable data.
        """
        return_data = image.processed_data

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
