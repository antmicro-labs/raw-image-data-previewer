#!/usr/bin/env python
"""Raw image data previewer - terminal functionality."""

import argparse
import os
from .core import run_core_functionality

parser = argparse.ArgumentParser(
    prog=__package__,
    description="preview raw data as an image of chosen format")
parser.add_argument("FILE_PATH", help="file containing raw image data")
parser.add_argument("-c",
                    "--color_format",
                    choices=["RGB3", "BGR3"],
                    default="RGB3",
                    help="target color format (default: %(default)s)")
parser.add_argument("-r",
                    "--resolution",
                    metavar=("width", "height"),
                    type=int,
                    nargs=2,
                    default=[600, 600],
                    help="target resolution (default: %(default)s)")

args = vars(parser.parse_args())

if not os.path.isfile(args["FILE_PATH"]):
    raise Exception("Given path does not lead to a file")

run_core_functionality(args)
