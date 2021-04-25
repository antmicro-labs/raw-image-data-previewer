import unittest
import numpy
import os
from unittest.mock import (Mock, patch)
from app.parser.rgb import ParserRGBA
from enum import Enum


class DummyPixelFormat(Enum):
    RGBA = 1
    BGRA = 2


class DummyEndianness(Enum):
    LITTLE_ENDIAN = 1
    BIG_ENDIAN = 2


class DummyPixelPlane(Enum):
    PACKED = 1


class TestRGBParserClass(unittest.TestCase):
    def setUp(self):

        self.RGB565_FORMAT = Mock(pixel_format=DummyPixelFormat.RGBA,
                                  endianness=DummyEndianness.LITTLE_ENDIAN,
                                  pixel_plane=DummyPixelPlane.PACKED)
        self.RGB565_FORMAT.bits_per_components = (5, 6, 5, 0)

        self.BGR32_FORMAT = Mock(pixel_format=DummyPixelFormat.BGRA,
                                 endianness=DummyEndianness.BIG_ENDIAN,
                                 pixel_plane=DummyPixelPlane.PACKED)
        self.BGR32_FORMAT.bits_per_components = (8, 8, 8, 8)

        self.RGB565_IMAGE = Mock(color_format=self.RGB565_FORMAT,
                                 width=2,
                                 height=1)
        self.RGB565_IMAGE.processed_data = numpy.array(
            [0, 0, 0, 0, 31, 63, 31, 0])

        self.raw_data = bytes((0, 0, 255, 255))

        self.RGB565_IMAGE.data_buffer = self.raw_data

        self.BGR32_IMAGE = Mock(color_format=self.BGR32_FORMAT,
                                width=1,
                                height=1)
        self.BGR32_IMAGE.processed_data = numpy.array([0, 0, 255, 255])
        self.BGR32_IMAGE.data_buffer = self.raw_data

        self.parser = ParserRGBA()

    @patch("app.parser.rgb.PixelFormat", DummyPixelFormat)
    @patch("app.parser.rgb.Endianness", DummyEndianness)
    @patch("app.parser.rgb.PixelPlane", DummyPixelPlane)
    def test_parse(self):

        parsed_img = self.parser.parse(self.raw_data, self.RGB565_FORMAT, 2, 1)

        self.assertEqual(parsed_img.data_buffer, self.RGB565_IMAGE.data_buffer)
        self.assertEqual(parsed_img.width, self.RGB565_IMAGE.width)
        self.assertEqual(parsed_img.height, self.RGB565_IMAGE.height)
        self.assertEqual(parsed_img.color_format,
                         self.RGB565_IMAGE.color_format)
        self.assertTrue(
            (parsed_img.processed_data == self.RGB565_IMAGE.processed_data
             ).all())

        parsed_img = self.parser.parse(self.raw_data, self.BGR32_FORMAT, 1, 1)

        self.assertEqual(parsed_img.data_buffer, self.BGR32_IMAGE.data_buffer)
        self.assertEqual(parsed_img.width, self.BGR32_IMAGE.width)
        self.assertEqual(parsed_img.height, self.BGR32_IMAGE.height)
        self.assertEqual(parsed_img.color_format,
                         self.BGR32_IMAGE.color_format)

        self.assertTrue(
            (parsed_img.processed_data == self.BGR32_IMAGE.processed_data
             ).all())

        with self.assertRaises(ValueError):
            self.parser.parse(self.raw_data, self.RGB565_FORMAT, 2, 2)

    @patch("app.parser.rgb.PixelFormat", DummyPixelFormat)
    @patch("app.parser.rgb.Endianness", DummyEndianness)
    @patch("app.parser.rgb.PixelPlane", DummyPixelPlane)
    def test_get_displayable(self):

        displayable = self.parser.get_displayable(self.RGB565_IMAGE)
        self.assertEqual(
            displayable.shape,
            (self.RGB565_IMAGE.height, self.RGB565_IMAGE.width, 4))

        self.assertTrue((displayable == numpy.array([[[0, 0, 0, 0],
                                                      [255, 255, 255,
                                                       0]]])).all())

        displayable = self.parser.get_displayable(self.BGR32_IMAGE)
        self.assertEqual(displayable.shape,
                         (self.BGR32_IMAGE.height, self.BGR32_IMAGE.width, 4))

        self.assertTrue((displayable == numpy.array([[[0, 0, 255,
                                                       255]]])).all())


if __name__ == "__main__":
    unittest.main()