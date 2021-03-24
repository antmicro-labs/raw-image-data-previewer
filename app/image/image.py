"""Container for processed image."""

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