#!/usr/bin/env python
import cv2 as cv
"""Raw image data previewer - terminal functionality."""

import argparse
import os
from .core import (load_image, get_displayable)
from .image.color_format import AVAILABLE_FORMATS
from .gui import MainWindow

parser = argparse.ArgumentParser(
    prog=__package__,
    description="preview raw data as an image of chosen format")
parser.add_argument("-f",
                    "--FILE_PATH",
                    help="file containing raw image data",
                    default=None)
parser.add_argument("-c",
                    "--color_format",
                    choices=AVAILABLE_FORMATS.keys(),
                    default=list(AVAILABLE_FORMATS.keys())[0],
                    help="target color format (default: %(default)s)")
parser.add_argument("-w",
                    "--width",
                    metavar=("width"),
                    type=int,
                    nargs=1,
                    default=600,
                    help="target width (default: %(default)s)")

args = vars(parser.parse_args())

if isinstance(args["FILE_PATH"], str):
    if not os.path.isfile(args["FILE_PATH"]):
        raise Exception("Given path does not lead to a file")

#img = load_image(args["FILE_PATH"], args["color_format"], args["resolution"])
app = MainWindow(args)
app.mainloop()
"""
cv.imshow(args["FILE_PATH"], get_displayable(img))
cv.waitKey(0)
cv.destroyAllWindows()
"""
