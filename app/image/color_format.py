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
    def __init__(self,
                 pixel_format,
                 endianness,
                 pixel_plane,
                 bpc1,
                 bpc2,
                 bpc3,
                 bpc4=0,
                 name="unnamed"):
        self.name = name
        self.pixel_format = pixel_format
        self.endianness = endianness
        self.pixel_plane = pixel_plane
        self._bpcs = (bpc1, bpc2, bpc3, bpc4)

    @property
    def bits_per_components(self):
        return self._bpcs

    @bits_per_components.setter
    def bits_per_components(self, bpcs):

        if isinstance(bpcs, (list, tuple)):
            if len(bpcs) == 3:
                self._bpcs = (tuple(bpcs) + (0, ))
                return
            elif len(bpcs) == 4:
                self._bpcs = tuple(bpcs)
                return

        raise ValueError(
            "Provided value should be an iterable of 3 or 4 values!")

    def __str__(self):
        return name


RGB3_FORMAT = ColorFormat(PixelFormat.RGBA,
                          Endianness.BIG_ENDIAN,
                          PixelPlane.PACKED,
                          8,
                          8,
                          8,
                          name="RGB3")
BGR3_FORMAT = ColorFormat(PixelFormat.BGRA,
                          Endianness.BIG_ENDIAN,
                          PixelPlane.PACKED,
                          8,
                          8,
                          8,
                          name="BGR3")
