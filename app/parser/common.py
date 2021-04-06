"""Support for parsing raw data."""

from abc import ABCMeta, abstractmethod
from ..image.image import Image
from ..image.color_format import (ColorFormat, PixelFormat, Endianness)
import numpy


def _calc_lcm(x, y):
    """Calculate least common multiply.

    Keyword arguments:
        x: first integer
        y: second integer

    Returns: Least common multiply of both integers.
    """
    if x > y:
        bigger = x
    else:
        bigger = y

    while True:
        if (bigger % x == 0) and (bigger % y == 0):
            lcm = bigger
            break
        bigger += 1

    return lcm


class AbstractParser(metaclass=ABCMeta):
    """An abstract data parser"""
    @abstractmethod
    def get_displayable(self):
        """Provides displayable image data (BGR formatted)

        Returns: Numpy array containing displayable data.
        """
        pass

    def parse(self, raw_data, color_format, width, height):
        """Parses provided raw data to an image.

        Keyword arguments:

            raw_data: bytes object
            color_format: target instance of ColorFormat
            width: target width to interpret
            height: target height to interpret

        Returns: instance of Image processed to chosen format
        """

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

        comp_bits = color_format.bits_per_components
        draft_data = bytearray(raw_data)
        step = int(_calc_lcm(sum(comp_bits), 8) / 8)

        if len(draft_data) % step != 0:
            draft_data += (0).to_bytes(len(raw_data) % step,
                                       byteorder="little")

        position = 0
        data_array = []
        while position < len(draft_data):
            current_bytes = draft_data[position:position + step]
            temp_number = int.from_bytes(
                current_bytes, "little" if color_format.endianness
                == Endianness.LITTLE_ENDIAN else "big")

            read_bits = 0
            while read_bits < step * 8:
                pixel_arr = []
                for i in range(3, -1, -1):
                    data = temp_number & (2**comp_bits[i] - 1)
                    pixel_arr.append(data)
                    temp_number >>= comp_bits[i]
                    read_bits += comp_bits[i]
                data_array += pixel_arr[::-1]
            position += step

        if len(data_array) < (width * height * 4):
            temp_arr = numpy.zeros(width * height * 4)
            temp_arr[0:len(data_array)] = data_array
            data_array = temp_arr
            processed_data = numpy.reshape(data_array, (height, width, 4))
        else:
            processed_data = numpy.reshape(
                numpy.array(data_array)[:width * height * 4],
                (height, width, 4))

        if comp_bits[3] == 0:
            processed_data[:, :, 3] = 255

        return Image(raw_data, color_format, processed_data)
