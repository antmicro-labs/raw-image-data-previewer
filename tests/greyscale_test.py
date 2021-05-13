from app.parser.greyscale import ParserGreyscale
import unittest
import numpy
from unittest.mock import (Mock, patch)
from enum import Enum


class DummyPixelFormat(Enum):
    MONO = 1


class DummyEndianness(Enum):
    LITTLE_ENDIAN = 1
    BIG_ENDIAN = 2


class DummyPixelPlane(Enum):
    PACKED = 1


class TestGreyscaleParserClass(unittest.TestCase):
    def setUp(self):

        self.GREY_FORMAT = Mock(pixel_format=DummyPixelFormat.MONO,
                                endianness=DummyEndianness.BIG_ENDIAN,
                                pixel_plane=DummyPixelPlane.PACKED)
        self.GREY_FORMAT.bits_per_components = (8, 0, 0, 0)

        self.GREY12_FORMAT = Mock(pixel_format=DummyPixelFormat.MONO,
                                  endianness=DummyEndianness.BIG_ENDIAN,
                                  pixel_plane=DummyPixelPlane.PACKED)
        self.GREY12_FORMAT.bits_per_components = (12, 0, 0, 0)

        self.GREY_IMAGE = Mock(color_format=self.GREY_FORMAT,
                               width=2,
                               height=1)
        self.GREY_IMAGE.processed_data = numpy.array([0, 255])

        self.raw_data = bytes((0, 255))

        self.GREY_IMAGE.data_buffer = self.raw_data

        self.GREY12_IMAGE = Mock(color_format=self.GREY12_FORMAT,
                                 width=1,
                                 height=1)
        self.GREY12_IMAGE.processed_data = numpy.array([255])
        self.GREY12_IMAGE.data_buffer = self.raw_data

        self.parser = ParserGreyscale()

    def test_parse(self):

        parsed_img = self.parser.parse(self.raw_data, self.GREY_FORMAT, 2)

        self.assertEqual(parsed_img.data_buffer, self.GREY_IMAGE.data_buffer)
        self.assertEqual(parsed_img.width, self.GREY_IMAGE.width)
        self.assertEqual(parsed_img.height, self.GREY_IMAGE.height)
        self.assertEqual(parsed_img.color_format, self.GREY_IMAGE.color_format)
        self.assertTrue((
            parsed_img.processed_data == self.GREY_IMAGE.processed_data).all())

        parsed_img = self.parser.parse(self.raw_data, self.GREY12_FORMAT, 1)

        self.assertEqual(parsed_img.data_buffer, self.GREY12_IMAGE.data_buffer)
        self.assertEqual(parsed_img.width, self.GREY12_IMAGE.width)
        self.assertEqual(parsed_img.height, self.GREY12_IMAGE.height)
        self.assertEqual(parsed_img.color_format,
                         self.GREY12_IMAGE.color_format)

        self.assertTrue(
            (parsed_img.processed_data == self.GREY12_IMAGE.processed_data
             ).all())

    def test_get_displayable(self):

        displayable = self.parser.get_displayable(self.GREY_IMAGE)
        self.assertEqual(displayable.shape,
                         (self.GREY_IMAGE.height, self.GREY_IMAGE.width, 3))

        self.assertTrue(
            (displayable == numpy.array([[[0, 0, 0], [255, 255, 255]]])).all())

        displayable = self.parser.get_displayable(self.GREY12_IMAGE)
        self.assertEqual(
            displayable.shape,
            (self.GREY12_IMAGE.height, self.GREY12_IMAGE.width, 3))
        self.assertTrue((displayable == numpy.array([[[15, 15, 15]]])).all())