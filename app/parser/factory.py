"""Factory returning proper parser"""

from app.parser.bayer import ParserBayerRG
from ..image.color_format import (PixelPlane, PixelFormat)
from .rgb import ParserARGB, ParserRGBA
from .yuv import (ParserYUV420, ParserYUV422)
from .greyscale import ParserGreyscale


class ParserFactory:
    """Parser factory"""
    @staticmethod
    def create_object(color_format):
        """Get parser for provided color format.

        Keyword arguments:
            color_format: instance of ColorFormat

        Returns: instance of parser
        """
        mapping = {}
        if color_format.pixel_plane == PixelPlane.PACKED:
            mapping = {
                PixelFormat.BAYER_RG: ParserBayerRG,
                PixelFormat.MONO: ParserGreyscale,
                PixelFormat.RGBA: ParserRGBA,
                PixelFormat.BGRA: ParserRGBA,
                PixelFormat.ARGB: ParserARGB,
                PixelFormat.ABGR: ParserARGB,
                PixelFormat.YUYV: ParserYUV422,
                PixelFormat.UYVY: ParserYUV422,
                PixelFormat.VYUY: ParserYUV422,
                PixelFormat.YVYU: ParserYUV422
            }
        elif color_format.pixel_plane == PixelPlane.SEMIPLANAR:
            mapping = {
                PixelFormat.YUV: ParserYUV420,
                PixelFormat.YVU: ParserYUV420,
            }

        proper_class = mapping.get(color_format.pixel_format)
        if proper_class is None:
            raise NotImplementedError(
                "No parser found for {} color format".format(
                    color_format.name))
        return proper_class()
