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
        curr_dtype = None
        if max_value <= 8:
            curr_dtype = numpy.int8
        elif max_value <= 16:
            curr_dtype = numpy.int16
        elif max_value <= 32:
            curr_dtype = numpy.int32
        else:
            curr_dtype = numpy.int64

        data_array = []
        try:
            if len(set(color_format.bits_per_components)
                   ) == 2 and max_value % 8 == 0:
                data_array = numpy.frombuffer(raw_data,
                                              dtype=curr_dtype,
                                              count=(int(height * width *
                                                         1.5)))
            else:
                data_array = self._parse_not_bytefilled(
                    raw_data, color_format, width, height)
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
        return_data = image.processed_data.astype('float64')

        return_data[0:(image.width * image.height)] = (
            255 * return_data[0:(image.width * image.height)]) / (
                2**image.color_format.bits_per_components[0] - 1)
        return_data[(image.width * image.height):2:] = (255 * return_data[
            (image.width * image.height):2:]) / (
                2**image.color_format.bits_per_components[1] - 1)
        return_data[(image.width * image.height) + 1:2:] = (255 * return_data[
            (image.width * image.height) + 1:2:]) / (
                2**image.color_format.bits_per_components[2] - 1)

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

    def _parse_not_bytefilled(self, raw_data, color_format, width, height):
        """Parses provided raw data to an image - bits per component are not multiple of 8.

        Keyword arguments:

            raw_data: bytes object
            color_format: target instance of ColorFormat
            width: target width to interpret
            height: target height to interpret

        Returns: instance of Image processed to chosen format
        Throws: ValueError if can't construct image of provided width and height from raw_data
        """

        comp_bits = color_format.bits_per_components
        draft_data = bytearray(raw_data)
        step = int(math.lcm(comp_bits[0], 8) / 8)

        if len(draft_data) % step != 0:
            draft_data += (0).to_bytes(len(raw_data) % step,
                                       byteorder="little")
        position = 0
        data_array = []
        while len(data_array) < (width * height):

            if position >= len(draft_data):
                raise ValueError()

            current_bytes = draft_data[position:position + step]
            temp_number = int.from_bytes(
                current_bytes, "little" if color_format.endianness
                == Endianness.LITTLE_ENDIAN else "big")

            read_bits = 0
            temp_data = []
            while read_bits < step * 8:
                temp_data.append(temp_number & (2**comp_bits[0] - 1))
                temp_number >>= comp_bits[0]
                read_bits += comp_bits[0]
            data_array += temp_data[::-1]
            position += step

        step = int(math.lcm(comp_bits[0] + comp_bits[1], 8) / 8)
        while len(data_array) < (width * height * 1.5):

            if position >= len(draft_data):
                raise ValueError()

            current_bytes = draft_data[position:position + step]
            temp_number = int.from_bytes(
                current_bytes, "little" if color_format.endianness
                == Endianness.LITTLE_ENDIAN else "big")

            read_bits = 0
            temp_data = []
            while read_bits < step * 8:
                for i in range(1, 3):
                    temp_data.append(temp_number & (2**comp_bits[i] - 1))
                    temp_number >>= comp_bits[i]
                    read_bits += comp_bits[i]
            data_array += temp_data[::-1]
            position += step

        return data_array


class ParserYUV422(AbstractParser):
    """A packed YUV422 implementation of a parser"""
    def parse(self, raw_data, color_format, width, height):
        image = None
        try:
            image = super().parse(raw_data, color_format, int(width / 2),
                                  height)
            image.width = width
        except ValueError:
            raise ValueError(
                "Not enough values in buffer to construct image of resolution {} x {}"
                .format(width, height))

        return image

    def get_displayable(self, image):
        """Provides displayable image data (BGR formatted)

        Returns: Numpy array containing displayable data.
        """
        return_data = numpy.reshape(image.processed_data.astype('float64'),
                                    (image.height, int(image.width / 2), 4))

        for i in range(4):
            return_data[:, :, i] = (255 * return_data[:, :, i]) / (
                2**image.color_format.bits_per_components[i] - 1)

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
