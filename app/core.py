"""Main functionalities."""

from .image.image import (Image, RawDataContainer)
from .image.color_format import (RGB3_FORMAT, BGR3_FORMAT)
from .parser.factory import ParserFactory


def run_core_functionality(args):

    image = create_Image(args)
    parser = ParserFactory.create_object(
        determine_color_format(args["color_format"]))

    image = parser.parse(image.data_buffer,
                         determine_color_format(args["color_format"]),
                         args["resolution"][0], args["resolution"][1])
    displayable_data = parser.get_displayable(image)


def create_Image(args):

    raw_data = RawDataContainer.from_file(args["FILE_PATH"])
    return Image(raw_data.data_buffer)


def determine_color_format(format_string):

    if format_string == "RGB3":
        return RGB3_FORMAT
    elif format_string == "BGR3":
        return BGR3_FORMAT
    else:
        raise NotImplementedError
