"""Factory returning proper parser"""

from ..image.color_format import (PixelFormat, ColorFormat)
from .bgra import ParserBGRA
from .rgba import ParserRGBA


class ParserFactory:
    """Parser factory"""
    @staticmethod
    def create_object(color_format):
        """Get parser for provided color format.

        Keyword arguments:
            color_format: instance of ColorFormat

        Returns: instance of parser
        """

        mapping = {PixelFormat.RGBA: ParserRGBA, PixelFormat.BGRA: ParserBGRA}

        proper_class = mapping.get(color_format.pixel_format)
        return proper_class()
