"""Main functionalities."""

import app.image.image as image
import app.image.color_format as color_format
import app.parser.factory as factory


def run_core_functionality(args):

    image = create_Image(args)
    parser = factory.ParserFactory.create_object(
        determine_color_format(args["color_format"]))

    if args["parse"] == True:
        image = parser.parse(image.data_buffer,
                             determine_color_format(args["color_format"]),
                             args["resolution"][0], args["resolution"][1])
        if args["display"] == True:
            displayable_data = parser.get_displayable(image)


def create_Image(args):

    raw_data = image.RawDataContainer(None).from_file(args["FILE_PATH"])
    return image.Image(raw_data.data_buffer)


def determine_color_format(format_string):

    if format_string == "RGB3":
        return color_format.ColorFormat(color_format.PixelFormat.RGBA,
                                        color_format.Endianness.BIG_ENDIAN,
                                        color_format.PixelPlane.PACKED,
                                        8,
                                        8,
                                        8,
                                        name="RGB3")
    elif format_string == "BGR3":
        return color_format.ColorFormat(color_format.PixelFormat.BGRA,
                                        color_format.Endianness.BIG_ENDIAN,
                                        color_format.PixelPlane.PACKED,
                                        8,
                                        8,
                                        8,
                                        name="BGR3")
    else:
        raise NotImplementedError
