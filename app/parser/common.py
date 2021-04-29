"""Support for parsing raw data."""

from abc import ABCMeta, abstractmethod
from ..image.image import Image
from ..image.color_format import (ColorFormat, PixelFormat, Endianness)
import numpy
import math


class AbstractParser(metaclass=ABCMeta):
    """An abstract data parser"""
    @abstractmethod
    def get_displayable(self, image):
        """Provides displayable image data (BGR formatted)
        
        Keyword arguments:

            image: processed image object

        Returns: Numpy array containing displayable data.
        """
        pass

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
        curr_dtype = None
        if max_value <= 8:
            curr_dtype = numpy.uint8
        elif max_value <= 16:
            curr_dtype = numpy.uint16
        elif max_value <= 32:
            curr_dtype = numpy.uint32
        else:
            curr_dtype = numpy.uint64

        data_array = []
        temp_set = set(color_format.bits_per_components)

        if (len(temp_set) == 1 or len(temp_set) == 2
                and not temp_set.add(0)) and max_value % 8 == 0:
            temp = numpy.frombuffer(raw_data, dtype=curr_dtype)
            data_array = temp
            if len(temp_set) == 2:
                if (temp.size % (width * 3) != 0):
                    temp = numpy.concatenate(
                        (temp,
                         numpy.zeros((width * 3) - (temp.size % (width * 3)))))
                temp = numpy.concatenate(
                    (numpy.reshape(temp,
                                   (int(temp.size / (width * 3)), width, 3)),
                     numpy.full((int(temp.size / (width * 3)), width, 1),
                                255,
                                dtype=curr_dtype)),
                    axis=2)
                data_array = numpy.reshape(temp, temp.size)
        else:
            data_array = self._parse_not_bytefilled(raw_data, color_format)

        processed_data = numpy.array(data_array, dtype=curr_dtype)
        if (processed_data.size % (width * 4) != 0):
            processed_data = numpy.concatenate(
                (processed_data,
                 numpy.zeros((width * 4) - (processed_data.size %
                                            (width * 4)))))
        print('costam {}'.format(processed_data.size / (width * 4)))
        return Image(raw_data, color_format, processed_data, width,
                     processed_data.size // (width * 4))

    def _parse_not_bytefilled(self, raw_data, color_format):
        """Parses provided raw data to an image - bits per component are not multiple of 8.

        Keyword arguments:

            raw_data: bytes object
            color_format: target instance of ColorFormat
            width: target width to interpret
            height: target height to interpret

        Returns: instance of Image processed to chosen format
        """

        comp_bits = color_format.bits_per_components
        draft_data = bytearray(raw_data)
        step = int(math.lcm(sum(comp_bits), 8) / 8)
        if len(draft_data) % step != 0:
            draft_data += (0).to_bytes(len(raw_data) % step,
                                       byteorder="little")
        position = 0
        data_array = []
        while position + step <= len(draft_data):

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

        return data_array