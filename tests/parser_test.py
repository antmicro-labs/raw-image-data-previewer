import unittest
import numpy
import os
from app.image.image import Image
from app.image.color_format import (ColorFormat, PixelFormat, PixelPlane,
                                    Endianness)
from app.parser.factory import ParserFactory
from app.parser.rgba import AbstractParser


class TestParserClass(unittest.TestCase):
    def setUp(self):
        self.RGB565_FORMAT = ColorFormat(PixelFormat.RGBA,
                                         Endianness.LITTLE_ENDIAN,
                                         PixelPlane.PACKED,
                                         5,
                                         6,
                                         5,
                                         name="RGB565")

        self.RGB332_FORMAT = ColorFormat(PixelFormat.RGBA,
                                         Endianness.LITTLE_ENDIAN,
                                         PixelPlane.PACKED,
                                         3,
                                         3,
                                         2,
                                         name="RGB332")

        self.BGR332_FORMAT = ColorFormat(PixelFormat.BGRA,
                                         Endianness.LITTLE_ENDIAN,
                                         PixelPlane.PACKED,
                                         3,
                                         3,
                                         2,
                                         name="BGR332")

        self.TEST_FILE_RGB = os.path.join(os.path.dirname(__file__),
                                          "resources/RGB565_643_636")
        self.TEST_FILE_RGB2 = os.path.join(os.path.dirname(__file__),
                                           "resources/RGB332_643_636")
        self.test_image = Image.from_file(self.TEST_FILE_RGB)
        self.test_image2 = Image.from_file(self.TEST_FILE_RGB2)
        self.parser = ParserFactory.create_object(self.RGB565_FORMAT)
        self.BGRParser = ParserFactory.create_object(self.BGR332_FORMAT)

    def test_parse(self):
        new_image = self.parser.parse(self.test_image.data_buffer,
                                      self.RGB565_FORMAT, 643, 636)
        self.assertEqual(new_image.data_buffer, self.test_image.data_buffer)
        self.assertEqual(new_image.width, 643)
        self.assertEqual(new_image.height, 636)
        self.assertEqual(new_image.color_format, self.RGB565_FORMAT)

        one_pixel = self.parser.parse(((0xF6).to_bytes(2, "little")),
                                      self.RGB332_FORMAT, 1, 1)
        self.assertTrue(
            (one_pixel.processed_data == numpy.array([[[7, 5, 2,
                                                        255]]])).all())

    def test_get_displayable(self):
        new_image = self.parser.parse(self.test_image2.data_buffer,
                                      self.RGB332_FORMAT, 643, 636)
        displayable = self.parser.get_displayable(new_image)
        self.assertEqual(displayable.shape,
                         (new_image.height, new_image.width, 4))
        self.assertTrue((displayable < 256).all())

        one_pixel = self.BGRParser.parse(((0xF6).to_bytes(2, "little")),
                                         self.BGR332_FORMAT, 1, 1)
        displayable = self.BGRParser.get_displayable(one_pixel)
        print(displayable)
        self.assertTrue((displayable == numpy.array([[[255, 182, 170,
                                                       255]]])).all())


if __name__ == "__main__":
    unittest.main()
