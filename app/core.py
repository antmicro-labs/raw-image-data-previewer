"""Main functionalities."""

from .image.image import (Image, RawDataContainer)
from .image.color_format import AVAILABLE_FORMATS
from .parser.factory import ParserFactory


def load_image(file_path, color_format, resolution):

    image = Image.from_file(file_path)
    parser = ParserFactory.create_object(determine_color_format(color_format))

    image = parser.parse(image.data_buffer,
                         determine_color_format(color_format), resolution[0],
                         resolution[1])

    return image


def get_displayable(image):

    if image.color_format is None:
        raise Exception()
    parser = ParserFactory.create_object(image.color_format)

    return parser.get_displayable(image)


def determine_color_format(format_string):

    if format_string in AVAILABLE_FORMATS.keys():
        return AVAILABLE_FORMATS[format_string]
    else:
        raise NotImplementedError()
