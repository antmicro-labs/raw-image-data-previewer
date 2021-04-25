import unittest
import numpy
import os
from unittest.mock import (Mock, patch)
from app.parser.yuv import ParserYUV420, ParserYUV422
from enum import Enum


class DummyPixelFormat(Enum):
    YUV = 1
    YVU = 2
    UYVY = 3
    YUYV = 4


class DummyEndianness(Enum):
    LITTLE_ENDIAN = 1
    BIG_ENDIAN = 2


class DummyPixelPlane(Enum):
    PACKED = 1
    SEMIPLANAR = 2


class TestParserClass(unittest.TestCase):
    def setUp(self):

        #YUV420 Parser
        self.Y420_FORMAT = Mock(pixel_format=DummyPixelFormat.YUV,
                                endianness=DummyEndianness.BIG_ENDIAN,
                                pixel_plane=DummyPixelPlane.SEMIPLANAR)
        self.Y420_FORMAT.bits_per_components = (8, 8, 8, 0)
        self.Y420_IMAGE = Mock(color_format=self.Y420_FORMAT,
                               width=2,
                               height=2)
        self.Y420_IMAGE.processed_data = numpy.array([255, 255, 0, 0, 255, 0])
        self.raw_data_Y420 = bytes((255, 255, 0, 0, 255, 0))
        self.Y420_IMAGE.data_buffer = self.raw_data_Y420

        self.parserY420 = ParserYUV420()

        #YUV422 Parser
        self.Y422_FORMAT = Mock(pixel_format=DummyPixelFormat.UYVY,
                                endianness=DummyEndianness.BIG_ENDIAN,
                                pixel_plane=DummyPixelPlane.PACKED)
        self.Y422_FORMAT.bits_per_components = (8, 8, 8, 8)

        self.Y422_IMAGE = Mock(color_format=self.Y422_FORMAT,
                               width=2,
                               height=2)
        self.Y422_IMAGE.processed_data = numpy.array(
            [255, 255, 0, 255, 0, 0, 255, 0])
        self.raw_data_Y422 = bytes((255, 255, 0, 255, 0, 0, 255, 0))
        self.Y422_IMAGE.data_buffer = self.raw_data_Y422

        self.parserY422 = ParserYUV422()

    @patch("app.parser.yuv.PixelFormat", DummyPixelFormat)
    @patch("app.parser.yuv.Endianness", DummyEndianness)
    @patch("app.parser.yuv.PixelPlane", DummyPixelPlane)
    def test_parse_Y420(self):

        parsed_img = self.parserY420.parse(self.raw_data_Y420,
                                           self.Y420_FORMAT, 2, 2)

        self.assertEqual(parsed_img.data_buffer, self.Y420_IMAGE.data_buffer)
        self.assertEqual(parsed_img.width, self.Y420_IMAGE.width)
        self.assertEqual(parsed_img.height, self.Y420_IMAGE.height)
        self.assertEqual(parsed_img.color_format, self.Y420_IMAGE.color_format)
        self.assertTrue((
            parsed_img.processed_data == self.Y420_IMAGE.processed_data).all())

        parsed_img = self.parserY420.parse(self.raw_data_Y420,
                                           self.Y420_FORMAT, 2, 2)

        with self.assertRaises(ValueError):
            self.parserY420.parse(self.raw_data_Y420, self.Y420_FORMAT, 4, 4)

    @patch("app.parser.yuv.PixelFormat", DummyPixelFormat)
    @patch("app.parser.yuv.Endianness", DummyEndianness)
    @patch("app.parser.yuv.PixelPlane", DummyPixelPlane)
    def test_parse_Y422(self):
        parsed_img = self.parserY422.parse(self.raw_data_Y422,
                                           self.Y422_FORMAT, 2, 2)

        self.assertEqual(parsed_img.data_buffer, self.Y422_IMAGE.data_buffer)
        self.assertEqual(parsed_img.width, self.Y422_IMAGE.width)
        self.assertEqual(parsed_img.height, self.Y422_IMAGE.height)
        self.assertEqual(parsed_img.color_format, self.Y422_IMAGE.color_format)
        self.assertTrue((
            parsed_img.processed_data == self.Y422_IMAGE.processed_data).all())

        with self.assertRaises(ValueError):
            self.parserY422.parse(self.raw_data_Y422, self.Y422_FORMAT, 4, 4)

    @patch("app.parser.yuv.PixelFormat", DummyPixelFormat)
    @patch("app.parser.yuv.Endianness", DummyEndianness)
    @patch("app.parser.yuv.PixelPlane", DummyPixelPlane)
    def test_get_displayable_Y420(self):

        displayable = self.parserY420.get_displayable(self.Y420_IMAGE)
        self.assertEqual(displayable.shape,
                         (self.Y420_IMAGE.height, self.Y420_IMAGE.width, 3))
        self.assertTrue((displayable == numpy.array([[[255, 255, 74],
                                                      [255, 255, 74]],
                                                     [[255, 54, 0],
                                                      [255, 54, 0]]])).all())

    @patch("app.parser.yuv.PixelFormat", DummyPixelFormat)
    @patch("app.parser.yuv.Endianness", DummyEndianness)
    @patch("app.parser.yuv.PixelPlane", DummyPixelPlane)
    def test_get_displayable_Y422(self):

        displayable = self.parserY422.get_displayable(self.Y422_IMAGE)
        self.assertEqual(displayable.shape,
                         (self.Y422_IMAGE.height, self.Y422_IMAGE.width, 3))
        self.assertTrue((displayable == numpy.array([[[255, 255, 74],
                                                      [255, 255, 74]],
                                                     [[0, 0, 203],
                                                      [0, 0, 203]]])).all())


if __name__ == "__main__":
    unittest.main()