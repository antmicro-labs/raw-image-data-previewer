"""Support for abstract color formats."""

from enum import Enum

class PixelFormat(Enum):
    """Respresenation defining color hierachy in pixel."""

    RGBA = 1
    BGRA = 2
    CUSTOM = 0

class Endianness(Enum):
    """Represenation of color format endianness."""

    LITTLE_ENDIAN = 1
    BIG_ENDIAN = 2


class PixelPlane(Enum):
    """Representation of color format pixel plane."""

    PACKED = 1
    PLANAR = 2


class ColorFormat():
    """Representation of color format."""

    def __init__(self, name="unnamed", pixel_format, endianness, pixel_plane, bpc1, bpc2, bpc3, bpc4=0):
        self.name = name
        self.pixel_format = pixel_format
        self.endianness = endianness
        self.pixel_plane = pixel_plane
        self._bpcs = (bpc1, bpc2, bpc3, bpc4)

    @property
    def bits_per_components(self):
        return self._bpc

    @bits_per_components.setter
    def bits_per_components(self, bpcs):
        try:
            v1, v2, v3 = bpcs
        except ValueError:
            raise ValueError("Pass a iterable with four color components (default 0 for forth component)!")
        else:
            self._bpcs = bpcs

    def __str__(self):
        return name

RGB3_FORMAT = ColorFormat("RGB3", PixelFormat.RGBA, Endianness.BIG_ENDIAN, PixelPlane.PACKED, 8, 8, 8)
BGR3_FORMAT = ColorFormat("BGR3", PixelFormat.BGRA, Endianness.BIG_ENDIAN, PixelPlane.PACKED, 8, 8, 8)