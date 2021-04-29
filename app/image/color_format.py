"""Support for abstract color formats."""

from enum import Enum


class PixelFormat(Enum):
    """Respresenation defining color hierachy in pixel."""

    RGBA = 1
    BGRA = 2
    YUYV = 3
    UYVY = 4
    YUV = 5
    YVU = 6
    CUSTOM = 0


class Endianness(Enum):
    """Represenation of color format endianness."""

    LITTLE_ENDIAN = 1
    BIG_ENDIAN = 2


class PixelPlane(Enum):
    """Representation of color format pixel plane."""

    PACKED = 1
    PLANAR = 2
    SEMIPLANAR = 3


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
        return self.name


AVAILABLE_FORMATS = {
    'RGB24':
    ColorFormat(PixelFormat.RGBA,
                Endianness.BIG_ENDIAN,
                PixelPlane.PACKED,
                8,
                8,
                8,
                name="RGB24"),
    'BGR24':
    ColorFormat(PixelFormat.BGRA,
                Endianness.BIG_ENDIAN,
                PixelPlane.PACKED,
                8,
                8,
                8,
                name="BGR24"),
    'RGB32':
    ColorFormat(PixelFormat.RGBA,
                Endianness.BIG_ENDIAN,
                PixelPlane.PACKED,
                8,
                8,
                8,
                8,
                name="RGB32"),
    'RGB332':
    ColorFormat(PixelFormat.RGBA,
                Endianness.LITTLE_ENDIAN,
                PixelPlane.PACKED,
                3,
                3,
                2,
                name="RGB332"),
    'RGB565':
    ColorFormat(PixelFormat.RGBA,
                Endianness.LITTLE_ENDIAN,
                PixelPlane.PACKED,
                5,
                6,
                5,
                name="RGB565"),
    'YUY2':
    ColorFormat(PixelFormat.YUYV,
                Endianness.BIG_ENDIAN,
                PixelPlane.PACKED,
                8,
                8,
                8,
                bpc4=8,
                name="YUY2"),
    'UYVY':
    ColorFormat(PixelFormat.UYVY,
                Endianness.BIG_ENDIAN,
                PixelPlane.PACKED,
                8,
                8,
                8,
                bpc4=8,
                name="UYVY"),
    'NV12':
    ColorFormat(PixelFormat.YUV,
                Endianness.BIG_ENDIAN,
                PixelPlane.SEMIPLANAR,
                8,
                8,
                8,
                name="NV12"),
    'NV21':
    ColorFormat(PixelFormat.YVU,
                Endianness.BIG_ENDIAN,
                PixelPlane.SEMIPLANAR,
                8,
                8,
                8,
                name="NV21"),
}
