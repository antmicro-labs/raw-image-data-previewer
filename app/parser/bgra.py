"""Parser implementation for BGRA pixel format"""

from .common import AbstractParser


class ParserBGRA(AbstractParser):
    """An BGRA implementation of a parser"""
    def get_displayable(self, image):
        """Provides displayable image data (BGR formatted)

        Returns: Numpy array containing displayable data.
        """
        return_data = image.processed_data.astype('float64')

        if (image.color_format.bits_per_components[3] == 0):
            bpcs = 3
        else:
            bpcs = 4

        for i in range(bpcs):
            return_data[:, :, i] = (255 * return_data[:, :, i]) / (
                2**image.color_format.bits_per_components[i] - 1)

        return return_data.astype('uint8')
