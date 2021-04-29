"""Support for containing image."""

import numpy


class RawDataContainer:
    """Structure for file data and communication."""
    def __init__(self, data_buffer):
        self.data_buffer = data_buffer

    @classmethod
    def from_file(cls, file_path):

        data_buffer = None

        try:
            with open(file_path, "rb") as file:
                data_buffer = file.read()
                return cls(data_buffer)

        except EnvironmentError as err:
            raise Exception(
                "Error occured while trying to read from file {}.\nReason: {}".
                format(file_path, err))


class Image(RawDataContainer):
    """Container for image data."""
    def __init__(self,
                 data_buffer,
                 color_format=None,
                 processed_data=None,
                 width=None,
                 height=None):
        """Constructs Image instance.

        Keyword arguments:

            data_buffer: bytes object
            color_format: instance of ColorFormat
            processed_data: numpy array
            width: image width
            height: image height
        """
        RawDataContainer.__init__(self, data_buffer=data_buffer)
        self.color_format = color_format
        self.processed_data = processed_data
        self.width = width
        self.height = height
