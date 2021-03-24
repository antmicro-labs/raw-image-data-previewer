"""Support for containing image."""

import numpy

class RawDataContainer:
    """Structure for file data and communication."""

    def __init__(self, data_buffer):
        self.data_buffer =  data_buffer

    @classmethod
    def from_file(cls, file_path):

        data_buffer = ""

        try:
            with open(file_path, 'rb') as file:
                data_buffer = file.read()
                return cls(data_buffer)
        
        except EnvironmentError as err:
            raise Exception('Error occured while trying to read from file {}'.format(file_path))


class Image(RawDataContainer):
    """Container for image data."""

    def __init__(self, data_buffer, color_format=None, processed_data=None):
        RawDataContainer.__init__(self,data_buffer=data_buffer)
        self.color_format = color_format
        self.processed_data = processed_data


    @property
    def height(self):
        if(self.processed_data == None):
            return None
        return self.processed_data.shape()[0]

    @property
    def width(self):
        if(self.processed_data == None):
            return None
        return self.processed_data.shape()[1]